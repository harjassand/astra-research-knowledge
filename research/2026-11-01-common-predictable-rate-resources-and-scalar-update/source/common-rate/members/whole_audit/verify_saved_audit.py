from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((A/'AUDIT_SHA256.json').read_text())
for name,z in m['files'].items():
 p=A/name
 assert p.is_file() and not p.is_symlink(),name
 assert len(p.read_bytes())==z['bytes'] and h(p)==z['sha256'],name
for version,expected in [('v1','16c0b44e613b2b779422ac81c7356d6b31ed61f47180d8ad177154527bfe9a44'),('v2','e54a3514c15a8ce5b0a62c18e28ab0c4b286339f52d880cde952e1c1c40c7112')]:
 d=A/('frozen_'+version);p=d/'AUTHOR_MANIFEST.json';assert h(p)==expected
 for name,z in json.loads(p.read_text())['files'].items():
  p=d/name;assert len(p.read_bytes())==z['bytes'] and h(p)==z['sha256'],name
print('PASS saved immutable whole v2 audit:',len(m['files']),'payload bindings; both exact source manifests/snapshots verified. V1 remains failure history.')
