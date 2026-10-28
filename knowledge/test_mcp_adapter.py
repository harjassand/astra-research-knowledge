"""Transport-free regressions for version/source/correction failure modes."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from knowledge.mcp_adapter import ResearchAdapter
from knowledge.model import ROOT, digest, encoded, Inputs


def complete(adapter, identifier):
    fragments, expected = [], None
    while identifier:
        read = adapter.fetch(identifier)
        expected = expected or read["metadata"]["payload_sha256"]
        assert read["metadata"]["payload_sha256"] == expected
        assert len(read["text"].encode()) <= adapter.page_bytes
        fragments.append(read["text"])
        identifier = read["metadata"]["next_id"]
    raw = "".join(fragments).encode()
    assert digest(raw) == expected
    return json.loads(raw)


class AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = ResearchAdapter(ROOT)

    def test_record_capsule_retains_all_current_corrections_and_review_scope(self):
        for identifier in ("N557", "N684", "N1121"):
            record = self.adapter.library.resolve(identifier)
            packet = complete(self.adapter, identifier)
            self.assertEqual(packet["notices"], record["notices"])
            self.assertEqual(packet["review_overlays"], record["review_overlays"])
            self.assertEqual(packet["contract"], record["contract"])
            self.assertEqual(packet["content_version"], record["content_version"])
            if record["review_overlays"]:
                self.assertTrue(any("current_review" in r["roles"] for r in packet["review_and_correction_sources"]))

    def test_pagination_is_bounded_lossless_and_never_silently_complete(self):
        with patch.object(self.adapter, "page_bytes", 1024):
            first = self.adapter.fetch("N557")
            self.assertTrue(first["metadata"]["partial"])
            self.assertIsNotNone(first["metadata"]["next_id"])
            self.assertIn("continuation", first["metadata"]["required_action"])
            packet = complete(self.adapter, "N557")
            self.assertEqual(packet["notices"], self.adapter.library.resolve("N557")["notices"])
            with self.assertRaises(ValueError):
                self.adapter.fetch(first["id"] + ":99999999")

    def test_source_route_reads_the_actual_compiler_passage_and_its_context(self):
        record = self.adapter.library.resolve("U675-ordered-word-compiler")
        reference = record["evidence"][0]
        value = complete(self.adapter, self.adapter.register(reference))
        _, actual = Inputs(ROOT).source(reference)
        self.assertEqual(value["text"], actual)
        self.assertIn("Suffix closure", actual)
        self.assertEqual(value["source"]["sha256"], reference["sha256"])
        self.assertIn(record["id"], [c["id"] for c in value["current_context"]])

    def test_search_menus_are_small_and_deduplicate_source_path_aliases(self):
        found = self.adapter.search("negative spectral trace mass bounded Hessian paid closure")
        self.assertLess(len(encoded(found)), 16384)
        sources = [r["metadata"]["source"] for r in found["results"] if "source" in r["metadata"]]
        self.assertEqual(len(sources), len({(s["path"], s["sha256"]) for s in sources}))
        self.assertTrue(all(self.adapter.revision in r["url"] for r in found["results"]))

    def test_citation_follows_matching_old_pre_block_when_original_path_has_newer_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = "An older scoped construction.\r\nA second line.\r\n"
            (root / "proof.tex").write_text("A newer incompatible construction.\n")
            (root / "old.html").write_bytes(("<pre>A wrong first block</pre><pre>" + old + "</pre>").encode())
            adapter = ResearchAdapter.__new__(ResearchAdapter)
            adapter.root, adapter.paths, adapter.revision = root, {"proof.tex", "old.html"}, "f" * 40
            adapter.locators, adapter.artifact_data = {}, {}
            ref = {"path": "proof.tex", "read_path": "old.html", "sha256": digest(old.encode()), "lines": [1, 2]}
            locator = adapter.source_locator(ref)
            self.assertEqual(locator["artifact_path"], "old.html")
            self.assertNotIn("#L", locator["url"])
            self.assertEqual(locator["artifact_sha256"], digest((root / "old.html").read_bytes()))
            self.assertEqual(locator["source_text_sha256"], digest(old.encode()))
            with self.assertRaisesRegex(ValueError, "No hash-matched"):
                adapter.source_url(dict(ref, sha256="0" * 64))

    def test_historical_unit_version_is_retrievable_with_current_correction_context(self):
        record = next(r for r in self.adapter.library.records.values() if len(r.get("history", [])) > 1 and r["notices"])
        previous = record["history"][0]
        value = complete(self.adapter, self.adapter.register(dict(previous, lines=None)))
        self.assertEqual(value["text"].encode(), (ROOT / previous["path"]).read_bytes())
        self.assertEqual(digest(value["text"].encode()), previous["sha256"])
        context = next(c for c in value["current_context"] if c["id"] == record["id"])
        self.assertEqual(context["notices"], record["notices"])
        self.assertIn("does not inherit", value["scope"])

    def test_invalid_and_stale_handles_fail_instead_of_following_paths(self):
        for identifier in ("../../private", "https://example.org/proof", "astra:old:record:N557", self.adapter.handle("source", "0" * 64)):
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                self.adapter.fetch(identifier)
        with patch.object(self.adapter, "git", return_value="another-head"):
            with self.assertRaisesRegex(ValueError, "snapshot changed"):
                self.adapter.search("a query")
        changed = next(iter(self.adapter.frozen_paths))
        with patch.object(self.adapter, "git", side_effect=lambda *args: self.adapter.revision if args[0] == "rev-parse" else changed + "\0"):
            with self.assertRaisesRegex(ValueError, "uncommitted source/view"):
                self.adapter.fetch("N557")

    def test_every_current_record_has_a_constructible_capsule_and_public_source_routes(self):
        for record in self.adapter.library.records.values():
            with self.subTest(identifier=record["id"]):
                packet = self.adapter.record_payload(record)
                self.assertEqual(packet["content_version"], record["content_version"])
                self.assertTrue(packet["full_packet_url"].startswith("https://github.com/"))
                if record["id"].startswith("T-"):
                    original = self.adapter.library.packet([record["id"]], max_bytes=16 * 1024 * 1024)["packets"][0]
                    if "dependencies" not in original:
                        self.assertIsInstance(packet["dependencies"], str)
                        self.assertTrue(packet["dependencies"].startswith("UNKNOWN"))

    def test_portable_server_needs_no_neural_dependencies_and_explicit_fallback(self):
        def absent(*args, **kwargs):
            if kwargs.get("method") == "agent":
                raise ValueError("Agent runtime missing. Portable search remains available.")
            return original(*args, **kwargs)
        original = self.adapter.library.search
        with patch.object(self.adapter, "method", "agent"), patch.object(self.adapter.library, "search", side_effect=absent):
            result = self.adapter.search("ordered noncommutative word representation")
            self.assertIn("Agent runtime missing", result["metadata"]["fallback"])
            self.assertTrue(result["results"])

    def test_notice_identity_survives_later_portable_lane_hits(self):
        identifier = "N33-endotactic-permanence"
        match = {"notice_id": "SN-N33-REVIEW-SUBJECT-LINEAGE-20261027", "source_count": 2}

        def lane(*args, **kwargs):
            hit = {"id": identifier}
            if kwargs.get("method") == "agent":
                hit["notice_match"] = match
            return {"results": [hit]}

        with patch.object(self.adapter, "method", "agent"), patch.object(self.adapter.library, "search", side_effect=lane):
            found = self.adapter.search("version lineage of completed permanence review")
        record = next(hit for hit in found["results"] if hit["metadata"].get("record_id") == identifier)
        self.assertEqual(record["metadata"]["matching_current_notice"], match)

    def test_existing_identifiers_route_before_ranked_candidates_without_aliases(self):
        for query, expected in (("N33", "N33-endotactic-permanence"),
                ("N33-endotactic-permanence", "N33-endotactic-permanence"),
                ("n33 current audit review source version correction", "N33-endotactic-permanence"),
                ("N684 governing assumptions", self.adapter.library.resolve("N684")["id"])):
            with self.subTest(query=query):
                result = self.adapter.search(query)
                self.assertEqual(result["results"][0]["metadata"]["record_id"], expected)
                self.assertIn(expected, result["metadata"]["exact_identifier_matches"])
                capsule = complete(self.adapter, result["results"][0]["id"])
                self.assertEqual(capsule["content_version"], self.adapter.library.records[expected]["content_version"])

    def test_multiple_ids_and_ambiguous_unit_prefix_do_not_blend_records(self):
        result = self.adapter.search("N33 versus N557")
        identifiers = [r["metadata"].get("record_id") for r in result["results"][:2]]
        self.assertEqual(identifiers, [self.adapter.library.resolve(i)["id"] for i in ("N33", "N557")])
        self.assertEqual(self.adapter.search("U1130")["metadata"]["exact_identifier_matches"], [])

    def test_current_scope_is_lossless_for_conditions_notices_reviews_and_gaps(self):
        record = self.adapter.library.resolve("N557")
        original = self.adapter.record_payload(record)
        current = complete(self.adapter, self.adapter.handle("current", record["id"]))
        refs = {r["fetch_id"]: r["source"] for r in current["evidence"]}
        refs.update({r["fetch_id"]: r["source"] for r in current["review_and_correction_sources"] if "source" in r})
        def expand(value):
            if isinstance(value, list):
                return [expand(v) for v in value]
            if isinstance(value, dict):
                if "source_fetch_id" in value:
                    return dict(refs[value["source_fetch_id"]], **value.get("source_ref_annotations", {}))
                return {k: expand(v) for k, v in value.items()}
            return value
        for field in ("notices", "review_overlays", "transfers"):
            self.assertEqual(expand(current[field]), original[field])
        self.assertEqual(expand(current["source_reported_gaps"]), original["reported_review"]["gaps"])
        self.assertEqual(current["contract"], original["contract"])
        self.assertLess(len(encoded(current)), len(encoded(original)))
        history = complete(self.adapter, current["history"]["fetch_id"])
        for field in ("reported_review", "historical_reviews", "historical_versions"):
            self.assertEqual(history[field], original[field])
        self.assertEqual(history["current_scope_fetch_id"], self.adapter.handle("current", record["id"]))


if __name__ == "__main__":
    unittest.main()
