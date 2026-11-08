"""Focused byte compatibility for temporary build storage, BM25 and exact cache reuse."""
from itertools import islice
import json
import os
from pathlib import Path
import tempfile
import unittest

from knowledge.build import BuildBytes, BuildSources, field_index_shards, publish
from knowledge.contextual_search import projection, MODEL, VIEWS, VECTORS, INDEX
from knowledge.evidence import projection as evidence_projection
from knowledge.model import ROOT, Inputs, digest, encoded, field_index


def collected(documents, **kwargs):
    return {term: values for _, shard in field_index_shards(documents, **kwargs)
            for term, values in shard.items()}


class BuildStorageCompatibility(unittest.TestCase):
    def test_bm25_original_bytes_for_real_cached_records_and_remapping(self):
        with (ROOT / "knowledge/current/records.jsonl").open() as source:
            documents = [json.loads(line) for line in islice(source, 32)]
        documents += [
            {"title": "alpha alpha β", "body": "beta alpha", "notices": ["retain UNKNOWN"]},
            {"body": "", "contract": {"requires": ["a fixed budget"], "costs": "all bits"}},
            {},
        ]
        self.assertEqual(encoded(field_index(documents)), encoded(collected(documents)))
        body = [{"body": d.get("body", "")} for d in documents[:8]]
        expected = field_index(body)
        remap = [29, 1, 22, 3, 19, 8, 11, 0]
        for values in expected.values():
            for entry in values:
                entry[0] = remap[entry[0]]
        actual = collected(documents[:8], project=lambda d: {"body": d.get("body", "")}, remap=remap)
        self.assertEqual(encoded(expected), encoded(actual))
        self.assertEqual(collected([]), {})

    def test_spooled_outputs_preserve_bytes_and_reject_changed_scratch(self):
        outputs = BuildBytes()
        value = encoded({"unicode": "τ", "values": list(range(80))})
        outputs.write_chunks("knowledge/current/fixture.json", (value[:17], value[17:]))
        self.assertEqual(outputs["knowledge/current/fixture.json"], value)
        self.assertEqual(outputs.sha256("knowledge/current/fixture.json"), digest(value))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            publish(root, outputs)
            target = root / "knowledge/current/fixture.json"
            self.assertEqual(target.read_bytes(), value)
            before = target.stat().st_mtime_ns
            publish(root, outputs)
            self.assertEqual(target.stat().st_mtime_ns, before)
        outputs.path("knowledge/current/fixture.json").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Temporary build output changed"):
            outputs["knowledge/current/fixture.json"]

    def test_source_and_evidence_projection_are_exactly_compatible(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = "A source τ statement.\nConditions and full costs remain.\n".encode()
            (root / "source.txt").write_bytes(raw)
            ref = {"path": "source.txt", "sha256": digest(raw), "lines": [1, 2],
                   "quote": "Conditions and full costs"}
            ordinary, spooled = Inputs(root), Inputs(root)
            spooled.sources = BuildSources()
            self.assertEqual(ordinary.source(ref), spooled.source(ref))
            self.assertEqual(ordinary.source(ref), spooled.source(ref))
            self.assertEqual(ordinary.hashes, spooled.hashes)
            self.assertEqual(list(ordinary.sources), list(spooled.sources))
            bad = dict(ref, quote="not present")
            with self.assertRaisesRegex(ValueError, "Wrong supporting passage"):
                spooled.source(bad)
            records = [{"id": "N-fixture", "evidence": [ref]}]
            before, coverage = evidence_projection(root, Inputs(root), records, [])
            after, actual_coverage = evidence_projection(root, Inputs(root), records, [],
                output_store=BuildBytes(), index_shards=field_index_shards)
            self.assertEqual(coverage, actual_coverage)
            self.assertEqual(set(before), set(after))
            for name, data in before.items():
                self.assertEqual(data, after[name], name)

    def test_original_cached_vectors_are_reused_byte_for_byte_without_inference(self):
        with (ROOT / "knowledge/current/records.jsonl").open() as source:
            records = [json.loads(line) for line in islice(source, 3)]
        with (ROOT / VIEWS).open("rb") as source:
            prior_views = b"".join(islice(source, len(records) * 2))
        with (ROOT / VECTORS).open("rb") as source:
            prior_vectors = source.read(len(records) * 2 * 384 * 4)
        prior_index = json.loads((ROOT / INDEX).read_bytes())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ["knowledge/contextual_search.py", MODEL]:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(ROOT / name, target)
            for name in json.loads((ROOT / MODEL).read_bytes())["files"]:
                target = root / Path(MODEL).parent / name
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(ROOT / Path(MODEL).parent / name, target)
            index = dict(prior_index, views=len(records) * 2, records=len(records),
                         views_sha256=digest(prior_views), vectors_sha256=digest(prior_vectors))
            outputs = {VIEWS: prior_views, VECTORS: prior_vectors, INDEX: encoded(index)}
            for name, data in outputs.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            (root / "knowledge/current/manifest.json").write_bytes(encoded(
                {"outputs": {name: digest(data) for name, data in outputs.items()}}))
            def forbidden(_):
                self.fail("An unchanged cached scientific view must not run model inference")
            actual = projection(root, Inputs(root), records, encode=forbidden)
            self.assertEqual(actual[VECTORS], prior_vectors)
            self.assertEqual(actual[VIEWS], prior_views)
            self.assertEqual(json.loads(actual[INDEX])["model_version"], prior_index["model_version"])


if __name__ == "__main__":
    unittest.main()

