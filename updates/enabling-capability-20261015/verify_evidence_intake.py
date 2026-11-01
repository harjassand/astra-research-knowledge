#!/usr/bin/env python3
"""Verify preserved bytes/paths only; this does not verify scientific claims."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys


REQUIRED = [
    "evidence/root/REPORT.txt",
    "evidence/root/QA_AND_CORRECTIONS.json",
    "evidence/root/CLAIM_LEDGER.json",
    "evidence/root/GOAL_TELEMETRY_FREEZE_v0001.json",
    "evidence/root/replay_uniform_sharp_audit.py",
    "evidence/root/uniform_sharp_audit.json",
    "evidence/workers/computation_search/CORRECTION_004.txt",
    "evidence/workers/computation_search/FINAL_AMENDMENT_004.txt",
    "evidence/workers/computation_search/FAST_VECTOR_REPLAY.json",
    "evidence/workers/computation_search/MATCHED_TARGET_FAST_VECTOR.json",
    "evidence/workers/s05_energy_certificates/inputs/CORRECTION_004.txt",
    "evidence/workers/s05_energy_certificates/inputs/FINAL_AMENDMENT_004.txt",
    "evidence/workers/a08_grouped_werner/UNIFORM_SCHMIDT_PROOF.txt",
    "evidence/workers/a08_grouped_werner/uniform_schmidt.json",
    "evidence/workers/s10_foundation_compute/UNIFORM_AUDIT.txt",
    "evidence/workers/s10_foundation_compute/uniform_sharp_audit.json",
    "evidence/workers/premise_challenge/SYNTHESIS_AUDIT.txt",
    "evidence/workers/s07_remote_control/data/20261015T052637Z_10000000_KFS_current_route_10MHz_iq.wav",
    "evidence/workers/computation_search/source/LICENSE",
    "evidence/workers/s08_photon_evidence/AUTHOR_BSD_LICENSE.txt",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("EVIDENCE_MANIFEST_v0002.json"))
    parser.add_argument("--verify-current-sources", action="store_true")
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    update = manifest_path.parent
    manifest = json.loads(manifest_path.read_text())
    errors, source_changes, json_issues, python_issues = [], [], [], []
    seen, total, workers = set(), 0, set()
    for row in manifest["files"]:
        relative = row["path"]
        if relative in seen:
            errors.append("duplicate manifest path: " + relative)
        seen.add(relative)
        path = update / relative
        if not path.resolve().is_relative_to(update) or path.is_symlink():
            errors.append("unsafe evidence path: " + relative)
            continue
        if not path.is_file():
            errors.append("missing copy: " + relative)
            continue
        data = path.read_bytes()
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            errors.append("copy/hash mismatch: " + relative)
        if len(data) > 5_000_000:
            errors.append("over compact file limit: " + relative)
        total += len(data)
        if relative.startswith("evidence/workers/"):
            workers.add(Path(relative).parts[2])
        if path.suffix == ".json":
            try:
                json.loads(data)
            except (json.JSONDecodeError, UnicodeError) as exc:
                json_issues.append({"path": relative, "error": str(exc)})
        if path.suffix == ".py":
            try:
                ast.parse(data)
            except (SyntaxError, UnicodeError) as exc:
                python_issues.append({"path": relative, "error": str(exc)})
        if args.verify_current_sources:
            source = row["source_path"]
            if source.startswith("workers/"):
                original = Path(manifest["workers_root"]) / source.removeprefix("workers/")
            elif source.startswith("root/") and manifest.get("root_artifacts_source"):
                original = Path(manifest["root_artifacts_source"]) / source.removeprefix("root/")
            else:
                errors.append("unknown source scope: " + source)
                continue
            if not original.is_file() or digest(original.read_bytes()) != row["sha256"]:
                source_changes.append(source)
    actual = {str(p.relative_to(update)) for p in (update / "evidence").rglob("*") if p.is_file()}
    errors.extend("unmanifested evidence: " + p for p in sorted(actual - seen))
    errors.extend("missing required final artifact: " + p for p in REQUIRED if manifest["status"] == "ROOT_FINAL_SYNC" and p not in seen)
    if len(workers) != 30 or sorted(workers) != manifest["workers"]:
        errors.append("worker coverage mismatch")
    if total != manifest["included_bytes"] or len(seen) != manifest["included_count"]:
        errors.append("count/byte total mismatch")
    for row in manifest.get("prior_snapshot_bytes_retained", []):
        path = update / row["path"]
        if not path.is_file() or digest(path.read_bytes()) != row["sha256"]:
            errors.append("preliminary history mismatch: " + row["path"])
    if (update / "evidence/root/spectral_deconvolution.py").exists():
        errors.append("forbidden publisher code copied into root evidence")
    if (update / "evidence/root/PR_BODY.txt").exists():
        errors.append("editorial PR body copied into scientific evidence")
    result = {
        "status": "PASS" if not errors and not source_changes and not json_issues and not python_issues else "FAIL",
        "manifest": str(manifest_path),
        "manifest_sha256": digest(manifest_path.read_bytes()),
        "workers": len(workers), "files": len(seen), "bytes": total,
        "copied_byte_or_path_errors": errors,
        "current_source_hash_changes": source_changes,
        "json_parse_issues": json_issues, "python_syntax_issues": python_issues,
        "current_sources_checked": args.verify_current_sources,
        "scope": "Byte/hash/coverage/history, JSON parse and Python syntax only. No original scientific script executed, no proof correctness, physical validation, novelty, licensing adjudication or universal self-contained replay certified.",
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
