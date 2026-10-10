#!/usr/bin/env python3
"""Verify CU source bytes and the attached directory's own manifest; run no research code."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "package"
META = json.loads((ROOT / "INTEGRITY.json").read_text(encoding="utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


source_root = PACKAGE
expected = META["source_files"]
actual: set[str] = set()
for path in source_root.rglob("*"):
    if path.is_symlink():
        raise SystemExit(f"Symlink is not allowed: {path}")
    if path.is_file():
        actual.add(path.relative_to(source_root).as_posix())
if actual != set(expected):
    raise SystemExit(f"Source membership mismatch: extra={sorted(actual-set(expected))}, missing={sorted(set(expected)-actual)}")
for rel, record in expected.items():
    data = (source_root / rel).read_bytes()
    if len(data) != record["bytes"] or sha(data) != record["sha256"]:
        raise SystemExit(f"Source hash/size mismatch: {rel}")

attached = PACKAGE / "attached" / "Astra_Two_Completed_Investigations_2026-10-10"
manifest = json.loads((attached / "ARCHIVE_MANIFEST.json").read_bytes())
entries = manifest["files"]
listed = {item["path"] for item in entries}
payload = {p.relative_to(attached).as_posix() for p in attached.rglob("*")
           if p.is_file() and p.name != "ARCHIVE_MANIFEST.json"}
if payload != listed:
    raise SystemExit(f"Attached manifest membership mismatch: extra={sorted(payload-listed)}, missing={sorted(listed-payload)}")
for item in entries:
    data = (attached / item["path"]).read_bytes()
    if len(data) != item["bytes"] or sha(data) != item["sha256"]:
        raise SystemExit(f"Attached manifest hash/size mismatch: {item['path']}")

if len(entries) != META["attached_manifest"]["payload_file_count"]:
    raise SystemExit("Attached manifest payload count mismatch")
if sha((attached / "ARCHIVE_MANIFEST.json").read_bytes()) != META["attached_manifest"]["manifest_sha256"]:
    raise SystemExit("Attached manifest hash mismatch")

print(f"PASS: {len(expected)} copied source files; {len(entries)} manifest-listed attached payload files; no research code executed")
