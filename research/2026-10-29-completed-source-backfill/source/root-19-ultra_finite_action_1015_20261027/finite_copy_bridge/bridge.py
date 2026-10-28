#!/usr/bin/env python3
"""Finite-count interface of arXiv:2506.06590v1's five-reaction majority.

All species are abstract, non-biological states. This is not a chemical recipe.
Exact rational recursions are independent of the numerical CTMC propagation.
The ordinary six-state comparator is a known population protocol, not invention.
"""
from __future__ import annotations
from collections import deque
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import math
import sys
import time

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
VENDOR = WORKSPACE / 'work/sol6_openings_20261027/independent_opening/vendor'
if VENDOR.is_dir():
    sys.path.insert(0, str(VENDOR))


def exact_source_limit(a: int, b: int, c0: int, volume: int,
                       rates=(1, 1, 1, 1, 1)):
    """Limiting probability that one reporter is YES, for either initial vote.

    Reactions A+N->A+Y; B+Y->B+N; A+B->waste;
    C+Y->C+N; 3C->waste. The last propensity is
    k5*c*(c-1)*(c-2)/volume**2, with no 1/6 factor.
    This convention has mean-field dC/dt=-3*k5*C**3.
    Each of M reporters has this same marginal probability.
    """
    k1, k2, k3, k4, k5 = map(F, rates)
    vol = F(volume)
    d = a - b
    r = c0 % 3

    @lru_cache(None)
    def rec(j, c):
        aa, bb = j + max(d, 0), j + max(-d, 0)
        ann = k3 * aa * bb / vol
        clk = k5 * c * (c-1) * (c-2) / vol**2 if c >= 3 else F(0)
        up, down = k1 * aa / vol, (k2 * bb + k4 * c) / vol
        if not ann and not clk:
            if up + down:
                p = up / (up + down)
                return (p, p)
            return (F(0), F(1))  # no catalyst: current vote freezes
        rhs0 = rhs1 = F(0)
        if ann:
            lo = rec(j-1, c)
            rhs0 += ann * lo[0]
            rhs1 += ann * lo[1]
        if clk:
            lo = rec(j, c-3)
            rhs0 += clk * lo[0]
            rhs1 += clk * lo[1]
        q0, q1 = ann + clk + up, ann + clk + down
        det = q0 * q1 - up * down
        ans = ((rhs0*q1 + up*rhs1)/det,
               (q0*rhs1 + down*rhs0)/det)
        assert all(0 <= z <= 1 for z in ans)
        # Replay both original equations with exact rational arithmetic.
        assert q0*ans[0] - up*ans[1] == rhs0
        assert q1*ans[1] - down*ans[0] == rhs1
        return ans

    answer = rec(min(a, b), c0)
    return {'p_yes_given_initial_no': answer[0],
            'p_yes_given_initial_yes': answer[1],
            'clock_residue': r, 'blocks': rec.cache_info().currsize}


def source_generator(a, b, c0, volume, rates=(1,1,1,1,1)):
    """Full reporter + independent upstream CTMC; no trajectory sampling."""
    import numpy as np
    from scipy.sparse import csr_matrix
    k1,k2,k3,k4,k5 = rates
    d = a-b
    states = [(j,c,y) for j in range(min(a,b)+1)
              for c in range(c0%3,c0+1,3) for y in (0,1)]
    ix = {s:i for i,s in enumerate(states)}
    rows, cols, vals = [], [], []
    for i,(j,c,y) in enumerate(states):
        aa,bb = j+max(d,0), j+max(-d,0)
        edges=[]
        if aa and bb: edges.append(((j-1,c,y), k3*aa*bb/volume))
        if c>=3: edges.append(((j,c-3,y),k5*c*(c-1)*(c-2)/volume**2))
        if y==0 and aa: edges.append(((j,c,1),k1*aa/volume))
        if y==1 and (bb or c): edges.append(((j,c,0),(k2*bb+k4*c)/volume))
        total=sum(q for _,q in edges)
        for s,q in edges:
            rows.append(i);cols.append(ix[s]);vals.append(q)
        rows.append(i);cols.append(i);vals.append(-total)
    Q=csr_matrix((vals,(rows,cols)),shape=(len(states),len(states)))
    assert np.max(np.abs(np.asarray(Q.sum(axis=1)))) < 1e-12
    p0=np.zeros(len(states));p0[ix[(min(a,b),c0,1)]]=1
    yes=np.array([s[2] for s in states],float)
    return Q,p0,yes


# Ordinary known six-state strong/weak protocol, states P,N,Z,p,n,z.
# P,N,Z have signed weights +1,-1,0; weak states all have weight zero.
SIX_RULES = [
    ((0,1),(2,2)),  # P+N -> 2Z (exact primary table: two strong zeroes)
    ((0,2),(0,3)),  # P+Z -> P+p
    ((1,2),(1,4)),  # N+Z -> N+n
    ((0,4),(0,3)), ((0,5),(0,3)),
    ((1,3),(1,4)), ((1,5),(1,4)),
    ((2,3),(2,5)), ((2,4),(2,5)),
]


def six_generator(a,b,spare,volume,rates=None):
    """Enumerate the entire reachable count process for the matched input."""
    import numpy as np
    from scipy.sparse import csr_matrix
    if rates is None: rates=[1.0]*len(SIX_RULES)
    assert len(rates)==len(SIX_RULES) and min(rates)>0
    initial=(a,b,0,0,0,spare)
    states=[initial];ix={initial:0};queue=deque([initial]); all_edges=[]
    while queue:
        s=queue.popleft();edges=[]
        for (reactants,products),k in zip(SIX_RULES,rates):
            i,j=reactants
            if not s[i] or not s[j]: continue
            t=list(s);t[i]-=1;t[j]-=1
            for z in products:t[z]+=1
            t=tuple(t)
            assert sum(t)==sum(initial) and t[0]-t[1]==a-b
            if t not in ix:
                ix[t]=len(states);states.append(t);queue.append(t)
            edges.append((ix[t],k*s[i]*s[j]/volume))
        all_edges.append(edges)
    rows=[];cols=[];vals=[]
    for i,edges in enumerate(all_edges):
        total=0
        for j,q in edges:
            rows.append(i);cols.append(j);vals.append(q);total+=q
        rows.append(i);cols.append(i);vals.append(-total)
    Q=csr_matrix((vals,(rows,cols)),shape=(len(states),len(states)))
    assert np.max(np.abs(np.asarray(Q.sum(axis=1))))<1e-11
    total=sum(initial);truth=a>b
    wrong=np.array([(s[1]+s[2]+s[4]+s[5] if truth else s[0]+s[3])/total
                    for s in states])
    nonconsensus=(wrong>0).astype(float)
    # Correct binary consensus cannot subsequently produce a wrong voter.
    for i,edges in enumerate(all_edges):
        if not nonconsensus[i]:
            assert all(not nonconsensus[j] for j,_ in edges)
    # Every state has a path to correct binary consensus (finite-graph check).
    reverse=[[] for _ in states]
    for i,edges in enumerate(all_edges):
        for j,_ in edges: reverse[j].append(i)
    reached={i for i,x in enumerate(nonconsensus) if not x}; q=deque(reached)
    while q:
        for j in reverse[q.popleft()]:
            if j not in reached:reached.add(j);q.append(j)
    assert len(reached)==len(states)
    p0=np.zeros(len(states));p0[0]=1
    return Q,p0,wrong,nonconsensus,states


def six_deadline(a,b,total,volume,kmin,eps):
    """Analytic upper bound, not fitted from numerical propagation.

    Annihilation time is a sum of independent exponentials. Use its mgf
    at half the smallest rate; then two conservative coupon-clearance phases.
    """
    m=min(a,b);d=abs(a-b)
    if m:
        theta=kmin*(d+1)/(2*volume)
        log_mgf=sum(-math.log1p(-theta/(kmin*j*(j+d)/volume))
                    for j in range(1,m+1))
        tann=(log_mgf+math.log(3/eps))/theta
        eann=sum(volume/(kmin*j*(j+d)) for j in range(1,m+1))
    else:tann=eann=0.0
    alpha=kmin*max(1,d)/volume
    clearance=2*math.log(3*total/eps)/alpha
    mean_bound=eann+2*volume*sum(1/j for j in range(1,total+1))/(kmin*max(1,d))
    return {'epsilon':eps,'deadline':tann+clearance,
            'annihilation_deadline':tann,'two_clearance_deadline':clearance,
            'mean_stabilization_upper_bound':mean_bound,
            'rate_lower_bound':kmin,
            'event_count_upper_bound':len(SIX_RULES)*total**2/volume*mean_bound}


def numeric_comparisons():
    import numpy as np
    from scipy.sparse.linalg import expm_multiply, spsolve
    out=[]
    for a,b,c in [(2,2,3),(3,2,3),(2,3,3),(2,2,4),(3,2,4),(2,3,4)]:
        M=1;volume=a+b+c+M
        Q,p0,yes=source_generator(a,b,c,volume)
        Q6,p6,w6,nc6,states=six_generator(a,b,c+M,volume)
        rows=[]
        for t in [1,10,100,1000]:
            p=expm_multiply(Q.T*t,p0,traceA=float(Q.diagonal().sum()*t))
            ps=expm_multiply(Q6.T*t,p6,traceA=float(Q6.diagonal().sum()*t))
            assert abs(p.sum()-1)<1e-10 and abs(ps.sum()-1)<1e-10
            py=float(p@yes)
            rows.append({'time':t,'source_random_reporter_error':1-py if a>b else py,
                         'ordinary_random_molecule_error':float(ps@w6),
                         'ordinary_not_unanimously_correct_probability':float(ps@nc6)})
        transient=np.flatnonzero(nc6)
        if len(transient):
            means=spsolve(-Q6[transient][:,transient],np.ones(len(transient)))
            mean=float(means[list(transient).index(0)]) if 0 in transient else 0.0
            event_rhs=-Q6.diagonal()[transient]
            events=spsolve(-Q6[transient][:,transient],event_rhs)
            mean_events=float(events[list(transient).index(0)]) if 0 in transient else 0.0
            residual=float(np.max(np.abs((-Q6[transient][:,transient])@means-1)))
        else:mean=mean_events=residual=0.0
        exact=exact_source_limit(a,b,c,volume)
        py=exact['p_yes_given_initial_yes']
        bound=six_deadline(a,b,volume,volume,1.0,0.01)
        pd=expm_multiply(Q6.T*bound['deadline'],p6,
                         traceA=float(Q6.diagonal().sum()*bound['deadline']))
        out.append({'a':a,'b':b,'clock':c,'reporters':M,'same_volume_and_initial_total_count':volume,
                    'source_states':len(p0),'ordinary_states':len(p6),
                    'source_limiting_error_exact':str(1-py if a>b else py),
                    'ordinary_limiting_error_exact':'0 (proved all finite inputs)',
                    'ordinary_mean_binary_stabilization_time':mean,
                    'ordinary_mean_nonidentity_events_to_binary_stabilization':mean_events,
                    'ordinary_mean_equation_residual':residual,'deadline_certificate':bound,
                    'ordinary_actual_error_at_certificate_deadline':float(pd@nc6),
                    'time_curve':rows})
    return out


def main():
    started=time.perf_counter()
    # Analytic two-by-two recursion values also hand-derived in PROOF.md.
    small=exact_source_limit(1,1,3,1)
    assert small['p_yes_given_initial_yes']==F(34,63)
    assert small['p_yes_given_initial_no']==F(20,63)
    residual=exact_source_limit(2,1,4,1)
    assert residual['p_yes_given_initial_yes']==F(1,2)
    assert residual['p_yes_given_initial_no']==F(1,2)
    exact_checks=[]
    for V in [6,12,18,24]:
        z=exact_source_limit(V//2,V//2,V,V)
        exact_checks.append({'volume':V,'a':V//2,'b':V//2,'C':V,'initial_Y':'all',
                             'limiting_wrong_random_reporter_probability':str(z['p_yes_given_initial_yes']),
                             'decimal':float(z['p_yes_given_initial_yes']),
                             'recursion_blocks':z['blocks']})
    result={'status':'FINITE_COPY_BRIDGE_AND_ORDINARY_REPAIR_CONSTRUCTED; NO_NEW_DEVICE_OR_ADVANTAGE',
            'source_version':'https://arxiv.org/html/2506.06590v1',
            'stochastic_convention':'falling-factorial propensity k*c*(c-1)*(c-2)/V^2 for3C; hence fluid drift-3k C^3',
            'hand_exact_checks':{k:str(v) for k,v in small.items()},
            'scaled_tie_errors':exact_checks,'matched_full_process_comparisons':numeric_comparisons(),
            'wall_seconds':time.perf_counter()-started,
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
