#!/usr/bin/env python3
"""Verify archive contents, not scientific correctness."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
checked = 0
for line in (root / 'MANIFEST.sha256').read_text().splitlines():
    digest, name = line.split('  ', 1)
    path = root / name
    assert path.is_file(), name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, name
    checked += 1
parent = root / 'preserved/Astra_Amplification_Cycle7_PRO1_20261022.zip'
assert parent.stat().st_size == 4800520
assert hashlib.sha256(parent.read_bytes()).hexdigest() == '4fe694bb30a7e6515af2a96b2bdabd8e81fb8308ea9981ae7611fb661ae8d9ff'
print(json.dumps({'status':'PASS','manifested_files':checked,
                  'predecessor_exact':True,
                  'scope':'File integrity only; not mathematical acceptance'}))
