"""One-time completed-audit freeze; refuses to overwrite its manifest."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent;out=root/'AUDIT_SHA256.json'
if out.exists():raise SystemExit('REFUSE: audit manifest already exists')
def entry(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
names=['AUTHOR_FREEZE.json','CHECK_RESULTS.json','EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md','check_harmonic_service.py']
original={n:entry(root.parent/n) for n in names}
for n in names:assert entry(root/'inputs'/n)==original[n]
m=json.loads((root/'inputs/AUTHOR_FREEZE.json').read_text())
for n,h in m['files'].items():assert original[n]['sha256']==h
assert original['EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md']['sha256']=='4d1ad7a929f7e3c6d81d06222bd8217eb96e06eb183e6f0cfe3f5dbca6ca16ca'
assert (root/'inputs/CHECK_RESULTS.json').read_bytes()==(root/'author_replay/CHECK_RESULTS.json').read_bytes()
payloads={str(p.relative_to(root)):entry(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p!=out}
m={'status':'PASS_SOURCE_BOUND_MATHEMATICAL_COMPONENT','scope':'Explicit actual harmonic macro endpoint service only; replacement joins and numerical runtime admission are separate.','audit_payloads':payloads,'original_source_bindings':original}
out.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
print(json.dumps({'manifest':str(out),'audit_payloads':len(payloads),**entry(out)},sort_keys=True))
