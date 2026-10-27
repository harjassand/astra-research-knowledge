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
        parents = {library.resolve("N" + str(i))["id"] for i in range(1093, 1118)}
        units = sorted(record["id"] for record in library.records.values() if parents.intersection(record["parents"]))
        for identifier in sorted(parents) + units + ["N993", "N994", "N995", "N1006"]:
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
        self.assertGreaterEqual(len(reviews), 25)
        for path in reviews:
            review = json.loads(path.read_text())
            for subject in review["subjects"]:
                record = records[subject["id"]]
                if subject["content_version"] == record["content_version"]:
                    self.assertTrue(any(item["id"] == review["id"] for item in record["review_overlays"]), subject["id"])
                else:
                    self.assertTrue(any(item["id"] == review["id"] for item in record["historical_reviews"]), subject["id"])
                    self.assertFalse(any(item["id"] == review["id"] for item in record["review_overlays"]), subject["id"])

    def test_decimal_display_does_not_replace_the_exact_certified_upper(self):
        ledger = INTAKE / "source/morrey_law_first_stress_20261026/cube_brownian_completion/fully_corrective141_half_K48/received_full_Gram_candidate.json"
        upper = Fraction(json.loads(ledger.read_text())["global_negative_mass_upper"])
        self.assertGreater(upper, Fraction("0.004714574814154892"))
        self.assertLess(upper, Fraction("0.004714574814154893"))
        report = json.loads((INTAKE / "validation/morrey-replay.json").read_text())
        certificate = report["adopted_negative_stress_certificate"]
        self.assertEqual(certificate["exact_upper_authority"]["field"], "global_negative_mass_upper")
        self.assertTrue(certificate["outward_decimal_verified_by_exact_rational_comparison"])
        enclosures = json.loads((INTAKE / "validation/decimal-enclosures.json").read_text())
        self.assertEqual(enclosures["checked_enclosures"], 8)
        for row in enclosures["rows"]:
            value = json.loads((INTAKE / row["source"]).read_text())
            for key in row["field"]:
                value = value[key]
            exact, decimal = Fraction(value), Fraction(row["safe_decimal_enclosure"])
            self.assertEqual(exact, Fraction(row["exact_rational"]))
            if row["bound_direction"] == "upper":
                self.assertGreaterEqual(decimal, exact)
            else:
                self.assertLessEqual(decimal, exact)

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
