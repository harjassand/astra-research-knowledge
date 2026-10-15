#!/usr/bin/env python3
"""Narrow the un-copied v1 plan by excluding unrelated full old-PR patch responses."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
old=R/'root/SELECTED_FREEZE.v0001.json'
raw=old.read_bytes(); d=json.loads(raw)
banned={f'workers/fz_current_capital_audit/PR{n}_FILES.json' for n in [84,85,87,88,95]}
removed=[x for x in d['files'] if x['research_relative_path'] in banned]
assert len(removed)==5
d['files']=[x for x in d['files'] if x['research_relative_path'] not in banned]
d['previous_selection']={'path':'root/SELECTED_FREEZE.v0001.json','sha256':hashlib.sha256(raw).hexdigest(),
 'status':'pre-copy superseded selection; retained locally, not an assertion that every old planned payload is published'}
d['excluded_old_pr_patches']=[{'path':x['research_relative_path'],'bytes':x['bytes'],'sha256':x['sha256']} for x in removed]
for name in ['PUBLIC_SELECTION_DECISIONS.v0001.md','select_public_evidence.v0002.py']:
 p=R/'root'/name;b=p.read_bytes()
 d['files'].append(dict(path='updates/FZ-positive-memory-genesis-20261016/package/derived/root/'+name,
 research_relative_path='root/'+name,origin_path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),
 provenance_role='root_synthesis',payload_kind='code' if p.suffix=='.py' else 'synthesis',source_origin='root_authored',
 selection_reason='Versioned publication-selection narrowing; preserve earlier plan and unrelated old PR evidence locally.',
 provenance_note='No original or scientific proof bytes changed.',
 **{k:False for k in ['contains_external_fulltext','contains_external_dataset','contains_external_workbook','contains_external_clone','contains_runtime_cache']}))
d['total_files']=len(d['files']);d['total_bytes']=sum(x['bytes']for x in d['files'])
out=R/'root/SELECTED_FREEZE.v0002.json';b=(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode()
if out.exists():assert out.read_bytes()==b
else:out.write_bytes(b)
print(json.dumps({'files':d['total_files'],'bytes':d['total_bytes'],'sha256':hashlib.sha256(b).hexdigest(),
 'excluded_patch_bytes':sum(x['bytes']for x in removed)}))
