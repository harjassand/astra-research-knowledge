#!/usr/bin/env python3
"""Small discriminating algebra checks; these do not independently audit proofs."""
from fractions import Fraction as F
from itertools import product
from math import prod, factorial
from pathlib import Path
import json
from support_receiver_certificate import diagnostic as support_fixture, acquire as support_acquire
from reciprocal_bath_certificate import diagnostic as bath_fixture, acquire as bath_acquire, inspect as bath_inspect

P=Path(__file__).resolve().parent
def decode(x):return F(int(x['numerator'],0) if x['numerator'].startswith(('0x','-0x')) else int(x['numerator']),int(x['denominator'],0) if x['denominator'].startswith('0x') else int(x['denominator']))
def ff(a,b):return 0 if a<b else prod(range(a-b+1,a+1))
def falling(x,y):return prod(ff(a,b) for a,b in zip(x,y))
def states(d,nmax):
    for x in product(range(nmax+1),repeat=d):
        if sum(x)<=nmax:yield x
def rank(rows):
    rows=[list(map(F,r)) for r in rows];r=0
    for c in range(len(rows[0])):
        hit=next((i for i in range(r,len(rows)) if rows[i][c]),None)
        if hit is None:continue
        rows[r],rows[hit]=rows[hit],rows[r];pivot=rows[r][c];rows[r]=[v/pivot for v in rows[r]]
        for i in range(len(rows)):
            if i!=r:
                cc=rows[i][c];rows[i]=[a-cc*b for a,b in zip(rows[i],rows[r])]
        r+=1
    return r
def graph_counts(raw):
    vertices={v for y,z,c in raw for v in [y,z]};adj={v:set() for v in vertices}
    for y,z,c in raw:adj[y].add(z);adj[z].add(y)
    count=0;seen=set()
    for v in vertices:
        if v in seen:continue
        count+=1;todo=[v];seen.add(v)
        while todo:
            a=todo.pop()
            for b in adj[a]-seen:seen.add(b);todo.append(b)
    rr=rank([tuple(b-a for a,b in zip(y,z)) for y,z,c in raw])
    return {'complexes':len(vertices),'linkages':count,'rank':rr,'deficiency':len(vertices)-count-rr}
def balance_at(raw,c):
    balances={v:F(0) for y,z,k in raw for v in [y,z]}
    for y,z,k in raw:
        flux=F(k)*prod(ci**yi for ci,yi in zip(c,y));balances[y]-=flux;balances[z]+=flux
    return all(v==0 for v in balances.values())
def overlap(alpha=(1,1,1,2),beta=(1,1,1,3)):
    C=[(0,0,0),(1,1,0),(2,1,1),(3,2,2)]
    I=[(tuple(y)+(0,),tuple(C[(i+1)%4])+(0,),F(alpha[i])) for i,y in enumerate(C)]
    II=[((0,)+tuple(y),(0,)+tuple(C[(i+1)%4]),F(beta[i])) for i,y in enumerate(C)]
    return I+II
def word(raw,x,indices):
    x=tuple(x)
    for i in indices:
        y,z,k=raw[i];assert falling(x,y)>0
        x=tuple(a-b+c for a,b,c in zip(x,y,z))
    return x
def normalized_generator(raw,x,t,g):
    gx=g(x);N=sum(x);ans=F(0)
    for y,z,k in raw:
        rate=F(k)*falling(x,y)
        if rate:
            xx=tuple(a-b+c for a,b,c in zip(x,y,z));ans+=rate*(t**(sum(xx)-N)*g(xx)-gx)
    return ans

def main():
    checks={};factor_checks=0
    for a in [0,1,2]:
        raw=support_fixture(a);cert=support_acquire(raw);assert cert['quantitative_status']=='GLOBAL_RETURN_REWARD_HEAD_ACQUIRED'
        assert graph_counts(raw)=={'complexes':7,'linkages':2,'rank':4,'deficiency':1}
        unit=[(y,z,1) for y,z,k in raw];assert balance_at(unit,(F(1),)*4)
        assert not balance_at(raw,(F(1),)*4)
        for x in states(4,7):
            for y,z,k in raw[2:]:
                if a and x[0]<a:assert falling(x,y)==0
                else:
                    xx=(x[0]-a,)+x[1:];yy=(y[0]-a,)+y[1:]
                    assert falling(x,y)==ff(x[0],a)*falling(xx,yy)
                factor_checks+=1
    checks['exact_factorial_clock_equalities']=factor_checks
    checks['support_scope_and_poisson_controls']='PASS; support constructor also checks unsupported support and budget refusal in its own main'

    total=0;heads=[]
    for h in [1,2,3]:
        raw=bath_fixture(h);cert=bath_acquire(raw);assert cert['quantitative_status']=='GLOBAL_FOSTER_HEAD_ACQUIRED'
        info=bath_inspect(raw);t=decode(cert['t']);cc=decode(cert['c']);ee=decode(cert['e']);pp=cert['p'];C0=decode(cert['C_0'])
        CH=decode(cert['C_H']);mu=info['mu'];dt=1-1/t
        def gg(x):return 1+cc/F((x[0]+1)**pp)+ee*sum(F(1,a+1) for a in x[1:])
        oriented=[]
        for i,j,aa,bb,ggg,dd in info['edges']:
            oriented.extend([(i,j,ggg/4),(j,i,aa/4)])
        def bound(x):
            if x[0]==0:return F(-1)
            dp=F(1,(x[0]+1)**pp)-F(1,(x[0]+2)**pp)
            return C0-3*mu*dt*x[0]/4-cc*sum(bb*x[0]*dp*x[i] for i,aa,bb in info['arms'])-ee*sum(ci*F(x[j],x[i]+1)**2 for i,j,ci in oriented)
        for x in states(h+1,9):
            actual=normalized_generator(raw,x,t,gg);assert actual<=bound(x),(h,x,actual,bound(x));total+=1
        head=int(decode(cert['head_N']));heads.append({'hidden_count':h,'head_bits':head.bit_length()})
        large=[]
        for i in range(h+1):
            x=[0]*(h+1);x[i]=2*head+1;large.append(tuple(x))
            if i:
                x[0]=1;large.append(tuple(x))
        large.extend([tuple([j]+[2*head+1]*h) for j in [0,1,2,cert['K_A']]])
        for x in large:
            actual=normalized_generator(raw,x,t,gg);assert actual<=-1,(h,x);total+=1
    checks['full_generator_inequalities_including_zero_faces']=total
    checks['bath_head_sizes']=heads

    raw=overlap();assert graph_counts(raw)=={'complexes':7,'linkages':1,'rank':4,'deficiency':2}
    assert balance_at(overlap((1,1,1,1),(1,1,1,1)),(F(1),)*4)
    a,b,c=F(2),F(1,2),F(1,2);assert (b,c)!=(F(3),F(1,3))
    ratio_count=0
    for A,B,C,D in product([3,4,9,30],[3,4,7],[2,3],[2,5,101]):
        x=(A,B,C,D);rates=[k*falling(x,y) for y,z,k in raw]
        assert rates[2]/rates[6]==F(A*(A-1),(B-1)*D)
        assert rates[3]/rates[7]==F(2,3)*F(A*(A-1)*(A-2),(B-2)*D*(D-1))
        ratio_count+=2
    for a,d in product(range(4),range(1,5)):
        assert word(raw,(a,0,0,d),[0,1,5,6,7])==(a+2,0,0,d)
        x=(a+2,1,3,d);assert word(raw,x,[2,6,7])==(a+3,0,3,d-1)
    checks['overlap_exact_competition_ratios']=ratio_count
    checks['overlap_words_and_complex_balance_baseline']='PASS; no general return or typical-scale claim follows'
    checks['scope']='same-principal finite algebra diagnostics, not independent audit or full-family recurrence proof'
    (P/'results'/'construction_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
