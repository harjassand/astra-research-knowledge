"""Synthetic registry tests. No research/model trial or scientific checker executes."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from research_eval import Registry, BUDGET_KEYS, LEDGERS, digest


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.store = self.base / "public" / "evaluation"
        self.private = self.base / "private"
        self.registry = Registry(self.store, self.private)
        self.statement = self.file("statement", "Synthetic bookkeeping fixture; not a scientific task.")
        self.receipt = self.file("receipt", "Synthetic role/exposure receipt; not scientific verification.")
        self.input = self.file("input", "same common input")
        self.gold = self.file("gold", "do not publish this private reference")
        self.gates = self.file("gates", json.dumps({"success_rule": "all_primary",
            "primary_gate_ids": ["g1"], "gates": [{"gate_id": "g1", "kind": "subtheorem",
            "acceptance": "Synthetic gate for registry tests only", "requirements": ["exact fixture bytes"]}]}))
        self.contract = {"task_id": "fixture", "split": "development", "provider": {
            "identity": "fixture-provider", "independent_from_repository_authors": False,
            "independent_from_run_operators": False, "receipt_file": self.receipt},
            "contamination": {"repository_overlap": "known_overlap",
                "prior_operator_or_worker_exposure": "known_exposed", "foundation_pretraining": "unknown",
                "screening_evidence_file": self.receipt}, "task_statement_file": self.statement,
            "proof_gate_file": self.gates, "common_input_files": [self.input], "private_reference_files": [self.gold]}

    def tearDown(self):
        self.temporary.cleanup()

    def file(self, name, data):
        p = self.base / name
        p.write_text(data)
        return str(p)

    def setup_plan(self):
        task = self.registry.register_task(self.contract)
        h = digest({task["task_id"]: [f for f in task["files"] if f["kind"] in
            ("task_statement", "common_input", "proof_gates")]})
        budget = {k: 1000 for k in BUDGET_KEYS}
        budget["context_tokens"] = 800
        model = {"provider": "fixture", "model_id": "no-model-called",
            "immutable_version": "fixture-1", "reasoning_effort": "none", "context_window_tokens": 1000,
            "tokenizer": "fixture", "tokenizer_version": "1"}
        manifest = self.file("inventory", "fixture inventory with source hashes")
        arms = [{"arm_id": arm, "condition": condition, "model": model,
            "common_information_sha256": h,
            "allowed_information_manifest_sha256": hashlib.sha256(Path(manifest).read_bytes()).hexdigest(),
            "information_manifest_file": manifest, "budget": budget,
            "compute_recipe": "synthetic fixture only, no runtime experiment",
            "tool_policy": "none", "prompt_file": self.statement}
            for arm, condition in [("A", "raw_archive"), ("B", "structured_repository")]]
        self.plan = {"comparison_id": "fixture-comparison", "task_ids": ["fixture"], "replicates": 1,
            "arms": arms, "checker_blinding": "independent_checker_arm_mapping_withheld",
            "charge_setup_and_failed_attempts": True, "randomization_file": self.receipt,
            "primary_metric": "all_primary_proof_gates_passed"}
        return self.plan

    def setup_run(self, usage=None, status="completed"):
        plan = self.registry.register_comparison(self.setup_plan())
        usage = usage or {k: 1 for k in BUDGET_KEYS}
        run = {"run_id": "fixture-run", "comparison_id": "fixture-comparison", "task_id": "fixture",
            "arm_id": "A", "replicate": 1, "started_at": plan["frozen_at"], "ended_at": plan["frozen_at"],
            "status": status, "actual_model": self.plan["arms"][0]["model"], "usage": usage,
            "transcript_file": self.receipt, "resource_receipt_file": self.receipt, "output_files": [self.statement]}
        self.run = run
        return self.registry.record_run(run)

    def outcome(self):
        run = self.setup_run()
        return {"outcome_id": "fixture-outcome", "run_id": run["run_id"], "checker_identity": "fixture-checker",
            "independence_attested": True, "blinded_to_arm_mapping": True,
            "checker_relationship": "external_expert",
            "checked_output_sha256": [hashlib.sha256(Path(self.statement).read_bytes()).hexdigest()],
            "gate_results": [{"gate_id": "g1", "status": "passed", "reason": "Synthetic bookkeeping receipt only"}],
            "evidence_files": [self.receipt], "independence_evidence_file": self.receipt}

    def test_task_gold_and_statement_are_sealed_not_published(self):
        result = self.registry.register_task(self.contract)
        public = (self.store / LEDGERS[0]).read_text()
        self.assertNotIn(Path(self.gold).read_text(), public)
        self.assertNotIn(self.statement, public)
        self.assertNotIn("gate_definition", public)
        self.assertFalse(result["statement_and_gold_public"])
        self.assertEqual(self.registry.validate()["rows"][LEDGERS[0]], 1)

    def test_private_location_inside_repository_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            Registry(self.store, self.store.parent / "private")

    def test_unknown_exposure_cannot_be_unseen(self):
        self.contract["split"] = "unseen_candidate"
        self.contract["provider"]["independent_from_repository_authors"] = True
        self.contract["provider"]["independent_from_run_operators"] = True
        self.contract["contamination"]["repository_overlap"] = "unknown"
        with self.assertRaisesRegex(ValueError, "development-only"):
            self.registry.register_task(self.contract)

    def test_task_sealed_bytes_tampering_rejected(self):
        self.registry.register_task(self.contract)
        target = next(p for p in (self.private / "tasks" / "fixture").iterdir() if p.name.startswith("0000-"))
        target.write_text("changed")
        with self.assertRaisesRegex(ValueError, "evidence changed"):
            self.registry.validate()

    def test_unequal_budget_rejected(self):
        plan = self.setup_plan()
        plan["arms"][1] = copy.deepcopy(plan["arms"][1])
        plan["arms"][1]["budget"]["model_calls"] += 1
        with self.assertRaisesRegex(ValueError, "Unequal comparison field"):
            self.registry.register_comparison(plan)

    def test_hidden_information_imbalance_rejected(self):
        plan = self.setup_plan()
        plan["arms"][1]["allowed_information_manifest_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "same source mathematics"):
            self.registry.register_comparison(plan)

    def test_pre_freeze_run_rejected(self):
        self.setup_run()
        another = dict(self.run, run_id="old-run", arm_id="B", started_at="2000-01-01T00:00:00+00:00")
        with self.assertRaisesRegex(ValueError, "after the frozen"):
            self.registry.record_run(another)

    def test_over_budget_and_unknown_costs_retained_ineligible(self):
        usage = {k: 1 for k in BUDGET_KEYS}
        usage["model_calls"] = 1001
        usage["compute_usd"] = None
        run = self.setup_run(usage)
        self.assertFalse(run["eligible_for_success"])
        self.assertEqual(run["budget_excess"], ["model_calls"])
        self.assertEqual(run["unmeasured_charges"], ["compute_usd"])
        report = self.registry.report("fixture-comparison")
        self.assertFalse(report["complete"])
        self.assertEqual(report["arms"][0]["unknown_cost_runs"], 1)
        self.assertEqual(report["arms"][1]["missing_runs"], 1)

    def test_failure_cannot_be_rerolled(self):
        run = self.setup_run(status="failed")
        self.assertFalse(run["eligible_for_success"])
        again = dict(self.run, run_id="second-run")
        with self.assertRaisesRegex(ValueError, "failures cannot be silently retried"):
            self.registry.record_run(again)

    def test_internal_audit_cannot_be_independent_outcome(self):
        receipt = self.outcome()
        receipt["checker_relationship"] = "internal_audit"
        with self.assertRaisesRegex(ValueError, "Internal/audit"):
            self.registry.record_outcome(receipt)

    def test_checker_output_hash_must_match_submission(self):
        receipt = self.outcome()
        receipt["checked_output_sha256"] = ["f" * 64]
        with self.assertRaisesRegex(ValueError, "exact submitted output"):
            self.registry.record_outcome(receipt)

    def test_all_primary_gates_required_and_receipts_not_certified(self):
        receipt = self.outcome()
        receipt["gate_results"][0]["status"] = "unknown"
        result = self.registry.record_outcome(receipt)
        self.assertFalse(result["primary_success"])
        self.assertEqual(result["independence_status"], "receipt_attested_not_certified_by_registry")
        self.assertFalse(self.registry.validate()["proofs_checked"])


if __name__ == "__main__":
    unittest.main()
