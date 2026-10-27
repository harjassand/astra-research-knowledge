#!/usr/bin/env python3
"""Current public scientific search, bounded packets, source reading and bridges."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knowledge.build import check
from knowledge.model import (ROOT, Inputs, digest, encoded, query_terms,
                             route_id, scientific_text, score_query, tokens)


class Library:
    def __init__(self, root=ROOT, validate=True):
        self.root = Path(root)
        self.manifest = check(self.root, regenerate=False) if validate else {}
        self.records = {row["id"]: row for row in self.rows("records.jsonl")}
        self.documents = self.rows("documents.jsonl")
        self.catalog = json.loads((self.root / "knowledge/current/catalog.json").read_bytes())
        self.transfers = json.loads((self.root / "knowledge/current/transfers.json").read_bytes())
        self.operation_frames = {row["id"]: row for row in self.rows("operations.jsonl")}

    def rows(self, name):
        return [json.loads(line) for line in (self.root / "knowledge/current" / name).read_bytes().splitlines() if line.strip()]

    def resolve(self, identifier):
        if identifier in self.records:
            return self.records[identifier]
        selected = [record for record in self.records.values() if route_id(record["id"]) == identifier]
        if len(selected) != 1:
            raise ValueError("Unknown or ambiguous ID: " + identifier)
        return selected[0]

    def search(self, query, limit=5, method="structured", kind=None, **facets):
        if method == "agent":
            from knowledge.agent_search import search
            return search(self, query, limit, kind, **facets)
        if any(facets.values()):
            raise ValueError("Object/operation/premise facets require --method agent; do not silently ignore assumptions")
        if not 1 <= limit <= 50:
            raise ValueError("limit must be in 1..50")
        if method in ("lexical", "content"):
            terms, expansions = {term: 1.0 for term in tokens(query)}, []
        else:
            terms, expansions = query_terms(query, self.catalog["concepts"])
        documents = self.documents
        postings = {}
        folder = method if method in ("lexical", "content") else "postings"
        for shard in sorted({digest(term.encode())[:2] for term in terms}):
            path = self.root / "knowledge/current" / folder / (shard + ".json")
            if path.is_file():
                postings.update(json.loads(path.read_bytes()))
        ranked, scores, matches = score_query(postings, terms)
        results = []
        seen = set()
        for index in ranked:
            document = documents[index]
            record = self.records[document["record_id"]]
            if kind and record["kind"] != kind:
                continue
            group = (record["parents"] or [record["id"]])[0]
            if group in seen:
                continue
            seen.add(group)
            original = set(tokens(query))
            results.append({"id": record["id"], "title": record["title"], "kind": record["kind"],
                "score": round(scores[index], 4), "matched_terms": sorted(matches[index]),
                "original_terms_matched": sorted(matches[index] & original),
                "match_scope": "candidate only; not an applicability verdict",
                "matched_document": document["id"],
                "source_match": document.get("evidence", []) if document.get("kind") == "source_window" else [],
                "statement": record["statement"], "contract": record["contract"],
                "review_overlays": record["review_overlays"], "reported_review": record["review"],
                "notice_count": len(record["notices"]),
                "packet": "knowledge/current/packets/" + route_id(record["id"]) + ".json"})
            if len(results) == limit:
                break
        if method == "structured" and limit > 1:
            safety = self.search(query, limit=1, method="lexical")["results"]
            if safety:
                group = safety[0]["id"]
                selected_groups = {(self.records[item["id"]]["parents"] or [item["id"]])[0] for item in results}
                if group not in selected_groups and (not kind or self.records[group]["kind"] == kind):
                    safety[0]["retrieval_lane"] = "full_card_lexical_safety; independent score scale"
                    results = results[:limit - 1] + safety
        return {"query": query, "method": method, "expansions": expansions,
                "scope": "Ranked candidates, not verified answers. Low overlap or absent matches means no supported answer found, not a corpus-wide impossibility.",
                "results": results}

    def packet(self, identifiers, max_bytes=32768):
        packets = []
        for identifier in identifiers:
            record = self.resolve(identifier)
            path = self.root / "knowledge/current/packets" / (route_id(record["id"]) + ".json")
            packets.append(json.loads(path.read_bytes()))
        value = {"packets": packets, "input_version": self.manifest.get("input_version")}
        if len(encoded(value)) > max_bytes:
            raise ValueError("Complete packet exceeds byte budget; choose fewer IDs or explicitly increase --max-bytes. No corrections were truncated.")
        return value

    def source(self, identifier, evidence_index=0, start=None, end=None, max_bytes=32768):
        if identifier.startswith("E-"):
            folder = self.root / "knowledge/current/evidence"
            selected = next((json.loads(line) for line in (folder / "documents.jsonl").read_bytes().splitlines()
                             if json.loads(line)["id"] == identifier), None)
            if selected is None or evidence_index != 0:
                raise ValueError("Unknown evidence window or index")
            ref = selected["source"]
            if ref.get("lines") is None:
                raise ValueError("Metadata-only artifact has no inferred supporting passage; read its original public path: " + ref["path"])
            text, _ = Inputs(self.root).source(ref)
            lower, upper = ref["lines"]
            start, end = lower if start is None else start, upper if end is None else end
            if not lower <= start <= end <= upper:
                raise ValueError("Read must remain within the cited inclusive source range")
            passage = "".join(text.splitlines(keepends=True)[start - 1:end])
            passage, selector = scientific_text(passage)
            artifact = next(json.loads(line) for line in (folder / "artifacts.jsonl").read_bytes().splitlines()
                            if json.loads(line)["id"] == selected["artifact_id"])
            value = {"id": identifier, "source": dict(ref, lines=[start, end]), "text": passage,
                     "text_selection": selector, "artifact": artifact,
                     "notices": [dict(notice, citation_context=record_id) for record_id in artifact["cited_by"]
                                 for notice in self.records[record_id]["notices"]],
                     "scope": "Evidence navigation only; citations and coarchive do not confer acceptance. Inspect cited_by packets and their current conditions/corrections."}
            if len(encoded(value)) > max_bytes:
                raise ValueError("Source read exceeds byte budget; select --start/--end or increase --max-bytes")
            return value
        selected = next((document for document in self.documents if document["id"] == identifier and document["kind"] == "source_window"), None)
        record = self.resolve(selected["record_id"] if selected else identifier)
        references = selected["evidence"] if selected else record["evidence"]
        if not 0 <= evidence_index < len(references):
            raise ValueError("Unknown evidence index")
        reference = references[evidence_index]
        if reference.get("lines") is None:
            raise ValueError("Binary artifact has no supporting text passage; read its original artifact route")
        text, _ = Inputs(self.root).source(reference)
        lower, upper = reference["lines"]
        start = lower if start is None else start
        end = upper if end is None else end
        if not lower <= start <= end <= upper:
            raise ValueError("Read must remain within the cited inclusive source range")
        passage = "".join(text.splitlines(keepends=True)[start - 1:end])
        selected_text, selection = scientific_text(passage)
        if selection.startswith(("JSON /answer/", "notebook cell sources")):
            passage = selected_text
        else:
            selection = "unchanged governing UTF8 passage"
        value = {"id": record["id"], "source": dict(reference, lines=[start, end]), "text": passage,
                 "text_selection": selection,
                 "notices": record["notices"], "review_overlays": record["review_overlays"],
                 "scope": "Exact governing passage or explicitly selected stored text value; raw source/hash remains authoritative. An extraction is not an independent proof."}
        if len(encoded(value)) > max_bytes:
            raise ValueError("Source read exceeds byte budget; select --start/--end or increase --max-bytes")
        return value

    def bridge(self, source, destination):
        source_record, destination_record = self.resolve(source), self.resolve(destination)
        selected = [transfer for transfer in self.transfers if transfer["from"] == source_record["id"]
                    and transfer["to"] == destination_record["id"]]
        if selected:
            return {"from": source_record["id"], "to": destination_record["id"], "transfers": selected,
                    "notices": source_record["notices"] + destination_record["notices"],
                    "scope": "A compatible interface does not certify its source claims or a new composed theorem"}
        return {"from": source_record["id"], "to": destination_record["id"],
                "state": "NO SUPPORTED CONNECTION", "source_contract": source_record["contract"],
                "destination_contract": destination_record["contract"],
                "historical_bridge_candidates": [bridge for bridge in source_record.get("relationships", {}).get("legacy_bridge_candidates", [])
                                                  if destination_record["id"] in bridge["cards"]],
                "remaining_obligations": "No version-bound source-supported bridge is recorded. Similar words, shared fields and matching type names are insufficient.",
                "notices": source_record["notices"] + destination_record["notices"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    search = sub.add_parser("search", help="describe a task, operation, obstruction or analogy")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--method", choices=("agent", "content", "structured", "field", "lexical"), default="structured")
    search.add_argument("--kind")
    search.add_argument("--object", dest="object_text", default="", help="scientific object/representation to rank")
    search.add_argument("--operation", default="", help="capability or reduction to rank")
    search.add_argument("--available", action="append", default=[], help="supplied premise to inspect, never automatically discharged")
    search.add_argument("--unavailable", action="append", default=[], help="unavailable premise to flag, not silently filter away")
    packet = sub.add_parser("packet")
    packet.add_argument("ids", nargs="+")
    packet.add_argument("--max-bytes", type=int, default=32768)
    source = sub.add_parser("source")
    source.add_argument("id")
    source.add_argument("--evidence", type=int, default=0)
    source.add_argument("--start", type=int)
    source.add_argument("--end", type=int)
    source.add_argument("--max-bytes", type=int, default=32768)
    bridge = sub.add_parser("bridge")
    bridge.add_argument("source")
    bridge.add_argument("destination")
    sub.add_parser("coverage")
    evidence = sub.add_parser("evidence", help="search all registered evidence ranges and selected public originals; no acceptance inferred")
    evidence.add_argument("query")
    evidence.add_argument("--method", choices=("field", "agent"), default="field")
    evidence.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    try:
        library = Library()
        if args.command == "search":
            result = library.search(args.query, args.limit, args.method, args.kind,
                                    object_text=args.object_text, operation=args.operation,
                                    available=args.available, unavailable=args.unavailable)
        elif args.command == "packet":
            result = library.packet(args.ids, args.max_bytes)
        elif args.command == "source":
            result = library.source(args.id, args.evidence, args.start, args.end, args.max_bytes)
        elif args.command == "bridge":
            result = library.bridge(args.source, args.destination)
        elif args.command == "evidence":
            from knowledge.evidence import search as search_evidence
            result = search_evidence(library, args.query, args.limit, args.method)
        else:
            result = library.manifest["counts"]
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
        result["checkout_revision"] = revision.stdout.strip() if revision.returncode == 0 else "UNKNOWN"
        if args.command in ("packet", "source"):
            # Bound the actual UTF-8 output, including revision and terminal LF.
            output = encoded(result)
            if len(output) > args.max_bytes:
                raise ValueError("Complete output exceeds byte budget; no history or corrections were truncated.")
            sys.stdout.buffer.write(output)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
