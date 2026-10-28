"""Protect model identity,rate conventions and qualified scientific interfaces."""
import hashlib
import json
from pathlib import Path
import unittest

from knowledge.model import ROOT, Inputs

BASE = "research/2026-10-28-p2-nonrwa-and-radiation/"
OLD = "N1080-same-end-symmetry-filtered-hardcore-pair"
NEW = "N1127-positive-spring-nonrwa-embedded-pair"


class P2ChannelScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Retain only the selected records,not another full corpus/model copy
        # throughout the scientific test suite.
        cls.records = {}
        with (ROOT / "knowledge/current/records.jsonl").open() as stream:
            for line in stream:
                r = json.loads(line)
                if r["id"].startswith(("N1127-", "N1128-", "U1127-", "U1128-")) or r["id"] in (
                        OLD, "U1080-ordered-detuning-eighth-order-width"):
                    cls.records[r["id"]] = r
        cls.transfers = {t["id"]: t for t in json.loads(
            (ROOT / "knowledge/current/transfers.json").read_bytes()) if t["id"].startswith("B1128-")}

    def test_public_scientific_selection_preserves_bytes_and_excludes_native_dialogue(self):
        availability = json.loads((ROOT / BASE / "source/AVAILABILITY.json").read_bytes())
        originals = availability["public_files"]
        self.assertEqual(len(originals), 6)
        self.assertFalse((ROOT / BASE / "source/originals/FULL_NATIVE_COPY.md").exists())
        for row in originals:
            data = (ROOT / BASE / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])
        audit = next(r for r in originals if r["path"].endswith("audit_nonrwa_proof.md"))
        self.assertEqual(audit["sha256"], "73724ebcae2f2bca1b68566d62b2c8dd0011f95429411c34befe01e557bab7a9")

    def test_actual_review_scope_does_not_promote_reported_cooperative_decay(self):
        for identifier, record in self.records.items():
            if not identifier.startswith(("N1127-", "N1128-", "U1127-", "U1128-")):
                continue
            accepted = [v for v in record["review_overlays"] if v["decision"] == "accepted_internally_verified"]
            expected = identifier != "N1128-complete-channel-and-composition-limits" and identifier != "U1128-cooperative-density-emission"
            self.assertEqual(bool(accepted), expected, identifier)
            for review in accepted:
                self.assertIn({"id": identifier, "content_version": record["content_version"]}, review["subjects"])
        tail = self.records["U1127-graded-analytic-number-tail"]
        _, proof = Inputs(ROOT).source(tail["evidence"][0])
        self.assertIn("Cauchy's coefficient bound", proof)
        self.assertIn("norm is bounded", proof)
        self.assertIn("not been", proof)  # The local-density candidate remains unproved.

    def test_object_match_and_missing_inputs_control_interface_state(self):
        expected = {
            "B1128-source-pair-to-inclusive-lowering": "ESTABLISHED COMPATIBLE INTERFACE",
            "B1128-original-pair-to-tensor-gap": "ESTABLISHED COMPATIBLE INTERFACE",
            "B1128-nonrwa-pair-to-tensor-gap": "ESTABLISHED COMPATIBLE INTERFACE",
            "B1128-nonrwa-to-fixed-number-gap": "INCOMPATIBLE ASSUMPTIONS",
            "B1128-nonrwa-local-density-emission-candidate": "CANDIDATE CONNECTION",
        }
        self.assertEqual({k: v["state"] for k, v in self.transfers.items()}, expected)
        for t in self.transfers.values():
            self.assertEqual(t["from_version"], self.records[t["from"]]["content_version"])
            self.assertEqual(t["to_version"], self.records[t["to"]]["content_version"])
            for reference in t["evidence"]:
                Inputs(ROOT).source(reference)
            if t["state"] != "ESTABLISHED COMPATIBLE INTERFACE":
                self.assertNotIn("slot_binding", t)
        consumer = self.records["U1128-one-sided-tensor-sum-gap"]
        providers = {v["provider"] for v in consumer["interface_navigation"]["bindings"]}
        self.assertEqual(providers, {OLD, NEW})
        self.assertFalse(any(t["from"] == OLD and t["to"] == NEW for t in self.transfers.values()))

    def test_old_detuning_proof_is_reused_with_population_not_amplitude_convention(self):
        old = self.records["U1080-ordered-detuning-eighth-order-width"]
        self.assertIn("64 b^2/(27pi)", old["statement"])
        self.assertIn("Probability linewidth", old["contract"]["units"])
        self.assertTrue(any(r["decision"] == "accepted_internally_verified" for r in old["review_overlays"]))
        self.assertFalse(any("detuning" in i for i in self.records if i.startswith(("U1127-", "U1128-"))))
        notice = next(n for n in self.records[OLD]["notices"] if n.get("notice_id") == "SN-P2-CHANNELS-AND-CURRENT-DETUNING-20261028")
        self.assertFalse(notice["whole_claim_invalidated"])
        self.assertIn("not current absence", notice["clarification"])

    def test_decimal_clarification_propagates_without_invalidating_symbolic_positivity(self):
        notice_id = "SN-P2-NONRWA-SYMBOLIC-BOUND-DECIMAL-20261028"
        for identifier in (NEW, "U1127-own-rail-positive-interaction"):
            notice = next(n for n in self.records[identifier]["notices"] if n.get("notice_id") == notice_id)
            self.assertFalse(notice["whole_claim_invalidated"])
            self.assertIn("does not prove", notice["clarification"])
            _, passage = Inputs(ROOT).source(notice["source_refs"][0])
            self.assertIn("not an outward evaluation of U", passage)
            self.assertIn("0.04786451314966059", passage)
        original = (ROOT / BASE / "source/originals/NON_RWA_LOCAL_OSCILLATOR_PAIR.txt").read_text()
        self.assertIn(".0478644803898", original)


if __name__ == "__main__":
    unittest.main()
