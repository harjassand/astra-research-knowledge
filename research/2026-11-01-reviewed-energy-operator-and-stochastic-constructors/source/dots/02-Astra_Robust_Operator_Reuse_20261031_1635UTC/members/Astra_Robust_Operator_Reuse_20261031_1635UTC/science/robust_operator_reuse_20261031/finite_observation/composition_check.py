#!/usr/bin/env python3
"""Compose acquired sparse observations with independently certified replay.

This is a conditional iid-data certificate, not proof of sampling provenance.
The small graph and matrices are reconstructed from saved observations only.
"""
import itertools
import json
from pathlib import Path
import random
import time
from fractions import Fraction as F
import sympy as sp
from risk_frontier import verify_record,SyntheticCounts,value
from robust_replay import acquire,encode_model,verify,compile_integer_replay,integer_step,integer_output


def reconstruct(record):
    knowledge={};centers={}
    for row in record['ledger']:
        key=tuple(row['row']);i,a=key;train=dict(row['training_counts']);valid=dict(row['validation_counts']);N=row['validation_draws']
        S=knowledge.get(key,set())|set(train)|{i};q=F(sum(v for j,v in valid.items() if j not in S),N)
        C={j:F(valid.get(j,0),N) for j in S};C[i]=C.get(i,F(0))+q
        centers[key]={j:p for j,p in C.items() if p};knowledge[key]=S|set(valid)
    states={17}
    for (i,a),row in centers.items():states.add(i);states.update(row)
    states=sorted(states);index={s:i for i,s in enumerate(states)};n=len(states)
    A=[sp.zeros(n) for _ in range(2)]
    for i,s in enumerate(states):
        for a in range(2):
            for j,p in centers.get((s,a),{s:F(1)}).items():A[a][i,index[j]]=sp.Rational(p.numerator,p.denominator)
    b=sp.Matrix([int(s==65003) for s in states]);ell=sp.Matrix([int(s==17) for s in states])
    return A,b,ell,states


class RetainedCenterOracle:
    def __init__(self,A):self.A=A;self.calls=[]
    def observe(self,bits):
        self.calls.append({'retained_center_entries_read':sum(X.rows*X.cols for X in self.A),
                           'new_physical_or_statistical_observations':0,'scope':'Exact finite observed centers, not exact true kernels.'})
        return [(X,X) for X in self.A]


def run():
    tic=time.perf_counter();record=json.loads(Path('risk_frontier_results.json').read_text())
    L=12;tol=F(1,10);delta=F(1,1000);initial={17:F(1)}
    assert verify_record(record,initial,2,expected_length=L,expected_tolerance=tol,expected_delta=delta)
    obs=F(record['observation_bound']);remaining=tol-obs
    A,b,ell,states=reconstruct(record)
    model=acquire(RetainedCenterOracle(A),b,ell,L,sp.Rational(remaining.numerator,remaining.denominator),precisions=(1,))
    if 'certificate' not in model:
        return {'admitted':False,'observation_bound':str(obs),'remaining_budget':str(remaining),
                'center_states':len(states),'acquisition':model['ledger'],
                'scope':'Observation admission succeeded; this stable-H replay route failed. Sparse ordinary center replay remains available.'}
    cert=model['certificate'];r=encode_model(model)
    assert verify(model['boxes'],b,ell,r,expected_length=L,expected_tolerance=sp.Rational(remaining.numerator,remaining.denominator))
    compiled=compile_integer_replay(model['operators'],cert['right'],cert['output'],cert['query_bits'])
    total=sp.Rational(obs.numerator,obs.denominator)+cert['bound'];assert total<=sp.Rational(tol.numerator,tol.denominator)
    rng=random.Random(3091);words=[[0]*L,[1]*L]+[[rng.randrange(2) for _ in range(L)] for _ in range(30)]
    truth=SyntheticCounts();worst=0
    for word in words:
        x=compiled['initial_grid_state']
        # value() advances a row distribution chronologically; the replay API
        # advances an observable column, so this comparison reverses the word.
        for a in reversed(word):x,_=integer_step(compiled['operators'][a],x)
        got=integer_output(compiled,x);actual=value(truth.distribution,initial,lambda i:F(i==65003),word)
        err=abs(got-sp.Rational(actual.numerator,actual.denominator));assert err<=total;worst=max(worst,float(err))
    Path('composed_replay_certificate.json').write_text(json.dumps(r,indent=2)+'\n')
    return {'admitted':True,'checks':len(words)+3,'confidence_failure_budget':str(delta),'observation_bound':str(obs),
            'compression_plus_execution_bound':str(cert['bound']),'total_bound':str(total),'total_bound_float':float(total),
            'center_states':len(states),'replay_rank':cert['rank'],'logical_iid_draws':record['logical_iid_draws'],
            'center_graph_labels_acquired':states,'common_denominator_coefficient_bits':compiled['common_denominator_coefficient_bits'],
            'maximum_checked_error':worst,'acquisition':model['ledger'],'elapsed_seconds':time.perf_counter()-tic,
            'scope':'End-to-end synthetic acquired-probe observation certificate plus bounded-integer replay. No useful probe set, active graph, metric or low-rank basis was supplied. Rank may remain full; ordinary retained methods receive the same knowledge and certificate.'}


if __name__=='__main__':
    out=run();Path('composition_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
