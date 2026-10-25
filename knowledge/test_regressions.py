"""Exposed diagnostics and actual current-packet checks, not held-out evaluation."""
import json
import shlex
import subprocess
import sys
import unittest

from knowledge.model import ROOT, compact_ref, evidence_refs
from knowledge.retrieve import Library


class CorpusRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_exposed_relative_entropy_query_keeps_n675_in_top_five(self):
        response = self.library.search("Compare quantum measurements by relative entropy for every pair of input states and any untouched auxiliary quantum system.")
        self.assertTrue(any(item["id"].startswith("N675-") for item in response["results"][:5]))
        unit = self.library.resolve("U966-conditional-sld-order-interface")
        self.assertIn("uniform conditional Umegaki order", unit["statement"])
        self.assertIn("complete equal-reference SLD metric order", unit["statement"])
        self.assertIn("Does not equate", unit["contract"]["obstruction"])

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

    def test_p3_default_packets_fit_and_preserve_review_evidence_routes(self):
        for identifier in ("N996", "U996-acquired-operator-law-defect-procedure"):
            with self.subTest(identifier=identifier):
                result = subprocess.run(
                    [sys.executable, "knowledge/retrieve.py", "packet", identifier],
                    cwd=ROOT, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                packet = json.loads(result.stdout)["packets"][0]
                self.assertTrue(packet["evidence"])
                for review in packet.get("review_overlays", []) + packet.get("historical_reviews", []):
                    self.assertEqual(review.get("evidence_ref_field"), "evidence")
                    refs = [compact_ref(ref) for ref in evidence_refs(
                        json.loads((ROOT / review["authority"]).read_text())["evidence"])]
                    resolved = [packet["evidence"][index] for index in review["evidence_ref_indices"]]
                    self.assertEqual(resolved, refs)

    def test_p3_circuit_proof_route_and_known_cost_fields_are_exposed(self):
        card = self.library.resolve("N996")
        self.assertIn("n=64", card["contract"]["costs"])
        self.assertNotEqual(card["contract"]["obstruction"], "UNKNOWN")
        for identifier in ("N996", "U996-acquired-operator-law-defect-procedure"):
            with self.subTest(identifier=identifier):
                packet = self.library.packet([identifier])["packets"][0]
                source = self.library.source(identifier, evidence_index=0)
                self.assertEqual(source["source"]["lines"], [408, 443])
                self.assertIn("Induction on a program DAG proves native correctness", source["text"])
                self.assertEqual(packet["evidence"][0]["lines"], [408, 443])

    def test_p3_advertised_catalogue_route_returns_the_accepted_packet(self):
        catalog_path = ROOT / "indexes/agent_catalog.d/2026-10-25-p3-operator-law-procedure.json"
        catalog = json.loads(catalog_path.read_text())
        entry = next(item for item in catalog["claims"]
                     if item["id"] == "N996-p3-acquired-operator-law-procedure")
        pointers = entry["pointers"]
        self.assertEqual(pointers["card_web"], pointers["card_local"])
        self.assertTrue(pointers["card_web"].endswith(".txt"))
        self.assertTrue((ROOT / pointers["card_web"]).is_file())
        self.assertNotIn("frontier/dossiers_v5/N996.txt", pointers["read_web"])
        for path in pointers["read_web"]:
            self.assertTrue((ROOT / path).is_file(), path)

        result = subprocess.run(shlex.split(pointers["read_local"]), cwd=ROOT,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLessEqual(len(result.stdout.encode('utf-8')), 32768)
        response = json.loads(result.stdout)
        self.assertEqual(len(response["packets"]), 1)
        packet = response["packets"][0]
        self.assertEqual(packet["id"], entry["id"])
        accepted = next(review for review in packet["review_overlays"]
                        if review['decision'] == 'accepted_internally_verified'
                        and any(subject['id'] == packet['id'] and subject['content_version'] == packet['content_version']
                                for subject in review['subjects']))
        self.assertEqual(accepted["decision"], "accepted_internally_verified")
        self.assertTrue(any(subject["id"] == packet["id"]
                            and subject["content_version"] == packet["content_version"]
                            for subject in accepted["subjects"]))
        if accepted['id'] != 'A997-p3-operator-law-procedure-source-review-v2':
            self.assertTrue(any(review['id'] == 'A997-p3-operator-law-procedure-source-review-v2'
                                for review in packet['historical_reviews']))


if __name__ == "__main__":
    unittest.main()
