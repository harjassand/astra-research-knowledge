#!/usr/bin/env python3
"""Plan or copy an exact root-approved evidence freeze into FV; no live curation."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fv_common import PREFIX, RESEARCH_ROOT, digest, excluded_media, local, need, selection_records, verify_incoming


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def plan_copy(repo, selection_raw, freeze_name, *, research_root=RESEARCH_ROOT):
    repo = Path(repo).resolve()
    verify_incoming(repo)
    excluded_media(repo)
    need(re.fullmatch(r"SELECTED_FREEZE\.v[0-9]{4}\.json", freeze_name), "Use a new versioned freeze filename")
    selection = json.loads(selection_raw)
    items = selection_records(selection, research_root=research_root, check_research=True)
    outputs = {PREFIX + freeze_name: selection_raw}
    inputs = {}
    for item in items:
        source = local(research_root, item["research_relative_path"])
        raw = source.read_bytes()
        need(digest(raw) == item["sha256"] and len(raw) == item["bytes"], "Selected research changed during preflight")
        inputs[item["research_relative_path"]] = raw
        outputs[item["path"]] = raw
    derived_name = freeze_name.replace("SELECTED_FREEZE", "DERIVED_MANIFEST")
    outputs[PREFIX + derived_name] = encoded({
        "schema": "astra.fv-derived-manifest.v1", "base_revision": selection["base_revision"],
        "source_freeze": {"path": PREFIX + freeze_name, "sha256": digest(selection_raw)},
        "total_files": len(items), "total_bytes": sum(x["bytes"] for x in items), "files": items,
        "scope": "Exact root-selected preserved evidence only; proof truth and external validation remain separately assessed.",
    })
    before = {}
    for name, raw in outputs.items():
        path = local(repo, name)
        before[name] = path.read_bytes() if path.is_file() else None
        need(before[name] in (None, raw), "Immutable preservation collision: " + name)
    allowed_existing = {PREFIX + "package/" + x for x in ["SOURCE_MANIFEST.json", "sources/physical_pasted.txt", "sources/mathematics_pasted.txt", "sources/computation_pasted.txt"]}
    observed = {str(p.relative_to(repo)) for p in local(repo, PREFIX + "package").rglob("*") if p.is_file()}
    need(observed <= allowed_existing | {x["path"] for x in items}, "Unselected package files exist; reconcile explicitly without deleting history")
    return {"repo": repo, "research_root": Path(research_root), "inputs": inputs,
            "before": before, "outputs": outputs, "selection": selection, "package_paths_before": observed}


def apply_copy(plan):
    # Every input and destination is rechecked before the first write.
    verify_incoming(plan["repo"])
    excluded_media(plan["repo"])
    observed = {str(p.relative_to(plan["repo"])) for p in local(plan["repo"], PREFIX + "package").rglob("*") if p.is_file()}
    need(observed == plan["package_paths_before"], "Concurrent package inventory change; replan")
    for name, raw in plan["inputs"].items():
        need(local(plan["research_root"], name).read_bytes() == raw, "Selected source changed; replan before copying")
    for name, before in plan["before"].items():
        target = local(plan["repo"], name)
        need((target.read_bytes() if target.is_file() else None) == before, "Concurrent preservation change; replan")
    changed = 0
    for name, raw in plan["outputs"].items():
        if plan["before"][name] == raw:
            continue
        target = local(plan["repo"], name)
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".fv-preservation-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
        changed += 1
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--selection", required=True, type=Path)
    parser.add_argument("--freeze-name", default="SELECTED_FREEZE.v0001.json")
    parser.add_argument("--copy", action="store_true", help="Copy only root-frozen evidence into the FV packet")
    parser.add_argument("--expect-selection-sha256", help="Required for copying")
    args = parser.parse_args()
    raw = args.selection.read_bytes()
    if args.copy:
        need(args.expect_selection_sha256 and digest(raw) == args.expect_selection_sha256,
             "--copy requires the exact root-frozen selection SHA-256")
    elif args.expect_selection_sha256:
        need(digest(raw) == args.expect_selection_sha256, "Selection input hash changed")
    plan = plan_copy(args.repo, raw, args.freeze_name)
    report = {"schema": "astra.fv-preservation-plan.v1", "mode": "read_only",
              "selection_sha256": digest(raw), "files": len(plan["selection"]["files"]),
              "research_bytes": plan["selection"]["total_bytes"],
              "output_paths": sorted(plan["outputs"]), "live_authority_application": "NOT_PERFORMED"}
    if args.copy:
        need(args.selection.read_bytes() == raw, "Selection input changed during planning")
        report["copied_file_count"] = apply_copy(plan)
        report["mode"] = "root_selected_packet_copy_only"
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("FV preservation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
