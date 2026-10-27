"""Protect actual proof routes, quantifiers and non-transfer in the curated slice."""
import json
import unittest

from knowledge.model import Inputs, ROOT, encoded
from knowledge.retrieve import Library


CONSUMER = "U1125-qualified-task-bound-consumer"


class TaskBoundInterfaces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library(validate=False)
        cls.library.manifest = json.loads((ROOT / "knowledge/current/manifest.json").read_bytes())

    def test_new_acceptance_is_exact_and_does_not_promote_the_whole_control_parent(self):
        for identifier in ("N1125", CONSUMER, "U768-fibre-gradient-regret", "U975-three-imaginary-time-heat-bound"):
            record = self.library.resolve(identifier)
            review = next(r for r in record["review_overlays"] if r["id"] == "A1125-qualified-task-bound-interfaces")
            subject = next(s for s in review["subjects"] if s["id"] == record["id"])
            self.assertEqual(subject["content_version"], record["content_version"])
            self.assertEqual(review["decision"], "accepted_internally_verified")
            self.assertNotIn(self.library.resolve("N768")["id"], [s["id"] for s in review["subjects"]])

    def test_control_premise_reads_the_actual_quadratic_argument_with_its_extra_region_gate(self):
        record = self.library.resolve("U768-fibre-gradient-regret")
        _, passage = Inputs(ROOT).source(record["evidence"][0])
        self.assertIn("maximizing that quadratic proves", passage)
        self.assertIn("global exclusion are essential", passage)
        self.assertIn("convex", str(record["contract"]))

    def test_heat_premise_reads_finite_certificate_and_full_error_payment(self):
        record = self.library.resolve("U975-three-imaginary-time-heat-bound")
        _, passage = Inputs(ROOT).source(record["evidence"][0])
        self.assertIn("H_hat-e_(1/4)-(2/3)e_(1/2)-(1/3)e_(1/8)", passage)
        self.assertIn("not being", passage)
        self.assertIn("laboratory-time measurements", passage)
        self.assertNotIn("## Qualitative effective-theory transfer theorem", passage)

    def test_exposed_signed_task_is_reachable_from_both_real_search_families(self):
        target = "U1069-signed-task-dual-and-no-value-observation"
        for parent in ("N768", "U1000-remaining-syndrome-value-stop", "N1125"):
            candidates = self.library.peers(parent)["candidates"]
            self.assertIn(target, [c["provider"] for c in candidates])
        self.assertEqual(self.library.bridge("N768", target)["state"], "NO SUPPORTED CONNECTION")
        source = self.library.source(target, start=97, end=126)
        self.assertIn("both signed-task extremizers", source["text"])

    def test_static_displacement_does_not_acquire_the_heat_interface(self):
        source = "U1012-finite-aperture-static-dipole"
        target = "U975-three-imaginary-time-heat-bound"
        peer = next(c for c in self.library.peers(source)["candidates"] if c["provider"] == target)
        self.assertIn("imaginary-time", peer["binding"]["qualification"])
        self.assertEqual(self.library.bridge(source, target)["state"], "NO SUPPORTED CONNECTION")

    def test_branch_local_benefit_and_global_capped_regret_are_not_conflated(self):
        consumer = self.library.resolve(CONSUMER)
        item = next(b for b in consumer["interface_navigation"]["bindings"]
                    if b["provider"] == "U1000-remaining-syndrome-value-stop")
        self.assertIn("actual branch v", item["binding"]["target"])
        self.assertIn("forced-cap leaf", item["binding"]["qualification"])
        record = self.library.resolve(item["provider"])
        _, passage = Inputs(ROOT).source(record["evidence"][0])
        self.assertIn("It may stop with a substantial total logical error", passage)
        self.assertIn("excess conditional risk relative to learning", passage)

    def test_complete_consumer_packet_references_identical_retained_mappings_within_budget(self):
        value = self.library.packet([CONSUMER])
        value["checkout_revision"] = "0" * 40
        self.assertLessEqual(len(encoded(value)), 32768)
        packet = value["packets"][0]
        transfers = {t["id"]: t for t in packet["transfers"]}
        canonical = self.library.resolve(CONSUMER)
        self.assertEqual(len(packet["interface_navigation"]["bindings"]), 6)
        for item, complete in zip(packet["interface_navigation"]["bindings"], canonical["interface_navigation"]["bindings"]):
            ref = item["binding_ref"]
            self.assertEqual(transfers[ref["id"]][ref["mapping_field"]], complete["binding"])
        self.assertEqual(packet["contract"], canonical["contract"])
        self.assertEqual(packet["notices"], canonical["notices"])


if __name__ == "__main__":
    unittest.main()
