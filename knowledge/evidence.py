"""Separate evidence navigation: registered ranges and selected public originals.

Artifacts never become accepted lemmas. Source indexes admit only their explicit
public path entries; origin/receipt/private workspace paths are never followed.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path

from knowledge.model import compact_ref, digest, encoded, evidence_refs, field_index, local, scientific_text


def source_indexes(root):
    found = []
    candidates = {path for name in ("INDEX.json", "SOURCE_INDEX.json")
                  for path in (root / "research").rglob(name)}
    for path in sorted(candidates):
        public_declaration = path.parent.name == "source" or path.name == "SOURCE_INDEX.json"
        try:
            value = json.loads(path.read_bytes())
        except (ValueError, UnicodeError) as error:
            if public_declaration:
                raise ValueError("INGESTION FAILED: invalid public source index: " + str(path)) from error
            continue
        if not isinstance(value, dict):
            if public_declaration:
                raise ValueError("INGESTION FAILED: public source index must be an object: " + str(path))
            continue
        if value.get("schema") in ("astra.intake-source-index.v1", "astra.scientific-source-selection.v1") or value.get("record_type") == "selected_frozen_source_index":
            found.append(path.relative_to(root).as_posix())
        elif public_declaration:
            raise ValueError("INGESTION FAILED: unsupported public source-index schema: " + str(path))
    return found


def projection(root, inputs, records, index_paths, transfers=()):
    artifacts = {}
    declarations = []

    def add(ref, record=None, declaration=None, exclusion=None, role="record_citation"):
        key = (ref["path"], ref["sha256"], ref.get("read_path"))
        identifier = "A-" + digest(encoded(key))[:24]
        item = artifacts.setdefault(identifier, {"id": identifier, "source": {k: v for k, v in ref.items() if k not in ("lines", "quote", "range_scope", "locator_scope")},
            "cited_by": [], "citation_roles": [], "declarations": [], "ranges": [], "exclusions": [],
            "scope": "Evidence navigation only. A citation/coarchive is not a logical dependency or scientific acceptance."})
        if record and record not in item["cited_by"]:
            item["cited_by"].append(record)
        if record and {"record_id": record, "role": role} not in item["citation_roles"]:
            item["citation_roles"].append({"record_id": record, "role": role})
        if declaration:
            item["declarations"].append(declaration)
        if exclusion:
            item["exclusions"].append(exclusion)
        elif ref.get("lines"):
            item["ranges"].append(ref["lines"])
        return item

    for record in records:
        # Audits, corrections, historical reviews and relationship support are
        # registered citations too. Never silently omit them from discovery.
        for field, value in record.items():
            for ref in evidence_refs(value):
                add(compact_ref(ref), record=record["id"], role=field,
                    exclusion="binary; original artifact route only" if ref.get("lines") is None else None)
    for transfer in transfers:
        for endpoint in ("from", "to"):
            for ref in evidence_refs(transfer.get("evidence", [])):
                add(compact_ref(ref), record=transfer[endpoint], role="transfer: " + transfer["state"],
                    exclusion="binary; original artifact route only" if ref.get("lines") is None else None)
    for name in index_paths:
        index = inputs.json(name)
        schema = index.get("schema")
        parent = Path(name).parent.parent if schema == "astra.intake-source-index.v1" else Path(name).parent
        entries = index.get("files") if schema in ("astra.intake-source-index.v1", "astra.scientific-source-selection.v1") else index.get("originals")
        path_field = "repository_path" if schema == "astra.scientific-source-selection.v1" else "path"
        if not isinstance(entries, list) or not entries:
            raise ValueError("INGESTION FAILED: selected source index requires a nonempty explicit entry list: " + name)
        declared_versions = []
        for entry in entries:
            if not isinstance(entry, dict) or not {path_field, "sha256", "bytes"} <= entry.keys() or type(entry["bytes"]) is not int or entry["bytes"] < 0:
                raise ValueError("INGESTION FAILED: selected source entry lacks path/hash/byte support: " + name)
            path = (parent / entry[path_field]).as_posix()
            data = inputs.read(path)
            if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
                raise ValueError("INGESTION FAILED: declared public original missing/mismatched: " + path)
            ref = {"path": path, "sha256": entry["sha256"], "lines": None}
            declared_versions.append((path, entry["sha256"]))
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
        declarations.append((name, declared_versions))

    # A declaration may use the original path while an existing citation also
    # supplies a read_path. Link identical source versions for correction/context
    # navigation without widening any citation's statement-support range.
    contexts = defaultdict(set)
    for item in artifacts.values():
        key = (item["source"]["path"], item["source"]["sha256"])
        contexts[key].update(item["cited_by"])
    for item in artifacts.values():
        if not item["declarations"]:
            continue
        key = (item["source"]["path"], item["source"]["sha256"])
        for record_id in sorted(contexts[key] - set(item["cited_by"])):
            item["cited_by"].append(record_id)
            item["citation_roles"].append({"record_id": record_id, "role": "same_source_version_context; inspect the record's actual citation range"})

    index_coverage = []
    for name, versions in declarations:
        routes = sorted(set().union(*(contexts[version] for version in versions)))
        index_coverage.append({"index": name, "index_sha256": inputs.hashes[name],
            "declared_originals": len(versions),
            "with_record_context": sum(bool(contexts[version]) for version in versions),
            "without_record_context": sum(not contexts[version] for version in versions),
            "record_routes": routes,
            "semantic_coverage": "Existing source-version citation contexts only; not a complete result census. Uncited originals require semantic reconciliation, not a new theorem per file."})
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
                "evidence_windows": len(documents), "text_windows": sum(d["source"].get("lines") is not None for d in documents),
                "metadata_documents": sum(d["source"].get("lines") is None for d in documents), "selected_source_indexes": len(index_paths),
                "source_index_routes": index_coverage,
                "exclusion_mentions": dict(Counter(x for v in artifacts.values() for x in v["exclusions"])),
                "denominator": "Distinct (public path, SHA256, read_path) keys in all nested current-record citations (including current/historical reviews, corrections and relationships), version-bound transfer evidence, and explicit selected-public-source-index entries. Citation roles stay separate; aliases may share bytes. Counts are not distinct discoveries.",
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
    candidates, seen = [], set()
    for index in ranked:
        artifact = docs[index]["artifact_id"]
        if artifact in seen:
            continue
        seen.add(artifact)
        candidates.append(index)
        if len(candidates) == 80:
            break
    ranked = candidates
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
                        "citation_roles": artifact.get("citation_roles", []),
                        "next": ["source", doc["id"]] if doc["source"].get("lines") else {"original_public_path": doc["source"]["path"]},
                        "exclusions": artifact["exclusions"], "scope": artifact["scope"]})
        if len(results) == limit:
            break
    return {"query": query, "method": method, "results": results,
            "scope": "Evidence discovery, not scientific acceptance. Follow exact E-id source and cited_by packets; uncited originals require a scientific review before reuse as premises."}
