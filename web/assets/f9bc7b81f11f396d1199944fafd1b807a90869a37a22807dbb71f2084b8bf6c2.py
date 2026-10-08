#!/usr/bin/env python3
"""Finite, exact arithmetic checks for sharp determinant-power coefficient theorem.
Python 3.11+ stdlib only. Not a general proof and not historical novelty review.
Run: python verify_global.py
"""
from fractions import Fraction as F
from itertools import combinations, product
from functools import lru_cache
from math import factorial
import random

def det(A):
    n=len(A)
    M=[list(map(F,row)) for row in A]
    z=F(1)
    for i in range(n):
        j=next((t for t in range(i,n) if M[t][i]!=0),None)
        if j is None:return F(0)
        if i!=j:M[i],M[j]=M[j],M[i];z=-z
        p=M[i][i];z*=p
        for j in range(i+1,n):
            fac=M[j][i]/p
            for k in range(i+1,n):M[j][k]-=fac*M[i][k]
            M[j][i]=F(0)
    return z

def packing_coefficient(columns):
    d=len(columns[0]);n=len(columns);assert n%d==0
    r=n//d
    minors={}
    for I in combinations(range(n),d):
        block=[[columns[j][i] for j in I] for i in range(d)]
        a=det(block)
        minors[sum(1<<j for j in I)]=a*a
    @lru_cache(None)
    def calc(mask):
        if mask==0:return F(1)
        first=(mask&-mask).bit_length()-1
        remaining=[j for j in range(n) if mask&(1<<j) and j!=first]
        tot=F(0)
        for other in combinations(remaining,d-1):
            b=(1<<first)+sum(1<<j for j in other)
            tot+=minors[b]*calc(mask^b)
        return tot
    return factorial(r)*calc((1<<n)-1)

def p_formula(d,r):
    result=F(1)
    for j in range(d):
        result*=F(factorial(j)*factorial(r),factorial(r+j))
    return result

def f_rect(d,r):
    n=d*r
    num=factorial(n)
    den=1
    for j in range(d):
        num*=factorial(j)
        den*=factorial(r+j)
    assert num%den==0
    return num//den

def main():
    checked=0
    random.seed(20261008)
    for d,r in [(1,3),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,1),(4,2)]:
        n=d*r
        balanced=[tuple(int(i==j) for i in range(d)) for j in range(d) for _ in range(r)]
        c=packing_coefficient(balanced)
        target=F(factorial(r)**d)
        assert c==target,(d,r,c,target)
        overlap=F(f_rect(d,r),factorial(n))*c
        assert overlap==p_formula(d,r)
        print(f"  equality d={d} r={r} : coefficient={c}; separable singlet overlap={overlap}")
        checked+=1
        for _ in range(20 if n<=8 else 5):
            columns=[tuple(random.randint(-3,3) for i in range(d)) for j in range(n)]
            if any(sum(v*v for v in col)==0 for col in columns):continue
            c=packing_coefficient(columns)
            bound=factorial(r)**d
            for col in columns:
                bound*=sum(v*v for v in col)
            assert 0<=c<=bound,(d,r,c,bound)
            checked+=1
    print(f"PASS {checked} rational tests; no claims of external validation.")

if __name__=="__main__":
    main()
