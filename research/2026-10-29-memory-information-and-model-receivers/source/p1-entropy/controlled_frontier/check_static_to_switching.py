#!/usr/bin/env python3
"""Exact CTMC checks plus actual native two-pulse trajectories.

No hidden generator is inferred. Two fully declared source hypotheses are
tested by an ordinary survival-count consumer using only retained outcomes.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import hashlib
import json
import math
import time
import numpy as np

ROOT=Path(__file__).resolve().parent
R=F(3,4)
N=65536

def eye(n):
    return [[F(i==j) for j in range(n)] for i in range(n)]

def zero(n):
    return [[F(0) for j in range(n)] for i in range(n)]

def transpose(a):
    return [list(x) for x in zip(*a)]

def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def add(a,b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def scale(a,x):
    return [[x*y for y in row] for row in a]

def scalar(a):
    return sum(map(sum,a))/3

def serialize(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:serialize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serialize(v) for v in x]
    return x

def exp2_bounds(terms=50):
    """Strict rational bracket for exp(2), using a positive Taylor series."""
    term=F(1); s=term
    for k in range(1,terms+1):
        term*=F(2,k); s+=term
    first=term*F(2,terms+1)
    upper=s+first/(1-F(2,terms+2))
    return s,upper

def exact_checks():
    a=zero(3); b=zero(3)
    a[0][1]=R; b[1][2]=R
    ats=[transpose(a),transpose(b)]
    I=eye(3)
    generator_cases=[]
    # At every u the diagonal is exactly -1 and absorption completes rows.
    for k in range(17):
        u=F(k,16)
        live=add(scale(a,1-u),scale(b,u))
        for sign,z in [("forward",live),("transpose",transpose(live))]:
            Q=add(z,scale(I,-1))
            kill=[-sum(row) for row in Q]
            assert all(x>=F(1,4) for x in kill)
            assert all(Q[i][i]==-1 for i in range(3))
            full=[row+[kill[i]] for i,row in enumerate(Q)]
            full.append([F(0)]*4)
            assert all(sum(row)==0 for row in full)
            assert all(full[i][j]>=0 for i in range(4) for j in range(4) if i!=j)
            powers=[I,z,mm(z,z),mm(mm(z,z),z)]
            assert powers[3]==zero(3)
            assert [scalar(x) for x in powers]==[F(1),R/3,R*R*u*(1-u)/3,F(0)]
            generator_cases.append({"u":u,"model":sign,"killing":kill})
    # All mixed-control polynomial coefficients are checked symbolically by
    # separately summing every chronological word with the same action count.
    grouped={}
    word_weights={}
    for depth in range(7):
        sums=[{},{}]
        for word in product(range(2),repeat=depth):
            m=I; mt=I
            for letter in word:
                m=mm(m,[a,b][letter]); mt=mm(mt,ats[letter])
            coeff,coefft=scalar(m),scalar(mt)
            counts=(word.count(0),word.count(1))
            for dd,cc in zip(sums,[coeff,coefft]): dd[counts]=dd.get(counts,F(0))+cc
            if depth<=2: word_weights[''.join('AB'[x] for x in word) or 'empty']=[coeff,coefft]
        assert sums[0]==sums[1]
        grouped[str(depth)]={str(k):v for k,v in sums[0].items()}
    assert mm(a,a)==zero(3) and mm(b,b)==zero(3)
    assert scalar(mm(a,b))==F(3,16)
    assert scalar(mm(ats[0],ats[1]))==0
    # Equal-duration pulse semigroup polynomials after removing exp(-2).
    forward=scalar(mm(add(I,a),add(I,b)))
    reverse=scalar(mm(add(I,ats[0]),add(I,ats[1])))
    assert forward==F(27,16) and reverse==F(3,2)
    elo,ehi=exp2_bounds()
    qlo,qhi=1/ehi,1/elo
    assert F(3,16)*qlo>F(1,40)
    threshold=(F(51,32)*qlo,F(51,32)*qhi)
    return {"generator_cases":generator_cases,"ordered_word_weights":word_weights,
            "frozen_shuffle_sums":grouped,"survival_exp_minus2_coefficients":[forward,reverse],
            "gap_lower_bound":"1/40","exp_minus2_bracket":[qlo,qhi],
            "decision_threshold_bracket":threshold,
            "all_frozen_laws_proof":"nilpotence and scalar transposition; numeric grid is ancillary",
            "source_calls":0},threshold

def produce(transposed,seed,filename):
    rng=np.random.default_rng(seed)
    event_times=np.full((N,3),np.nan,dtype=np.float64)
    absorbed=np.zeros(N,dtype=np.bool_)
    elapsed=np.empty(N,dtype=np.float64)
    counts=np.zeros(N,dtype=np.uint8)
    hold_draws=0; branch_draws=0; jumps=0
    for trial in range(N):
        hidden=int(rng.integers(0,3))
        t=0.; count=0
        while True:
            hold_draws+=1
            tnext=t+float(rng.exponential())
            if tnext>=2.:
                elapsed[trial]=2.; break
            t=tnext
            action=0 if t<1. else 1
            event_times[trial,count]=t; count+=1; jumps+=1
            if not transposed:
                eligible=(action==0 and hidden==0) or (action==1 and hidden==1)
                destination=hidden+1
            else:
                eligible=(action==0 and hidden==1) or (action==1 and hidden==2)
                destination=hidden-1
            if eligible:
                branch_draws+=1
                survives=bool(rng.random()<.75)
            else:
                survives=False
            if survives:
                hidden=destination
            else:
                absorbed[trial]=True; elapsed[trial]=t; break
        counts[trial]=count
    np.savez_compressed(filename,event_times=event_times,absorbed=absorbed,
                        elapsed=elapsed,native_jump_counts=counts)
    return {"trials":N,"resets":N,"native_jumps":jumps,"exponential_draws":hold_draws,
            "conditional_branch_draws":branch_draws,"hidden_reset_draws":N,
            "actual_elapsed_source_clock":math.fsum(map(float,elapsed)),
            "scheduled_horizon_clock":2*N,"seed":seed,"source_hypothesis":'transpose' if transposed else 'forward',
            "raw_file":filename.name,"raw_bytes":filename.stat().st_size,
            "raw_sha256":hashlib.sha256(filename.read_bytes()).hexdigest()}

def consume(filename,threshold):
    """Only event record and declared two-hypothesis threshold enter here."""
    with np.load(filename) as rec:
        absorbed=rec['absorbed']; t=rec['event_times']; elapsed=rec['elapsed']; counts=rec['native_jump_counts']
        assert len(absorbed)==N
        assert np.array_equal(np.sum(np.isfinite(t),axis=1),counts)
        assert np.all((elapsed>0)&(elapsed<=2))
        assert np.all(elapsed[~absorbed]==2)
        for i in range(N):
            es=t[i,:counts[i]]
            assert np.all(np.diff(es)>0) and np.all((es>0)&(es<2))
            if absorbed[i]: assert es[-1]==elapsed[i]
        alive=int(np.sum(~absorbed)); empirical=F(alive,N)
        verdict='forward' if empirical>threshold[1] else 'transpose' if empirical<threshold[0] else 'unresolved'
        return {"survivors":alive,"trials":N,"empirical_survival":str(empirical),
                "decision":verdict,"ideal_law_error_bound_per_hypothesis":"exp(-65536/3200) < 2e-9",
                "private_generator_read":False,"hidden_start_identities_read":False}

def main():
    t0=time.perf_counter()
    exact,threshold=exact_checks()
    acquisition=[]
    for transposed,seed,name in [(False,2026102911,'TWO_PULSE_FORWARD_RECORD.npz'),
                                 (True,2026102912,'TWO_PULSE_TRANSPOSE_RECORD.npz')]:
        file=ROOT/name
        cost=produce(transposed,seed,file)
        consumer=consume(file,threshold)
        assert consumer['decision']==cost['source_hypothesis']
        acquisition.append({"producer":cost,"consumer":consumer})
    result={"exact_checks":serialize(exact),"acquisition":acquisition,
            "numpy_version":np.__version__,"wall_seconds":time.perf_counter()-t0,
            "total_resets":sum(x['producer']['resets'] for x in acquisition),
            "total_native_jumps":sum(x['producer']['native_jumps'] for x in acquisition),
            "total_source_clock":sum(x['producer']['actual_elapsed_source_clock'] for x in acquisition),
            "scope":"Finite CTMC two-hypothesis proof; ideal numerical native trials, no physical or floating-law validation",
            "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'STATIC_TO_SWITCHING_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['exact_checks','acquisition']},indent=2))
    print(json.dumps(acquisition,indent=2))

if __name__=='__main__': main()
