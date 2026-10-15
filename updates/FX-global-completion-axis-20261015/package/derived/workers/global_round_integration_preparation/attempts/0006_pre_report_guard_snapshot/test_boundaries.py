"""Hostile archive and append-only fixtures; no source scripts or Git mutations."""
from pathlib import Path
import copy
import json
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fx_common as common
import protected_baseline as boundary


class HistoricalBoundaries(unittest.TestCase):
    def setUp(self):
        fixture_dir = common.RESEARCH_ROOT / "workers/global_round_integration_preparation/fixtures"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="fx-boundary-", dir=fixture_dir)
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
