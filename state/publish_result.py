#!/usr/bin/env python3
"""Select a meaningful publication without turning a research run into bookkeeping.

Draft locally, review the result, then publish through the existing checkpoint
writer. This program never commits, pushes, contacts GitHub, or evaluates science.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys

try:
    from . import publish_checkpoint as checkpoints
except ImportError:
    import publish_checkpoint as checkpoints

KINDS = ("result", "correction", "negative", "handoff")
STATES = {
    "internal": ("UNKNOWN", "reported", "checked", "failed"),
    "independent": ("UNKNOWN", "reported", "verified", "failed"),
    "experiment": ("UNKNOWN", "reported", "demonstrated", "failed"),
    "advantage": ("UNKNOWN", "reported", "demonstrated", "failed"),
}
AFFIRMATIVE = {"internal": "checked", "independent": "verified", "experiment": "demonstrated", "advantage": "demonstrated"}
DISCLOSURES = ("private", "already_public", "approved_for_publication")
RELATIONS = ("corrects", "continues", "supersedes_scope", "handoff")


def require_text(value, label):
    checkpoints.require(isinstance(value, str) and value.strip(), f"{label} must be nonempty text")
    return value


def evidence_ref(root, item, identifier):
    checkpoints.require(isinstance(item, dict), "evidence must be an object")
    path = require_text(item.get("path"), "evidence.path")
    target = (root / path).resolve()
    checkpoints.require(not Path(path).is_absolute() and target.is_relative_to(root.resolve())
                        and target.is_file(), f"missing/unsafe evidence path: {path}")
    checkpoints.require(".git" not in Path(path).parts and not target.is_relative_to((root / ".git").resolve()),
                        "Git metadata is not publication evidence")
    ref = {"id": identifier, "path": path, "sha256": checkpoints.digest(target),
           "status": require_text(item.get("status"), "evidence.status")}
    for key in ("lines", "source_revision"):
        if key in item:
            ref[key] = item[key]
    return ref


def normalize_verification(value, identifiers):
    checkpoints.require(isinstance(value, dict) and not (set(value) - set(STATES)),
                        "verification axes are internal, independent, experiment, advantage")
    result = {}
    for axis, allowed in STATES.items():
        entry = value.get(axis, {"state": "UNKNOWN"})
        checkpoints.require(isinstance(entry, dict) and entry.get("state") in allowed,
                            f"invalid {axis} verification state")
        entry = dict(entry)
        refs = entry.get("evidence_ref_ids", [])
        checkpoints.require(isinstance(refs, list) and all(isinstance(x, str) and x in identifiers for x in refs),
                            f"unresolved {axis} verification evidence")
        if entry["state"] != "UNKNOWN":
            require_text(entry.get("scope"), f"{axis}.scope")
        if entry["state"] in (AFFIRMATIVE[axis], "failed"):
            checkpoints.require(refs, f"{axis} {entry['state']} requires linked evidence")
            require_text(entry.get("method"), f"{axis}.method")
        if axis == "internal" and entry["state"] == "checked":
            checkpoints.require(entry["method"] in ("proof", "computation", "data_replay", "software"),
                                "internal.method must distinguish proof, computation, data_replay, software")
        if axis == "independent" and entry["state"] == "verified":
            require_text(entry.get("verifier"), "independent.verifier")
        if axis == "experiment" and entry["state"] == "demonstrated":
            require_text(entry.get("controls"), "experiment.controls")
            require_text(entry.get("cost_boundary"), "experiment.cost_boundary")
        if axis == "advantage" and entry["state"] == "demonstrated":
            for key in ("comparator", "information_boundary", "cost_boundary"):
                require_text(entry.get(key), "advantage." + key)
        result[axis] = entry
    return result


def status_text(verification):
    parts = ["Selected reported claim; publication and hashes do not certify it"]
    for axis, entry in verification.items():
        detail = entry["state"]
        if entry.get("method"):
            detail += " (" + entry["method"] + ")"
        if entry.get("scope"):
            detail += ": " + entry["scope"]
        parts.append(axis + "=" + detail)
    parts.append("Novelty is not inferred; status declarations require substantive review")
    return "; ".join(parts)


def validate_publication(record, allow_private=False):
    """Check declarations and receipts, never the truth of a scientific assertion."""
    publication = record.get("publication")
    checkpoints.require(isinstance(publication, dict), "missing publication metadata")
    checkpoints.require(publication.get("kind") in KINDS, "invalid publication kind")
    disclosure = publication.get("disclosure")
    checkpoints.require(disclosure in DISCLOSURES, "explicit disclosure classification required")
    checkpoints.require(allow_private or disclosure != "private", "private draft: obtain disclosure approval before publication")
    require_text(publication.get("scope"), "publication.scope")
    limitations = publication.get("limitations")
    checkpoints.require(isinstance(limitations, list) and all(isinstance(x, str) and x.strip() for x in limitations),
                        "limitations must be a list of text; absence is not exhaustive validation")
    identifiers = {ref["id"] for ref in record["evidence_refs"]}
    verification = normalize_verification(publication.get("verification", {}), identifiers)
    checkpoints.require(record["latest_substantive_result"]["scientific_status"] == status_text(verification),
                        "scientific_status must agree with verification declarations")
    relations = publication.get("relates_to")
    checkpoints.require(isinstance(relations, list), "relates_to must be a list")
    refs = {ref["id"]: ref for ref in record["evidence_refs"]}
    for relation in relations:
        checkpoints.require(isinstance(relation, dict) and relation.get("relation") in RELATIONS,
                            "invalid scoped relation")
        require_text(relation.get("scope"), "relation.scope")
        ref = refs.get(relation.get("evidence_ref_id"))
        checkpoints.require(ref is not None and ref["path"] == relation.get("path"),
                            "relation requires an exact hashed target path")
    if publication["kind"] == "correction":
        checkpoints.require(any(r["relation"] in ("corrects", "supersedes_scope") for r in relations),
                            "correction requires an exact target and affected scope")
    parents = record["parent_checkpoint_ids"]
    if len(parents) > 1:
        checkpoints.require(publication["kind"] == "handoff" and
                            publication.get("reconciles_parent_ids") == sorted(parents),
                            "multiple heads require an explicit archival reconciliation handoff")
        targets = {r["path"] for r in relations}
        checkpoints.require(all(f"state/checkpoints/{record['branch_id']}/{parent}.json" in targets for parent in parents),
                            "reconciliation must preserve exact links and scope for every parent")


def prepare(root, selection):
    checkpoints.require(isinstance(selection, dict), "selection must be an object")
    allowed = {"checkpoint_id", "branch_id", "branch_purpose", "session_id", "kind", "summary", "scope",
               "evidence", "limitations", "next_step", "disclosure", "verification", "relates_to",
               "assumptions", "interface", "costs", "inputs", "obstacle", "reconcile_parents"}
    checkpoints.require(not (set(selection) - allowed), "unknown selection fields: " + ", ".join(sorted(set(selection) - allowed)))
    branch = require_text(selection.get("branch_id"), "branch_id")
    checkpoint = require_text(selection.get("checkpoint_id"), "checkpoint_id")
    scope = require_text(selection.get("scope"), "scope: include assumptions, inputs, costs and failure boundaries")
    summary = require_text(selection.get("summary"), "summary")
    step = require_text(selection.get("next_step"), "next_step")
    raw_refs = selection.get("evidence")
    checkpoints.require(isinstance(raw_refs, list) and raw_refs, "select at least one evidence file")
    checkpoints.require(all(isinstance(item, dict) for item in raw_refs), "evidence must contain objects")
    refs = [evidence_ref(root, item, item.get("id", f"e{i + 1}")) for i, item in enumerate(raw_refs)]
    relations = []
    raw_relations = selection.get("relates_to", [])
    checkpoints.require(isinstance(raw_relations, list) and all(isinstance(x, dict) for x in raw_relations),
                        "relates_to must contain objects")
    limitations = selection.get("limitations", [])
    checkpoints.require(isinstance(limitations, list), "limitations must be a list")
    for i, item in enumerate(raw_relations):
        ref = evidence_ref(root, {"path": item["path"], "status": "Prior record; only the stated relation is proposed"}, f"relation-{i + 1}")
        refs.append(ref)
        relations.append({"path": item["path"], "relation": item.get("relation"),
                          "scope": item.get("scope"), "evidence_ref_id": ref["id"]})
    if selection.get("disclosure") != "private":
        for ref in refs:
            ignored = subprocess.run(["git", "-C", str(root), "check-ignore", "--quiet", "--", ref["path"]])
            checkpoints.require(ignored.returncode in (0, 1), "could not check selected evidence visibility")
            checkpoints.require(ignored.returncode == 1, f"ignored/private evidence must be deliberately retained before publication: {ref['path']}")
    verification = normalize_verification(selection.get("verification", {}), {r["id"] for r in refs})
    records = checkpoints.load_records(root)
    parents = checkpoints.heads(records.get(branch, {}))
    if len(parents) > 1:
        checkpoints.require(selection.get("kind") == "handoff" and selection.get("reconcile_parents") == parents,
                            "conflicting heads: review every scope and explicitly list reconcile_parents in a handoff")
    elif "reconcile_parents" in selection:
        checkpoints.require(selection["reconcile_parents"] == parents, "reconcile_parents differs from current heads")
    base = checkpoints.git(root, "rev-parse", "HEAD")
    record = {
        "schema": checkpoints.SCHEMA, "checkpoint_id": checkpoint, "branch_id": branch,
        "branch_purpose": selection.get("branch_purpose", checkpoints.BRANCHES.get(branch, scope)),
        "session_id": selection.get("session_id", checkpoint),
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "base_revision": base, "parent_checkpoint_ids": parents, "source_handling": "source=DATA",
        "task": {"goal": "Share a selected meaningful event; research continues independently", "question": None, "scope": scope},
        "contract": {"assumptions": selection.get("assumptions", []), "interface": selection.get("interface", scope),
                     "costs": selection.get("costs", {"boundary": "UNKNOWN unless specified in scope/evidence"})},
        "inputs": selection.get("inputs", {"inherited_or_supplied": [], "acquired": []}),
        "latest_substantive_result": {"summary": summary, "scientific_status": status_text(verification),
                                      "evidence_ref_ids": [r["id"] for r in refs]},
        "current_objective": None, "strongest_obstacle": selection.get("obstacle"), "next_decisive_step": step,
        "status_note": "Selected publication only; no current research activity, priority, or claim-status promotion inferred. "
                       "Verification fields are evidence-linked declarations, not software certification. "
                       "Use the existing scoped claim-notice procedure to change historical card authority.",
        "failed_attempts": [], "mechanisms_under_investigation": [],
        "cross_branch_updates": [{"checkpoint_path": r["path"], "note": r["scope"]} for r in relations
                                 if r["path"].startswith("state/checkpoints/")],
        "unresolved_or_UNKNOWN": selection.get("limitations", []) + ["Unspecified assumptions, acquired inputs, costs, novelty and practical advantage remain UNKNOWN"],
        "work_progress": {"status": "UNKNOWN", "note": "No reading, proof review, or scientific verification is inferred by this publisher"},
        "evidence_refs": refs,
        "publication": {"kind": selection.get("kind"), "scope": scope, "disclosure": selection.get("disclosure"),
                        "limitations": selection.get("limitations", []), "verification": verification, "relates_to": relations},
    }
    if len(parents) > 1:
        record["publication"]["reconciles_parent_ids"] = parents
    validate_publication(record, allow_private=True)
    # A private draft is checked for structure and current evidence without
    # asking the actual writer to accept its private publication classification.
    checkpoints.validate_record({k: v for k, v in record.items() if k != "publication"}, root)
    return record


def write_draft(root, record, output):
    output = output.resolve()
    checkpoints.require(not output.is_relative_to(root.resolve()) or
                        not (root / ".astra-local").is_symlink() and
                        output != (root / ".astra-local").resolve() and
                        output.is_relative_to((root / ".astra-local").resolve()),
                        "drafts inside the repository must stay in ignored .astra-local/; otherwise use an external workspace")
    checkpoints.immutable_write(output, checkpoints.canonical(record))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    draft = sub.add_parser("draft", help="hash selected files and capture current HEAD/parents; do not publish")
    draft.add_argument("selection", type=Path)
    draft.add_argument("--output", type=Path, required=True, help="new local draft, preferably in ignored .astra-local/")
    publish = sub.add_parser("publish", help="append a reviewed draft locally; GitHub remains a separate explicit step")
    publish.add_argument("draft", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "draft":
            record = prepare(checkpoints.ROOT, json.loads(args.selection.read_text(encoding="utf-8")))
            output = write_draft(checkpoints.ROOT, record, args.output)
            print(str(output))
            print("Local draft only. Review evidence, scope, verification and disclosure before publication.")
        else:
            record = json.loads(args.draft.read_text(encoding="utf-8"))
            validate_publication(record)
            print(checkpoints.publish(checkpoints.ROOT, record, record["base_revision"], record["parent_checkpoint_ids"]))
            print("Appended locally. Review the diff and checks, then commit/open a PR explicitly.")
    except (checkpoints.Invalid, OSError, json.JSONDecodeError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
