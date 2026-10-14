#!/usr/bin/env python3
"""Exact rational replay of the shared-tree acquisition query decoder."""
from __future__ import annotations
from fractions import Fraction
import json, math, random
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "replay" / "query_tree_exact_replay.json"

def tree(lo, hi):
    if hi-lo == 1:
        return (1 << lo, None, None)
    mid=(lo+hi)//2
    L,R=tree(lo,mid),tree(mid,hi)
    return (L[0]|R[0],L,R)

def boundaries(mask,n,edges):
    return sum(((mask>>u)&1) != ((mask>>v)&1) for u,v in edges)

def exact_weight(mask,n,edges,t,r):
    return r**mask.bit_count() * t**(n-boundaries(mask,n,edges))

def rational_sqrt(x):
    a=math.isqrt(x.numerator); b=math.isqrt(x.denominator)
    if a*a != x.numerator or b*b != x.denominator:
        raise ValueError("not a perfect rational square")
    return Fraction(a,b)

def learn(order,t=Fraction(3,2),r=Fraction(5,3)):
    n=len(order); V=(1<<n)-1
    edges={tuple(sorted((order[j],order[(j+1)%n]))) for j in range(n)}
    calls=[]; cache={}
    def W(mask):
        if mask not in cache:
            cache[mask]=exact_weight(mask,n,edges,t,r)
            calls.append(mask)
        return cache[mask]
    # Bootstrap cache: empty, all singleton weights, full, and V\{0}.
    for mask in [0,V,*[1<<j for j in range(n)],V^1]: W(mask)
    root_ratio=W(V)*W(0)/(W(V^1)*W(1))
    q=rational_sqrt(root_ratio)
    recovered=set(); contrasts=0; visited=0
    def recurse(i,node,L,R,k):
        nonlocal contrasts,visited
        visited+=1
        if L is None:
            assert node.bit_count()==1 and k==1
            j=node.bit_length()-1
            recovered.add(tuple(sorted((i,j))))
            return
        if node & (1<<i):
            A,B=(R,L) if L[0] & (1<<i) else (L,R)
        else:
            A,B=L,R
        a=A[0]
        ratio=W(a|(1<<i))*W(0)/(W(a)*W(1<<i))
        candidates=[0,1,2]
        ms=[m for m in candidates if q**m==ratio]
        assert len(ms)==1, (i,a,ratio,q)
        ka=ms[0]; kb=k-ka
        assert 0<=kb<=2
        contrasts+=1
        if ka: recurse(i,a,A[1],A[2],ka)
        if kb: recurse(i,B[0],B[1],B[2],kb)
    T=tree(0,n)
    for i in range(n): recurse(i,V,T[1],T[2],2)
    assert recovered==edges, (recovered^edges)
    return {"n":n,"t":str(t),"r":str(r),"weight_queries_unique":len(cache),
            "seed_unique":len({0,V,V^1,*[1<<j for j in range(n)]}),
            "pairwise_baseline":1+n+n*(n-1)//2,"contrast_calls":contrasts,
            "positive_nodes":visited,"cycle_edges_recovered":len(recovered),
            "exact_weight_cache_masks":sorted(cache)}

def run():
    # Verify one canonical ring and a deterministic sample of random relabelings.
    rng=random.Random(0xF4E5CA9E)
    cases=[list(range(24))]
    for _ in range(100):
        p=list(range(24)); rng.shuffle(p); cases.append(p)
    rows=[learn(p) for p in cases]
    counts=[x["weight_queries_unique"] for x in rows]
    source_like_rng=random.Random(0x1000)
    source_like_orders=[]
    for _ in range(25):
        p=list(range(24));source_like_rng.shuffle(p);source_like_orders.append(p)
    source_like=[learn(p,Fraction(1000),Fraction(1)) for p in source_like_orders]
    source_like_counts=[x["weight_queries_unique"] for x in source_like]
    lq=math.log(3/2); delta=lq/10
    # Adversarial deterministic error bound for m=0,1,2.
    maxdevs=[]
    a=2*lq
    for k in (0,1,2):
        maxdevs.append((4*delta+2*k*delta)/(a-2*delta))
    result={"claim":"Exact rational weight-oracle replay; all cache entries are unique subset masks; cycle recovered exactly.",
      "n":24,"sample_count":len(rows),"seed":0xF4E5CA9E,
      "counts":{"min":min(counts),"median":sorted(counts)[len(counts)//2],"max":max(counts),"natural_order":rows[0]["weight_queries_unique"],"pairwise_baseline":301},
      "source_parameter_fixture":{"t":"1000","r":"1","samples":len(source_like),"all_recovered_exactly":all(x["cycle_edges_recovered"]==24 for x in source_like),"unique_masks":{"min":min(source_like_counts),"median":sorted(source_like_counts)[len(source_like_counts)//2],"max":max(source_like_counts)}},
      "all_recovered_exactly":all(x["cycle_edges_recovered"]==24 for x in rows),
      "canonical_case":rows[0],
      "finite_error_check":{"assumption":"Each queried dimensionless energy has deterministic absolute error at most delta; t >= t_min > 1.","delta_over_log_t":0.1,"log_q_error_bound":2*delta,"candidate_error_bounds_k0_k1_k2":maxdevs,"strictly_below_half":all(d<0.5 for d in maxdevs),"generic_sufficient_threshold":"delta < log(t_min)/9; the proposed delta < log(t_min)/10 is stricter."},
      "limitations":["This validates the algebra and decoder under the promised homogeneous degree-2 cycle family only.","A finite set of queried configurations does not establish that a physical energy oracle has no higher-order terms.","Oracle mask-call counts omit preparation/calibration, physical readout, arithmetic bit costs, and all-source uncertainty unless explicitly included elsewhere."]}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__":run()
