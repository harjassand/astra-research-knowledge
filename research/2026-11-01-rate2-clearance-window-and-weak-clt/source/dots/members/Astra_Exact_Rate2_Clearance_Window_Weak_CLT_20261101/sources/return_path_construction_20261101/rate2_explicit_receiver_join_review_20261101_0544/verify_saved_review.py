#!/usr/bin/env python3
"""Read-only verification of the two joins and their exact harmonic receipt."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;root=p.parents[1]
r=json.loads((p/'REVIEW_RECEIPT.json').read_text())
assert r['status']=='INDEPENDENT_EXPLICIT_RECEIVER_REPLACEMENTS_PASS'
assert not r['open_blockers']
for name,item in r['payloads'].items():
 raw=(p/name).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==item['sha256'],name
 assert len(raw)==item['bytes'],name
for name,item in r['source_bindings'].items():
 assert hashlib.sha256((root/item['path']).read_bytes()).hexdigest()==item['sha256'],name
mf=root/r['source_bindings']['harmonic_manifest']['path'];j=json.loads(mf.read_text())
for name,item in j['audit_payloads'].items():
 raw=(mf.parent/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==item['sha256'],name
 assert len(raw)==item['bytes'],name
for name,item in j['original_source_bindings'].items():
 raw=(mf.parent.parent/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==item['sha256'],name
 assert len(raw)==item['bytes'],name
print('PASS: both replacements, qualified dependency scopes, and all harmonic payload bindings are intact.')
