#!/usr/bin/env python3
"""Polynomial rank-weighted Hom count for finite nilpotent modules.

The Hom counter is an exact Birkhoff/Hall calculation. Its identification
with the even-string matrix Kloosterman sum is proved by the fixed-block
Fourier lemma in EVEN_STRING_RESUMMATION.tex.
"""
from functools import lru_cache
from pathlib import Path
import json,time
from nilpotent_pair_counter import choose

def columns(partition):
    p=tuple(sorted(partition,reverse=True))
    if any(x<=0 for x in p):raise ValueError('positive partition parts required')
    return tuple(sum(x>=j for x in p) for j in range(1,max(p,default=0)+1))

@lru_cache(None)
def gl_order(n,q):
    return q**(n*(n-1)//2)*__import__('math').prod(q**j-1 for j in range(1,n+1))

def rank_weighted_hom(left,right,q,stats=None,image_blocks=None,radical_source=()):
    """Sum q^rank(f) over f:J_left -> J_right intertwining nilpotents.

    Sum over image-module types is aggregated by their successive column
    heights. No partitions, module elements, or subspaces are enumerated.
    Time O(L min(|left|,|right|)^2) integer arithmetic operations.
    """
    if q<2:raise ValueError('q must be a prime power at least two')
    a=columns(left);b=columns(right);e=columns(radical_source);L=max(len(a),len(b),len(e))
    a=a+(0,)*(L-len(a));b=b+(0,)*(L-len(b))
    e=e+(0,)*(L-len(e))
    next_height={0:1};transitions=0
    for aj,bj,ej in reversed(tuple(zip(a,b,e))):
        current={}
        for t,tail in next_height.items():
            for c in range(t,min(aj,bj)+1):
                d=c-t
                factor=q**(c+t*(aj+bj+ej-t))*choose(aj-t,d,q)*choose(bj-t,d,q)*gl_order(d,q)
                current[c]=current.get(c,0)+factor*tail
                transitions+=1
        next_height=current
    if stats is not None:stats.update(columns=L,transitions=transitions,enumerated_partitions=0,enumerated_maps=0)
    return (sum(next_height.values()) if image_blocks is None
            else next_height.get(image_blocks,0))

def even_string_kloosterman(parts,q,stats=None):
    """Proved closed evaluation for a pair consisting only of even strings."""
    if any(l%2 for l,c in parts):raise ValueError('all string lengths must be even')
    left=[l//2 for l,c in parts if c==0];right=[l//2 for l,c in parts if c==1]
    n=sum(left)+sum(right)
    return (-1)**n*q**(n*(n-1)//2)*rank_weighted_hom(left,right,q,stats)

def one_sided_even_kloosterman(parts,q,stats=None):
    """Closed maximal-defect Hom evaluation when even strings have one color.

    Odd strings of both colors are allowed with arbitrary multiplicity/length.
    """
    parts=tuple(parts);even_colors={c for l,c in parts if l%2==0}
    if len(even_colors)>1:raise ValueError('even strings must have one terminal color')
    source_color=next(iter(even_colors),0)
    left=[(l+1)//2 for l,c in parts if l%2 and c==source_color]
    right=[(l+1)//2 for l,c in parts if l%2 and c!=source_color]
    extra=[l//2 for l,c in parts if l%2==0]
    o=len(left)
    if len(right)!=o:raise ValueError('unbalanced odd strings')
    n=sum(l for l,c in parts)//2
    value=rank_weighted_hom(left,right,q,stats,image_blocks=o,radical_source=extra)
    divisor=q**(o*(o+1)//2)
    assert value%divisor==0
    return (-1)**(n+o)*q**(n*(n-1)//2)*(value//divisor)

def partitions(n,limit=None):
    if n==0:yield ();return
    for k in range(min(n,limit if limit is not None else n),0,-1):
        for tail in partitions(n-k,k):yield (k,)+tail

def check():
    from endpoint_pair_counter import EndpointPairCounter
    from nilpotent_pair_counter import NilpotentPairCounter
    start=time.perf_counter();rows=[]
    for q in (2,4,8,256):
        endpoint=EndpointPairCounter(q);rank_counter=NilpotentPairCounter(q);total=0
        for n in range(11):
            for l in range(n+1):
                for left in partitions(l):
                    for right in partitions(n-l):
                        parts=tuple((2*x,0) for x in left)+tuple((2*x,1) for x in right)
                        got=even_string_kloosterman(parts,q)
                        expected=endpoint.count(parts)
                        assert got==expected,(q,parts,got,expected)
                        assert got==rank_counter.count(parts)
                        total+=1
        rows.append(dict(q=q,types=total,endpoint=endpoint.metadata(),rank_compression=rank_counter.metadata()))
        print('passed',q,total,flush=True)
    examples=[]
    for n,q in [(100,2),(500,256),(1000,65536)]:
        left=(n//4,)*2;right=(n//10,)*5;stats={}
        value=rank_weighted_hom(left,right,q,stats)
        examples.append(dict(left=left,right=right,q=q,value_bit_length=value.bit_length(),statistics=stats))
    result=dict(status='proved even-string Fourier identity and Birkhoff/Hall Hom DP',checks=rows,examples=examples,seconds=time.perf_counter()-start)
    Path(__file__).with_name('rank_hom_resummation_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':check()
