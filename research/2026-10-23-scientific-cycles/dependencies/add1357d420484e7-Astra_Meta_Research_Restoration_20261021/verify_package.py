#!/usr/bin/env python3
"""Verify source transport integrity; does not certify scientific claims."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
manifest = json.loads((base/"MANIFEST.json").read_text())
checked = 0
for row in manifest["files"]:
    rel = Path(row["path"])
    assert not rel.is_absolute() and ".." not in rel.parts
    data = (base/rel).read_bytes()
    assert len(data) == row["bytes"], row["path"]
    assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
    checked += 1
print(json.dumps({"status":"PASS","files_checked":checked,
                  "scope":"Transport/source integrity only; not truth, novelty or research amplification."}))
