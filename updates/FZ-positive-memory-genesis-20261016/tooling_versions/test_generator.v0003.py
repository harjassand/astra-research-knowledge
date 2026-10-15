"""Synthetic disposable FZ generator/selection fixtures; no live science or Git writes."""
from pathlib import Path
import copy
import json
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
import fz_common as common
import validate_intake as validator


class GeneratorBoundaries(unittest.TestCase):
    def setUp(self):
        fixtures = HERE / ".fixtures"
        fixtures.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="fz-generator-", dir=fixtures)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        update = self.root / common.PREFIX
        shutil.copytree(HERE / "package/originals", update / "package/originals")
        for name in ("SOURCE_MANIFEST.json", "package/SOURCE_MANIFEST.json", "package/SOURCE_MANIFEST.v0002.json"):
            self.write(common.PREFIX + name, (HERE / name).read_bytes())
        for name, value in {
            "indexes/agent_catalog.json": {"scope": "fixture", "claims": []},
            "indexes/agent_graph.json": {"scope": "fixture", "nodes": [], "edges": []},
            "mechanisms/bridge_candidates.json": {"scope": "fixture", "bridges": [], "rejected_transfers": []},
            "web/catalog.json": [], "indexes/query_aliases.json": {"legacy-alias": "keep"},
        }.items():
            self.write(name, common.encoded(value))
        for name in ("indexes/claims.jsonl", "frontier/CURRENT_CLAIM_STATUS.jsonl", "frontier/OPEN_PROOF_GATES.jsonl", "agent/SEMANTIC_NOTICES.jsonl", "web/documents.jsonl"):
            self.write(name, b"")
        self.write("indexes/source_metadata.jsonl", b'{"id":"legacy-minimal"}\n{"unidentified":"legacy"}\n')
        self.head = "a" * 40
        patcher = mock.patch.object(builder, "check_baseline", return_value={"fixture": True})
        self.boundary = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch.object(builder, "git", return_value=self.head)
        self.git = patcher.start()
        self.addCleanup(patcher.stop)
        self.research = Path(self.temp.name) / "synthetic-research"
        self.proof = b"Synthetic preservation fixture only.\nNo scientific assertion.\n"
        proof_path = self.research / "root/SYNTHETIC.md"
        proof_path.parent.mkdir(parents=True)
        proof_path.write_bytes(self.proof)
        self.item = {"research_relative_path": "root/SYNTHETIC.md", "path": common.PREFIX + "package/derived/root/SYNTHETIC.md",
                     "sha256": common.digest(self.proof), "bytes": len(self.proof), "provenance_role": "root_synthesis",
                     "payload_kind": "proof", "source_origin": "root_authored", "provenance_note": "Synthetic campaign fixture only.",
                     "selection_reason": "Synthetic generator fixture only.", **{flag: False for flag in common.EXTERNAL_FLAGS}}
        self.selection = {"schema": "astra.fz-selected-freeze.v1", "status": "root_frozen", "selected_by": "root",
                          "base_revision": common.INITIAL_MAIN, "research_root": str(common.RESEARCH_ROOT),
                          "original_manifest_sha256": common.ORIGINAL_MANIFEST_SHA256,
                          "total_files": 1, "total_bytes": len(self.proof), "files": [self.item]}
        preserver.apply_copy(preserver.plan_copy(self.root, common.encoded(self.selection), "SELECTED_FREEZE.v0001.json", research_root=self.research))
        original = common.verify_incoming(self.root)["files"][0]
        self.curation = {"schema": builder.SCHEMA, "intake_id": common.INTAKE_ID, "curation_status": "root_final", "curated_by": "root",
                         "base_revision": common.INITIAL_MAIN, "expected_branch_head": self.head, "expected_remote_main": common.INITIAL_MAIN,
                         "date_version": "2026-10-16", "checkpoint_path": None, "checkpoint_draft_path": None,
                         "selected_freeze": {"path": common.PREFIX + "SELECTED_FREEZE.v0001.json", "sha256": common.digest(common.encoded(self.selection))},
                         "sources": [], "evidence": {}, "cards": [], "reserved_routes": [], "notices": [], "bridges": [], "gates": []}
        for label, item in (("original", original), ("proof", self.item)):
            sid = "src-FZ-SIG-synthetic-" + label
            self.curation["sources"].append({"path": item["path"], "sha256": item["sha256"], "source_id": sid,
                                             "title": "Synthetic fixture only", "read_depth": "Synthetic fixture only",
                                             "provenance_role": item["provenance_role"]})
            self.curation["evidence"][label] = {"path": item["path"], "sha256": item["sha256"], "source_id": sid,
                                                "lines": [1, 1 if label == "original" else 2], "range_scope": "Synthetic fixture only", "status": "Synthetic fixture only"}
        for number in range(990001, 990006):
            card = {key: "Synthetic fixture only; no scientific assertion." for key in (
                "title", "scientific_scope", "statement", "costs", "information_acquisition", "obstruction", "comparator",
                "missing_lemma", "next_decisive_step", "read_review_depth", "reported_status", "proof_availability_scope")}
            card.update({"id": "N" + str(number) + "-synthetic-fixture", "topics": ["synthetic-fixture"],
                         "assumptions": ["Synthetic fixture only"], "proof_spine": ["Synthetic fixture only"],
                         "proof_refs": ["proof"], "inventory_refs": ["original"], "proof_availability": "provisional_manuscript_available",
                         "internal_proof_status": "complete_internal_proof"})
            self.curation["cards"].append(card)
            self.curation["reserved_routes"].append("N" + str(number))

    def write(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def snapshot(self):
        return {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}

    def plan(self, curation=None, *, allow_draft=False):
        value = curation or self.curation
        return builder.build_plan(self.root, value, common.digest(common.encoded(value)), allow_draft=allow_draft)

    def test_read_only_plan_preserves_every_repository_byte_and_47_originals(self):
        before = self.snapshot()
        plan = self.plan()
        self.assertGreater(plan.summary()["changed_file_count"], 0)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(common.verify_incoming(self.root)["original_count"], 47)
        self.assertFalse((self.root / "cards").exists())

    def test_finalized_frozen_input_is_required_and_draft_cannot_apply(self):
        value = copy.deepcopy(self.curation)
        value["selected_freeze"] = None
        with self.assertRaisesRegex(ValueError, "root-frozen"):
            self.plan(value)
        value = copy.deepcopy(self.curation)
        value["curation_status"] = "DRAFT_FIXTURE"
        with self.assertRaisesRegex(ValueError, "not ready"):
            self.plan(value)
        plan = self.plan(value, allow_draft=True)
        with self.assertRaisesRegex(ValueError, "cannot be applied"):
            builder.apply_plan(plan)

    def test_head_and_remote_main_are_independent_explicit_contracts(self):
        plan = self.plan()
        self.assertNotEqual(plan.expected_branch_head, plan.expected_remote_main)
        self.boundary.assert_called_with(self.root, immutable_base=common.INITIAL_MAIN, expected_head=self.head,
                                         expected_remote_main=common.INITIAL_MAIN, phase="integrated")
        for key in ("expected_branch_head", "expected_remote_main"):
            value = copy.deepcopy(self.curation)
            del value[key]
            with self.assertRaises(ValueError):
                self.plan(value)

    def test_fixture_application_is_append_only_idempotent_and_unreviewed(self):
        old = (self.root / "indexes/source_metadata.jsonl").read_bytes()
        builder.apply_plan(self.plan())
        self.assertTrue((self.root / "indexes/source_metadata.jsonl").read_bytes().startswith(old))
        self.assertEqual(self.plan().summary()["changed_file_count"], 0)
        for line in (self.root / "frontier/CURRENT_CLAIM_STATUS.jsonl").read_text().splitlines():
            record = json.loads(line)
            self.assertEqual(record["claim_status"], "source_derived_unreviewed")
            self.assertTrue(all(record["validation"][key] == "UNKNOWN" for key in ("external_correctness", "historical_priority", "physical_capability", "formal_verification", "empirical_confirmation")))

    def test_scoped_internal_proof_attestation_keeps_external_validation_unknown(self):
        value = copy.deepcopy(self.curation)
        value["cards"][0]["internal_proof_status"] = "scoped_internal_proofs_and_separately_marked_open_obligations"
        plan = self.plan(value)
        record = json.loads(plan.after["frontier/cards/" + value["cards"][0]["id"] + ".json"])
        self.assertEqual(record["proof_availability"]["internal_proof_status"], value["cards"][0]["internal_proof_status"])
        self.assertEqual(record["claim_status"], "source_derived_unreviewed")
        self.assertTrue(all(record["validation"][key] == "UNKNOWN" for key in ("external_correctness", "historical_priority", "physical_capability", "formal_verification", "empirical_confirmation")))

    def test_concurrent_registry_change_rejects_before_any_generator_write(self):
        plan = self.plan()
        self.write("indexes/claims.jsonl", b'{"id":"concurrent"}\n')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Concurrent modification"):
            builder.apply_plan(plan)
        self.assertEqual(before, self.snapshot())

    def test_last_moment_head_or_frozen_proof_change_rejects_before_writes(self):
        plan = self.plan()
        before = self.snapshot()
        self.git.return_value = "b" * 40
        with self.assertRaisesRegex(ValueError, "HEAD changed before apply"):
            builder.apply_plan(plan)
        self.assertEqual(before, self.snapshot())
        self.git.return_value = self.head
        self.write(self.item["path"], b"changed\n")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Reference hash mismatch"):
            builder.apply_plan(plan)
        self.assertEqual(before, self.snapshot())

    def test_last_moment_remote_freshness_check_is_required(self):
        builder.apply_plan(self.plan())
        self.assertTrue(any(call.kwargs.get("check_remote") is True
                            and call.kwargs.get("expected_remote_main") == common.INITIAL_MAIN for call in self.boundary.call_args_list))

    def test_original_subtree_allows_pinned_derived_but_selection_rejects_unselected_bytes(self):
        common.verify_incoming(self.root)
        with self.assertRaisesRegex(ValueError, "Source-only package inventory"):
            common.verify_incoming(self.root, source_only=True)
        common.verify_selection(self.root, self.curation["selected_freeze"])
        self.write(common.PREFIX + "package/derived/root/UNSELECTED.md", b"not selected\n")
        with self.assertRaisesRegex(ValueError, "Derived package differs"):
            self.plan()

    def test_unselected_package_path_and_derived_manifest_rewrite_are_rejected(self):
        self.write(common.PREFIX + "package/UNSELECTED.json", b"{}\n")
        with self.assertRaisesRegex(ValueError, "unselected path"):
            self.plan()
        (self.root / common.PREFIX / "package/UNSELECTED.json").unlink()
        path = common.PREFIX + "DERIVED_MANIFEST.v0001.json"
        value = json.loads((self.root / path).read_bytes())
        value["total_files"] += 1
        self.write(path, common.encoded(value))
        with self.assertRaisesRegex(ValueError, "Derived manifest differs"):
            self.plan()

    def test_unselected_index_source_and_provenance_relabelling_are_rejected(self):
        value = copy.deepcopy(self.curation)
        value["sources"][1]["path"] = common.PREFIX + "package/derived/root/NOT_FROZEN.md"
        with self.assertRaisesRegex(ValueError, "exact original or root-frozen"):
            self.plan(value)
        value = copy.deepcopy(self.curation)
        value["sources"][1]["provenance_role"] = "supplied_original_file"
        with self.assertRaisesRegex(ValueError, "provenance role changed"):
            self.plan(value)

    def test_wrong_hash_range_namespace_and_numeric_route_collision_are_rejected(self):
        value = copy.deepcopy(self.curation)
        value["evidence"]["proof"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "not recoverable"):
            self.plan(value)
        value = copy.deepcopy(self.curation)
        value["evidence"]["proof"]["lines"] = [1, 999]
        with self.assertRaisesRegex(ValueError, "Invalid evidence range"):
            self.plan(value)
        value = copy.deepcopy(self.curation)
        value["sources"][1]["source_id"] = "src-FY-SIG-old"
        with self.assertRaisesRegex(ValueError, "FZ namespace"):
            self.plan(value)
        self.write("indexes/claims.jsonl", b'{"id":"N990001-old"}\n')
        with self.assertRaisesRegex(ValueError, "Numeric route collision"):
            self.plan()

    def test_immutable_output_and_reserved_route_changes_are_rejected(self):
        self.write("cards/" + self.curation["cards"][0]["id"] + ".txt", b"collision\n")
        with self.assertRaisesRegex(ValueError, "Immutable artifact collision"):
            self.plan()
        value = copy.deepcopy(self.curation)
        value["reserved_routes"] = value["reserved_routes"][:-1]
        with self.assertRaisesRegex(ValueError, "exact root-reserved routes"):
            self.plan(value)

    def test_selected_origin_must_remain_distinct_from_supplied_and_capital(self):
        item = copy.deepcopy(self.item)
        del item["source_origin"]
        with self.assertRaisesRegex(ValueError, "source_origin"):
            common.check_payload_record(item)
        item = copy.deepcopy(self.item)
        item.update({"source_origin": "located_prior_capital", "origin_path": str(self.research / item["research_relative_path"])})
        with self.assertRaisesRegex(ValueError, "capital_comparison"):
            common.check_payload_record(item)
        item["provenance_role"] = "capital_comparison"
        common.check_payload_record(item)
        selection = copy.deepcopy(self.selection)
        selection["files"] = [item]
        common.selection_records(selection, research_root=self.research, check_research=True)

    def test_explicit_parent_frozen_status_is_supported_but_draft_is_rejected(self):
        selection = copy.deepcopy(self.selection)
        selection["status"] = "FROZEN_ROOT_SELECTED"
        common.selection_records(selection)
        selection["status"] = "DRAFT_NOT_FROZEN"
        with self.assertRaisesRegex(ValueError, "not ready"):
            common.selection_records(selection)

    def test_located_prior_capital_metadata_survives_generator_planning(self):
        self.item.update({"source_origin": "located_prior_capital", "provenance_role": "capital_comparison",
                          "provenance_note": "Synthetic prior authored capital, located independently; not supplied.",
                          "origin_path": str(self.research / self.item["research_relative_path"])})
        raw = common.encoded(self.selection)
        self.write(common.PREFIX + "SELECTED_FREEZE.v0001.json", raw)
        derived_path = common.PREFIX + "DERIVED_MANIFEST.v0001.json"
        derived = json.loads((self.root / derived_path).read_bytes())
        derived.update({"source_freeze": {"path": common.PREFIX + "SELECTED_FREEZE.v0001.json", "sha256": common.digest(raw)}, "files": [self.item]})
        self.write(derived_path, common.encoded(derived))
        self.curation["selected_freeze"]["sha256"] = common.digest(raw)
        self.curation["sources"][1]["provenance_role"] = "capital_comparison"
        plan = self.plan()
        metadata = json.loads(plan.after[common.PREFIX + "INDEXED_SOURCES.json"])["files"][1]
        for key in ("source_origin", "provenance_note", "origin_path"):
            self.assertEqual(metadata[key], self.item[key])

    def test_apply_cli_requires_root_authorization_and_exact_hash_before_git(self):
        path = Path(self.temp.name) / "curation.json"
        raw = common.encoded(self.curation)
        path.write_bytes(raw)
        base_args = ["build_integration.py", "--repo", str(self.root), "--input", str(path), "--apply"]
        for extra, message in (([], "root authorization"), (["--root-authorized-apply"], "expect-input-sha256"),
                               (["--root-authorized-apply", "--expect-input-sha256", "0" * 64], "input changed")):
            self.git.reset_mock()
            before = self.snapshot()
            with mock.patch.object(sys, "argv", base_args + extra), self.assertRaisesRegex(ValueError, message):
                builder.main()
            self.git.assert_not_called()
            self.assertEqual(before, self.snapshot())

    def test_apply_cli_rejects_moved_remote_before_lock_or_live_write(self):
        path = Path(self.temp.name) / "curation.json"
        raw = common.encoded(self.curation)
        path.write_bytes(raw)
        args = ["build_integration.py", "--repo", str(self.root), "--input", str(path), "--apply", "--root-authorized-apply",
                "--expect-input-sha256", common.digest(raw)]
        before = self.snapshot()
        self.git.side_effect = [self.head, "c" * 40 + "\trefs/heads/main"]
        with mock.patch.object(sys, "argv", args), self.assertRaisesRegex(ValueError, "Remote main changed"):
            builder.main()
        self.assertEqual(before, self.snapshot())

    def test_integrated_guard_checks_exact_owned_records_without_promoting_science(self):
        for name in ("PREPARATION_STATE.v0001.json", "PREPARATION_STATE.v0002.json",
                     "CURATION_INPUT.template.v0001.json", "CURATION_INPUT.template.v0002.json",
                     "SELECTED_FREEZE.template.v0001.json", "SELECTED_FREEZE.template.v0002.json",
                     "AUTHORED_FILE.template.v0002.json", "CHECKPOINT_RECORD.preservation.v0001.json",
                     "SOURCE_PRESERVATION_RECEIPT.v0001.json", "build_integration.py"):
            self.write(common.PREFIX + name, (HERE / name).read_bytes())
        real_root = HERE.parents[1]
        self.write("state/publish_checkpoint.py", (real_root / "state/publish_checkpoint.py").read_bytes())
        for name in validator.INHERITED:
            self.write(name, (real_root / name).read_bytes())
        self.write(common.PREFIX + "CURATION_INPUT.json", common.encoded(self.curation))
        builder.apply_plan(self.plan())
        for line in (self.root / "frontier/OPEN_PROOF_GATES.jsonl").read_text().splitlines():
            gate = json.loads(line)
            self.write("frontier/gates/" + gate["gate_id"] + ".json", common.encoded(gate))
        path = self.root / "frontier/OPEN_PROOF_GATES.jsonl"
        path.write_bytes(path.read_bytes() + b'{"gate_id":"G-FZ-SIG-UNRELATED","status":"open"}\n')
        with mock.patch.object(validator, "check_baseline", return_value={"fixture": True}), \
             mock.patch("protected_baseline.check_baseline", return_value={"fixture": True}):
            result = validator.validate(self.root, phase="integrated")
        self.assertEqual(result["integrated_record_check"]["cards"], 5)
        self.assertEqual(result["integrated_record_check"]["open_gates"], 10)
        self.assertFalse(result["scientific_truth_checked"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
