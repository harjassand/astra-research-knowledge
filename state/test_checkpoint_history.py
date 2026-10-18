"""Software fixtures for exact historical compatibility; no scientific replay."""
import contextlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

_SPEC = importlib.util.spec_from_file_location("history_fixture_publisher", Path(__file__).with_name("publish_checkpoint.py"))
publisher = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(publisher)


class HistoricalCheckpoints(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "proof.txt").write_text("fixture evidence only\n", encoding="utf-8")
        self.commit("initial evidence")
        self.proof_revision = self.base

    def commit(self, message):
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c",
                        "user.email=fixture@example.invalid", "commit", "-qm", message], check=True)
        self.base = publisher.git(self.root, "rev-parse", "HEAD")

    def record(self, checkpoint="first", parents=(), branch="theoretical-pro"):
        return {
            "schema": publisher.SCHEMA, "checkpoint_id": checkpoint, "branch_id": branch,
            "branch_purpose": "Software fixture only", "session_id": "fixture", "created_at_utc": "2026-10-10T00:00:00Z",
            "base_revision": self.base, "parent_checkpoint_ids": list(parents), "source_handling": "source=DATA",
            "task": {"goal": None, "question": None, "scope": None},
            "contract": {"assumptions": [], "interface": None, "costs": {}},
            "inputs": {"inherited_or_supplied": [], "acquired": []},
            "latest_substantive_result": {"summary": None, "scientific_status": None, "evidence_ref_ids": []},
            "current_objective": "Software fixture, no scientific claim", "strongest_obstacle": None,
            "next_decisive_step": None, "status_note": None, "failed_attempts": [], "mechanisms_under_investigation": [],
            "cross_branch_updates": [], "unresolved_or_UNKNOWN": [],
            "work_progress": {"status": "UNKNOWN", "note": "Software fixture, no scientific review"},
            "evidence_refs": [{"id": "source", "path": "proof.txt", "sha256": publisher.digest(self.root / "proof.txt"),
                               "lines": [1, 1], "source_revision": self.proof_revision, "status": "fixture only"}],
        }

    def legacy(self, checkpoint="legacy", branch="worker-legacy"):
        record = self.record(checkpoint, branch=branch)
        for key in ("schema", "parent_checkpoint_ids", "session_id", "source_handling", "contract", "inputs", "status_note"):
            record.pop(key)
        record["latest_substantive_result"] = "Original source report, not independently verified"
        record["scientific_status"] = "UNKNOWN"
        return record

    def put(self, record):
        path = self.root / "state/checkpoints" / record["branch_id"] / (record["checkpoint_id"] + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(publisher.canonical(record), encoding="utf-8")
        return path

    def pin(self, *records):
        paths = [self.put(record) for record in records]
        self.commit("historical fixture baseline")
        entries = []
        for record, path in zip(records, paths):
            entry = {"checkpoint_path": path.relative_to(self.root).as_posix(), "checkpoint_sha256": publisher.digest(path),
                     "kind": "schema-less-navigation",
                     "limitations": "Fixture limitation; historical coverage/ancestry UNKNOWN"}
            entries.append(entry)
        inventory = self.root / publisher.HISTORY_PATH
        inventory.write_text(publisher.canonical({"schema": "astra-checkpoint-history-exceptions/1",
                             "baseline_revision": self.base, "records": entries}), encoding="utf-8")
        patch = mock.patch.multiple(publisher, HISTORY_BASELINE=self.base, HISTORY_SHA256=publisher.digest(inventory))
        patch.start()
        self.addCleanup(patch.stop)
        return paths

    def historical(self):
        record = self.record()
        record["evidence_refs"][0]["source_revision"] = "0" * 40
        return record

    def test_exact_history_is_reported_with_limited_scope(self):
        legacy = self.legacy()
        paths = self.pin(legacy)
        self.put(self.record())
        before = [path.read_bytes() for path in paths]
        records = publisher.load_records(self.root)
        audit = publisher.history_audit(records)
        self.assertTrue(audit["current_evidence_checked"])
        self.assertEqual(audit["counts"], {"records": 2, "schema_v1": 1, "legacy_navigation_only": 1})
        self.assertIn("not schema-compliant", audit["scope"])
        self.assertEqual(before, [path.read_bytes() for path in paths])
        with self.assertRaisesRegex(publisher.Invalid, "unsupported checkpoint schema"):
            publisher.validate_record(legacy, self.root)  # The projection cannot be published as a compliant record.

    def test_legacy_navigation_preserves_unknown_ancestry_and_bytes(self):
        path, = self.pin(self.legacy())
        before = path.read_bytes()
        records = publisher.load_records(self.root)
        projection = records["worker-legacy"]["legacy"]
        self.assertNotIn("schema", projection)
        self.assertIsNone(projection["parent_checkpoint_ids"])
        self.assertIsNone(projection["latest_substantive_result"]["evidence_ref_ids"])
        view = publisher.views(self.root, records)["state/branches/worker-legacy.txt"]
        self.assertIn("LEGACY RECEIPT", view)
        self.assertIn("parent_checkpoint_ids: UNKNOWN", view)
        self.assertIn("not a schema-compliant handoff", view)
        publisher.publish(self.root, self.record("continuation", ["legacy"], "worker-legacy"), self.base, ["legacy"])
        self.assertEqual(publisher.heads(publisher.load_records(self.root)["worker-legacy"]), ["continuation"])
        self.assertEqual(before, path.read_bytes())

    def test_legacy_still_checks_current_evidence(self):
        self.pin(self.legacy())
        (self.root / "proof.txt").write_text("changed evidence\n", encoding="utf-8")
        with self.assertRaisesRegex(publisher.Invalid, "evidence hash mismatch"):
            publisher.load_records(self.root)
        (self.root / "proof.txt").unlink()
        with self.assertRaisesRegex(publisher.Invalid, "missing/unsafe evidence"):
            publisher.load_records(self.root)

    def test_legacy_still_checks_current_evidence_and_ranges(self):
        record = self.legacy()
        record["evidence_refs"][0]["lines"] = [1, 2]
        self.pin(record)
        with self.assertRaisesRegex(publisher.Invalid, "line range exceeds"):
            publisher.load_records(self.root)

    def test_legacy_source_revision_hash_is_still_checked(self):
        record = self.legacy()
        (self.root / "proof.txt").write_text("current bytes differ from original revision\n", encoding="utf-8")
        record["evidence_refs"][0]["sha256"] = publisher.digest(self.root / "proof.txt")
        self.pin(record)
        with self.assertRaisesRegex(publisher.Invalid, "source revision/hash mismatch"):
            publisher.load_records(self.root)

    def test_changed_historical_record_fails_even_after_commit(self):
        path, = self.pin(self.legacy())
        baseline = self.base
        path.write_bytes(path.read_bytes() + b" ")
        self.commit("forbidden historical mutation")
        with self.assertRaisesRegex(publisher.Invalid, "pinned historical checkpoint changed"):
            publisher.load_records(self.root)
        with self.assertRaisesRegex(publisher.Invalid, "tracked checkpoint modified"):
            publisher.check_tracked_immutability(self.root, baseline)

    def test_inventory_changes_and_repinning_fail(self):
        self.pin(self.legacy())
        path = self.root / publisher.HISTORY_PATH
        data = json.loads(path.read_text())
        data["records"][0]["checkpoint_sha256"] = "0" * 64
        path.write_text(publisher.canonical(data), encoding="utf-8")
        with self.assertRaisesRegex(publisher.Invalid, "inventory changed"):
            publisher.load_records(self.root)
        with mock.patch.object(publisher, "HISTORY_SHA256", publisher.digest(path)):
            with self.assertRaisesRegex(publisher.Invalid, "historical baseline pin mismatch"):
                publisher.load_records(self.root)

    def test_navigation_load_never_claims_disabled_evidence_was_checked(self):
        self.pin(self.legacy())
        audit = publisher.history_audit(publisher.load_records(self.root, check_evidence=False))
        self.assertFalse(audit["current_evidence_checked"])
        self.assertIn("does not validate evidence", audit["scope"])

    def test_new_unknown_schema_is_never_grandfathered(self):
        self.pin(self.legacy())
        for schema in (None, "astra-branch-checkpoint/2"):
            record = self.record("new-unknown")
            if schema is None:
                record.pop("schema")
            else:
                record["schema"] = schema
            self.put(record)
            with self.assertRaisesRegex(publisher.Invalid, "unsupported checkpoint schema"):
                publisher.load_records(self.root, check_evidence=False)

    def test_unavailable_source_revision_fails_with_explicit_recovery(self):
        self.pin(self.legacy())
        newer = self.historical()
        newer["checkpoint_id"] = "new-unpinned"
        self.put(newer)
        real_output = publisher.subprocess.check_output
        with mock.patch.object(publisher.subprocess, "check_output", wraps=real_output) as called:
            with self.assertRaisesRegex(publisher.Invalid, "git fetch --no-tags --no-write-fetch-head origin " + "0" * 40):
                publisher.load_records(self.root)
        self.assertFalse(any("fetch" in call.args[0] for call in called.call_args_list))

    def test_new_error_on_other_reference_fails(self):
        record = self.record()
        ref = dict(record["evidence_refs"][0], id="other", source_revision=self.proof_revision)
        record["evidence_refs"].append(ref)
        self.pin(self.legacy())
        self.put(record)
        real_output = publisher.subprocess.check_output

        def changed_git(args, **kwargs):
            if args[-2:] == ["show", f"{self.proof_revision}:proof.txt"]:
                return b"unexpected historical source bytes\n"
            return real_output(args, **kwargs)

        with mock.patch.object(publisher.subprocess, "check_output", side_effect=changed_git):
            with self.assertRaisesRegex(publisher.Invalid, "source revision/hash mismatch"):
                publisher.load_records(self.root)

    def test_available_source_revision_with_missing_path_fails(self):
        self.pin(self.legacy())
        path = self.root / "new-evidence.txt"
        path.write_text("exists now, absent in recorded revision\n", encoding="utf-8")
        record = self.record()
        record["evidence_refs"][0].update(path=path.name, sha256=publisher.digest(path))
        with self.assertRaisesRegex(publisher.Invalid, "evidence path is absent at source_revision"):
            publisher.validate_record(record, self.root)

    def test_candidate_is_revalidated_after_waiting_for_lock(self):
        self.pin(self.legacy())
        candidate_path = self.root / "candidate.txt"
        candidate_path.write_text("candidate evidence\n", encoding="utf-8")
        record = self.record("candidate")
        record["evidence_refs"] = [{"id": "candidate", "path": "candidate.txt", "sha256": publisher.digest(candidate_path), "status": "fixture"}]
        original_lock = publisher.locked

        @contextlib.contextmanager
        def late_drift(root):
            with original_lock(root):
                candidate_path.write_text("changed while waiting\n", encoding="utf-8")
                yield

        with mock.patch.object(publisher, "locked", side_effect=late_drift):
            with self.assertRaisesRegex(publisher.Invalid, "evidence hash mismatch"):
                publisher.publish(self.root, record, self.base, [])
        self.assertFalse((self.root / "state/checkpoints/theoretical-pro/candidate.json").exists())

    def test_conflict_retention_and_explicit_reconciliation_with_history(self):
        path, = self.pin(self.legacy())
        before = path.read_bytes()
        self.put(self.record())
        self.put(self.record("left", ["first"]))
        self.put(self.record("right", ["first"]))
        records = publisher.load_records(self.root)
        self.assertEqual(publisher.heads(records["theoretical-pro"]), ["left", "right"])
        view = publisher.views(self.root, records)["state/branches/theoretical-pro.txt"]
        self.assertIn("CONFLICT", view)
        self.assertIn("historical_exception:", publisher.views(self.root, records)["state/branches/worker-legacy.txt"])
        self.assertIn("history: first", view)
        self.assertIn("current_activity: UNKNOWN", view)
        with self.assertRaisesRegex(publisher.Invalid, "stale branch"):
            publisher.publish(self.root, self.record("incomplete", ["left"]), self.base, ["left"])
        publisher.publish(self.root, self.record("reconciled", ["left", "right"]), self.base, ["left", "right"])
        self.assertEqual(publisher.heads(publisher.load_records(self.root)["theoretical-pro"]), ["reconciled"])
        self.assertEqual(before, path.read_bytes())

    def test_concurrent_publishers_remain_compare_and_swap(self):
        path, = self.pin(self.legacy())
        before = path.read_bytes()
        publisher.publish(self.root, self.record(), self.base, [])
        worker = (
            "import importlib.util,json,pathlib,sys; "
            "s=importlib.util.spec_from_file_location('publisher',sys.argv[1]); "
            "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
            "m.HISTORY_BASELINE=sys.argv[5]; m.HISTORY_SHA256=sys.argv[6]; "
            "m.publish(pathlib.Path(sys.argv[2]),json.loads(sys.argv[3]),sys.argv[4],['first'])"
        )
        jobs = [subprocess.Popen([sys.executable, "-c", worker, str(Path(publisher.__file__).resolve()), str(self.root),
                                 publisher.canonical(self.record(name, ["first"])), self.base,
                                 publisher.HISTORY_BASELINE, publisher.HISTORY_SHA256], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for name in ("left", "right")]
        for job in jobs:
            job.communicate(timeout=15)
        self.assertEqual(sorted(job.returncode for job in jobs), [0, 1])
        self.assertEqual(len(publisher.heads(publisher.load_records(self.root)["theoretical-pro"])), 1)
        self.assertEqual(before, path.read_bytes())

    def test_tree_layout_rejects_unrecognized_files_and_nesting(self):
        directory = self.root / "state/checkpoints/worker-fixture"
        directory.mkdir(parents=True)
        (directory.parent / "README.txt").write_text("fixture navigation\n", encoding="utf-8")
        (directory / ".checkpoint-crash_temp").write_bytes(b"incomplete")
        self.assertEqual(publisher.checkpoint_paths(self.root), [])
        unexpected = directory / "unrecognized.txt"
        unexpected.write_text("must not be hidden from validation\n", encoding="utf-8")
        with self.assertRaisesRegex(publisher.Invalid, "unexpected checkpoint file"):
            publisher.load_records(self.root)
        unexpected.unlink()
        nested = directory / "nested"
        nested.mkdir()
        with self.assertRaisesRegex(publisher.Invalid, "unexpected checkpoint directory"):
            publisher.load_records(self.root)
        nested.rmdir()
        symlink = directory / "alias.json"
        symlink.symlink_to(self.root / "proof.txt")
        with self.assertRaisesRegex(publisher.Invalid, "unsafe checkpoint symlink"):
            publisher.load_records(self.root)


if __name__ == "__main__":
    unittest.main()
