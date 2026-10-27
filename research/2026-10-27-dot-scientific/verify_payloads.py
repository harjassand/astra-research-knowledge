#!/usr/bin/env python3
"""Verify the selected immutable scientific bytes; never run scientific code."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def verify(root: Path = ROOT) -> dict:
    index = json.loads((root / "SOURCE_INDEX.json").read_text())
    inventory = json.loads((root / "provenance/FROZEN_INVENTORY.json").read_text())
    frozen = {row["path"]: row for row in inventory["files"]}
    seen = set()
    total = 0
    for row in index["files"]:
        logical = row["original_path"]
        expected = frozen[logical]
        if row["sha256"] != expected["sha256"] or row["bytes"] != expected["bytes"]:
            raise ValueError("Index disagrees with frozen source: " + logical)
        path = (root / row["repository_path"]).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("Source path escapes this intake: " + row["repository_path"])
        data = path.read_bytes()
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError("Selected source bytes changed: " + logical)
        if logical in seen:
            raise ValueError("Duplicate logical source identity: " + logical)
        seen.add(logical)
        total += len(data)
        if path.suffix == ".py":
            ast.parse(data, filename=logical)
        elif path.suffix == ".json":
            json.loads(data)
    indexed_paths = {row["repository_path"] for row in index["files"]}
    retained = {p.relative_to(root).as_posix() for p in (root / "source").rglob("*")
                if p.is_file() and "__pycache__" not in p.parts}
    if indexed_paths != retained:
        raise ValueError("Source inventory is incomplete: " + str(sorted(indexed_paths ^ retained)[:5]))
    omissions = json.loads((root / "provenance/REPOSITORY_SELECTION.json").read_text())
    unselected = {row["path"] for row in omissions["unselected_frozen_paths"]}
    if seen & unselected or seen | unselected != set(frozen):
        raise ValueError("Frozen path selection does not form an exact partition")
    for row in omissions["unselected_frozen_paths"]:
        expected = frozen[row["path"]]
        if row["sha256"] != expected["sha256"] or row["bytes"] != expected["bytes"]:
            raise ValueError("Unselected source identity changed: " + row["path"])
    closure = json.loads((root / "provenance/RECEIPT_DEPENDENCY_CLOSURE.json").read_text())
    gaps = [row for row in closure["checks"] if row["status"] == "no_matching_frozen_bytes_located"]
    if len(gaps) != 9 or closure["summary"]["no_matching_frozen_bytes_located"] != len(gaps):
        raise ValueError("Historical receipt gap declaration changed")
    return {"retained_original_files": len(seen), "retained_original_bytes": total,
            "unselected_frozen_paths": len(unselected), "historical_unverified_receipt_references": len(gaps),
            "scope": "Immutable selected-byte and syntax verification; not a scientific proof or replay."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root), indent=2))
    except (ValueError, OSError, KeyError, SyntaxError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
