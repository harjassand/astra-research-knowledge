#!/usr/bin/env python3
"""Nonmutating verification of the preserved release bytes."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256_MANIFEST.json').read_text())
fail=[]
for name,expected in manifest['sha256'].items():
    p=root/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        fail.append(name)
if fail:
    raise SystemExit('Byte verification failed: '+', '.join(fail))
print('Verified '+str(len(manifest['sha256']))+' preserved files. This checks bytes, not theorem correctness.')
