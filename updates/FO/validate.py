#!/usr/bin/env python3
"""FO append-only evidence/status checks; no scientific truth certification."""
from pathlib import Path
import ast,hashlib,importlib.util,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
BASE=MAIN='1c45f77e32d6fbd72483aed5014061c7bda4f372'
def need(x,msg):
 if not x:raise ValueError(msg)
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines() if s]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a])
def refs(x):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x:yield x
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
def check(r):
 p=r['path'];need(not Path(p).is_absolute() and (ROOT/p).resolve().is_relative_to(ROOT),'unsafe ref:'+p)
 need((ROOT/p).is_file() and sha(p)==r['sha256'],'hash drift:'+p)
 if 'bytes' in r:need((ROOT/p).stat().st_size==r['bytes'],'size drift:'+p)
 if r.get('lines'):
  a,b=r['lines'];need(1<=a<=b<=len((ROOT/p).read_text().splitlines()),'bad range:'+p)
def main():
 source=load('updates/FO/SOURCE_MANIFEST.json');derived=load('updates/FO/DERIVED_MANIFEST.json')['files']
 need(source['main_revision']==MAIN and source['previous_pr_head']==BASE,'source pins')
 need(len(source['files'])==23 and sum(x['bytes'] for x in source['files'])==165959,'source inventory')
 need(len(derived)==176 and sum(x['bytes'] for x in derived)==1396776,'selected evidence inventory')
 for r in source['files']+derived:check(r)
 need({x['scientific_stream'] for x in source['files']}=={'resonant','ancestry','physical'},'stream mapping')
 need(sha('updates/FO/INTAKE_MANIFEST.json')=='3d8a4bdbb70978074beb6bba8587c50186d2524c36759a2eafa5a1c3969d82ea','original localFMmanifest changed')
 for x in source['files']:need(Path(x['source_absolute_path']).is_absolute(),'original provenance')
 for x in derived:need(Path(x['owned_original_absolute_path']).is_absolute(),'selected provenance')
 need(not any(x['path'].endswith(('.pdf','.png','.html')) or 'site-packages' in x['path'] or '__pycache__' in x['path'] for x in derived),'primary/runtime republished')
 q=load('updates/FO/SELECTION_QUALIFICATIONS.json');need(q['selected_evidence_files']==176 and q['prior_dependency_copies']==6,'selection roles')
 for x in q['prior_hash_matches']:check(x)
 late=load('updates/FO/concurrent_PR85/SNAPSHOT_MANIFEST.json')
 need(late['revision']=='5611ad3fc9aa31b6bd09738d1831020ca4235e49' and len(late['files'])==9,'late capital pin')
 for x in late['files']:check(dict(x,path='updates/FO/concurrent_PR85/'+x['path']))
 for x in load('updates/FO/LATE_REVIEW_RECEIPT.json')['files']:check(x)
 for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','web/documents.jsonl','agent/SEMANTIC_NOTICES.jsonl','state/branches.tsv']:
  need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'not append-only:'+p)
 for p,key in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges'),('mechanisms/bridge_candidates.json','rejected_transfers')]:
  old=json.loads(git('show',BASE+':'+p))[key];need(load(p)[key][:len(old)]==old,'old sequence changed:'+p)
 old=json.loads(git('show',BASE+':web/catalog.json'));need(load('web/catalog.json')[:len(old)]==old,'old web catalog')
 old=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in old.items()),'old aliases')
 history=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
 immutable=('state/branches/','state/checkpoints/','frontier/review_cards/','frontier/cards/','cards/','updates/','technology/records/','evaluation/workflows/records/','web/pages/')
 for p in git('diff','--name-only',BASE).decode().splitlines():need(not(p in history and p.startswith(immutable)),'prior immutable changed:'+p)
 own=load('updates/FO/CLAIMS.json')['claims'];need(len(own)==3 and {x['id'].split('-')[0] for x in own}=={'N819','N820','N821'},'claim set')
 idmap=load('updates/FO/CANONICAL_ID_MAP.json');need({x['provisional_id']:x['canonical_id'] for x in idmap['mapping']}=={'N817':'N819','N818':'N820','N819':'N821'} and not idmap['scientific_change'],'canonical remap')
 import zipfile
 with zipfile.ZipFile(ROOT/'updates/FO/publication_history/PROVISIONAL_AUTHORITY.zip') as z:
  need(z.testzip() is None,'provisional archive CRC')
  old=json.loads(z.read('MANIFEST.json'))
  for f in old['files']:
   data=z.read(f['path']);need(len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256'],'provisional history drift')
 checked=0
 for c in own:
  st=load('frontier/cards/'+c['id']+'.json');need(st['claim_status']=='source_derived_unreviewed','status promotion')
  need(sha(st['card_path'])==st['card_sha256'],'card hash')
  need((ROOT/'frontier/dossiers'/(c['id'].split('-')[0]+'.txt')).is_file(),'dossier missing')
  need((ROOT/'web/pages'/(c['id']+'.html')).is_file(),'card page missing')
  need((ROOT/c['checkpoint']).is_file(),'canonical checkpoint pointer')
  for r in refs(st):check(r);checked+=1
 notices=load('updates/FO/SCOPED_NOTICES.json');need(len(notices)==3 and all(not x['whole_claim_invalidated'] for x in notices),'notice scope')
 bridges=load('updates/FO/BRIDGES.json')['bridges'];need(len(bridges)==8,'bridge count')
 states={'PROVEN LOGICAL DEPENDENCY','ESTABLISHED COMPATIBLE INTERFACE','CANDIDATE CONNECTION','INCOMPATIBLE ASSUMPTIONS','REFUTED TRANSFER'}
 for b in bridges:
  need(b['id'].startswith('FO_') and b['state']==b['status'] and b['state'] in states,'bridge state')
  for side in ['source_interface','destination_interface']:need(all(b[side].get(k) for k in ['objects','regime_and_quantifiers','supplied_information','acquired_information','legal_access','guarantee','units_norm_and_precision','costs']),'incomplete contract')
 for r in refs(notices+bridges):check(r);checked+=1
 metadata=[x for x in rows('indexes/source_metadata.jsonl') if x.get('source_id','').startswith('src-FO-')]
 need(len(metadata)==199 and {x['path'] for x in metadata}=={x['path'] for x in source['files']+derived},'source index set')
 for x in metadata:check(x);need((ROOT/'web/pages'/(x['source_id']+'.html')).is_file(),'source page missing')
 gates=[x for x in rows('frontier/OPEN_PROOF_GATES.jsonl') if x['gate_id'].startswith('G-FO-')]
 need(len(gates)==6 and all(x['status']=='open' and not x['completion_evidence'] for x in gates),'gate promotion')
 parsed=0
 for p in (ROOT/'updates/FO').rglob('*.py'):ast.parse(p.read_text(),filename=str(p));parsed+=1
 pub=load('updates/FO/PUBLICATION_STATUS.json');need(pub['standard_publisher_exit_code']!=0 and len(pub['individually_validated_new_checkpoints'])==1,'publication scope')
 for r in pub['inherited_records_preserved']:check(r);need(sha(r['path'])==hashlib.sha256(git('show',BASE+':'+r['path'])).hexdigest(),'inherited record changed')
 spec=importlib.util.spec_from_file_location('fo_pub',ROOT/'state/publish_checkpoint.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for p in pub['individually_validated_new_checkpoints']:
  x=load(p);m.validate_record(x,ROOT);need(x['base_revision']==BASE and x['parent_checkpoint_ids']==[],'new lineage')
 replay=load('updates/FO/PORTABLE_REPLAY_RECEIPT.json');need(replay['status']=='PASS' and replay['total_steps']==23,'replay scope')
 counts={}
 for r in replay['groups']:
  check(r);x=load(r['path']);need(x['status']=='PASS' and len(x['checks'])==x['expected_steps'] and all(z['exit_code']==0 for z in x['checks']),'replay group')
  need(x['published_inputs_hash_unchanged'] and x['hashed_original_and_derived_files']==199,'input drift');counts[x['group']]=len(x['checks'])
  for z in x['checks']:need(sha(str(Path(r['path']).parent/z['log']))==z['log_sha256'],'replay log drift')
 need(counts=={'math':12,'chemical':3,'physical':7,'response':1},'replay counts')
 repair=load('updates/FO/REPLAY_ADAPTER_REPAIR.json');check(repair['initial_receipt']);check(repair['final_receipt'])
 need(load(repair['initial_receipt']['path'])['status']=='FAIL','initial adapter failure lost')
 root=load('updates/FO/synthesis/root/CONTINUUM_STORAGE_CHECKS.json');need(root['status']=='PASS' and root['group_count']==7,'root exact algebra')
 mf=load('updates/FO/synthesis/root/MULTIFREQUENCY_STORAGE_CHECK.json');need(mf['exact_negative'] and mf['exact_margin']=='-183426997/480000000','crossfrequency scope witness')
 workers=load('updates/FO/synthesis/root/WORKER_DEPLOYMENT.json');aa=workers['initial_workers']
 need(len(aa)==15 and len({x['agent'] for x in aa})==15 and all(x['configured_model']=='gpt-6-luna' and x['reasoning_effort']=='max' and x['fork_turns']=='none' for x in aa),'worker config')
 need(workers['initial_concurrent_running_observation']['all15_observed_running'],'concurrency evidence')
 for tid in ['T-chemical-state-targeted-decision','T-phase-selective-retained-polarity']:
  rec=load('technology/records/'+tid+'/v0001.json');need(rec['version']==1 and rec['stage']=='model' and all(any(x['stage']==s and x['decision']=='open' for x in rec['gates']) for s in ['simulation','experiment']),'tech promotion')
 print(json.dumps(dict(status='PASS',base_revision=BASE,original_files=23,original_bytes=165959,selected_evidence_files=176,selected_evidence_bytes=1396776,indexed_sources=199,prior_dependency_copies=6,new_cards=3,notices=3,paired_bridges=8,new_checkpoints=1,concurrent_luna_max_workers=15,portable_steps=23,syntax_checks=parsed,scoped_refs=checked,global_checkpoint_validation='Inherited schema failure retained; new record individually valid.',scientific_truth_checked=False),indent=2))
if __name__=='__main__':main()
