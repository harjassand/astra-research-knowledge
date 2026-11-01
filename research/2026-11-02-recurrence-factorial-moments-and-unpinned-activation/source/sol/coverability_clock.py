#!/usr/bin/env python3
"""Exact backward coverability and actual-clock word data.

The antichain algorithm is ordinary established Petri-net machinery. The
polynomial stopped-clock implication is proved separately, not by samples.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json, math

P=Path(__file__).resolve().parent

def le(a,b):return all(x<=y for x,y in zip(a,b))
def pre(y,z,b):return tuple(u+max(v-w,0) for u,w,v in zip(y,z,b))

def minimize(words):
    keys=sorted(words,key=lambda b:(sum(b),b))
    out={}
    for b in keys:
        if not any(le(a,b) for a in out):out[b]=words[b]
    return out

def acquire(raw,targets):
    words=minimize({tuple(t):() for t in targets});rounds=0;maxbasis=len(words);added=0
    while True:
        proposed=dict(words)
        for b,word in words.items():
            for k,(y,z,rate) in enumerate(raw):
                a=pre(y,z,b);candidate=(k,)+word
                if a not in proposed or len(candidate)<len(proposed[a]):proposed[a]=candidate
        new=minimize(proposed);rounds+=1;maxbasis=max(maxbasis,len(new))
        if set(new)==set(words):
            # Keep the shorter exact acquired words on the terminal basis.
            words=new;break
        added+=len(set(new)-set(words));words=new
    for b,word in words.items():
        x=b
        for k in word:
            y,z,rate=raw[k];assert le(y,x)
            x=tuple(a-u+v for a,u,v in zip(x,y,z));assert min(x)>=0
        assert any(le(t,x) for t in targets)
    return words,{'iterations':rounds,'max_basis':maxbasis,'new_basis_members':added}

def weakly_reversible(raw):
    vertices={v for y,z,k in raw for v in [y,z]}
    adj={v:set() for v in vertices}
    for y,z,k in raw:adj[y].add(z)
    for y,z,k in raw:
        seen={z};pending=[z]
        while pending:
            a=pending.pop()
            for b in adj[a]:
                if b not in seen:seen.add(b);pending.append(b)
        if y not in seen:return False
    return True

def falling(a,k):
    if a<k:return 0
    out=1
    for j in range(k):out*=a-j
    return out

def rate_at(x,y,k):
    q=k
    for a,b in zip(x,y):q*=falling(a,b)
    return q

def cubic():
    c=[(2,1,0),(0,2,1),(1,0,2),(1,1,1)]
    return [(c[i],c[(i+1)%4],F(k)) for i,k in enumerate([1,2,3,5])]+[((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1))]

if __name__=='__main__':
    raw=cubic();assert weakly_reversible(raw)
    words,stats=acquire(raw,[(6,6,6)])
    # Challenge actual enabling after many distinct large translations.
    translated=0
    for b,word in words.items():
        for shift in product([0,1,10,10000],repeat=3):
            x=tuple(a+c for a,c in zip(b,shift))
            for k in word:
                y,z,rate=raw[k];assert rate_at(x,y,rate)>0
                x=tuple(a-u+v for a,u,v in zip(x,y,z))
            assert le((6,6,6),x);translated+=1
    # An actual competing raw reaction cannot leave the acquired upward set.
    transitions=0
    for x in product(range(10),repeat=3):
        if not any(le(b,x) for b in words):continue
        for y,z,k in raw:
            if rate_at(x,y,k):
                out=tuple(a-u+v for a,u,v in zip(x,y,z))
                assert any(le(b,out) for b in words);transitions+=1
    L=max(1,max(map(len,words.values())))
    out={'scope':'Exact ordinary backward-coverability acquisition with actual raw words; translated enabling checks supplement the general monotonicity proof.',
         'raw_network':'2A+B -> 2B+C -> A+2C -> A+B+C -> 2A+B, rates 1,2,3,5; 0<->A unit rates',
         'target':[6,6,6],'weakly_reversible':True,'basis':[{'state':b,'word':w} for b,w in words.items()],
         'stats':stats,'L':L,'D':max(sum(y) for y,z,k in raw),'kmin':str(min(k for y,z,k in raw)),
         'rate_sum':str(sum(k for y,z,k in raw)),
         'translated_words_checked':translated,'actual_competing_transitions_checked':transitions,
         'stopped_clock':'E tau <= L/(kmin*(kmin/[S*(2N)^D])^L), stopping at target or actual shell exit',
         'global_return':'NOT_PROVED; weighted outward-exit contraction is not supplied by this clock'}
    (P/'results/coverability_clock.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='basis'},indent=2))
