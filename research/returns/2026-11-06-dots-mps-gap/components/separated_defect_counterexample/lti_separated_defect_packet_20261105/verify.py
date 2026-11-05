"""Verify packet hashes and replay the two unchanged internal audit scripts.

Usage: python verify.py [--report /outside/packet/result.json]
The packet itself is never modified. No network access or SDP solver is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest() -> dict:
    manifest_path = ROOT / "MANIFEST.sha256.json"
    manifest = json.loads(manifest_path.read_text())
    expected = manifest["sha256"]
    actual_files = {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and p != manifest_path and "__pycache__" not in p.parts
    }
    assert actual_files == set(expected), {
        "missing": sorted(set(expected) - actual_files),
        "unexpected": sorted(actual_files - set(expected)),
    }
    for rel, digest in expected.items():
        path = Path(rel)
        assert not path.is_absolute() and ".." not in path.parts
        assert sha256(ROOT / path) == digest, f"Hash mismatch: {rel}"
    # The second audit also supplied a separate original-file manifest.
    original_dir = ROOT / "audits" / "ising_and_toric"
    originals = json.loads((original_dir / "SHA256.json").read_text())
    for rel, digest in originals.items():
        assert sha256(original_dir / rel) == digest, f"Original audit changed: {rel}"
    return {
        "packet_files_checked": len(expected),
        "original_audit_files_checked": len(originals),
        "all_hashes_match": True,
    }


def run_script(script: Path) -> tuple[str, float]:
    start = time.perf_counter()
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=script.parent,
        capture_output=True,
        text=True,
        check=True,
    )
    assert not result.stderr.strip(), result.stderr
    return result.stdout, time.perf_counter() - start


def replay() -> dict:
    with tempfile.TemporaryDirectory(prefix="lti_obstruction_replay_") as temp:
        root = Path(temp)
        local = root / "toric_local"
        combined = root / "ising_and_toric"
        shutil.copytree(ROOT / "audits" / "toric_local", local)
        shutil.copytree(ROOT / "audits" / "ising_and_toric", combined)

        stdout, local_seconds = run_script(local / "check_lti.py")
        expected_stdout = (local / "expected_stdout.txt").read_text()
        assert stdout == expected_stdout, "Local toric exact output changed"

        expected = json.loads((combined / "results.json").read_text())
        summary_stdout, combined_seconds = run_script(
            combined / "check_explicit_witnesses.py"
        )
        actual = json.loads((combined / "results.json").read_text())
        # The original script records execution time, not a mathematical datum.
        del expected["elapsed_seconds"]
        del actual["elapsed_seconds"]
        assert actual == expected, "Exact witness result differs from original audit"
        summary = json.loads(summary_stdout)
        assert summary["all_exact_checks_passed"] is True

        return {
            "scripts_run_only_in_temporary_copies": True,
            "local_toric_stdout_identical": True,
            "combined_json_identical_except_elapsed_seconds": True,
            "ising_finite_windows": len(actual["ising_finite_witnesses"]),
            "ising_extendible_windows": len(actual["ising_extendible_witnesses"]),
            "local_toric_all_subrectangle_cases": len(stdout.strip().splitlines()),
            "independent_toric_open_rectangles": len(actual["toric_open_windows"]),
            "toric_global_syndrome_cases": len(actual["toric_global_witnesses"]),
            "dense_density_dimension": actual["toric_dense_check"]["dimension"],
            "local_toric_script_wall_seconds": local_seconds,
            "combined_script_wall_seconds": combined_seconds,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report is not None:
        dest = args.report.resolve()
        assert not dest.is_relative_to(ROOT), "Save reports outside the unchanged packet"
    result = {
        "all_checks_passed": True,
        "manifest": verify_manifest(),
        "reproduction": replay(),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "scope": "Exact witness checks, not an SDP solve, proof assistant, novelty determination, or external review.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        args.report.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
