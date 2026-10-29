"""Protect incremental current membership, vector integrity and premise boundaries."""
from array import array
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from knowledge.contextual_search import (DIMENSIONS, INDEX, MODEL, VECTORS, VIEWS,
                                         Encoder, SemanticIndex, matrix, projection, scientific_views)
from knowledge.model import ROOT, Inputs, digest, encoded
from knowledge.operations import operation_frame


def record(identifier="U-test"):
    return {"id": identifier, "parents": ["N-test"], "kind": "mechanism",
            "content_version": "1" * 64, "title": "Supplied finite operation",
            "statement": "The supplied operation returns a finite bound.", "body": "Actual source construction.",
            "contract": {"requires": "A measured input.", "provides": "A conditional bound.",
                         "assumptions": "Independent fresh bath. No returning record.",
                         "costs": "Charge preparation.", "units": "seconds", "obstruction": "Unknown input."},
            "notices": [], "review_overlays": []}


class IncrementalContextualTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("knowledge/contextual_search.py", b"fixture protocol version1")
        self.write("knowledge/runtime/contextual/model.onnx", b"inert test artifact")
        self.write(MODEL, encoded({"files": {"model.onnx": digest(b"inert test artifact")}}))
        self.calls = []

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def encode(self, texts):
        self.calls.extend(texts)
        result = []
        for text in texts:
            vector = [0.] * DIMENSIONS
            vector[int(digest(text.encode())[:8], 16) % DIMENSIONS] = 1.
            result.append(vector)
        return result

    def compile(self, records):
        outputs = projection(self.root, Inputs(self.root), records, encode=self.encode)
        for name, data in outputs.items():
            self.write(name, data)
        self.write("knowledge/current/manifest.json", encoded({"outputs": {name: digest(data) for name, data in outputs.items()}}))
        return outputs

    def test_new_revised_and_removed_records_have_complete_current_membership(self):
        original = record()
        first = self.compile([original])
        self.assertEqual(len(self.calls), 2)
        self.calls.clear()
        self.assertEqual(first, self.compile([original]))
        self.assertEqual(self.calls, [])
        revised = copy.deepcopy(original)
        revised["content_version"] = "2" * 64
        revised["contract"]["assumptions"] = "The returning bath is retained with its real history."
        second = self.compile([revised, record("U-new")])
        self.assertEqual(len(self.calls), 1)  # unchanged scientific text reuses its vector even at another ID
        rows = [json.loads(line) for line in second[VIEWS].splitlines()]
        self.assertEqual({row["id"] for row in rows}, {"U-test", "U-new"})
        self.assertEqual({row["content_version"] for row in rows if row["id"] == "U-test"}, {"2" * 64})
        self.assertIn("returning bath", next(row["text"] for row in rows if row["id"] == "U-test" and row["role"] == "conditions"))
        self.calls.clear()
        third = self.compile([revised])
        self.assertEqual(self.calls, [])
        self.assertEqual(json.loads(third[INDEX])["views"], 2)
        self.assertEqual(len(third[VECTORS]), 2 * DIMENSIONS * 4)

    def test_current_consumer_overrides_historical_contract_without_promoting_review(self):
        item = record()
        item["current_consumer"] = {"statement": "Actual corrected operation.",
                                    "contract": dict(item["contract"], requires="Actual supplied source inputs."),
                                    "authority_notice": "Exact-version correction"}
        rows = scientific_views([item])
        self.assertTrue(all("Actual supplied source inputs." in row["text"] for row in rows))
        self.assertTrue(all("A measured input." not in row["text"] for row in rows))
        self.assertEqual(item["review_overlays"], [])

    def test_structured_statement_views_survive_canonical_json_transport(self):
        item = record()
        item["statement"] = {"quantifiers": "For every supplied finite object.",
                             "claim": "One common construction returns the bound.",
                             "assumptions": "The given resource is paid."}
        before = copy.deepcopy(item)
        transported = json.loads(encoded(item))
        self.assertEqual(scientific_views([item]), scientific_views([transported]))
        self.assertEqual(item, before)

    def test_corrupt_prior_vector_cannot_be_reused_or_published_silently(self):
        self.compile([record()])
        path = self.root / VECTORS
        damaged = bytearray(path.read_bytes()); damaged[0] ^= 1; path.write_bytes(damaged)
        with self.assertRaisesRegex(ValueError, "prior contextual projection integrity"):
            self.compile([record()])

    def test_protocol_or_model_change_invalidates_every_cached_vector(self):
        self.compile([record()]); self.calls.clear()
        self.write("knowledge/contextual_search.py", b"fixture protocol version2")
        self.compile([record()])
        self.assertEqual(len(self.calls), 2)
        self.calls.clear()
        self.write("knowledge/runtime/contextual/model.onnx", b"changed model")
        with self.assertRaisesRegex(ValueError, "model bytes changed"):
            self.compile([record()])

    def test_partial_encoder_output_and_nonfinite_vectors_fail(self):
        with self.assertRaisesRegex(ValueError, "omitted required views"):
            projection(self.root, Inputs(self.root), [record()], encode=lambda texts: [])
        with self.assertRaisesRegex(ValueError, "finite unit vectors"):
            matrix(array("f", [float("nan")] * DIMENSIONS).tobytes(), 1)
        with self.assertRaisesRegex(ValueError, "shape differs"):
            matrix(b"", 1)

    def test_query_reader_rejects_stale_record_views_even_with_valid_vector_hashes(self):
        self.compile([record()])
        revised = record(); revised["contract"]["requires"] = "Changed acquisition input."
        library = SimpleNamespace(root=self.root, records={revised["id"]: revised})
        with patch("knowledge.contextual_search.Encoder"), self.assertRaisesRegex(ValueError, "current-record membership or fields differ"):
            SemanticIndex(library)


@unittest.skipUnless(all(importlib.util.find_spec(name) for name in ("numpy", "onnxruntime", "tokenizers")), "free CPU runtime not installed")
class ContextualRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.encoder = Encoder(ROOT)

    def test_real_cpu_model_returns_normalized_finite_cls_vectors(self):
        vectors = self.encoder.encode(["A finite source operation with explicit conditions."])
        self.assertEqual(vectors.shape, (1, DIMENSIONS))
        matrix(vectors.astype("<f4").tobytes(), 1)

    def test_semantic_condition_spans_are_verbatim_and_never_discharge_negated_premises(self):
        item = record(); frame = operation_frame(item)
        index = object.__new__(SemanticIndex); index.encoder = self.encoder
        result = index.condition_candidates(frame, ["fresh environment"], ["returning quantum record"])
        self.assertEqual(result["compatibility"], "NOT ESTABLISHED")
        self.assertEqual(result["checks"][0]["state"], "NOT DISCHARGED")
        for check in result["checks"]:
            self.assertTrue(check["semantic_spans"])
            for span in check["semantic_spans"]:
                self.assertIn(span["text"], frame[span["field"]])
        self.assertIn("possible negations", result["semantic_scope"])


if __name__ == "__main__":
    unittest.main()
