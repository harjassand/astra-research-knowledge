#!/usr/bin/env python3
"""Fail-closed FL history/provenance/routing checks; not scientific certification."""
from pathlib import Path
import ast,hashlib,importlib.util,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
BASE='3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d';MAIN='ace0cfc4437fe91c20ccd24d69e0ee4bb335e871'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines() if s]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
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
 source=load('updates/FL/SOURCE_MANIFEST.json');derived=load('updates/FL/DERIVED_MANIFEST.json')['files']
 need(source['main_revision']==MAIN and source['previous_pr_head']==BASE,'source pins')
 need(len(source['files'])==16 and sum(x['bytes'] for x in source['files'])==323695,'source inventory')
 need(len(derived)==128 and sum(x['bytes'] for x in derived)==969710,'derived inventory')
 for row in source['files']+derived:check(row)
 need({x['scientific_stream'] for x in source['files']}=={'global','ancestry','activation'},'semantic intake mapping')
 activation=next(x for x in source['files'] if x['path'].endswith('/temporal_PASTED_SOURCE.txt'))
 need(activation['scientific_stream']=='activation' and activation['group']=='temporal','provisional filename mapping')
 need(sha('updates/FL/INTAKE_MANIFEST.json')=='e66de8b042a3e445ec7aa35aaed63bf32440344c527ba897494034099707b9ab','initial manifest changed')
 need(sha('updates/FL/SUPPLEMENTAL_INTAKE_MANIFEST.json')=='765399e29c370fae24f3080d87ada50874536e690e76d6202a05055c7f95c913','supplement changed')
 for row in source['files']:need(Path(row['source_absolute_path']).is_absolute(),'source absolute provenance')
 for row in derived:need(Path(row['owned_original_absolute_path']).is_absolute(),'owned absolute provenance')
 need(not any(x['path'].endswith(('.pdf','.png','.html')) or '__pycache__' in x['path'] or 'site-packages' in x['path'] for x in derived),'primary paper/environment republished')
 for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','web/documents.jsonl','agent/SEMANTIC_NOTICES.jsonl','state/branches.tsv']:
  need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'not append-only:'+p)
 for p,key in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges'),('mechanisms/bridge_candidates.json','rejected_transfers')]:
  old=json.loads(git('show',BASE+':'+p))[key];need(load(p)[key][:len(old)]==old,'old sequence changed:'+p+':'+key)
 old=json.loads(git('show',BASE+':web/catalog.json'));need(load('web/catalog.json')[:len(old)]==old,'old web catalog')
 old=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in old.items()),'old aliases')
 history=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
 immutable=('state/branches/','state/checkpoints/','frontier/review_cards/','frontier/cards/','cards/','updates/','technology/records/','evaluation/workflows/records/','web/pages/')
 for p in git('diff','--name-only',BASE).decode().splitlines():need(not(p in history and p.startswith(immutable)),'prior immutable file changed:'+p)
 own=load('updates/FL/CLAIMS.json')['claims'];need(len(own)==3 and {x['id'].split('-')[0] for x in own}=={'N812','N813','N814'},'claim set')
 checked=0
 for c in own:
  st=load('frontier/cards/'+c['id']+'.json');need(st['claim_status']=='source_derived_unreviewed','status promotion')
  need(sha(st['card_path'])==st['card_sha256'],'card hash')
  need((ROOT/'frontier/dossiers'/(c['id'].split('-')[0]+'.txt')).is_file(),'missing dossier')
  need((ROOT/'web/pages'/(c['id']+'.html')).is_file(),'missing card page')
  for r in refs(st):check(r);checked+=1
 notices=load('updates/FL/SCOPED_NOTICES.json');need(len(notices)==2 and all(not x['whole_claim_invalidated'] for x in notices),'notice scope')
 bridges=load('updates/FL/BRIDGES.json')['bridges'];need(len(bridges)==8,'bridge count')
 states={'PROVEN LOGICAL DEPENDENCY','ESTABLISHED COMPATIBLE INTERFACE','CANDIDATE CONNECTION','INCOMPATIBLE ASSUMPTIONS','REFUTED TRANSFER'}
 for b in bridges:
  need(b['id'].startswith('FL_') and b['state']==b['status'] and b['state'] in states,'bridge state')
  for side in ['source_interface','destination_interface']:need(all(b[side].get(k) for k in ['objects','regime_and_quantifiers','supplied_information','acquired_information','legal_access','guarantee','units_norm_and_precision','costs']),'incomplete paired contract')
 for r in refs(notices+bridges):check(r);checked+=1
 metadata=[x for x in rows('indexes/source_metadata.jsonl') if x.get('source_id','').startswith('src-FL-')]
 need(len(metadata)==144 and {x['path'] for x in metadata}=={x['path'] for x in source['files']+derived},'indexed source set')
 for x in metadata:check(x);need((ROOT/'web/pages'/(x['source_id']+'.html')).is_file(),'missing source page')
 gates=[x for x in rows('frontier/OPEN_PROOF_GATES.jsonl') if x['gate_id'].startswith('G-FL-')]
 need(len(gates)==6 and all(x['status']=='open' and not x['completion_evidence'] for x in gates),'gate promotion')
 parsed=0
 for p in (ROOT/'updates/FL').rglob('*.py'):ast.parse(p.read_text(),filename=str(p));parsed+=1
 pub=load('updates/FL/PUBLICATION_STATUS.json');need(pub['standard_publisher_exit_code']!=0 and len(pub['individually_validated_new_checkpoints'])==1,'publication scope')
 for r in pub['inherited_records_preserved']:check(r);need(sha(r['path'])==hashlib.sha256(git('show',BASE+':'+r['path'])).hexdigest(),'inherited unsupported record changed')
 spec=importlib.util.spec_from_file_location('fl_publisher',ROOT/'state/publish_checkpoint.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for p in pub['individually_validated_new_checkpoints']:
  x=load(p);m.validate_record(x,ROOT);need(x['base_revision']==BASE and x['parent_checkpoint_ids']==[],'new checkpoint lineage')
 replay=load('updates/FL/PORTABLE_REPLAY_RECEIPT.json');need(replay['status']=='PASS' and replay['total_steps']==21,'replay scope')
 counts={}
 for r in replay['groups']:
  check(r);x=load(r['path']);need(x['status']=='PASS' and len(x['checks'])==x['expected_steps'] and all(c['exit_code']==0 for c in x['checks']),'replay group')
  need(x['published_inputs_hash_unchanged'] and x['hashed_original_and_derived_files']==144,'replay source drift');counts[x['group']]=len(x['checks'])
  for log in x['checks']:need(sha(str(Path(r['path']).parent/log['log']))==log['log_sha256'],'replay log drift')
 need(counts=={'global':8,'ancestry':9,'physical':4},'replay counts')
 joint=load('updates/FL/synthesis/root/JOINT_ANCESTRY_CHECKS.json');simple=load('updates/FL/synthesis/root/SIMPLE_BINARY_CHECKS.json')
 need(joint['status']=='PASS' and joint['checks_passed']==114 and joint['cost']['M_difference']=='9/8192','joint exact witness')
 need(joint['binary_waveforms_checked']==64 and len(joint['distinguishing_binary_waveforms'])==4,'matched grid competitor')
 need(simple['status']=='PASS' and simple['checks_passed']==329 and simple['histories']==15,'binary acquisition exact check')
 proof=(ROOT/'updates/FL/synthesis/root/JOINT_ANCESTRY_OPERATION.md').read_text();need('independent of its ancestry-pattern draw' in proof,'sampling correction omitted')
 correction=(ROOT/'updates/FL/synthesis/root/JOINT_ANCESTRY_REVIEW_CORRECTION.md').read_text();need('0.1216' in correction and '0.125' in correction,'counterexample omitted')
 need((ROOT/'updates/FL/synthesis/root/history/JOINT_ANCESTRY_DRAFT_01.md').is_file(),'former draft omitted')
 table=(ROOT/'updates/FL/synthesis/root/PHYSICAL_TABLE_REVIEW.md').read_text();need('0.020,0.004,0.005' in table and 'error was ours' in table,'table correction omitted')
 refresh=load('updates/FL/PROVENANCE_REFRESH.json');need(refresh['final_worker_manifest_validated'],'final provenance manifest')
 for row in refresh['unchanged_scientific_payloads']:check(row);need(row['unchanged'],'analytical change mislabeled')
 for row in refresh['provenance_versions']:
  need(sha(row['initial_path'])==row['initial_sha256'] and sha(row['final_path'])==row['final_sha256'],'provenance version drift')
 workers=load('updates/FL/synthesis/root/WORKER_DEPLOYMENT.json');aa=workers['initial_workers']
 need(len(aa)==15 and len({x['agent'] for x in aa})==15 and all(x['configured_model']=='gpt-6-luna' and x['reasoning_effort']=='max' and x['fork_turns']=='none' for x in aa),'worker configuration')
 need(workers['initial_concurrent_running_observation']['all15_observed_running'],'concurrency evidence absent')
 for tid,stage in [('T-joint-isotope-ancestry-functional','simulation'),('T-regenerative-molecular-work-return','model')]:
  rec=load('technology/records/'+tid+'/v0001.json');need(rec['version']==1 and rec['stage']==stage and any(x['stage']=='experiment' and x['decision']=='open' for x in rec['gates']),'technology status promotion')
 print(json.dumps(dict(status='PASS',base_revision=BASE,main_revision=MAIN,original_files=16,original_bytes=323695,derived_files=128,derived_bytes=969710,indexed_sources=144,new_cards=3,notices=2,paired_bridges=8,new_checkpoints=1,concurrent_luna_max_workers=15,portable_steps=21,syntax_checks=parsed,scoped_refs=checked,global_checkpoint_validation='Inherited schema failure retained; new record individually valid.',scientific_truth_checked=False),indent=2))
if __name__=='__main__':main()
