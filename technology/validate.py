#!/usr/bin/env python3
"""Validate public technology records; never execute experiments or promote claims."""
import argparse
import csv
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from technology.contracts import history, immutable, links, load, local, need, public_record, refs, shape, stored_path
from frontier.retrieve import route_id

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path(__file__).with_name("schema.json")
STAGES = ("opportunity", "mechanism", "model", "simulation", "experiment", "prototype", "scaling")
KINDS = {"mechanism": {"hypothesis", "theoretical_derivation"},
         "model": {"theoretical_derivation"}, "simulation": {"simulation", "reproduced_simulation"},
         "experiment": {"experimental_measurement"}, "prototype": {"validated_prototype"},
         "scaling": {"demonstrated_system"}}
INDEPENDENT = {"reproduced_simulation", "independent_computational_test", "experimental_measurement",
               "validated_prototype", "demonstrated_system"}


def routes(root):
    with (root / "technology/routes.tsv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    need(len({r["role"] for r in rows}) == len(rows), "duplicate routing role")
    for row in rows:
        local(root, row["entry_point"])
        need(row["acceptance"] and row["continuity"], "incomplete routing contract")
    return {r["role"]: r for r in rows}


def validate(record, root=ROOT):
    shape(record, load(SCHEMA_PATH))
    history(root, record, "technology/records" if not record["fixture"] else "technology/fixtures")
    references = refs(root, record["refs"])
    for assessment in record["assessment"].values():
        links(assessment["basis_ref_ids"], references, "assessment")
    links(record["capability"]["baseline_ref_ids"], references, "baseline")
    experiments = {e["id"]: e for e in record.get("experiments", [])}
    need(len(experiments) == len(record.get("experiments", [])), "duplicate experiment ID")
    evidence = {}
    for item in record.get("evidence", []):
        need(item["id"] not in evidence, "duplicate evidence ID")
        evidence[item["id"]] = item
        links(item["ref_ids"], references, "evidence", True)
        independence = item["independence"]
        links(independence["basis_ref_ids"], references, "independence")
        if independence["attested"] is True:
            need(independence["basis_ref_ids"] and independence["relationship"], "independence needs a receipt and relationship")
        if item["kind"] in INDEPENDENT:
            need(independence["attested"] is True, "independent evidence requires an attestation; never inferred from worker count")
        if item["kind"] not in ("hypothesis", "theoretical_derivation"):
            need(item["experiment_id"] in experiments, "execution needs its decisive experiment contract")
            need(item["subject_ref_ids"], "execution needs exact output/data references")
        elif item["experiment_id"] is not None:
            need(item["experiment_id"] in experiments, "unknown experiment ID")
        links(item["subject_ref_ids"], references, "tested subject")
        need(set(item["subject_ref_ids"]) <= set(item["ref_ids"]), "tested subject must be among evidence references")
        if item["kind"] == "experimental_measurement":
            need(item["environment"] == "physical" and experiments[item["experiment_id"]]["kind"] == "laboratory",
                 "simulation cannot become a physical measurement")
        if item["kind"] in ("simulation", "reproduced_simulation"):
            need(experiments[item["experiment_id"]]["kind"] == "simulation", "simulation evidence requires its simulation plan")
        if item["kind"] == "independent_computational_test":
            need(item["environment"] == "software" and experiments[item["experiment_id"]]["kind"] == "software_benchmark",
                 "computational validation requires a software benchmark contract")
        if item["kind"] in INDEPENDENT - {"reproduced_simulation"}:
            need(item.get("observations"), "measurement/benchmark/prototype/system evidence requires quantities, units and uncertainty")
        if item["kind"] == "validated_prototype":
            permitted = {"software_benchmark", "system"} if item["environment"] == "software" else {"laboratory", "system"}
            need(experiments[item["experiment_id"]]["kind"] in permitted, "prototype evidence requires a compatible validation plan")
        if item["kind"] == "demonstrated_system":
            need(experiments[item["experiment_id"]]["kind"] == "system", "system evidence requires a system demonstration plan")
    gates = {}
    for gate in record.get("gates", []):
        need(gate["stage"] not in gates, "duplicate stage gate")
        gates[gate["stage"]] = gate
        links(gate["evidence_ids"], evidence, "gate")
        if gate["decision"] == "passed":
            need(STAGES.index(gate["stage"]) <= STAGES.index(record["stage"]), "passed gate exceeds completed stage")
            acceptable = KINDS[gate["stage"]]
            if gate["stage"] == "experiment" and record["domain"] == "software":
                acceptable = {"independent_computational_test"}
            eligible = [evidence[x] for x in gate["evidence_ids"] if evidence[x]["result"] == "passed"
                        and evidence[x]["kind"] in acceptable]
            need(eligible, "passed gate lacks the required evidence kind/result: " + gate["stage"])
            if gate["stage"] in ("prototype", "scaling"):
                need(any(e["environment"] == ("software" if record["domain"] == "software" else "physical")
                         for e in eligible), "physical prototype/system cannot be supported by software evidence")
    rank = STAGES.index(record["stage"])
    for stage in STAGES[1:rank + 1]:
        need(stage in gates and gates[stage]["decision"] == "passed", "unmet prior stage: " + stage)
    if rank >= 2:
        need("contract" in record, "model stage requires a scientific/engineering contract")
    if rank >= 3:
        need(experiments, "simulation stage requires a decisive test contract")
    if rank >= 6:
        need("scaling" in record, "scaling stage requires a scaling assessment")
    role_map = routes(root)
    status_rows = [json.loads(row) for row in (root / "frontier/CURRENT_CLAIM_STATUS.jsonl").read_text().splitlines() if row.strip()]
    for path in sorted((root / "frontier/CURRENT_CLAIM_STATUS.d").glob("*.jsonl")):
        status_rows.extend(json.loads(row) for row in path.read_text().splitlines() if row.strip())
    cards = {r["card_id"] for r in status_rows}
    cards |= {route_id(r) for r in cards}
    proof_gates = {json.loads(row)["gate_id"] for row in (root / "frontier/OPEN_PROOF_GATES.jsonl").read_text().splitlines() if row.strip()}
    bridge_ids = set()
    for bridge in record.get("bridges", []):
        need(bridge["id"] not in bridge_ids, "duplicate bridge ID")
        bridge_ids.add(bridge["id"])
        links(bridge["source_card_ids"], cards, "source cards")
        links(bridge["source_gate_ids"], proof_gates, "source proof gates")
        links(bridge["source_ref_ids"], references, "bridge source", True)
        links(bridge["proof_ref_ids"], references, "bridge proof")
        links(bridge["validation_experiment_ids"], experiments, "bridge validation", True)
        if bridge["state"] in ("PROVEN LOGICAL DEPENDENCY", "ESTABLISHED COMPATIBLE INTERFACE", "REFUTED TRANSFER"):
            need(bridge["proof_ref_ids"], "established/refuted transfer requires scoped proof references")
        if bridge["state"] in ("CANDIDATE CONNECTION", "INCOMPATIBLE ASSUMPTIONS"):
            need(bridge["missing_operations"], "candidate/incompatible transfer requires exact missing operations")
    handoff_ids = set()
    for handoff in record.get("handoffs", []):
        need(handoff["id"] not in handoff_ids, "duplicate handoff ID")
        handoff_ids.add(handoff["id"])
        need(handoff["destination_role"] in role_map, "unknown destination role")
        links(handoff["source_ref_ids"], references, "handoff source", True)
        links(handoff["acceptance_experiment_ids"], experiments, "handoff acceptance", True)
        if handoff["checkpoint_path"] is not None:
            need(handoff["checkpoint_path"].startswith("state/checkpoints/"), "handoff checkpoint must use continuity store")
            local(root, handoff["checkpoint_path"])
    for failure in record.get("failures", []):
        links(failure["ref_ids"], references, "failure", True)
    if record["disposition"] == "abandoned":
        need(record.get("failures"), "abandonment needs a scoped, evidenced failure")
    return {"id": record["id"], "version": record["version"], "stage": record["stage"],
            "fixture": record["fixture"], "evidence_items": len(evidence), "scientific_truth_checked": False}


def paths(root, fixtures=False):
    result = sorted((root / "technology/records").rglob("*.json"))
    if fixtures:
        result += sorted((root / "technology/fixtures").glob("*/record.json"))
    return result


def route(root=ROOT, card=None, role=None, fixtures=False, limit=5):
    need(type(limit) is int and limit >= 0, "route limit must be non-negative")
    role_map = routes(root)
    if role:
        need(role in role_map, "unknown role")
    latest = {}
    for path in paths(root, fixtures):
        record = public_record(root, path)
        validate(record, root)
        stored_path(path, root, record, "technology/records")
        if record["id"] not in latest or record["version"] > latest[record["id"]][0]["version"]:
            latest[record["id"]] = (record, path)
    output = []
    for record, path in latest.values():
        participating = {c for b in record.get("bridges", []) for c in b["source_card_ids"]}
        participating |= {route_id(c) for c in participating}
        if card and card not in participating and route_id(card) not in participating:
            continue
        if role and not any(h["destination_role"] == role for h in record.get("handoffs", [])):
            continue
        output.append({"id": record["id"], "version": record["version"], "fixture": record["fixture"],
                       "path": path.relative_to(root).as_posix(), "stage": record["stage"],
                       "next_obligation": record["next_obligation"]})
    output.sort(key=lambda row: row["id"])
    return {"routes": output[:limit], "matching_records": len(output),
            "role": role_map.get(role), "navigation_is_not_applicability": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("files", nargs="*", type=Path)
    check.add_argument("--include-fixtures", action="store_true")
    check.add_argument("--immutable-base")
    find = sub.add_parser("route")
    find.add_argument("--card")
    find.add_argument("--role")
    find.add_argument("--include-fixtures", action="store_true")
    find.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    try:
        if args.command == "route":
            result = route(card=args.card, role=args.role, fixtures=args.include_fixtures, limit=args.limit)
        else:
            immutable(ROOT, args.immutable_base, [":(glob)technology/records/**/*.json"])
            result = []
            seen = set()
            for path in args.files or paths(ROOT, args.include_fixtures):
                record = public_record(ROOT, path)
                checked = validate(record)
                need((record["id"], record["version"]) not in seen, "duplicate record ID/version")
                seen.add((record["id"], record["version"]))
                stored_path(path, ROOT, record, "technology/records")
                result.append(checked)
            result = {"records": result, "experiments_executed": 0, "scientific_truth_checked": False}
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, KeyError, OSError, UnicodeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
