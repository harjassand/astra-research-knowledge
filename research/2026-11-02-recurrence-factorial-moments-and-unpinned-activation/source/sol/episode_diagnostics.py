#!/usr/bin/env python3
"""Exact episode probabilities, actual clocks, and fixed-class obstruction checks.

These finite checks do not replace the universal proofs in the companion files.
"""
from fractions import Fraction as F
from collections import deque,defaultdict
from pathlib import Path
from math import prod
import json
import mpmath as mp

mp.mp.dps=50
P=Path(__file__).resolve().parent

def ordered():
    c=[(0,0,0),(1,1,0),(2,1,1),(3,2,2)]
    return [(c[i],c[(i+1)%4],F(1)) for i in range(4)]

def ack():
    c=[(1,0,0),(1,1,0),(1,0,1),(0,0,1),(0,2,0)]
    return [(c[i],c[(i+1)%5],F(1)) for i in range(5)]

def small():return [((0,0),(1,1),F(1)),((1,1),(0,1),F(2)),((0,1),(0,0),F(3))]

def rate(x,y,k):
    if any(a<b for a,b in zip(x,y)):return F(0)
    return k*prod(prod(range(a-b+1,a+1)) for a,b in zip(x,y))

def jump(x,e):
    y,z,k=e;assert rate(x,y,k)>0
    return tuple(a-u+v for a,u,v in zip(x,y,z))

def factorial_ratio(end,begin):
    r=F(1)
    for a,b in zip(end,begin):
        if a>b:r*=prod(range(b+1,a+1))
        elif a<b:r/=prod(range(a+1,b+1))
    return r

def mpf(r):return mp.mpf(r.numerator)/r.denominator

def path(raw,tag,terminal):
    queue=deque([tag]);back={tag:None}
    while queue:
        x=queue.popleft()
        if x==terminal:break
        for i,(y,z,k) in enumerate(raw):
            if y==x and z not in back:back[z]=(x,i);queue.append(z)
    assert terminal in back
    out=[];x=terminal
    while back[x] is not None:y,i=back[x];out.append(i);x=y
    return list(reversed(out))

def episode(raw,residual,tag,terminal,alpha=F(1,10),reward_r=mp.mpf('0.1')):
    word=path(raw,tag,terminal);x=tuple(a+b for a,b in zip(residual,tag));origin=x
    reach=F(1);branches=[];clock=F(0);relative_reward=mp.mpf(0)
    for phase in range(len(word)+1):
        rates=[rate(x,y,k) for y,z,k in raw];q=sum(rates);assert q>0
        clock+=reach/q
        relative_reward+=mpf(reach/q)*mp.exp(reward_r*(sum(x)-sum(origin)))
        designated=word[phase] if phase<len(word) else None
        for i,(e,r) in enumerate(zip(raw,rates)):
            if not r or i==designated:continue
            dst=jump(x,e);outres=tuple(a-b for a,b in zip(dst,e[1]));assert min(outres)>=0
            fr=factorial_ratio(outres,residual);pr=reach*r/q
            branches.append((pr,fr,dst,e[1]))
        if designated is not None:
            e=raw[designated];assert e[0]==tag
            reach*=rates[designated]/q;x=jump(x,e);tag=e[1]
    assert sum(p for p,ratio,dst,t in branches)==1
    mean=sum(mpf(p)*mp.log(mpf(ratio)) for p,ratio,dst,t in branches)
    mgf=sum(mpf(p)*mp.power(mpf(ratio),mpf(alpha)) for p,ratio,dst,t in branches)
    return {'terminal':terminal,'word':word,'branches':len(branches),'probability_sum_exact':'1',
            'mean_entropy_reward':str(mean),'alpha':str(alpha),'factorial_MGF_minus_one':str(mgf-1),
            'minimum_endpoint_factorial_ratio':str(min(r for p,r,dst,t in branches)),
            'maximum_endpoint_factorial_ratio':str(max(r for p,r,dst,t in branches)),
            'physical_mean_episode_time_exact':str(clock),
            'physical_exp_count_reward_relative_to_initial':str(relative_reward)},branches

def obstruction_words():
    raw=ordered();checked=0
    for b,c in [(1,0),(1,1),(2,7),(100,200),(0,1),(0,100)]:
        for word,delta,ok in [([0,1,1,3],(0,-1,0),b>=1),([0,0,1,3],(0,0,-1),c>=1)]:
            if not ok:continue
            x=(0,b,c)
            for i in word:x=jump(x,raw[i])
            assert x==tuple(a+d for a,d in zip((0,b,c),delta));checked+=1
    # Exact symbolic enabling conditions are in the proof; this checks witnesses.
    return checked

if __name__=='__main__':
    out=[]
    fixtures=[('prior_three_complex',small(),lambda n:(n,0),(0,0)),
              ('prior_coupled_ACK',ack(),lambda n:(n-1,1,0),(1,0,0)),
              ('ordered_unpinned_obstruction',ordered(),lambda n:(0,n,n),(0,0,0))]
    for name,raw,resfun,tag in fixtures:
        complexes=sorted({v for y,z,k in raw for v in [y,z]})
        for n in [10,1000,10**6]:
            rows=[]
            for terminal in complexes:
                r,branches=episode(raw,resfun(n),tag,terminal)
                if name=='ordered_unpinned_obstruction':assert all(fr>=1 for p,fr,dst,t in branches)
                rows.append(r)
            out.append({'fixture':name,'n':n,'episodes':rows})
            print(name,n,'min mean',min(float(r['mean_entropy_reward']) for r in rows),
                  'min MGF-1',min(float(r['factorial_MGF_minus_one']) for r in rows),flush=True)
    result={'scope':'Exact finite probability, factorial-ratio and clock identities; MGF values are 50-digit numerical diagnostics. General claims come from the companion proofs.',
            'fixed_class_deletion_witness_checks':obstruction_words(),'results':out}
    (P/'results/episode_diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
