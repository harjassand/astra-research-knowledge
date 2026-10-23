#!/usr/bin/env python3
"""Verify exact delivered bytes; this is not scientific acceptance."""
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for item in manifest['files']:
    p=ROOT/item['path']
    assert p.is_file(), ('Missing',item['path'])
    assert p.stat().st_size==item['bytes'], ('Size',item['path'])
    assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'], ('Hash',item['path'])
print(json.dumps({'status':'PASS','verified_payload_files':len(manifest['files']),
                  'scope':'Delivered bytes only; not scientific acceptance or novelty.'}))
