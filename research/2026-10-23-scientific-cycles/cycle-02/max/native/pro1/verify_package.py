#!/usr/bin/env python3
"""Verify this packet's manifest and immutable inherited owner archive."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
checked = 0
for line in (root / "MANIFEST.sha256").read_text().splitlines():
    expected, name = line.split("  ", 1)
    p = root / name
    if not p.is_file():
        raise SystemExit(f"Missing: {name}")
    if hashlib.sha256(p.read_bytes()).hexdigest() != expected:
        raise SystemExit(f"Hash mismatch: {name}")
    checked += 1
p = root / "preserved/Astra_Restore_PRO1_20261021.zip"
assert p.stat().st_size == 923683
assert hashlib.sha256(p.read_bytes()).hexdigest() == (
    "28ba9b7e26b061081d65cda6c0d7b0fed8db7ec423f5e4acb9af0ab1286b0b8d")
print(json.dumps({"status": "verified", "manifest_files": checked,
                  "preserved_owner_identity": "unchanged"}, indent=2))
