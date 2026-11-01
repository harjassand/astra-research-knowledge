"""One-time local audit freeze; refuses to overwrite its manifest."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
out=root/'AUDIT_SHA256.json'
if out.exists(): raise SystemExit('REFUSE: manifest already exists')
def entry(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
names=['AUTHOR_FREEZE.json','CHECK_RESULTS.json','UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md','check_initial_growth.py']
original={n:entry(root.parent/n) for n in names}
for n in names:
    assert entry(root/'inputs'/n)==original[n]
freeze=json.loads((root/'inputs/AUTHOR_FREEZE.json').read_text())
for n,expected in freeze['files'].items(): assert original[n]['sha256']==expected
assert original['UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md']['sha256']=='90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e'
assert (root/'inputs/CHECK_RESULTS.json').read_bytes()==(root/'author_replay/CHECK_RESULTS.json').read_bytes()
payloads={str(p.relative_to(root)):entry(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='AUDIT_SHA256.json'}
obj={'status':'PASS_SOURCE_BOUND_MATHEMATICAL_COMPONENT',
     'scope':'Full rate-2 uniform M-hit or B-half-exit law only; not activation/removal/recurrence or an executable receiver.',
     'audit_payloads':payloads,'original_source_bindings':original}
out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
print(json.dumps({'manifest':str(out),'payloads':len(payloads),**entry(out)},sort_keys=True))
