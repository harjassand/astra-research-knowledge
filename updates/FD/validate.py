"""Fail-closed FD preservation/routing audit; never certifies scientific truth."""
from pathlib import Path
import ast, hashlib, importlib.util, json, subprocess

ROOT=Path(__file__).resolve().parents[2]
BASE='ace0cfc4437fe91c20ccd24d69e0ee4bb335e871'

def need(ok,message):
    if not ok:raise ValueError(message)
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines() if s]
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def refs(obj):
    if isinstance(obj,dict):
        if 'path' in obj and 'sha256' in obj:yield obj
        for value in obj.values():yield from refs(value)
    elif isinstance(obj,list):
        for value in obj:yield from refs(value)
def check_ref(r):
    p=r['path'];need(not Path(p).is_absolute() and (ROOT/p).resolve().is_relative_to(ROOT),'unsafe ref')
    need((ROOT/p).is_file() and sha(p)==r['sha256'],'evidence hash mismatch:'+p)
    if r.get('lines'):
        a,b=r['lines'];need(1<=a<=b<=len((ROOT/p).read_text().splitlines()),'invalid range:'+p)

def main():
    originals=load('updates/FD/SOURCE_MANIFEST.json')['files']
    need(len(originals)==131 and sum(r['bytes'] for r in originals)==3720588,'original inventory drift')
    for r in originals:
        need(sha(r['path'])==r['sha256'] and (ROOT/r['path']).stat().st_size==r['bytes'],'original bytes changed:'+r['path'])
    derived=load('updates/FD/DERIVED_MANIFEST.json')['files']
    for r in derived:check_ref(r)
    for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl',
              'frontier/OPEN_PROOF_GATES.jsonl','web/documents.jsonl','agent/SEMANTIC_NOTICES.jsonl','state/branches.tsv']:
        need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'not append-only:'+p)
    for p,key in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),
                  ('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges'),
                  ('mechanisms/bridge_candidates.json','rejected_transfers')]:
        before=json.loads(git('show',BASE+':'+p))[key];need(load(p)[key][:len(before)]==before,'historical sequence changed:'+p+':'+key)
    before=json.loads(git('show',BASE+':web/catalog.json'));need(load('web/catalog.json')[:len(before)]==before,'historical web catalog changed')
    before=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in before.items()),'historical alias changed')
    historical=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    immutable=('cards/','frontier/cards/','state/checkpoints/','technology/records/','evaluation/workflows/records/','updates/','web/pages/')
    for p in git('diff','--name-only',BASE).decode().splitlines():need(not(p in historical and p.startswith(immutable)),'historical immutable file changed:'+p)
    claim_map=load('updates/FD/CLAIMS.json')['claims'];need(len(claim_map)==3,'new claim count')
    count=0
    for c in claim_map:
        status=load('frontier/cards/'+c['id']+'.json');need(status['claim_status']=='source_derived_unreviewed','status promotion')
        need(sha(status['card_path'])==status['card_sha256'],'card hash')
        need((ROOT/'frontier/dossiers'/str(c['id'].split('-')[0]+'.txt')).is_file(),'missing dossier')
        need((ROOT/'web/pages'/str(c['id']+'.html')).is_file(),'missing static card')
        for r in refs(status):check_ref(r);count+=1
    notices=load('updates/FD/SCOPED_NOTICES.json');need(len(notices)==2,'notice scope')
    need(all(n['whole_claim_invalidated'] is False for n in notices),'whole claim invalidated')
    bridges=load('updates/FD/BRIDGES.json')['bridges'];need(len(bridges)==6,'bridge scope')
    states={'PROVEN LOGICAL DEPENDENCY','ESTABLISHED COMPATIBLE INTERFACE','CANDIDATE CONNECTION','INCOMPATIBLE ASSUMPTIONS','REFUTED TRANSFER'}
    for b in bridges:
        need(b['status'] in states and b['status']==b['state'],'bridge state')
        for side in ['source_interface','destination_interface']:
            need(all(b[side].get(k) for k in ['objects','regime_and_quantifiers','supplied_information','acquired_information','legal_access','guarantee','units_norm_and_precision','costs']),'incomplete paired contract')
    for r in refs(notices+bridges):check_ref(r);count+=1
    own_sources=[r for r in rows('indexes/source_metadata.jsonl') if r.get('source_id','').startswith('src-FD-')]
    for r in own_sources:
        check_ref(r);need((ROOT/'web/pages'/str(r['source_id']+'.html')).is_file(),'missing source page')
    parsed=0
    for p in (ROOT/'updates/FD').rglob('*.py'):
        ast.parse(p.read_text(),filename=str(p));parsed+=1
    audit=load('updates/FD/DECODER_REUSE_AUDIT.json');need(len(audit['inputs'])==4 and not audit['new_intake_of_original_claim'] and not audit['new_n64_replay_performed'],'decoder duplicate scope')
    for r in audit['inputs']:
        need(r['byte_identical'] and sha(r['existing_path'])==r['sha256'],'decoder reuse mismatch')
        need(hashlib.sha256(git('show',BASE+':'+r['existing_path'])).hexdigest()==r['sha256'],'decoder baseline drift')
    publication=load('updates/FD/PUBLICATION_STATUS.json')
    need(publication['standard_publisher_exit_code']!=0 and len(publication['individually_validated_new_checkpoints'])==1,'publication boundary')
    for r in publication['inherited_records_preserved']:
        need(sha(r['path'])==r['sha256']==hashlib.sha256(git('show',BASE+':'+r['path'])).hexdigest(),'malformed old record changed')
    spec=importlib.util.spec_from_file_location('fd_publisher',ROOT/'state/publish_checkpoint.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for p in publication['individually_validated_new_checkpoints']:
        r=load(p);m.validate_record(r,ROOT);need(r['base_revision']==BASE and r['parent_checkpoint_ids']==[],'new checkpoint lineage')
    need(all(r['status']=='open' and not r['completion_evidence'] for r in rows('frontier/OPEN_PROOF_GATES.jsonl') if r['gate_id'].startswith('G-FD-')),'unjustified gate closure')
    print(json.dumps(dict(status='PASS',base_revision=BASE,original_files=len(originals),original_bytes=sum(r['bytes'] for r in originals),
        derived_files=len(derived),indexed_sources=len(own_sources),python_syntax_checks=parsed,scoped_evidence_refs=count,new_cards=3,notices=2,paired_bridges=6,new_checkpoints=1,
        global_checkpoint_validation='inherited schema failure preserved;not passed',scientific_truth_checked=False),indent=2))

if __name__=='__main__':main()
