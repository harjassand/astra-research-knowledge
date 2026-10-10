#!/usr/bin/env python3
"""Verify CV intake byte inventories and nested source manifests; never run research code."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTAKE = ROOT / "updates/CV"
PKG = INTAKE / "package"

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def manifest_lines(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        result[rel.strip().lstrip("*")] = digest
    return result

def check_subset(base: Path, manifest: Path, expected: dict[str, str]) -> None:
    declared = manifest_lines(manifest)
    if declared != expected:
        raise SystemExit(f"manifest contents differ: {manifest.relative_to(ROOT)}")
    for rel, digest in declared.items():
        if sha((base / rel).read_bytes()) != digest:
            raise SystemExit(f"manifest hash mismatch: {manifest.relative_to(ROOT)}:{rel}")

inventory = json.loads((INTAKE / "INTEGRITY.json").read_text(encoding="utf-8"))
if inventory.get("intake_id") != "CV" or inventory.get("source_root") != "updates/CV/package":
    raise SystemExit("incorrect intake identity or source root")
expected = inventory["source_files"]
actual = {p.relative_to(PKG).as_posix() for p in PKG.rglob("*") if p.is_file()}
if actual != set(expected):
    raise SystemExit(f"source membership mismatch: missing={sorted(set(expected)-actual)} extra={sorted(actual-set(expected))}")
if any(p.is_symlink() for p in PKG.rglob("*")):
    raise SystemExit("symlink in preserved source package")
for rel, record in expected.items():
    data = (PKG / rel).read_bytes()
    if len(data) != record["bytes"] or sha(data) != record["sha256"]:
        raise SystemExit(f"intake inventory mismatch: {rel}")

natural = PKG / "evidence_gated_natural_science_screen_supporting_record_2026-10-10"
for name in ("ARTIFACTS.sha256", "FREEZE.sha256"):
    check_subset(natural, natural / name, manifest_lines(natural / name))

burst = PKG / "burst_qec_investigation_20261010"
burst_manifest = json.loads((burst / "manifest.json").read_text(encoding="utf-8"))
burst_expected = {p.relative_to(burst).as_posix(): sha(p.read_bytes()) for p in burst.rglob("*") if p.is_file() and p.name != "manifest.json"}
if burst_manifest.get("artifacts_sha256") != burst_expected:
    raise SystemExit("burst QEC manifest membership/hash mismatch")

entropy = PKG / "Astra_Entropy_Mechanism_and_Transfer_Tests_2026-10-10"
entropy_manifest_path = entropy / "ARCHIVE_MANIFEST.json"
entropy_expected = json.loads(entropy_manifest_path.read_text(encoding="utf-8"))
entropy_actual = {p.relative_to(entropy).as_posix(): sha(p.read_bytes()) for p in entropy.rglob("*") if p.is_file() and p != entropy_manifest_path}
if entropy_actual != entropy_expected:
    missing = sorted(set(entropy_expected) - set(entropy_actual))
    extra = sorted(set(entropy_actual) - set(entropy_expected))
    wrong = sorted(k for k in set(entropy_expected) & set(entropy_actual) if entropy_expected[k] != entropy_actual[k])
    raise SystemExit(f"entropy archive manifest mismatch: missing={missing} extra={extra} wrong={wrong}")

print(json.dumps({"intake_id":"CV","source_files":len(actual),"source_bytes":sum(v["bytes"] for v in expected.values()),"nested_manifests":{"natural_artifacts":len(manifest_lines(natural/"ARTIFACTS.sha256")),"natural_freeze":len(manifest_lines(natural/"FREEZE.sha256")),"burst_qec":len(burst_expected),"entropy_archive":len(entropy_actual)},"research_scripts_executed":False,"result":"PASS"},indent=2))
