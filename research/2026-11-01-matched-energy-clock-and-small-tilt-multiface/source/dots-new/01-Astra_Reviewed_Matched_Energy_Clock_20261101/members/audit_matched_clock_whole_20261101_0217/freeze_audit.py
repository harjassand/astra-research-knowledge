from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parent;W=A.parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bindings=json.loads((A/'FINAL_SOURCE_BINDINGS.json').read_text())
assert len(bindings)==100
for z in bindings:
 p=W/z['path'];assert len(p.read_bytes())==z['bytes'] and h(p)==z['sha256'],str(p)
f=W/'matched_energy_clock_constructor_20261101/FROZEN_SHA256.json'
assert len(f.read_bytes())==18256 and h(f)=='b8179929c53e2eaa0f22809137efdd02da0fc7372f8efab9ae3527122349fed3'
files={}
for p in sorted(A.rglob('*')):
 if not p.is_file() or '__pycache__'in p.parts or p.suffix=='.pyc' or p==A/'AUDIT_SHA256.json':continue
 assert not p.is_symlink()
 files[str(p.relative_to(A))]={'bytes':len(p.read_bytes()),'sha256':h(p)}
m={'schema':'matched_energy_clock_independent_whole_audit.v1','verdict':'PASS frozen whole executable and finite original-task receiving; restrictions in WHOLE_REVIEW.md govern','author_freeze_sha256':h(f),'full_receiver_sha256':'5308c5ba22810d72a3792a19cfba74adede235ed0d60d603e64448e64d74ec9e','author_source_bindings':100,'independent_whole_assertions':1035,'independent_primitive_assertions_separate':4306,'independent_whole_UNKNOWN':467,'additional_exploratory_UNKNOWN':1,'replayed_author_assertions':1036,'replayed_author_UNKNOWN':50,'full_successful_producer_calls':1,'actual_saved_large_refusals_replayed':2,'files':files}
p=A/'AUDIT_SHA256.json';assert not p.exists();p.write_text(json.dumps(m,indent=2)+'\n')
for name,z in files.items():
 p=A/name;assert len(p.read_bytes())==z['bytes'] and h(p)==z['sha256'],name
for z in bindings:
 p=W/z['path'];assert len(p.read_bytes())==z['bytes'] and h(p)==z['sha256'],str(p)
for name in ['SOURCE_BOUND_ACCEPTANCE.md','WHOLE_REVIEW.md','AUDIT_SHA256.json']:
 p=A/name;print(name,len(p.read_bytes()),h(p))
print('FINAL IMMUTABLE READBACK PASS',len(files),'audit payload bindings and',len(bindings),'original source bindings; no further writes.')
