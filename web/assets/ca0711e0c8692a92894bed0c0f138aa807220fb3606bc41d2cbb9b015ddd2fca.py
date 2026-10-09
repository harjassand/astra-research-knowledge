#!/usr/bin/env python3
"""Small exact rational checks of the antisymmetric local ladder.

This checks tensor reductions and conditional states; it is not a general
proof, optimized broadcaster computation, or EB optimization certificate.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import comb, log
import json

def shuffle_sign(first, second):
    return (-1)**sum(a>b for a in first for b in second)

def a_state(d,n):
    # a_(n+1) represented on V tensor wedge^n V, orthonormal wedge bases.
    out={}
    c=F(1,(n+1)*comb(d,n+1))
    for w in combinations(range(d),n+1):
        terms=[((i,tuple(x for x in w if x!=i)),(-1)**k) for k,i in enumerate(w)]
        for x,s in terms:
            for y,t in terms:out[x,y]=c*s*t
    return out

def reduce_b(mat,n,k):
    out=defaultdict(F)
    denom=comb(n,k)
    for ((i,s),(j,t)),value in mat.items():
        ts=set(t)
        for discarded in combinations(s,n-k):
            if not set(discarded)<=ts:continue
            ds=set(discarded)
            r=tuple(a for a in s if a not in ds)
            q=tuple(a for a in t if a not in ds)
            out[(i,r),(j,q)]+=value*shuffle_sign(r,discarded)*shuffle_sign(q,discarded)/denom
    return {key:value for key,value in out.items() if value}

def run():
    rows=[]
    for d in (4,8):
        L=d.bit_length()-1
        for j in range(L):
            n=2**j
            a=a_state(d,n)
            assert sum(v for (x,y),v in a.items() if x==y)==1
            assert reduce_b(a,n,1)==a_state(d,1)
            if n>=2:assert reduce_b(a,n,n//2)==a_state(d,n//2)
            conditional={(s,t):d*v for ((i,s),(ii,t)),v in a.items() if i==ii==0}
            expected={(s,s):F(1,comb(d-1,n)) for s in combinations(range(1,d),n)}
            assert conditional==expected
            td=sum(abs(conditional.get((s,s),F())-F(1,comb(d,n))) for s in combinations(range(d),n))/2
            assert td==F(n,d)
            rows.append({'d':d,'n':n,'nonzero_entries':len(a),'conditional_halftrace':str(td),'status':'exact_pass'})
        I=sum(log(d*(2**j+1)/(d-2**j)) for j in range(L))/L
        cap=sum(-log(1-2**j/d) for j in range(L))/L
        assert (L-1)*log(2)/2 <= I <= (L-1)*log(2)/2+4/L
        assert cap<=2/L
    print(json.dumps({'scope':'finite rational tensor identities plus scalar floating-point sanity checks','rows':rows,'status':'PASS'},indent=2))

if __name__=='__main__':run()
