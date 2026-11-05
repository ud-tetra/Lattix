import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lattix import Store, digest, write_json
from governance import resolve_profile, receipt_check, protocol_check, validate_program


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_json(self.root / 'config/contributors.json', {'schema_version': 1, 'contributors': [
            {'id': 'alice', 'github': 'alice', 'roles': ['researcher']},
            {'id': 'bob', 'github': 'bob', 'roles': ['integrator', 'reviewer']}]})
        self.store = Store(self.root)
        self.store.bootstrap('test only', 'task', 'synthetic governance checks', 'session', actor='alice')
        self.protocol = {'record_type': 'preregistration', 'schema_version': 1, 'protocol_id': 'p',
                         'lane': 'C12A', 'status': 'frozen', 'workload': 'synthetic fixture',
                         'acceptance_rule': 'no product claim', 'exclusions': 'none', 'timing_scope': 'test',
                         'repetitions': '1', 'source_refs': ['synthetic'], 'target_exposure': 'TEST_ONLY'}
        self.proto_path = self.root / 'benchmarks/preregistrations/p.json'
        write_json(self.proto_path, self.protocol)
        result = self.root / 'raw.json'
        result.write_text('{"fixture":true}')
        self.folder = self.store.capture('session', 'run', 'OPEN', 'synthetic fixture, not benchmark evidence',
                                         'test', [self.proto_path], [result])
        self.receipt = {'record_type': 'benchmark_receipt', 'schema_version': 1, 'receipt_id': 'r',
            'session_id': 'session', 'lane': 'C12A', 'status': 'PASS',
            'execution': {'mode': 'CPU_REFERENCE', 'source_revision': 'a'*40, 'device': 'synthetic CPU',
                          'software': 'test', 'timing_method': 'synthetic', 'synchronization': 'serial'},
            'protocol': {'path': 'benchmarks/preregistrations/p.json', 'sha256': digest(self.proto_path),
                         'preregistration_revision': 'b'*40},
            'artifact_manifest': 'artifacts/session/run/manifest.json',
            'determinism_scope': 'synthetic fixture only',
            'metrics': [{'name': 'fixture count', 'unit': 'items', 'value': 1}],
            'limitations': ['No actual benchmark executed'], 'quality_gates': [], 'transfer': None}

    def tearDown(self):
        self.tmp.cleanup()

    def lane(self, lane):
        self.receipt['lane'] = lane
        self.protocol['lane'] = lane
        write_json(self.proto_path, self.protocol)
        self.receipt['protocol']['sha256'] = digest(self.proto_path)

    def test_distinct_roles_and_unknown_identity_rejected(self):
        self.assertEqual(resolve_profile(self.root, 'bob', 'integrator')['actor'], 'bob')
        for actor, role in [('alice', 'integrator'), ('unknown', 'researcher'), (None, 'researcher')]:
            with self.assertRaises(ValueError):
                resolve_profile(self.root, actor, role)

    def test_profile_persisted_and_local_profile_resolves(self):
        self.assertEqual(self.store.session('session')['profile']['actor'], 'alice')
        write_json(self.root/'config/runtime.local.json', {'actor':'bob','role':'reviewer','model':'unknown'})
        self.assertEqual(resolve_profile(self.root)['role'], 'reviewer')
        self.assertEqual(validate_program(self.root), [])

    def test_invalid_session_profile_rejected(self):
        p=self.store.session_path('session');obj=json.loads(p.read_text());obj['profile']['role']='maintainer';write_json(p,obj)
        self.assertTrue(validate_program(self.root))

    def test_valid_structural_receipt_is_not_empirical_certification(self):
        receipt_check(self.root, self.receipt)

    def test_not_run_cannot_report_measured_metrics(self):
        self.receipt['status']='NOT_RUN';self.receipt['execution']['mode']='NOT_RUN'
        with self.assertRaisesRegex(ValueError, 'measured metrics'): receipt_check(self.root,self.receipt)
        self.receipt['metrics']=[];receipt_check(self.root,self.receipt)

    def test_protocol_tampering_and_lane_mismatch(self):
        self.proto_path.write_text(self.proto_path.read_text()+'\n')
        with self.assertRaisesRegex(ValueError,'digest'):receipt_check(self.root,self.receipt)
        self.receipt['protocol']['sha256']=digest(self.proto_path);self.receipt['lane']='C12B'
        with self.assertRaisesRegex(ValueError,'matching frozen'):receipt_check(self.root,self.receipt)

    def test_missing_hardware_metadata_or_bad_source_sha_rejected(self):
        self.receipt['execution']['mode']='WEBGPU_HARDWARE';self.receipt['execution']['device']=None
        with self.assertRaises(ValueError):receipt_check(self.root,self.receipt)
        self.receipt['execution']['device']='synthetic GPU';self.receipt['execution']['source_revision']='main'
        with self.assertRaisesRegex(ValueError,'commit SHA'):receipt_check(self.root,self.receipt)

    def test_solver_pass_cannot_hide_failed_quality_gate(self):
        self.lane('C12B')
        with self.assertRaisesRegex(ValueError,'quality gates'):receipt_check(self.root,self.receipt)
        self.receipt['quality_gates']=[{'name':'contact','rule':'synthetic','status':'FAIL'}]
        with self.assertRaisesRegex(ValueError,'all declared'):receipt_check(self.root,self.receipt)
        self.receipt['status']='FAIL';receipt_check(self.root,self.receipt)

    def test_integration_receipt_requires_measured_transfers(self):
        self.lane('C12C')
        with self.assertRaisesRegex(ValueError,'engine adapter'):receipt_check(self.root,self.receipt)
        self.receipt['execution']['mode']='ENGINE_ADAPTER'
        with self.assertRaises(ValueError):receipt_check(self.root,self.receipt)
        self.receipt['transfer']={'path':'staging-copy','synchronization':'explicit wait','effort_method':'logged',
                                 'bytes_per_frame':8,'copies_per_frame':1,'implementation_hours':1}
        receipt_check(self.root,self.receipt)
        self.receipt['transfer']['path']='zero-copy'
        with self.assertRaisesRegex(ValueError,'conflicts'):receipt_check(self.root,self.receipt)
        self.receipt['transfer']['copies_per_frame']=0
        with self.assertRaises(ValueError):receipt_check(self.root,self.receipt)

    def test_nonfinite_metrics_and_escape_rejected(self):
        for value in [float('nan'),float('inf'),True,'1']:
            self.receipt['metrics'][0]['value']=value
            with self.assertRaises(ValueError):receipt_check(self.root,self.receipt)
        self.receipt['metrics'][0]['value']=1;self.receipt['artifact_manifest']='../secret.json'
        with self.assertRaisesRegex(ValueError,'escapes'):receipt_check(self.root,self.receipt)

    def test_draft_protocol_cannot_support_run(self):
        self.protocol['status']='draft';write_json(self.proto_path,self.protocol)
        self.receipt['protocol']['sha256']=digest(self.proto_path)
        with self.assertRaisesRegex(ValueError,'frozen'):receipt_check(self.root,self.receipt)

    def test_frozen_protocol_requires_substantive_fields(self):
        self.protocol['acceptance_rule']='REPLACE'
        with self.assertRaises(ValueError):protocol_check(self.protocol)


if __name__ == '__main__': unittest.main()
