import concurrent.futures
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from discovery import Store, git, publish_claim, release_claim, remote_claim
from validate import validate


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store = Store(self.root)
        self.session = self.store.bootstrap("test runtime", "test-task", "Test capture", "test-session")
        self.payload = self.root / "result.json"
        self.payload.write_text('{"value": 3}\n')

    def tearDown(self):
        self.tmp.cleanup()

    def capture(self, run="run-1"):
        return self.store.capture(self.session, run, "NUMERICAL", "test result", "test command", [], [self.payload])

    def test_capture_and_tampering(self):
        folder = self.capture()
        self.assertEqual(validate(self.root)[1], [])
        (folder / "files" / "result.json").write_text('{"value": 4}\n')
        self.assertTrue(any("SHA-256 mismatch" in error for error in validate(self.root)[1]))

    def test_run_is_immutable(self):
        folder = self.capture()
        manifest = (folder / "manifest.json").read_bytes()
        with self.assertRaises(FileExistsError):
            self.capture()
        self.assertEqual((folder / "manifest.json").read_bytes(), manifest)

    def test_paths_cannot_escape(self):
        with self.assertRaises(ValueError):
            self.store.bootstrap("test", "test-task", "escape", "../escape")
        folder = self.capture()
        path = folder / "manifest.json"
        manifest = json.loads(path.read_text())
        manifest["files"][0]["path"] = "../../../../result.json"
        path.write_text(json.dumps(manifest))
        self.assertTrue(any("escapes" in error for error in validate(self.root)[1]))

    def test_symlink_and_duplicate_inputs_rejected(self):
        link = self.root / "link.json"
        link.symlink_to(self.payload)
        with self.assertRaises(ValueError):
            self.store.capture(self.session, "links", "OPEN", "test", "test", [], [link])
        second = self.root / "other" / "result.json"
        second.parent.mkdir()
        second.write_text("different")
        with self.assertRaises(ValueError):
            self.store.capture(self.session, "duplicates", "OPEN", "test", "test", [], [self.payload, second])

    def test_unmanifested_output_rejected(self):
        folder = self.capture()
        (folder / "files" / "extra.txt").write_text("unrecorded")
        self.assertTrue(any("Unmanifested" in error for error in validate(self.root)[1]))

    def test_session_resume_does_not_overwrite(self):
        before = self.store.session_path(self.session).read_bytes()
        with self.assertRaises(FileExistsError):
            self.store.bootstrap("new owner", "test-task", "overwrite", self.session)
        self.assertEqual(before, self.store.session_path(self.session).read_bytes())

    def test_candidate_reference_and_checkpoint(self):
        self.store.new_candidate(self.session, "candidate-1", "Question")
        self.store.checkpoint(self.session, "handoff", "conditional result", "baseline comparison")
        self.assertEqual(validate(self.root)[1], [])
        path = self.root / "candidates" / "candidate-1" / "candidate.json"
        obj = json.loads(path.read_text())
        obj["session_id"] = "missing"
        path.write_text(json.dumps(obj))
        self.assertTrue(any("Referenced session" in error for error in validate(self.root)[1]))

    def test_input_metadata_and_legacy_ambiguity_rejected(self):
        folder = self.capture()
        path = folder / "manifest.json"
        manifest = json.loads(path.read_text())
        manifest["schema_version"] = 1
        manifest["inputs"] = "not an array"
        path.write_text(json.dumps(manifest))
        self.assertTrue(any("inputs must be an array" in error for error in validate(self.root)[1]))
        item = {"name": "same.json", "sha256": "0" * 64, "size_bytes": 0}
        manifest["inputs"] = [item, dict(item)]
        path.write_text(json.dumps(manifest))
        self.assertTrue(any("Ambiguous legacy input names" in error for error in validate(self.root)[1]))

    def test_same_named_inputs_are_preserved_and_verified(self):
        sources = []
        for directory, value in (("a", "first"), ("b", "second")):
            path = self.root / directory / "input.json"
            path.parent.mkdir()
            path.write_text(value)
            sources.append(path)
        folder = self.store.capture(self.session, "input-test", "OPEN", "test", "test", sources, [self.payload])
        manifest = json.loads((folder / "manifest.json").read_text())
        self.assertEqual(manifest["schema_version"], 2)
        self.assertEqual([x["source_path"] for x in manifest["inputs"]], ["a/input.json", "b/input.json"])
        self.assertNotEqual(manifest["inputs"][0]["path"], manifest["inputs"][1]["path"])
        self.assertEqual(validate(self.root)[1], [])
        (folder / manifest["inputs"][0]["path"]).write_text("tampered")
        self.assertTrue(any("Captured input digest/size mismatch" in error for error in validate(self.root)[1]))

    def test_captured_input_cannot_escape_and_extra_input_is_rejected(self):
        folder = self.store.capture(self.session, "input-test", "OPEN", "test", "test", [self.payload], [self.payload])
        manifest_path = folder / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        original = manifest["inputs"][0]["path"]
        manifest["inputs"][0]["path"] = "inputs/../../../../result.json"
        manifest_path.write_text(json.dumps(manifest))
        self.assertTrue(any("escapes" in error for error in validate(self.root)[1]))
        manifest["inputs"][0]["path"] = original
        manifest_path.write_text(json.dumps(manifest))
        (folder / "inputs" / "unrecorded.txt").write_text("extra")
        self.assertTrue(any("Unmanifested or missing captured input" in error for error in validate(self.root)[1]))

    def test_captured_markdown_is_opaque_payload(self):
        source = self.root / "source.md"
        source.write_text("[reference](outside-original-context.md)")
        self.store.capture(self.session, "markdown", "OPEN", "test", "test", [source], [source])
        source.unlink()
        self.assertEqual(validate(self.root)[1], [])


class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(self.remote)], check=True, capture_output=True)
        self.clients = []
        for index in range(2):
            client = self.root / f"client-{index}"
            subprocess.run(["git", "clone", str(self.remote), str(client)], check=True, capture_output=True)
            self.clients.append(client)

    def tearDown(self):
        self.tmp.cleanup()

    def claim(self, session):
        return {"record_type": "claim", "schema_version": 1, "task": "same-task", "session": session,
                "created_at": "test", "base_revision": "test", "owned_paths": ["candidates/test"]}

    def test_simultaneous_claim_has_one_winner(self):
        def attempt(index):
            try:
                return publish_claim(self.clients[index], self.claim(f"session-{index}"))
            except RuntimeError:
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(attempt, range(2)))
        self.assertEqual(sum(value is not None for value in results), 1)
        winner = next(value for value in results if value is not None)
        self.assertEqual(remote_claim(self.clients[0], "same-task"), winner)

    def test_stale_release_cannot_delete_new_owner(self):
        first = publish_claim(self.clients[0], self.claim("first"))
        marker = release_claim(self.clients[0], "same-task", first, "first")
        self.assertEqual(remote_claim(self.clients[0], "same-task"), marker)
        second = publish_claim(self.clients[1], self.claim("second"))
        with self.assertRaises(RuntimeError):
            release_claim(self.clients[0], "same-task", first, "first")
        self.assertEqual(remote_claim(self.clients[0], "same-task"), second)

    def test_release_requires_owner_and_preserves_audit_history(self):
        first = publish_claim(self.clients[0], self.claim("owner"))
        with self.assertRaises(RuntimeError):
            release_claim(self.clients[0], "same-task", first, "other-session")
        marker = release_claim(self.clients[0], "same-task", first, "owner")
        payload = json.loads(git(self.clients[0], "show", marker + ":claim.json"))
        self.assertEqual(payload["status"], "released")
        self.assertEqual(payload["released_from_sha"], first)
        self.assertEqual(git(self.clients[0], "rev-parse", marker + "^"), first)

    def test_reacquisition_of_released_marker_has_one_winner(self):
        first = publish_claim(self.clients[0], self.claim("first"))
        marker = release_claim(self.clients[0], "same-task", first, "first")
        def attempt(index):
            try:
                return publish_claim(self.clients[index], self.claim(f"next-{index}"))
            except RuntimeError:
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(attempt, range(2)))
        self.assertEqual(sum(value is not None for value in results), 1)
        winner = next(value for value in results if value is not None)
        self.assertEqual(remote_claim(self.clients[0], "same-task"), winner)
        owner = results.index(winner)
        self.assertEqual(git(self.clients[owner], "rev-parse", winner + "^"), marker)

    def test_dependency_blocks_claim(self):
        store = Store(self.clients[0])
        session = store.bootstrap("test", "dependent", "test", "dependent-session")
        store.new_task("parent", "parent", ["parent"], [])
        store.new_task("dependent", "dependent", ["dependent"], ["parent"])
        with self.assertRaisesRegex(ValueError, "not complete"):
            store.claim(session, "dependent")
        self.assertIsNone(remote_claim(self.clients[0], "dependent"))


if __name__ == "__main__":
    unittest.main()
