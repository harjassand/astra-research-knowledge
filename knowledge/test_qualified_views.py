"""Qualification relevance must retain actual source branches and current scope."""
import copy
import unittest

from knowledge import test_knowledge as fixtures
from knowledge.model import digest, encoded
from knowledge.operations import operation_frame, premise_check, qualified_views
from knowledge.retrieve import Library


class QualificationSources(unittest.TestCase):
    setUp = fixtures.Fixture.setUp
    write = fixtures.Fixture.write
    statuses = fixtures.Fixture.statuses
    compile = fixtures.Fixture.compile

    def prepare(self):
        body = b"New current correction: independent noise is not acquired.\n"
        self.write("correction.txt", body)
        self.notice = {"notice_id": "actual-correction", "card_ids": ["N1-fixture"],
                       "clarification": body.decode().strip(),
                       "source_refs": [{"path": "correction.txt", "sha256": digest(body),
                                        "lines": [1, 1], "quote": "not acquired"}]}
        self.write("agent/SEMANTIC_NOTICES.jsonl", encoded(self.notice))
        self.compile()
        return Library(self.root)

    def test_notice_source_reads_its_actual_branch_and_checks_scope(self):
        library = self.prepare()
        original = library.source("N1-fixture")
        corrected = library.source("N1-fixture", notice="actual-correction")
        self.assertEqual(original["source"]["path"], "source.txt")
        self.assertEqual(corrected["source"]["path"], "correction.txt")
        self.assertIn("not acquired", corrected["text"])
        self.assertEqual(corrected["current_notice_id"], "actual-correction")
        with self.assertRaisesRegex(ValueError, "Unknown or ambiguous current notice"):
            library.source("N1-fixture", notice="another-card-notice")
        with self.assertRaisesRegex(ValueError, "Unknown evidence index"):
            library.source("N1-fixture", notice="actual-correction", evidence_index=1)
        with self.assertRaisesRegex(ValueError, "within the cited"):
            library.source("N1-fixture", notice="actual-correction", end=2)
        with self.assertRaisesRegex(ValueError, "byte budget"):
            library.source("N1-fixture", notice="actual-correction", max_bytes=len(encoded(corrected)) - 1)

    def test_revision_rebuilds_notice_view_without_stale_source_or_acceptance(self):
        library = self.prepare()
        old = library.resolve("N1-fixture")
        changed = b"New current correction: calibration is also not acquired.\n"
        self.write("correction.txt", changed)
        self.notice["clarification"] = changed.decode().strip()
        self.notice["source_refs"][0]["sha256"] = digest(changed)
        self.write("agent/SEMANTIC_NOTICES.jsonl", encoded(self.notice))
        with self.assertRaisesRegex(ValueError, "Stale"):
            Library(self.root)
        first, _ = self.compile()
        second, _ = self.compile()
        self.assertEqual(first, second)
        current = Library(self.root)
        record = current.resolve("N1-fixture")
        self.assertEqual(old["content_version"], record["content_version"])
        self.assertFalse(record["review_overlays"])
        self.assertIn("calibration", current.source("N1-fixture", notice="actual-correction")["text"])

    def test_selected_notice_navigation_never_uses_record_evidence_zero(self):
        library = self.prepare()

        class FixtureRanking:
            version = "fixture-relevance-only"

            def score(self, pairs):
                return [float("New current correction" in text) for _, text in pairs], [False] * len(pairs)

        library.reranker = FixtureRanking()
        response = library.search("finite mechanism independent noise", method="agent")
        hit = response["results"][0]
        self.assertEqual(hit["ranking_view"], "current_notice")
        self.assertEqual(hit["notice_match"]["notice_id"], "actual-correction")
        self.assertEqual(hit["next"]["notice_source"],
                         ["source", "N1-fixture", "--notice", "actual-correction", "--evidence", "0"])
        self.assertEqual(hit["premise_check"]["compatibility"], "NOT ESTABLISHED")

    def test_qualified_excerpt_never_changes_complete_conditions_or_units(self):
        library = self.prepare()
        record = copy.deepcopy(library.resolve("N1-fixture"))
        record["contract"]["assumptions"] = ["Calibration is not acquired. " * 30]
        record["contract"]["units"] = "squared angular frequency, not cycles per second"
        before = encoded(record)
        frame = operation_frame(record)
        views = list(qualified_views(record, frame, "calibration frequency"))
        self.assertEqual(encoded(record), before)
        self.assertIn("qualified_operation", [role for role, _, _ in views])
        self.assertIn("squared angular frequency", next(text for role, text, _ in views if role == "qualified_operation"))
        check = premise_check(frame, available=["calibration"], unavailable=["frequency"])
        self.assertEqual(check["compatibility"], "NOT ESTABLISHED")
        self.assertEqual(check["checks"][0]["state"], "NOT DISCHARGED")


if __name__ == "__main__":
    unittest.main()
