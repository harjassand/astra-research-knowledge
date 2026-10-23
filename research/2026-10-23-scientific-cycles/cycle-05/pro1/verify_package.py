#!/usr/bin/env python3
"""Verify source byte integrity, never mathematical truth."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
count = 0
for line in (root / 'MANIFEST.sha256').read_text().splitlines():
    expected, name = line.split('  ', 1)
    path = root / name
    assert path.resolve().is_relative_to(root.resolve()), name
    assert path.is_file(), name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
    count += 1
p = root / 'preserved' / 'Astra_Amplification_Cycle4_PRO1_20261022.zip'
assert p.stat().st_size == 3149965
assert hashlib.sha256(p.read_bytes()).hexdigest() == '26e741f32745216cd4f4a773e5e5001952008015c68f9a1187805f87ad079ac8'
print(json.dumps({'status': 'passed', 'manifest_files': count,
                  'unchanged_parent': True,
                  'scope': 'Byte integrity only; not theorem certification.'}))
