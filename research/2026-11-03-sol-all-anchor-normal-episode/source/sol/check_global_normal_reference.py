#!/usr/bin/env python3
"""Exact all-state adjoint checks for the translated normal-cycle reference."""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from pathlib import Path
import json
from native_corner_bridge import channels

P=Path(__file__).resolve().parent
factorial=lru_cache(maxsize=None)(factorial)

def gift(a):
    k,j=divmod(a,3)
    return 2*k+int(j>=1),2*k+int(j==2)

def residual(x):
    a,b,c,d,e,f=x;u,v=gift(a);uu,vv=gift(d)
    return b-u,c-v,e-uu,f-vv

def normal(x,label):
    if label[0]=='core':return True
    port,j=label[1:];a=x[3*port]
    return j==a%3 if j<3 else a%3==0

V=((1,1,0),(1,0,1),(1,1,1),(-3,-2,-2))

def displacement(label):
    if label[0]=='core':
        return (0,-2,-2,0,2,2) if label[1]==0 else (0,2,2,0,-2,-2)
    ans=[0]*6;o=3*label[1]
    for j,v in enumerate(V[label[2]]):ans[o+j]=v
    return tuple(ans)

def weight(x,base,alpha,beta,core):
    z=residual(x);diff=z[2]-base[2]
    assert diff%2==0;k=diff//2
    assert z==tuple(base[j]+k*v for j,v in enumerate((-2,-2,2,2)))
    a,b,c,d,e,f=x
    ans=(F(core[0],core[1])**k * F(alpha[0],alpha[3])**(a//3)
          *F(beta[0],beta[3])**(d//3)/(alpha[a%3]*beta[d%3]))
    for v in x:ans/=factorial(v)
    return ans

def probe(x,alpha,beta,core):
    base=residual(x);mu=weight(x,base,alpha,beta,core)
    row=list(channels(x,alpha,beta,core));q=sum(r for _,r,l in row if normal(x,l))
    flux=-mu*q
    labels=[('block',p,j) for p in (0,1) for j in range(4)]+[('core',0),('core',1)]
    for label in labels:
        v=displacement(label);pre=tuple(x[j]-v[j] for j in range(6))
        if min(pre)<0 or not normal(pre,label):continue
        r=next((r for out,r,l in channels(pre,alpha,beta,core) if l==label),F(0))
        if r:
            assert tuple(pre[j]+v[j] for j in range(6))==x
            flux+=weight(pre,base,alpha,beta,core)*r
    assert flux==0,(x,alpha,beta,core,flux)
    h=sum(r for _,r,l in row if not normal(x,l))
    if h==0:
        assert q==alpha[0]+beta[0]
        for out,r,label in row:
            if r and label[0]=='block' and label[2]==0:
                assert sum(rr for _,rr,ll in channels(out,alpha,beta,core) if not normal(out,ll))>0
    return int(h==0),int(q==0)

def main():
    checked=0;zero_h=0;zero_normal=0
    rates=[((1,1,1,1),(1,1,1,1),(2,1)),
           ((1,5,3,7),(2,2,4,11),(3,7)),
           ((1,1000,1,1),(10,1,100,1),(100,1))]
    hidden=[(0,0,0,0),(1,0,0,1),(2,2,0,0),(5,3,4,8),(0,100,2,300),(100,0,2,0)]
    for a in (0,1,2,3,4,5,6,8,10,12):
        for d in (0,1,2,3,4,5,6,8,10,12):
            for b,c,e,f in hidden:
                for alpha,beta,core in rates:
                    zh,zn=probe((a,b,c,d,e,f),alpha,beta,core)
                    zero_h+=zh;zero_normal+=zn;checked+=1
    result={'scope':'Exact pointwise normal adjoint balance and zero-kill successor checks. The infinite reference/physical-clock theorem is separate.',
            'all_state_cases':checked,'zero_unexpected_hazard_cases':zero_h,
            'zero_normal_hazard_cases':zero_normal,'maximum_tested_anchor':12,
            'rate_lists':rates}
    (P/'results/global_normal_reference_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
