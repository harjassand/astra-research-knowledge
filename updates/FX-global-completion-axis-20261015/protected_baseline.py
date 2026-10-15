"""Read-only baseline checks: old evidence and historical registry values persist."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import subprocess

from fx_common import IMMUTABLE_PREFIXES, PREFIX, digest, local, need

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


def check_baseline(root, base, *, phase="prepared", check_remote=False):
    root = Path(root).resolve()
    need(re.fullmatch(r"[0-9a-f]{40}", str(base)), "Protected baseline must be a full Git revision")
    subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", base, "HEAD"], check=True, capture_output=True)
    before_paths = set(git(root, "ls-tree", "-r", "--name-only", base).decode().splitlines())
    changed = git(root, "diff", "--name-only", "--no-renames", base).decode().splitlines()
    historical_changed = [name for name in changed if name in before_paths]
    if phase == "prepared":
        need(not historical_changed, "Preparation changed tracked baseline files: " + str(historical_changed))
        untracked = git(root, "ls-files", "--others", "--exclude-standard").decode().splitlines()
        need(all(name.startswith(PREFIX) for name in untracked), "Unowned untracked paths require separate attribution: " + str([x for x in untracked if not x.startswith(PREFIX)]))
    else:
        for name in historical_changed:
            need(not name.startswith(IMMUTABLE_PREFIXES), "Historical immutable artifact changed: " + name)
    for name in JSONL_PATHS:
        before = git(root, "show", base + ":" + name)
        need(local(root, name).read_bytes().startswith(before), "Historical registry byte prefix changed: " + name)
    for name, fields in JSON_GROUPS.items():
        raw = git(root, "show", base + ":" + name)
        before, current = json.loads(raw), json.loads(local(root, name).read_bytes())
        projection = copy.deepcopy(current)
        for field in fields:
            old, new = (before[field], current[field]) if field else (before, current)
            need(new[:len(old)] == old, "Historical JSON values/order changed: " + name)
            if field:
                projection[field] = new[:len(old)]
            else:
                projection = new[:len(old)]
        need((json.dumps(projection, ensure_ascii=False, indent=2) + "\n").encode() == raw, "Historical JSON keys/format changed: " + name)
    name = "indexes/query_aliases.json"
    before = json.loads(git(root, "show", base + ":" + name))
    current = json.loads(local(root, name).read_bytes())
    need(all(current.get(k) == v for k, v in before.items()), "Historical query alias changed")
    remote = None
    if check_remote:
        answer = git(root, "ls-remote", "--heads", "origin", "main").decode().split()
        need(answer and re.fullmatch(r"[0-9a-f]{40}", answer[0]), "Remote main could not be read")
        remote = answer[0]
        need(remote == base, "Remote main moved; rebase/reconcile and recheck IDs before root application")
    return {"schema": "astra.fx-protected-baseline-check.v1", "base_revision": base, "phase": phase,
            "head": git(root, "rev-parse", "HEAD").decode().strip(), "baseline_tracked_paths": len(before_paths),
            "historical_immutable_artifacts_unchanged": True, "historical_registry_prefixes_and_values_unchanged": True,
            "historical_changed_path_count": len(historical_changed), "remote_main": remote,
            "git_mutations": "NOT_PERFORMED", "scope": "Byte/history preservation only; no historical scientific-status promotion."}
