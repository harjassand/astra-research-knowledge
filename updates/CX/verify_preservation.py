#!/usr/bin/env python3
"""Check CX source membership, exact bytes, hash, and line inventory only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTAKE = ROOT / "updates/CX"
PACKAGE = INTAKE / "package"

record = json.loads((INTAKE / "INTEGRITY.json").read_text(encoding="utf-8"))
if record.get("schema") != "astra-intake-integrity/1" or record.get("intake_id") != "CX":
    raise SystemExit("incorrect intake identity")
expected = record["source_files"]
actual = {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob("*") if p.is_file()}
if actual != set(expected):
    raise SystemExit(f"source membership mismatch: missing={sorted(set(expected)-actual)} extra={sorted(actual-set(expected))}")
if any(p.is_symlink() for p in PACKAGE.rglob("*")):
    raise SystemExit("symlink in preserved source package")
for rel, item in expected.items():
    data = (PACKAGE / rel).read_bytes()
    if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
        raise SystemExit(f"source hash/size mismatch: {rel}")
    if len(data.decode("utf-8").splitlines()) != item["lines"]:
        raise SystemExit(f"source line count mismatch: {rel}")

print(json.dumps({"intake_id": "CX", "source_files": len(actual),
                  "source_bytes": sum(item["bytes"] for item in expected.values()),
                  "research_scripts_executed": False, "result": "PASS"}, indent=2))
