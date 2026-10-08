#!/usr/bin/env python3
"""Standard-library replay of exact finite claims. Not a general proof checker."""
from fractions import Fraction
from itertools import product
from collections import deque
from pathlib import Path
import json
from compiler import Reaction, compile_network, propensity, falling
from serialize import serialize, encode, decode, positive_offset


def rank(rows):
    a=[[Fraction(v) for v in row] for row in rows]
    r=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]
        p=a[r][col];a[r]=[v/p for v in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][col]:
                c=a[i][col];a[i]=[v-c*w for v,w in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r


def reachable(start,rs,limit=200000):
    seen={start};q=deque([start])
    while q:
        x=q.popleft()
        for r in rs:
            if all(a>=b for a,b in zip(x,r.source)):
                y=tuple(a+b for a,b in zip(x,r.change))
                if y not in seen:
                    seen.add(y);q.append(y)
                    if len(seen)>limit:raise RuntimeError('Fixture not completed.')
    return seen


def main():
    stats={'generator_fixtures':0,'direction_fixtures':0,'rank_fixtures':0,
           'parity_fixtures':0,'clock_fixtures':0,'reachability_fixtures':[]}
    inputs=[[Reaction((2,),(3,))],
            [Reaction((0,0),(0,1)),Reaction((0,1),(1,0),Fraction(4)),Reaction((1,2),(0,0))],
            [Reaction((3,0),(0,3)),Reaction((0,2),(2,0))]]
    for orig in inputs:
        host,meta=compile_network(orig)
        d=len(orig[0].source);n=d+2
        assert rank([r.change for r in host])==n
        stats['rank_fixtures']+=1
        for x in product(range(6),repeat=d):
            z=x+(1,1)
            assert [propensity(r,x) for r in orig]==[propensity(r,z) for r in host[:len(orig)]]
            assert all(propensity(r,z)==0 for r in host[len(orig):])
            stats['generator_fixtures']+=1
        for w in product(range(-3,4),repeat=n):
            if not any(w):continue
            scores=[sum(a*b for a,b in zip(w,r.source)) for r in host]
            h=max(scores)
            drift=[sum(a*b for a,b in zip(w,r.change)) for r,s in zip(host,scores) if s==h]
            assert max(drift)<=0 and min(drift)<0
            stats['direction_fixtures']+=1
    q=Fraction(9,10);c=Fraction(103,3645)
    assert q**(-3)-1+4*(q-1)==-c
    for a,b in product(range(32),range(32)):
        P=b%2;W=Fraction(a)-Fraction(b,2)+P
        dw_birth=Fraction(-1,2)+1-2*P
        dw_convert=Fraction(3,2)+1-2*P
        drift=dw_birth+4*b*dw_convert
        assert drift==Fraction(1,2)+4*(b-P)*(Fraction(3,2)+(-1)**P)
        ratio=q**int(2*dw_birth)-1+4*b*(q**int(2*dw_convert)-1)
        assert ratio<=-c
        stats['parity_fixtures']+=1
        for p in range(4):
            factor=falling(a+p,p)
            assert falling(a+p,p+1)*falling(b,2)==factor*a*falling(b,2)
            stats['clock_fixtures']+=1
    fixtures=[([Reaction((3,0),(0,3)),Reaction((0,2),(2,0))],(5,0)),
              ([Reaction((2,1),(0,3)),Reaction((0,2),(2,0))],(4,1)),
              ([Reaction((4,0),(1,3)),Reaction((0,3),(3,0))],(5,0)),
              ([Reaction((1,0),(0,1)),Reaction((0,1),(1,0))],(3,0))]
    for orig,x0 in fixtures:
        ref=reachable(x0,orig);rs,meta=serialize(orig)
        states=reachable(encode(x0,meta),rs)
        idle=[x for x in states if x[meta['idle_index']]==1]
        assert {decode(x,meta) for x in idle}==ref
        assert all(encode(x,meta) in states for x in ref)
        shifted=positive_offset(rs)
        positive=reachable(tuple(v+1 for v in encode(x0,meta)),shifted)
        assert positive=={tuple(v+1 for v in x) for x in states}
        assert all(min(x)>=1 for x in positive)
        for payload,order in [(rs,5),(shifted,7)]:
            host,info=compile_network(payload)
            assert max(sum(r.source) for r in host)<=order
            assert max(sum(r.target) for r in host)<=order
        stats['reachability_fixtures'].append({'original':len(ref),'serialized':len(states),
                                               'positive':len(positive)})
    stats['status']='PASS: listed finite fixtures only; general proofs and novelty not certified'
    path=Path(__file__).resolve().parent/'core_replay_results.json'
    path.write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
