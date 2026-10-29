"""Lossless citation sharing protects complete current packets as notices grow."""
import copy
import unittest

from knowledge.build import packet_default_read_paths, packet_review, packet_shared_citations
from knowledge.model import encoded


def reference():
    return dict(path="research/source/proof.md", read_path="research/source/proof.md",
                sha256="a" * 64, lines=[8, 23], quote="The actual construction",
                range_scope="This exact branch and its conditions.")


def expanded(value, root):
    if isinstance(value, list):
        return [expanded(child, root) for child in value]
    if not isinstance(value, dict):
        return value
    if set(value) == {"evidence_ref_pointer"}:
        target = root
        for token in value["evidence_ref_pointer"].split("/")[1:]:
            token = token.replace("~1", "/").replace("~0", "~")
            target = target[int(token)] if isinstance(target, list) else target[token]
        return expanded(target, root)
    return {key: expanded(child, root) for key, child in value.items()}


class CompleteCitationBudget(unittest.TestCase):
    def test_named_validation_evidence_retains_annotations(self):
        ref = reference()
        original = {"reported_status_evidence": [dict(ref, purpose="historical audit scope")],
                    "internal": "Source-reported assessment, not new acceptance"}
        compact = packet_review(original, [ref], preserve_annotations=True,
                                evidence_field="reported_status_evidence")
        self.assertNotIn("reported_status_evidence", compact)
        self.assertEqual(compact["evidence_ref_field"], "reported_status_evidence")
        restored = dict(ref, **compact["evidence_ref_annotations"][0])
        self.assertEqual(restored, original["reported_status_evidence"][0])
        self.assertEqual(compact["internal"], original["internal"])

    def test_unique_or_mixed_validation_evidence_is_not_lost(self):
        ref = reference()
        different = dict(ref, range_scope="A different qualification")
        for values in ([different], [{"scope": "Keep this text", "source": ref}]):
            original = {"reported_status_evidence": values}
            self.assertEqual(packet_review(original, [ref], True,
                                          evidence_field="reported_status_evidence"), original)

    def test_shared_citations_roundtrip_and_qualified_branches_stay_distinct(self):
        ref = reference()
        other = dict(ref, lines=[31, 49], quote="A different branch")
        packet = {"evidence": [ref], "notices": [{"source_refs": [ref, other]}],
                  "review_overlays": [{"evidence": [other]}], "transfers": [{"evidence": [ref, other]}],
                  "relationships": {"evidence": [other]},
                  "historical_reviews": [{"evidence": [ref]}]}
        original = copy.deepcopy(packet)
        result = packet_shared_citations(packet)
        self.assertEqual(packet, original)
        self.assertEqual(result["evidence"], original["evidence"])
        self.assertEqual(result["notices"], original["notices"])
        self.assertEqual(result["review_overlays"], original["review_overlays"])
        self.assertEqual(result["notices"][0]["source_refs"][1], other)
        self.assertEqual(result["historical_reviews"], original["historical_reviews"])
        self.assertEqual(expanded(result, result), original)
        self.assertLess(len(encoded(result)), len(encoded(original)))

    def test_escaped_pointer_origins_survive_and_never_use_history_only_fields(self):
        ref = reference()
        packet = {"evidence": [], "notices": [{"a/b~c": [ref]}],
                  "review_overlays": [], "transfers": [{"evidence": [ref]}],
                  "historical_reviews": [{"evidence": [ref]}]}
        result = packet_shared_citations(packet)
        self.assertEqual(result["transfers"][0]["evidence"][0],
                         {"evidence_ref_pointer": "/notices/0/a~1b~0c/0"})
        self.assertEqual(expanded(result, result), packet)

    def test_only_redundant_citation_read_paths_are_omitted(self):
        same = reference()
        derivative = dict(same, read_path="research/source/selected-page.html")
        original = {"evidence": [same, derivative],
                    "scientific_object": {"path": "trajectory", "read_path": "trajectory"}}
        compact = packet_default_read_paths(original)
        self.assertNotIn("read_path", compact["evidence"][0])
        self.assertEqual(compact["evidence"][1], derivative)
        self.assertEqual(compact["scientific_object"], original["scientific_object"])
        self.assertEqual(dict(compact["evidence"][0], read_path=compact["evidence"][0]["path"]), same)
        self.assertEqual(original["evidence"][0], same)


if __name__ == "__main__":
    unittest.main()
