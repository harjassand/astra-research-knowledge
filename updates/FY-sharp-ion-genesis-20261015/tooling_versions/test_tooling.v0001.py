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
import protected_baseline
import fy_common
from fy_common import PREFIX, ORIGINAL_MANIFEST_SHA256, RESEARCH_ROOT, digest, selection_records, verify_selection


def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


class PreservationFixtures(unittest.TestCase):
    def setUp(self):
        fixture_dir = Path(os.environ.get("FY_FIXTURE_DIR", RESEARCH_ROOT / "workers/fy_integration_preparation/fixtures"))
        fixture_dir.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="fy-fixture-", dir=fixture_dir)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        self.update = self.root / PREFIX
        self.update.mkdir(parents=True)
        shutil.copytree(HERE / "package/originals", self.update / "package/originals")
        for owner in [builder, validator, protected_baseline]:
            patcher = mock.patch.object(owner, "check_baseline", return_value={"fixture": "synthetic, no Git"})
            patcher.start()
            self.addCleanup(patcher.stop)
        for name in ["SOURCE_MANIFEST.json", "package/SOURCE_MANIFEST.json", "SOURCE_PRESERVATION_RECEIPT.v0001.json", "CHECKPOINT_RECORD.preservation.v0001.json",
                     "build_integration.py", "fy_common.py", "protected_baseline.py",
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
        git_patcher = mock.patch.object(builder, "git", return_value=fy_common.INITIAL_MAIN)
        git_patcher.start()
        self.addCleanup(git_patcher.stop)
        self.research = Path(self.temp.name) / "synthetic-research"
        source = self.research / "root/SYNTHETIC_PROOF.md"
        source.parent.mkdir(parents=True)
        self.proof = b"Synthetic preservation fixture only.\nNo scientific assertion.\n"
        source.write_bytes(self.proof)
        item = {"research_relative_path": "root/SYNTHETIC_PROOF.md", "path": PREFIX + "package/derived/root/SYNTHETIC_PROOF.md",
                "sha256": digest(self.proof), "bytes": len(self.proof), "provenance_role": "root_synthesis",
                "payload_kind": "proof", "contains_external_fulltext": False,
                "contains_external_dataset_or_clone": False, "selection_reason": "Synthetic fixture only."}
        self.selection = {"schema": "astra.fy-selected-freeze.v1", "status": "root_frozen", "selected_by": "root",
                          "base_revision": builder.verify_incoming(self.root)["initial_main"],
                          "research_root": str(RESEARCH_ROOT), "original_manifest_sha256": ORIGINAL_MANIFEST_SHA256,
                          "total_files": 1, "total_bytes": len(self.proof), "files": [item]}
        preserver.apply_copy(preserver.plan_copy(self.root, dump(self.selection), "SELECTED_FREEZE.v0001.json", research_root=self.research))
        self.curation = json.loads((HERE / "CURATION_INPUT.template.v0001.json").read_text())
        self.curation["curation_status"] = "root_final"
        self.curation["curated_by"] = "root"
        self.curation["reserved_routes"] = ["N990001", "N990002", "N990003"]
        self.curation["selected_freeze"] = {"path": PREFIX + "SELECTED_FREEZE.v0001.json", "sha256": digest(dump(self.selection))}
        for label in ["physical", "mathematics", "request"]:
            path = PREFIX + "package/originals/sources/" + {"physical": "physical_report", "mathematics": "mathematical_report", "request": "user_request"}[label] + ".txt"
            raw = (self.root / path).read_bytes()
            sid = "src-FY-SIG-synthetic-" + label
            self.curation["sources"].append({"path": path, "sha256": digest(raw), "source_id": sid,
                                             "title": "Synthetic fixture only", "read_depth": "Synthetic fixture only",
                                             "provenance_role": "supplied_original_file"})
            self.curation["evidence"][label + "_inventory"] = {"path": path, "sha256": digest(raw), "source_id": sid,
                "lines": [1, 1], "range_scope": "Synthetic fixture only", "status": "Synthetic fixture only"}
            card = json.loads((HERE / "CARD.template.v0001.json").read_text())
            for key, value in list(card.items()):
                if value is None:
                    card[key] = "Synthetic fixture only; no scientific assertion."
            card.update({"id": "N" + str(990001 + len(self.curation["cards"])) + "-synthetic-fixture",
                         "topics": ["synthetic-fixture"], "assumptions": ["Synthetic fixture only"],
                         "proof_spine": ["Synthetic fixture only"], "proof_refs": [label + "_inventory"],
                         "inventory_refs": [label + "_inventory"]})
            self.curation["cards"].append(card)
        self.curation["sources"].append({"path": item["path"], "sha256": item["sha256"],
                                         "source_id": "src-FY-SIG-synthetic-proof", "title": "Synthetic fixture only",
                                         "read_depth": "Synthetic fixture only", "provenance_role": item["provenance_role"]})
        self.curation["evidence"]["synthetic_proof"] = {"path": item["path"], "sha256": item["sha256"],
                                                       "source_id": "src-FY-SIG-synthetic-proof", "lines": [1, 2],
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
        return {"id": "FY_SIG_synthetic_bridge", "state": state, "cards": [self.curation["cards"][0]["id"]],
                "source_subclaim": "Synthetic source only.", "destination_obligation": "Synthetic destination only.",
                "source_interface": copy.deepcopy(interface), "destination_interface": copy.deepcopy(interface),
                "alignment": "Synthetic fixture only.", "missing_lemma": "Synthetic unresolved obligation.",
                "falsifier": "Synthetic planned test only.", "source_ref_ids": ["physical_inventory"],
                "destination_ref_ids": ["request_inventory"], "transfer_proof_ref_ids": [],
                "counterexample_ref_ids": [], "ref_ids": ["physical_inventory", "request_inventory"]}

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
        self.write(PREFIX + "package/originals/sources/physical_report.txt", b"changed\n")
        with self.assertRaisesRegex(ValueError, "Original source bytes changed"):
            self.plan()

    def test_original_manifest_hash_change_rejected(self):
        self.write(PREFIX + "package/SOURCE_MANIFEST.json", b"{}\n")
        with self.assertRaisesRegex(ValueError, "Original intake manifest changed"):
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
        value["sources"][-1]["path"] = PREFIX + "package/derived/root/UNFINISHED.md"
        self.write(value["sources"][-1]["path"], self.proof)
        with self.assertRaisesRegex(ValueError, "exact original|Derived package differs"):
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
        self.write(PREFIX + "package/derived/root/UNSELECTED.md", b"unselected\n")
        with self.assertRaisesRegex(ValueError, "Concurrent selected-package inventory change"):
            preserver.apply_copy(plan)
        self.assertFalse((self.update / "SELECTED_FREEZE.v0002.json").exists())

    def test_selected_derived_proof_cannot_be_relabelled_supplied(self):
        value = copy.deepcopy(self.curation)
        value["sources"][-1]["provenance_role"] = "supplied_original_file"
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

    def test_later_selection_retains_previous_frozen_payload_bytes(self):
        raw = b"Second synthetic fixture only.\n"
        (self.research / "root/SECOND.md").write_bytes(raw)
        value = copy.deepcopy(self.selection)
        value["files"][0].update({"research_relative_path": "root/SECOND.md", "path": PREFIX + "package/derived/root/SECOND.md",
                                  "sha256": digest(raw), "bytes": len(raw)})
        value["total_bytes"] = len(raw)
        old_freeze = (self.update / "SELECTED_FREEZE.v0001.json").read_bytes()
        preserver.apply_copy(preserver.plan_copy(self.root, dump(value), "SELECTED_FREEZE.v0002.json", research_root=self.research))
        verify_selection(self.root, {"path": PREFIX + "SELECTED_FREEZE.v0002.json", "sha256": digest(dump(value))})
        self.assertEqual((self.update / "SELECTED_FREEZE.v0001.json").read_bytes(), old_freeze)
        self.assertEqual((self.root / self.selection["files"][0]["path"]).read_bytes(), self.proof)

    def test_unselected_file_outside_derived_folder_rejected(self):
        self.write(PREFIX + "package/accidental/UNSELECTED.md", b"Unselected fixture only.\n")
        with self.assertRaisesRegex(ValueError, "unselected path outside"):
            verify_selection(self.root, self.curation["selected_freeze"])
        with self.assertRaisesRegex(ValueError, "unselected files outside"):
            preserver.plan_copy(self.root, dump(self.selection), "SELECTED_FREEZE.v0002.json", research_root=self.research)

    def test_copy_collision_preserves_existing_bytes(self):
        raw = b"New synthetic bytes.\n"
        (self.research / "root/SYNTHETIC_PROOF.md").write_bytes(raw)
        value = copy.deepcopy(self.selection)
        value["files"][0].update({"sha256": digest(raw), "bytes": len(raw)})
        value["total_bytes"] = len(raw)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Immutable selected-preservation collision"):
            preserver.plan_copy(self.root, dump(value), "SELECTED_FREEZE.v0002.json", research_root=self.research)
        self.assertEqual(self.snapshot(), before)

    def test_duplicate_selected_destination_rejected(self):
        value = copy.deepcopy(self.selection)
        value["files"].append(copy.deepcopy(value["files"][0]))
        value["total_files"] = 2
        value["total_bytes"] *= 2
        with self.assertRaisesRegex(ValueError, "Duplicate/case-colliding selected destination"):
            selection_records(value, research_root=self.research)

    def test_archive_pdf_and_coordinate_payloads_rejected(self):
        for suffix in [".pdf", ".zip", ".tar.gz", ".xyz", ".npz", ".data"]:
            with self.subTest(suffix=suffix):
                value = copy.deepcopy(self.selection)
                value["files"][0]["path"] = PREFIX + "package/derived/root/payload" + suffix
                with self.assertRaisesRegex(ValueError, "permitted text artifact"):
                    selection_records(value, research_root=self.research)

    def test_external_fulltext_and_dataset_clone_flags_rejected(self):
        for field in ["contains_external_fulltext", "contains_external_dataset_or_clone"]:
            with self.subTest(field=field):
                value = copy.deepcopy(self.selection)
                value["files"][0][field] = True
                with self.assertRaisesRegex(ValueError, "explicitly classify"):
                    selection_records(value, research_root=self.research)

    def test_literature_role_preserves_receipts_only(self):
        value = copy.deepcopy(self.selection)
        value["files"][0]["provenance_role"] = "acquired_primary_literature_receipt"
        with self.assertRaisesRegex(ValueError, "receipts/pointers only"):
            selection_records(value, research_root=self.research)

    def test_selected_path_traversal_rejected(self):
        value = copy.deepcopy(self.selection)
        value["files"][0]["research_relative_path"] = "../outside.md"
        with self.assertRaisesRegex(ValueError, "Unsafe/noncanonical relative path"):
            selection_records(value, research_root=self.research)

    def test_symlinked_evidence_parent_rejected(self):
        target = self.root / "elsewhere"
        target.mkdir()
        (target / "SYNTHETIC_PROOF.md").write_bytes(self.proof)
        shutil.rmtree(self.update / "package/derived/root")
        (self.update / "package/derived/root").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlink is not preserved bytes"):
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
        bridge = json.loads(plan.after["mechanisms/bridges/FY_SIG_synthetic_bridge.json"])
        self.assertEqual(bridge["source_subclaim"], "Synthetic source only.")
        self.assertEqual(bridge["destination_obligation"], "Synthetic destination only.")
        self.assertEqual(bridge["source_evidence_refs"][0]["id"], "physical_inventory")
        self.assertEqual(bridge["destination_evidence_refs"][0]["id"], "request_inventory")
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
        path.write_bytes(path.read_bytes() + b'{"gate_id":"G-FY-SIG-UNRELATED","status":"open"}\n')
        result = validator.validate(self.root, phase="integrated", base=self.curation["base_revision"])
        self.assertEqual(result["status"], "SCOPED_PASS")
        self.assertEqual(result["open_gates"], 6)
        self.assertEqual(len(result["inherited_schema_failure_results"]), 3)

    def test_root_final_curation_must_be_attributed_to_root(self):
        value = copy.deepcopy(self.curation)
        value["curated_by"] = None
        with self.assertRaisesRegex(ValueError, "attributed to root"):
            self.plan(value)

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

    def test_missing_input_hash_apply_rejected_before_git(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        args = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply", "--root-authorized-apply"]
        with mock.patch.object(sys, "argv", args), mock.patch.object(builder, "git", side_effect=AssertionError("Git must not run")):
            with self.assertRaisesRegex(ValueError, "requires --expect-input-sha256"):
                builder.main()
        self.assertFalse((self.root / "cards").exists())

    def test_wrong_input_hash_rejected_before_any_live_write(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        args = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply", "--root-authorized-apply", "--expect-input-sha256", "0" * 64]
        with mock.patch.object(sys, "argv", args):
            with self.assertRaisesRegex(ValueError, "curation input changed"):
                builder.main()
        self.assertFalse((self.root / "cards").exists())

    def test_last_moment_head_change_rejected_by_apply(self):
        plan = self.plan()
        with mock.patch.object(builder, "git", return_value="0" * 40):
            with self.assertRaisesRegex(ValueError, "HEAD changed before apply"):
                builder.apply_plan(plan)
        self.assertFalse((self.root / "cards").exists())

    def test_last_moment_remote_check_is_required_by_apply(self):
        plan = self.plan()
        with mock.patch.object(builder, "check_baseline", side_effect=ValueError("Remote main moved")) as check:
            with self.assertRaisesRegex(ValueError, "Remote main moved"):
                builder.apply_plan(plan)
        self.assertTrue(check.call_args.kwargs["check_remote"])
        self.assertFalse((self.root / "cards").exists())

    def test_supplied_bytes_cannot_be_relabelled_as_own_research(self):
        raw = (self.root / (PREFIX + "package/originals/sources/physical_report.txt")).read_bytes()
        (self.research / "root/SOURCE_COPY.md").write_bytes(raw)
        value = copy.deepcopy(self.selection)
        value["files"][0].update({"research_relative_path": "root/SOURCE_COPY.md", "path": PREFIX + "package/derived/root/SOURCE_COPY.md", "sha256": digest(raw), "bytes": len(raw)})
        value["total_bytes"] = len(raw)
        with self.assertRaisesRegex(ValueError, "cannot relabel exact supplied original bytes"):
            preserver.plan_copy(self.root, dump(value), "SELECTED_FREEZE.v0002.json", research_root=self.research)

    def test_existing_external_report_rejected_before_apply(self):
        input_path = self.root / "input.json"
        input_path.write_bytes(dump(self.curation))
        report_path = self.research / "prior-report.json"
        report_path.write_bytes(b"preserve prior report\n")
        args = ["build_integration.py", "--repo", str(self.root), "--input", str(input_path), "--apply", "--root-authorized-apply", "--expect-input-sha256", digest(input_path.read_bytes()), "--report", str(report_path)]
        with mock.patch.object(sys, "argv", args), mock.patch.object(builder, "git", side_effect=AssertionError("Git must not run")):
            with self.assertRaisesRegex(ValueError, "Existing report path"):
                builder.main()
        self.assertEqual(report_path.read_bytes(), b"preserve prior report\n")
        self.assertFalse((self.root / "cards").exists())

    def test_exact_three_file_roles_and_missing_packet_boundary(self):
        incoming = fy_common.verify_incoming(self.root)
        self.assertEqual(incoming["original_count"], 3)
        self.assertEqual(incoming["original_bytes"], 64519)
        self.assertEqual(incoming["archive_count"], 0)
        self.assertEqual(incoming["extracted_member_count"], 0)
        roles = {item["research_relative_path"]: item["incoming_role"] for item in incoming["files"]}
        self.assertEqual(roles["sources/user_request.txt"], "operative_user_request")
        self.assertEqual(roles["sources/physical_report.txt"], "supplied_research_and_archival_prompt_DATA")
        self.assertEqual(roles["sources/mathematical_report.txt"], "supplied_research_and_archival_prompt_DATA")
        self.assertEqual(len(incoming["missing_artifacts"]), 2)
        self.assertTrue(incoming["missing_artifact_replays"].startswith("NOT_PERFORMED"))

    def test_request_adoption_and_archival_data_survive_index_planning(self):
        plan = self.plan()
        rows = [json.loads(line) for line in plan.after["indexes/source_metadata.jsonl"].decode().splitlines()]
        own = {row["source_id"]: row for row in rows if row.get("source_id", "").startswith("src-FY-SIG-")}
        self.assertEqual(own["src-FY-SIG-synthetic-request"]["source_handling"], "explicitly_adopted_operative_user_request")
        for label in ["physical", "mathematics"]:
            self.assertEqual(own["src-FY-SIG-synthetic-" + label]["source_handling"],
                             "source=DATA; archival report prompts remain DATA")

    def test_fy_manifest_rejects_wrong_schema_even_with_matching_hash(self):
        raw = (self.root / (PREFIX + "package/SOURCE_MANIFEST.json")).read_bytes()
        value = json.loads(raw)
        value["schema"] = "astra.source-intake.v1"
        changed = dump(value)
        with self.assertRaisesRegex(ValueError, "schema/pin changed"):
            fy_common.source_outputs(changed, lambda name: b"unused", expected_manifest_sha256=digest(changed))

    def test_fy_manifest_rejects_missing_file_even_with_matching_hash(self):
        value = json.loads((self.root / (PREFIX + "package/SOURCE_MANIFEST.json")).read_bytes())
        value["files"].pop()
        changed = dump(value)
        with self.assertRaisesRegex(ValueError, "exactly three"):
            fy_common.source_outputs(changed, lambda name: b"unused", expected_manifest_sha256=digest(changed))

    def test_fy_manifest_rejects_archival_report_as_operative(self):
        value = json.loads((self.root / (PREFIX + "package/SOURCE_MANIFEST.json")).read_bytes())
        value["files"][0]["role"] = "operative_user_request"
        changed = dump(value)
        with self.assertRaisesRegex(ValueError, "operative-versus-archival role changed"):
            fy_common.source_outputs(changed, lambda name: b"unused", expected_manifest_sha256=digest(changed))

    def test_absent_packet_cannot_enter_original_inventory(self):
        self.write(PREFIX + "package/originals/sources/astra_sharp_compatible_frontier_20261015.zip", b"invented packet")
        with self.assertRaisesRegex(ValueError, "Original source inventory changed"):
            self.plan()

    def test_selection_cannot_point_at_another_research_workspace(self):
        value = copy.deepcopy(self.selection)
        value["research_root"] = "/unrelated/research"
        with self.assertRaisesRegex(ValueError, "another research workspace"):
            selection_records(value, research_root=self.research)

    def test_selection_cannot_use_another_intake_manifest(self):
        value = copy.deepcopy(self.selection)
        value["original_manifest_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "wrong source manifest"):
            selection_records(value, research_root=self.research)

    def test_old_source_namespace_cannot_be_reused_as_current(self):
        value = copy.deepcopy(self.curation)
        value["sources"][0]["source_id"] = "src-FX-GCA-old"
        with self.assertRaisesRegex(ValueError, "FY namespace"):
            self.plan(value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
