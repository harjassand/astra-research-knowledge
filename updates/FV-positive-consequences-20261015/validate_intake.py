#!/usr/bin/env python3
"""FV preservation and exact-owned-record validation; no scientific certification."""
from __future__ import annotations

import argparse
import ast
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fv_common import INTAKE_ID, PREFIX, PROVENANCE_ROLES, IMMUTABLE_PREFIXES, check_ref, digest, excluded_media, local, need, references, verify_incoming, verify_selection

INHERITED = {
    "state/checkpoints/worker-conditional-copy-hierarchy/2026-10-11-conditional-copy-hierarchy.json": "6b720c2bea3cfaabc050da53cdb16e46d981e4b78ef05554425e53de4361c2e5",
    "state/checkpoints/worker-mixed-state-classicalization/2026-10-11-mixed-state-classicalization.json": "41dc953fe161f2b01e885987242c8f26cc61fcf3845dd9e99f30ad6d2f3f69bd",
    "state/checkpoints/worker-weighted-union-uniformization/2026-10-11-weighted-union-uniformization.json": "a88dd1f5255b131af712c67f591df897ea2f9867b3ba3ea1e3dac8d5975b371a",
}


def load(root, path):
    return json.loads(local(root, path).read_text())


def rows(root, path):
    return [json.loads(x) for x in local(root, path).read_text().splitlines() if x.strip()]


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def one(items, key, identifier):
    found = [x for x in items if x.get(key) == identifier]
    need(len(found) == 1, "Missing/duplicate owned identifier: " + identifier)
    return found[0]


def history(root, base):
    subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", base, "HEAD"], check=True, capture_output=True)
    before_paths = set(git(root, "ls-tree", "-r", "--name-only", base).decode().splitlines())
    changed = git(root, "diff", "--name-only", base).decode().splitlines()
    for name in changed:
        need(not (name in before_paths and name.startswith(IMMUTABLE_PREFIXES)), "Historical immutable artifact changed: " + name)
    for name in ["indexes/claims.jsonl", "indexes/source_metadata.jsonl", "frontier/CURRENT_CLAIM_STATUS.jsonl",
                 "frontier/OPEN_PROOF_GATES.jsonl", "agent/SEMANTIC_NOTICES.jsonl", "web/documents.jsonl", "state/branches.tsv"]:
        need(local(root, name).read_bytes().startswith(git(root, "show", base + ":" + name)), "Historical byte prefix changed: " + name)
    groups = {"indexes/agent_catalog.json": ["claims"], "indexes/agent_graph.json": ["nodes", "edges"],
              "mechanisms/bridge_candidates.json": ["bridges", "rejected_transfers"], "web/catalog.json": [None]}
    for name, fields in groups.items():
        raw = git(root, "show", base + ":" + name)
        before = json.loads(raw)
        current = load(root, name)
        projection = copy.deepcopy(current)
        for field in fields:
            old = before[field] if field else before
            new = current[field] if field else current
            need(new[:len(old)] == old, "Historical array values/order changed: " + name)
            if field:
                projection[field] = new[:len(old)]
            else:
                projection = new[:len(old)]
        need((json.dumps(projection, ensure_ascii=False, indent=2) + "\n").encode() == raw, "Historical JSON keys/format changed: " + name)
    aliases = json.loads(git(root, "show", base + ":indexes/query_aliases.json"))
    need(all(load(root, "indexes/query_aliases.json").get(k) == v for k, v in aliases.items()), "Historical alias changed")
    return {"immutable_existing_paths_unchanged": True, "registry_prefixes_and_historical_arrays_unchanged": True}


def validate(root, phase="skeleton", base=None, check_global=False, freeze_path=None, check_history=False, authorize_git=False):
    need(not (check_global or check_history) or authorize_git, "Git-based checks require separate root authorization")
    root = root.resolve()
    incoming = verify_incoming(root)
    excluded_media(root)
    parsed = []
    for p in sorted(local(root, PREFIX).glob("*.py")):
        ast.parse(p.read_text(), filename=str(p))
        parsed.append(str(p.relative_to(root)))
    curation = load(root, PREFIX + "CURATION_INPUT.json") if phase == "integrated" else None
    draft_path = (curation.get("checkpoint_draft_path") if curation else None) or PREFIX + "CHECKPOINT_RECORD.preservation.v0001.json"
    draft = load(root, draft_path)
    publisher = module(root / "state/publish_checkpoint.py", "fv_individual_checkpoint")
    publisher.validate_record(draft, root)
    need(draft["branch_id"] == "worker-fv-positive-consequences", "Unexpected draft branch identity")
    need(not (root / "state/checkpoints" / draft["branch_id"] / (draft["checkpoint_id"] + ".json")).exists(),
         "Draft unexpectedly present in canonical checkpoint tree")
    for ref in draft["evidence_refs"]:
        check_ref(root, ref)
    inherited_failures = []
    for name, wanted in INHERITED.items():
        need(digest(local(root, name).read_bytes()) == wanted, "Inherited unsupported-schema bytes changed: " + name)
        try:
            publisher.validate_record(load(root, name), root)
        except publisher.Invalid as error:
            need(str(error) == "unsupported checkpoint schema", "Inherited failure changed; inspect its scope")
            inherited_failures.append({"path": name, "sha256": wanted, "actual_error": str(error)})
        else:
            raise ValueError("Inherited unsupported schema unexpectedly validates: " + name)
    result = {"schema": "astra.fv-scoped-validation.v1", "status": "SCOPED_PASS", "phase": phase,
              "intake_id": INTAKE_ID, "incoming_files": 3, "incoming_bytes": incoming["total_bytes"],
              "original_acquisition_scope": incoming["original_acquisition_scope"],
              "inherited_schema_failure_results": inherited_failures,
              "parsed_python_files": parsed, "individual_checkpoint_draft": "PASS; shape/references only",
              "canonical_checkpoint_publication": "NOT_PERFORMED", "preserved_inherited_schema_failures": len(INHERITED),
              "global_checkpoint_validation": "NOT_RUN", "scientific_truth_checked": False,
              "scope": "Preservation, exact record identity, reference linkage and software integrity only. No external proof, priority, physical or practical certification."}
    if phase in {"skeleton", "preserved"}:
        need(not local(root, PREFIX + "INTEGRATION_GENERATOR_RECEIPT.json").exists(), "Integrated packet requires --phase integrated")
        result["live_authority_application"] = "NOT_PERFORMED by preservation tooling"
        if phase == "skeleton":
            original_paths = {x["path"] for x in incoming["files"]} | {PREFIX + "package/SOURCE_MANIFEST.json"}
            observed = {str(x.relative_to(root)) for x in local(root, PREFIX + "package").rglob("*") if x.is_file()}
            need(observed == original_paths, "New research needs an explicit root freeze and --phase preserved")
            result["selected_research_freeze"] = "PENDING_ROOT_SELECTION; no unfinished worker result copied"
        else:
            need(freeze_path, "--phase preserved requires an explicit --freeze-path")
            freeze_raw = local(root, freeze_path).read_bytes()
            frozen = verify_selection(root, {"path": freeze_path, "sha256": digest(freeze_raw)}, expected_base=base)
            derived = load(root, freeze_path.replace("SELECTED_FREEZE", "DERIVED_MANIFEST"))
            need(derived["schema"] == "astra.fv-derived-manifest.v1" and derived["base_revision"] == frozen["base_revision"] and
                 derived["files"] == frozen["files"] and derived["total_files"] == frozen["total_files"] and
                 derived["total_bytes"] == frozen["total_bytes"] and
                 derived["source_freeze"] == {"path": freeze_path, "sha256": digest(freeze_raw)}, "Derived manifest differs from exact frozen selection")
            result["selected_research_freeze"] = {"path": freeze_path, "sha256": digest(freeze_raw), "files": len(frozen["files"])}
    else:
        curation_raw = local(root, PREFIX + "CURATION_INPUT.json").read_bytes()
        curation = json.loads(curation_raw)
        receipt = load(root, PREFIX + "INTEGRATION_GENERATOR_RECEIPT.json")
        base = base or curation["base_revision"]
        need(base == curation["base_revision"] == receipt["base_revision"], "Integration base mismatch")
        need(draft["base_revision"] == base, "Final checkpoint draft requires actual reconciled base")
        need(receipt["schema"] == "astra.fv-generator-receipt.v1" and receipt["intake_id"] == INTAKE_ID,
             "Generator receipt scope mismatch")
        generator_path = root / PREFIX / "build_integration.py"
        need(receipt["generator_sha256"] == digest(generator_path.read_bytes()) and
             receipt["curation_input_sha256"] == digest(curation_raw), "Generator/input receipt hash mismatch")
        generator = module(generator_path, "fv_final_curation_reconstruction")
        need(generator.build_plan(root, curation, digest(curation_raw)).summary()["changed_file_count"] == 0,
             "Finalized curation is not idempotent")
        for name, wanted in receipt["owned_artifacts"].items():
            need(digest(local(root, name).read_bytes()) == wanted, "Generated owned artifact changed: " + name)
        frozen = verify_selection(root, curation.get("selected_freeze"), expected_base=base)
        derived = load(root, curation["selected_freeze"]["path"].replace("SELECTED_FREEZE", "DERIVED_MANIFEST"))
        need(derived["source_freeze"] == curation["selected_freeze"] and derived["files"] == frozen["files"], "Derived manifest differs from exact root freeze")
        need(derived["schema"] == "astra.fv-derived-manifest.v1" and derived["base_revision"] == base,
             "Derived manifest schema/base mismatch")
        need(derived["total_files"] == len(derived["files"]) and
             derived["total_bytes"] == sum(x["bytes"] for x in derived["files"]), "Derived inventory totals mismatch")
        derived_paths = {x["path"] for x in derived["files"]}
        need(len(derived_paths) == len(derived["files"]), "Duplicate derived inventory path")
        for ref in derived["files"]:
            need(ref["path"].startswith(PREFIX) and ref["provenance_role"] in PROVENANCE_ROLES - {"supplied_original_text"}, "Derived provenance boundary failed")
            check_ref(root, ref)
        observed = set()
        original_paths = {x["path"] for x in incoming["files"]} | {PREFIX + "package/SOURCE_MANIFEST.json"}
        for folder in ["package", "replays"]:
            p = local(root, PREFIX + folder)
            if p.exists():
                observed.update(str(x.relative_to(root)) for x in p.rglob("*") if x.is_file() and str(x.relative_to(root)) not in original_paths)
        need(observed == derived_paths, "Selected root/worker/replay inventory differs from frozen manifest")
        claims = rows(root, "indexes/claims.jsonl")
        statuses = rows(root, "frontier/CURRENT_CLAIM_STATUS.jsonl")
        catalog = load(root, "indexes/agent_catalog.json")["claims"]
        claim_map = load(root, PREFIX + "CLAIMS.json")
        ids = set(receipt["cards"])
        need(ids == {x["id"] for x in claim_map["claims"]}, "Owned claim map mismatch")
        need({x.split("-")[0] for x in ids} == set(curation["reserved_routes"]) == set(receipt["reserved_routes"]), "Exact root-reserved numeric route mismatch")
        for cid in ids:
            claim = one(claims, "id", cid)
            status = one(statuses, "card_id", cid)
            entry = one(catalog, "id", cid)
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
        selected_notices = load(root, PREFIX + "SCOPED_NOTICES.json")
        need({x["notice_id"] for x in selected_notices} == set(receipt["notice_ids"]), "Owned notice inventory mismatch")
        for notice in selected_notices:
            need(one(notices, "notice_id", notice["notice_id"]) == notice, "Owned notice differs from registry")
        indexed = load(root, PREFIX + "INDEXED_SOURCES.json")["files"]
        metadata = rows(root, "indexes/source_metadata.jsonl")
        need({x["source_id"] for x in indexed} == set(receipt["source_ids"]), "Owned indexed-source inventory mismatch")
        allowed_sources = {x["path"] for x in incoming["files"]} | derived_paths
        for source in indexed:
            need(source["path"] in allowed_sources and one(metadata, "source_id", source["source_id"]) == source,
                 "Indexed source is not preserved incoming/frozen derived evidence")
        bridges = load(root, PREFIX + "BRIDGES.json")["bridges"]
        need({x["id"] for x in bridges} == set(receipt["bridge_ids"]), "Owned bridge inventory mismatch")
        for item in list(curation["evidence"].values()) + bridges + selected_notices:
            for ref in references(item):
                check_ref(root, ref)
        result.update({"base_revision": base, "cards": len(ids), "open_gates": len(receipt["gate_ids"]),
                       "indexed_sources": len(indexed), "derived_files": len(derived_paths), "exact_owned_ID_selection": True,
                       "history": history(root, base) if check_history else "NOT_RUN; separate root-authorized Git check required", "curation_idempotent": True})
    if check_global:
        need(base, "Global checkpoint validation requires an explicit reconciled base")
        chosen_base = base
        argv = [sys.executable, "-B", "state/publish_checkpoint.py", "validate", "--immutable-base", chosen_base]
        process = subprocess.run(argv, cwd=root, capture_output=True, text=True)
        need(process.returncode != 0 and "unsupported checkpoint schema" in process.stderr,
             "Global checkpoint outcome changed; inspect before relying on inherited-failure boundary")
        result["global_checkpoint_validation"] = {"argv": argv, "exit_code": process.returncode,
            "stdout": process.stdout, "stderr": process.stderr, "status": "FAIL: inherited schemas preserved; individually valid draft only"}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--phase", choices=["skeleton", "preserved", "integrated"], default="skeleton")
    parser.add_argument("--base-revision")
    parser.add_argument("--check-global", action="store_true")
    parser.add_argument("--freeze-path", help="Exact repository-relative versioned root freeze for --phase preserved")
    parser.add_argument("--check-history", action="store_true")
    parser.add_argument("--root-authorized-git", action="store_true", help="Use only after root authorizes Git-based read-only checks")
    args = parser.parse_args()
    print(json.dumps(validate(args.repo, args.phase, args.base_revision, args.check_global, args.freeze_path, args.check_history, args.root_authorized_git), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print("FV scoped validation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
