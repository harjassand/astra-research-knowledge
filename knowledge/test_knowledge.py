"""Deterministic intake/reader regressions. Scientific usefulness is evaluated separately."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from knowledge.build import build, check, publish
from knowledge.model import ROOT, Inputs, digest, encoded, field_index, query_terms, scientific_text, score_query
from knowledge.retrieve import Library


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in ("knowledge/model.py", "knowledge/build.py", "knowledge/retrieve.py", "knowledge/search.js",
                     "knowledge/index.html", "knowledge/README.md", "knowledge/INTAKE.md", "knowledge/concepts.json",
                     "00_START_HERE.txt", "AGENTS.md", "agent/ACCESS.txt"):
            self.write(name, (ROOT / name).read_bytes())
        self.write("source.txt", b"A finite source statement.\nAssume independent noise.\nThe bound has units seconds.\n")
        self.source = {"path": "source.txt", "sha256": digest((self.root / "source.txt").read_bytes()),
                       "lines": [1, 3], "quote": "Assume independent noise."}
        self.body = b"TITLE: Finite mechanism\nEXACT CLAIM | A finite source statement.\nCOST | All costs are paid.\n"
        self.status = {"card_id": "N1-fixture", "card_path": "cards/N1-fixture.txt",
                       "card_sha256": digest(self.body), "title": "Finite mechanism", "claim_status": "source_derived_unreviewed",
                       "proof_availability": {"located_proof_sources": [self.source]},
                       "depends_on": [], "material_updates": []}
        self.write("cards/N1-fixture.txt", self.body)
        self.statuses()
        self.write("indexes/claims.jsonl", encoded({"id": "N1-fixture", "path": "cards/N1-fixture.txt", "title": "Finite mechanism"}))
        self.write("indexes/agent_catalog.json", encoded({"claims": [{"id": "N1-fixture", "card_sha256": digest(self.body)}]}))
        self.write("indexes/query_aliases.json", b"{}\n")
        self.write("agent/SEMANTIC_NOTICES.jsonl", b"")
        self.write("literature/LEMMA_ATLAS.jsonl", b"")

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def statuses(self):
        self.write("frontier/CURRENT_CLAIM_STATUS.jsonl", encoded(self.status))
        self.write("frontier/cards/N1-fixture.json", encoded(self.status))

    def unit(self):
        unit = {"id": "U1-fixture", "version": 1, "previous": None, "parents": ["N1-fixture"],
                "title": "Finite unit", "statement": "A finite source statement.", "kind": "mechanism", "body": "",
                "contract": {key: "explicit fixture" for key in ("requires", "provides", "assumptions", "costs", "units", "obstruction")},
                "evidence": [self.source], "review": {"acceptance": "not_audited"}}
        self.write("knowledge/units/U1-fixture/v0001.json", encoded(unit))
        return unit

    def compile(self):
        outputs, manifest = build(self.root)
        publish(self.root, outputs)
        return outputs, manifest

    def test_repeated_intake_is_byte_idempotent(self):
        first, _ = self.compile()
        second, _ = self.compile()
        self.assertEqual(first, second)
        check(self.root)

    def test_missing_support_fails_before_publication(self):
        self.compile()
        prior = (self.root / "knowledge/current/manifest.json").read_bytes()
        (self.root / "source.txt").unlink()
        with self.assertRaisesRegex(ValueError, "required source bytes"):
            build(self.root)
        self.assertEqual(prior, (self.root / "knowledge/current/manifest.json").read_bytes())
        with self.assertRaisesRegex(ValueError, "Stale"):
            Library(self.root)

    def test_wrong_branch_quote_and_out_of_range_rejected(self):
        self.unit()
        path = "knowledge/units/U1-fixture/v0001.json"
        unit = json.loads((self.root / path).read_bytes())
        unit["evidence"][0]["quote"] = "A statement from another branch"
        self.write(path, encoded(unit))
        with self.assertRaisesRegex(ValueError, "Wrong supporting passage"):
            build(self.root)
        unit["evidence"][0] = dict(self.source, lines=[1, 999])
        self.write(path, encoded(unit))
        with self.assertRaisesRegex(ValueError, "Invalid source range"):
            build(self.root)

    def test_new_shard_membership_and_tampered_output_refuse_stale(self):
        self.compile()
        self.write("indexes/claims.d/new.jsonl", b"")
        with self.assertRaisesRegex(ValueError, "membership changed"):
            Library(self.root)
        self.compile()
        self.write("knowledge/current/packets/N1.json", b"{}\n")
        with self.assertRaisesRegex(ValueError, "outputs"):
            Library(self.root)

    def test_correction_updates_child_and_direct_dependency(self):
        self.unit()
        self.compile()
        notice = {"notice_id": "SN-test", "card_ids": ["N1-fixture"], "scope": "Only the old branch fails", "evidence": [self.source]}
        self.write("agent/SEMANTIC_NOTICES.d/revision.jsonl", encoded(notice))
        self.compile()
        library = Library(self.root)
        self.assertEqual(library.resolve("U1-fixture")["notices"][0]["scope"], "Only the old branch fails")
        self.assertEqual(library.resolve("N1")["notices"][0]["notice_id"], "SN-test")

    def test_new_and_revised_material_same_pipeline(self):
        self.unit()
        first, _ = self.compile()
        old_record = Library(self.root).resolve("U1-fixture")
        revised = self.body.replace(b"finite source", b"revised finite source")
        self.write("cards/N1-fixture.txt", revised)
        self.status["card_sha256"] = digest(revised)
        self.statuses()
        self.write("indexes/agent_catalog.json", encoded({"claims": [{"id": "N1-fixture", "card_sha256": digest(revised)}]}))
        with self.assertRaisesRegex(ValueError, "Stale"):
            Library(self.root)
        second, _ = self.compile()
        self.assertNotEqual(first["knowledge/current/records.jsonl"], second["knowledge/current/records.jsonl"])
        self.assertEqual(old_record["content_version"], Library(self.root).resolve("U1-fixture")["content_version"])

    def test_missing_card_status_update_is_explicit_failure(self):
        self.write("cards/N1-fixture.txt", b"silently changed")
        with self.assertRaisesRegex(ValueError, "card/status/catalog bytes disagree"):
            build(self.root)

    def test_prior_review_cannot_accept_a_revised_version(self):
        unit = self.unit()
        self.compile()
        record = Library(self.root).resolve("U1-fixture")
        review = {"id": "audit-test", "subjects": [{"id": unit["id"], "content_version": record["content_version"]}],
                  "decision": "accepted_internally_verified", "scope": "conditional finite fixture",
                  "evidence": [self.source]}
        self.write("knowledge/reviews/acceptance.json", encoded(review))
        self.compile()
        self.assertEqual(Library(self.root).resolve(unit["id"])["review_overlays"][0]["decision"], "accepted_internally_verified")
        revised = dict(unit, statement="a different claim", version=2, previous=digest(encoded(unit)))
        self.write("knowledge/units/U1-fixture/v0002.json", encoded(revised))
        self.compile()
        record = Library(self.root).resolve(unit["id"])
        self.assertEqual(record["review_overlays"], [])
        self.assertIn("HISTORICAL VERSION ONLY", record["historical_reviews"][0]["applicability"])

    def test_missing_audit_support_and_broken_version_chain_fail(self):
        unit = self.unit()
        self.write("knowledge/reviews/unsupported.json", encoded({"subjects": [{"id": unit["id"], "content_version": "bad"}],
                   "decision": "accepted_internally_verified", "scope": "claim", "evidence": []}))
        with self.assertRaisesRegex(ValueError, "audit evidence"):
            build(self.root)
        (self.root / "knowledge/reviews/unsupported.json").unlink()
        self.write("knowledge/units/U1-fixture/v0002.json", encoded(dict(unit, version=2, previous="bad")))
        with self.assertRaisesRegex(ValueError, "version chain"):
            build(self.root)

    def test_revised_support_preserves_old_unit_bytes_and_versions(self):
        unit = self.unit()
        old = encoded(unit)
        self.compile()
        self.write("source-v2.txt", b"A new bounded statement.\nAssume dependent noise with a supplied correction.\n")
        reference = {"path": "source-v2.txt", "sha256": digest((self.root / "source-v2.txt").read_bytes()),
                     "lines": [1, 2], "quote": "Assume dependent noise"}
        self.status["proof_availability"]["located_proof_sources"] = [reference]
        self.statuses()
        self.write("knowledge/units/U1-fixture/v0002.json", encoded(dict(unit, version=2, previous=digest(old),
                   evidence=[reference], statement="The revised conditional construction.")))
        self.compile()
        current = Library(self.root).resolve(unit["id"])
        self.assertEqual(current["evidence"][0]["path"], "source-v2.txt")
        self.assertEqual((self.root / "knowledge/units/U1-fixture/v0001.json").read_bytes(), old)
        self.assertEqual(len(current["history"]), 2)

    def test_unmanifested_generated_file_is_stale(self):
        self.compile()
        self.write("knowledge/current/packets/obsolete.json", b"{}\n")
        with self.assertRaisesRegex(ValueError, "output membership"):
            Library(self.root)

    def test_no_bridge_is_not_inferred_from_words_or_types(self):
        self.unit()
        self.compile()
        library = Library(self.root)
        self.assertEqual(library.bridge("N1", "U1-fixture")["state"], "NO SUPPORTED CONNECTION")

    def test_source_and_packet_budgets_never_cut_corrections(self):
        self.compile()
        library = Library(self.root)
        with self.assertRaisesRegex(ValueError, "byte budget"):
            library.packet(["N1"], 20)
        with self.assertRaisesRegex(ValueError, "within the cited"):
            library.source("N1", start=1, end=4)
        self.assertIn("Assume independent noise.", library.source("N1")["text"])

    def test_html_source_is_selected_by_hash_not_first_block(self):
        reference = dict(self.source, path="absent.txt", read_path="export.html")
        self.write("export.html", b"<pre>Wrong branch</pre><pre>A finite source statement.\nAssume independent noise.\nThe bound has units seconds.\n</pre>")
        _, passage = Inputs(self.root).source(reference)
        self.assertIn("Assume independent noise.", passage)
        self.assertNotIn("Wrong branch", passage)


class SearchTests(unittest.TestCase):
    def test_original_qualifiers_and_expansion_are_visible(self):
        concepts = [{"id": "reference", "phrases": ["untouched auxiliary"], "terms": ["reference"]}]
        terms, expansion = query_terms("not every untouched auxiliary", concepts)
        self.assertIn("not", terms)
        self.assertIn("every", terms)
        self.assertEqual(expansion[0]["terms"], ["reference"])

    def test_json_html_is_not_searchable_scientific_text(self):
        raw = json.dumps({"answer": {"innerText": "actual mechanism", "html": "fake boilerplate"}})
        text, selector = scientific_text(raw)
        self.assertEqual(text, "actual mechanism")
        self.assertIn("innerText", selector)

    def test_field_scores_are_deterministic(self):
        documents = [{"title": "matrix compiler", "body": "word"}, {"title": "other", "body": "compiler"}]
        postings = field_index(documents)
        ranked, _, _ = score_query(postings, {"compiler": 1})
        self.assertEqual(ranked[0], 0)
        self.assertEqual(postings, field_index(documents))


if __name__ == "__main__":
    unittest.main()
