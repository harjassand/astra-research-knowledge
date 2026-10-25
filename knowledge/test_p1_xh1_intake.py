"""Selected-source receiving contracts, not scientific-script replay."""
import hashlib
import json
from pathlib import Path
import unittest

from knowledge.model import ROOT, evidence_refs


UPDATE = Path("research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-p1-xh1-completed-intake")
SHARD = "2026-10-25-p1-xh1"
UNIT_IDS = [
    "U986-p1-gamma-root-factor-memory-bound",
    "U987-p1-exact-aggregate-count-quantum-quotient",
    "U988-xh1-product-negative-display-proposal",
    "U989-xh1-empty-carrier-false-completion",
]


class SelectedP1XH1Intake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / UPDATE / "source/INDEX.json").read_text())["files"]
        cls.indexed_paths = {(UPDATE / row["path"]).as_posix(): row for row in cls.index}
        cls.records = {record["id"]: record for record in map(json.loads, (ROOT / "knowledge/current/records.jsonl").read_text().splitlines())}
        cls.units = [cls.records[identifier] for identifier in UNIT_IDS]

    def passage(self, unit, filename, start, end):
        reference = next(reference for reference in unit["evidence"]
                         if Path(reference["path"]).name == filename
                         and reference["lines"][0] <= start and reference["lines"][1] >= end)
        lines = (ROOT / reference["path"]).read_text().splitlines()
        return "\n".join(lines[start - 1:end])

    def test_six_originals_have_unique_document_ids_and_exact_bytes(self):
        self.assertEqual(len(self.index), 6)
        self.assertEqual(len({row["source_id"] for row in self.index}), 6)
        for row in self.index:
            content = (ROOT / UPDATE / row["path"]).read_bytes()
            self.assertEqual(len(content), row["bytes"])
            self.assertEqual(hashlib.sha256(content).hexdigest(), row["sha256"])
            self.assertEqual(row["source_id"], row["family_id"] + "-" + Path(row["path"]).suffix.lstrip("."))

    def test_current_source_references_resolve_to_selected_documents(self):
        statuses = list(map(json.loads, (ROOT / "frontier/CURRENT_CLAIM_STATUS.d" / (SHARD + ".jsonl")).read_text().splitlines()))
        authored_units = [json.loads((ROOT / unit["authority"]).read_text()) for unit in self.units]
        for record in statuses + authored_units:
            for reference in evidence_refs(record):
                row = self.indexed_paths[reference["path"]]
                self.assertEqual(reference["sha256"], row["sha256"])
                self.assertEqual(reference["source_id"], row["source_id"])

    def test_each_current_unit_has_an_exact_scoped_review(self):
        for unit in self.units:
            decisions = {review["decision"] for review in unit["review_overlays"]
                         if any(subject["id"] == unit["id"] and subject["content_version"] == unit["content_version"]
                                for subject in review["subjects"])}
            self.assertEqual(decisions, {"open"} if unit["id"] == UNIT_IDS[2] else {"accepted_internally_verified"})
            for field in ("requires", "provides", "assumptions", "costs", "units", "obstruction"):
                self.assertTrue(unit["contract"][field])

    def test_root_operation_and_budget_conditions_reach_actual_passages(self):
        unit = self.units[0]
        construction = self.passage(unit, "GAMMA_ROOT_FILTER_AND_PREDICTIVE_RANK.txt", 31, 148)
        self.assertIn("P(z)=exp[lambda(z-1)] R(z)", construction)
        self.assertIn("m+k+lambda z+sum_i z/(z-r_i)", construction)
        self.assertIn("Leijdekker", construction)
        assumptions = " ".join(unit["contract"]["assumptions"])
        self.assertIn("0<tau<1", assumptions)
        self.assertIn("0<epsilon<2 c_max m nu T", assumptions)
        self.assertIn("0<epsilon<2 c_max m nu t0", assumptions)
        self.assertIn("same predictable control", assumptions)
        self.assertIn("c_t S is a count rate, not a probability", unit["contract"]["units"])
        coarsening = self.passage(unit, "GAMMA_ROOT_FILTER_AND_PREDICTIVE_RANK.txt", 400, 420)
        self.assertIn("PGF has a pole", coarsening)
        self.assertIn("unexposed finer counts", coarsening)

    def test_quantum_transfer_is_an_instrument_not_only_a_moment_match(self):
        unit = self.units[1]
        proof = self.passage(unit, "EXACT_QUANTUM_AGGREGATE_POISSON_INTERTWINING.txt", 59, 125)
        self.assertIn("J_N,t P_s(z)=theta c_t partial_z P_s(z)=c_t s P_s(z)", proof)
        self.assertIn("(L_N-J_N,t) P mu", proof)
        self.assertIn("conservative nonexplosive", " ".join(unit["contract"]["assumptions"]).lower())
        self.assertIn("cannot steer K", unit["contract"]["obstruction"])
        self.assertIn("coarse", unit["contract"]["obstruction"])

    def test_proposal_retains_decoding_credit_and_unacquired_capture(self):
        unit = self.units[2]
        decoding = self.passage(unit, "astra_product_qualified_assembly_2026-10-25.md", 45, 51)
        self.assertIn("same tRNA species", decoding)
        self.assertIn("NOT the Figure 8", decoding)
        self.assertEqual(unit["kind"], "mechanism_proposal")
        self.assertIn("codon/charged-tRNA", " ".join(unit["contract"]["requires"]))
        self.assertIn("unacquired", unit["statement"])
        self.assertIn("not product-gated progression", unit["contract"]["obstruction"])
        credit = self.passage(unit, "astra_product_qualified_assembly_2026-10-25.md", 6, 16)
        self.assertIn("Roberts", credit)
        self.assertIn("Johansen-Leete", credit)

    def test_false_completion_is_a_stated_pair_not_measured_kinetics(self):
        unit = self.units[3]
        passage = self.passage(unit, "astra_product_qualified_assembly_2026-10-25.md", 17, 24)
        self.assertIn("produce U–OH", passage)
        self.assertIn("leaves the incoming tRNA_A unchanged", passage)
        self.assertIn("does not assert", " ".join(unit["contract"]["assumptions"]))

    def test_current_public_pointers_exist_without_frozen_v5_dossiers(self):
        catalog = json.loads((ROOT / "indexes/agent_catalog.d" / (SHARD + ".json")).read_text())
        for record in catalog["claims"]:
            for path in record["pointers"]["read_web"]:
                self.assertTrue((ROOT / path).is_file(), path)
            self.assertIn("knowledge/retrieve.py packet", record["pointers"]["read_local"])

    def test_exact_subset_refinement_reaches_the_older_bridge_packet(self):
        notices = self.records["N954-p1-positive-quartic-record-bridge"]["notices"]
        notice = next(notice for notice in notices if notice.get("notice_id") == "SN-P1-EXACT-AGGREGATE-NOT-COARSE-RECORD-20261025")
        self.assertFalse(notice["whole_claim_invalidated"])
        self.assertIn("ONLY", notice["clarification"])
        self.assertIn("Port-sensitive uses remain separate", notice["clarification"])


if __name__ == "__main__":
    unittest.main()
