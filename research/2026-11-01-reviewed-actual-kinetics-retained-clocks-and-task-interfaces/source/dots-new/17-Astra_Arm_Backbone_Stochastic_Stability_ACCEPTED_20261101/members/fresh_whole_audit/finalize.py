from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;b=json.loads((R/'INPUT_BINDING.json').read_text());s=Path(b['source'])
for name,w in b['files'].items():
 data=(s/name).read_bytes();assert len(data)==w['bytes']and hashlib.sha256(data).hexdigest()==w['sha256'],name
assert hashlib.sha256((s/'frozen_aggregate/fresh_whole_audit/FINAL_AUDIT_MANIFEST.json').read_bytes()).hexdigest()=='8231fb76e53b66eb6eddd21616eea47abefe8d7c42a8d559b5f3f315661865a0'
assert hashlib.sha256((s/'frozen_aggregate/MANIFEST.json').read_bytes()).hexdigest()=='3c060bc10571183f743b6c588a7f1ebddae5dd2ce207e1f17cd2877e17d47c8f'
prior={}
for p in sorted((R/'retained').rglob('*.py')):
 rel=p.relative_to(R/'retained');src=s/'frozen_aggregate/fresh_whole_audit'/rel
 assert p.read_bytes()==src.read_bytes(),str(rel)
 prior[str(p.relative_to(R))]={'source':str(src.relative_to(s)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(R/'RETAINED_BINDING.json').write_text(json.dumps({'status':'EXPLICIT_PRIMITIVE_REUSE_NOT_EXTENSION_ACCEPTANCE','files':prior},indent=2)+'\n')
for fn in ('COMPONENT_RESULTS.json','RAW_RESULTS.json','RECEIVING_RESULTS.json','STAGED_REPLAY.json'):
 assert json.loads((R/fn).read_text())['status'].startswith('PASS')
for p in R.rglob('*stderr*'):assert p.stat().st_size==0,p
stage=Path(json.loads((R/'STAGED_REPLAY.json').read_text())['stage_dir'])/'audit'
for name in ('independent_backbone.py','fixtures.py','check_components.py','check_raw.py','check_receiving.py'):
 assert (R/name).read_bytes()==(stage/name).read_bytes(),name
summary=dict(status='SCOPED_NEW_RECOVERY_WHOLE_PASS',source_manifest_sha256='f900821ba07bc39259ab0fe3acf43874e7be0e9e4568f594d5e7c6178e489010',review_binding_sha256='b08ae3e6d710de1b80c140fa5fc86847142a0ede8da32b39105a670ce500a76f',source_entries=155,bound_file_union=158,frozen_source_unchanged=True,old_c606_source_acceptance=False,old_partial_review_promoted=False,substantive_defects_found=0,source_repairs=0,main_receipt_sha256='27ecb8f421997598b89b2c0089ba9c809b99b5cb41652ac1f9f900b2bdff791f',main_bytes=1351442,production_receipt_sha256='181979210f47b93a7d8b8e21a2b726ae0f5161360ae2a5b8397901df61619442',production_bytes=150663,main_K=60092953097452439556,actual_mass_head_expanded=False,actual_global_head_expanded=False,actual_stationary_bound_expanded=False,scope='Canonical armed-hub backbone with arbitrary amplification-only detours, plus core-only route; arbitrary positive real rates. Not general WR, complete finder, practical tail, historical novelty or source-process clearance.',no_fresh_scientific_retrieval=True)
(R/'AUDIT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
names=sorted(str(p.relative_to(R))for p in R.rglob('*')if p.is_file()and p.name not in('FINAL_AUDIT_MANIFEST.json','ARTIFACT_ALLOWLIST.json')and '__pycache__'not in p.parts)
names=sorted(names+['ARTIFACT_ALLOWLIST.json','FINAL_AUDIT_MANIFEST.json'])
(R/'ARTIFACT_ALLOWLIST.json').write_text(json.dumps({'members':names,'count':len(names),'scope':'Strict current audit artifacts only; no historical lost audit bytes or scratch sources'},indent=2)+'\n')
files={}
for name in names:
 if name=='FINAL_AUDIT_MANIFEST.json':continue
 data=(R/name).read_bytes();files[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(R/'FINAL_AUDIT_MANIFEST.json').write_text(json.dumps(dict(**summary,files=files),indent=2)+'\n')
for name in ('WHOLE_PROOF_CODE_AUDIT.md','ARTIFACT_ALLOWLIST.json','FINAL_AUDIT_MANIFEST.json'):
 print(name,hashlib.sha256((R/name).read_bytes()).hexdigest())
print('strict members',len(names),'manifest-bound artifacts',len(files))
