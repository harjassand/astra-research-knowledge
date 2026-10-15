"""Read-only preparation boundary adapted from FY with distinct HEAD/remote pins."""
from __future__ import annotations

from pathlib import Path
import re
import subprocess

from fz_common import PREFIX, need


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def check_baseline(root, *, immutable_base, expected_head, expected_remote_main, check_remote=False):
    root = Path(root).resolve()
    for name, revision in (("immutable_base", immutable_base), ("expected_head", expected_head), ("expected_remote_main", expected_remote_main)):
        need(isinstance(revision, str) and re.fullmatch(r"[0-9a-f]{40}", revision), name + " must be a full Git revision")
    actual_head = git(root, "rev-parse", "HEAD").decode().strip()
    need(actual_head == expected_head, "Current branch HEAD differs from expected_head; inspect and refresh this check")
    subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", immutable_base, actual_head], check=True, capture_output=True)
    before = set(git(root, "ls-tree", "-r", "--name-only", immutable_base).decode().splitlines())
    changed = git(root, "diff", "--name-only", "--no-renames", immutable_base).decode().splitlines()
    historical = [name for name in changed if name in before]
    need(not historical, "Preparation changed tracked baseline files: " + str(historical))
    need(all(name.startswith(PREFIX) for name in changed), "Preparation added tracked paths outside FZ: " + str([name for name in changed if not name.startswith(PREFIX)]))
    untracked = git(root, "ls-files", "--others", "--exclude-standard").decode().splitlines()
    need(all(name.startswith(PREFIX) for name in untracked), "Unowned untracked paths require separate attribution: " + str([name for name in untracked if not name.startswith(PREFIX)]))
    remote = None
    if check_remote:
        answer = git(root, "ls-remote", "--heads", "origin", "main").decode().split()
        need(answer and re.fullmatch(r"[0-9a-f]{40}", answer[0]), "Remote main could not be read")
        remote = answer[0]
        need(remote == expected_remote_main, "Remote main moved; reconcile against expected_remote_main")
    return {"schema": "astra.fz-protected-baseline-check.v1", "immutable_base": immutable_base,
            "expected_head": expected_head, "actual_head": actual_head,
            "expected_remote_main": expected_remote_main, "observed_remote_main": remote,
            "baseline_tracked_paths": len(before), "historical_changed_path_count": len(historical),
            "changed_FZ_paths": changed, "unowned_untracked_paths": [], "git_mutations": "NOT_PERFORMED",
            "scope": "FZ-only preparation and historical byte preservation. Evidence commits may advance HEAD independently of remote main."}
