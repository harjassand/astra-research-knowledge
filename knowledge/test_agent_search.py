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

    def test_every_current_citation_has_evidence_navigation(self):
        artifacts = [json.loads(line) for line in (ROOT / "knowledge/current/evidence/artifacts.jsonl").read_bytes().splitlines()]
        memberships = {(a["source"]["path"], a["source"]["sha256"], identifier) for a in artifacts for identifier in a["cited_by"]}
        for record in self.library.records.values():
            for ref in record["evidence"]:
                self.assertIn((ref["path"], ref["sha256"], record["id"]), memberships)

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
