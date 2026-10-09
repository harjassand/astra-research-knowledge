"""Exact algebraic and kernel checks; finite tests are not all-input proofs."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from fractions import Fraction as F
from itertools import combinations,product
import time,json
from pathlib import Path
import numpy as np
import sympy as sp
from exact_completion import ExactCompletionSampler,_matvec,_dot
from sampler import state_type,mask_from_bits,log_volume


def det_fraction(M):
    if not M:return F(1)
    v=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in row] for row in M]).det()
    return F(int(v.p),int(v.q))

def run():
    start=time.perf_counter()
    X=[[F(x,5) for x in row] for row in [[4,0,1],[3,1,0],[0,3,1],[1,4,1],
          [2,1,3],[1,0,4],[3,-2,1],[2,-1,2]]]
    groups=np.repeat(np.arange(4),2).tolist(); obj=ExactCompletionSampler(X,groups)
    N=len(X); allprob={}; valid_weight=F(0)
    for mask in range(1<<N):
        ix=[i for i in range(N) if mask>>i&1]
        A=[[_dot(X[i],X[j]) for j in ix] for i in ix]
        w=det_fraction(A)*F(1,2)**len(ix)
        allprob[mask]=w/obj.dpp_normalizer
        if all(sum(groups[i]==g for i in ix)<=1 for g in range(4)): valid_weight+=w
    assert sum(allprob.values())==1
    # Check every leaf of the exact sequential low-rank DPP sampler.
    leaves={}
    def recurse(i,R,mask,prefix):
        if i==N: leaves[mask]=prefix; return
        z=_matvec(R,X[i]); h=_dot(X[i],z); q=obj.p[i]*h
        assert 0<=q<=1
        for inc,prob in [(False,1-q),(True,q)]:
            if prob==0: continue
            c=-1/h if inc else (obj.p[i]/(1-q) if q!=0 else F(0))
            Q=[[R[a][b]+c*z[a]*z[b] for b in range(obj.d)] for a in range(obj.d)]
            recurse(i+1,Q,mask|((1<<i) if inc else 0),prefix*prob)
    recurse(0,obj.R,0,F(1))
    assert all(leaves.get(mask,0)==p for mask,p in allprob.items())
    direct={}; completed={}
    for bits in range(16):
        S=[2*g+((bits>>g)&1) for g in range(4)]
        B=[[F(int(a==b))+sum(X[i][a]*X[i][b] for i in S) for b in range(3)] for a in range(3)]
        direct[bits]=F(1,16)*det_fraction(B)
        val=F(0)
        for sub in range(16):
            T=[S[g] for g in range(4) if sub>>g&1]
            A=[[_dot(X[i],X[j]) for j in T] for i in T]
            val+=F(1,16)*det_fraction(A)
        completed[bits]=val
    assert direct==completed
    assert sum(direct.values())==valid_weight
    exact_a=valid_weight/obj.dpp_normalizer
    assert exact_a>=obj.acceptance_lower_bound
    # Finite exchange-degree and detailed-balance audit for random SPD Gram.
    rng=np.random.default_rng(55); n=4; V=rng.normal(size=(5,2*n)); G=V.T@V
    states=[sum(1<<i for i in S) for S in combinations(range(2*n),n)]
    states=[s for s in states if state_type(s,n)>=0]; index={s:i for i,s in enumerate(states)}
    weights=[]; neighbors=[]
    for s in states:
        typ=state_type(s,n)
        weights.append(np.exp(log_volume(G,s,.8))*(1. if typ==0 else .15))
        neigh=[]
        for a in range(2*n):
            if not(s>>a&1):continue
            for b in range(2*n):
                if s>>b&1:continue
                t=s^(1<<a)^(1<<b)
                if t in index:neigh.append(index[t])
        assert len(set(neigh))==(n*n if typ==0 else 5*n-6)
        neighbors.append(neigh)
    w=np.array(weights); pi=w/w.sum(); P=np.zeros((len(states),len(states)))
    for i,neigh in enumerate(neighbors):
        for j in neigh:
            P[i,j]=.5/len(neigh)*min(1.,w[j]/w[i]*len(neigh)/len(neighbors[j]))
        P[i,i]=1-P[i].sum()
    db=float(np.max(np.abs(pi[:,None]*P-pi[None,:]*P.T)))
    assert db<1e-14
    sample_start=time.perf_counter()
    exact_samples,counters=obj.sample(1000,1618,max_trials=10000)
    sample_seconds=time.perf_counter()-sample_start
    ids=[sum((i%2)<<g for g,i in enumerate(row)) for row in exact_samples]
    p=np.array([float(direct[b]/valid_weight) for b in range(16)])
    hist=np.bincount(ids,minlength=16)/len(ids)
    report=dict(exact_completion_identity_states=16,exact_DPP_probability_checks=256,
       exact_sequential_probability_leaves=len(leaves),exact_collision_sum=str(obj.collision_sum),
       collision_sum=float(obj.collision_sum),acceptance_lower_bound=float(obj.acceptance_lower_bound),
       exact_acceptance=str(exact_a),exact_acceptance_float=float(exact_a),
       finite_exchange_states=len(states),max_detailed_balance_error=db,
       exact_reference_samples=1000,reference_seconds=sample_seconds,
       reference_empirical_tv=float(.5*np.abs(hist-p).sum()),reference_work=counters,
       total_seconds=time.perf_counter()-start)
    Path('results/validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
