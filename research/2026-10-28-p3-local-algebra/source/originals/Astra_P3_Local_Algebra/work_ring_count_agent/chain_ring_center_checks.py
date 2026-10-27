#!/usr/bin/env python3
"""Manufacture nonzero stationary examples for an acquisition audit.
The main counter receives u only; the planted center is used solely afterward.
"""
from chain_ring_kloosterman import *
from chain_ring_checks import brute_k
import json,random,time
from pathlib import Path

def manufacture_parameter(R,a,rng):
    c=(R.e+2)//3
    ai=R.inv(a); ai2=R.mul(ai,ai); ai3=R.mul(ai2,ai)
    a02=gf_mul(a[0],a[0],R.h)
    u=[0]*R.e
    for i in range(R.e-c):
        U=R.add(R.one,R.mul(u,ai2)); V=R.mul(u,ai3); j=2*i-R.e+1
        target=U[i]^(R.sqrt_field(V[j]) if j>=0 else 0)
        u[i]=gf_mul(a02,target,R.h)
    for i in range(R.e-c,R.e): u[i]=rng.randrange(R.q)
    return tuple(u)

def main():
    rng=random.Random(202610272005); rows=[]
    for h,e,repeats in [(3,8,20),(7,5,20),(11,4,20),(11,6,10),
                         (0x10000008d,16,1),(0x10000008d,31,1),
                         (0x10000008d,64,1),(0x10000008d,128,1)]:
        R=ChainRing(h,e); z=(e+1)//3
        for j in range(repeats):
            a=[rng.randrange(1,R.q)]+[rng.randrange(R.q) for _ in range(e-1)]
            u=manufacture_parameter(R,a,rng)
            start=time.perf_counter(); ans,data=unit_kloosterman(R,u,details=True)
            elapsed=time.perf_counter()-start
            assert data['center']==a[:z] and not data['failed_equations']
            oracle=None
            if R.d*e<=18:
                oracle=brute_k(R,R.one,u); assert ans==oracle
            rows.append(dict(h=h,e=e,planted_center=a[:z],u=u,K=ans,
                             brute_oracle=oracle,seconds=elapsed,evidence=data))
    path=Path(__file__).with_name('chain_ring_center_results.json')
    path.write_text(json.dumps(dict(cases=len(rows),rows=rows),indent=2)+'\n')
    print('passed',len(rows),'center acquisitions and',sum(x['brute_oracle'] is not None for x in rows),'full unit sums')
    print('large',[(x['e'],x['seconds'],x['K']==0) for x in rows[-4:]])
if __name__=='__main__': main()
