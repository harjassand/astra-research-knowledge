"""One-time local audit freeze; refuses overwrite."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent;ws=root.parents[2];out=root/'AUDIT_SHA256.json'
if out.exists():raise SystemExit('REFUSE: existing audit manifest')
def ent(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
inputs=json.loads((root/'INPUT_BINDINGS.json').read_text())
original={}
for n,e in inputs['own'].items():
 source='return_path_construction_20261101/rate2_induction_clock_20261101/'+n
 assert ent(ws/source)==e and ent(root/'inputs'/n)==e
 original[source]=e
for n,e in inputs['dependencies'].items():assert ent(ws/n)==e
for name in ['FINITE_LEVEL_AUTHOR_FREEZE.json','CLEARANCE_AUTHOR_FREEZE.json']:
 m=json.loads((root/'inputs'/name).read_text())
 for n,h in m['files'].items():assert inputs['own'][n]['sha256']==h
for n in ['CLOCK_CHECK_RESULTS.json','CLEARANCE_CHECK_RESULTS.json']:
 assert (root/'inputs'/n).read_bytes()==(root/'author_replay/rate2_induction_clock_20261101'/n).read_bytes()
payloads={str(p.relative_to(root)):ent(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p!=out}
data={'status':'PASS_TWO_SOURCE_BOUND_MATHEMATICAL_COMPONENTS','scope':'Actual corrected finite-level clock and analytical clearance/occupation/LLN join; interior numerical constants remain unevaluated; no executable admission or point-mass CDF claim.',
'audit_payloads':payloads,'original_source_bindings':original,'dependency_bindings':inputs['dependencies']}
out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
print(json.dumps({'manifest':str(out),'audit_payloads':len(payloads),**ent(out)},sort_keys=True))
