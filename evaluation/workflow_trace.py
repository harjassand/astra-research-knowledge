#!/usr/bin/env python3
"""Optional observational traces; does not register a trial or infer prompting gains."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from technology.contracts import history, immutable, links, load, need, public_record, refs, shape, stored_path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path(__file__).with_name("workflows") / "schema.json"


def validate(record, root=ROOT):
    shape(record, load(SCHEMA_PATH))
    history(root, record, "evaluation/workflows/records")
    references = refs(root, record["refs"])
    for values, label in [(record["prompt_ref_ids"], "prompt"), (record["output_ref_ids"], "output"),
                          (record["context"]["context_ref_ids"], "context")]:
        links(values, references, label)
    need(bool(record["prompt_ref_ids"]) == (record["prompt_availability"] == "exact"),
         "exact initiating prompt requires its preserved bytes; unknown is not an empty prompt")
    relation = record["context"]["conversation_relation"]
    if record["mode"] in ("targeted_warm_continuation", "fresh_direction_retained_context"):
        need(relation == "same" and record["context"]["retained_context"], "warm/retained mode requires recorded same-conversation context")
    if record["mode"] == "new_instance":
        need(relation == "new", "new instance requires a new conversation")
    if record["mode"] == "independent_selective_capital":
        need(record["context"]["capital_access"], "selective Capital access must be described")
    need(record["model"]["immutable_version"] not in ("UNKNOWN", "unknown", "latest", "REPLACE"),
         "unavailable immutable model version must be null; mutable labels are not fixed versions")
    if record["status"] == "completed":
        need(record["output_ref_ids"], "completed trace requires exact output bytes")
    resources = record["resources"]
    for key in ("reported_duration_ref_ids", "usage_receipt_ref_ids", "worker_receipt_ref_ids"):
        links(resources[key], references, key)
    if resources["reported_inference_seconds"] is not None:
        need(resources["reported_duration_ref_ids"], "reported inference duration requires its source receipt")
    if any(value is not None for value in resources["usage"].values()):
        need(resources["usage_receipt_ref_ids"], "measured usage requires a receipt; never infer it from reported duration")
    if resources["worker_invocations"] is not None:
        need(resources["worker_receipt_ref_ids"], "worker counts require a receipt")
    workers = resources["usage"]["parallel_workers"]
    if record["mode"] == "source_intensive_multi_agent" and workers is not None:
        need(workers >= 2, "multi-agent mode contradicts recorded worker peak")
    advance = record["advance"]
    links(advance["evidence_ref_ids"], references, "advance evidence")
    if advance["summary"] is not None:
        need(advance["evidence_ref_ids"], "advance narrative requires scoped evidence")
    if advance["verification"] != "unassessed":
        need(advance["evidence_ref_ids"], "verification status requires evidence")
    receipt = advance["verification_receipt"]
    if receipt is not None:
        links(receipt["ref_ids"], references, "verification receipt", True)
        outputs = {references[x]["sha256"] for x in record["output_ref_ids"]}
        need(set(receipt["checked_output_sha256"]) <= outputs, "receipt must bind exact submitted output hashes")
    if advance["verification"] in ("independent_receipt", "experimental_receipt"):
        need(receipt is not None and receipt["independence_attested"] is True,
             "independent/experimental status requires an output-bound independent receipt, not model agreement")
    if record["matched_run_id"] is not None:
        need(not record["fixture"], "fixtures cannot be linked as real matched trials")
        rows = [json.loads(line) for line in (root / "evaluation/MODEL_COMPARISONS.jsonl").read_text().splitlines() if line.strip()]
        matched = [r for r in rows if r.get("kind") == "run_record" and r.get("run_id") == record["matched_run_id"]]
        need(len(matched) == 1, "matched_run_id must refer to a real registered run, not historical navigation")
        output_hashes = {r["sha256"] for r in matched[0]["files"] if r["kind"] == "output"}
        need({references[x]["sha256"] for x in record["output_ref_ids"]} == output_hashes,
             "trace outputs differ from the matched run")
        need(resources["usage"] == matched[0]["usage"], "trace usage differs from the matched run")
        for key, value in record["model"].items():
            if value is not None:
                need(value == matched[0]["actual_model"][key], "trace model differs from the matched run")
        status = {"timed_out": "timeout"}.get(record["status"], record["status"])
        need(status == matched[0]["status"] or record["status"] == "failed" and matched[0]["status"] == "budget_exceeded",
             "trace status differs from the matched run")
    return {"id": record["id"], "version": record["version"], "fixture": record["fixture"],
            "mode": record["mode"], "status": record["status"],
            "all_usage_recorded": all(v is not None for v in resources["usage"].values()),
            "scientific_status": advance["scientific_status"],
            "verification_is_receipt_attestation_only": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "report"))
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--include-fixtures", action="store_true")
    parser.add_argument("--immutable-base")
    args = parser.parse_args()
    try:
        immutable(ROOT, args.immutable_base, [":(glob)evaluation/workflows/records/**/*.json"])
        paths = args.files or sorted((ROOT / "evaluation/workflows/records").rglob("*.json"))
        if args.include_fixtures and not args.files:
            paths += sorted((ROOT / "evaluation/workflows/fixtures").glob("*.json"))
        results, seen = [], set()
        for path in paths:
            record = public_record(ROOT, path)
            checked = validate(record)
            stored_path(path, ROOT, record, "evaluation/workflows/records")
            need((record["id"], record["version"]) not in seen, "duplicate trace ID/version")
            seen.add((record["id"], record["version"]))
            results.append(checked)
        latest = {}
        for row in results:
            if row["id"] not in latest or row["version"] > latest[row["id"]]["version"]:
                latest[row["id"]] = row
        live = [r for r in latest.values() if not r["fixture"]]
        result = {"records": results, "live_latest_trace_count": len(live),
                  "modes": dict(Counter(r["mode"] for r in live)),
                  "cost_incomplete_traces": sum(not r["all_usage_recorded"] for r in live),
                  "comparative_advantage_inferred": False, "models_called": 0, "scientific_truth_checked": False}
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, KeyError, OSError, UnicodeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
