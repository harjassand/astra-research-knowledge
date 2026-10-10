#!/usr/bin/env python3
"""Deterministically verify CT source preservation; does not run research code."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "package"
META = json.loads((ROOT / "INTEGRITY.json").read_text(encoding="utf-8"))

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

archive = PACKAGE / "RESEARCH_PACKET.zip"
archive_bytes = archive.read_bytes()
expected_archive = META["archive"]
assert len(archive_bytes) == expected_archive["bytes"]
assert sha(archive_bytes) == expected_archive["sha256"]
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist()) == expected_archive["zip_members"]
    assert len(z.namelist()) == len(set(z.namelist()))
    assert z.testzip() is None
    prefix = "ASTRA_ULTRA_CHECKPOINT/"
    manifest_path = prefix + "MANIFEST.json"
    raw_manifest = z.read(manifest_path)
    assert sha(raw_manifest) == expected_archive["internal_manifest_sha256"]
    manifest = json.loads(raw_manifest)
    entries = manifest["files"] if isinstance(manifest, dict) else manifest
    assert entries is not None and len(entries) == expected_archive["manifest_entries"]
    listed = {item["path"] for item in entries}
    members = {name[len(prefix):] for name in z.namelist()
               if name.startswith(prefix) and name != manifest_path and not name.endswith("/")}
    assert members == listed | {"README.txt"}
    for item in entries:
        data = z.read(prefix + item["path"])
        assert len(data) == item["bytes"], item["path"]
        assert sha(data) == item["sha256"], item["path"]
    extracted = {
        "RESEARCH_STATUS.txt": "RESEARCH_STATUS.txt",
        "ARCHIVE_README.txt": "README.txt",
        "work/ERRATA.txt": "work/ERRATA.txt",
        "work/VERIFICATION.txt": "work/VERIFICATION.txt",
        "work/COORDINATOR_ENERGY_DERIVATION.txt": "work/COORDINATOR_ENERGY_DERIVATION.txt",
        "work/round3/04_gaussian_reduction.txt": "work/round3/04_gaussian_reduction.txt",
        "work/COORDINATOR_GL_OBSTRUCTION.txt": "work/COORDINATOR_GL_OBSTRUCTION.txt",
        "work/COORDINATOR_CHANNEL_COMPRESSION.txt": "work/COORDINATOR_CHANNEL_COMPRESSION.txt",
        "work/COORDINATOR_LOOP_VARIANCE.txt": "work/COORDINATOR_LOOP_VARIANCE.txt",
        "work/COORDINATOR_COMPLEX_LY.txt": "work/COORDINATOR_COMPLEX_LY.txt",
        "work/COORDINATOR_NPT_LOCAL.txt": "work/COORDINATOR_NPT_LOCAL.txt",
    }
    for rel, member in extracted.items():
        assert (PACKAGE / rel).read_bytes() == z.read(prefix + member), rel
    for rel in ["RESEARCH_STATUS.txt", "RETAINED_MATHEMATICS.txt", "RESEARCH_STATE.json"]:
        assert (PACKAGE / rel).read_bytes() == z.read(prefix + rel), rel
    assert (PACKAGE / "RESEARCH_STATUS.txt").read_bytes() == z.read(prefix + "RESEARCH_STATUS.txt")

for rel, record in META["source_files"].items():
    data = (PACKAGE / rel).read_bytes()
    assert len(data) == record["bytes"], rel
    assert sha(data) == record["sha256"], rel
print(f"PASS: {len(entries)} manifest entries, {len(members)} packet payload members, "
      f"{len(META['source_files'])} copied source views; no research code executed")
