#!/usr/bin/env python3
"""Reproducible candidate comparison; source correctness needs a written assessment.

Cases live outside implementation fixtures. No ranking parameters are learned
from cases. A family hit is navigation only, never a scientific answer score.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knowledge.model import Inputs, digest, encoded, field_index, flatten, route_id, scientific_text, score_query, tokens
from knowledge.retrieve import Library


def content_index(library):
    inputs, documents = Inputs(library.root), []
    for document in library.documents:
        if document["kind"] == "source_window":
            _, passage = inputs.source(document["evidence"][0])
            body = document["title"] + " " + scientific_text(passage)[0]
        else:
            record = library.records[document["record_id"]]
            body = flatten({key: record.get(key, "") for key in ("title", "statement", "contract", "body", "aliases", "notices")})
        documents.append({"body": body})
    return field_index(documents)


def compare(cases, library):
    started = time.monotonic()
    postings = content_index(library)
    index_seconds = time.monotonic() - started
    results = []
    for case in cases:
        task = "\n".join(x for x in (case["query"], case.get("object", ""), case.get("operation", "")) if x)
        row = dict(case, methods={})
        for method in ("lexical", "content_lexical", "structured", "agent"):
            started = time.monotonic()
            if method == "content_lexical":
                ranked, scores, _ = score_query(postings, {term: 1 for term in tokens(task)})
                items, seen = [], set()
                for index in ranked:
                    doc = library.documents[index]
                    record = library.records[doc["record_id"]]
                    family = (record["parents"] or [record["id"]])[0]
                    if family in seen:
                        continue
                    seen.add(family)
                    items.append({"id": record["id"], "matched_document": doc["id"], "score": scores[index],
                                  "source_match": doc.get("evidence", []) if doc["kind"] == "source_window" else [],
                                  "next": {"packet": ["packet", record["id"]], "source": ["source", doc["id"] if doc["kind"] == "source_window" else record["id"]]}})
                    if len(items) == 5:
                        break
                response = {"results": items}
            elif method == "agent":
                response = library.search(case["query"], method=method, object_text=case.get("object", ""),
                    operation=case.get("operation", ""), available=case.get("available", []), unavailable=case.get("unavailable", []))
            else:
                response = library.search(task, method=method)
            candidates = []
            for item in response["results"]:
                record = library.records[item["id"]]
                family = route_id((record["parents"] or [record["id"]])[0])
                selected = {key: item[key] for key in ("id", "matched_document", "score", "relevance_logit", "ranking_view", "ranking_text_truncated", "source_match", "next", "premise_check") if key in item}
                selected["family"] = family
                candidates.append(selected)
            acceptable = case.get("acceptable_families", [])
            rank = next((i + 1 for i, item in enumerate(candidates) if item["family"] in acceptable), None)
            row["methods"][method] = {"family_hit_rank": rank, "seconds": time.monotonic() - started,
                                      "candidates": candidates, "candidate_records": response.get("candidate_records"),
                                      "ranked_views": response.get("ranked_views")}
        results.append(row)
        print(case["id"], {key: value["family_hit_rank"] for key, value in row["methods"].items()}, flush=True)
    return {"schema": "astra.retrieval-comparison.v1", "input_version": library.manifest["input_version"],
            "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=library.root, text=True).strip(),
            "scope": "Same-owner navigation comparison, five family slots and identical object/operation query text. Available/unavailable facts are inspection inputs, not ranking boosts. A family hit is not source correctness. See written passage-level assessment. No blind/independent or general search superiority claim.",
            "content_index_seconds": index_seconds, "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    case_file = Path(args.cases)
    value = json.loads(case_file.read_bytes())
    result = compare(value["cases"], Library())
    result["case_file_sha256"] = digest(case_file.read_bytes())
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded(result))


if __name__ == "__main__":
    main()
