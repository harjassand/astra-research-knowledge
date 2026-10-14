#!/usr/bin/env python3
"""Verify listed packet bytes; this establishes no scientific claim."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
for row in manifest['files']:
    path = (root / row['path']).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('missing or unsafe path: ' + row['path'])
    payload = path.read_bytes()
    if len(payload) != row['bytes'] or hashlib.sha256(payload).hexdigest() != row['sha256']:
        raise ValueError('hash or size drift: ' + row['path'])
print(json.dumps({'status':'PASS','files':len(manifest['files']),
                  'scope':'listed packet byte integrity only','mission_status':'NOT_ACHIEVED'}))
