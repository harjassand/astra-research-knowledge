"""Separate evidence navigation: registered ranges and selected public originals.

Artifacts never become accepted lemmas. Source indexes admit only their explicit
public path entries; origin/receipt/private workspace paths are never followed.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path

from knowledge.model import compact_ref, digest, encoded, field_index, local, scientific_text


def source_indexes(root):
    found = []
    for path in sorted((root / "research").rglob("INDEX.json")):
        try:
            value = json.loads(path.read_bytes())
        except (ValueError, UnicodeError) as error:
            if path.parent.name == "source":
                raise ValueError("INGESTION FAILED: invalid public source index: " + str(path)) from error
            continue
        if value.get("schema") == "astra.intake-source-index.v1" or value.get("record_type") == "selected_frozen_source_index":
            found.append(path.relative_to(root).as_posix())
        elif path.parent.name == "source":
            raise ValueError("INGESTION FAILED: unsupported public source-index schema: " + str(path))
    return found


def projection(root, inputs, records, index_paths):
    artifacts = {}

    def add(ref, record=None, declaration=None, exclusion=None):
        key = (ref["path"], ref["sha256"], ref.get("read_path"))
        identifier = "A-" + digest(encoded(key))[:24]
        item = artifacts.setdefault(identifier, {"id": identifier, "source": {k: v for k, v in ref.items() if k not in ("lines", "quote", "range_scope", "locator_scope")},
            "cited_by": [], "declarations": [], "ranges": [], "exclusions": [],
            "scope": "Evidence navigation only. A citation/coarchive is not a logical dependency or scientific acceptance."})
        if record and record not in item["cited_by"]:
            item["cited_by"].append(record)
        if declaration:
            item["declarations"].append(declaration)
        if exclusion:
            item["exclusions"].append(exclusion)
        elif ref.get("lines"):
            item["ranges"].append(ref["lines"])
        return item

    for record in records:
        for ref in record["evidence"]:
            add(compact_ref(ref), record=record["id"], exclusion="binary; original artifact route only" if ref.get("lines") is None else None)
    for name in index_paths:
        index = inputs.json(name)
        parent = Path(name).parent.parent if index.get("schema") == "astra.intake-source-index.v1" else Path(name).parent
        for entry in index.get("files", index.get("originals", [])):
            path = (parent / entry["path"]).as_posix()
            data = inputs.read(path)
            if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
                raise ValueError("INGESTION FAILED: declared public original missing/mismatched: " + path)
            ref = {"path": path, "sha256": entry["sha256"], "lines": None}
            reason = None
            kind = entry.get("kind", "frozen_original")
            # Selected extraction/index scopes must not be widened to a full
            # transcript or external publication by an automatic adapter.
            if "derived_non_authoritative" in kind or "curator_extract" in kind:
                reason = "scoped extraction; only existing statement-specific citations are searched"
            elif any(part in path.lower() for part in ("upstream_source", "/dependencies/", "source_receipt", "acquired_objects")):
                reason = "upstream/operational artifact; metadata only unless explicitly cited"
            elif Path(path).suffix.lower() in (".pdf", ".html", ".zip", ".gz", ".png", ".jpg", ".npy", ".npz", ".onnx"):
                reason = "binary/external container; metadata only unless explicitly cited"
            else:
                try:
                    text = data.decode("utf-8")
                    if text.splitlines():
                        ref["lines"] = [1, len(text.splitlines())]
                    else:
                        reason = "empty original; metadata only"
                except UnicodeError:
                    reason = "binary; metadata only"
            add(ref, declaration={"index": name, "index_sha256": inputs.hashes[name], "kind": kind}, exclusion=reason)
    documents = []
    for item in artifacts.values():
        merged = []
        for lower, upper in sorted(item["ranges"]):
            if merged and lower <= merged[-1][1] + 1:
                merged[-1][1] = max(upper, merged[-1][1])
            else:
                merged.append([lower, upper])
        item["ranges"] = merged
        if not merged:
            documents.append({"id": "E-" + digest(encoded({"artifact": item["id"], "metadata_only": True}))[:24],
                "artifact_id": item["id"], "source": dict(item["source"], lines=None),
                "title": Path(item["source"]["path"]).name,
                "body": item["source"]["path"] + " " + " ".join(item["exclusions"]),
                "text_selection": "metadata only; no scientific passage inferred"})
        for lower, upper in merged:
            ref = dict(item["source"], lines=[lower, upper])
            text, passage = inputs.source(ref)
            searchable, selector = scientific_text(passage)
            # JSON selectors retain the original range; derived character
            # offsets are never passed off as authoritative source line numbers.
            chunks = [(ref, searchable)]
            if selector == "unchanged_utf8":
                lines = text.splitlines(keepends=True)
                chunks = [(dict(ref, lines=[start, min(upper, start + 79)]),
                           "".join(lines[start - 1:min(upper, start + 79)])) for start in range(lower, upper + 1, 64)]
            for selected, body in chunks:
                documents.append({"id": "E-" + digest(encoded({"artifact": item["id"], "source": selected}))[:24],
                    "artifact_id": item["id"], "source": selected, "title": Path(ref["path"]).name,
                    "body": body, "text_selection": selector})
    outputs = {"knowledge/current/evidence/artifacts.jsonl": b"".join(encoded(v) for v in artifacts.values()),
               "knowledge/current/evidence/documents.jsonl": b"".join(encoded({k: v for k, v in d.items() if k != "body"}) for d in documents)}
    shards = defaultdict(dict)
    for term, values in field_index(documents).items():
        shards[digest(term.encode())[:2]][term] = values
    for shard, values in shards.items():
        outputs["knowledge/current/evidence/postings/" + shard + ".json"] = encoded(values)
    coverage = {"artifacts": len(artifacts), "searchable_artifacts": sum(bool(v["ranges"]) for v in artifacts.values()),
                "evidence_windows": len(documents), "selected_source_indexes": len(index_paths),
                "exclusion_mentions": dict(Counter(x for v in artifacts.values() for x in v["exclusions"])),
                "denominator": "Distinct (public path, SHA256, read_path) keys in current record evidence plus explicit entries in recognized selected-public-source indexes. Aliases may share bytes; counts are not distinct discoveries.",
                "unassessed": "Unregistered archives, other source-index formats, private/withheld work, scientific completeness and unextracted reusable mechanisms. Metadata-only exclusions retain explicit reasons."}
    return outputs, coverage


def search(library, query, limit=5, method="field"):
    from knowledge.model import tokens, score_query
    if not 1 <= limit <= 50:
        raise ValueError("limit must be in 1..50")
    folder = library.root / "knowledge/current/evidence"
    docs = [json.loads(line) for line in (folder / "documents.jsonl").read_bytes().splitlines()]
    artifacts = {a["id"]: a for a in (json.loads(line) for line in (folder / "artifacts.jsonl").read_bytes().splitlines())}
    terms = {term: 1.0 for term in tokens(query)}
    postings = {}
    for shard in sorted({digest(term.encode())[:2] for term in terms}):
        path = folder / "postings" / (shard + ".json")
        if path.is_file():
            postings.update(json.loads(path.read_bytes()))
    ranked, scores, _ = score_query(postings, terms)
    ranked = ranked[:80]
    truncated = {}
    if method == "agent":
        from knowledge.agent_search import Reranker
        from knowledge.model import Inputs
        if not hasattr(library, "reranker"):
            library.reranker = Reranker()
        pairs = []
        for index in ranked:
            if docs[index]["source"].get("lines") is None:
                passage = docs[index]["source"]["path"] + " " + docs[index]["text_selection"]
            else:
                _, passage = Inputs(library.root).source(docs[index]["source"])
            pairs.append((query, docs[index]["title"] + "\n" + scientific_text(passage)[0]))
        values, overflow = library.reranker.score(pairs)
        scores = dict(zip(ranked, values))
        truncated = dict(zip(ranked, overflow))
        ranked.sort(key=lambda index: -scores[index])
    results, seen = [], set()
    for index in ranked:
        doc = docs[index]
        if doc["artifact_id"] in seen:
            continue
        seen.add(doc["artifact_id"])
        artifact = artifacts[doc["artifact_id"]]
        results.append({**doc, "score": round(scores[index], 5), "ranking_text_truncated": truncated.get(index, False),
                        "cited_by": artifact["cited_by"], "declarations": artifact["declarations"],
                        "next": ["source", doc["id"]] if doc["source"].get("lines") else {"original_public_path": doc["source"]["path"]},
                        "exclusions": artifact["exclusions"], "scope": artifact["scope"]})
        if len(results) == limit:
            break
    return {"query": query, "method": method, "results": results,
            "scope": "Evidence discovery, not scientific acceptance. Follow exact E-id source and cited_by packets; uncited originals require a scientific review before reuse as premises."}
