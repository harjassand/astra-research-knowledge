#!/usr/bin/env python3
"""Exact Laurent boundary drift for the actual embedded count chain.

This retains every raw competing reaction and every actual changed count.
It is a diagnostic, not a substitution of jump count for physical time.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import random,json
from coverability_clock import cubic

P=Path(__file__).resolve().parent

def addpoly(a,b):
    c=[F(0)]*max(len(a),len(b))
    for j,x in enumerate(a):c[j]+=x
    for j,x in enumerate(b):c[j]+=x
    return c

def mulpoly(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def conv(a,b,M):
    c=[F(0)]*(M+1)
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b[:M+1-i]):
            if y:c[i+j]+=x*y
    return c

def rate_poly(state,source,k):
    a,db,c=state;aa,bb,cc=source
    if a<aa or c<cc:return [F(0)]
    out=[k]
    for q in range(aa):out[0]*=a-q
    for q in range(cc):out[0]*=c-q
    for q in range(bb):out=mulpoly(out,[F(db-q),F(1)])
    return out

def transitions(raw,state,M):
    polys=[rate_poly(state,y,k) for y,z,k in raw]
    q=[F(0)]
    for pol in polys:q=addpoly(q,pol)
    while len(q)>1 and not q[-1]:q.pop()
    d=len(q)-1
    if not q[-1]:return []
    inv=[1/q[-1]]
    for j in range(1,M+1):
        inv.append(-sum(q[d-i]*inv[j-i] for i in range(1,min(j,d)+1))/q[-1])
    out=[]
    for (y,z,k),pol in zip(raw,polys):
        if not any(pol):continue
        pr=[F(0)]*(M+1)
        for deg,co in enumerate(pol):
            start=d-deg
            for j in range(start,M+1):pr[j]+=co*inv[j-start]
        dst=tuple(a-u+v for a,u,v in zip(state,y,z))
        assert dst[0]>=0 and dst[2]>=0
        out.append((dst,pr))
    assert all(sum(v[j] for s,v in out)==(1 if j==0 else 0) for j in range(M+1))
    return out

def maxlevel(raw,state):
    a,db,c=state
    return max((y[1] for y,z,k in raw if a>=y[0] and c>=y[2]),default=0)

def drift_steps(raw,a,c,K=8,M=6):
    start=(a,0,c);base=-maxlevel(raw,start);dist={start:[F(1)]+[F(0)]*M};cache={};rows=[]
    for step in range(1,K+1):
        nxt={}
        for state,prob in dist.items():
            if state not in cache:cache[state]=transitions(raw,state,M)
            for dst,pr in cache[state]:
                if dst not in nxt:nxt[dst]=[F(0)]*(M+1)
                term=conv(prob,pr,M)
                nxt[dst]=[x+y for x,y in zip(nxt[dst],term)]
        dist=nxt
        drift=[F(0)]*(M+1)
        for state,prob in dist.items():
            delta=state[1]-maxlevel(raw,state)-base
            for j,v in enumerate(prob):drift[j]+=delta*v
        first=next((j for j,v in enumerate(drift) if v),None)
        rows.append({'steps':step,'states':len(dist),'order':first,
                     'leading':str(drift[first]) if first is not None else 'UNRESOLVED_TO_ORDER_'+str(M),
                     'sign':0 if first is None else (1 if drift[first]>0 else -1)})
    return rows

if __name__=='__main__':
    fixtures={'coupled_cubic':cubic(),
              'neutral_rank_one':[((1,2,0),(0,1,2),F(1)),((0,1,2),(1,2,0),F(1)),((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1))],
              'residual_one_step_failure':[((1,2,0),(0,2,1),F(4)),((0,2,1),(0,1,2),F(1)),((0,1,2),(1,2,0),F(7)),((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1))]}
    results=[]
    for name,raw in fixtures.items():
        for a,c in [(0,0),(1,0),(2,0),(3,0),(0,1)]:
            rows=drift_steps(raw,a,c)
            results.append({'fixture':name,'a':a,'c':c,'rows':rows})
            print(name,a,c,[(r['steps'],r['order'],r['sign']) for r in rows],flush=True)
    (P/'results/residual_steps.json').write_text(json.dumps({'scope':'Exact finite-k Laurent diagnostic for embedded drift. Physical-time and full asymptotic recurrence remain separate.','order':6,'results':results},indent=2)+'\n')
