#!/usr/bin/env python3
"""Small real forward-call protocol test, intentionally insufficient precision.

Reuses the existing four-state nonpredictive counterexample, not a new task or
performance benchmark. Algebra tests with fabricated arrays remain separate.
"""
from pathlib import Path
from math import lcm
import json,hashlib,copy,gzip
import sympy as S
import control as C
import episode_protocol as E
ROOT=Path(__file__).resolve().parent

class ExactRationalFixtureSource:
    def __init__(self):
        Z,W,_=C.partitions([[0,1],[2,3]],4);P=Z*W;J=S.ones(4)/4;perm=S.zeros(4)
        for i,j in enumerate([0,2,1,3]):perm[i,j]=1
        A0=S.Rational(9,10)*perm+J/10;A1=S.Rational(9,10)*perm+P/10
        self._rows=[];self.calls=0;self.cdf_entries_examined=0
        for A in [A0,A1]:
            ar=[]
            for i in range(4):
                D=lcm(*(int(x.q) for x in A.row(i)));ar.append((D,[int(x*D) for x in A.row(i)]))
            self._rows.append(ar)
    def step(self,i,a,rng):
        self.calls+=1;D,nums=self._rows[a][i];j=rng.randrange(D)
        for k,v in enumerate(nums):
            self.cdf_entries_examined+=1
            if j<v:return k
            j-=v
        raise ArithmeticError('source normalization')

def run(return_paths=False):
    design={'n':4,'m':2,'gamma':'9/10','parts':[[0,1],[2,3]],'N':512,'cap':32,'delta':'1/100','root_bits':64,'source_id':'old-four-state-nonpredictive-counterexample-rational-v1'}
    src=ExactRationalFixtureSource();record,ledger,paths=E.acquire(src,design,834091);cert=C.receive_counts(record,expected_design=design)
    assert src.calls==ledger['actual_source_calls'];assert ledger['episodes']==4096;assert src.calls<=4096*33
    # Independent replay of actual observed paths, with source row/action tags.
    counts=[[[0,0] for i in range(4)] for a in range(2)]
    for p in paths:
        assert p['micro_path'][0]==p['source_row'];assert 2<=len(p['micro_path'])<=34
        counts[p['action']][p['source_row']][p['micro_path'][-1]//2]+=1
    assert counts==record['counts']
    g=['1','0'];plan=C.robust_plan(cert,g,expected_certificate_sha256=C.digest(cert),expected_goal_sha256=C.digest(g),expected_tolerance='1/100')
    assert plan['status']=='UNKNOWN_ROBUST_MARGIN'
    # Truncation/noise uncertainty is honestly visible; exact closure is not
    # recovered as an empirical equality from these finite observations.
    out={'status':'PASS_ACTUAL_FORWARD_PROTOCOL_REFUSAL','record':record,'ledger':dict(ledger,source_cdf_entries_examined=src.cdf_entries_examined),'certificate':cert,'plan':plan,'micro_path_sha256':C.digest(paths),'scope':'4096 actual sampled episodes on the existing exact four-state software source. No practical/novel capability claim; 0.01-regret request correctly refuses. All actual chosen-row tags retained in this run.','source_sha256':hashlib.sha256((ROOT/'episode_protocol.py').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    return (out,paths) if return_paths else out
if __name__=='__main__':
    out,paths=run(True);(ROOT/'episode_micro_paths.json.gz').write_bytes(gzip.compress(json.dumps(paths,sort_keys=True,separators=(',',':')).encode(),mtime=0));(ROOT/'episode_protocol_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['record','certificate']},indent=2))
