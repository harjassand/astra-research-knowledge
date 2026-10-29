"""Offline contextual candidates over current scientific operations.

Embeddings locate records and conditions to inspect. They neither discharge
assumptions nor create compatible interfaces, acceptance or source support.
"""
from __future__ import annotations

from array import array
import json
import math
import os
from pathlib import Path
import re
import sys

from knowledge.model import digest, encoded, flatten, route_id
from knowledge.operations import operation_frame, premise_check, statement_view

MODEL = "knowledge/runtime/contextual/manifest.json"
VIEWS = "knowledge/current/semantic/views.jsonl"
VECTORS = "knowledge/current/semantic/vectors.f32"
INDEX = "knowledge/current/semantic/index.json"
LAYOUT = "current-operation-and-conditions-v1"
DIMENSIONS = 384
INSTRUCTION = "Represent this sentence for searching relevant passages: "


def scientific_views(records):
    """Deterministic projections of authoritative current fields; no manual tags."""
    rows = []
    for record in sorted(records, key=lambda item: item["id"]):
        # Canonical JSON transport sorts dictionary keys. Structured theorem
        # fields must have the same text order before and after publication.
        record = json.loads(encoded(record))
        frame = operation_frame(record)
        statement = statement_view(record, frame)["statement"]
        for role, fields in (
            ("operation", [("Statement", statement), ("Requires", frame["requires"]),
                           ("Returns", frame["returns"])]),
            ("conditions", [("Returns", frame["returns"]), ("Conditions", frame["conditions"]),
                            ("Obstruction", frame["obstruction"]), ("Requires", frame["requires"])])
        ):
            text = record["title"] + "\n" + "\n".join(key + ": " + flatten(value) for key, value in fields)
            rows.append({"id": record["id"], "role": role, "content_version": record["content_version"],
                         "operation_frame_sha256": digest(encoded(frame)),
                         "fields": [key for key, _ in fields], "text": text,
                         "text_sha256": digest(text.encode())})
    return rows


def matrix(data, rows, dimensions=DIMENSIONS):
    if len(data) != rows * dimensions * 4:
        raise ValueError("INGESTION FAILED: contextual vector shape differs")
    values = array("f")
    values.frombytes(data)
    if sys.byteorder != "little":
        values.byteswap()
    for offset in range(0, len(values), dimensions):
        vector = values[offset:offset + dimensions]
        if not all(math.isfinite(value) for value in vector) or abs(sum(v * v for v in vector) - 1) > .002:
            raise ValueError("INGESTION FAILED: contextual vectors must be finite unit vectors")
    return values


class Encoder:
    def __init__(self, root, manifest=None):
        try:
            import numpy as np
            import onnxruntime as ort
            from tokenizers import Tokenizer
        except ImportError as error:
            raise ValueError("Contextual runtime missing. Install knowledge/requirements-agent.txt; portable content/structured search remains available. New semantic views cannot be published stale.") from error
        root = Path(root)
        manifest = manifest or json.loads((root / MODEL).read_bytes())
        if any(manifest.get(key) != value for key, value in {
            "pooling": "CLS", "normalize": "unit_L2", "max_tokens": 512,
            "dimensions": DIMENSIONS, "query_instruction": INSTRUCTION}.items()):
            raise ValueError("Unsupported contextual encoder protocol")
        folder = root / Path(MODEL).parent
        for name, expected in manifest["files"].items():
            if digest((folder / name).read_bytes()) != expected:
                raise ValueError("Contextual model integrity failure: " + name)
        os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
        self.np = np
        self.tokenizer = Tokenizer.from_file(str(folder / "tokenizer.json"))
        self.tokenizer.enable_truncation(max_length=512)
        self.tokenizer.enable_padding(pad_id=0, pad_token="[PAD]")
        options = ort.SessionOptions()
        options.intra_op_num_threads = 2
        options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(str(folder / "model.onnx"), options,
                                           providers=["CPUExecutionProvider"])
        self.names = {item.name for item in self.session.get_inputs()}

    def encode(self, texts):
        values = []
        for offset in range(0, len(texts), 8):
            batch = self.tokenizer.encode_batch(texts[offset:offset + 8])
            feed = {"input_ids": self.np.array([x.ids for x in batch], dtype=self.np.int64),
                    "attention_mask": self.np.array([x.attention_mask for x in batch], dtype=self.np.int64),
                    "token_type_ids": self.np.array([x.type_ids for x in batch], dtype=self.np.int64)}
            vector = self.session.run(None, {k: v for k, v in feed.items() if k in self.names})[0][:, 0, :]
            vector = vector / self.np.maximum(self.np.linalg.norm(vector, axis=1, keepdims=True), 1e-12)
            values.append(vector)
        return self.np.concatenate(values) if values else self.np.empty((0, DIMENSIONS), dtype=self.np.float32)


def projection(root, inputs, records, encode=None):
    """Rebuild membership/text every intake; infer only missing exact-text vectors."""
    root = Path(root)
    manifest = inputs.json(MODEL)
    inputs.read("knowledge/contextual_search.py")
    for name, expected in manifest["files"].items():
        if digest(inputs.read(str(Path(MODEL).parent / name))) != expected:
            raise ValueError("INGESTION FAILED: contextual model bytes changed: " + name)
    model_version = digest(encoded([manifest, digest(inputs.read("knowledge/contextual_search.py"))]))
    rows = scientific_views(records)
    key = lambda row: digest(encoded([LAYOUT, model_version, row["text_sha256"]]))
    cache = {}
    previous_path = root / "knowledge/current/manifest.json"
    if previous_path.is_file():
        outputs = json.loads(previous_path.read_bytes()).get("outputs", {})
        if all(name in outputs and (root / name).is_file() for name in (INDEX, VECTORS, VIEWS)):
            raw = {name: (root / name).read_bytes() for name in (INDEX, VECTORS, VIEWS)}
            if any(digest(raw[name]) != outputs[name] for name in raw):
                raise ValueError("INGESTION FAILED: prior contextual projection integrity differs; restore its recorded bytes before reuse")
            index = json.loads(raw[INDEX])
            prior_rows = [json.loads(line) for line in raw[VIEWS].splitlines()]
            vectors = matrix(raw[VECTORS], len(prior_rows))
            if index["layout"] == LAYOUT and index["model_version"] == model_version:
                if index["views"] != len(prior_rows) or index["dimensions"] != DIMENSIONS:
                    raise ValueError("INGESTION FAILED: contextual cache membership differs")
                if index["views_sha256"] != digest(raw[VIEWS]) or index["vectors_sha256"] != digest(raw[VECTORS]):
                    raise ValueError("INGESTION FAILED: contextual cache mappings differ")
                for number, row in enumerate(prior_rows):
                    if row["text_sha256"] != digest(row["text"].encode()):
                        raise ValueError("INGESTION FAILED: contextual cache text differs")
                    cache[key(row)] = vectors[number * DIMENSIONS:(number + 1) * DIMENSIONS]
    missing = {key(row): row["text"] for row in rows if key(row) not in cache}
    if missing:
        encode = encode or Encoder(root, manifest).encode
        items = list(missing.items())
        for offset in range(0, len(items), 128):
            chunk = items[offset:offset + 128]
            fresh = encode([text for _, text in chunk])
            if len(fresh) != len(chunk):
                raise ValueError("INGESTION FAILED: contextual encoder omitted required views")
            for (identity, _), vector in zip(chunk, fresh):
                values = array("f", vector)
                if len(values) != DIMENSIONS:
                    raise ValueError("INGESTION FAILED: contextual encoder dimension differs")
                cache[identity] = values
    all_values = array("f")
    for row in rows:
        all_values.extend(cache[key(row)])
    if sys.byteorder != "little":
        all_values.byteswap()
    raw_vectors = all_values.tobytes()
    matrix(raw_vectors, len(rows))
    raw_rows = b"".join(encoded(row) for row in rows)
    index = {"schema": "astra.contextual-operation-index.v1", "layout": LAYOUT,
             "model_version": model_version, "views": len(rows), "records": len(records),
             "dimensions": DIMENSIONS, "dtype": "float32-little-endian",
             "views_sha256": digest(raw_rows), "vectors_sha256": digest(raw_vectors),
             "scope": "Two current scientific operation/condition views per canonical record, at stated versions. Token limit512 per view; complete fields, corrections and sources remain in current packets. Candidate discovery only, never acceptance, applicability or composition."}
    return {VIEWS: raw_rows, VECTORS: raw_vectors, INDEX: encoded(index)}


class SemanticIndex:
    def __init__(self, library):
        self.library = library
        root = library.root
        if not (root / INDEX).is_file():
            raise ValueError("Contextual index unavailable for this historical snapshot; use portable content/structured retrieval")
        self.index = json.loads((root / INDEX).read_bytes())
        model = json.loads((root / MODEL).read_bytes())
        version = digest(encoded([model, digest((root / "knowledge/contextual_search.py").read_bytes())]))
        if (self.index.get("schema") != "astra.contextual-operation-index.v1"
                or self.index.get("layout") != LAYOUT or self.index.get("model_version") != version
                or self.index.get("dimensions") != DIMENSIONS):
            raise ValueError("Contextual index/model protocol differs; run the ordinary build/check path")
        raw_views, raw_vectors = (root / VIEWS).read_bytes(), (root / VECTORS).read_bytes()
        if digest(raw_views) != self.index["views_sha256"] or digest(raw_vectors) != self.index["vectors_sha256"]:
            raise ValueError("Contextual index integrity failure")
        self.encoder = Encoder(root)
        self.rows = [json.loads(line) for line in raw_views.splitlines()]
        if (self.rows != scientific_views(list(library.records.values()))
                or self.index["views"] != len(self.rows) or self.index["records"] != len(library.records)):
            raise ValueError("Contextual current-record membership or fields differ; run the ordinary build/check path")
        matrix(raw_vectors, len(self.rows))
        self.vectors = self.encoder.np.frombuffer(raw_vectors, dtype="<f4").reshape(-1, DIMENSIONS)

    def condition_candidates(self, frame, available, unavailable):
        check = premise_check(frame, available, unavailable)
        fields = [(field, clause) for field in ("requires", "conditions", "costs", "units", "obstruction")
                  for clause in re.split(r"(?<=[.;\n])\s+", flatten(frame[field])) if clause.strip()]
        if not check["checks"] or not fields:
            return check
        vectors = self.encoder.encode([text for _, text in fields])
        queries = self.encoder.encode([INSTRUCTION + item["input"] for item in check["checks"]])
        for item, values in zip(check["checks"], queries @ vectors.T):
            item["semantic_spans"] = [{"field": fields[i][0], "text": fields[i][1],
                                       "relevance_cosine": round(float(values[i]), 5)}
                                      for i in self.encoder.np.argsort(-values)[:3]]
        check["semantic_scope"] = "Nearest verbatim conditions to inspect, including possible negations. Cosine is relevance only; no threshold establishes a conflict, satisfies a requirement or validates a supplied fact. Every existing premise state is unchanged."
        return check


def search(library, query, limit=5, kind=None, object_text="", operation="", available=(), unavailable=()):
    if not 1 <= limit <= 50:
        raise ValueError("limit must be in1..50")
    if not isinstance(query, str) or not query.strip() or len(query) > 10000:
        raise ValueError("query must contain1..10000 characters")
    if not hasattr(library, "contextual_index"):
        library.contextual_index = SemanticIndex(library)
    index = library.contextual_index
    task = "\n".join(text for text in (query, object_text, operation) if text)
    scores = index.encoder.encode([INSTRUCTION + task])[0] @ index.vectors.T
    results, seen = [], set()
    for position in index.encoder.np.argsort(-scores):
        row = index.rows[position]
        record = library.records[row["id"]]
        family = (record["parents"] or [record["id"]])[0]
        if family in seen or (kind and record["kind"] != kind):
            continue
        seen.add(family)
        frame = library.operation_frames[record["id"]]
        results.append({"id": record["id"], "title": record["title"], "kind": record["kind"],
                        "content_version": record["content_version"], "ranking_view": row["role"],
                        "relevance_cosine": round(float(scores[position]), 5),
                        "operation_frame": frame, "notice_count": len(record["notices"]),
                        "review_overlays": record["review_overlays"],
                        "premise_check": index.condition_candidates(frame, available, unavailable),
                        "next": {"packet": ["packet", record["id"]], "family_packet": ["packet", family],
                                 "source_selection": "Read complete conditions/corrections and choose actual governing evidence. A semantic match does not establish an interface or source support."},
                        "packet": "knowledge/current/packets/" + route_id(record["id"]) + ".json",
                        **statement_view(record, frame)})
        if len(results) == limit:
            break
    return {"query": query, "object": object_text, "operation": operation, "method": "semantic",
            "model_version": index.index["model_version"], "indexed_records": index.index["records"],
            "scope": index.index["scope"], "results": results}
