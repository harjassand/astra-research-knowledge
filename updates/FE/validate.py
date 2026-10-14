#!/usr/bin/env python3
"""Fail-closed FE source/history/routing audit. Never certifies scientific truth."""
from pathlib import Path
import ast,hashlib,importlib.util,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
BASE='c4d92096c818c0f07b2815e26148827d40b42c0f'
MAIN='ace0cfc4437fe91c20ccd24d69e0ee4bb335e871'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines() if s]
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a])
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def refs(o):
 if isinstance(o,dict):
  if 'path' in o and 'sha256' in o:yield o
  for v in o.values():yield from refs(v)
 elif isinstance(o,list):
  for v in o:yield from refs(v)
def check(r):
 p=r['path'];need(not Path(p).is_absolute() and (ROOT/p).resolve().is_relative_to(ROOT),'unsafe reference:'+p)
 need((ROOT/p).is_file() and sha(p)==r['sha256'],'hash mismatch:'+p)
 if 'bytes' in r:need((ROOT/p).stat().st_size==r['bytes'],'size mismatch:'+p)
 if r.get('lines'):
  a,b=r['lines'];need(1<=a<=b<=len((ROOT/p).read_text().splitlines()),'bad line range:'+p)

def main():
 sources=load('updates/FE/SOURCE_MANIFEST.json');need(sources['main_revision']==MAIN and sources['previous_pr_head']==BASE,'pin mismatch')
 need(len(sources['files'])==47 and sum(x['bytes'] for x in sources['files'])==2642902,'original inventory drift')
 for r in sources['files']:check(r);need(Path(r['source_absolute_path']).is_absolute(),'missing original provenance')
 derived=load('updates/FE/DERIVED_MANIFEST.json')['files'];need(len(derived)==76,'derived inventory drift')
 for r in derived:check(r)
 # Exact old line streams and authority sequences are retained.
 for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','web/documents.jsonl','agent/SEMANTIC_NOTICES.jsonl','state/branches.tsv']:
  need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'not append-only:'+p)
 for p,k in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges'),('mechanisms/bridge_candidates.json','rejected_transfers')]:
  old=json.loads(git('show',BASE+':'+p))[k];need(load(p)[k][:len(old)]==old,'historical sequence changed:'+p+':'+k)
 old=json.loads(git('show',BASE+':web/catalog.json'));need(load('web/catalog.json')[:len(old)]==old,'historical web catalog changed')
 old=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in old.items()),'historical aliases changed')
 historical=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines());immutable=('cards/','frontier/cards/','state/checkpoints/','technology/records/','evaluation/workflows/records/','updates/','web/pages/')
 for p in git('diff','--name-only',BASE).decode().splitlines():need(not(p in historical and p.startswith(immutable)),'old immutable file changed:'+p)
 own=load('updates/FE/CLAIMS.json')['claims'];need(len(own)==3,'new claim count');count=0
 for c in own:
  st=load('frontier/cards/'+c['id']+'.json');need(st['claim_status']=='source_derived_unreviewed','status promotion')
  need(sha(st['card_path'])==st['card_sha256'],'card hash')
  need((ROOT/'frontier/dossiers'/str(c['id'].split('-')[0]+'.txt')).is_file(),'missing dossier')
  need((ROOT/'web/pages'/str(c['id']+'.html')).is_file(),'missing card page')
  for r in refs(st):check(r);count+=1
 ns=load('updates/FE/SCOPED_NOTICES.json');bs=load('updates/FE/BRIDGES.json')['bridges']
 need(len(ns)==3 and all(x['whole_claim_invalidated'] is False for x in ns),'notice scope')
 need(len(bs)==8,'bridge scope');states={'PROVEN LOGICAL DEPENDENCY','ESTABLISHED COMPATIBLE INTERFACE','CANDIDATE CONNECTION','INCOMPATIBLE ASSUMPTIONS','REFUTED TRANSFER'}
 for b in bs:
  need(b['state']==b['status'] and b['state'] in states,'bridge state')
  for side in ['source_interface','destination_interface']:
   need(all(b[side].get(k) for k in ['objects','regime_and_quantifiers','supplied_information','acquired_information','legal_access','guarantee','units_norm_and_precision','costs']),'incomplete paired contract')
 for r in refs(ns+bs):check(r);count+=1
 metadata=[x for x in rows('indexes/source_metadata.jsonl') if x.get('source_id','').startswith('src-FE-')]
 need(len(metadata)==123,'indexed evidence count')
 for r in metadata:check(r);need((ROOT/'web/pages'/str(r['source_id']+'.html')).is_file(),'missing evidence page')
 need(all(x['status']=='open' and not x['completion_evidence'] for x in rows('frontier/OPEN_PROOF_GATES.jsonl') if x['gate_id'].startswith('G-FE-')),'unjustified open-gate closure')
 parsed=0
 for p in (ROOT/'updates/FE').rglob('*.py'):ast.parse(p.read_text(),filename=str(p));parsed+=1
 pub=load('updates/FE/PUBLICATION_STATUS.json');need(pub['standard_publisher_exit_code']!=0 and len(pub['individually_validated_new_checkpoints'])==1,'publisher boundary')
 for r in pub['inherited_records_preserved']:
  check(r);need(sha(r['path'])==hashlib.sha256(git('show',BASE+':'+r['path'])).hexdigest(),'old malformed checkpoint changed')
 spec=importlib.util.spec_from_file_location('fe_publisher',ROOT/'state/publish_checkpoint.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for p in pub['individually_validated_new_checkpoints']:
  x=load(p);m.validate_record(x,ROOT);need(x['base_revision']==BASE and x['parent_checkpoint_ids']==[],'new lineage')
 portable=load('updates/FE/PORTABLE_REPLAY_RECEIPT.json');need(portable['status']=='PASS' and portable['total_scripts']==11,'portable replay scope')
 for r in portable['groups']:
  check(r);receipt=load(r['path']);need(receipt['status']=='PASS' and all(x['exit_code']==0 for x in receipt['checks']),'portable replay failure')
  for log in receipt['checks']:
   p=str(Path(r['path']).parent/log['log']);need(sha(p)==log['log_sha256'],'replay log mismatch')
 print(json.dumps(dict(status='PASS',base_revision=BASE,main_revision=MAIN,original_files=47,original_bytes=2642902,
   derived_files=len(derived),indexed_sources=len(metadata),new_cards=3,scoped_notices=3,paired_bridges=8,new_checkpoints=1,
   python_syntax_checks=parsed,scoped_evidence_refs=count,portable_replay_scripts=11,
   global_checkpoint_validation='inherited unsupported-schema failure preserved;not passed',scientific_truth_checked=False),indent=2))

if __name__=='__main__':main()
