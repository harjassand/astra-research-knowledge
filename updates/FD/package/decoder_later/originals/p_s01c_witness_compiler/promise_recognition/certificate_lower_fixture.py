#!/usr/bin/env python3
"""Construct off-class completions of insufficient exact recognition transcripts."""
import json
from pathlib import Path
import random
from recognition_fixture import anf_degree

HERE=Path(__file__).resolve().parent


def topological(block,edges):
    remaining=set(block)
    result=[]
    while remaining:
        available=[x for x in remaining if not any(y in remaining and z==x for y,z in edges)]
        assert available
        x=min(available)
        result.append(x);remaining.remove(x)
    return result


def completion(n,h,edges):
    N=1 << n;L=1 << (n-h);B=1 << h
    reach=[0]*N
    for x,y in edges:reach[x]|=1 << y
    for k in range(N):
        for x in range(N):
            if reach[x] >> k & 1:reach[x]|=reach[k]
    choice=None
    for j in range(B-1):
        left=list(range(j*L,(j+1)*L));right=list(range((j+1)*L,(j+2)*L))
        pair=next(((u,v) for u in left for v in right if not (reach[u] >> v & 1)),None)
        if pair is None:continue
        u,v=pair
        above=[x for x in left if x==u or reach[u] >> x & 1]
        maxima=[x for x in above if not any(reach[x] >> y & 1 for y in left)]
        below=[x for x in right if x==v or reach[x] >> v & 1]
        minima=[x for x in below if not any(reach[y] >> x & 1 for y in right)]
        a,b=maxima[0],minima[0]
        assert not (reach[a] >> b & 1)
        choice=j,a,b
        break
    assert choice is not None,'insufficient transcript unexpectedly forces prefix order'
    boundary,a,b=choice
    order=[]
    for j in range(B):
        block=list(range(j*L,(j+1)*L))
        if j==boundary:ordered=topological([x for x in block if x!=a],edges)+[a]
        elif j==boundary+1:ordered=[b]+topological([x for x in block if x!=b],edges)
        else:ordered=topological(block,edges)
        order+=ordered
    positive=[0]*N
    for rank,x in enumerate(order):positive[x]=rank
    assert positive[b]==positive[a]+1
    assert all((positive[x] >> (n-h))==(x >> (n-h)) for x in range(N))
    assert all(positive[x]<positive[y] for x,y in edges)
    negative=list(positive);negative[a],negative[b]=negative[b],negative[a]
    assert all(negative[x]<negative[y] for x,y in edges)
    changed=[i for i in range(h) if ((a >> (n-i-1))&1)!=((b >> (n-i-1))&1)]
    assert changed
    degree=max(anf_degree([(negative[x] >> (n-i-1))&1 for x in range(N)],n) for i in changed)
    assert degree==n-1
    return dict(n=n,h=h,queries=len(edges),boundary=boundary,swapped_raw_pair=[a,b],
                positive_prefix_same=True,negative_prefix_degree=degree,
                all_transcript_answers_identical=True)


def main():
    rng=random.Random(9977321)
    records=[]
    for n in (3,4):
        N=1 << n
        universe=[(x,y) for x in range(N) for y in range(x+1,N)]
        for h in range(1,n+1):
            for q in range(N-1):
                for _ in range(12):
                    edges=rng.sample(universe,q)
                    records.append(completion(n,h,edges))
    out=dict(status='PASS',scope='finite transcript completion construction; general proof is separate',
        positive_degree=1,required_assumption='n-1>d>=1',traces=len(records),records=records)
    (HERE/'certificate_lower_fixture.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',traces=len(records))))
if __name__=='__main__':main()
