#!/usr/bin/env python3
"""Nonmutating scientific reproduction and manifest checks."""
from pathlib import Path
import gzip,hashlib,json,sys,time

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'two_rate_operator_acquisition_20261031'))
from quadratic_leakage import run_checks as quadratic
from sparse_norm_probe import run_checks as norms
from reviewer_quadratic_checks import run as independent_math
from reviewer_retained_receiving_checks import run as independent_receiving
from check_retained_large_acquisition import replay,R
from retained_large_acquisition import integer_step,integer_output


def main():
    tic=time.perf_counter();manifest=ROOT/'MANIFEST_SHA256.json'
    if manifest.exists():
        for x in json.loads(manifest.read_text())['files']:
            p=ROOT/x['path'];assert p.stat().st_size==x['bytes']
            assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
    else:
        # Used once while building this package, before its final manifest.
        for x in json.loads((ROOT/'ALLOWLIST.json').read_text())['source_files']:
            assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']
    out={'quadratic_exact':quadratic()['checks'],'norm_exact':norms()['checks'],
         'independent_math':independent_math(),'independent_receiving':independent_receiving()}
    p=ROOT/'two_rate_operator_acquisition_20261031'
    x=json.loads((p/'history_sensitive_4096_result.json').read_text())
    raw=(p/'history_sensitive_4096_observations.json.gz').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==x['transcript_gzip_sha256']
    records=json.loads(gzip.decompress(raw))['records']
    out['history_replay']=replay(x,records,expected_b=x['task_b'],expected_ell_num=x['task_ell_numer'],
       expected_ell_den=x['task_ell_denominator'],expected_length=24,expected_tolerance=R(1,50),
       expected_confidence=R(1,1000),expected_generators=2)
    c=x['compiled'];word_hash=hashlib.sha256();count=0
    with gzip.open(p/'history_sensitive_4096_predictions.tsv.gz','rt') as file:
        header=next(file);assert header.startswith('query_id\t')
        for line in file:
            i,w,num,den=line.rstrip().split('\t');assert int(i)==count
            word=tuple(map(int,w));word_hash.update(bytes(word));state=c['initial_grid_state'][:]
            for a in word:state,_=integer_step(c['operators'][a],state)
            assert integer_output(c,state)==R(num,den);count+=1
    assert count==50000 and word_hash.hexdigest()==x['screening']['word_list_sha256']
    out.update({'stream_predictions':count,'status':'PASS','seconds':time.perf_counter()-tic,
                'scope':'Conditional mathematical/scientific-record reproduction; not iid provenance, physical truth, or individually executed source calls.'})
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
