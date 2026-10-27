#!/usr/bin/env python3
"""Independent finite exhaustive and randomized oracle checks."""
from chain_ring_kloosterman import *
import itertools,json,random,time
from pathlib import Path


def brute_k(R,A,D):
    answer=0
    for i in range(R.q**R.e):
        x=R.packed(i)
        if x[0]: answer+=R.psi(R.add(R.mul(A,x),R.mul(D,R.inv(x))))
    return answer

def brute_fiber(R,a,b,c):
    xs=[R.packed(i) for i in range(R.q**R.e)]
    answer=0
    for x in xs:
        for y in xs:
            if R.mul(x,y)==c: answer+=R.psi(R.add(R.mul(a,x),R.mul(b,y)))
    return answer

def brute_cubic(R,coeff):
    xs=[R.packed(i) for i in range(R.q**R.e)]
    lam,A,B,C,D,E,F,G=coeff
    answer=0
    for x in xs:
        for y in xs:
            for z in xs:
                p=R.add(R.mul(lam,R.mul(x,R.mul(y,z))),R.mul(A,R.mul(x,y)),
                        R.mul(B,R.mul(x,z)),R.mul(C,R.mul(y,z)),R.mul(D,x),
                        R.mul(E,y),R.mul(F,z),G)
                answer+=R.psi(p)
    return answer

def main():
    rng=random.Random(202610271704); results={}; start=time.perf_counter()
    totals=0; data=[]
    for h,e in [(3,e) for e in range(2,10)]+[(7,e) for e in range(2,5)]+[(11,e) for e in range(2,4)]:
        R=ChainRing(h,e); count=0; hist={}
        for num in range(R.q**R.e):
            u=R.packed(num)
            if not u[0]: continue
            fast=unit_kloosterman(R,u); slow=brute_k(R,R.one,u)
            assert fast==slow,(h,e,u,fast,slow)
            hist[str(fast)]=hist.get(str(fast),0)+1; count+=1
        data.append(dict(h=h,e=e,unit_parameters=count,values=hist))
        totals+=count
        print('units',h,e,count,flush=True)
    results['unit_exhaustive']=dict(cases=totals,rows=data)
    general=0
    for h,e in [(3,e) for e in range(1,8)]+[(7,e) for e in range(1,5)]+[(11,e) for e in range(1,4)]:
        R=ChainRing(h,e)
        for j in range(25):
            A=R.packed(rng.randrange(R.q**R.e)); D=R.packed(rng.randrange(R.q**R.e))
            if j%5==0: A=R.zero
            if j%7==0: D=R.zero
            assert kloosterman(R,A,D)==brute_k(R,A,D),(h,e,A,D)
            general+=1
    results['arbitrary_parameters']=general
    fibers=0
    for h,e in [(3,e) for e in range(1,6)]+[(7,e) for e in range(1,4)]:
        R=ChainRing(h,e)
        for j in range(30):
            coeff=[R.packed(rng.randrange(R.q**R.e)) for _ in range(3)]
            if j%5==0: coeff[j%3]=R.zero
            if j==29: coeff=[R.zero]*3
            got=product_fiber_sum(R,*coeff); expected=brute_fiber(R,*coeff)
            assert got==expected,(h,e,coeff,got,expected)
            fibers+=1
    results['product_fibers']=fibers
    cubics=0
    for h,e in [(3,1),(3,2),(3,3),(7,1),(7,2)]:
        R=ChainRing(h,e)
        for j in range(10):
            coeff=[R.packed(rng.randrange(R.q**R.e)) for _ in range(8)]
            coeff[0]=(rng.randrange(1,R.q),)+coeff[0][1:]
            got=cubic_sum(R,*coeff); expected=brute_cubic(R,coeff)
            assert got==expected,(h,e,coeff,got,expected)
            cubics+=1
    results['fully_enumerated_cubics']=cubics
    R=ChainRing(3,4); u=(1,0,1,0)
    terms=[]
    for num in range(16):
        x=R.packed(num)
        if x[0]: terms.append(dict(x=x,inverse=R.inv(x),phase=R.add(x,R.mul(u,R.inv(x))),sign=R.psi(R.add(x,R.mul(u,R.inv(x))))))
    results['source_bound_counterexample']=dict(h=3,e=4,u=u,terms=terms,sum=sum(x['sign'] for x in terms),claimed_bound_squared=32,actual_sum_squared=64)
    large=[]
    for h,e in [(0x10000008d,16),(0x10000008d,31),(0x10000008d,64),(0x10000008d,128)]:
        R=ChainRing(h,e); c=(e+2)//3; u=[1]+[0]*(e-1)
        for i in range(1,e-c):
            j=2*i-e+1
            if j>=0: u[i]=R.sqrt_field(u[j])
        for i in range(e-c,e): u[i]=rng.randrange(R.q)
        t=time.perf_counter(); got,evidence=unit_kloosterman(R,u,details=True)
        large.append(dict(h=h,e=e,input_bits=3*R.d*e,u=u,K=got,Z=R.q**e*got,seconds=time.perf_counter()-t,evidence=evidence))
    results['large_structured_backend_runs']=large
    results['seconds']=time.perf_counter()-start
    path=Path(__file__).with_name('chain_ring_results.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k not in ('unit_exhaustive','large_structured_backend_runs','source_bound_counterexample')},indent=2))
    print('saved',path)

if __name__=='__main__': main()
