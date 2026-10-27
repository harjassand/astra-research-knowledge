"""Source-informed retrieval comparison; never executes the preserved archive."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from knowledge.model import Inputs
from knowledge.retrieve import Library

BASE = Path(__file__).resolve().parent


def main():
    specification = json.loads((BASE / "RETRIEVAL_PROBLEMS.json").read_bytes())
    library = Library(validate=False)
    inputs = Inputs(ROOT)
    results = []
    for case in specification["cases"]:
        unit = library.resolve(case["premise_unit"])
        rows = []
        for method in ("lexical", "structured", "content"):
            hits = library.search(case["query"], method=method, limit=5)["results"]
            ranks = []
            for rank, hit in enumerate(hits, 1):
                record = library.resolve(hit["id"])
                if hit["id"] == unit["id"] or set(record["parents"] + [record["id"]]) & set(unit["parents"]):
                    ranks.append(rank)
            rows.append(dict(method=method, ids=[h["id"] for h in hits],
                             parent_or_unit_rank=min(ranks) if ranks else None,
                             exact_unit_rank=next((i for i, h in enumerate(hits, 1) if h["id"] == unit["id"]), None)))
        matches = []
        for reference in unit["evidence"]:
            _, passage = inputs.source(reference)
            if case["proof_contains"].casefold() in passage.casefold():
                matches.append(dict(source=reference, supporting_passage=passage))
        if not matches:
            raise ValueError("Wrong/missing proof branch for " + case["id"])
        results.append(dict(case=case, rankings=rows, read_support=matches,
                            route_scope="Targeted unit source read after candidate retrieval; a parent hit is navigation, not the exact intermediate premise. No automatic correctness judgment from rank."))
    manifest = json.loads((ROOT / "knowledge/current/manifest.json").read_bytes())
    output = dict(exposure=specification["exposure"], input_version=manifest["input_version"],
                  methods={"lexical": "Full-card lexical BM25 baseline", "structured": "Existing fields/concept/source-window ranking with lexical safety", "content": "Existing full scientific-content lane"}, results=results)
    (BASE / "RETRIEVAL_RESULTS.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    for row in results:
        print(row["case"]["id"], [(r["method"], r["parent_or_unit_rank"], r["exact_unit_rank"]) for r in row["rankings"]])


if __name__ == "__main__":
    main()
