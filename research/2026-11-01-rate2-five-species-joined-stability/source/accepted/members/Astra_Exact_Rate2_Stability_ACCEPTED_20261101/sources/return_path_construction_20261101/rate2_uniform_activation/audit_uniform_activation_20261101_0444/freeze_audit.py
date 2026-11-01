"""One-time freeze of the completed local proof review; refuses overwrite."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent;out=root/'AUDIT_SHA256.json'
if out.exists():raise SystemExit('REFUSE: existing audit manifest')
def entry(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
files=['AUTHOR_FREEZE.json','CHECK_RESULTS.json','UNIFORM_ACTIVATION_OR_REMOVAL.md','check_activation.py']
original={n:entry(root.parent/n) for n in files}
for n in files:assert entry(root/'inputs'/n)==original[n]
source_manifest=json.loads((root/'inputs/AUTHOR_FREEZE.json').read_text())
for n,h in source_manifest['files'].items():assert original[n]['sha256']==h
assert original['UNIFORM_ACTIVATION_OR_REMOVAL.md']['sha256']=='c1d2ed0820d4f92ea236dcb27eab1cd29e27665f9b1a2e826617cc34e3c3fda8'
assert (root/'inputs/CHECK_RESULTS.json').read_bytes()==(root/'author_replay/CHECK_RESULTS.json').read_bytes()
base='../rate2_uniform_initial_growth/'
gate='audit_uniform_growth_20261101_0435/'
deps={base+'UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md':'90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e',
      base+gate+'SOURCE_BOUND_ACCEPTANCE.md':'a1eb22f7376fb8cfd138908629f7242edc164dc721476be0999dde4716de67e8',
      base+gate+'MATHEMATICAL_REVIEW.md':'70cf81fd5d27fe68bc90bf32ac1b21cd254fecfe1e56a049ec28fdb0998d3e00',
      base+gate+'AUDIT_SHA256.json':'e4e73437f7958c35e339617dc14cef6595c7138cdccc20cbe393336ae3f2a6d8'}
depentries={}
for n,h in deps.items():
    e=entry(root.parent/n);assert e['sha256']==h
    assert entry(root/'dependencies'/Path(n).name)==e
    depentries[n]=e
payloads={str(p.relative_to(root)):entry(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p!=out}
obj={'status':'PASS_SOURCE_BOUND_MATHEMATICAL_COMPONENT','scope':'Actual uniform activation-or-removal OR-target hitting law; no interior-entry/full population-reduction/recurrence or executable numerical receiver.',
     'audit_payloads':payloads,'original_source_bindings':original,'dependency_bindings':depentries}
out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
print(json.dumps({'audit_payloads':len(payloads),'manifest':str(out),**entry(out)},sort_keys=True))
