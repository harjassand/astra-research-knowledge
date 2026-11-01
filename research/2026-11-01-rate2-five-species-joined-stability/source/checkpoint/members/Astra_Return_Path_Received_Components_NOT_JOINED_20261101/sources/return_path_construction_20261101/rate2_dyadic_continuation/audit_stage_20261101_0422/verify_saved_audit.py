from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parent
for name,z in json.loads((A/'AUDIT_SHA256.json').read_text())['files'].items():
 p=A/name;assert p.is_file()and not p.is_symlink()
 assert len(p.read_bytes())==z['bytes']and hashlib.sha256(p.read_bytes()).hexdigest()==z['sha256'],name
print('PASS immutable conditional-stage audit bindings; stopping conventions and scope in SOURCE_BOUND_ACCEPTANCE.md govern.')
