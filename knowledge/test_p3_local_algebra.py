"""Archive preservation and real proof/interface failure boundaries, without source execution."""
import hashlib
import json
import unittest
import zipfile

from knowledge.model import Inputs, ROOT
from knowledge.retrieve import Library


BASE = ROOT / "research/2026-10-28-p3-local-algebra"
SOURCE = BASE / "source/originals/Astra_P3_Local_Algebra"


class LocalAlgebraAcquisition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library(validate=False)
        cls.selection = json.loads((BASE / "INTAKE_SELECTION.json").read_bytes())

    def test_archive_members_and_receipt_match_the_registered_bytes(self):
        index = json.loads((BASE / "source/INDEX.json").read_bytes())
        self.assertEqual(len(index["files"]), 254)
        for row in index["files"]:
            data = (BASE / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])
        archive = BASE / "source/Astra_P3_Local_Algebra_Proofs_and_Code.zip"
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), self.selection["archive_sha256"])
        with zipfile.ZipFile(archive) as original:
            members = [m for m in original.infolist() if not m.is_dir()]
            self.assertEqual(len(members), 251)
            for member in members:
                target = BASE / "source/originals" / member.filename
                self.assertEqual(original.read(member), target.read_bytes(), member.filename)

    def test_acceptance_is_bound_to_the_actual_acquired_units_and_passages(self):
        subjects = [self.selection["card"]] + self.selection["units"]
        self.assertEqual(len(self.selection["units"]), 9)
        inputs = Inputs(ROOT)
        for identifier in subjects:
            record = self.library.resolve(identifier)
            self.assertTrue(record["review_overlays"], identifier)
            for review in record["review_overlays"]:
                self.assertEqual(review["decision"], "accepted_internally_verified")
                subject = next(s for s in review["subjects"] if s["id"] == identifier)
                self.assertEqual(subject["content_version"], record["content_version"])
                for reference in review["evidence"]:
                    _, passage = inputs.source(reference)
                    self.assertIn(reference["quote"], passage)
            for reference in record["evidence"]:
                _, passage = inputs.source(reference)
                self.assertIn(reference["quote"], passage)

    def test_acquired_proofs_fit_a_default_packet_without_losing_review_or_corrections(self):
        packet = self.library.packet(["N1122"])["packets"][0]
        record = self.library.resolve("N1122")
        self.assertEqual(packet["notices"], record["notices"])
        self.assertEqual(packet["evidence"], record["evidence"])
        self.assertEqual(packet["contract"], record["contract"])
        self.assertEqual(len(packet["review_overlays"]), len(record["review_overlays"]))
        self.assertTrue(any("text_omitted" in excerpt for excerpt in packet["source_excerpts"]))
        for excerpt in packet["source_excerpts"]:
            _, passage = Inputs(ROOT).source(excerpt["source"])
            self.assertIn(excerpt["source"]["quote"], passage)

    def test_current_gap_resolution_reaches_old_review_routes_without_rewriting_them(self):
        for number in range(1118, 1125):
            record = self.library.resolve("N" + str(number))
            notices = [n for n in record["notices"]
                       if n.get("notice_id") == "SN-N1122-LOCAL-ALGEBRA-PROOF-ACQUIRED-20261028"]
            self.assertEqual(len(notices), 1)
            self.assertFalse(notices[0]["whole_claim_invalidated"])
        old = json.loads((BASE / "history/N1122-summary-only-status.json").read_bytes())
        card = (BASE / "history/N1122-summary-only-card.txt").read_bytes()
        self.assertEqual(hashlib.sha256(card).hexdigest(), old["card_sha256"])
        self.assertEqual(old["proof_availability"]["located_proof_sources"], [])
        # The earlier review is historical evidence; its availability sentence
        # stays visible alongside the new dated notice.
        old_review = json.loads((ROOT / "knowledge/reviews/A1121-p3-constructive-counting.json").read_bytes())
        self.assertTrue(any("not acquired" in gap for gap in old_review["remaining_gaps"]))

    def test_callback_route_is_the_eight_moment_branch_with_actual_cardinality_conversion(self):
        unit = self.library.resolve("U1122-eight-moment-point-count-terminal")
        callback = next(ref for ref in unit["evidence"] if ref["path"].endswith("/acquired_pair_counter.py"))
        _, passage = Inputs(ROOT).source(callback)
        self.assertIn("return number-(1<<R.d)**reduction['subtract_field_power']", passage)
        self.assertIn("field_bit_budget=24", passage)
        self.assertIn("ordinary={tuple(row['exponents'])", passage)
        terminal = next(ref for ref in unit["evidence"] if ref["path"].endswith("/acquired_pair_terminal.py"))
        _, production = Inputs(ROOT).source(terminal)
        self.assertIn("moment_terminal=moment_terminal_eight", production)
        self.assertIn("moment_terminal_reference49", production)
        self.assertIn("not", str(unit["contract"]["obstruction"]))

    def test_field_identity_does_not_erase_acquisition_degree_or_geometric_gates(self):
        palette = self.library.resolve("U1122-eight-state-gaussian-palette")
        self.assertIn("every residue degree", palette["statement"])
        card = self.library.resolve("N1122")
        self.assertIn("3 not dividing d", str(card["contract"]))
        witness = self.library.resolve("U1122-centroid-critical-locus-obstruction")
        _, passage = Inputs(ROOT).source(witness["evidence"][0])
        self.assertIn("(q+1)^2+1", passage)
        self.assertIn("**81**", passage)
        self.assertIn("not claimed #P-hard", str(witness["contract"]))

    def test_incompatible_ring_to_field_transfer_retains_the_nilpotent_phase(self):
        transfer = json.loads((ROOT / "knowledge/transfers/B1122-nonreduced-ring-not-field-decoder.json").read_bytes())
        self.assertEqual(transfer["state"], "INCOMPATIBLE ASSUMPTIONS")
        self.assertIn("nilradical", transfer["scope"])
        self.assertIn("e=1", transfer["remaining_obligations"])
        for endpoint in ("from", "to"):
            self.assertEqual(transfer[endpoint + "_version"],
                             self.library.resolve(transfer[endpoint])["content_version"])
        hard = self.library.resolve("U1122-same-J-residue-hardness")
        _, passage = Inputs(ROOT).source(hard["evidence"][1])
        self.assertIn("s_0", passage)
        self.assertIn("2^(N-1)", passage)


if __name__ == "__main__":
    unittest.main()
