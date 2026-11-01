#!/usr/bin/env python3
"""Read-only verification of this review and its exact received dependencies."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
root=p.parents[2]
r=json.loads((p/'REVIEW_RECEIPT.json').read_text())
for name,item in r['payloads'].items():
    raw=(p/name).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==item['sha256'],name
    assert len(raw)==item['bytes'],name
for name,item in r['dependencies'].items():
    assert hashlib.sha256((root/item['path']).read_bytes()).hexdigest()==item['sha256'],name
assert not r['open_blockers']
print('PASS: review payloads and exact dependencies match; no open blocker.')
