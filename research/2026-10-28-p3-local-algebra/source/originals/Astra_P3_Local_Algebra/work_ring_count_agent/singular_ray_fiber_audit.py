#!/usr/bin/env python3
"""Independent 30-bit oracle: enumerate low prefixes, contract each quadratic fiber.
The main singular-ray algorithm does not receive the fibers and does not
perform this enumeration. This is an exact verification, not a benchmark.
"""
from singular_ray_quadratic import *
from smooth_ring_checks import raw_from
from pathlib import Path
import json,random,time

def quad_poly_sum(poly,n):
    poly=set(poly); remaining=set(range(n)); factor=1
    while True:
        pair=next((m for m in poly if m.bit_count()==2),None)
        if pair is None:
            if any(poly): return 0
            return factor*(-1 if 0 in poly else 1)*(1<<len(remaining))
        i,j=[k for k in remaining if pair>>k&1]
        A={m^(1<<i) for m in poly if m>>i&1 and not m>>j&1}
        B={m^(1<<j) for m in poly if m>>j&1 and not m>>i&1}
        poly={m for m in poly if not m&pair}
        for a in A:
            for b in B: poly.symmetric_difference_update({a|b})
        remaining.remove(i); remaining.remove(j); factor*=2

def compress(mask,indices): return sum(((mask>>old)&1)<<new for new,old in enumerate(indices))

def fiber_oracle(poly,n,low):
    prefix=[i for i in range(n) if low>>i&1]; tail=[i for i in range(n) if not low>>i&1]
    terms=[(compress(m,prefix),compress(m,tail)) for m in poly]
    total=0; hist={}
    for x in range(1<<len(prefix)):
        p=set()
        for need,high in terms:
            if (x&need)==need: p.symmetric_difference_update({high})
        assert all(m.bit_count()<=2 for m in p)
        z=quad_poly_sum(p,len(tail)); total+=z; hist[str(z)]=hist.get(str(z),0)+1
    return total,dict(prefix_bits=len(prefix),fibers=1<<len(prefix),quadratic_bits=len(tail),fiber_histogram=hist)

def main():
    rng=random.Random(202610280150); R=ChainRing(7,5); n=30; depth=2
    low=quotient_bitmask(R,depth); ids=[i for i in range(n) if low>>i&1]; H={(1,1,1):R.one}; rows=[]
    for rep in range(3):
        forms=[]
        while len(forms)<len(ids):
            a=rng.randrange(1<<len(ids))
            if len(span(forms+[a]))>len(forms): forms.append(a)
        Q=set()
        for a,b in zip(forms[::2],forms[1::2]):
            for i in range(len(ids)):
                if a>>i&1:
                    for j in range(len(ids)):
                        if b>>j&1: Q.symmetric_difference_update({(1<<ids[i])|(1<<ids[j])})
        for i in ids:
            if rng.randrange(2): Q.symmetric_difference_update({1<<i})
        B=[sum(1<<j for j in range(n) if i!=j and ((1<<i)|(1<<j)) in Q) for i in range(n)]
        assert len(span(B))==12
        raw=raw_from(R,H,Q); fast,evidence=homogeneous_quotient_sum(R,H,Q,details=True)
        oracle,checks=fiber_oracle(raw,n,low)
        assert fast==oracle
        rows.append(dict(n=n,h=R.h,e=R.e,noise_rank=12,Q=sorted(Q),raw_anf=sorted(raw),
                         signed_count=fast,zero_count=((1<<n)+fast)//2,evidence=evidence,independent_oracle=checks))
        print('passed',rep,fast,flush=True)
    Path(__file__).with_name('singular_ray_fiber_results.json').write_text(json.dumps(dict(cases=3,rows=rows),indent=2)+'\n')
if __name__=='__main__': main()
