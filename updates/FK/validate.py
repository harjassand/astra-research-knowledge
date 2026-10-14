#!/usr/bin/env python3
"""Fail-closed FK provenance/history/routing checks; not scientific validation."""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json
import subprocess

ROOT=Path(__file__).resolve().parents[2]
BASE='4c47df1fda950e27e48295689dd642194bfac046'
MAIN='ace0cfc4437fe91c20ccd24d69e0ee4bb335e871'


def need(ok,message):
    if not ok:raise ValueError(message)


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
    p=r['path']
    need(not Path(p).is_absolute() and (ROOT/p).resolve().is_relative_to(ROOT),'unsafe ref: '+p)
    need((ROOT/p).is_file() and sha(p)==r['sha256'],'hash mismatch: '+p)
    if 'bytes' in r:need((ROOT/p).stat().st_size==r['bytes'],'size mismatch: '+p)
    if r.get('lines'):
        a,b=r['lines'];need(1<=a<=b<=len((ROOT/p).read_text().splitlines()),'bad range: '+p)


def main():
    source=load('updates/FK/SOURCE_MANIFEST.json');derived=load('updates/FK/DERIVED_MANIFEST.json')['files']
    need(source['main_revision']==MAIN and source['previous_pr_head']==BASE,'source pins')
    need(len(source['files'])==29 and sum(x['bytes'] for x in source['files'])==233736,'source inventory')
    need(sum(x['kind']=='directory_payload' for x in source['files'])==26 and sum(x['kind']=='pasted_source' for x in source['files'])==3,'source kinds')
    need(len(derived)==131 and sum(x['bytes'] for x in derived)==1107580,'derived inventory')
    for x in source['files']+derived:check(x)
    for x in source['files']:need(Path(x['source_absolute_path']).is_absolute(),'source original provenance')
    for x in derived:need(Path(x['owned_original_absolute_path']).is_absolute(),'derived original provenance')
    need(not any(x['path'].endswith(('.pdf','.html','.png')) or '__pycache__' in x['path'] or 'site-packages' in x['path'] for x in derived),'thirdparty full paper/environment/cache republished')
    for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','web/documents.jsonl','agent/SEMANTIC_NOTICES.jsonl','state/branches.tsv']:
        need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'not append-only: '+p)
    for p,key in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges'),('mechanisms/bridge_candidates.json','rejected_transfers')]:
        old=json.loads(git('show',BASE+':'+p))[key]
        need(load(p)[key][:len(old)]==old,'old sequence changed: '+p+':'+key)
    old=json.loads(git('show',BASE+':web/catalog.json'))
    need(load('web/catalog.json')[:len(old)]==old,'old web catalog changed')
    old=json.loads(git('show',BASE+':indexes/query_aliases.json'))
    need(all(load('indexes/query_aliases.json').get(k)==v for k,v in old.items()),'old aliases changed')
    history=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    immutable=('state/branches/','state/checkpoints/','frontier/review_cards/','frontier/cards/','cards/','updates/','technology/records/','evaluation/workflows/records/','web/pages/')
    for p in git('diff','--name-only',BASE).decode().splitlines():
        need(not(p in history and p.startswith(immutable)),'immutable prior file changed: '+p)
    own=load('updates/FK/CLAIMS.json')['claims']
    need(len(own)==3 and {x['id'].split('-')[0] for x in own}=={'N809','N810','N811'},'claim set')
    checked=0
    for c in own:
        st=load('frontier/cards/'+c['id']+'.json')
        need(st['claim_status']=='source_derived_unreviewed','scientific status promotion')
        need(sha(st['card_path'])==st['card_sha256'],'card hash')
        need((ROOT/'frontier/dossiers'/(c['id'].split('-')[0]+'.txt')).is_file(),'missing dossier')
        need((ROOT/'web/pages'/(c['id']+'.html')).is_file(),'missing card page')
        for r in refs(st):check(r);checked+=1
    notices=load('updates/FK/SCOPED_NOTICES.json')
    need(len(notices)==3 and all(x['whole_claim_invalidated'] is False for x in notices),'notice scope')
    bridges=load('updates/FK/BRIDGES.json')['bridges']
    need(len(bridges)==7,'bridge count')
    allowed={'PROVEN LOGICAL DEPENDENCY','ESTABLISHED COMPATIBLE INTERFACE','CANDIDATE CONNECTION','INCOMPATIBLE ASSUMPTIONS','REFUTED TRANSFER'}
    for b in bridges:
        need(b['id'].startswith('FK_') and b['state']==b['status'] and b['state'] in allowed,'bridge schema/state')
        for side in ['source_interface','destination_interface']:
            need(all(b[side].get(k) for k in ['objects','regime_and_quantifiers','supplied_information','acquired_information','legal_access','guarantee','units_norm_and_precision','costs']),'incomplete paired interface')
    for r in refs(notices+bridges):check(r);checked+=1
    metadata=[x for x in rows('indexes/source_metadata.jsonl') if x.get('source_id','').startswith('src-FK-')]
    need(len(metadata)==160 and {x['path'] for x in metadata}=={x['path'] for x in source['files']+derived},'indexed payload set')
    for x in metadata:
        check(x);need((ROOT/'web/pages'/(x['source_id']+'.html')).is_file(),'missing payload page')
    gates=[x for x in rows('frontier/OPEN_PROOF_GATES.jsonl') if x['gate_id'].startswith('G-FK-')]
    need(len(gates)==6 and all(x['status']=='open' and not x['completion_evidence'] for x in gates),'open gate promotion')
    parsed=0
    for p in (ROOT/'updates/FK').rglob('*.py'):
        ast.parse(p.read_text(),filename=str(p));parsed+=1
    pub=load('updates/FK/PUBLICATION_STATUS.json')
    need(pub['standard_publisher_exit_code']!=0 and len(pub['individually_validated_new_checkpoints'])==1,'publisher scope')
    for r in pub['inherited_records_preserved']:
        check(r);need(sha(r['path'])==hashlib.sha256(git('show',BASE+':'+r['path'])).hexdigest(),'inherited unsupported schema changed')
    spec=importlib.util.spec_from_file_location('fk_publisher',ROOT/'state/publish_checkpoint.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for p in pub['individually_validated_new_checkpoints']:
        x=load(p);m.validate_record(x,ROOT)
        need(x['base_revision']==BASE and x['parent_checkpoint_ids']==[],'new checkpoint lineage')
    replay=load('updates/FK/PORTABLE_REPLAY_RECEIPT.json')
    need(replay['status']=='PASS' and replay['total_steps']==21,'portable replay')
    counts={}
    for r in replay['groups']:
        check(r);x=load(r['path'])
        need(x['status']=='PASS' and len(x['checks'])==x['expected_steps'] and all(c['exit_code']==0 for c in x['checks']),'failed replay group')
        need(x['published_inputs_hash_unchanged'] and x['hashed_original_and_derived_files']==160,'replay input drift')
        counts[x['group']]=len(x['checks'])
        for log in x['checks']:need(sha(str(Path(r['path']).parent/log['log']))==log['log_sha256'],'replay log drift')
    need(counts==dict(moving=5,thermal=11,physical=5),'replay scope/count')
    initial=load(replay['initial_attempt']['path'])
    need(initial['status']=='FAIL' and 'scipy' in (ROOT/'updates/FK/replay_validation/initial_missing_dependency/0-checks.log').read_text(),'initial dependency failure omitted')
    result=load('updates/FK/synthesis/root/THERMAL_TRANSITION_RESULTS.json')
    need(result['status']=='PASS' and len(result['cases'])==10 and result['spin_dimension']==64,'root finite fixture')
    need(result['exact_sector']['response_difference']=='3/32' and result['rejected_exponential_weight']>2180,'root negative witness scope')
    need(result['sampling']['trials']==4239 and 'synthetic' in result['sampling']['note'],'raw synthetic trial scope')
    scope=(ROOT/'updates/FK/synthesis/root/SCOPE_CLARIFICATIONS.md').read_text()
    need('precision-alignment' in scope and 'different powers' in scope and 'functions of H' in scope,'material corrections omitted')
    for p in ['updates/FK/synthesis/response_bounds/CORRECTION_01.md','updates/FK/synthesis/response_bounds/CORRECTION_01_RESULTS.json','updates/FK/synthesis/affine_audit_delta/REPORT.md','updates/FK/synthesis/anchor_audit/delta/REPORT.md','updates/FK/synthesis/anchor_scaling_correlated_source_delta/REPORT.md']:
        need((ROOT/p).is_file(),'missing corrected/cold evidence: '+p)
    deployment=load('updates/FK/synthesis/root/WORKER_DEPLOYMENT.json');workers=deployment['initial_workers']
    need(len(workers)==15 and len({x['agent'] for x in workers})==15 and all(x['configured_model']=='gpt-6-luna' and x['reasoning_effort']=='max' and x['fork_turns']=='none' for x in workers),'actual worker configuration')
    need(deployment['initial_concurrent_running_observation']['all15_observed_running'],'concurrency observation absent')
    for tid in ['T-bounded-thermal-transition-functional','T-carrier-gated-retained-reaction-selection']:
        t=load('technology/records/'+tid+'/v0001.json')
        need(t['version']==1 and t['stage']=='simulation' and any(x['stage']=='experiment' and x['decision']=='open' for x in t['gates']),'physical stage promotion')
    print(json.dumps(dict(status='PASS',base_revision=BASE,main_revision=MAIN,original_files=29,original_bytes=233736,derived_files=131,derived_bytes=1107580,
      indexed_sources=160,new_cards=3,notices=3,paired_bridges=7,new_checkpoints=1,configured_concurrent_luna_max_workers=15,portable_steps=21,
      python_syntax_checks=parsed,scoped_refs=checked,global_checkpoint_validation='Inherited unsupported schema failure preserved; new checkpoint individually validated.',scientific_truth_checked=False),indent=2))


if __name__=='__main__':main()
