"""Prevent native-only wave claims inheriting the three scoped proof acceptances."""
import hashlib
import json
import unittest

from knowledge.model import ROOT, Inputs
from knowledge.retrieve import Library

BASE = "research/2026-10-28-p1-wave-native/"
PARENT = "N1126-quadratic-wave-current-and-window-cost"
ACCEPTED = {
    "U1126-affine-current-passive-lift",
    "U1126-hilbert-curve-positive-majorant",
    "U1126-singular-moment-residual-control",
}


class P1NativeScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library(validate=False)
        cls.units = [r for r in cls.library.records.values() if PARENT in r["parents"]]

    def test_native_identity_and_missing_archives_stay_explicit(self):
        data = (ROOT / BASE / "source/originals/FULL_NATIVE_COPY.md").read_bytes()
        self.assertEqual(len(data), 22193)
        self.assertEqual(hashlib.sha256(data).hexdigest(),
                         "51c5a3e0d2f893a4193466ebb5f3092f463855521109a6ee0054e8296088d3a4")
        availability = json.loads((ROOT / BASE / "source/AVAILABILITY.json").read_bytes())
        index = json.loads((ROOT / BASE / "source/INDEX.json").read_bytes())
        self.assertEqual(len(availability["unacquired_originals"]), 2)
        for missing in availability["unacquired_originals"]:
            self.assertNotIn(missing["name"], [r["path"].rsplit("/", 1)[-1] for r in index["files"]])

    def test_acceptance_is_bound_only_to_three_complete_proofs(self):
        self.assertEqual(len(self.units), 9)
        for record in [self.library.resolve(PARENT)] + self.units:
            accepted = [v for v in record["review_overlays"]
                        if v["decision"] == "accepted_internally_verified"]
            self.assertEqual(bool(accepted), record["id"] in ACCEPTED, record["id"])
            for review in accepted:
                self.assertIn({"id": record["id"], "content_version": record["content_version"]},
                              review["subjects"])
        self.assertEqual(self.library.resolve(PARENT)["review"]["reported_status"], "source_report_only")

    def test_accepted_source_routes_reach_the_right_complete_branch(self):
        anchors = {"U1126-affine-current-passive-lift": "Gamma^a_ab vanishes",
                   "U1126-hilbert-curve-positive-majorant": "interval is contained in [0,ell+1]",
                   "U1126-singular-moment-residual-control": "(ker T)^perp=range T"}
        for identifier, anchor in anchors.items():
            source = self.library.source(identifier)
            self.assertEqual(source["source"]["path"], BASE + "source/THREE_DISPLAYED_IDENTITIES.md")
            self.assertIn(anchor, source["text"])
            for reference in self.library.resolve(identifier)["evidence"]:
                Inputs(ROOT).source(reference)

    def test_reported_obstructions_keep_their_nontransfer_conditions(self):
        cases = {
            "universal-free-orbit-trace-cost": "restricted amplitude classes",
            "passive-quadratic-background-rigidity": "K invertible at one time",
            "beyond-quadratic-positive-completion": "not componentwise smallness",
            "physical-brinkmann-wall-obstruction": "rather than the auxiliary affine connection",
        }
        for suffix, phrase in cases.items():
            record = self.library.resolve("U1126-" + suffix)
            self.assertIn(phrase, json.dumps(record["contract"]))
            self.assertEqual(record["review"]["acceptance"], "source_report_only")


if __name__ == "__main__":
    unittest.main()
