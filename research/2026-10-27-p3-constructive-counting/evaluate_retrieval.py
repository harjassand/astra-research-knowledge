#!/usr/bin/env python3
"""Replay fixed source-informed intake probes; never tune the search index."""
import argparse
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from knowledge.retrieve import Library


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--methods", nargs="+", default=["content", "structured"])
    args = parser.parse_args()
    fixture = json.loads((HERE / "RETRIEVAL_EVALUATION.json").read_bytes())
    library = Library(ROOT)
    results = []
    for old in fixture["results"]:
        row = {key: old[key] for key in ("id", "query", "target_family")}
        row["methods"] = {}
        for method in args.methods:
            start = time.monotonic()
            response = library.search(row["query"], method=method)
            families = [(library.records[item["id"]]["parents"] or [item["id"]])[0].split("-")[0]
                        for item in response["results"]]
            row["methods"][method] = {
                "seconds": time.monotonic() - start, "families": families,
                "target_in_top5": row["target_family"] in families if row["target_family"] else None,
                "response": response,
            }
        results.append(row)
        print(row["id"], {method: value["families"] for method, value in row["methods"].items()}, flush=True)
    value = {"scope": fixture["scope"], "input_version": library.manifest["input_version"], "results": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")


if __name__ == "__main__":
    main()
