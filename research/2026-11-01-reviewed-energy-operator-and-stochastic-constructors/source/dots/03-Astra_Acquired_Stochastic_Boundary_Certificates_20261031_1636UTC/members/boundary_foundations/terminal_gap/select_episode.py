#!/usr/bin/env python3
"""Acquired finite-episode selector using exact rational log intervals."""
from fractions import Fraction as F
from collections import deque
import json, math
from exact_terminal_gap import linkage_classes, cycle

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(q,a):
    assert q>=0
    return (q*a[0],q*a[1])

def _log_unit_interval(q,tol):
    """1<=q<=2; exact atanh series, rigorous positive remainder bound."""
    assert 1<=q<=2 and tol>0
    t=(q-1)/(q+1); z=t; total=F(0); j=0
    while True:
        total+=2*z/(2*j+1)
        j+=1; z*=t*t
        remainder=2*z/((2*j+1)*(1-t*t))
        if remainder<=tol:return (total,total+remainder),j

def log_interval(q,tol):
    q=F(q);tol=F(tol);assert q>0 and tol>0
    k=q.numerator.bit_length()-q.denominator.bit_length()
    twok=F(2**k) if k>=0 else F(1,2**(-k))
    z=q/twok
    while z<1:z*=2;k-=1
    while z>=2:z/=2;k+=1
    eps=tol/(abs(k)+1)
    iz,nz=_log_unit_interval(z,eps)
    i2,n2=_log_unit_interval(F(2),eps)
    if k>=0:out=add(iz,mul(k,i2))
    else:out=add(iz,(-(-k)*i2[1],-(-k)*i2[0]))
    assert out[1]-out[0]<=tol
    return out,nz+n2

def falling(x,y):
    out=1
    for a,b in zip(x,y):
        if a<b:return 0
        for k in range(b):out*=a-k
    return out

def select(reactions,x,t,width=F(1,4)):
    """reactions are (source,target,positive rational rate); x>=carried t."""
    reactions=[(tuple(s),tuple(u),F(k)) for s,u,k in reactions if tuple(s)!=tuple(u)]
    assert all(k>0 for s,u,k in reactions)
    edges=[(s,u) for s,u,k in reactions]
    C,Ls,wr=linkage_classes(edges);assert wr
    x=tuple(x);t=tuple(t);assert all(a>=b for a,b in zip(x,t))
    L=next(L for L in Ls if t in L);rho=tuple(a-b for a,b in zip(x,t));M=len(L)
    rates={s:F(0) for s in C};edge_rate={}
    for s,u,k in reactions:rates[s]+=k;edge_rate[s,u]=edge_rate.get((s,u),F(0))+k
    # Canonical BFS paths. Exact parallel channels may be combined.
    paths={t:[t]};queue=deque([t])
    while queue:
        y=queue.popleft()
        for u in sorted(v for a,v in edge_rate if a==y):
            if u not in paths:paths[u]=paths[y]+[u];queue.append(u)
    phase={};terms=0;log_calls=0
    for y in L:
        pop=tuple(a+b for a,b in zip(rho,y));ff={s:falling(pop,s) for s in C}
        lam=sum(rates[s]*ff[s] for s in C);assert lam>0 and ff[y]>0
        delta=(F(0),F(0))
        for s in C:
            if not ff[s]:continue
            li,n=log_interval(F(ff[y],ff[s]),width/(2*M))
            terms+=n;log_calls+=1;delta=add(delta,mul(rates[s]*ff[s]/lam,li))
        phase[y]=(delta,rates[y]*ff[y]/lam)
    choices=[]
    for c in L:
        path=paths[c];J=phase[c][0]
        for j in range(len(path)-2,-1,-1):
            y,u=path[j],path[j+1]
            J=add(phase[y][0],mul(edge_rate[y,u]/rates[y]*phase[y][1],J))
        assert J[1]-J[0]<=width
        choices.append((sum(J)/2,c,path,J))
    _,c,path,J=min(choices)
    def outward(interval):
        scale=2**24
        lo=(interval[0]*scale).__floor__()
        hi=(interval[1]*scale).__ceil__()
        return (F(lo,scale),F(hi,scale))
    raw_J=J;J=outward(J)
    assert J[1]-J[0]<=width
    max_bits=max(max(q.numerator.bit_length(),q.denominator.bit_length()) for _,_,_,z in choices for q in z)
    return {'terminal':c,'path':path,'reward_interval':list(map(str,J)),
      'reward_midpoint':float(sum(J)/2),'certified_width':str(J[1]-J[0]),
      'all_episode_intervals':[{'terminal':c,'path':p,'interval':list(map(str,outward(j)))} for _,c,p,j in choices],
      'work':{'largest_final_fraction_bits_before_outward_rounding':max_bits,'phase_evaluations':M,'log_interval_calls':log_calls,'atanh_series_terms':terms,
              'path_edges_evaluated':sum(len(p)-1 for _,c,p,j in choices)}}

def main():
    C1=[(0,0,0),(1,1,0),(1,0,1),(0,1,1)]
    C2=[(1,0,0),(0,1,0),(0,0,1),(2,0,0)]
    raw=[(s,t,2 if s==(2,0,0) else 1) for s,t in cycle(C1)+cycle(C2)]
    results=[]
    for x,t in [((10,10,10),(1,1,0)),((1000,1000,1000),(1,1,0)),((10**100,10**100,10**100),(1,1,0)),((1000,0,0),(1,0,0)),((0,1000,0),(0,1,0))]:
        r=select(raw,x,t);results.append({'population':x,'target':t,**r})
    for q in [F(1,1024),F(3,7),F(1),F(2),F(19,2),F(2**100+1,3)]:
        inter,_=log_interval(q,F(1,10**12))
        # Floating comparison only consistency, the proof uses exact remainder.
        assert float(inter[0])-1e-13<=math.log(float(q))<=float(inter[1])+1e-13
    print(json.dumps({'executed_selectors':results,'log_formula_checks':6},indent=2))
if __name__=='__main__':main()
