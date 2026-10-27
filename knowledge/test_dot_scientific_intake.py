"""Protect immutable input selection and scoped current scientific acceptance."""
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import unittest

from knowledge.model import ROOT, encoded


INTAKE = ROOT / "research/2026-10-27-dot-scientific"


class DotScientificIntake(unittest.TestCase):
    def test_new_and_affected_default_packets_retain_every_scope_within_budget(self):
        from knowledge.retrieve import Library
        library = Library()
        for identifier in ["N" + str(i) for i in range(1093, 1118)] + ["N993", "N994", "N995", "N1006"]:
            packet = library.packet([identifier])
            packet["checkout_revision"] = "0" * 40
            self.assertLessEqual(len(encoded(packet)), 32768, identifier)

    def test_selected_scientific_bytes_and_explicit_omissions(self):
        spec = importlib.util.spec_from_file_location("dot_payload_verifier", INTAKE / "verify_payloads.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        report = module.verify(INTAKE)
        self.assertEqual(report["historical_unverified_receipt_references"], 9)
        self.assertGreater(report["retained_original_files"], 0)

    def test_new_review_subjects_bind_the_actual_current_content(self):
        records = {row["id"]: row for row in map(json.loads, (ROOT / "knowledge/current/records.jsonl").read_text().splitlines())}
        reviews = list((ROOT / "knowledge/reviews").glob("A11*-dot-*.json"))
        self.assertEqual(len(reviews), 25)
        for path in reviews:
            review = json.loads(path.read_text())
            for subject in review["subjects"]:
                record = records[subject["id"]]
                self.assertEqual(subject["content_version"], record["content_version"], subject["id"])
                self.assertTrue(any(item["id"] == review["id"] for item in record["review_overlays"]), subject["id"])

    def test_optional_overlap_replay_keeps_its_actual_proof_inequalities(self):
        report = json.loads((INTAKE / "validation/morrey-replay.json").read_text())
        self.assertEqual(report["fresh_moment_acquisition"], "NOT_RERUN")
        self.assertTrue(all(row["bitwise_original_match"] for row in report["stored_fields"]["outputs"]))
        overlap = next(row for row in report["comparisons"] if row["path"].endswith("compatible_box_overlap_receipt.json"))
        self.assertTrue(overlap["certified_gain_and_all_other_fields_equal"])
        self.assertNotIn("comparison_guard", overlap)
        self.assertGreater(Fraction(overlap["minimum_gradient_cap_slack"]), 0)
        self.assertGreater(Fraction(overlap["minimum_scalar_negativity_margin"]), 0)
        self.assertEqual({row["field"] for row in overlap["changed_fields"]}, {"guarded_gradient_L1_upper"})
        for row in overlap["changed_fields"]:
            self.assertGreater(Fraction(row["certified_gradient_cap_minus_new_bound"]), 0)
            self.assertGreater(Fraction(row["scalar_negativity_margin_minus_q_minus_bound"]), 0)


if __name__ == "__main__":
    unittest.main()
