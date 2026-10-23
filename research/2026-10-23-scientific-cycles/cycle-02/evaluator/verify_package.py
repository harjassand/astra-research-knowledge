#!/usr/bin/env python3
"""Portable identity verification only; not scientific or source authentication."""
from pathlib import Path
import hashlib,json,sys

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    root=Path(__file__).resolve().parent
    data=json.loads((root/"MANIFEST.json").read_text())
    failures=[]
    for row in data["files"]:
        rel=Path(row["path"])
        if rel.is_absolute() or ".." in rel.parts:
            failures.append({"path":str(rel),"error":"unsafe manifest path"});continue
        p=root/rel
        if not p.is_file():
            failures.append({"path":str(rel),"error":"missing"});continue
        if p.stat().st_size!=row["bytes"] or digest(p)!=row["sha256"]:
            failures.append({"path":str(rel),"error":"identity mismatch"})
    print(json.dumps({"status":"FAIL" if failures else "PASS", "checked_payload_files":len(data["files"]),"failures":failures,"scope":"Payload identities only. A mutable package cannot authenticate itself; compare archive/source digests to independently received references. No scientific calculation executed."},indent=2))
    return bool(failures)
if __name__=="__main__":
    sys.exit(main())
