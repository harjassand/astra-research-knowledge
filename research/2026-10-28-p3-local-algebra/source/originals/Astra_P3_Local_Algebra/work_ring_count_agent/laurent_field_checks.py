#!/usr/bin/env python3
from laurent_field_counter import *
from itertools import product
from pathlib import Path
import random,json,time

def brute_laurent(poly,h):
    q=1<<(h.bit_length()-1)
    return sum(1-2*gf_trace(sumxor(gf_mul(c,gf_pow(x,e%(q-1),h),h) for e,c in poly.items()),h) for x in range(1,q))

def sumxor(values):
    out=0
    for x in values: out^=x
    return out

def brute_hesse(h,a,rho,sigma,tau,constant):
    q=1<<(h.bit_length()-1); total=0
    for x,y,z in product(range(q),repeat=3):
        v=gf_mul(gf_mul(x,x,h),y,h)^gf_mul(x,gf_mul(y,y,h),h)^gf_mul(gf_mul(z,z,h),z,h)
        v^=gf_mul(a,gf_mul(gf_mul(x,y,h),z,h),h)^gf_mul(rho,x,h)^gf_mul(sigma,y,h)^gf_mul(tau,z,h)^constant
        total+=1-2*gf_trace(v,h)
    return total

def main():
    rng=random.Random(202610272344); rows=[]; hs=[]; start=time.perf_counter()
    for h in (3,7,11,19):
        q=1<<(h.bit_length()-1)
        for _ in range(5):
            p={e:rng.randrange(q) for e in (-5,-3,-1,0,1,3)}
            ans,data=laurent_dwork(p,h,details=True); expected=brute_laurent(p,h)
            assert ans==expected,(h,p,ans,expected)
            rows.append(dict(h=h,polynomial=p,answer=ans,metadata=data))
        for rep in range(6):
            params=[rng.randrange(1,q) if rep<5 else 0]+[rng.randrange(q) for _ in range(4)]
            if rep==0: params[1]=0
            ans,data=shifted_hesse_sum(h,*params,details=True)
            expected=brute_hesse(h,*params)
            assert ans==expected,(h,params,ans,expected)
            hs.append(dict(h=h,parameters=params,signed_count=ans,metadata=data))
        print('passed field degree',h.bit_length()-1,flush=True)
    homogeneous=[]
    for h,a in [(7,0),(19,2),(19,3)]:
        ans,data=shifted_hesse_sum(h,a,details=True)
        assert ans==brute_hesse(h,a,0,0,0,0)
        homogeneous.append(dict(h=h,a=a,signed_count=ans,metadata=data))
    result=dict(laurent_cases=rows,shifted_hesse_cases=hs,homogeneous_even_regressions=homogeneous,seconds=time.perf_counter()-start)
    Path(__file__).with_name('laurent_field_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('passed',len(rows),len(hs),'seconds',result['seconds'])
if __name__=='__main__': main()
