#!/usr/bin/env python3
"""Verify this private delivery's exact payload bytes; execute no scientific code."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text())['files']
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
if actual != set(manifest) | {'MANIFEST.json'}:
    raise SystemExit('Unexpected or absent payload file')
for name, record in manifest.items():
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts:
        raise SystemExit('Unsafe manifest path')
    data = (root / name).read_bytes()
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise SystemExit('Payload mismatch: ' + name)
print(json.dumps({'status': 'PASS_TRANSPORT_HASHES_ONLY', 'files_verified': len(manifest),
                  'scientific_code_executed': False, 'scientific_acceptance_inferred': False}))
