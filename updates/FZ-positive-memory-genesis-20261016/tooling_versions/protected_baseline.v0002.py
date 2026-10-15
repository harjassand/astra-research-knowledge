"""Read-only preparation boundary adapted from FY with distinct HEAD/remote pins."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import subprocess

from fz_common import PREFIX, local, need

IMMUTABLE_PREFIXES = (
    "cards/", "frontier/cards/", "frontier/review_cards/", "updates/", "state/checkpoints/",
    "state/branches/", "technology/records/", "web/pages/", "evaluation/workflows/records/", "mechanisms/bridges/",
)
JSONL_PATHS = (
    "indexes/claims.jsonl", "indexes/source_metadata.jsonl", "frontier/CURRENT_CLAIM_STATUS.jsonl",
    "frontier/OPEN_PROOF_GATES.jsonl", "agent/SEMANTIC_NOTICES.jsonl", "web/documents.jsonl", "state/branches.tsv",
)
JSON_GROUPS = {
    "indexes/agent_catalog.json": ["claims"], "indexes/agent_graph.json": ["nodes", "edges"],
    "mechanisms/bridge_candidates.json": ["bridges", "rejected_transfers"], "web/catalog.json": [None],
}


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def check_baseline(root, *, immutable_base, expected_head, expected_remote_main, phase="prepared", check_remote=False):
    root = Path(root).resolve()
    for name, revision in (("immutable_base", immutable_base), ("expected_head", expected_head), ("expected_remote_main", expected_remote_main)):
        need(isinstance(revision, str) and re.fullmatch(r"[0-9a-f]{40}", revision), name + " must be a full Git revision")
    actual_head = git(root, "rev-parse", "HEAD").decode().strip()
    need(actual_head == expected_head, "Current branch HEAD differs from expected_head; inspect and refresh this check")
    subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", immutable_base, actual_head], check=True, capture_output=True)
    before = set(git(root, "ls-tree", "-r", "--name-only", immutable_base).decode().splitlines())
    changed = git(root, "diff", "--name-only", "--no-renames", immutable_base).decode().splitlines()
    historical = [name for name in changed if name in before]
    untracked = git(root, "ls-files", "--others", "--exclude-standard").decode().splitlines()
    need(phase in {"prepared", "integrated"}, "Unknown boundary phase")
    if phase == "prepared":
        need(not historical, "Preparation changed tracked baseline files: " + str(historical))
        need(all(name.startswith(PREFIX) for name in changed), "Preparation added tracked paths outside FZ: " + str([name for name in changed if not name.startswith(PREFIX)]))
        need(all(name.startswith(PREFIX) for name in untracked), "Unowned untracked paths require separate attribution: " + str([name for name in untracked if not name.startswith(PREFIX)]))
    else:
        for name in historical:
            need(not name.startswith(IMMUTABLE_PREFIXES), "Historical immutable artifact changed: " + name)
        for name in JSONL_PATHS:
            before_raw = git(root, "show", immutable_base + ":" + name)
            need(local(root, name).read_bytes().startswith(before_raw), "Historical registry byte prefix changed: " + name)
        for name, fields in JSON_GROUPS.items():
            before_raw = git(root, "show", immutable_base + ":" + name)
            old, current = json.loads(before_raw), json.loads(local(root, name).read_bytes())
            projection = copy.deepcopy(current)
            for field in fields:
                old_values, new_values = (old[field], current[field]) if field else (old, current)
                need(new_values[:len(old_values)] == old_values, "Historical JSON values/order changed: " + name)
                if field:
                    projection[field] = new_values[:len(old_values)]
                else:
                    projection = new_values[:len(old_values)]
            need((json.dumps(projection, ensure_ascii=False, indent=2) + "\n").encode() == before_raw,
                 "Historical JSON keys/format changed: " + name)
        old = json.loads(git(root, "show", immutable_base + ":indexes/query_aliases.json"))
        current = json.loads(local(root, "indexes/query_aliases.json").read_bytes())
        need(all(current.get(key) == value for key, value in old.items()), "Historical query alias changed")
    remote = None
    if check_remote:
        answer = git(root, "ls-remote", "--heads", "origin", "main").decode().split()
        need(answer and re.fullmatch(r"[0-9a-f]{40}", answer[0]), "Remote main could not be read")
        remote = answer[0]
        need(remote == expected_remote_main, "Remote main moved; reconcile against expected_remote_main")
    return {"schema": "astra.fz-protected-baseline-check.v1", "phase": phase, "immutable_base": immutable_base,
            "expected_head": expected_head, "actual_head": actual_head,
            "expected_remote_main": expected_remote_main, "observed_remote_main": remote,
            "baseline_tracked_paths": len(before), "historical_changed_path_count": len(historical),
            "changed_FZ_paths": changed, "unowned_untracked_paths": [], "git_mutations": "NOT_PERFORMED",
            "scope": "FZ-only preparation and historical byte preservation. Evidence commits may advance HEAD independently of remote main."}
