#!/usr/bin/env python3
"""Verify delivered package hashes. Integrity is not a scientific certificate."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
data=json.loads((root/"MANIFEST.json").read_text())
failures=[]
for record in data["files"]:
    p=root/record["path"]
    try:
        content=p.read_bytes()
        if len(content)!=record["bytes"] or hashlib.sha256(content).hexdigest()!=record["sha256"]:
            failures.append(record["path"])
    except OSError:
        failures.append(record["path"])
print(json.dumps({"status":"PASS" if not failures else "FAIL",
                  "checked_files":len(data["files"]),"failures":failures,
                  "scope":"Package integrity only, not theorem correctness or novelty."}))
raise SystemExit(bool(failures))
