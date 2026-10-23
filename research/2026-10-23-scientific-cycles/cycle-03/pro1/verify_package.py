#!/usr/bin/env python3
"""Verify the delivered bytes, not the scientific theorems."""
from pathlib import Path
import hashlib
import json
import zipfile

root=Path(__file__).resolve().parent
manifest=root/'MANIFEST.sha256'
if not manifest.exists():
    raise SystemExit('Run this script from the extracted delivered package, which contains MANIFEST.sha256.')
checked=0
for line in manifest.read_text().splitlines():
    digest,name=line.split('  ',1)
    path=root/name
    if not path.is_file():
        raise SystemExit(f'Missing manifest file: {name}')
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f'Hash mismatch: {name}')
    checked+=1
parent=root/'preserved/Astra_Amplification_Cycle2_PRO1_20261022.zip'
assert parent.stat().st_size==2041187
assert hashlib.sha256(parent.read_bytes()).hexdigest()=='1cb1b91c3c79e46d67d1686d7aa5d33ab889d28f826048710fa24ec6f81753c3'
with zipfile.ZipFile(parent) as z:
    assert z.testzip() is None
print(json.dumps({'status':'PASS','manifest_files_verified':checked,
                  'unchanged_parent_bytes':2041187,
                  'scope':'Integrity/provenance only, not scientific certification.'},indent=2))
