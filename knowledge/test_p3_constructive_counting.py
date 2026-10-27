"""Protect the actual P3 preservation, source-routing and acceptance boundaries."""
import hashlib
import json
import unittest
import zipfile

from knowledge.model import Inputs, ROOT, encoded
from knowledge.retrieve import Library, bounded_reference


BASE = ROOT / "research/2026-10-27-p3-constructive-counting"


class P3ConstructiveCountingIntake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selection = json.loads((BASE / "INTAKE_SELECTION.json").read_bytes())
        cls.library = Library(validate=False)
        cls.library.manifest = json.loads((ROOT / "knowledge/current/manifest.json").read_bytes())

    def test_archives_members_and_native_bytes_remain_explicitly_registered(self):
        source = BASE / "source"
        index = json.loads((source / "INDEX.json").read_bytes())
        entries = {row["path"]: row for row in index["originals"]}
        for name, row in entries.items():
            data = (source / name).read_bytes()
            self.assertEqual(len(data), row["bytes"], name)
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], name)
        packages = [
            ("phase", "Astra_P3_Proofs_and_Programs.zip", "Astra_P3/"),
            ("quadratic", "Astra_P3_Acquired_Representations_Source.zip", "Astra_P3_Acquired_Representations/"),
            ("response", "Astra_P3_Hidden_Response_Sources.zip", "Astra_P3_Hidden_Response_Types/"),
            ("field", "Astra_P3_Field_Counting_Proofs_and_Code.zip", ""),
        ]
        for stage, archive, prefix in packages:
            with zipfile.ZipFile(source / "archives" / archive) as original:
                for member in original.infolist():
                    if member.is_dir():
                        continue
                    name = stage + "/" + member.filename[len(prefix):]
                    self.assertIn(name, entries)
                    self.assertEqual(original.read(member), (source / name).read_bytes(), name)
        self.assertIn("FULL_NATIVE_COPY.md", entries)

    def test_summary_only_local_algebra_does_not_inherit_other_audits(self):
        record = self.library.resolve("N1122")
        authority = json.loads((ROOT / record["authority"]).read_bytes())
        self.assertEqual(authority["proof_availability"]["located_proof_sources"], [])
        self.assertFalse(record["review_overlays"])
        self.assertEqual(record["review"]["reported_status"], "source_reported_unreviewed")
        self.assertTrue(all(ref["path"].endswith("FULL_NATIVE_COPY.md") for ref in record["evidence"]))
        field = self.library.resolve("N1121")
        self.assertTrue(field["review_overlays"])
        self.assertFalse(field["dependencies"], "The field theorem must not inherit the phase theorem's ETH import")
        for number in (1119, 1120, 1123, 1124):
            record = self.library.resolve("N" + str(number))
            self.assertEqual(len(record["dependencies"]), 1)
            self.assertTrue(record["dependencies"][0].startswith("N1118-"))
            self.assertIn("Only the explicitly conditional", str(record["relationships"]["declared_dependencies"]))

    def test_units_read_actual_parent_sources_and_default_packets_keep_conditions(self):
        inputs = Inputs(ROOT)
        for identifier in self.selection["cards"] + self.selection["units"]:
            record = self.library.resolve(identifier)
            packet = self.library.packet([identifier])
            self.assertLessEqual(len(encoded(packet)), 32768, identifier)
            self.assertIn("contract", packet["packets"][0])
            self.assertTrue(record["evidence"], identifier)
            for reference in record["evidence"]:
                _, passage = inputs.source(reference)
                self.assertIn(reference["quote"], passage)
            if identifier.startswith("U"):
                support = {(r["path"], r["sha256"]) for p in record["parents"]
                           for r in self.library.resolve(p)["evidence"]}
                self.assertTrue(all((r["path"], r["sha256"]) in support for r in record["evidence"]), identifier)
                self.assertTrue(record["review_overlays"], identifier)
        decoder = self.library.resolve("U1121-frobenius-rank-decoder")
        self.assertIn("2r<=d-2s-1", decoder["statement"])
        self.assertIn("linear correction", str(decoder["contract"]))
        synthesis = self.library.resolve("U1120-summary-fiber-optimal-synthesis")
        self.assertIn("Disjoint", str(synthesis["contract"]))
        self.assertIn("4^R", str(synthesis["contract"]))

    def test_unknown_congruences_are_not_published_as_annihilator_compatibility(self):
        path = ROOT / "knowledge/transfers/B1124-orbit-gauges-not-annihilator-invariance.json"
        transfer = json.loads(path.read_bytes())
        self.assertEqual(transfer["state"], "INCOMPATIBLE ASSUMPTIONS")
        self.assertIn("need not preserve", transfer["scope"])
        for endpoint in ("from", "to"):
            self.assertEqual(transfer[endpoint + "_version"],
                             self.library.resolve(transfer[endpoint])["content_version"])
        for reference in transfer["evidence"]:
            _, passage = Inputs(ROOT).source(reference)
            self.assertIn("does not survive arbitrary congruence", passage)

    def test_narrow_source_read_does_not_inherit_an_outside_header_quote(self):
        record = self.library.resolve("N1121")
        index = next(i for i, r in enumerate(record["evidence"])
                     if r["path"].endswith("field/proof/Astra_P3_Acquired_Field_Counters.tex"))
        reference = record["evidence"][index]
        lines = (ROOT / reference["path"]).read_text().splitlines()
        start = next(i + 1 for i, text in enumerate(lines)
                     if "\\subsection{Counting is the demonstrated" in text)
        narrowed = self.library.source("N1121", evidence_index=index, start=start, end=start + 3)
        self.assertIn("prefix constraints", narrowed["text"])
        self.assertNotIn("quote", narrowed["source"])
        self.assertIn("quote", reference, "The original packet citation must remain intact")
        self.assertNotIn("quote", bounded_reference(reference, start, start + 3, narrowed["text"]))
        full = self.library.source("N1121", evidence_index=index, max_bytes=100000)
        self.assertEqual(full["source"]["quote"], reference["quote"])


if __name__ == "__main__":
    unittest.main()
