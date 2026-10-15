#!/usr/bin/env python3
"""FW exact preservation, draft and root-owned-record checks; no science inference."""
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
from fw_common import INTAKE_ID, PREFIX, check_ref, digest, excluded_media, local, need, references, verify_incoming, verify_selection
from protected_baseline import check_baseline

INHERITED = {
    "state/checkpoints/worker-conditional-copy-hierarchy/2026-10-11-conditional-copy-hierarchy.json": "6b720c2bea3cfaabc050da53cdb16e46d981e4b78ef05554425e53de4361c2e5",
    "state/checkpoints/worker-mixed-state-classicalization/2026-10-11-mixed-state-classicalization.json": "41dc953fe161f2b01e885987242c8f26cc61fcf3845dd9e99f30ad6d2f3f69bd",
    "state/checkpoints/worker-weighted-union-uniformization/2026-10-11-weighted-union-uniformization.json": "a88dd1f5255b131af712c67f591df897ea2f9867b3ba3ea1e3dac8d5975b371a",
}


def load(root, name):
    return json.loads(local(root, name).read_bytes())


def rows(root, name):
    return [json.loads(x) for x in local(root, name).read_text().splitlines() if x.strip()]


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def one(items, key, identifier):
    found = [x for x in items if x.get(key) == identifier]
    need(len(found) == 1, "Missing/duplicate owned identifier: " + identifier)
    return found[0]


def package_paths(root):
    packet = local(root, PREFIX + "package")
    for path in packet.rglob("*"):
        need(not path.is_symlink(), "Package symlink is forbidden: " + str(path))
    return {str(p.relative_to(root)) for p in packet.rglob("*") if p.is_file()}


def preparation_state(root):
    paths = sorted(local(root, PREFIX).glob("PREPARATION_STATE.v[0-9][0-9][0-9][0-9].json"))
    previous = None
    latest = None
    for number, path in enumerate(paths, 1):
        raw = path.read_bytes()
        state = json.loads(raw)
        need(state.get("schema") == "astra.fw-preparation-state.v1" and state.get("preparation_version") == number,
             "Preparation state version/schema mismatch")
        need(state.get("previous_preparation_state") == previous, "Preparation state history changed")
        for ref in references(state):
            check_ref(root, ref)
        previous = {"path": str(path.relative_to(root)), "sha256": digest(raw)}
        latest = state
    return latest


def validate(root, *, phase="prepared", base=None, freeze_path=None, check_remote=False, check_global=False):
    root = Path(root).resolve()
    incoming = verify_incoming(root)
    excluded_media(root)
    parsed = []
    for path in sorted(local(root, PREFIX).glob("*.py")):
        ast.parse(path.read_text(), filename=str(path))
        parsed.append(str(path.relative_to(root)))
    state = preparation_state(root)
    curation = load(root, PREFIX + "CURATION_INPUT.json") if phase == "integrated" else None
    draft_path = (curation.get("checkpoint_draft_path") if curation else None) or (state["checkpoint_draft"]["path"] if state else PREFIX + "CHECKPOINT_RECORD.preservation.v0001.json")
    draft = load(root, draft_path)
    publisher = module(root / "state/publish_checkpoint.py", "fw_individual_checkpoint")
    publisher.validate_record(draft, root)
    need(draft["branch_id"] == "worker-fw-moving-heat-observable", "Unexpected checkpoint draft branch")
    need(not (root / "state/checkpoints" / draft["branch_id"] / (draft["checkpoint_id"] + ".json")).exists(), "Draft unexpectedly present in canonical checkpoint tree")
    for ref in draft["evidence_refs"]:
        check_ref(root, ref)
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
    base = base or (curation["base_revision"] if curation else draft["base_revision"])
    need(draft["base_revision"] == base, "Checkpoint draft/reconciled base mismatch")
    result = {"schema": "astra.fw-scoped-validation.v1", "status": "SCOPED_PASS", "phase": phase,
              "intake_id": INTAKE_ID, "original_files": incoming["original_count"], "original_bytes": incoming["original_bytes"],
              "extracted_members": incoming["extracted_member_count"], "all_source_files": incoming["source_count"],
              "all_source_bytes": incoming["total_bytes"], "original_acquisition_scope": incoming["original_acquisition_scope"],
              "parsed_python_files": parsed, "individual_checkpoint_draft": "PASS; shape/references only",
              "canonical_checkpoint_publication": "NOT_PERFORMED", "inherited_schema_failure_results": inherited,
              "global_checkpoint_validation": "NOT_RUN", "scientific_truth_checked": False,
              "history": check_baseline(root, base, phase="prepared" if phase == "prepared" else "integrated", check_remote=check_remote),
              "scope": "Exact preservation, historical append-only boundaries, reference linkage and software integrity only. No mathematical correctness, priority, physical or practical certification."}
    source_paths = {x["path"] for x in incoming["files"]} | {PREFIX + "package/SOURCE_MANIFEST.json"}
    if phase != "integrated":
        need(not local(root, PREFIX + "INTEGRATION_GENERATOR_RECEIPT.json").exists(), "Integrated packet requires --phase integrated")
        template_path = state["curation_template"]["path"] if state else PREFIX + "CURATION_INPUT.template.json"
        template = load(root, template_path)
        need(template["base_revision"] == base, "Preparation template/current base mismatch")
        need(template["curation_status"] == "DRAFT_PENDING_ROOT_ADJUDICATION" and template["curated_by"] is None,
             "Preparation template curation status changed")
        need(all(not template[key] for key in ["sources", "evidence", "cards", "reserved_routes", "notices", "bridges", "gates"]),
             "Preparation template must leave scientific curation empty")
        result["live_authority_application"] = "NOT_PERFORMED"
        result["preparation_state"] = state
        if phase == "prepared":
            need(package_paths(root) == source_paths, "Unselected research entered source-only preparation packet")
            result["selected_research_freeze"] = "PENDING_ROOT_SELECTION; no worker results copied"
        else:
            need(freeze_path, "--phase preserved requires an exact --freeze-path")
            raw = local(root, freeze_path).read_bytes()
            frozen = verify_selection(root, {"path": freeze_path, "sha256": digest(raw)}, expected_base=base)
            derived = load(root, freeze_path.replace("SELECTED_FREEZE", "DERIVED_MANIFEST"))
            need(derived["schema"] == "astra.fw-derived-manifest.v1" and derived["base_revision"] == frozen["base_revision"]
                 and derived["files"] == frozen["files"] and derived["total_files"] == frozen["total_files"]
                 and derived["total_bytes"] == frozen["total_bytes"]
                 and derived["source_freeze"] == {"path": freeze_path, "sha256": digest(raw)}, "Derived manifest differs from exact frozen selection")
            result["selected_research_freeze"] = {"path": freeze_path, "sha256": digest(raw), "files": len(frozen["files"])}
    else:
        curation_raw = local(root, PREFIX + "CURATION_INPUT.json").read_bytes()
        receipt = load(root, PREFIX + "INTEGRATION_GENERATOR_RECEIPT.json")
        need(curation["curation_status"] == "root_final" and curation["curated_by"] == "root", "Scientific curation is not root-final")
        need(base == curation["base_revision"] == receipt["base_revision"] == draft["base_revision"], "Reconciled curation/draft/base mismatch")
        need(receipt["schema"] == "astra.fw-generator-receipt.v1" and receipt["intake_id"] == INTAKE_ID, "Generator receipt scope mismatch")
        path = local(root, PREFIX + "build_integration.py")
        need(receipt["generator_sha256"] == digest(path.read_bytes()) and receipt["curation_input_sha256"] == digest(curation_raw), "Generator/input receipt hash mismatch")
        generator = module(path, "fw_final_curation_reconstruction")
        need(generator.build_plan(root, curation, digest(curation_raw)).summary()["changed_file_count"] == 0, "Finalized curation is not idempotent")
        for name, wanted in receipt["owned_artifacts"].items():
            need(digest(local(root, name).read_bytes()) == wanted, "Generated owned artifact changed: " + name)
        frozen = verify_selection(root, curation.get("selected_freeze"), expected_base=base)
        derived = load(root, curation["selected_freeze"]["path"].replace("SELECTED_FREEZE", "DERIVED_MANIFEST"))
        need(derived["schema"] == "astra.fw-derived-manifest.v1" and derived["base_revision"] == base
             and derived["source_freeze"] == curation["selected_freeze"] and derived["files"] == frozen["files"], "Derived manifest differs from exact root freeze")
        derived_paths = {x["path"] for x in derived["files"]}
        need(derived["total_files"] == len(derived_paths) and derived["total_bytes"] == sum(x["bytes"] for x in derived["files"]), "Derived inventory totals mismatch")
        claims, statuses = rows(root, "indexes/claims.jsonl"), rows(root, "frontier/CURRENT_CLAIM_STATUS.jsonl")
        catalog = load(root, "indexes/agent_catalog.json")["claims"]
        claim_map = load(root, PREFIX + "CLAIMS.json")
        ids = set(receipt["cards"])
        need(ids == {x["id"] for x in claim_map["claims"]}, "Owned claim map mismatch")
        need({x.split("-")[0] for x in ids} == set(curation["reserved_routes"]) == set(receipt["reserved_routes"]), "Exact root-reserved route mismatch")
        for cid in ids:
            claim, status, entry = one(claims, "id", cid), one(statuses, "card_id", cid), one(catalog, "id", cid)
            need(claim["status"] == status["claim_status"] == entry["status"] == "source_derived_unreviewed", "Scientific status promotion")
            need(all(status["validation"][k] == "UNKNOWN" for k in ["external_correctness", "historical_priority", "physical_capability", "formal_verification", "empirical_confirmation"]), "Scientific validation promotion")
            need(status == load(root, "frontier/cards/" + cid + ".json"), "Current status/sidecar disagreement")
            need(digest(local(root, status["card_path"]).read_bytes()) == status["card_sha256"] == entry["card_sha256"], "Raw card hash mismatch")
            for ref in references(status):
                check_ref(root, ref)
        gates = rows(root, "frontier/OPEN_PROOF_GATES.jsonl")
        for gid in receipt["gate_ids"]:
            gate = one(gates, "gate_id", gid)
            need(gate == load(root, "frontier/gates/" + gid + ".json") and gate["status"] == "open" and not gate["completion_evidence"], "Owned gate changed/promoted")
            for ref in references(gate):
                check_ref(root, ref)
        notices = rows(root, "agent/SEMANTIC_NOTICES.jsonl")
        scoped_notices = load(root, PREFIX + "SCOPED_NOTICES.json")
        need({x["notice_id"] for x in scoped_notices} == set(receipt["notice_ids"]), "Owned notice inventory mismatch")
        for notice in scoped_notices:
            need(one(notices, "notice_id", notice["notice_id"]) == notice, "Owned notice differs from registry")
        indexed = load(root, PREFIX + "INDEXED_SOURCES.json")["files"]
        metadata = rows(root, "indexes/source_metadata.jsonl")
        need({x["source_id"] for x in indexed} == set(receipt["source_ids"]), "Owned indexed-source inventory mismatch")
        for source in indexed:
            need(source["path"] in source_paths | derived_paths and one(metadata, "source_id", source["source_id"]) == source, "Indexed source is not pinned source/frozen research")
        bridges = load(root, PREFIX + "BRIDGES.json")["bridges"]
        need({x["id"] for x in bridges} == set(receipt["bridge_ids"]), "Owned bridge inventory mismatch")
        for bridge in bridges:
            need(bridge == load(root, "mechanisms/bridges/" + bridge["id"] + ".json"), "Owned bridge sidecar changed")
        for item in list(curation["evidence"].values()) + bridges + scoped_notices:
            for ref in references(item):
                check_ref(root, ref)
        result.update({"cards": len(ids), "open_gates": len(receipt["gate_ids"]), "indexed_sources": len(indexed),
                       "selected_derived_files": len(derived_paths), "curation_idempotent": True,
                       "live_authority_application": "ROOT_FINAL_RECORDS_CHECKED; no writes by this validator"})
    if check_global:
        argv = [sys.executable, "-B", "state/publish_checkpoint.py", "validate", "--immutable-base", base]
        process = subprocess.run(argv, cwd=root, capture_output=True, text=True)
        need(process.returncode != 0 and "unsupported checkpoint schema" in process.stderr, "Global checkpoint outcome changed; inspect before relying on inherited-failure boundary")
        result["global_checkpoint_validation"] = {"argv": argv, "exit_code": process.returncode,
            "stdout": process.stdout, "stderr": process.stderr, "status": "FAIL: inherited schemas preserved; individual draft only"}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase", choices=["prepared", "preserved", "integrated"], default="prepared")
    parser.add_argument("--base-revision")
    parser.add_argument("--freeze-path")
    parser.add_argument("--check-remote", action="store_true", help="Read-only remote main freshness check")
    parser.add_argument("--check-global", action="store_true", help="Read-only reproduction of inherited global schema failure")
    args = parser.parse_args()
    print(json.dumps(validate(args.repo, phase=args.phase, base=args.base_revision, freeze_path=args.freeze_path,
                              check_remote=args.check_remote, check_global=args.check_global), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print("FW scoped validation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
