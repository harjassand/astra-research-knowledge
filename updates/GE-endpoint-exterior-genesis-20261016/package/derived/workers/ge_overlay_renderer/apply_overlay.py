#!/usr/bin/env python3
"""Apply a reviewed, create-only GE overlay with append-only registry deltas.

This command mutates the Astra checkout only when invoked explicitly. It never
stages, commits, or pushes Git changes. The receipt is written outside the
checkout and records the exact file hashes applied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


INTAKE = "GE-endpoint-exterior-genesis-20261016"
ALLOWED_ADDITIONS = {
    "indexes/source_metadata.jsonl",
    "indexes/claims.jsonl",
    "frontier/CURRENT_CLAIM_STATUS.jsonl",
    "frontier/OPEN_PROOF_GATES.jsonl",
    "agent/SEMANTIC_NOTICES.jsonl",
    "web/documents.jsonl",
    "indexes/agent_catalog.json",
    "indexes/agent_graph.json",
    "web/catalog.json",
    "mechanisms/bridge_candidates.json",
    "indexes/query_aliases.json",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def check_pins(repo: Path, pins: dict) -> dict:
    need(isinstance(pins, dict), "Plan needs base_revision, expected_branch_head, and expected_remote_main pins")
    base = pins.get("base_revision")
    head = pins.get("expected_branch_head")
    remote_expected = pins.get("expected_remote_main")
    for name, value in (("base_revision", base), ("expected_branch_head", head),
                        ("expected_remote_main", remote_expected)):
        need(isinstance(value, str) and len(value) == 40
             and all(char in "0123456789abcdef" for char in value),
             f"{name} must be a full Git SHA")
    actual = run_git(repo, "rev-parse", "HEAD")
    need(actual == head, f"HEAD changed: expected {head}, observed {actual}")
    baseline_tools = repo / "updates/FZ-positive-memory-genesis-20261016"
    need((baseline_tools / "protected_baseline.py").is_file(),
         "Pinned FZ baseline checker is unavailable")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(baseline_tools))
    try:
        from protected_baseline import check_baseline  # type: ignore
        baseline = check_baseline(
            repo, immutable_base=base, expected_head=head,
            expected_remote_main=remote_expected, phase="integrated", check_remote=True,
        )
    finally:
        try:
            sys.path.remove(str(baseline_tools))
        except ValueError:
            pass
    need(not run_git(repo, "status", "--porcelain"),
         "Astra working tree is not clean; reconcile before applying the staged overlay")
    return baseline


def compact_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def validate_stage(repo: Path, stage: Path) -> tuple[dict, dict[str, bytes]]:
    repo = repo.resolve()
    stage = stage.resolve()
    need(stage.is_dir() and not stage.is_relative_to(repo),
         "Stage must be an existing directory outside the Astra checkout")
    plan_path = stage / "PLAN.json"
    need(plan_path.is_file(), "Stage is missing PLAN.json")
    plan_raw = plan_path.read_bytes()
    plan = json.loads(plan_raw)
    need(plan.get("schema") == "astra.ge-overlay-plan.v1"
         and plan.get("intake_id") == INTAKE, "Unsupported GE plan")
    pins = plan.get("pins")
    check_pins(repo, pins)
    expected = pins["expected_branch_head"]

    listed = plan.get("staged_files")
    base_hashes = plan.get("base_registry_sha256")
    need(isinstance(listed, dict) and isinstance(base_hashes, dict),
         "Plan needs staged_files and base_registry_sha256 maps")
    need(set(base_hashes) == ALLOWED_ADDITIONS,
         "Plan must pin every allowed append-only registry")
    actual_files: dict[str, bytes] = {}
    actual_hashes: dict[str, str] = {}
    for path in stage.rglob("*"):
        if not path.is_file() or path == plan_path:
            continue
        relative = path.relative_to(stage).as_posix()
        raw = path.read_bytes()
        actual_files[relative] = raw
        actual_hashes[relative] = sha(raw)
    need(actual_hashes == listed, "Stage contents or hashes differ from PLAN.json")
    need(plan.get("staged_file_count") == len(listed),
         "staged_file_count disagrees with staged_files")
    for path in listed:
        need(path.startswith("overlay/") or path.startswith("additions/"),
             "Staged file is outside overlay/ or additions/: " + path)
        if path.startswith("additions/"):
            target = path.removeprefix("additions/")
            need(target in ALLOWED_ADDITIONS, "Unexpected registry addition target: " + target)
        if path.startswith("overlay/"):
            target = path.removeprefix("overlay/")
            need(not (repo / target).exists(),
                 "Create-only target already exists in checkout: " + target)
    return plan, actual_files


def append_jsonl(old: bytes, delta: bytes, path: str) -> bytes:
    need(old.endswith(b"\n"), "Existing JSONL registry lacks final newline: " + path)
    need(delta.endswith(b"\n"), "JSONL delta lacks final newline: " + path)
    for line in delta.splitlines():
        if line.strip():
            json.loads(line.decode("utf-8"))
    return old + delta


def extend_json_registry(old: bytes, delta: bytes, path: str) -> bytes:
    original = json.loads(old.decode("utf-8"))
    addition = json.loads(delta.decode("utf-8"))
    if path == "indexes/query_aliases.json":
        need(isinstance(original, dict) and isinstance(addition, dict),
             "Query alias registry and delta must be objects")
        need(not (set(original) & set(addition)), "Query alias key collision")
        original.update(addition)
    elif path == "web/catalog.json":
        need(isinstance(original, list) and isinstance(addition, list),
             "Web catalog registry and delta must be arrays")
        original.extend(addition)
    else:
        need(isinstance(original, dict) and isinstance(addition, dict),
             "Nested JSON registry and delta must be objects: " + path)
        for key, values in addition.items():
            need(key in original and isinstance(original[key], list) and isinstance(values, list),
                 "Registry append target is not an existing array: " + path + ":" + key)
            original[key].extend(values)
    # Python dict insertion order preserves all historical keys and appends new
    # alias keys in delta order. Existing array elements remain an exact prefix.
    return compact_json(original)


def prepare_writes(repo: Path, stage: Path, plan: dict,
                   staged: dict[str, bytes]) -> dict[str, bytes]:
    repo = repo.resolve()
    stage = stage.resolve()
    writes: dict[str, bytes] = {}
    base_hashes = plan["base_registry_sha256"]
    for relative, raw in staged.items():
        if relative.startswith("overlay/"):
            target = relative.removeprefix("overlay/")
            destination = (repo / target).resolve()
            need(destination.is_relative_to(repo), "Overlay target escapes checkout: " + target)
            need(not destination.exists(), "Create-only target appeared after staging: " + target)
            writes[target] = raw
        elif relative.startswith("additions/"):
            target = relative.removeprefix("additions/")
            need(target in ALLOWED_ADDITIONS, "Unexpected additions path: " + target)
            current = (repo / target).read_bytes()
            need(sha(current) == base_hashes[target],
                 "Protected registry changed since staging: " + target)
            if target.endswith(".jsonl"):
                writes[target] = append_jsonl(current, raw, target)
            else:
                writes[target] = extend_json_registry(current, raw, target)
    return writes


def write_create_only(repo: Path, relative: str, raw: bytes) -> None:
    target = repo / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(target, flags, 0o644)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(fd)


def atomic_replace(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile("wb", dir=path.parent, prefix=".ge-append-", delete=False) as handle:
            temp_name = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name is not None:
            temp_name.unlink(missing_ok=True)


def apply(repo: Path, stage: Path, receipt: Path) -> dict:
    repo = repo.resolve()
    stage = stage.resolve()
    receipt = receipt.resolve()
    need(not receipt.is_relative_to(repo),
         "Apply receipt must be written outside the Astra checkout")
    need(not receipt.exists(), "Refusing to overwrite apply receipt: " + str(receipt))
    plan, staged = validate_stage(repo, stage)
    writes = prepare_writes(repo, stage, plan, staged)

    # Recheck the branch and all append-only baselines immediately before the
    # first write. The staged overlay has no Git add/commit behavior.
    expected = plan["pins"]["expected_branch_head"]
    check_pins(repo, plan["pins"])
    for path, digest in plan["base_registry_sha256"].items():
        need(sha((repo / path).read_bytes()) == digest,
             "Protected registry changed during apply preflight: " + path)
    for path in writes:
        if path not in ALLOWED_ADDITIONS:
            need(not (repo / path).exists(), "Create-only target appeared during apply preflight: " + path)

    for path, raw in writes.items():
        if path in ALLOWED_ADDITIONS:
            atomic_replace(repo / path, raw)
        else:
            write_create_only(repo, path, raw)
    for path, raw in writes.items():
        need((repo / path).read_bytes() == raw, "Post-write byte verification failed: " + path)

    receipt_data = {
        "schema": "astra.ge-overlay-apply-receipt.v1",
        "status": "APPLIED_REVIEWED_OVERLAY",
        "intake_id": INTAKE,
        "head_before": expected,
        "stage_plan_sha256": sha((stage / "PLAN.json").read_bytes()),
        "files_written": {path: sha(raw) for path, raw in sorted(writes.items())},
        "git_mutations": "NOT_PERFORMED",
        "boundary": "File and append-only registry integrity only; scientific statuses are unchanged.",
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    with receipt.open("xb") as handle:
        handle.write(compact_json(receipt_data))
        handle.flush()
        os.fsync(handle.fileno())
    return {"files_written": len(writes), "receipt": str(receipt)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="Astra checkout to update after review")
    parser.add_argument("--stage", type=Path, required=True, help="External GE staging directory")
    parser.add_argument("--receipt", type=Path, required=True, help="New receipt path outside the checkout")
    args = parser.parse_args()
    result = apply(args.repo, args.stage, args.receipt)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print("GE overlay apply failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
