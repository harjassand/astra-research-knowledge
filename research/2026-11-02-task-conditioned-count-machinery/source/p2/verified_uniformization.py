"""Reproducible rational outward bounds for the projected CTMC decision.

Rates are interpreted as exact finite decimal numbers repr(float(native_rate)).
This is an explicit rationalized source model, not a certified physical device.
Proof of validity: P is constructed as an exact rational stochastic matrix;
integer-floor iteration is a componentwise lower bound on the exact law;
a deterministic bound on accumulated downward rounding is added above;
positive-series rational bounds for exp(x) and a geometric bound for the
Poisson tail enclose continuous-time expectation.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import ceil, prod
from time import perf_counter
from decimal import Decimal, localcontext
import numpy as np
from machinery import coarse_states, Model

def fr(v):
    v=float(v)
    return F(str(v)) if v else F(0)

def exact_group_rates(model: Model, groups):
    G=len(groups);q=model.q
    a=[[[F(0) for t in range(q)] for s in range(q)] for g in range(G)]
    b=[[[[[F(0) for t in range(q)] for s in range(q)] for r in range(q)] for z in range(G)] for h in range(G)]
    for g,sites in enumerate(groups):
        for j in sites:
            for s in range(q):
                for t in range(q):
                    a[g][s][t]+=fr(model.unary[j,s,t])/len(sites)
    for h,ss in enumerate(groups):
        for z,dd in enumerate(groups):
            pairs=[(i,j) for i in ss for j in dd if i!=j]
            if not pairs:continue
            for i,j in pairs:
                for r in range(q):
                    for s in range(q):
                        for t in range(q):
                            b[h][z][r][s][t]+=fr(model.pair[i,j,r,s,t])/len(pairs)
    return a,b

def exact_eta(model,groups,a,b):
    gid={site:g for g,sites in enumerate(groups) for site in sites}
    eta=F(0); q=model.q
    for j in range(model.n):
        for s in range(q):
            for t in range(q):
                eta+=abs(fr(model.unary[j,s,t])-a[gid[j]][s][t])
    for i in range(model.n):
        for j in range(model.n):
            if i==j:continue
            for r in range(q):
                for s in range(q):
                    for t in range(q):
                        eta+=abs(fr(model.pair[i,j,r,s,t])-b[gid[i]][gid[j]][r][s][t])
    return eta

def make_rational_uniformized(model,groups):
    a,b=exact_group_rates(model,groups)
    states,idx=coarse_states(groups,model.q)
    Q=[]; max_exit=F(0)
    for c in states:
        dest={};exit_rate=F(0)
        for z in range(len(groups)):
            for s in range(model.q):
                if not c[z][s]:continue
                for t in range(model.q):
                    if s==t:continue
                    rate=a[z][s][t]
                    for h in range(len(groups)):
                        for r in range(model.q):
                            rate+=b[h][z][r][s][t]*(c[h][r]-(h==z and r==s))
                    rate*=c[z][s]
                    assert rate>=0
                    if not rate: continue
                    nextstate=[list(v) for v in c];nextstate[z][s]-=1;nextstate[z][t]+=1
                    j=idx[tuple(map(tuple,nextstate))]
                    dest[j]=dest.get(j,F(0))+rate
                    exit_rate+=rate
        Q.append((dest,exit_rate))
        if exit_rate>max_exit:max_exit=exit_rate
    lam=ceil(max_exit)
    assert lam>0
    P=[];nnz=0
    for i,(edges,exit_rate) in enumerate(Q):
        p={j:v/lam for j,v in edges.items()}
        p[i]=1-exit_rate/lam
        assert all(x>=0 for x in p.values()) and sum(p.values())==1
        p={j:v for j,v in p.items() if v!=0};nnz+=len(p)
        P.append(tuple(p.items()))
    return P,states,idx,lam,nnz,exact_eta(model,groups,a,b)

def exp_enclosure(x,M):
    """Exact rational lower and upper bound on e^-x from positive Taylor."""
    term=F(1);S=term
    for j in range(1,M+1):
        term=term*x/j
        S+=term
    nextterm=term*x/(M+1)
    assert F(M+2)>x
    tail=nextterm/(1-x/F(M+2))
    return 1/(S+tail),1/S,tail

def verify_policy(model,groups,initial_counts,time_horizon=F('2.6'),K=155,M=170,bits=80):
    t0=perf_counter()
    P,states,idx,lam,nnz,eta=make_rational_uniformized(model,groups)
    x=lam*time_horizon
    assert F(K+2)>x and M+2>x
    e_lo,e_hi,exp_tail=exp_enclosure(x,M)
    poisson_term=x**(K+1)/prod(range(1,K+2))
    poisson_tail_hi=poisson_term/(1-x/F(K+2)) # e^-x < 1
    S=1<<bits
    p=[0]*len(states);p[idx[initial_counts]]=S
    A=F(0);weight=F(1);mul_count=0
    for k in range(K+1):
        infected0=sum(p[j] for j,c in enumerate(states) if all(y[1]==0 for y in c))
        A+=weight*infected0/S
        if k==K:break
        pnext=[0]*len(states)
        for i,v in enumerate(p):
            if not v:continue
            for j,rat in P[i]:
                pnext[j]+=(v*rat.numerator)//rat.denominator
                mul_count+=1
        p=pnext
        weight=weight*x/(k+1)
    round_err=F(K*nnz,S)
    low=e_lo*A
    hi=e_hi*A+round_err+poisson_tail_hi
    assert low<=hi and hi<=1
    with localcontext() as c:
        c.prec=38
        conv=lambda v: str(Decimal(v.numerator)/Decimal(v.denominator))
        return {'lower':conv(low),'upper':conv(hi),
                'width':conv(hi-low),'eta_exact':conv(eta),
                'perturbation_halfwidth':conv(eta**2*time_horizon**2),
                'poisson_tail_upper':conv(poisson_tail_hi),
                'integer_round_error_upper':conv(round_err),
                'exp_positive_series_tail_upper':conv(exp_tail),
                'states':len(states),'lambda':lam,'K':K,'M':M,
                'fixed_point_bits':bits,'matrix_nnz':nnz,
                'floor_multiplications':mul_count,'rational_build_and_verify_seconds':perf_counter()-t0}

if __name__=='__main__':
    from experiments import create_sis,discover,counts_initial,distributed_hetero,uniform_recovery_policy
    import json
    from pathlib import Path
    large,_=create_sis([9,8,8],rates=([.29,.35,.31],[[.042,.012,0],[.01,.055,.016],[0,.013,.049]]))
    gl,_=discover(large)
    counts,_=counts_initial(gl,large.q,[0,9,17])
    disturbed=distributed_hetero(large,gl,0.0057)
    treated=uniform_recovery_policy(disturbed,gl[0],0.08)
    results={'ordinary_no_treatment':verify_policy(disturbed,gl,counts),
             'treated':verify_policy(treated,gl,counts)}
    for label,obj in results.items():
        from decimal import Decimal
        l=Decimal(obj['lower'])-Decimal(obj['perturbation_halfwidth'])
        u=Decimal(obj['upper'])+Decimal(obj['perturbation_halfwidth'])
        obj['true_observable_interval']=[str(max(Decimal(0),l)),str(min(Decimal(1),u))]
        print(label,'projected',obj['lower'],obj['upper'],'actual',obj['true_observable_interval'],
              'time',obj['rational_build_and_verify_seconds'],'mults',obj['floor_multiplications'])
    Path(__file__).with_name('verified_results.json').write_text(json.dumps(results,indent=2))
