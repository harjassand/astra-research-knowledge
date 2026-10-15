"""Hostile archive and append-only fixtures; no source scripts or Git mutations."""
from pathlib import Path
import copy
import io
import json
import stat
import sys
import tempfile
import unittest
import warnings
from unittest import mock
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fw_common as common
import protected_baseline as boundary


def archive(entries):
    stream = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(stream, "w") as target:
            for name, raw, mode in entries:
                item = zipfile.ZipInfo(name)
                item.external_attr = mode << 16
                target.writestr(item, raw)
    return stream.getvalue()


class ArchiveBoundaries(unittest.TestCase):
    def test_exact_binary_and_whitespace_bytes_survive(self):
        raw = b"\x00\xff\n trailing whitespace \t\n"
        value = archive([("a/data.npz", raw, stat.S_IFREG | 0o644)])
        self.assertEqual(common.safe_zip_members(value), {"a/data.npz": raw})

    def test_parent_traversal_absolute_windows_and_backslash_rejected(self):
        for name in ["../escape", "/absolute", "C:/drive", "a\\escape", "./same", "a//ambiguous"]:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "Unsafe"):
                common.safe_zip_members(archive([(name, b"x", stat.S_IFREG)]))

    def test_zip_symlink_and_device_rejected(self):
        for kind in [stat.S_IFLNK, stat.S_IFCHR, stat.S_IFIFO]:
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "special files"):
                common.safe_zip_members(archive([("a", b"target", kind | 0o644)]))

    def test_duplicate_and_case_collision_rejected(self):
        for second in ["same", "SAME"]:
            with self.subTest(second=second), self.assertRaisesRegex(ValueError, "colliding archive"):
                common.safe_zip_members(archive([("same", b"first", stat.S_IFREG), (second, b"other", stat.S_IFREG)]))

    def test_file_directory_ancestor_collision_rejected(self):
        for names in [("a", "a/child"), ("A", "a/child")]:
            with self.subTest(names=names), self.assertRaisesRegex(ValueError, "file/directory collision|Case-colliding archive directory"):
                common.safe_zip_members(archive([(names[0], b"file", stat.S_IFREG), (names[1], b"child", stat.S_IFREG)]))

    def test_implicit_directory_case_alias_rejected(self):
        with self.assertRaisesRegex(ValueError, "Case-colliding archive directory"):
            common.safe_zip_members(archive([("A/x", b"x", stat.S_IFREG), ("a/y", b"y", stat.S_IFREG)]))

    def test_corrupt_member_crc_rejected(self):
        value = archive([("payload", b"unique-member-payload", stat.S_IFREG)])
        value = value.replace(b"unique-member-payload", b"unique-member-payloae", 1)
        with self.assertRaises(zipfile.BadZipFile):
            common.safe_zip_members(value)

    def test_source_manifest_pin_and_member_bytes_are_independent(self):
        zipped = archive([("data.txt", b"exact supplied bytes  \n", stat.S_IFREG)])
        record = {"path": "sources/supplied.zip", "bytes": len(zipped), "sha256": common.digest(zipped),
                  "original_path": "/synthetic/supplied.zip", "kind": "supplied_archive"}
        manifest = {"schema": "astra.source-intake.v2", "initial_main": common.INITIAL_MAIN,
                    "files": [record], "total_original_files": 1, "total_original_bytes": len(zipped),
                    "archive_members_are_derived_extractions": True, "source_handling": "DATA"}
        raw = common.encoded(manifest)
        result, wrapper = common.source_outputs(raw, lambda name: zipped, expected_manifest_sha256=common.digest(raw))
        self.assertEqual(result[common.PREFIX + "package/originals/sources/supplied.zip"], zipped)
        self.assertEqual(result[common.PREFIX + "package/extractions/supplied/data.txt"], b"exact supplied bytes  \n")
        self.assertEqual(wrapper["original_count"], 1)
        self.assertEqual(wrapper["extracted_member_count"], 1)
        with self.assertRaisesRegex(ValueError, "Original intake manifest changed"):
            common.source_outputs(raw + b"\n", lambda name: zipped, expected_manifest_sha256=common.digest(raw))
        with self.assertRaisesRegex(ValueError, "Original source bytes changed"):
            common.source_outputs(raw, lambda name: zipped + b"x", expected_manifest_sha256=common.digest(raw))

    def test_symlinked_parent_reference_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "actual").mkdir()
            (root / "link").symlink_to(root / "actual", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Symlink"):
                common.local(root, "link/file.txt")


class HistoricalBoundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fw-boundary-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.baseline = {"cards/N1-old.txt": b"old scientific artifact\n"}
        for name in boundary.JSONL_PATHS:
            self.baseline[name] = b'{"old":"preserve"}\n'
        for name, fields in boundary.JSON_GROUPS.items():
            self.baseline[name] = common.encoded({key: [{"old": key}] for key in fields}) if fields != [None] else common.encoded([{"old": "catalog"}])
        self.baseline["indexes/query_aliases.json"] = common.encoded({"old": "keep"})
        for name, raw in self.baseline.items():
            self.write(name, raw)
        self.remote = common.INITIAL_MAIN
        self.untracked = []

        def fake_git(root, *args):
            if args[0] == "ls-tree":
                return ("\n".join(self.baseline) + "\n").encode()
            if args[0] == "diff":
                return "\n".join(name for name, raw in self.baseline.items() if not (self.root / name).is_file() or (self.root / name).read_bytes() != raw).encode()
            if args[0] == "show":
                return self.baseline[args[1].split(":", 1)[1]]
            if args[0] == "rev-parse":
                return (common.INITIAL_MAIN + "\n").encode()
            if args[0] == "ls-remote":
                return (self.remote + "\trefs/heads/main\n").encode()
            if args[0] == "ls-files":
                return "\n".join(self.untracked).encode()
            raise AssertionError("Unexpected Git operation in fixture: " + str(args))

        patcher = mock.patch.object(boundary, "git", side_effect=fake_git)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch.object(boundary.subprocess, "run", return_value=None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def check(self, phase="integrated", remote=False):
        return boundary.check_baseline(self.root, common.INITIAL_MAIN, phase=phase, check_remote=remote)

    def test_unchanged_history_passes_without_writes(self):
        before = {name: (self.root / name).read_bytes() for name in self.baseline}
        self.check("prepared")
        self.assertEqual(before, {name: (self.root / name).read_bytes() for name in self.baseline})

    def test_existing_scientific_artifact_change_and_deletion_rejected(self):
        self.write("cards/N1-old.txt", b"promoted\n")
        with self.assertRaisesRegex(ValueError, "Historical immutable artifact changed"):
            self.check()
        (self.root / "cards/N1-old.txt").unlink()
        with self.assertRaisesRegex(ValueError, "Historical immutable artifact changed"):
            self.check()

    def test_jsonl_prefix_rewrite_rejected(self):
        self.write("frontier/CURRENT_CLAIM_STATUS.jsonl", b'{"old":"promoted"}\n')
        with self.assertRaisesRegex(ValueError, "Historical registry byte prefix changed"):
            self.check()

    def test_appended_jsonl_and_array_entries_allowed(self):
        name = "frontier/CURRENT_CLAIM_STATUS.jsonl"
        self.write(name, self.baseline[name] + b'{"new":"unreviewed"}\n')
        name = "indexes/agent_catalog.json"
        value = json.loads(self.baseline[name])
        value["claims"].append({"new": "unreviewed"})
        self.write(name, common.encoded(value))
        self.check()

    def test_historical_array_value_and_order_rewrites_rejected(self):
        name = "indexes/agent_catalog.json"
        self.write(name, common.encoded({"claims": [{"old": "changed"}]}))
        with self.assertRaisesRegex(ValueError, "Historical JSON values/order changed"):
            self.check()

    def test_historical_alias_rewrite_rejected(self):
        self.write("indexes/query_aliases.json", common.encoded({"old": "changed"}))
        with self.assertRaisesRegex(ValueError, "Historical query alias changed"):
            self.check()

    def test_preparation_rejects_even_append_only_registry_mutation(self):
        name = "frontier/CURRENT_CLAIM_STATUS.jsonl"
        self.write(name, self.baseline[name] + b'{"new":"unreviewed"}\n')
        with self.assertRaisesRegex(ValueError, "Preparation changed tracked baseline files"):
            self.check("prepared")

    def test_preparation_rejects_unowned_new_paths(self):
        self.untracked = ["cards/N999-unowned.txt"]
        with self.assertRaisesRegex(ValueError, "Unowned untracked paths"):
            self.check("prepared")

    def test_remote_main_movement_rejected(self):
        self.remote = "0" * 40
        with self.assertRaisesRegex(ValueError, "Remote main moved"):
            self.check(remote=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
