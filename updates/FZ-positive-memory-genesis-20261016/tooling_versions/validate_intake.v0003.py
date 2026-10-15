#!/usr/bin/env python3
"""FZ source-only scaffolding, individual draft and immutable-history checks."""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fz_common import INTAKE_ID, PREFIX, NAMESPACES, check_ref, digest, local, need, verify_incoming, verify_selection
from protected_baseline import check_baseline

INHERITED = {
    "state/checkpoints/worker-conditional-copy-hierarchy/2026-10-11-conditional-copy-hierarchy.json": "6b720c2bea3cfaabc050da53cdb16e46d981e4b78ef05554425e53de4361c2e5",
    "state/checkpoints/worker-mixed-state-classicalization/2026-10-11-mixed-state-classicalization.json": "41dc953fe161f2b01e885987242c8f26cc61fcf3845dd9e99f30ad6d2f3f69bd",
    "state/checkpoints/worker-weighted-union-uniformization/2026-10-11-weighted-union-uniformization.json": "a88dd1f5255b131af712c67f591df897ea2f9867b3ba3ea1e3dac8d5975b371a",
}


def load(root, name):
    return json.loads(local(root, name).read_bytes())


def rows(root, name):
    return [json.loads(line) for line in local(root, name).read_text().splitlines() if line.strip()]


def one(items, key, identifier):
    found = [item for item in items if item.get(key) == identifier]
    need(len(found) == 1, "Missing/duplicate owned identifier: " + identifier)
    return found[0]


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def preparation_state(root):
    paths = sorted(local(root, PREFIX).glob("PREPARATION_STATE.v[0-9][0-9][0-9][0-9].json"))
    need(paths, "FZ preparation state is missing")
    previous, latest = None, None
    for number, path in enumerate(paths, 1):
        raw = path.read_bytes()
        state = json.loads(raw)
        need(state.get("schema") == "astra.fz-preparation-state.v1" and state.get("preparation_version") == number,
             "Preparation schema/version mismatch")
        need(state.get("previous_preparation_state") == previous, "Preparation history linkage changed")
        for ref in state["artifact_refs"].values():
            check_ref(root, ref)
        previous = {"path": str(path.relative_to(root)), "sha256": digest(raw)}
        latest = state
    return latest


def validate(root, *, phase="prepared", freeze_path=None, expected_head=None, expected_remote_main=None,
             immutable_base=None, check_remote=False, check_global=False):
    root = Path(root).resolve()
    need(phase in {"prepared", "preserved", "integrated"}, "Unsupported validation phase")
    incoming = verify_incoming(root, source_only=phase == "prepared")
    parsed = []
    for path in sorted(local(root, PREFIX).glob("*.py")):
        ast.parse(path.read_text(), filename=str(path))
        parsed.append(str(path.relative_to(root)))
    state = preparation_state(root)
    need(state.get("scientific_curation") == "PENDING_PARENT_ADJUDICATION"
         and state.get("selected_research") == "NONE_COPIED_OR_FROZEN"
         and state.get("namespaces") == NAMESPACES, "Preparation authority boundary changed")
    refs = state["artifact_refs"]
    finalized = load(root, PREFIX + "CURATION_INPUT.json") if phase == "integrated" else None
    draft_path = (finalized.get("checkpoint_draft_path") if finalized else None) or refs["checkpoint_draft"]["path"]
    draft = load(root, draft_path)
    publisher = module(root / "state/publish_checkpoint.py", "fz_individual_checkpoint")
    publisher.validate_record(draft, root)
    need(draft["branch_id"] == "worker-fz-positive-memory-genesis", "Unexpected draft branch")
    if phase != "integrated":
        need(draft["base_revision"] == state["preparation_base_revision"], "Preservation draft/base mismatch")
    need(not (root / "state/checkpoints" / draft["branch_id"] / (draft["checkpoint_id"] + ".json")).exists(),
         "Preservation draft unexpectedly present in canonical state")
    if phase != "integrated":
        need(draft["latest_substantive_result"]["summary"] is None
             and draft["latest_substantive_result"]["scientific_status"] == "NO_SCIENTIFIC_CLAIM",
             "Preparation draft must not assert a scientific result")
    for ref in draft["evidence_refs"]:
        check_ref(root, ref)
    curation = load(root, refs["curation_template"]["path"])
    need(curation.get("schema") == "astra.fz-curation-input.v1"
         and curation.get("curation_status") == "DRAFT_PENDING_PARENT_ADJUDICATION"
         and curation.get("curated_by") is None and curation.get("scientific_curation_base_revision") is None,
         "Curation template must remain an unadjudicated draft")
    need(all(not curation[key] for key in ("sources", "evidence", "cards", "reserved_routes", "notices", "bridges", "gates", "technology_records", "workflow_records")),
         "Preparation template must leave scientific curation empty")
    selection = load(root, refs["selection_template"]["path"])
    need(selection.get("schema") == "astra.fz-selected-freeze.v1" and selection.get("status") == "DRAFT_NOT_FROZEN"
         and selection.get("selected_by") is None and selection.get("base_revision") is None
         and selection.get("files") == [] and selection.get("total_files") == selection.get("total_bytes") == 0,
         "Selection template must remain empty and unfrozen")
    inherited = []
    for name, wanted in INHERITED.items():
        need(digest(local(root, name).read_bytes()) == wanted, "Inherited unsupported-schema bytes changed: " + name)
        try:
            publisher.validate_record(load(root, name), root)
        except publisher.Invalid as error:
            need(str(error) == "unsupported checkpoint schema", "Inherited failure changed; inspect its scope")
            inherited.append({"path": name, "sha256": wanted, "actual_error": str(error)})
        else:
            raise ValueError("Inherited unsupported schema unexpectedly validates: " + name)
    immutable_base = immutable_base or (finalized.get("base_revision") if finalized else None) or state["immutable_base"]
    history = check_baseline(root, immutable_base=immutable_base,
                             expected_head=expected_head or (finalized.get("expected_branch_head") if finalized else None) or state["expected_current_branch_head"],
                             expected_remote_main=expected_remote_main or (finalized.get("expected_remote_main") if finalized else None) or state["expected_remote_main"],
                             phase="integrated" if phase == "integrated" else "prepared",
                             check_remote=check_remote)
    selected_result = "PENDING_PARENT_SELECTION; no worker results copied"
    integrated_result = None
    if phase == "preserved":
        need(freeze_path, "Preserved validation requires an exact --freeze-path")
        ref = {"path": freeze_path, "sha256": digest(local(root, freeze_path).read_bytes())}
        frozen = verify_selection(root, ref, expected_base=immutable_base)
        selected_result = {**ref, "files": len(frozen["files"])}
    elif phase == "integrated":
        need(finalized.get("curation_status") == "root_final" and finalized.get("curated_by") == "root", "Scientific curation is not root-final")
        receipt = load(root, PREFIX + "INTEGRATION_GENERATOR_RECEIPT.json")
        need(receipt.get("schema") == "astra.fz-generator-receipt.v1" and receipt.get("intake_id") == INTAKE_ID, "Wrong generator receipt scope")
        raw = local(root, PREFIX + "CURATION_INPUT.json").read_bytes()
        generator_path = local(root, PREFIX + "build_integration.py")
        need(receipt["generator_sha256"] == digest(generator_path.read_bytes())
             and receipt["curation_input_sha256"] == digest(raw), "Final generator/input receipt hash mismatch")
        need(receipt["base_revision"] == finalized["base_revision"] == immutable_base, "Reconciled baseline mismatch")
        need(receipt["expected_branch_head"] == finalized["expected_branch_head"]
             and receipt["expected_remote_main"] == finalized["expected_remote_main"], "Expected HEAD/remote receipt mismatch")
        frozen = verify_selection(root, finalized.get("selected_freeze"), expected_base=immutable_base)
        generator = module(generator_path, "fz_final_curation_reconstruction")
        need(generator.build_plan(root, finalized, digest(raw)).summary()["changed_file_count"] == 0, "Finalized curation is not idempotent")
        for name, wanted in receipt["owned_artifacts"].items():
            check_ref(root, {"path": name, "sha256": wanted})
        claims, statuses = rows(root, "indexes/claims.jsonl"), rows(root, "frontier/CURRENT_CLAIM_STATUS.jsonl")
        catalog = load(root, "indexes/agent_catalog.json")["claims"]
        ids = set(receipt["cards"])
        need(ids == {item["id"] for item in load(root, PREFIX + "CLAIMS.json")["claims"]}, "Owned claim inventory mismatch")
        need({item.split("-")[0] for item in ids} == set(finalized["reserved_routes"]) == set(receipt["reserved_routes"]), "Exact root route mismatch")
        for identifier in ids:
            claim, status, entry = one(claims, "id", identifier), one(statuses, "card_id", identifier), one(catalog, "id", identifier)
            need(claim["status"] == status["claim_status"] == entry["status"] == "source_derived_unreviewed", "Scientific status promotion")
            need(all(status["validation"][key] == "UNKNOWN" for key in ("external_correctness", "historical_priority", "physical_capability", "formal_verification", "empirical_confirmation")), "Scientific validation promotion")
            need(status == load(root, "frontier/cards/" + identifier + ".json"), "Owned status sidecar changed")
        gates = rows(root, "frontier/OPEN_PROOF_GATES.jsonl")
        for identifier in receipt["gate_ids"]:
            gate = one(gates, "gate_id", identifier)
            need(gate == load(root, "frontier/gates/" + identifier + ".json") and gate["status"] == "open" and not gate["completion_evidence"], "Owned gate changed/promoted")
        indexed = load(root, PREFIX + "INDEXED_SOURCES.json")["files"]
        metadata = rows(root, "indexes/source_metadata.jsonl")
        allowed = {item["path"] for item in incoming["files"] + frozen["files"]}
        need({item["source_id"] for item in indexed} == set(receipt["source_ids"]), "Owned indexed-source inventory mismatch")
        for item in indexed:
            need(item["path"] in allowed and one(metadata, "source_id", item["source_id"]) == item, "Indexed source is not original/frozen evidence")
        selected_result = {**finalized["selected_freeze"], "files": len(frozen["files"])}
        integrated_result = {"cards": len(ids), "open_gates": len(receipt["gate_ids"]), "indexed_sources": len(indexed), "curation_idempotent": True}
    global_result = "NOT_RUN"
    if check_global:
        argv = [sys.executable, "-B", "state/publish_checkpoint.py", "validate", "--immutable-base", immutable_base]
        result = subprocess.run(argv, cwd=root, capture_output=True, text=True)
        need(result.returncode != 0 and "unsupported checkpoint schema" in result.stderr,
             "Global validation boundary changed; inspect instead of assuming inherited failure")
        global_result = {"argv": argv, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
                         "status": "FAIL: inherited schemas preserved; individual draft only"}
    return {"schema": "astra.fz-scoped-validation.v1", "status": "SCOPED_PASS", "phase": phase, "intake_id": INTAKE_ID,
            "original_files": incoming["original_count"], "original_bytes": incoming["original_bytes"],
            "original_manifest_files": incoming["original_manifest_files"], "original_manifest": incoming["original_manifest"],
            "previous_original_manifest": incoming["previous_original_manifest"],
            "all_preserved_file_count": incoming["all_preserved_file_count"], "all_preserved_bytes": incoming["all_preserved_bytes"],
            "operative_request": incoming["operative_request"], "parsed_python_files": parsed,
            "individual_checkpoint_draft": "PASS; shape and references only; remains outside canonical tree",
            "draft_base_revision": draft["base_revision"],
            "draft_publication_requirement": "Prepare a new version against actual HEAD and current parents before any canonical publication; advancing branch HEAD does not rewrite this preservation draft.",
            "inherited_schema_failure_results": inherited, "global_checkpoint_validation": global_result,
            "scientific_truth_checked": False, "selected_research_freeze": selected_result,
            "integrated_record_check": integrated_result,
            "live_authority_application": "ROOT_FINAL_RECORDS_CHECKED; validator performs no writes" if phase == "integrated" else "NOT_PERFORMED",
            "canonical_checkpoint_publication": "NOT_PERFORMED",
            "history": history, "scope": "Exact byte preservation, empty scaffolding, individual reference validity and FZ-only history boundary; no science, novelty, physical validation or capability certification."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase", choices=["prepared", "preserved", "integrated"], default="prepared")
    parser.add_argument("--freeze-path")
    parser.add_argument("--expected-head")
    parser.add_argument("--expected-remote-main")
    parser.add_argument("--immutable-base")
    parser.add_argument("--check-remote", action="store_true")
    parser.add_argument("--check-global", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(args.repo, phase=args.phase, freeze_path=args.freeze_path,
                              expected_head=args.expected_head, expected_remote_main=args.expected_remote_main,
                              immutable_base=args.immutable_base, check_remote=args.check_remote, check_global=args.check_global), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print("FZ scoped validation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
