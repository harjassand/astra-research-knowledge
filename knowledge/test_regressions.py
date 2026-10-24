"""Exposed diagnostics and actual current-packet checks, not held-out evaluation."""
import unittest

from knowledge.retrieve import Library


class CorpusRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_exposed_relative_entropy_query_routes_n675(self):
        response = self.library.search("Compare quantum measurements by relative entropy for every pair of input states and any untouched auxiliary quantum system.")
        self.assertTrue(response["results"][0]["id"].startswith("N675-"))

    def test_named_compiler_and_late_units_are_linked(self):
        response = self.library.search("ordered-word inverse-Jordan compiler")
        self.assertEqual(response["results"][0]["id"], "U675-ordered-word-compiler")
        packet = self.library.packet(["N684"], max_bytes=262144)["packets"][0]
        self.assertIn("U684-zero-rate-helper", {item["id"] for item in packet["related_units"]})

    def test_compiler_support_is_actual_gap_statement(self):
        source = self.library.source("U675-ordered-word-compiler")
        self.assertIn("positive gap is essential", source["text"])
        self.assertIn("Suffix closure preserves", source["text"])

    def test_review_applies_at_actual_unit_version_not_every_card(self):
        accepted = self.library.resolve("U947-contrast-reset")["review_overlays"]
        self.assertEqual(accepted[0]["decision"], "accepted_internally_verified")
        self.assertEqual(self.library.resolve("U675-ordered-word-compiler")["review_overlays"], [])

    def test_compatible_analogy_and_refuted_routes_remain_distinct(self):
        expectations = [("U947-reset-amplification", "ESTABLISHED COMPATIBLE INTERFACE"),
                        ("U947-exposed-key-obstruction", "REFUTED TRANSFER"),
                        ("U959-local-guard-acquisition", "CANDIDATE CONNECTION")]
        for destination, state in expectations:
            with self.subTest(destination=destination):
                result = self.library.bridge("U947-contrast-reset", destination)
                self.assertEqual(result["transfers"][0]["state"], state)

    def test_current_material_axis_correction_is_not_dropped(self):
        source = self.library.source("U960-material-axis-correction")
        self.assertIn("both", source["text"])
        self.assertIn("stable", source["text"])
        self.assertIn("does not survive", source["text"])

    def test_extracted_unit_keeps_parent_prerequisite_notice_context(self):
        parent = self.library.resolve("N684")
        unit = self.library.resolve("U684-zero-rate-helper")
        expected = {notice["dependency"] for notice in parent["notices"] if "dependency" in notice}
        inherited = {notice["dependency"] for notice in unit["notices"] if "dependency" in notice}
        self.assertTrue(expected)
        self.assertEqual(expected, inherited)
        self.assertTrue(all(notice.get("context_only_notice") for notice in unit["notices"]))


if __name__ == "__main__":
    unittest.main()
