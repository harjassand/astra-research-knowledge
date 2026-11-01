from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parent;W=A.parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((A/'FINAL_SOURCE_BINDINGS.json').read_text());count=0
for v,x in b.items():
 S=W/x['directory'];assert h(S/'AUTHOR_MANIFEST.json')==x['manifest_sha256']
 for name,z in x['bindings'].items():
  p=S/name;assert len(p.read_bytes())==z['bytes']and h(p)==z['sha256'],str(p);count+=1
assert count==55
files={}
for p in sorted(A.rglob('*')):
 if not p.is_file()or '__pycache__'in p.parts or p.suffix=='.pyc'or p==A/'AUDIT_SHA256.json':continue
 assert not p.is_symlink()
 files[str(p.relative_to(A))]={'bytes':len(p.read_bytes()),'sha256':h(p)}
m={'schema':'common_predictable_box_independent_whole_audit.v2','verdict':'PASS exact frozen v2 and stated contract; v1 NOT_ACCEPTED_FAILURE_HISTORY','v2_author_manifest_sha256':b['v2']['manifest_sha256'],'v2_code_sha256':'774f89413ac6bf3cf2f194c82e06abe878de15b9681fb6c4d36b345f5e41a4bc','v1_author_manifest_sha256':b['v1']['manifest_sha256'],'independent_v2_assertions':22367,'expected_exception_refusals':1044,'theorem_assertions_separate':4046,'actual_author_v2_entrypoints_replayed':4,'original_source_payload_bindings':55,'files':files}
p=A/'AUDIT_SHA256.json';assert not p.exists();p.write_text(json.dumps(m,indent=2)+'\n')
for name,z in files.items():
 p=A/name;assert len(p.read_bytes())==z['bytes']and h(p)==z['sha256'],name
for v,x in b.items():
 S=W/x['directory'];assert h(S/'AUTHOR_MANIFEST.json')==x['manifest_sha256']
 for name,z in x['bindings'].items():
  p=S/name;assert len(p.read_bytes())==z['bytes']and h(p)==z['sha256'],str(p)
for name in ['SOURCE_BOUND_ACCEPTANCE.md','WHOLE_REVIEW.md','AUDIT_SHA256.json','REPLAY_INSTRUCTIONS.md']:
 p=A/name;print(name,len(p.read_bytes()),h(p))
print('FINAL IMMUTABLE READBACK PASS',len(files),'audit payload bindings;',count,'original source payload bindings unchanged. No further writes.')
