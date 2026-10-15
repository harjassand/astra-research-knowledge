"""Disposable integrity fixtures; synthetic statements and no live Git operations."""
from pathlib import Path
import copy
import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_integration as builder
import preserve_selected as preserver
import validate_intake as validator
from fv_common import PREFIX, ORIGINAL_MANIFEST_SHA256, RESEARCH_ROOT, digest, selection_records, verify_selection


def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


class PreservationFixtures(unittest.TestCase):
    def setUp(self):
        fixture_dir = Path(os.environ.get("FV_FIXTURE_DIR", RESEARCH_ROOT / "workers/integration_engine_sol/fixtures"))
        fixture_dir.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="fv-fixture-", dir=fixture_dir)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        self.update = self.root / PREFIX
        self.update.mkdir(parents=True)
        shutil.copytree(HERE / "package/sources", self.update / "package/sources")
        for name in ["SOURCE_MANIFEST.json", "package/SOURCE_MANIFEST.json", "CHECKPOINT_RECORD.preservation.v0001.json",
                     "INHERITED_SCHEMA_FAILURES.v0001.json", "build_integration.py", "fv_common.py",
                     "preserve_selected.py", "validate_intake.py"]:
            target = self.update / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / name, target)
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
        self.research = Path(self.temp.name) / "synthetic-research"
        source = self.research / "root/SYNTHETIC_PROOF.md"
        source.parent.mkdir(parents=True)
        self.proof = b"Synthetic preservation fixture only.\nNo scientific assertion.\n"
        source.write_bytes(self.proof)
        item = {"research_relative_path": "root/SYNTHETIC_PROOF.md", "path": PREFIX + "package/root/SYNTHETIC_PROOF.md",
                "sha256": digest(self.proof), "bytes": len(self.proof), "provenance_role": "root_synthesis",
                "payload_kind": "proof", "contains_external_fulltext": False,
                "contains_full_lj_network_or_coordinates": False, "selection_reason": "Synthetic fixture only."}
        self.selection = {"schema": "astra.fv-selected-freeze.v1", "status": "root_frozen", "selected_by": "root",
                          "base_revision": builder.verify_incoming(self.root)["initial_main"],
                          "research_root": str(RESEARCH_ROOT), "original_manifest_sha256": ORIGINAL_MANIFEST_SHA256,
                          "total_files": 1, "total_bytes": len(self.proof), "files": [item]}
        preserver.apply_copy(preserver.plan_copy(self.root, dump(self.selection), "SELECTED_FREEZE.v0001.json", research_root=self.research))
        self.curation = json.loads((HERE / "CURATION_INPUT.template.json").read_text())
        self.curation["curation_status"] = "root_final"
        self.curation["reserved_routes"] = ["N990001", "N990002", "N990003"]
        self.curation["selected_freeze"] = {"path": PREFIX + "SELECTED_FREEZE.v0001.json", "sha256": digest(dump(self.selection))}
        for number, card in enumerate(self.curation["cards"], 990001):
            card["id"] = "N" + str(number) + "-synthetic-fixture"
            for key, value in list(card.items()):
                if isinstance(value, str) and value.startswith("REPLACE_"):
                    card[key] = "Synthetic fixture only; no scientific assertion."
                elif isinstance(value, list):
                    card[key] = ["Synthetic fixture only." if isinstance(x, str) and x.startswith("REPLACE_") else x for x in value]
        self.curation["sources"].append({"path": item["path"], "sha256": item["sha256"],
                                         "source_id": "src-FV-PC-synthetic-proof", "title": "Synthetic fixture only",
                                         "read_depth": "Synthetic fixture only", "provenance_role": item["provenance_role"]})
        self.curation["evidence"]["synthetic_proof"] = {"path": item["path"], "sha256": item["sha256"],
                                                       "source_id": "src-FV-PC-synthetic-proof", "lines": [1, 2],
                                                       "range_scope": "Synthetic fixture only", "status": "Synthetic fixture only"}

    def write(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def plan(self, curation=None, allow_draft=False):
        value = curation or self.curation
        return builder.build_plan(self.root, value, digest(dump(value)), allow_draft=allow_draft)

    def apply_fixture(self):
        self.write(PREFIX + "CURATION_INPUT.json", dump(self.curation))
        builder.apply_plan(self.plan())
        for gate in validator.rows(self.root, "frontier/OPEN_PROOF_GATES.jsonl"):
            self.write("frontier/gates/" + gate["gate_id"] + ".json", dump(gate))

    def bridge(self, state="CANDIDATE CONNECTION"):
        interface = {key: "Synthetic fixture only." for key in builder.INTERFACE}
        return {"id": "FV_PC_synthetic_bridge", "state": state, "cards": [self.curation["cards"][0]["id"]],
                "source_subclaim": "Synthetic source only.", "destination_obligation": "Synthetic destination only.",
                "source_interface": copy.deepcopy(interface), "destination_interface": copy.deepcopy(interface),
                "alignment": "Synthetic fixture only.", "missing_lemma": "Synthetic unresolved obligation.",
                "falsifier": "Synthetic planned test only.", "source_ref_ids": ["physical_inventory"],
                "destination_ref_ids": ["computation_inventory"], "transfer_proof_ref_ids": [],
                "counterexample_ref_ids": [], "ref_ids": ["physical_inventory", "computation_inventory"]}

    def test_read_only_plan_preserves_all_repository_bytes(self):
        before = self.snapshot()
        plan = self.plan()
        self.assertGreater(plan.summary()["changed_file_count"], 0)
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.root / "cards").exists())

    def test_unfinished_root_curation_rejected(self):
        value = copy.deepcopy(self.curation)
        value["curation_status"] = "DRAFT_PENDING_ROOT_ADJUDICATION"
        with self.assertRaisesRegex(ValueError, "not ready"):
            self.plan(value)

    def test_explicit_draft_plan_cannot_apply(self):
        value = copy.deepcopy(self.curation)
        value["curation_status"] = "DRAFT_ROOT_REVIEW"
        plan = self.plan(value, allow_draft=True)
        self.assertEqual(plan.summary()["mode"], "read_only_draft_plan")
        with self.assertRaisesRegex(ValueError, "cannot be applied"):
            builder.apply_plan(plan)
        self.assertFalse((self.root / "cards").exists())

    def test_final_curation_requires_root_selected_freeze(self):
        value = copy.deepcopy(self.curation)
        value["selected_freeze"] = None
        with self.assertRaisesRegex(ValueError, "root-frozen selected proof manifest"):
            self.plan(value)

    def test_original_source_hash_change_rejected(self):
        self.write(PREFIX + "package/sources/physical_pasted.txt", b"changed\n")
        with self.assertRaisesRegex(ValueError, "Incoming text bytes changed"):
            self.plan()

    def test_original_manifest_hash_change_rejected(self):
        self.write(PREFIX + "package/SOURCE_MANIFEST.json", b"{}\n")
        with self.assertRaisesRegex(ValueError, "Original incoming manifest changed"):
            self.plan()

    def test_wrong_evidence_hash_rejected(self):
        value = copy.deepcopy(self.curation)
        value["evidence"]["physical_inventory"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "bytes/hash"):
            self.plan(value)

    def test_invalid_inclusive_line_range_rejected(self):
        value = copy.deepcopy(self.curation)
        value["evidence"]["physical_inventory"]["lines"] = [1, 99999]
        with self.assertRaisesRegex(ValueError, "Invalid evidence range"):
            self.plan(value)

    def test_unselected_research_cannot_be_indexed(self):
        value = copy.deepcopy(self.curation)
        value["sources"][-1]["path"] = PREFIX + "package/root/UNFINISHED.md"
        self.write(value["sources"][-1]["path"], self.proof)
        with self.assertRaisesRegex(ValueError, "exact original-plus-root-frozen|exact original|exact original|Package differs"):
            self.plan(value)

    def test_numeric_route_collision_rejected(self):
        self.write("indexes/claims.jsonl", b'{"id":"N990001-existing-unrelated"}\n')
        with self.assertRaisesRegex(ValueError, "Numeric route collision"):
            self.plan()

    def test_root_reserved_routes_must_match_exactly(self):
        value = copy.deepcopy(self.curation)
        value["reserved_routes"].append("N990004")
        with self.assertRaisesRegex(ValueError, "root-reserved routes"):
            self.plan(value)

    def test_append_only_heterogeneous_metadata_and_idempotence(self):
        before = (self.root / "indexes/source_metadata.jsonl").read_bytes()
        self.apply_fixture()
        self.assertTrue((self.root / "indexes/source_metadata.jsonl").read_bytes().startswith(before))
        self.assertEqual(self.plan().summary()["changed_file_count"], 0)
        self.assertEqual(builder.apply_plan(self.plan()), 0)

    def test_changed_immutable_output_rejected(self):
        self.apply_fixture()
        self.write("cards/" + self.curation["cards"][0]["id"] + ".txt", b"changed\n")
        with self.assertRaisesRegex(ValueError, "Immutable artifact collision"):
            self.plan()

    def test_concurrent_registry_change_rejected_before_writes(self):
        plan = self.plan()
        self.write("indexes/source_metadata.jsonl", b'{"concurrent":"change"}\n')
        with self.assertRaisesRegex(ValueError, "Concurrent modification"):
            builder.apply_plan(plan)
        self.assertFalse((self.root / "cards").exists())

    def test_concurrent_frozen_proof_change_rejected_before_live_writes(self):
        plan = self.plan()
        self.write(self.selection["files"][0]["path"], b"concurrent change\n")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            builder.apply_plan(plan)
        self.assertFalse((self.root / "cards").exists())

    def test_concurrent_package_addition_rejected_before_copy(self):
        plan = preserver.plan_copy(self.root, dump(self.selection), "SELECTED_FREEZE.v0002.json", research_root=self.research)
        self.write(PREFIX + "package/root/UNSELECTED.md", b"unselected\n")
        with self.assertRaisesRegex(ValueError, "Concurrent package inventory change"):
            preserver.apply_copy(plan)
        self.assertFalse((self.update / "SELECTED_FREEZE.v0002.json").exists())

    def test_selected_derived_proof_cannot_be_relabelled_supplied(self):
        value = copy.deepcopy(self.curation)
        value["sources"][-1]["provenance_role"] = "supplied_original_text"
        with self.assertRaisesRegex(ValueError, "provenance role changed"):
            self.plan(value)

    def test_root_freeze_status_required_before_copy(self):
        value = copy.deepcopy(self.selection)
        value["status"] = "DRAFT_NOT_FROZEN"
        with self.assertRaisesRegex(ValueError, "not ready"):
            preserver.plan_copy(self.root, dump(value), "SELECTED_FREEZE.v0002.json", research_root=self.research)

    def test_selected_source_hash_required_before_copy(self):
        (self.research / "root/SYNTHETIC_PROOF.md").write_bytes(b"changed\n")
        with self.assertRaisesRegex(ValueError, "Selected research bytes changed"):
            preserver.plan_copy(self.root, dump(self.selection), "SELECTED_FREEZE.v0002.json", research_root=self.research)

    def test_frozen_destination_hash_change_rejected(self):
        self.write(self.selection["files"][0]["path"], b"changed\n")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.plan()

    def test_preservation_copy_is_idempotent(self):
        plan = preserver.plan_copy(self.root, dump(self.selection), "SELECTED_FREEZE.v0001.json", research_root=self.research)
        self.assertEqual(preserver.apply_copy(plan), 0)

    def test_copy_collision_preserves_existing_bytes(self):
        raw = b"New synthetic bytes.\n"
        (self.research / "root/SYNTHETIC_PROOF.md").write_bytes(raw)
        value = copy.deepcopy(self.selection)
        value["files"][0].update({"sha256": digest(raw), "bytes": len(raw)})
        value["total_bytes"] = len(raw)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Immutable preservation collision"):
            preserver.plan_copy(self.root, dump(value), "SELECTED_FREEZE.v0002.json", research_root=self.research)
        self.assertEqual(self.snapshot(), before)

    def test_duplicate_selected_destination_rejected(self):
        value = copy.deepcopy(self.selection)
        value["files"].append(copy.deepcopy(value["files"][0]))
        value["total_files"] = 2
        value["total_bytes"] *= 2
        with self.assertRaisesRegex(ValueError, "Duplicate selected destination"):
            selection_records(value, research_root=self.research)

    def test_archive_pdf_and_coordinate_payloads_rejected(self):
        for suffix in [".pdf", ".zip", ".tar.gz", ".xyz", ".npz", ".data"]:
            with self.subTest(suffix=suffix):
                value = copy.deepcopy(self.selection)
                value["files"][0]["path"] = PREFIX + "package/root/payload" + suffix
                with self.assertRaisesRegex(ValueError, "Excluded PDF/archive/full-network/coordinate"):
                    selection_records(value, research_root=self.research)

    def test_external_fulltext_and_full_lj_flags_rejected(self):
        for field in ["contains_external_fulltext", "contains_full_lj_network_or_coordinates"]:
            with self.subTest(field=field):
                value = copy.deepcopy(self.selection)
                value["files"][0][field] = True
                with self.assertRaisesRegex(ValueError, "explicitly exclude"):
                    selection_records(value, research_root=self.research)

    def test_literature_role_preserves_receipts_only(self):
        value = copy.deepcopy(self.selection)
        value["files"][0]["provenance_role"] = "acquired_primary_literature_receipt"
        with self.assertRaisesRegex(ValueError, "receipts/pointers only"):
            selection_records(value, research_root=self.research)

    def test_selected_path_traversal_rejected(self):
        value = copy.deepcopy(self.selection)
        value["files"][0]["research_relative_path"] = "../outside.md"
        with self.assertRaisesRegex(ValueError, "Unsafe repository path"):
            selection_records(value, research_root=self.research)

    def test_symlinked_evidence_parent_rejected(self):
        target = self.root / "elsewhere"
        target.mkdir()
        (target / "SYNTHETIC_PROOF.md").write_bytes(self.proof)
        shutil.rmtree(self.update / "package/root")
        (self.update / "package/root").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlink evidence"):
            verify_selection(self.root, self.curation["selected_freeze"])

    def test_positive_bridge_requires_completed_transfer_reference(self):
        for state in ["PROVEN LOGICAL DEPENDENCY", "ESTABLISHED COMPATIBLE INTERFACE"]:
            with self.subTest(state=state):
                value = copy.deepcopy(self.curation)
                value["bridges"] = [self.bridge(state)]
                with self.assertRaisesRegex(ValueError, "completed transfer proof reference"):
                    self.plan(value)

    def test_refuted_transfer_requires_executed_argument_reference(self):
        value = copy.deepcopy(self.curation)
        value["bridges"] = [self.bridge("REFUTED TRANSFER")]
        with self.assertRaisesRegex(ValueError, "executed counterexample/argument"):
            self.plan(value)

    def test_bridge_retains_both_interfaces_and_evidence(self):
        value = copy.deepcopy(self.curation)
        value["bridges"] = [self.bridge()]
        plan = self.plan(value)
        bridge = json.loads(plan.after["mechanisms/bridges/FV_PC_synthetic_bridge.json"])
        self.assertEqual(bridge["source_subclaim"], "Synthetic source only.")
        self.assertEqual(bridge["destination_obligation"], "Synthetic destination only.")
        self.assertEqual(bridge["source_evidence_refs"][0]["id"], "physical_inventory")
        self.assertEqual(bridge["destination_evidence_refs"][0]["id"], "computation_inventory")
        self.assertEqual(bridge["state"], "CANDIDATE CONNECTION")

    def test_internal_completeness_does_not_promote_external_status(self):
        value = copy.deepcopy(self.curation)
        value["cards"][0]["internal_proof_status"] = "complete_internal_proof"
        plan = self.plan(value)
        status = json.loads(plan.after["frontier/cards/" + value["cards"][0]["id"] + ".json"])
        self.assertEqual(status["claim_status"], "source_derived_unreviewed")
        self.assertTrue(all(status["validation"][key] == "UNKNOWN" for key in ["external_correctness", "historical_priority", "physical_capability", "formal_verification", "empirical_confirmation"]))
        gates = [json.loads(row) for row in plan.after["frontier/OPEN_PROOF_GATES.jsonl"].decode().splitlines()]
        self.assertEqual(len(gates), 6)
        self.assertTrue(all(gate["status"] == "open" and gate["completion_evidence"] == [] for gate in gates))

    def test_exact_owned_validator_ignores_unrelated_prefix_gate(self):
        self.apply_fixture()
        path = self.root / "frontier/OPEN_PROOF_GATES.jsonl"
        path.write_bytes(path.read_bytes() + b'{"gate_id":"G-FV-PC-UNRELATED","status":"open"}\n')
        with mock.patch.object(validator, "git", side_effect=AssertionError("No Git in scoped validation")):
            result = validator.validate(self.root, "integrated", self.curation["base_revision"])
        self.assertEqual(result["status"], "SCOPED_PASS")
        self.assertTrue(result["exact_owned_ID_selection"])
        self.assertEqual(result["open_gates"], 6)
        self.assertEqual(result["preserved_inherited_schema_failures"], 3)

    def test_git_checks_require_explicit_later_authorization(self):
        with self.assertRaisesRegex(ValueError, "separate root authorization"):
            validator.validate(self.root, "skeleton", check_global=True)

    def test_live_apply_requires_explicit_root_authorization(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        args = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply",
                "--expect-input-sha256", digest(input_path.read_bytes())]
        with mock.patch.object(sys, "argv", args), mock.patch.object(builder, "git", side_effect=AssertionError("Git must not run")):
            with self.assertRaisesRegex(ValueError, "explicit root authorization"):
                builder.main()
        self.assertFalse((self.root / "cards").exists())

    def test_stale_head_apply_rejected_without_writes(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        args = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply",
                "--root-authorized-apply", "--expect-input-sha256", digest(input_path.read_bytes())]
        with mock.patch.object(sys, "argv", args), mock.patch.object(builder, "git", return_value="0" * 40):
            with self.assertRaisesRegex(ValueError, "HEAD changed"):
                builder.main()
        self.assertFalse((self.root / "cards").exists())

    def test_changed_remote_apply_rejected_without_writes(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        args = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply",
                "--root-authorized-apply", "--expect-input-sha256", digest(input_path.read_bytes())]
        with mock.patch.object(sys, "argv", args), mock.patch.object(builder, "git", side_effect=[self.curation["base_revision"], "0" * 40 + "\trefs/heads/main"]):
            with self.assertRaisesRegex(ValueError, "Remote main changed"):
                builder.main()
        self.assertFalse((self.root / "cards").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
