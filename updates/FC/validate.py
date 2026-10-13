#!/usr/bin/env python3
"""FC integrity/scope/append-only checks. Does not validate scientific truth."""
import ast,copy,hashlib,json,stat,subprocess,sys
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[2]
BASE='b34e22e8f8ef8bd853595952fcbd9c74c5ace306'
sys.path.insert(0,str(ROOT))
from state.publish_checkpoint import validate_record,views
from technology.validate import validate as validate_tech
from evaluation.workflow_trace import validate as validate_trace

def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(l) for l in (ROOT/p).read_text().splitlines() if l.strip()]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def check_ref(r):
 need(sha(r['path'])==r['sha256'],'reference SHA changed: '+r['path'])
 if r.get('lines'):
  a,b=r['lines'];need(1<=a<=b<=len((ROOT/r['path']).read_text().splitlines()),'bad inclusive evidence range: '+r['path'])

def main():
 m=load('updates/FC/SOURCE_MANIFEST.json');need(m['base_revision']==BASE and m['missing_artifacts']==[],'source pin/availability changed')
 orig=m['original_files'];need(len(orig)==31 and sum(x['bytes'] for x in orig)==263279,'source inventory changed')
 pins={'collision_dual': 'f0ca383ee364c7722bcb715d9ca6ef31b266b496398f8798c10179f25b0bdcf3', 'nongaussian_design': '23e113c326a737ebc4b0e134f506336521fa64f651d87ea7a4a257397aff4db8', 'phonon_addressing': '9a1687d2ac3ca8643fc0ce0bb057f246061bd67ed75b64efc52ee4612dc40aea'}
 for slug,h in pins.items():need(sha('updates/FC/package/'+slug+'/ORIGINAL_PASTED_SOURCE.txt')==h,'paste changed')
 need(len(m['input_receipts'])==6,'input/dependency provenance lost')
 derived=load('updates/FC/DERIVED_MANIFEST.json')['records'];need(len(derived)==70,'new proof/replay inventory changed')
 py=0
 for v in orig+derived:
  need(sha(v['path'])==v['sha256'] and (ROOT/v['path']).stat().st_size==v['bytes'],'artifact bytes changed: '+v['path'])
  if 'lines' in v:need(len((ROOT/v['path']).read_text().splitlines())==v['lines'],'line count changed')
  if v['path'].endswith('.py'):ast.parse((ROOT/v['path']).read_bytes(),filename=v['path']);py+=1
 hashes=members=0
 for b in m['archives']:
  need(sha(b['path'])==b['sha256'],'ZIP bytes changed')
  with ZipFile(ROOT/b['path']) as z:
   need(z.testzip() is None and len(z.infolist())==b['members'],'CRC/members changed');members+=b['members']
   ns=z.namelist();need(len(ns)==len(set(ns)),'duplicate ZIP members');dest=ROOT/Path(b['path']).parent/'recovered'
   for entry in z.infolist():
    p=PurePosixPath(entry.filename);need(not p.is_absolute() and '..' not in p.parts and not stat.S_ISLNK(entry.external_attr>>16),'unsafe ZIP path')
    if not entry.is_dir():need((dest/entry.filename).read_bytes()==z.read(entry),'recovered member changed')
   if b['producer_manifest'] is None:
    need(b['producer_hashes_checked']==0,'invented producer manifest');continue
   mn=b['producer_manifest'];prefix=str(PurePosixPath(mn).parent);prefix='' if prefix=='.' else prefix+'/'
   if mn.endswith('.json'):
    raw=json.loads(z.read(mn));p=raw.get('files',raw)
    pp={x.get('name',x.get('path')):x for x in p} if isinstance(p,list) else p
   else:pp={line.split(maxsplit=1)[1].lstrip('*'):line.split(maxsplit=1)[0] for line in z.read(mn).decode().splitlines() if line.strip()}
   need(len(pp)==b['producer_hashes_checked'],'producer hash coverage changed')
   for name,pin in pp.items():
    data=z.read(prefix+name);h=pin.get('sha256') if isinstance(pin,dict) else pin
    need(hashlib.sha256(data).hexdigest()==h,'producer hash mismatch')
    if isinstance(pin,dict) and 'bytes' in pin:need(len(data)==pin['bytes'],'producer byte length mismatch')
   hashes+=len(pp)
 need(hashes==20 and members==26,'archive totals changed')
 maps=load('updates/FC/CLAIMS.json')['claims'];need(len(maps)==4,'claim count')
 ledger={s['card_id']:s for s in rows('frontier/CURRENT_CLAIM_STATUS.jsonl')};cl={s['id']:s for s in rows('indexes/claims.jsonl')}
 cat={s['id']:s for s in load('indexes/agent_catalog.json')['claims']};web={s['id']:s for s in load('web/catalog.json')};gates=rows('frontier/OPEN_PROOF_GATES.jsonl');proofs=traces=0
 for q in maps:
  cid=q['id'];s=load('frontier/cards/'+cid+'.json')
  need(s==ledger[cid] and s['claim_status']==cl[cid]['status']=='source_derived_unreviewed','scientific promotion/mismatch')
  need(sha(s['card_path'])==s['card_sha256']==cat[cid]['card_sha256'],'card hash mismatch')
  need(cl[cid]['source_paths']==web[cid]['source_paths'] and cl[cid]['source_ids']==web[cid]['source_ids'],'web provenance mismatch')
  need(cl[cid]['depends_on']==[d['target'] for d in s['depends_on']]==cat[cid]['dependencies']['depends_on'],'dependency mismatch')
  need(s['validation']['external_correctness']==s['validation']['historical_priority']=='UNKNOWN','external validation invented')
  need(s['supersedes']==s['invalidates']==[],'unscoped supersession/invalidation')
  for r in s['proof_availability']['located_proof_sources']+s['proof_availability']['available_evidence_sources']:check_ref(r)
  proofs+=len(s['proof_availability']['located_proof_sources'])
  cg=[g for g in gates if g['gate_id'].startswith('G-FC-') and cid in g['card_ids']]
  need(len(cg)==2 and all(g['status']=='open' and not g['completion_evidence'] for g in cg),'open scientific gates promoted')
  for topic in s['topics']:
   p='agent/topics/'+topic+'.tsv';data=(ROOT/p).read_text();need(data.startswith(git('show',BASE+':'+p).decode()),'historical topic bytes rewritten')
   need(sum(l.startswith(cid+'\t') for l in data.splitlines())==1,'topic route missing/duplicated')
   need(topic+': '+p+' ('+str(len(data.splitlines())-1)+' cards)' in (ROOT/'agent/topics.txt').read_text(),'topic count stale')
  cp=load(q['checkpoint']);validate_record(cp,ROOT);need(cp['base_revision']==BASE and cp['parent_checkpoint_ids']==[],'new ancestry guessed')
  vs=views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}});p='state/branches/'+cp['branch_id']+'.txt';need((ROOT/p).read_text()==vs[p],'new branch view stale')
  row=next(l for l in vs['state/branches.tsv'].splitlines() if l.startswith(cp['branch_id']+'\t'));need((ROOT/'state/branches.tsv').read_text().splitlines().count(row)==1,'new branch registry row mismatch')
  if q['workflow_trace']:
   tr=load(q['workflow_trace']);validate_trace(tr,ROOT);traces+=1
   need(tr['mode']==tr['context']['conversation_relation']=='UNKNOWN','retained context inferred')
   need(all(x is None for x in tr['model'].values()) and all(x is None for x in tr['resources']['usage'].values()),'aggregate unobserved model/usage inferred')
 need(traces==3,'workflow observation count changed')
 bs=load('updates/FC/BRIDGES.json')['bridges'];need(len(bs)==18,'bridge count')
 canonical={x['id']:x for x in load('mechanisms/bridge_candidates.json')['bridges']}
 for b in bs:
  need(b==canonical[b['id']] and b['state']==b['status'],'bridge mismatch')
  need(all(k in b for k in ['source_interface','destination_interface','missing_lemma','cost','evidence_refs']),'paired bridge incomplete')
  for r in b['evidence_refs']:check_ref(r)
 for p,stage in [('T-finite-mark-collision-sampling/v0001.json','simulation'),('T-coupled-equilibrium-design-certificates/v0001.json','simulation'),('T-phonon-recoil-sublattice-addressing/v0001.json','opportunity')]:
  t=load('technology/records/'+p);validate_tech(t,ROOT)
  need(t['stage']==stage,'capability readiness promoted')
  if stage=='simulation':need(any(g['stage']=='experiment' and g['decision']=='open' for g in t['gates']),'independent acquired-operation gate promoted')
 for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','agent/SEMANTIC_NOTICES.jsonl','agent/routes.tsv','state/branches.tsv','web/documents.jsonl']:
  need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'historical ledger bytes changed: '+p)
 for p,k in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges')]:
  before=json.loads(git('show',BASE+':'+p))[k];need(load(p)[k][:len(before)]==before,'historical semantic entry changed')
 before=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in before.items()),'historical aliases changed')
 before=json.loads(git('show',BASE+':web/catalog.json'));need(load('web/catalog.json')[:len(before)]==before,'historical web entries changed')
 historical=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines());immutable=('cards/','frontier/cards/','state/checkpoints/','technology/records/','evaluation/workflows/records/','updates/')
 for p in git('diff','--name-only',BASE).decode().splitlines():need(not(p in historical and p.startswith(immutable)),'historical immutable object changed: '+p)
 publication=load('updates/FC/PUBLICATION_STATUS.json');need(publication['standard_publisher_exit_code']!=0 and len(publication['individually_validated_new_checkpoints'])==4,'publisher/fallback scope misreported')
 for r in publication['inherited_records_preserved']:need(sha(r['path'])==r['sha256']==hashlib.sha256(git('show',BASE+':'+r['path'])).hexdigest(),'malformed historical checkpoint changed')
 audit=load('updates/FC/DECODER_REUSE_AUDIT.json')
 need(audit['base_revision']==BASE and len(audit['inputs'])==4,'decoder reuse coverage')
 need(subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',audit['prior_merge'],BASE],capture_output=True).returncode==0,'decoder prior merge not ancestor')
 for entry in audit['inputs']:
  need(entry['byte_identical'] and sha(entry['existing_path'])==entry['sha256'],'decoder source changed')
  for alias in entry['existing_identical_aliases']:need(sha(alias)==entry['sha256'],'decoder alias changed')
  need(hashlib.sha256(git('show',BASE+':'+entry['existing_path'])).hexdigest()==entry['sha256'],'decoder baseline changed')
 aliases=load('updates/FC/DIRECTORY_ALIAS_AUDIT.json');need(len(aliases['directories'])==2,'directory alias count')
 for directory in aliases['directories']:
  need(directory['exact_membership_match'] and directory['byte_identical'] and len(directory['files'])==11,'directory alias scope changed')
  for entry in directory['files']:need(sha(entry['existing_path'])==entry['sha256'] and (ROOT/entry['existing_path']).stat().st_size==entry['bytes'],'directory alias bytes changed')
 observations=load('updates/FC/REPORTED_WORKFLOW_OBSERVATIONS.json')['observations']
 need([o['reported_ui_elapsed_work_seconds'] for o in observations]==[3450,3793,3108],'source UI duration changed')
 for observation in observations:
  need(observation['pure_inference_seconds'] is None and observation['aggregate_usage']=='UNKNOWN','UI elapsed conflated with inference/usage');check_ref(observation['source_ref'])
 for q in maps:
  if q['workflow_trace']:need(load(q['workflow_trace'])['resources']['reported_inference_seconds'] is None,'pure inference time inferred')
 corrections=load('updates/FC/WORKFLOW_PROVENANCE_CORRECTIONS.json')
 need(corrections['base_revision']==BASE and len(corrections['records'])==7 and corrections['original_versions_preserved'],'historical trace correction scope changed')
 for correction in corrections['records']:
  old=load(correction['previous_path']);new=load(correction['path']);validate_trace(new,ROOT)
  need(sha(correction['previous_path'])==correction['previous_sha256']==hashlib.sha256(git('show',BASE+':'+correction['previous_path'])).hexdigest(),'historical trace bytes changed')
  need(sha(correction['path'])==correction['sha256'] and new['previous']['path']==correction['previous_path'] and new['previous']['sha256']==correction['previous_sha256'],'trace successor pin mismatch')
  expected=copy.deepcopy(old);expected['version']=new['version'];expected['previous']=new['previous'];expected['advance']['summary']=new['advance']['summary']
  elapsed=correction['reported_ui_elapsed_work_seconds']
  if elapsed is not None:
   check_ref(correction['duration_source_ref']);r=correction['duration_source_ref'];a,b=r['lines'];text='\n'.join((ROOT/r['path']).read_text().splitlines()[a-1:b])
   need('Worked for' in text and elapsed==old['resources']['reported_inference_seconds'],'UI elapsed source mismatch')
   need(str(elapsed)+' elapsed work seconds' in new['context']['capital_access'],'UI elapsed observation lost')
   expected['resources']['reported_inference_seconds']=None;expected['context']['capital_access']=new['context']['capital_access']
  need(new==expected and new['resources']['reported_inference_seconds'] is None,'unscoped historical trace mutation')
 reviewed=load('updates/FC/synthesis/critic/ADDENDUM_INPUTS.json')
 need(len(reviewed['entries'])==9 and reviewed['capital_base']==BASE,'synthesis criticism coverage')
 for entry in reviewed['entries']:
  p=entry['path'].replace('work/FC-agents/','updates/FC/synthesis/')
  need(sha(p)==entry['sha256'] and (ROOT/p).stat().st_size==entry['bytes'],'reviewed final proof changed');check_ref(dict(entry,path=p))
 print(json.dumps(dict(status='PASS',base_revision=BASE,original_files=len(orig),original_bytes=sum(x['bytes'] for x in orig),producer_hashes=hashes,archive_members=members,python_syntax_checks=py,derived_and_replay_files=len(derived),cards=4,proof_routes=proofs,paired_bridges=18,individual_checkpoints=4,workflow_traces=traces,workflow_corrective_versions=7,technology_new_records=3,technology_new_versions=0,global_checkpoint_validation='inherited failure preserved;not passed',scientific_truth_checked=False),indent=2))
if __name__=='__main__':main()
