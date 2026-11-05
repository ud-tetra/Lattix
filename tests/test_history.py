import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_history import check_change


class HistoryTests(unittest.TestCase):
    def test_new_run_allowed(self):
        self.assertIsNone(check_change('artifacts/s/new/manifest.json',None,b'new'))

    def test_recaptured_digest_does_not_allow_rewriting_old_run(self):
        for path in ['artifacts/s/r/manifest.json','artifacts/s/r/files/x','artifacts/s/r/files/README.md',
                     'sources/imports/v1/provenance.json','sources/imports/v1/files/README.md']:
            self.assertIsNotNone(check_change(path,b'old',b'new'))
            self.assertIsNotNone(check_change(path,b'old',None))

    def test_frozen_protocol_cannot_be_unfrozen_or_deleted(self):
        old=json.dumps({'status':'frozen'}).encode()
        self.assertIsNotNone(check_change('benchmarks/preregistrations/p.json',old,b'{"status":"draft"}'))
        self.assertIsNotNone(check_change('benchmarks/preregistrations/p.json',old,None))

    def test_draft_protocol_can_be_frozen(self):
        self.assertIsNone(check_change('benchmarks/preregistrations/p.json',b'{"status":"draft"}',b'{"status":"frozen"}'))

    def test_journal_and_updates_append_only(self):
        for path in ['sessions/s/journal.md','state/UPDATES.md']:
            self.assertIsNone(check_change(path,b'old\n',b'old\nnew\n'))
            self.assertIsNotNone(check_change(path,b'old\n',b'changed\n'))

    def test_normal_source_edits_allowed(self):
        self.assertIsNone(check_change('scripts/lattix.py',b'old',b'new'))


if __name__ == '__main__': unittest.main()
