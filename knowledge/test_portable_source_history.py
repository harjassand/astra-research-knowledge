"""Explicit historical copies must not weaken current support or merge identities."""
import copy
import json
import unittest

from knowledge import test_knowledge as fixtures
from knowledge.build import build
from knowledge.model import digest, encoded
from knowledge.retrieve import Library


class PortableSourceHistory(unittest.TestCase):
    setUp = fixtures.Fixture.setUp
    write = fixtures.Fixture.write
    statuses = fixtures.Fixture.statuses
    unit = fixtures.Fixture.unit
    compile = fixtures.Fixture.compile

    def prepare(self):
        original = (self.root / "source.txt").read_bytes() + b"Original location metadata.\n"
        self.write("source.txt", original)
        self.source["sha256"] = digest(original)
        self.statuses()
        first = self.unit()
        self.compile()
        old_version = Library(self.root).resolve(first["id"])["content_version"]
        review = {"id": "old-exact-review", "subjects": [{"id": first["id"], "content_version": old_version}],
                  "decision": "accepted_internally_verified", "scope": "Original conditional science only",
                  "evidence": [copy.deepcopy(self.source)]}
        self.write("knowledge/reviews/old.json", encoded(review))
        current = original.replace(b"Original location metadata.", b"Public portable location metadata.")
        self.public_path = "research/portable/source/public/source.txt"
        self.write(self.public_path, current)
        self.current_source = dict(self.source, path=self.public_path, sha256=digest(current))
        second = copy.deepcopy(first)
        second.update(version=2, previous=digest(encoded(first)), evidence=[self.current_source])
        self.write("knowledge/units/U1-fixture/v0002.json", encoded(second))
        self.status["proof_availability"]["located_proof_sources"] = [self.current_source]
        self.statuses()
        self.entry = {"path": "source/public/source.txt", "bytes": len(current), "sha256": digest(current),
                      "kind": "public_path_portability_derivative", "original_path": "source.txt",
                      "original_sha256": digest(original)}
        self.index()
        (self.root / "source.txt").unlink()
        self.old_unit = encoded(first)
        self.old_review = encoded(review)

    def index(self):
        self.write("research/portable/source/INDEX.json", encoded({
            "schema": "astra.intake-source-index.v1", "files": [self.entry]}))

    def test_history_retains_identity_and_actual_quote_without_retargeting_review(self):
        self.prepare()
        self.compile()
        record = Library(self.root).resolve("U1-fixture")
        self.assertEqual((self.root / "knowledge/units/U1-fixture/v0001.json").read_bytes(), self.old_unit)
        self.assertEqual((self.root / "knowledge/reviews/old.json").read_bytes(), self.old_review)
        self.assertFalse(record["review_overlays"])
        historical = record["historical_reviews"][0]
        self.assertEqual(historical["subjects"], json.loads(self.old_review)["subjects"])
        self.assertEqual(historical["evidence"][0]["path"], self.public_path)
        note = record["history"][0]["source_derivatives"][0]
        self.assertEqual(note["original_sha256"], self.source["sha256"])
        self.assertNotEqual(note["original_sha256"], note["public_derivative"]["sha256"])
        self.assertIn("privately preserved", note["scope"])

    def test_undeclared_missing_historical_source_still_fails(self):
        self.prepare()
        self.entry["kind"] = "frozen_original"
        self.index()
        with self.assertRaisesRegex(ValueError, "required source bytes"):
            build(self.root)

    def test_current_reference_cannot_use_historical_fallback(self):
        self.prepare()
        path = "knowledge/units/U1-fixture/v0002.json"
        unit = json.loads((self.root / path).read_bytes())
        unit["evidence"] = [self.source]
        self.write(path, encoded(unit))
        with self.assertRaisesRegex(ValueError, "required source bytes"):
            build(self.root)

    def test_wrong_derivative_hash_and_changed_scientific_quote_fail(self):
        self.prepare()
        self.entry["sha256"] = "0" * 64
        self.index()
        with self.assertRaisesRegex(ValueError, "derivative bytes"):
            build(self.root)
        data = (self.root / self.public_path).read_bytes().replace(b"independent noise", b"correlated noise")
        self.write(self.public_path, data)
        self.entry.update(sha256=digest(data), bytes=len(data))
        self.index()
        # Keep the new current source internally consistent so this assertion
        # reaches the old historical quotation, rather than failing earlier
        # on a stale current hash. The immutable v1/review are not changed.
        self.current_source.update(sha256=digest(data), quote="Assume correlated noise.")
        self.statuses()
        path = "knowledge/units/U1-fixture/v0002.json"
        current = json.loads((self.root / path).read_bytes())
        current["evidence"] = [self.current_source]
        self.write(path, encoded(current))
        with self.assertRaisesRegex(ValueError, "Wrong supporting passage"):
            build(self.root)

    def test_original_identity_is_not_a_private_location_to_follow(self):
        self.prepare()
        self.entry["original_path"] = "/not-repository/source.txt"
        self.index()
        with self.assertRaisesRegex(ValueError, "repository-relative"):
            build(self.root)


if __name__ == "__main__":
    unittest.main()
