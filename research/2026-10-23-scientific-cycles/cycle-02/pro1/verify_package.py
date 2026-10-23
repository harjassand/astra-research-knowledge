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
parent=root/'preserved/Astra_Intelligence_Cycle_PRO1_20261021.zip'
assert parent.stat().st_size==1468188
assert hashlib.sha256(parent.read_bytes()).hexdigest()=='672fd5c387e051bfeaaad5e718b5642a84fa2e57931003dabde7277705c50739'
with zipfile.ZipFile(parent) as z:
    assert z.testzip() is None
print(json.dumps({'status':'PASS','manifest_files_verified':checked,
                  'unchanged_parent_bytes':1468188,
                  'scope':'Integrity/provenance only, not scientific certification.'},indent=2))
