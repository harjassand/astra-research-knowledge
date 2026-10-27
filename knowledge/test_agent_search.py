"""Failure-mode checks; exposed examples are not fresh evaluation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from knowledge.evidence import projection, source_indexes, search as evidence_search
from knowledge.model import Inputs, ROOT, digest
from knowledge.operations import operation_frame, premise_check
from knowledge.retrieve import Library


class OperationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_frames_bind_exact_current_content_without_converting_units(self):
        for record in self.library.records.values():
            frame = self.library.operation_frames[record["id"]]
            self.assertEqual(frame, operation_frame(record))
            self.assertEqual(frame["units"], record["contract"].get("units", "UNKNOWN"))

    def test_supplied_facts_do_not_discharge_premises_or_negation(self):
        frame = {"requires": "A calibrated scalar reading without reconstruction.",
                 "conditions": "Finite dimensional only.", "costs": "Charge reset.", "units": "native", "obstruction": "UNKNOWN"}
        check = premise_check(frame, ["calibrated scalar reading"], ["reconstruction"])
        self.assertEqual(check["compatibility"], "NOT ESTABLISHED")
        self.assertEqual(check["checks"][0]["state"], "NOT DISCHARGED")
        self.assertEqual(check["checks"][1]["state"], "INSPECT POTENTIAL CONFLICT")
        self.assertIn("without reconstruction", check["checks"][1]["literal_spans"][0]["text"])

    def test_portable_method_does_not_silently_ignore_assumptions(self):
        with self.assertRaisesRegex(ValueError, "require --method agent"):
            self.library.search("a task", available=["calibration"])

    def test_historical_status_is_not_the_only_visible_scientific_text(self):
        record = self.library.resolve("N557")
        from knowledge.operations import historical_summary
        self.assertTrue(historical_summary(record))
        frame = self.library.operation_frames[record["id"]]
        excerpt = frame["scientific_excerpt"]
        self.assertEqual(excerpt["role"], "claim")
        card = self.library.card(record["id"], *excerpt["lines"])
        self.assertEqual(card["text"].rstrip("\n"), excerpt["text"])
        self.assertIn("independent", excerpt["text"])
        self.assertTrue(any(p["role"] == "interface" for p in frame["card_roles"]))
        self.assertEqual(frame["requires"], record["contract"]["requires"])
        self.assertEqual(card["review_overlays"], record["review_overlays"])
        from knowledge.operations import statement_view
        view = statement_view(record, frame)
        self.assertFalse(view["statement"].startswith("status="))
        self.assertEqual(view["historical_reported_status"], record["statement"])
        self.assertEqual(view["statement_origin"]["lines"], excerpt["lines"])
        packet = self.library.packet([record["id"]], max_bytes=262144)["packets"][0]
        self.assertEqual(packet["scientific_card_excerpt"]["text"], excerpt["text"])
        source = packet["scientific_card_excerpt"]["source"]
        raw = (ROOT / source["path"]).read_bytes()
        self.assertEqual(digest(raw), source["sha256"])
        for record in self.library.records.values():
            frame = self.library.operation_frames[record["id"]]
            if frame.get("scientific_excerpt"):
                selected = frame["scientific_excerpt"]
                lines = record["body"].splitlines(keepends=True)
                expected = "".join(lines[selected["lines"][0] - 1:selected["lines"][1]]).rstrip("\r\n")
                self.assertEqual(expected, selected["text"])

    def test_card_reader_preserves_current_notices_and_never_cuts_them(self):
        record = self.library.resolve("N684")
        read = self.library.card(record["id"], start=1, end=2)
        self.assertEqual(read["notices"], record["notices"])
        with self.assertRaisesRegex(ValueError, "byte budget"):
            self.library.card(record["id"], max_bytes=10)

    def test_completed_internal_amplifier_review_is_current_at_actual_version(self):
        record = self.library.resolve("N557")
        accepted = next(r for r in record["review_overlays"] if r["id"] == "A557-completed-internal-cfdb")
        self.assertEqual(accepted["decision"], "accepted_internally_verified")
        self.assertEqual(accepted["subjects"][0]["content_version"], record["content_version"])
        proof = ROOT / "updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex"
        self.assertEqual(digest(proof.read_bytes()), "cfdbb6a0ca85861788d39c8843ce7533a641633c4cabab8070ac09b9d41d170d")
        self.assertIn("W49", accepted["remaining_gaps"][1])
        self.assertIn("external", accepted["scope"].lower())
        self.assertTrue(any(n.get("notice_id") == "SN-N557-COMPLETED-INTERNAL-REVIEW-RECOGNIZED-20261027" for n in record["notices"]))
        self.assertEqual(self.library.resolve("U675-ordered-word-compiler")["review_overlays"], [])

    def test_optional_card_previews_do_not_break_existing_default_packets(self):
        from knowledge.model import encoded
        for identifier in ("N574", "N552", "N727", "N330", "N166"):
            packet = self.library.packet([identifier])
            packet["checkout_revision"] = "f" * 40
            self.assertLessEqual(len(encoded(packet)), 32768)
            self.assertEqual(packet["packets"][0]["notices"], self.library.resolve(identifier)["notices"])

    def test_every_current_citation_has_evidence_navigation(self):
        artifacts = [json.loads(line) for line in (ROOT / "knowledge/current/evidence/artifacts.jsonl").read_bytes().splitlines()]
        memberships = {(a["source"]["path"], a["source"]["sha256"], identifier) for a in artifacts for identifier in a["cited_by"]}
        from knowledge.model import evidence_refs
        for record in self.library.records.values():
            for ref in evidence_refs(record):
                self.assertIn((ref["path"], ref["sha256"], record["id"]), memberships)
        for transfer in self.library.transfers:
            for ref in evidence_refs(transfer["evidence"]):
                for endpoint in ("from", "to"):
                    self.assertIn((ref["path"], ref["sha256"], transfer[endpoint]), memberships)

    def test_search_window_never_inherits_an_anchor_outside_its_range(self):
        inputs = Inputs(ROOT)
        for document in self.library.documents:
            if document["kind"] == "source_window":
                for ref in document["evidence"]:
                    inputs.source(ref)

    def test_evidence_hit_reads_its_actual_range_and_current_context(self):
        result = evidence_search(self.library, "positive gap is essential", limit=1)["results"][0]
        read = self.library.source(result["id"], max_bytes=262144)
        self.assertEqual(read["source"], result["source"])
        self.assertEqual(read["artifact"]["cited_by"], result["cited_by"])
        raw, _ = Inputs(ROOT).source(result["source"])
        start, end = result["source"]["lines"]
        self.assertEqual(read["text"], "".join(raw.splitlines(keepends=True)[start - 1:end]))


class AdmissionTests(unittest.TestCase):
    def test_valid_json_with_missing_entry_list_cannot_empty_the_view(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "research/update/source"
            folder.mkdir(parents=True)
            index = folder / "INDEX.json"
            index.write_text("[]")
            with self.assertRaisesRegex(ValueError, "INGESTION FAILED"):
                source_indexes(root)
            index.write_text(json.dumps({"record_type": "selected_frozen_source_index"}))
            with self.assertRaisesRegex(ValueError, "INGESTION FAILED"):
                projection(root, Inputs(root), [], source_indexes(root))

    def test_evidence_budget_counts_artifacts_not_windows_of_one_long_source(self):
        from types import SimpleNamespace
        from knowledge.model import encoded
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "knowledge/current/evidence"
            (folder / "postings").mkdir(parents=True)
            artifacts = [{"id": key, "cited_by": [], "declarations": [], "exclusions": [], "scope": "navigation"} for key in ("A1", "A2")]
            documents = [{"id": "E-" + str(i), "artifact_id": "A1" if i < 85 else "A2", "source": {"path": "source.txt", "lines": [1, 1]}, "title": "needle"} for i in range(86)]
            (folder / "artifacts.jsonl").write_bytes(b"".join(encoded(a) for a in artifacts))
            (folder / "documents.jsonl").write_bytes(b"".join(encoded(d) for d in documents))
            (folder / "postings" / (digest(b"needle")[:2] + ".json")).write_bytes(encoded({"needle": [[i, 100 - i] for i in range(86)]}))
            result = evidence_search(SimpleNamespace(root=root), "needle", limit=2)
            self.assertEqual([r["artifact_id"] for r in result["results"]], ["A1", "A2"])

    def test_malformed_index_cannot_silently_remove_evidence_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "research/update/source"
            folder.mkdir(parents=True)
            (folder / "INDEX.json").write_text("{broken")
            with self.assertRaisesRegex(ValueError, "INGESTION FAILED"):
                source_indexes(root)

    def test_new_and_revised_index_entries_regenerate_without_new_forms(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "research/update/source"
            folder.mkdir(parents=True)
            source = folder / "proof.txt"
            index = folder / "INDEX.json"
            def compile(text):
                source.write_text(text)
                index.write_text(json.dumps({"record_type": "selected_frozen_source_index", "originals": [
                    {"path": "proof.txt", "bytes": source.stat().st_size, "sha256": digest(source.read_bytes())}]}))
                inputs = Inputs(root)
                return projection(root, inputs, [], source_indexes(root))
            first, _ = compile("A conditional construction.\n")
            again, _ = compile("A conditional construction.\n")
            self.assertEqual(first, again)
            second, _ = compile("A corrected conditional construction.\n")
            self.assertNotEqual(first, second)
            # The actual source/index bytes are preserved independently; a
            # missing declared original fails even before output publication.
            source.unlink()
            with self.assertRaises(FileNotFoundError):
                projection(root, Inputs(root), [], source_indexes(root))

    def test_metadata_only_still_requires_exact_declared_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "research/update/source"
            folder.mkdir(parents=True)
            (folder / "evidence.pdf").write_bytes(b"%PDF-test")
            index = folder / "INDEX.json"
            index.write_text(json.dumps({"record_type": "selected_frozen_source_index", "originals": [
                {"path": "evidence.pdf", "bytes": 9, "sha256": "0" * 64}]}))
            with self.assertRaisesRegex(ValueError, "INGESTION FAILED"):
                projection(root, Inputs(root), [], source_indexes(root))


@unittest.skipUnless(all(importlib.util.find_spec(m) for m in ("onnxruntime", "tokenizers", "numpy")), "optional agent runtime not installed")
class LocalRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_local_model_and_generic_family_expansion_find_exposed_mechanisms(self):
        probes = [("which one extra experiment resolves two indistinguishable action choices", "N1089"),
                  ("coherent probe selectivity should pay interference and all collateral atoms", "N1092"),
                  ("smooth passive device fits all historical observations but activates above untested dose", "N1090")]
        from knowledge.model import route_id
        for query, expected in probes:
            response = self.library.search(query, method="agent", unavailable=["calibration"])
            self.assertIn(expected, {route_id((self.library.records[r["id"]]["parents"] or [r["id"]])[0]) for r in response["results"]})
            self.assertTrue(all(r["premise_check"]["compatibility"] == "NOT ESTABLISHED" for r in response["results"]))
            for hit in response["results"]:
                if hit.get("source_match"):
                    source = self.library.source(hit["next"]["source"][1], max_bytes=1048576)
                    self.assertEqual(source["source"], hit["source_match"][0])

    def test_named_compiler_still_first_with_neural_ranking(self):
        response = self.library.search("ordered-word inverse-Jordan compiler", method="agent")
        self.assertEqual(response["results"][0]["id"], "U675-ordered-word-compiler")

    def test_content_candidates_recover_retry_passage_without_id_ranking_rules(self):
        response = self.library.search("When a monomer fails to incorporate I retry the same synthesis step. The light pulse also occasionally unlocks later addresses. How should retry frequency enter the eventual correct-chain yield?", method="agent")
        self.assertTrue(any(r["id"] == "U1083-fresh-retry-downstream-exposure" for r in response["results"]))
        self.assertIn("matched_content_BM25_without_expansion", response["candidate_generators"])

    def test_family_menu_exposes_alternative_construction_and_no_guessed_source(self):
        response = self.library.search("I need two jointly valid samples from a tagged permutation experiment. A witness is not supplied and I cannot invert the permutation. Could a shared random seed and forward evaluations generate the whole joint object instead?", method="agent")
        hits = response["results"]
        ids = {r["id"] for r in hits} | {u["id"] for r in hits for u in r["within_family"]}
        self.assertIn("U1015-forward-joint-cover", ids)
        for hit in hits:
            self.assertIn("source_selection", hit["next"])
            if hit.get("ranking_view") == "operation":
                self.assertNotIn("source", hit["next"])
