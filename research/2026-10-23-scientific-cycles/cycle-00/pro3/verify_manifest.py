#!/usr/bin/env python3
"""Verify capsule members before any replay mutates result receipts."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root/"MANIFEST.json").read_text())
for item in manifest["files"]:
    path = root/item["path"]
    data = path.read_bytes()
    assert len(data) == item["bytes"], item["path"]
    assert hashlib.sha256(data).hexdigest() == item["sha256"], item["path"]
print(json.dumps({"all_files_verified": True, "file_count": len(manifest["files"])}))
