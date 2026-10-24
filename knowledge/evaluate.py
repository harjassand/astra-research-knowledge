#!/usr/bin/env python3
"""Retain an exposed, source-informed retrieval comparison; not a blind invention trial."""
import argparse
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knowledge.model import (ROOT, Inputs, digest, encoded, field_index, flatten,
                             route_id, scientific_text, score_query, tokens)
from knowledge.retrieve import Library


def evaluate(cases, library):
    inputs = Inputs(library.root)
    lexical_documents = []
    for document in library.documents:
        if document["kind"] == "source_window":
            _, passage = inputs.source(document["evidence"][0])
            passage, _ = scientific_text(passage)
            body = document["title"] + " " + passage
        else:
            record = library.records[document["record_id"]]
            body = flatten({key: record.get(key, "") for key in ("title", "statement", "contract", "body", "aliases", "notices")})
        lexical_documents.append({"body": body})
    content_postings = field_index(lexical_documents)
    results = []
    for case in cases:
        row = dict(case)
        row["methods"] = {}
        for method in ("lexical", "content_lexical", "structured"):
            if method == "content_lexical":
                ranked, scores, _ = score_query(content_postings, {term: 1 for term in tokens(case["query"])})
                selected, seen = [], set()
                for index in ranked:
                    document = library.documents[index]
                    record = library.records[document["record_id"]]
                    group = (record["parents"] or [record["id"]])[0]
                    if group in seen:
                        continue
                    seen.add(group)
                    selected.append({"id": record["id"], "matched_document": document["id"], "score": scores[index],
                                     "source_match": document.get("evidence", []) if document["kind"] == "source_window" else []})
                    if len(selected) == 5:
                        break
                response = {"results": selected, "expansions": []}
            else:
                response = library.search(case["query"], limit=5, method=method)
            candidates = []
            hit_rank = None
            for rank, item in enumerate(response["results"], 1):
                record = library.resolve(item["id"])
                parents = record["parents"] or [record["id"]]
                matches = any(route_id(parent) in case["parents"] for parent in parents)
                if matches and hit_rank is None:
                    hit_rank = rank
                candidates.append({"id": item["id"], "matched_document": item["matched_document"],
                                   "score": item["score"], "expected_parent_hit": matches,
                                   "source_match": item["source_match"]})
            row["methods"][method] = {"hit_rank": hit_rank, "candidates": candidates,
                                       "expansions": response["expansions"]}
        if case.get("unit"):
            record = library.resolve(case["unit"])
            passage = library.source(record["id"], max_bytes=1048576)
            row["support_route"] = {"unit": record["id"], "source": passage["source"],
                                    "read_bytes": len(passage["text"].encode()),
                                    "conditions": record["contract"]["assumptions"],
                                    "verification_scope": "Exact route read and quote checked; semantic scientific assessment is in the written research-use review, not inferred from a hash."}
        results.append(row)
    supported = [row for row in results if row["parents"]]
    summary = {method: {"top1_parent_hits": sum(row["methods"][method]["hit_rank"] == 1 for row in supported),
                        "top5_parent_hits": sum(row["methods"][method]["hit_rank"] is not None for row in supported),
                        "supported_case_denominator": len(supported)} for method in ("lexical", "content_lexical", "structured")}
    return {"scope": "Same-owner source-informed exposed evaluation, not held-out, blind, independent or a measured invention-gain experiment. Both methods may use the same packets/sources and five candidate slots. A parent hit is navigation, not a correct scientific answer.",
            "input_version": library.manifest["input_version"], "summary": summary,
            "unsupported_case_count": len(results) - len(supported), "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    path = Path(args.cases)
    value = json.loads(path.read_bytes())
    cases = value if isinstance(value, list) else value["cases"]
    result = evaluate(cases, Library())
    result["case_file_sha256"] = digest(path.read_bytes())
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded(result))
    print(json.dumps({"summary": result["summary"], "unsupported_cases": result["unsupported_case_count"]}))


if __name__ == "__main__":
    main()
