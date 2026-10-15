#!/usr/bin/env python3
"""Read-only PR92/PR93 authority, immutable-history and manifest comparison."""
from pathlib import Path
import copy,hashlib,json,subprocess,datetime
BASE='b7cada92d2eb304578be5ed974f1e44b10a89928'
A=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-pr92-audit-20261015')
B=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-direction-transport-20261015')
OUT=Path(__file__).resolve().parent
P='updates/FT-foundational-capability-20261015/'
Q='updates/FT-direction-transport-20261015/'
def git(r,*a):return subprocess.check_output(['git','-C',str(r),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def read(r,p):return json.loads((r/p).read_text())
def rows(b):return [json.loads(x) for x in b.decode().splitlines() if x.strip()]
def encoded(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def need(v,msg):
 if not v:raise ValueError(msg)
def head(r):return git(r,'rev-parse','HEAD').decode().strip()
need(head(A)=='5eb2441c93011d4fefb819b6f751f33537427dc3','PR92 head changed')
ha,hb=head(A),head(B)
need(git(A,'status','--porcelain')==b'','PR92 audit worktree not clean')
changes={}
for tag,r in [('92',A),('93',B)]:
 changes[tag]=dict(x.split('\t',1)[::-1] for x in git(r,'diff','--name-status',BASE,'HEAD').decode().splitlines())
immutable=('cards/','frontier/cards/','frontier/review_cards/','updates/','state/checkpoints/','state/branches/','technology/records/','web/pages/','evaluation/workflows/records/','mechanisms/bridges/')
old=set(git(A,'ls-tree','-r','--name-only',BASE).decode().splitlines())
old_changed=[p for p in changes['92'] if p in old and p.startswith(immutable)]
need(not old_changed,'old immutable changed: '+str(old_changed))
registry_checks=[];keysets={};keycollisions={}
for p,key in [('indexes/claims.jsonl','id'),('indexes/source_metadata.jsonl','source_id'),('frontier/CURRENT_CLAIM_STATUS.jsonl','card_id'),('frontier/OPEN_PROOF_GATES.jsonl','gate_id'),('agent/SEMANTIC_NOTICES.jsonl','notice_id'),('web/documents.jsonl','id')]:
 baseline=git(A,'show',BASE+':'+p); sets=[]
 for tag,r in [('92',A),('93',B)]:
  current=(r/p).read_bytes();need(current.startswith(baseline),'historical byte prefix altered: '+tag+':'+p)
  added=rows(current[len(baseline):]);ids=[x.get(key,x.get('id')) for x in added];need(len(ids)==len(set(ids)),'new duplicate key '+p)
  registry_checks.append({'branch':tag,'path':p,'base_bytes':len(baseline),'appended_rows':len(added),'old_byte_prefix_preserved':True})
  keysets[tag+':'+p]=ids;sets.append(set(ids))
 keycollisions[p]=sorted(sets[0]&sets[1])
array_checks=[]
for p,fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges']),('mechanisms/bridge_candidates.json',['bridges','rejected_transfers']),('web/catalog.json',[None])]:
 before=git(A,'show',BASE+':'+p); original=json.loads(before)
 branchitems=[]
 for tag,r in [('92',A),('93',B)]:
  current=read(r,p);projection=copy.deepcopy(current);adds={}
  for field in fields:
   x=original[field] if field else original;y=current[field] if field else current
   need(y[:len(x)]==x,'historical array altered: '+tag+':'+p)
   if field:projection[field]=y[:len(x)]
   else:projection=y[:len(x)]
   adds[str(field)]=len(y)-len(x)
  need(encoded(projection)==before,'historical JSON key order/format altered: '+tag+':'+p)
  array_checks.append({'branch':tag,'path':p,'old_key_order_bytes_and_array_prefix_preserved':True,'appended':adds})
  branchitems.append(current)
 if p=='indexes/agent_graph.json':
  baseids={x['id'] for x in original['nodes']}
  keycollisions[p+':new_nodes']=sorted(({x['id'] for x in branchitems[0]['nodes']}-baseids)&({x['id'] for x in branchitems[1]['nodes']}-baseids))
 if p=='mechanisms/bridge_candidates.json':
  baseids={x['id'] for f in fields for x in original[f]}
  keycollisions[p+':bridges']=sorted(({x['id'] for f in fields for x in branchitems[0][f]}-baseids)&({x['id'] for f in fields for x in branchitems[1][f]}-baseids))
source=read(A,P+'SOURCE_MANIFEST.json');package=read(A,P+'package/SOURCE_MANIFEST.json');derived=read(A,P+'DERIVED_MANIFEST.json')
need(sha((A/P/'package/SOURCE_MANIFEST.json').read_bytes())==source['campaign_manifest_sha256']=='1b953dbf369b7daec492037ab07086a52b881f3d27fd4caca75e28624fb4262b','source pin mismatch')
need(len(package['files'])==source['declared_file_count']==78 and sum(x['bytes'] for x in package['files'])==source['declared_bytes']==391572,'source count mismatch')
need(len(source['files'])==source['copied_item_count']==79,'copied item count mismatch')
available=0
for ref in source['files']:
 raw=(A/ref['preserved_path']).read_bytes();need(sha(raw)==ref['sha256'] and len(raw)==ref['bytes'],'source byte hash mismatch: '+ref['preserved_path'])
 original=Path(source['campaign_source_root'])/ref['source_path']
 if original.is_file():need(original.read_bytes()==raw,'available original differs: '+str(original));available+=1
need(len(derived['files'])==derived['file_count_excluding_this_manifest']==174,'derived count mismatch')
for ref in derived['files']:
 raw=(A/ref['path']).read_bytes();need(sha(raw)==ref['sha256'] and len(raw)==ref['bytes'],'derived snapshot hash mismatch: '+ref['path'])
manifestpath=P+'DERIVED_MANIFEST.json'
need(set(x['path'] for x in derived['files'])==set(changes['92'])-{manifestpath},'derived snapshot not exact PR92 delta excluding own manifest')
newfiles92={p for p,s in changes['92'].items() if s=='A'};newfiles93={p for p,s in changes['93'].items() if s=='A'}
addcollisions=sorted(newfiles92&newfiles93);need(not addcollisions,'add/add path collision')
need(not any(keycollisions.values()),'actual new authority key collision')
collisions={'base_revision':BASE,'pr92_head':ha,'pr93_head':hb,'pr92_changed_files':len(changes['92']),'pr93_changed_files':len(changes['93']),'shared_modified_paths':sorted(set(changes['92'])&set(changes['93'])),'added_path_collisions':addcollisions,'actual_new_authority_key_intersections':keycollisions,'exact_added_keys':keysets,'namespace_scope_issues':['PR92 validate_intake.py counts all SN-FT-* notices and expects5; combined tree has13.','PR93 validate.py counts all G-FT-* gates and expects6; combined tree has16.'],'exporter_safety':['PR92 exporter writes at module top level; do not import or rerun in checkout.','PR92 original runner writes logs and receipt into the package containing the runner; execute only a complete outside-checkout package copy.']}
(OUT/'COLLISION_AUDIT.json').write_bytes(encoded(collisions))
receipt={'schema':'astra.late-pr92.structural-tooling-review.v1','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INTEGRITY_WITH_TOOLING_LIMITATIONS','base_revision':BASE,'pr92_head':ha,'pr93_head':hb,'source_manifest_schema':source['schema'],'campaign_source_manifest_schema':package['schema'],'derived_manifest_schema':derived['schema'],'declared_source_files':78,'declared_source_bytes':391572,'copied_source_items':79,'copied_source_bytes':sum(x['bytes'] for x in source['files']),'available_originals_unchanged':available,'derived_snapshot_files':174,'derived_snapshot_covers_full_pr_delta_except_itself':True,'old_immutable_paths_changed':old_changed,'historical_immutable_paths_checked_by_git_delta':len([p for p in old if p.startswith(immutable)]),'jsonl_checks':registry_checks,'json_array_checks':array_checks,'scope':'Structural/hash/history only. Claims under separate scientific review; no mathematical or physical certification.','source_inputs':{name:sha((A/P/name).read_bytes()) for name in ['build_integration.py','validate_intake.py','SOURCE_MANIFEST.json','DERIVED_MANIFEST.json','VALIDATION_RECEIPT.json','CHECKPOINT_RECORD.json','package/root/replay_selected.py']}}
(OUT/'STRUCTURAL_RECEIPT.json').write_bytes(encoded(receipt))
print(json.dumps({k:v for k,v in receipt.items() if k not in ('jsonl_checks','json_array_checks','source_inputs')},indent=2))
print(json.dumps({'shared_paths':len(collisions['shared_modified_paths']),'actual_key_collisions':keycollisions,'add_add_collisions':addcollisions,'exact_card_ids92':keysets['92:indexes/claims.jsonl'],'exact_card_ids93':keysets['93:indexes/claims.jsonl']},indent=2))
