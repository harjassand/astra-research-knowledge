"""Synthetic observational trace checks. No actual research/model trial."""
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from technology.contracts import load
from workflow_trace import ROOT, validate


class WorkflowTraceTests(unittest.TestCase):
    def setUp(self):
        self.record = load(ROOT / "evaluation/workflows/fixtures/unknown.json")

    def add_refs(self):
        self.record["refs"] = copy.deepcopy(load(ROOT / "technology/fixtures/contraction/record.json")["refs"])

    def test_unknown_values_stay_unknown_and_cost_incomplete(self):
        result = validate(self.record)
        self.assertFalse(result["all_usage_recorded"])
        self.assertEqual(result["mode"], "UNKNOWN")
        self.assertTrue(all(v is None for v in self.record["resources"]["usage"].values()))

    def test_five_modes_are_recordable_without_fabricating_usage(self):
        self.record["context"].update(retained_context="Synthetic retained context description",
                                       capital_access="Synthetic selective dossier access")
        for mode, relation in [("targeted_warm_continuation", "same"), ("fresh_direction_retained_context", "same"),
                               ("new_instance", "new"), ("source_intensive_multi_agent", "UNKNOWN"),
                               ("independent_selective_capital", "new")]:
            with self.subTest(mode=mode):
                self.record["mode"] = mode
                self.record["context"]["conversation_relation"] = relation
                self.assertEqual(validate(self.record)["mode"], mode)

    def test_warm_and_new_modes_cannot_exchange_context_relations(self):
        self.record["mode"] = "targeted_warm_continuation"
        with self.assertRaisesRegex(ValueError, "same-conversation"):
            validate(self.record)
        self.record["mode"] = "new_instance"
        with self.assertRaisesRegex(ValueError, "new conversation"):
            validate(self.record)

    def test_exact_prompt_requires_original_bytes(self):
        self.record["prompt_availability"] = "exact"
        with self.assertRaisesRegex(ValueError, "preserved bytes"):
            validate(self.record)
        self.add_refs()
        self.record["prompt_ref_ids"] = ["mechanism"]
        self.assertEqual(validate(self.record)["status"], "missing")

    def test_reported_duration_does_not_fill_measured_usage(self):
        self.add_refs()
        self.record["resources"]["reported_inference_seconds"] = 123
        with self.assertRaisesRegex(ValueError, "duration requires"):
            validate(self.record)
        self.record["resources"]["reported_duration_ref_ids"] = ["mechanism"]
        self.assertFalse(validate(self.record)["all_usage_recorded"])
        self.assertIsNone(self.record["resources"]["usage"]["wall_seconds"])

    def test_measured_zero_requires_receipt_and_unknown_is_not_zero(self):
        self.record["resources"]["usage"]["model_calls"] = 0
        with self.assertRaisesRegex(ValueError, "measured usage requires"):
            validate(self.record)
        self.add_refs()
        self.record["resources"]["usage_receipt_ref_ids"] = ["result"]
        self.assertFalse(validate(self.record)["all_usage_recorded"])

    def test_worker_invocations_and_peak_need_distinct_receipts(self):
        self.record["resources"]["worker_invocations"] = 12
        with self.assertRaisesRegex(ValueError, "worker counts require"):
            validate(self.record)
        self.add_refs()
        self.record["resources"]["worker_receipt_ref_ids"] = ["result"]
        self.assertIsNone(self.record["resources"]["usage"]["parallel_workers"])
        self.assertFalse(validate(self.record)["all_usage_recorded"])

    def test_multi_agent_label_cannot_contradict_measured_peak(self):
        self.add_refs()
        self.record["mode"] = "source_intensive_multi_agent"
        self.record["resources"]["usage"].update(parallel_workers=1)
        self.record["resources"]["usage_receipt_ref_ids"] = ["result"]
        with self.assertRaisesRegex(ValueError, "contradicts recorded"):
            validate(self.record)

    def test_completed_attempt_requires_output_and_failure_is_retained(self):
        self.record["status"] = "completed"
        with self.assertRaisesRegex(ValueError, "exact output"):
            validate(self.record)
        for status in ("failed", "timed_out", "aborted", "missing"):
            self.record["status"] = status
            self.assertEqual(validate(self.record)["status"], status)

    def test_independent_status_requires_output_bound_receipt(self):
        self.add_refs()
        self.record["output_ref_ids"] = ["result"]
        self.record["advance"].update(verification="independent_receipt", evidence_ref_ids=["result"])
        with self.assertRaisesRegex(ValueError, "output-bound independent receipt"):
            validate(self.record)
        self.record["advance"]["verification_receipt"] = {"checked_output_sha256": ["0" * 64],
            "independence_attested": True, "scope": "Synthetic linkage test only", "ref_ids": ["mechanism"]}
        with self.assertRaisesRegex(ValueError, "exact submitted output"):
            validate(self.record)
        self.record["advance"]["verification_receipt"]["checked_output_sha256"] = [self.record["refs"][2]["sha256"]]
        self.assertTrue(validate(self.record)["verification_is_receipt_attestation_only"])

    def test_fixture_cannot_enter_matched_ledger_or_claim_a_score(self):
        self.record["matched_run_id"] = "fake-run"
        with self.assertRaisesRegex(ValueError, "fixtures cannot be linked"):
            validate(self.record)
        self.record["matched_run_id"] = None
        self.record["prompting_advantage_score"] = 10
        with self.assertRaisesRegex(ValueError, "unexpected fields"):
            validate(self.record)

    def test_matched_link_binds_output_usage_model_and_status(self):
        self.add_refs()
        self.record.update(fixture=False, matched_run_id="synthetic-run", status="failed", output_ref_ids=["result"])
        self.record["model"]["model_id"] = "synthetic-model"
        row = {"kind": "run_record", "run_id": "synthetic-run", "status": "failed",
               "actual_model": {"model_id": "synthetic-model"},
               "usage": copy.deepcopy(self.record["resources"]["usage"]),
               "files": [{"kind": "output", "sha256": self.record["refs"][2]["sha256"]}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for ref in self.record["refs"]:
                p = root / ref["path"]
                p.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / ref["path"], p)
            (root / "evaluation").mkdir()
            (root / "evaluation/MODEL_COMPARISONS.jsonl").write_text(json.dumps(row) + "\n")
            self.assertEqual(validate(self.record, root)["status"], "failed")
            self.record["model"]["model_id"] = "different-model"
            with self.assertRaisesRegex(ValueError, "model differs"):
                validate(self.record, root)
            self.record["model"]["model_id"] = "synthetic-model"
            self.record["status"] = "completed"
            with self.assertRaisesRegex(ValueError, "status differs"):
                validate(self.record, root)
            self.record["status"] = "failed"
            self.record["output_ref_ids"] = ["mechanism"]
            with self.assertRaisesRegex(ValueError, "outputs differ"):
                validate(self.record, root)

    def test_mutable_model_label_cannot_claim_immutable_version(self):
        self.record["model"]["immutable_version"] = "latest"
        with self.assertRaisesRegex(ValueError, "must be null"):
            validate(self.record)


if __name__ == "__main__":
    unittest.main()
