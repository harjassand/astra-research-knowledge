"""Packaging-only nonmutating replay; zero source calls."""
from pathlib import Path
import sys,json,hashlib,gzip,importlib.util
ROOT=Path(__file__).resolve().parent
for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
    h,p=line.split('  ',1);assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
D=ROOT/'resolvent_control_reuse_20261031';sys.path.insert(0,str(D))
import control as C
import check_control as a
import check_uniform_control as b
def clean(x):
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k not in ['seconds','wall_seconds']}
    if isinstance(x,list):return [clean(v) for v in x]
    return x
out={}
for name,mod,saved in [('author_exact',a,'control_checks.json'),('author_uniform',b,'uniform_control_checks.json')]:
    result=mod.run();assert clean(result)==clean(json.loads((D/saved).read_text())),name;out[name]={k:result[k] for k in ['checks','refusals']}
p=D/'reviewer_2231/extra_checks.py';spec=importlib.util.spec_from_file_location('independent_extra',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
result=mod.run();saved=json.loads((p.parent/'extra_checks.json').read_text());assert clean(result)==clean(saved),'independent';out['independent']={k:v for k,v in result.items() if 'check' in k or 'refusal' in k}
saved=json.loads((D/'episode_protocol_checks.json').read_text());paths=json.loads(gzip.decompress((D/'episode_micro_paths.json.gz').read_bytes()));assert C.digest(paths)==saved['micro_path_sha256']
record=saved['record'];design=record['design'];counts=[[[0]*len(design['parts']) for i in range(design['n'])] for a in range(design['m'])];mapping={i:j for j,p in enumerate(design['parts']) for i in p};calls=0
for p in paths:
    path=p['micro_path'];assert path[0]==p['source_row'] and 2<=len(path)<=design['cap']+2;calls+=len(path)-1;counts[p['action']][p['source_row']][mapping[path[-1]]]+=1
assert counts==record['counts'] and calls==saved['ledger']['actual_source_calls'];assert C.receive_counts(record,expected_design=design)==saved['certificate'];out['saved_actual_episodes']=len(paths);out['saved_actual_calls']=calls;out['new_source_calls']=0;out['status']='PASS_EXTRACTED_NONMUTATING_REPLAY'

D2=ROOT/'resolvent_canonical_comparator_20261031';sys.path.insert(0,str(D2))
import check_canonical as cc
result=cc.run();assert clean(result)==clean(json.loads((D2/'canonical_checks.json').read_text()));out['canonical_author']={k:result[k] for k in ['checks','refusals']}
p=D2/'reviewer_2251/extra_checks.py';spec=importlib.util.spec_from_file_location('canonical_independent',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);result=mod.run();assert clean(result)==clean(json.loads((p.parent/'extra_checks.json').read_text()));out['canonical_independent']={k:v for k,v in result.items() if 'check' in k or 'refusal' in k};print(json.dumps(out,indent=2))
