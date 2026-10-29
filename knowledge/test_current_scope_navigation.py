"""Explicit correction routes, not semantic inference or acceptance propagation."""
import copy
import json
import unittest
from pathlib import Path

from knowledge.operations import current_scope_navigation
from knowledge.retrieve import Library

ROOT = Path(__file__).resolve().parents[1]


class CurrentScopeNavigation(unittest.TestCase):
    def fixture(self):
        target = {"id": "U1-target", "content_version": "a" * 64, "title": "A conditional construction"}
        notice = {"notice_id": "SN-real-correction", "current_scope_unit": target["id"],
                  "source_refs": [{"path": "actual-proof.md", "sha256": "b" * 64, "lines": [3, 9]}]}
        record = {"id": "N1-old", "notices": [{"notice": notice, "inherited_from": "N0"}]}
        return record, {record["id"]: record, target["id"]: target}

    def test_explicit_route_uses_actual_target_version_without_mutation(self):
        record, rows = self.fixture(); before = copy.deepcopy(rows)
        route = current_scope_navigation(record, rows)["routes"][0]
        self.assertEqual(route["content_version"], "a" * 64)
        self.assertEqual(route["authority_notice"], "SN-real-correction")
        self.assertNotIn("acceptance", route)
        self.assertNotIn("contract", route)
        self.assertEqual(rows, before)
        rows["U1-target"]["content_version"] = "c" * 64
        self.assertEqual(current_scope_navigation(record, rows)["routes"][0]["content_version"], "c" * 64)

    def test_missing_target_or_required_authority_is_explicit_failure(self):
        record, rows = self.fixture()
        del rows["U1-target"]
        with self.assertRaisesRegex(ValueError, "Unknown explicit"):
            current_scope_navigation(record, rows)
        record, rows = self.fixture(); record["notices"][0]["notice"]["source_refs"] = []
        with self.assertRaisesRegex(ValueError, "authority notice and support"):
            current_scope_navigation(record, rows)

    def test_no_route_inferred_from_similar_words_or_untyped_card_ids(self):
        record, rows = self.fixture()
        record["notices"] = [{"notice_id": "SN-analogy", "clarification": "Use the same operator construction",
                              "card_ids": ["U1-target"]}]
        self.assertEqual(current_scope_navigation(record, rows)["routes"], [])

    def test_duplicate_and_self_routes_do_not_loop_and_omission_is_visible(self):
        record, rows = self.fixture(); record["notices"] *= 2
        self.assertEqual(current_scope_navigation(record, rows)["total_routes"], 1)
        rows["U2-next"] = dict(rows["U1-target"], id="U2-next")
        record["notices"].append({"notice_id": "SN-new", "current_scope_unit": "U2-next", "source_refs": ["real"]})
        result = current_scope_navigation(record, rows, limit=1)
        self.assertEqual((len(result["routes"]), result["total_routes"], result["omitted_routes"]), (1, 2, 1))
        self.assertEqual(current_scope_navigation(dict(rows["U1-target"], notices=record["notices"]), rows)["total_routes"], 1)

    def test_every_real_route_is_supported_and_search_order_scores_do_not_change(self):
        library = Library(ROOT)
        checked = 0
        for record in library.records.values():
            result = current_scope_navigation(record, library.records)
            checked += result["total_routes"]
            for route in result["routes"]:
                self.assertEqual(route["content_version"], library.records[route["id"]]["content_version"])
        self.assertGreater(checked, 0)
        for method in ("lexical", "content", "structured"):
            before = library._search("N1296", method=method)
            after = library.search("N1296", method=method)
            for response in (before, after):
                for hit in response["results"]:
                    hit.pop("current_scope_navigation", None)
            self.assertEqual(before, after)

    def test_actual_native_menu_route_fetches_current_target_capsule(self):
        from knowledge.mcp_adapter import ResearchAdapter
        adapter = ResearchAdapter(ROOT, method="structured")
        result = adapter.search("N1296")
        hit = next(x for x in result["results"] if x["metadata"].get("record_id", "").startswith("N1296-"))
        routes = hit["metadata"]["current_scope_navigation"]["routes"]
        route = next(x for x in routes if x["id"] == "U1302-causal-prefix-record-preservation")
        identifier, pages = route["fetch_id"], []
        while identifier:
            payload = adapter.fetch(identifier)
            pages.append(payload["text"])
            identifier = payload["metadata"]["next_id"]
        capsule = json.loads("".join(pages))
        self.assertEqual(capsule["content_version"], route["content_version"])
        self.assertEqual(capsule["id"], route["id"])
        self.assertIn("causal", json.dumps(capsule))


if __name__ == "__main__":
    unittest.main()
