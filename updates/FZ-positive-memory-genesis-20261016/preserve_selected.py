#!/usr/bin/env python3
"""Plan/copy an exact root-approved research freeze; no live authority writes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fz_common import PREFIX, RESEARCH_ROOT, digest, encoded, excluded_media, local, need, selection_records, source_package_paths, verify_incoming
from preserve_sources import create_exclusive


def plan_copy(repo, selection_raw, freeze_name, *, research_root=RESEARCH_ROOT):
    repo = Path(repo).resolve()
    incoming = verify_incoming(repo)
    excluded_media(repo)
    need(re.fullmatch(r"SELECTED_FREEZE\.v[0-9]{4}\.json", freeze_name), "Use a versioned freeze filename")
    selection = json.loads(selection_raw)
    items = selection_records(selection, research_root=research_root, check_research=True)
    need(all(x["sha256"] not in {y["sha256"] for y in incoming["files"]} for x in items), "Selected research cannot relabel exact supplied original bytes")
    outputs = {PREFIX + freeze_name: selection_raw}
    inputs = {}
    for item in items:
        raw = local(research_root, item["research_relative_path"]).read_bytes()
        need(digest(raw) == item["sha256"] and len(raw) == item["bytes"], "Selected source changed during preflight")
        inputs[item["research_relative_path"]] = raw
        outputs[item["path"]] = raw
    outputs[PREFIX + freeze_name.replace("SELECTED_FREEZE", "DERIVED_MANIFEST")] = encoded({
        "schema": "astra.fz-derived-manifest.v1", "base_revision": selection["base_revision"],
        "source_freeze": {"path": PREFIX + freeze_name, "sha256": digest(selection_raw)},
        "total_files": len(items), "total_bytes": sum(x["bytes"] for x in items), "files": items,
        "scope": "Root-selected preserved evidence only; scientific truth and external validation separately assessed.",
    })
    before = {}
    for name, raw in outputs.items():
        path = local(repo, name)
        before[name] = path.read_bytes() if path.is_file() else None
        need(before[name] in (None, raw), "Immutable selected-preservation collision: " + name)
    allowed = {x["path"] for x in items}
    for old in local(repo, PREFIX).glob("SELECTED_FREEZE.v[0-9][0-9][0-9][0-9].json"):
        for item in selection_records(json.loads(old.read_bytes())):
            path = local(repo, item["path"])
            need(path.is_file() and digest(path.read_bytes()) == item["sha256"], "Earlier frozen payload changed")
            allowed.add(item["path"])
    observed = {str(p.relative_to(repo)) for p in local(repo, PREFIX + "package/derived").rglob("*") if p.is_file()}
    need(observed <= allowed, "Unselected derived files exist; reconcile without deleting history")
    source_paths = source_package_paths(incoming)
    all_observed = {str(p.relative_to(repo)) for p in local(repo, PREFIX + "package").rglob("*") if p.is_file()}
    need(all_observed <= source_paths | allowed, "Package contains unselected files outside source/derived freezes")
    for path in local(repo, PREFIX + "package").rglob("*"):
        need(not path.is_symlink(), "Package symlink is forbidden")
    return {"repo": repo, "research_root": Path(research_root), "inputs": inputs,
            "before": before, "outputs": outputs, "selection": selection, "package_paths_before": all_observed}


def apply_copy(plan):
    verify_incoming(plan["repo"])
    excluded_media(plan["repo"])
    observed = {str(p.relative_to(plan["repo"])) for p in local(plan["repo"], PREFIX + "package").rglob("*") if p.is_file()}
    need(observed == plan["package_paths_before"], "Concurrent selected-package inventory change; replan")
    for name, raw in plan["inputs"].items():
        need(local(plan["research_root"], name).read_bytes() == raw, "Selected source changed; replan")
    for name, before in plan["before"].items():
        path = local(plan["repo"], name)
        need((path.read_bytes() if path.is_file() else None) == before, "Concurrent selected-preservation change; replan")
    changed = 0
    for name, raw in plan["outputs"].items():
        if plan["before"][name] != raw:
            create_exclusive(local(plan["repo"], name), raw)
            changed += 1
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--selection", required=True, type=Path)
    parser.add_argument("--freeze-name", default="SELECTED_FREEZE.v0001.json")
    parser.add_argument("--copy", action="store_true")
    parser.add_argument("--expect-selection-sha256")
    args = parser.parse_args()
    raw = args.selection.read_bytes()
    if args.copy:
        need(args.expect_selection_sha256 and digest(raw) == args.expect_selection_sha256, "Copy requires exact root-frozen selection SHA-256")
    elif args.expect_selection_sha256:
        need(digest(raw) == args.expect_selection_sha256, "Selection hash changed")
    plan = plan_copy(args.repo, raw, args.freeze_name)
    report = {"schema": "astra.fz-selected-preservation-plan.v1", "mode": "read_only",
              "selection_sha256": digest(raw), "files": len(plan["selection"]["files"]),
              "research_bytes": plan["selection"]["total_bytes"], "output_paths": sorted(plan["outputs"]),
              "live_authority_application": "NOT_PERFORMED"}
    if args.copy:
        need(args.selection.read_bytes() == raw, "Selection input changed during planning")
        report["copied_file_count"] = apply_copy(plan)
        report["mode"] = "root_selected_packet_copy_only"
    print(encoded(report).decode(), end="")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("FZ selected preservation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
