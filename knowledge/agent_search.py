"""Local CPU retrieve/rerank with family expansion and exact source actions.

The model ranks relevance only. It cannot confer acceptance or compatibility.
No network, model service, private database, or source program execution.
"""
import json
import itertools
import os
from pathlib import Path

from knowledge.model import digest, flatten, query_terms, score_query, tokens
from knowledge.operations import premise_check

RUNTIME = Path(__file__).parent / "runtime"


class Reranker:
    def __init__(self):
        try:
            import numpy as np
            import onnxruntime as ort
            from tokenizers import Tokenizer
        except ImportError as error:
            raise ValueError("Agent runtime missing. Install knowledge/requirements-agent.txt in a local Python 3.12/3.13 environment; portable --method structured remains available.") from error
        manifest = json.loads((RUNTIME / "manifest.json").read_text())
        for name, expected in manifest["files"].items():
            if digest((RUNTIME / name).read_bytes()) != expected:
                raise ValueError("Agent model integrity failure: " + name)
        os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
        self.np = np
        self.tokenizer = Tokenizer.from_file(str(RUNTIME / "tokenizer.json"))
        self.tokenizer.enable_truncation(max_length=512)
        self.tokenizer.enable_padding(pad_id=0, pad_token="[PAD]")
        options = ort.SessionOptions()
        options.intra_op_num_threads = 2
        options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(str(RUNTIME / "model.onnx"), options, providers=["CPUExecutionProvider"])
        self.version = manifest["upstream_revision"]

    def score(self, pairs):
        scores, truncated = [], []
        for offset in range(0, len(pairs), 16):
            batch = self.tokenizer.encode_batch(pairs[offset:offset + 16])
            feed = {"input_ids": self.np.array([x.ids for x in batch], dtype=self.np.int64),
                    "attention_mask": self.np.array([x.attention_mask for x in batch], dtype=self.np.int64),
                    "token_type_ids": self.np.array([x.type_ids for x in batch], dtype=self.np.int64)}
            scores.extend(self.session.run(None, feed)[0].reshape(-1).tolist())
            truncated.extend(bool(x.overflowing) for x in batch)
        return scores, truncated


def search(library, query, limit=5, kind=None, object_text="", operation="", available=(), unavailable=()):
    if not 1 <= limit <= 50:
        raise ValueError("limit must be in 1..50")
    # Assumption declarations are inspection inputs, not positive ranking terms:
    # adding 'no calibration' must not reward a calibration-dependent result.
    task = "\n".join(x for x in (query, object_text, operation) if x)
    terms, expansions = query_terms(task, library.catalog["concepts"])
    postings = {}
    for shard in sorted({digest(term.encode())[:2] for term in terms}):
        path = library.root / "knowledge/current/postings" / (shard + ".json")
        if path.is_file():
            postings.update(json.loads(path.read_bytes()))
    ranked, lexical_scores, matches = score_query(postings, terms)
    original_terms = {term: 1.0 for term in tokens(task)}
    content_postings = {}
    for shard in sorted({digest(term.encode())[:2] for term in original_terms}):
        path = library.root / "knowledge/current/content" / (shard + ".json")
        if path.is_file():
            content_postings.update(json.loads(path.read_bytes()))
    content_ranked, _, _ = score_query(content_postings, original_terms)
    # Independent candidate generators: field weights can bury a complete
    # source passage while unweighted content can bury a concise operation.
    ranked = list(dict.fromkeys(index for pair in itertools.zip_longest(ranked, content_ranked)
                                for index in pair if index is not None))
    documents = library.documents
    records = library.records
    family = lambda r: (r["parents"] or [r["id"]])[0]
    families, seeds = [], {}
    for index in ranked:
        record = records[documents[index]["record_id"]]
        if kind and record["kind"] != kind:
            continue
        seeds.setdefault(record["id"], index)
        if family(record) not in families:
            families.append(family(record))
        if len(seeds) >= 80:
            break
    # Expand siblings BEFORE grouping results: an unmentioned intermediate can
    # be relevant even when the broad parent has only a moderately ranked hit.
    candidates = list(seeds)
    siblings = sorted(records.values(), key=lambda r: (families.index(family(r)) if family(r) in families else len(families), r["kind"] == "result", r["id"]))
    for record in siblings:
        if family(record) in families[:24] and (not kind or record["kind"] == kind) and record["id"] not in seeds:
            candidates.append(record["id"])
    candidates = candidates[:192]
    frames = library.operation_frames
    views, pairs = [], []
    for identifier in candidates:
        record, frame = records[identifier], frames[identifier]
        text = record["title"] + "\n" + flatten(record["statement"])
        if record["kind"] != "result":
            text += "\n" + record["body"]
        views.append((identifier, "operation", None))
        pairs.append((task, text))
    # Source passages supply buried constructions; keep their score/route
    # separate from a synthesized card. Never redirect them to evidence[0].
    for identifier, index in seeds.items():
        doc = documents[index]
        if doc["kind"] != "source_window":
            continue
        ref = doc["evidence"][0]
        from knowledge.model import Inputs, scientific_text
        _, passage = Inputs(library.root).source(ref)
        text, _ = scientific_text(passage)
        views.append((identifier, "source_passage", index))
        pairs.append((task, records[identifier]["title"] + "\n" + text))
    if not hasattr(library, "reranker"):
        library.reranker = Reranker()
    values, truncated = library.reranker.score(pairs)
    results, seen = [], set()
    for j in sorted(range(len(views)), key=lambda j: (-values[j], j)):
        identifier, view, index = views[j]
        record = records[identifier]
        group = family(record)
        if group in seen:
            continue
        seen.add(group)
        frame = frames[identifier]
        item = {"id": identifier, "title": record["title"], "kind": record["kind"],
                "content_version": record["content_version"], "relevance_logit": round(values[j], 5),
                "ranking_view": view, "ranking_text_truncated": truncated[j],
                "statement": record["statement"], "operation_frame": frame,
                "premise_check": premise_check(frame, available, unavailable),
                "notice_count": len(record["notices"]), "review_decisions": [
                    {key: review[key] for key in ("decision", "scope", "subject") if key in review}
                    for review in record["review_overlays"]],
                "next": {"packet": ["packet", identifier], "family_packet": ["packet", group],
                         "source_selection": "Inspect packet.evidence scopes and choose --evidence INDEX; different citations may support different subclaims. No first citation is presumed to prove the entire statement."},
                "packet": "knowledge/current/packets/" + identifier.split("-", 1)[0] + ".json" if record["kind"] == "result" else "knowledge/current/packets/" + identifier + ".json"}
        if index is not None:
            item["source_match"] = documents[index]["evidence"]
            item["next"]["source"] = ["source", documents[index]["id"]]
        results.append(item)
        if len(results) == limit:
            break
    # Preserve an independent full-card route: neural relevance is unreliable
    # on mathematical notation and can overvalue a familiar physical analogy.
    safety = library.search(task, limit=1, method="lexical", kind=kind)["results"]
    if limit > 1 and safety and family(records[safety[0]["id"]]) not in seen:
        record = records[safety[0]["id"]]
        frame = frames[record["id"]]
        results = results[:limit - 1] + [{**safety[0], "content_version": record["content_version"],
            "ranking_view": "full_card_lexical_safety; independent score scale", "operation_frame": frame,
            "premise_check": premise_check(frame, available, unavailable),
            "next": {"packet": ["packet", record["id"]], "family_packet": ["packet", record["id"]],
                     "source_selection": "Inspect packet.evidence scopes and choose --evidence INDEX; no first citation is presumed to prove the entire statement."}}]
    for item in results:
        group = family(records[item["id"]])
        alternatives, selected = [], {item["id"]}
        for j in sorted(range(len(views)), key=lambda j: (-values[j], j)):
            identifier = views[j][0]
            record = records[identifier]
            if identifier in selected or family(record) != group or record["kind"] == "result":
                continue
            selected.add(identifier)
            alternatives.append({"id": identifier, "title": record["title"], "content_version": record["content_version"],
                                 "next": ["packet", identifier]})
            if len(alternatives) == 3:
                break
        item["within_family"] = alternatives
        item["family_navigation_scope"] = "Up to three separately ranked units; the family packet lists all units. Shared family is navigation, not compatibility or inherited acceptance."
    return {"query": query, "object": object_text, "operation": operation, "method": "agent",
            "expansions": expansions, "candidate_records": len(candidates), "ranked_views": len(views),
            "candidate_budget": 192, "family_expansion_budget": 24, "candidate_generators": ["field_BM25_with_visible_expansions", "matched_content_BM25_without_expansion"],
            "model_revision": library.reranker.version,
            "scope": "Relevance candidates, not answers or applicability probabilities. Read next.packet (including corrections/history) and next.source before reuse. Empty/low-scoring results do not establish impossibility. No automatic composition.",
            "results": results}
