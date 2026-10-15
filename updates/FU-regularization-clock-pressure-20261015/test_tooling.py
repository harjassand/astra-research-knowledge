"""Disposable preservation fixtures. No source-repository writes or Git commits."""
from pathlib import Path
import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_integration as builder
import validate_intake as validator
from fu_common import PREFIX


def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


class PreservationFixtures(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fu-rcp-fixture-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.update = self.root / PREFIX
        self.update.mkdir(parents=True)
        (self.update / "package").mkdir()
        shutil.copyfile(HERE / "package/SOURCE_MANIFEST.json", self.update / "package/SOURCE_MANIFEST.json")
        shutil.copytree(HERE / "package/sources", self.update / "package/sources")
        for name in ["SOURCE_MANIFEST.json", "build_integration.py", "fu_common.py", "validate_intake.py"]:
            shutil.copyfile(HERE / name, self.update / name)
        checkpoint = HERE / "CHECKPOINT_RECORD.preservation.v0001.json"
        shutil.copyfile(checkpoint if checkpoint.exists() else HERE / "CHECKPOINT_RECORD.json", self.update / "CHECKPOINT_RECORD.json")
        real_root = HERE.parents[1]
        for name in validator.INHERITED:
            self.write(name, (real_root / name).read_bytes())
        self.write("state/publish_checkpoint.py", (real_root / "state/publish_checkpoint.py").read_bytes())
        self.write("state/branches.tsv", b"branch_id\tpurpose\tstate\thead_checkpoint_ids\tview_path\n")
        for name, value in {
            "indexes/agent_catalog.json": {"scope": "fixture", "claims": []},
            "indexes/agent_graph.json": {"scope": "fixture", "nodes": [], "edges": []},
            "mechanisms/bridge_candidates.json": {"scope": "fixture", "bridges": [], "rejected_transfers": []},
            "web/catalog.json": [], "indexes/query_aliases.json": {"legacy-alias": "preserve"},
        }.items():
            self.write(name, dump(value))
        for name in ["indexes/claims.jsonl", "frontier/CURRENT_CLAIM_STATUS.jsonl", "frontier/OPEN_PROOF_GATES.jsonl",
                     "agent/SEMANTIC_NOTICES.jsonl", "web/documents.jsonl"]:
            self.write(name, b"")
        self.write("indexes/source_metadata.jsonl", b'{"id":"legacy-no-optional-fields"}\n{"unidentified":"legacy"}\n')
        self.curation = json.loads((HERE / "CURATION_INPUT.template.json").read_text())
        self.curation["curation_status"] = "root_final"
        for card in self.curation["cards"]:
            for key, value in list(card.items()):
                if isinstance(value, str) and value.startswith("REPLACE_"):
                    card[key] = "Synthetic fixture only; no scientific assertion."
                elif isinstance(value, list):
                    card[key] = ["Synthetic fixture only." if isinstance(x, str) and x.startswith("REPLACE_") else x for x in value]
        self.baseline = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def write(self, name, raw):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)

    def plan(self, curation=None):
        value = curation or self.curation
        return builder.build_plan(self.root, value, builder.sha(dump(value)))

    def apply_fixture(self):
        self.write(PREFIX + "CURATION_INPUT.json", dump(self.curation))
        plan = self.plan()
        builder.apply_plan(plan)
        for gate in validator.rows(self.root, "frontier/OPEN_PROOF_GATES.jsonl"):
            self.write("frontier/gates/" + gate["gate_id"] + ".json", dump(gate))
        self.write(PREFIX + "DERIVED_MANIFEST.json", dump({"schema": "astra.fu-rcp-derived-manifest.v1",
            "base_revision": self.curation["base_revision"], "total_files": 0, "total_bytes": 0, "files": []}))

    def fake_git(self, root, *args):
        if args[:2] == ("ls-tree", "-r"):
            return ("\n".join(sorted(self.baseline)) + "\n").encode()
        if args[:2] == ("diff", "--name-only"):
            names = [name for name, raw in self.baseline.items() if not (self.root / name).is_file() or (self.root / name).read_bytes() != raw]
            return ("\n".join(names) + "\n").encode()
        if args[0] == "show":
            return self.baseline[args[1].split(":", 1)[1]]
        raise AssertionError(args)

    def test_three_originals_and_no_live_apply_in_dry_plan(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        plan = self.plan()
        self.assertGreater(plan.summary()["changed_file_count"], 0)
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertEqual(len([p for p in plan.after if p.startswith("cards/")]), 3)

    def test_incomplete_root_curation_rejected(self):
        curation = copy.deepcopy(self.curation)
        curation["curation_status"] = "DRAFT_PENDING_ROOT_ADJUDICATION"
        with self.assertRaisesRegex(ValueError, "not ready"):
            self.plan(curation)

    def test_explicit_draft_plan_cannot_apply(self):
        curation = copy.deepcopy(self.curation)
        curation["curation_status"] = "DRAFT_ROOT_REVIEW"
        plan = builder.build_plan(self.root, curation, builder.sha(dump(curation)), allow_draft=True)
        self.assertEqual(plan.summary()["mode"], "read_only_draft_plan")
        with self.assertRaisesRegex(ValueError, "cannot be applied"):
            builder.apply_plan(plan)
        self.assertFalse((self.root / "cards").exists())

    def test_wrong_evidence_hash_rejected(self):
        curation = copy.deepcopy(self.curation)
        curation["evidence"]["clock_inventory"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "bytes/hash"):
            self.plan(curation)

    def test_invalid_inclusive_line_range_rejected(self):
        curation = copy.deepcopy(self.curation)
        curation["evidence"]["clock_inventory"]["lines"] = [1, 99999]
        with self.assertRaisesRegex(ValueError, "Invalid evidence range"):
            self.plan(curation)

    def test_unsafe_source_path_rejected(self):
        curation = copy.deepcopy(self.curation)
        curation["sources"][0]["path"] = PREFIX + "../escape.txt"
        with self.assertRaisesRegex(ValueError, "traversal"):
            self.plan(curation)

    def test_numeric_route_collision_rejected(self):
        self.write("indexes/claims.jsonl", b'{"id":"N857-existing-unrelated"}\n')
        with self.assertRaisesRegex(ValueError, "Numeric route collision"):
            self.plan()

    def test_missing_original_copy_rejected(self):
        (self.update / "package/sources/clock_pasted.txt").unlink()
        with self.assertRaisesRegex(ValueError, "Incoming text bytes changed"):
            self.plan()

    def test_append_only_heterogeneous_metadata_and_idempotence(self):
        before = (self.root / "indexes/source_metadata.jsonl").read_bytes()
        self.apply_fixture()
        self.assertTrue((self.root / "indexes/source_metadata.jsonl").read_bytes().startswith(before))
        self.assertEqual(self.plan().summary()["changed_file_count"], 0)
        self.assertEqual(builder.apply_plan(self.plan()), 0)

    def test_changed_immutable_output_rejected(self):
        self.apply_fixture()
        cid = self.curation["cards"][0]["id"]
        self.write("cards/" + cid + ".txt", b"changed\n")
        with self.assertRaisesRegex(ValueError, "Immutable artifact collision"):
            self.plan()

    def test_concurrent_input_change_rejected_before_writes(self):
        plan = self.plan()
        self.write("indexes/source_metadata.jsonl", b'{"concurrent":"change"}\n')
        with self.assertRaisesRegex(ValueError, "Concurrent modification"):
            builder.apply_plan(plan)
        self.assertFalse((self.root / "cards").exists())

    def test_optional_root_card_and_required_programmes(self):
        curation = copy.deepcopy(self.curation)
        extra = copy.deepcopy(curation["cards"][0])
        extra["id"] = "N860-synthetic-root-fixture"
        curation["cards"].append(extra)
        self.assertEqual(len([p for p in self.plan(curation).after if p.startswith("cards/")]), 4)
        curation["cards"] = curation["cards"][1:]
        with self.assertRaisesRegex(ValueError, "Required source programmes"):
            self.plan(curation)

    def test_stale_head_apply_rejected_without_writes(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        argv = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply",
                "--expect-input-sha256", builder.sha(input_path.read_bytes())]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(builder, "git", return_value="0" * 40):
            with self.assertRaisesRegex(ValueError, "HEAD changed"):
                builder.main()
        self.assertFalse((self.root / "cards").exists())

    def test_changed_remote_apply_rejected_without_writes(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        argv = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply",
                "--expect-input-sha256", builder.sha(input_path.read_bytes())]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(builder, "git", side_effect=[self.curation["base_revision"], "0" * 40 + "\trefs/heads/main"]):
            with self.assertRaisesRegex(ValueError, "Remote main changed"):
                builder.main()
        self.assertFalse((self.root / "cards").exists())

    def test_changed_final_input_hash_rejected_without_writes(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        argv = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply",
                "--expect-input-sha256", "0" * 64]
        with mock.patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(ValueError, "Finalized curation input changed"):
                builder.main()
        self.assertFalse((self.root / "cards").exists())

    def test_derived_proof_cannot_be_labelled_supplied_original(self):
        curation = copy.deepcopy(self.curation)
        path = PREFIX + "package/root/fixture.txt"
        self.write(path, b"fixture\n")
        curation["sources"].append({"path": path, "sha256": builder.sha(b"fixture\n"),
            "source_id": "src-FU-RCP-fake-original", "title": "fixture", "read_depth": "fixture",
            "provenance_role": "supplied_original_text"})
        with self.assertRaisesRegex(ValueError, "Only the three original texts"):
            self.plan(curation)

    def test_scoped_validator_ignores_unrelated_same_prefix_gate(self):
        self.apply_fixture()
        p = self.root / "frontier/OPEN_PROOF_GATES.jsonl"
        p.write_bytes(p.read_bytes() + b'{"gate_id":"G-FU-RCP-UNRELATED","status":"open"}\n')
        with mock.patch.object(validator, "git", side_effect=self.fake_git), mock.patch.object(validator.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)):
            result = validator.validate(self.root, "integrated", self.curation["base_revision"])
        self.assertEqual(result["status"], "SCOPED_PASS")
        self.assertTrue(result["exact_owned_ID_selection"])
        self.assertEqual(result["open_gates"], 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
