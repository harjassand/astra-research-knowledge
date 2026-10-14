#!/usr/bin/env python3
"""Fail-closed FH source/history/routing audit. Never certifies scientific truth."""
from pathlib import Path
import ast,hashlib,importlib.util,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
BASE='74a1ab09ba75324bc3d2a14f05ce6196f43ffd77'
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
 sources=load('updates/FH/SOURCE_MANIFEST.json');need(sources['main_revision']==MAIN and sources['previous_pr_head']==BASE,'pin mismatch')
 need(len(sources['files'])==76 and sum(x['bytes'] for x in sources['files'])==1350816,'original inventory drift')
 for r in sources['files']:check(r);need(Path(r['source_absolute_path']).is_absolute(),'missing original provenance')
 derived=load('updates/FH/DERIVED_MANIFEST.json')['files'];need(len(derived)==105,'derived inventory drift')
 for r in derived:check(r)
 # Exact old line streams and authority sequences are retained.
 for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','web/documents.jsonl','agent/SEMANTIC_NOTICES.jsonl','state/branches.tsv']:
  need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'not append-only:'+p)
 for p,k in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges'),('mechanisms/bridge_candidates.json','rejected_transfers')]:
  old=json.loads(git('show',BASE+':'+p))[k];need(load(p)[k][:len(old)]==old,'historical sequence changed:'+p+':'+k)
 old=json.loads(git('show',BASE+':web/catalog.json'));need(load('web/catalog.json')[:len(old)]==old,'historical web catalog changed')
 old=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in old.items()),'historical aliases changed')
 historical=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines());immutable=('state/branches/','frontier/review_cards/','cards/','frontier/cards/','state/checkpoints/','technology/records/','evaluation/workflows/records/','updates/','web/pages/')
 for p in git('diff','--name-only',BASE).decode().splitlines():need(not(p in historical and p.startswith(immutable)),'old immutable file changed:'+p)
 own=load('updates/FH/CLAIMS.json')['claims'];need(len(own)==3,'new claim count');count=0
 for c in own:
  st=load('frontier/cards/'+c['id']+'.json');need(st['claim_status']=='source_derived_unreviewed','status promotion')
  need(sha(st['card_path'])==st['card_sha256'],'card hash')
  need((ROOT/'frontier/dossiers'/str(c['id'].split('-')[0]+'.txt')).is_file(),'missing dossier')
  need((ROOT/'web/pages'/str(c['id']+'.html')).is_file(),'missing card page')
  for r in refs(st):check(r);count+=1
 ns=load('updates/FH/SCOPED_NOTICES.json');bs=load('updates/FH/BRIDGES.json')['bridges']
 need(len(ns)==2 and all(x['whole_claim_invalidated'] is False for x in ns),'notice scope')
 need(len(bs)==9,'bridge scope');states={'PROVEN LOGICAL DEPENDENCY','ESTABLISHED COMPATIBLE INTERFACE','CANDIDATE CONNECTION','INCOMPATIBLE ASSUMPTIONS','REFUTED TRANSFER'}
 for b in bs:
  need(b['state']==b['status'] and b['state'] in states,'bridge state')
  for side in ['source_interface','destination_interface']:
   need(all(b[side].get(k) for k in ['objects','regime_and_quantifiers','supplied_information','acquired_information','legal_access','guarantee','units_norm_and_precision','costs']),'incomplete paired contract')
 for r in refs(ns+bs):check(r);count+=1
 metadata=[x for x in rows('indexes/source_metadata.jsonl') if x.get('source_id','').startswith('src-FH-')]
 need(len(metadata)==181,'indexed evidence count')
 for r in metadata:check(r);need((ROOT/'web/pages'/str(r['source_id']+'.html')).is_file(),'missing evidence page')
 need(all(x['status']=='open' and not x['completion_evidence'] for x in rows('frontier/OPEN_PROOF_GATES.jsonl') if x['gate_id'].startswith('G-FH-')),'unjustified open-gate closure')
 parsed=0
 for p in (ROOT/'updates/FH').rglob('*.py'):ast.parse(p.read_text(),filename=str(p));parsed+=1
 pub=load('updates/FH/PUBLICATION_STATUS.json');need(pub['standard_publisher_exit_code']!=0 and len(pub['individually_validated_new_checkpoints'])==1,'publisher boundary')
 for r in pub['inherited_records_preserved']:
  check(r);need(sha(r['path'])==hashlib.sha256(git('show',BASE+':'+r['path'])).hexdigest(),'old malformed checkpoint changed')
 spec=importlib.util.spec_from_file_location('fh_publisher',ROOT/'state/publish_checkpoint.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for p in pub['individually_validated_new_checkpoints']:
  x=load(p);m.validate_record(x,ROOT);need(x['base_revision']==BASE and x['parent_checkpoint_ids']==[],'new lineage')
 portable=load('updates/FH/PORTABLE_REPLAY_RECEIPT.json');need(portable['status']=='PASS' and portable['total_steps']==13,'portable replay scope')
 for r in portable['groups']:
  check(r);receipt=load(r['path']);need(receipt['status']=='PASS' and all(x['exit_code']==0 and x.get('integer_output_equal') is not False for x in receipt['checks']),'portable replay failure')
  for log in receipt['checks']:
   p=str(Path(r['path']).parent/log['log']);need(sha(p)==log['log_sha256'],'replay log mismatch')
 # Preserved ZIPs are the exact source of every indexed extracted member.
 import zipfile
 archives={r['group']:r for r in sources['files'] if r['kind']=='original_archive'}
 members=0
 for group,a in archives.items():
  with zipfile.ZipFile(ROOT/a['path']) as z:
   need(z.testzip() is None,'ZIP CRC failure:'+group)
   for r in sources['files']:
    if r['group']==group and r['kind']=='archive_member':
     need(z.read(r['archive_member'])==(ROOT/r['path']).read_bytes(),'ZIP/member mismatch:'+r['path']);members+=1
 need(members==70,'archive member count')
 for tid,version in [('T-completion-directed-kinetic-acquisition',3),('T-static-matched-spectral-substitution',1)]:
  t=load('technology/records/'+tid+'/v'+str(version).zfill(4)+'.json')
  if version>1:check(t['previous'])
  need(t['version']==version and t['stage']=='simulation' and any(g['stage']=='experiment' and g['decision']=='open' for g in t['gates']),'unjustified technology promotion')
 a=load('updates/FH/synthesis/root/GRAPH_ACQUISITION_RESULTS.json')
 need(a['status']=='PASS' and a['cases']==260 and a['source_n24_queries']==210 and a['source_n24_pairwise_queries']==301 and a['source_n24_proven_bound']==265,'acquisition scope')
 c=load('updates/FH/synthesis/root/ACQUIRED_RETAINED_WITNESS_RECEIPT.json')
 from fractions import Fraction
 need(c['status']=='PASS' and c['trial_states']==554 and c['residual_support']==10178 and Fraction(c['upper_exact'])/Fraction(c['lower_exact'])<Fraction(11,10),'certificate scope')
 d=load('updates/FH/synthesis/root/NEAR_FACE_DEFLATION_RESULTS.json')
 need(d['status']=='PASS' and d['minimum_at_eps_zero']=='1/4' and d['residual_example']['null_load_rejected'] is True,'near-face scope')
 d=load('updates/FH/synthesis/escape/replay/independent_checks.json')
 need(d['higher_order_energy_countermodel']['hidden_mean_exceeds_baseline_certificate'] is True and d['clock_countermodel']['same_energy_law_and_queries'] is True,'countermodel scope')
 ledger=load('updates/FH/synthesis/root/READ_AND_PRIMARY_LEDGER.json')
 need(ledger['worker_configuration']['configured_model']=='gpt-6-luna' and ledger['worker_configuration']['reasoning_effort']=='max' and ledger['worker_configuration']['workers']==4,'worker contract')
 need(not any('site-packages' in x['path'] or '__pycache__' in x['path'] for x in derived),'environment/cache in owned synthesis')
 print(json.dumps(dict(status='PASS',base_revision=BASE,main_revision=MAIN,original_files=76,original_bytes=1350816,
   verified_archive_members=members,derived_files=len(derived),indexed_sources=len(metadata),new_cards=3,scoped_notices=2,paired_bridges=9,new_checkpoints=1,
   python_syntax_checks=parsed,scoped_evidence_refs=count,portable_replay_steps=13,
   global_checkpoint_validation='inherited unsupported-schema failure preserved;not passed',scientific_truth_checked=False),indent=2))

if __name__=='__main__':main()
