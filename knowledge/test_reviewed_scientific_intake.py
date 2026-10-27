"""Guard real selection, reviewed-version and resource-branch failures."""
import runpy
import unittest

from knowledge.mcp_adapter import ResearchAdapter
from knowledge.model import ROOT
from knowledge.build import packet_review
from knowledge.test_mcp_adapter import complete


class ReviewedScientificIntake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = ResearchAdapter(ROOT)

    def test_public_subset_reaggregates_without_releasing_excluded_bodies(self):
        check = runpy.run_path(str(ROOT / "research/2026-10-28-reviewed-scientific-intake/verify_selection.py"))
        result = check["verify"]()
        self.assertTrue(result["passed"])
        self.assertEqual(result["numeric_starts"], 12)
        self.assertEqual(result["public_response_bodies"], 8)

    def test_changed_public_availability_has_its_own_exact_review(self):
        record = self.adapter.library.resolve("U1008-cued-prompt-pilot-evidence")
        self.assertEqual(record["version"], 2)
        self.assertIn("withheld", str(record["contract"]))
        self.assertIn("Complete public rescoring is unavailable", str(record["review_overlays"]))
        current = {r["id"] for r in record["review_overlays"]}
        historical = {r["id"] for r in record["historical_reviews"]}
        self.assertIn("A1008-public-selection-arithmetic", current)
        self.assertNotIn("A1008-descriptive-pilot-arithmetic", current)
        self.assertIn("A1008-descriptive-pilot-arithmetic", historical)

    def test_old_variance_budget_keeps_current_sufficiency_correction(self):
        record = self.adapter.library.resolve("U712-state-accuracy-does-not-control-fisher-derivatives")
        self.assertEqual(record["version"], 2)
        self.assertIn("sufficient", str(record["contract"]).lower())
        self.assertIn("not a necessary", str(record["contract"]).lower())
        prior = record["history"][0]
        fetched = complete(self.adapter, self.adapter.register(dict(prior, lines=None)))
        self.assertEqual(fetched["text"].encode(), (ROOT / prior["path"]).read_bytes())
        context = next(c for c in fetched["current_context"] if c["id"] == record["id"])
        self.assertEqual(context["notices"], record["notices"])
        self.assertIn("READOUT-VARIANCE-BUDGET-SUFFICIENCY-CORRECTION", str(context["notices"]))
        self.assertIn("A712-state-accuracy-sufficient-budget-v2", str(record["review_overlays"]))
        self.assertIn("A712-preparation-and-local-refresh-boundaries", str(record["historical_reviews"]))

    def test_rational_resource_example_is_not_relabeled_as_exact_optimum(self):
        check = runpy.run_path(str(ROOT / "research/2026-10-28-reviewed-scientific-intake/verify_resource_example.py"))
        result = check["verify"]()
        self.assertTrue(result["distinct_from_exact_joint_optimum"])
        self.assertEqual(result["stiffness_slack_to_20_02"], "1/10000")

    def test_growing_parent_packet_retains_complete_notices_and_gap_provenance(self):
        library = self.adapter.library
        for identifier in ("N946", "N687", "N952", "N33"):
            record = library.resolve(identifier)
            packet = library.packet([identifier])["packets"][0]
            self.assertEqual(packet["notices"], record["notices"])
            self.assertEqual(packet["contract"], record["contract"])
            for projected, original in zip(packet["review"]["gaps"], record["review"]["gaps"]):
                if not isinstance(projected, dict) or "evidence_ref_indices" not in projected:
                    self.assertEqual(projected, original)
                    continue
                annotations = projected.get("evidence_ref_annotations", [{}] * len(projected["evidence_ref_indices"]))
                restored = [dict(packet["evidence"][index], **extra)
                            for index, extra in zip(projected["evidence_ref_indices"], annotations)]
                self.assertEqual(restored, original["evidence"])
                self.assertEqual(projected["scope"], original["scope"])

    def test_gap_reference_factoring_does_not_blend_conflicting_support(self):
        reference = {"path": "a-proof.md", "sha256": "a" * 64, "lines": [1, 3]}
        conflict = dict(reference, sha256="b" * 64, status="Different historical assertion")
        gap = {"scope": "Actual unresolved condition", "evidence": [conflict]}
        projected = packet_review(gap, [reference], preserve_annotations=True)
        self.assertEqual(projected, gap)
        self.assertNotIn("evidence_ref_indices", projected)


if __name__ == "__main__":
    unittest.main()
