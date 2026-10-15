"""Intake rejection and distinct HEAD/remote-pin fixtures; no science scripts run."""
from pathlib import Path
import copy
import json
import sys
import unittest
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fz_common as common
import protected_baseline as boundary


class SourceBoundaries(unittest.TestCase):
    def setUp(self):
        self.manifest_raw = (HERE / "package/SOURCE_MANIFEST.v0002.json").read_bytes()
        self.previous_raw = (HERE / "package/SOURCE_MANIFEST.json").read_bytes()
        self.manifest = json.loads(self.manifest_raw)
        self.originals = {item["path"]: (HERE / "package/originals" / item["path"]).read_bytes() for item in self.manifest["files"]}

    def outputs(self, manifest_raw=None, reader=None, **kwargs):
        return common.source_outputs(manifest_raw or self.manifest_raw, self.previous_raw,
                                     reader or self.originals.__getitem__, **kwargs)

    def test_exact_manifest_inventory_and_both_versions_are_preserved(self):
        outputs, wrapper = self.outputs()
        self.assertEqual(wrapper["original_count"], self.manifest["total_files"])
        self.assertEqual(wrapper["original_bytes"], self.manifest["total_bytes"])
        self.assertEqual(outputs[common.PREFIX + "package/SOURCE_MANIFEST.v0002.json"], self.manifest_raw)
        self.assertEqual(outputs[common.PREFIX + "package/SOURCE_MANIFEST.json"], self.previous_raw)
        self.assertTrue(all(item["source_id"].startswith("src-FZ-") for item in wrapper["files"]))

    def test_changed_manifest_and_source_bytes_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "v2 intake manifest changed"):
            self.outputs(self.manifest_raw + b" ")
        name = self.manifest["files"][0]["path"]
        with self.assertRaisesRegex(ValueError, "Original source bytes changed"):
            self.outputs(reader=lambda path: self.originals[path] + (b"changed" if path == name else b""))

    def test_duplicate_path_and_role_change_fail_closed_even_with_new_pin(self):
        for mutation, message in (("duplicate", "Duplicate/case-colliding"), ("role", "source role changed")):
            value = copy.deepcopy(self.manifest)
            if mutation == "duplicate":
                value["files"][1] = copy.deepcopy(value["files"][0])
            else:
                value["files"][0]["role"] = "operative_user_request"
            raw = common.encoded(value)
            with self.assertRaisesRegex(ValueError, message):
                self.outputs(raw, expected_manifest_sha256=common.digest(raw))

    def test_path_escape_is_rejected(self):
        for name in ("../escape", "/absolute", "sources/../escape", "C:/escape", "sources\\escape"):
            with self.assertRaises(ValueError):
                common.local(HERE, name)


class ProspectivePublicationBoundaries(unittest.TestCase):
    def setUp(self):
        self.item = {"path": common.PREFIX + "package/derived/root/proof.md", "research_relative_path": "root/proof.md",
                     "sha256": "a" * 64, "bytes": 10, "provenance_role": "root_synthesis", "payload_kind": "proof",
                     "selection_reason": "Example root-authored derivation; fixture only", **{flag: False for flag in common.EXTERNAL_FLAGS}}

    def test_authored_text_metadata_is_eligible_without_selecting_or_copying(self):
        common.check_authored_payload(self.item)

    def test_every_external_collection_flag_and_missing_classification_are_rejected(self):
        for flag in common.EXTERNAL_FLAGS:
            for mode in ("true", "missing"):
                item = copy.deepcopy(self.item)
                if mode == "true":
                    item[flag] = True
                else:
                    del item[flag]
                with self.assertRaisesRegex(ValueError, "Root must explicitly exclude"):
                    common.check_authored_payload(item)

    def test_workbook_fulltext_binary_dataset_and_clone_paths_are_rejected(self):
        for suffix in (".xlsx", ".xls", ".pdf", ".epub", ".parquet", ".npy", ".zip", ".pdf.txt"):
            item = copy.deepcopy(self.item)
            item["path"] = common.PREFIX + "package/derived/root/external" + suffix
            with self.assertRaisesRegex(ValueError, "Publication allowlist"):
                common.check_authored_payload(item)
        for part in ("clones", "caches", "datasets", "workbooks", "fulltexts", "__pycache__", ".git"):
            item = copy.deepcopy(self.item)
            item["path"] = common.PREFIX + "package/derived/" + part + "/file.md"
            with self.assertRaisesRegex(ValueError, "Publication allowlist"):
                common.check_authored_payload(item)

    def test_supplied_originals_cannot_be_relabelled_authored(self):
        self.item["research_relative_path"] = "sources/positive_core_report.txt"
        with self.assertRaisesRegex(ValueError, "cannot relabel"):
            common.check_authored_payload(self.item)


class HistoricalBoundaries(unittest.TestCase):
    def setUp(self):
        self.head, self.remote = "a" * 40, common.INITIAL_MAIN
        self.changed, self.untracked = [], []

        def fake_git(root, *args):
            if args[0] == "rev-parse":
                return (self.head + "\n").encode()
            if args[0] == "ls-tree":
                return b"cards/N1-old.txt\nstate/checkpoints/old.json\n"
            if args[0] == "diff":
                return "\n".join(self.changed).encode()
            if args[0] == "ls-files":
                return "\n".join(self.untracked).encode()
            if args[0] == "ls-remote":
                return (self.remote + "\trefs/heads/main\n").encode()
            raise AssertionError("Unexpected Git operation: " + str(args))

        patcher = mock.patch.object(boundary, "git", side_effect=fake_git)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch.object(boundary.subprocess, "run", return_value=None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def check(self, **kwargs):
        return boundary.check_baseline(HERE, immutable_base=common.INITIAL_MAIN,
                                       expected_head=kwargs.get("expected_head", self.head),
                                       expected_remote_main=common.INITIAL_MAIN, check_remote=True)

    def test_evidence_commit_HEAD_can_differ_from_remote_main(self):
        self.changed = [common.PREFIX + "SOURCE_MANIFEST.json"]
        result = self.check()
        self.assertNotEqual(result["actual_head"], result["observed_remote_main"])

    def test_stale_head_is_rejected_separately(self):
        with self.assertRaisesRegex(ValueError, "HEAD differs from expected_head"):
            self.check(expected_head="b" * 40)

    def test_moved_remote_is_rejected_separately(self):
        self.remote = "c" * 40
        with self.assertRaisesRegex(ValueError, "Remote main moved"):
            self.check()

    def test_historical_changes_and_unowned_paths_are_rejected(self):
        self.changed = ["cards/N1-old.txt"]
        with self.assertRaisesRegex(ValueError, "tracked baseline files"):
            self.check()
        self.changed = ["cards/N999-new.txt"]
        with self.assertRaisesRegex(ValueError, "outside FZ"):
            self.check()
        self.changed, self.untracked = [], ["cards/N999-new.txt"]
        with self.assertRaisesRegex(ValueError, "Unowned untracked paths"):
            self.check()


if __name__ == "__main__":
    unittest.main(verbosity=2)
