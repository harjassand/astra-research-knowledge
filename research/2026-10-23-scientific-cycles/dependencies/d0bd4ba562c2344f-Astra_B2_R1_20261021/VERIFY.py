#!/usr/bin/env python3
"""Relocatable package integrity and bounded finite-model replay.

This does not certify infinite-dimensional proofs, novelty, or practical advantage.
It writes no files into the package.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time


def main():
    root = Path(__file__).resolve().parent
    started = time.perf_counter()
    manifest = root / "SHA256SUMS"
    expected = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        path = (root / name).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"Manifest path escapes package: {name}")
        if name in expected:
            raise ValueError(f"Duplicate manifest entry: {name}")
        expected[name] = digest
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(f"SHA256 mismatch: {name}")
    actual_names = {
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and p.name != "SHA256SUMS"
        and "__pycache__" not in p.parts
    }
    if actual_names != set(expected):
        raise ValueError({
            "unlisted": sorted(actual_names - set(expected)),
            "missing": sorted(set(expected) - actual_names),
        })
    replay_started = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, str(root / "verification" / "loglaw_replay.py")],
        cwd=root, check=True, text=True, capture_output=True,
    )
    diagnostic = json.loads(proc.stdout)
    if diagnostic["status"] != "passed_finite_diagnostics":
        raise ValueError(diagnostic)
    result = {
        "status": "PASS",
        "manifest_files": len(expected),
        "finite_diagnostic_cases": len(diagnostic["cases"]),
        "replay_seconds_observed": time.perf_counter() - replay_started,
        "total_seconds_observed": time.perf_counter() - started,
        "scope": "SHA256 integrity and finite identity diagnostics only",
        "universal_theorem_certification": False,
        "historical_archive_replay": False,
        "external_review": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
