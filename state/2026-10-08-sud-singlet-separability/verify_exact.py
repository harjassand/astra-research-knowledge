#!/usr/bin/env python3
"""Exact, stdlib-only finite algebra checks for RESEARCH_STATE.md.
Runs finite tests; DOES NOT certify the limiting theorem or priority.
"""
from functools import lru_cache
from fractions import Fraction
from math import factorial
@lru_cache(None)
def partitions(n,d,lim=None):
    if d==0: return [()] if n==0 else []
    if lim is None: lim=n
    return [(i,)+v for i in range(min(n,lim),-1,-1)
            for v in partitions(n-i,d-1,i)]
def f(lam):
    d=len(lam); n=sum(lam); num=factorial(n)
    for i in range(d):
        for j in range(i+1,d):
            num*=lam[i]-lam[j]+j-i
    den=1
    for i in range(d):den*=factorial(lam[i]+d-1-i)
    assert num%den==0
    return num//den
def casimir(lam):
    d=len(lam); k=sum(lam)
    return sum(Fraction((d*x-k)**2,d*d)+(d-1-2*i)*x
               for i,x in enumerate(lam))
count=0
for d in (2,3,4,5):
    for N in range(d,10*d+1,d):
        r=N//d
        den=f((r,)*d)
        for k in range(N+1):
            total=Fraction(0); moment=Fraction(0)
            for lam in partitions(k,d):
                if lam[0]>r:continue
                mu=tuple(r-lam[d-1-i] for i in range(d))
                w=Fraction(f(lam)*f(mu),den)
                total+=w
                moment+=w*casimir(lam)
            assert total==1,(d,N,k,total)
            assert moment==Fraction((d*d-1)*k*(N-k),d*(N-1))
            count+=1
print("PASS:",count,"exact SU(d) branching and Casimir identities")
print("These exact finite checks are not a proof of the asymptotic theorem.")
