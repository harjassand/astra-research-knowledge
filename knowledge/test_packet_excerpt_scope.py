"""A changed packet budget must not republish host paths from legacy evidence."""
import unittest

from knowledge.build import packet_excerpt
from knowledge.model import scientific_text


class PacketExcerptScope(unittest.TestCase):
    def test_json_projection_omits_locator_without_altering_source_or_passage(self):
        original = '{"claim":"Exact finite statement", "origin":"/' + 'Users/fixture/review.md"}'
        passage, selection = scientific_text(original)
        reference = {"path": "research/legacy-review.json", "sha256": "a" * 64, "lines": [1, 1]}
        excerpt = packet_excerpt(reference, passage, selection)
        self.assertNotIn("text", excerpt)
        self.assertIn("Original evidence remains unchanged", excerpt["text_omitted"])
        self.assertEqual(excerpt["source"], reference)
        self.assertIn("Exact finite statement", passage)
        self.assertIn("/" + "Users/fixture/review.md", original)

    def test_file_url_omitted_but_scientific_slash_notation_preserved(self):
        self.assertNotIn("text", packet_excerpt({}, "file" + "://local/review", "unchanged_utf8"))
        statement = "input/output; gates/workspace; A/B; reviews/root_receipt.json"
        self.assertEqual(packet_excerpt({}, statement, "unchanged_utf8")["text"], statement)


if __name__ == "__main__":
    unittest.main()
