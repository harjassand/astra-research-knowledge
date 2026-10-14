#!/usr/bin/env python3
"""Scoped FR integrity/continuity validation. No scientific truth certification."""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json
import subprocess

ROOT=Path(__file__).resolve().parents[2]
BASE='00631610750c708263d5cf6d812ebbb8edc77335'
PREFIX='updates/FR-capital-mining-20261015/'

def need(value,message):
    if not value:raise ValueError(message)
def load(path):return json.loads((ROOT/path).read_text())
def rows(path):return [json.loads(s) for s in (ROOT/path).read_text().splitlines() if s]
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def check(ref):
    path=ref['path'];p=(ROOT/path).resolve()
    need(not Path(path).is_absolute() and p.is_relative_to(ROOT) and p.is_file(),'unsafe/missing evidence: '+path)
    need(sha(path)==ref['sha256'],'hash mismatch: '+path)
    if 'bytes' in ref:need(p.stat().st_size==ref['bytes'],'size mismatch: '+path)
    if ref.get('lines'):
        a,b=ref['lines'];need(1<=a<=b<=len(p.read_text().splitlines()),'bad inclusive range: '+path)
    if ref.get('source_revision'):
        need(hashlib.sha256(git('show',ref['source_revision']+':'+path)).hexdigest()==ref['sha256'],'revision mismatch: '+path)

def main():
    src=load(PREFIX+'SOURCE_MANIFEST.json');derived=load(PREFIX+'DERIVED_MANIFEST.json')
    need(src['main_revision']==BASE and src['total_files']==40 and src['total_bytes']==329875,'source inventory/pin mismatch')
    for ref in src['files']+derived['files']:check(ref)
    need(len(derived['files'])==derived['total_files'] and sum(x['bytes'] for x in derived['files'])==derived['total_bytes'],'derived inventory mismatch')
    original_observations=0
    for ref in src['files']:
        original=Path(ref['source_absolute_path'])
        if original.exists():
            need(hashlib.sha256(original.read_bytes()).hexdigest()==ref['sha256'],'original source changed: '+str(original));original_observations+=1
    c=load(PREFIX+'CURATION_INPUT.json');receipt=load(PREFIX+'INTEGRATION_GENERATOR_RECEIPT.json')
    need(c['base_revision']==BASE and c['intake_id']=='FR','curation scope')
    # The generator receipt's exact input hash may be nested in its schema.
    need(hashlib.sha256((ROOT/(PREFIX+'CURATION_INPUT.json')).read_bytes()).hexdigest() in json.dumps(receipt),'curation hash missing from generator receipt')
    for ref in c['evidence'].values():check(ref)
    for path,digest in receipt['owned_artifacts'].items():
        need(sha(path)==digest,'generated artifact hash mismatch: '+path)
    ids={x['id'] for x in c['cards']};need({x.split('-')[0] for x in ids}=={'N830','N831','N832'},'claim reservation')
    current={x['card_id']:x for x in rows('frontier/CURRENT_CLAIM_STATUS.jsonl')}
    catalog={x['id']:x for x in load('indexes/agent_catalog.json')['claims']}
    for cid in ids:
        x=current[cid];need(x['claim_status']=='source_derived_unreviewed','scientific promotion')
        need(load('frontier/cards/'+cid+'.json')==x,'status sidecar disagreement')
        need(sha(x['card_path'])==x['card_sha256']==catalog[cid]['card_sha256'],'card hash disagreement')
        need((ROOT/'frontier/review_cards'/f'{cid}.txt').read_bytes().endswith((ROOT/x['card_path']).read_bytes()),'historical card wrapper')
        need((ROOT/'frontier/dossiers'/f'{cid.split("-")[0]}.txt').is_file(),'generated dossier absent')
        for ref in x['proof_availability']['located_proof_sources']:check(ref)
    gates=[x for x in rows('frontier/OPEN_PROOF_GATES.jsonl') if x['gate_id'].startswith('G-FR-')]
    need(len(gates)==6 and all(x['status']=='open' and not x['completion_evidence'] for x in gates),'gate promotion/count')
    need(len(load(PREFIX+'BRIDGES.json')['bridges'])==5,'bridge count')
    for path in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','agent/SEMANTIC_NOTICES.jsonl','web/documents.jsonl','state/branches.tsv']:
        need((ROOT/path).read_bytes().startswith(git('show',BASE+':'+path)),'historical byte prefix changed: '+path)
    for path,key in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges'),('mechanisms/bridge_candidates.json','rejected_transfers')]:
        old=json.loads(git('show',BASE+':'+path))[key];need(load(path)[key][:len(old)]==old,'historical array value/order changed: '+path)
    old=json.loads(git('show',BASE+':web/catalog.json'));need(load('web/catalog.json')[:len(old)]==old,'historical web catalog changed')
    old=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in old.items()),'historical alias changed')
    history=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    immutable=('cards/','frontier/cards/','frontier/review_cards/','updates/','state/checkpoints/','state/branches/','technology/records/','web/pages/','evaluation/workflows/records/')
    for path in git('diff','--name-only',BASE).decode().splitlines():
        need(not(path in history and path.startswith(immutable)),'historical immutable artifact changed: '+path)
    replay=load(PREFIX+'replay_validation/RECEIPT.json')
    need(replay['status']=='PASS' and replay['total_steps']==14 and replay['published_inputs_hash_unchanged'],'fresh scientific replay scope')
    for item in replay['checks']:
        need(item['exit_code']==0 and sha(PREFIX+'replay_validation/'+item['log'])==item['log_sha256'],'fresh replay log mismatch')
    pub=load(PREFIX+'PUBLICATION_STATUS.json')
    need(pub['standard_publisher_exit_code']==1 and 'unsupported checkpoint schema' in pub['standard_publisher_stderr'],'normal publisher failure must remain explicit')
    need(pub['global_validation_exit_code']==1 and 'unsupported checkpoint schema' in pub['global_validation_stderr'],'global inherited failure must remain explicit')
    for ref in pub['inherited_records_preserved']:
        check(ref);need((ROOT/ref['path']).read_bytes()==git('show',BASE+':'+ref['path']),'inherited malformed record changed')
    spec=importlib.util.spec_from_file_location('fr_pub',ROOT/'state/publish_checkpoint.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    checkpoint=load(pub['individually_validated_checkpoint']);m.validate_record(checkpoint,ROOT)
    need(checkpoint['base_revision']==BASE and checkpoint['parent_checkpoint_ids']==[],'new checkpoint ancestry')
    q=load('technology/records/T-task-matched-conditional-exchange/v0001.json');p=load('technology/records/T-phase-selective-retained-polarity/v0002.json')
    need(q['stage']=='opportunity' and p['stage']=='model','technology stage promotion')
    need(all(g['decision']=='open' for g in p['gates'] if g['stage'] in ['simulation','experiment']),'physical gate promotion')
    parsed=0
    for path in (ROOT/PREFIX).rglob('*.py'):
        if '__pycache__' not in path.parts:ast.parse(path.read_text(),filename=str(path));parsed+=1
    return dict(status='PASS',scope='FR additive integrity and new-record validity only; mathematical truth/novelty/physical obtainability not certified.',base_revision=BASE,original_files=40,original_bytes=329875,available_originals_observed_unchanged=original_observations,derived_files=derived['total_files'],derived_bytes=derived['total_bytes'],new_cards=3,typed_bridges=5,scoped_notices=4,open_gates=6,fresh_scientific_replay_steps=14,parsed_python_files=parsed,new_checkpoint_validated=True,global_checkpoint_validation='FAIL: inherited unsupported schemas preserved; not a global pass.',technology='New opportunity lead and append-only physical model v2; no simulation/experiment promotion.',scientific_truth_checked=False)

if __name__=='__main__':print(json.dumps(main(),indent=2))
