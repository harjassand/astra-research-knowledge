"""Local CPU retrieve/rerank with family expansion and exact source actions.

The model ranks relevance only. It cannot confer acceptance or compatibility.
No network, model service, private database, or source program execution.
"""
import json
import itertools
import os
from pathlib import Path

from knowledge.model import digest, flatten, query_terms, score_query, tokens
from knowledge.operations import premise_check, statement_view, historical_summary, qualified_views

RUNTIME = Path(__file__).parent / "runtime"


def current_scope_candidates(records, seeds, budget=192, kind=None):
    """One query-independent hop over actual curator-authored scope outlinks.

    Seeds retain priority and the fixed overall reranking cap. New targets are
    scored normally with their own scientific statements and qualifications;
    this navigation supplies neither applicability nor acceptance.
    """
    from knowledge.operations import current_scope_navigation
    if not isinstance(budget, int) or not 1 <= budget <= 192:
        raise ValueError("Current-scope candidate budget must be in 1..192")
    candidates = list(dict.fromkeys(seeds))[:budget]
    paths, seen = {}, set(candidates)
    for identifier in tuple(candidates):
        if identifier not in records:
            raise ValueError("Unknown candidate seed: " + identifier)
        navigation = current_scope_navigation(records[identifier], records, limit=50)
        for route in navigation["routes"]:
            target = route["id"]
            if kind and records[target]["kind"] != kind:
                continue
            if target in seen or len(candidates) >= budget:
                continue
            seen.add(target)
            candidates.append(target)
            paths[target] = dict(route, from_record=identifier,
                scope="Explicit current-scope candidate route only; normal relevance scoring applies. No scientific compatibility or acceptance transfer.")
    return candidates, paths


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


def rerank(library, query, limit=5, kind=None, object_text="", operation="", available=(), unavailable=()):
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
    candidates, current_scope_paths = current_scope_candidates(records, seeds, kind=kind)
    siblings = sorted(records.values(), key=lambda r: (families.index(family(r)) if family(r) in families else len(families), r["kind"] == "result", r["id"]))
    for record in siblings:
        if family(record) in families[:24] and (not kind or record["kind"] == kind) and record["id"] not in candidates:
            candidates.append(record["id"])
    candidates = candidates[:192]
    frames = library.operation_frames
    views, pairs, qualification_context = [], [], {}
    for identifier in candidates:
        record, frame = records[identifier], frames[identifier]
        scientific = frame.get("scientific_excerpt", {}).get("text") if historical_summary(record) else None
        if record.get("current_consumer"):
            scientific = record["current_consumer"]["statement"]
        text = record["title"] + "\n" + (scientific or flatten(record["statement"]))
        if record["kind"] != "result":
            text += "\n" + record["body"]
        views.append((identifier, "operation", None))
        pairs.append((task, text))
        for role, qualified, notice_index in qualified_views(record, frame, task):
            qualification_context[len(views)] = notice_index
            views.append((identifier, role, None))
            pairs.append((task, qualified))
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
        if view in ("qualified_operation", "current_notice"):
            item["ranking_view_scope"] = "Relevance-only excerpts of actual current fields; not a proof, complete field or applicability decision. Fetch the complete packet and selected governing source."
        if view == "current_notice":
            notice_index = qualification_context[j]
            notice = record["notices"][notice_index]
            notice_id = notice.get("notice_id")
            from knowledge.model import evidence_refs
            refs = list(evidence_refs(notice))
            item["notice_match"] = {"notice_index": notice_index, "notice_id": notice_id,
                                    "source_count": len(refs),
                                    "scope": "Selected current notice; source indices refer only to this notice, not record.evidence. Inspect the complete notice before choosing a citation."}
            if notice_id and refs:
                item["next"]["notice_source"] = ["source", identifier, "--notice", notice_id, "--evidence", "0"]
        if index is not None:
            item["source_match"] = documents[index]["evidence"]
            item["next"]["source"] = ["source", documents[index]["id"]]
        item.update(statement_view(record, frame))
        if identifier in current_scope_paths:
            item["current_scope_candidate"] = current_scope_paths[identifier]
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
        if records[item["id"]]["kind"] == "result":
            item["next"]["card"] = ["card", item["id"]]
            item["historical_status_is_not_statement"] = historical_summary(records[item["id"]])
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
        navigation = library.peers(item["id"], limit=6)
        if navigation["routes"] or navigation["total_candidates"]:
            item["interface_navigation"] = navigation
            item["next"]["peers"] = ["peers", item["id"]]
    return {"query": query, "object": object_text, "operation": operation, "method": "agent",
            "expansions": expansions, "candidate_records": len(candidates), "ranked_views": len(views),
            "candidate_budget": 192, "family_expansion_budget": 24, "candidate_generators": ["field_BM25_with_visible_expansions", "matched_content_BM25_without_expansion", "one_hop_explicit_current_scope_outlinks"],
            "current_scope_candidate_count": len(current_scope_paths),
            "ranking_views": ["operation", "source_passage", "qualified_operation", "current_notice"],
            "qualification_view_scope": "One bounded current contract view and at most one query-selected current-notice view per candidate. Same model and candidate cap; fields/units stay source-local. Available/unavailable declarations are inspection-only, never positive ranking terms.",
            "model_revision": library.reranker.version,
            "scope": "Relevance candidates, not answers or applicability probabilities. Read next.packet (including corrections/history) and next.source before reuse. Empty/low-scoring results do not establish impossibility. No automatic composition.",
            "results": results}


def search(library, query, limit=5, kind=None, object_text="", operation="", available=(), unavailable=()):
    """Keep contextual, cross-encoder and content leaders on independent scales."""
    from knowledge.mcp_adapter import record_menu
    from knowledge.contextual_search import search as contextual_search
    task = "\n".join(text for text in (query, object_text, operation) if text)
    cross = rerank(library, query, max(8, limit), kind, object_text, operation)
    dense = contextual_search(library, query, max(8, limit), kind, object_text, operation)
    lanes = [dense["results"], cross["results"],
             library.search(task, limit=max(8, limit), method="structured", kind=kind)["results"],
             library.search(task, limit=max(8, limit), method="content", kind=kind)["results"]]
    selected = record_menu(lanes, [], library.records, limit=limit)
    names = ["semantic", "rerank", "structured", "content"]
    family = lambda identifier: (library.records[identifier]["parents"] or [identifier])[0]
    cross_by_id = {hit["id"]: hit for hit in cross["results"]}
    dense_by_id = {hit["id"]: hit for hit in dense["results"]}
    results = []
    for identifier in selected:
        # Fusion selects identities, not a source branch. Preserve the exact
        # selected record's cross-encoder qualification/source navigation,
        # especially --notice routes; record.evidence[0] is not a substitute.
        item = dict(cross_by_id.get(identifier) or next(
            hit for lane in lanes for hit in lane if hit["id"] == identifier))
        if identifier in dense_by_id:
            semantic = dense_by_id[identifier]
            item["semantic_match"] = {key: semantic[key] for key in
                                      ("ranking_view", "relevance_cosine", "content_version")}
        record, frame = library.records[identifier], library.operation_frames[identifier]
        item["operation_frame"] = frame
        item["premise_check"] = library.contextual_index.condition_candidates(frame, available, unavailable)
        item["retrieval_lanes"] = [name for name, lane in zip(names, lanes)
                                   if any(family(hit["id"]) == family(identifier) for hit in lane)]
        item["independent_leader_lanes"] = [name for name, lane in zip(names, lanes)
                                            if lane and family(lane[0]["id"]) == family(identifier)]
        siblings = []
        for hit in cross["results"]:
            if family(hit["id"]) != family(identifier):
                continue
            siblings.extend([hit] + hit.get("within_family", []))
        seen = {identifier}
        item["within_family"] = []
        for sibling in siblings:
            sid = sibling["id"]
            if sid in seen or library.records[sid]["kind"] == "result":
                continue
            seen.add(sid)
            item["within_family"].append({"id": sid, "title": library.records[sid]["title"],
                                         "content_version": library.records[sid]["content_version"],
                                         "next": ["packet", sid]})
            if len(item["within_family"]) == 3:
                break
        item["family_navigation_scope"] = "Separately ranked units; shared family is navigation, not compatible composition or inherited acceptance. Family packet retains all units."
        item.update(statement_view(record, frame))
        results.append(item)
    return {**cross, "method": "agent", "results": results,
            "candidate_generators": cross["candidate_generators"] + ["contextual_current_operations"],
            "contextual_model_version": dense["model_version"],
            "fusion_scope": "Independent semantic/cross-encoder/structured/content family ranks, retaining method leaders. Scores are not combined across scales; no proof or assumption discharge is inferred."}
