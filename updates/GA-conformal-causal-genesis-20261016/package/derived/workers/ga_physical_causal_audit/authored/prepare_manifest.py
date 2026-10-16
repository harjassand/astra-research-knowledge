#!/usr/bin/env python3
"""Allowlist only authored audit outputs and public receipts, never external sources."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
paths=[ROOT/"REPORT.md",ROOT/"AUDIT.md"]
paths+=sorted((ROOT/"authored").glob("*.py"))
paths+=sorted((ROOT/"authored").glob("*.json"))
paths+=sorted((ROOT/"receipts").glob("*.json"))
entries=[]
for path in paths:
    rel=path.relative_to(ROOT)
    assert "external_excluded_from_publication" not in rel.parts
    data=path.read_bytes()
    entries.append({"path":str(rel),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
manifest={"scope":"integrity/publication allowlist only; no scientific or rights certification",
          "recursive_exclusions":["external_excluded_from_publication/"],"files":entries}
(ROOT/"PUBLICATION_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps({"allowlisted_files":len(entries),"external_files_allowlisted":0}))
