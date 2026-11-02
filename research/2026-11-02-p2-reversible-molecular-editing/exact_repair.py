#!/usr/bin/env python3
"""Exact rational 4-site same-scaffold error-correction verifier.

States are sets of wrong chemical labels, not latent-state observations.
Warrants on microscopic primitive rates are *assumptions*, not experimental results.
"""
from fractions import Fraction as F
from itertools import product

N=4
S=F(3,4)
Q=F(1,20)
DRIFT=S-(N-1)*Q

def row(mask):
    """Return exact next-state distribution, targeting smallest wrong address."""
    assert mask
    wrong=[i for i in range(N) if mask>>i&1]
    chosen=wrong[0]
    correct=[j for j in range(N) if j not in wrong]
    probs={}
    for repaired in (False, True):
        p_repair=S if repaired else (1-S)
        base=mask & ~(1<<chosen) if repaired else mask
        for flips in product((False,True),repeat=len(correct)):
            nxt=base
            prob=p_repair
            for j,flip in zip(correct,flips):
                prob*=Q if flip else 1-Q
                if flip:nxt|=1<<j
            probs[nxt]=probs.get(nxt,F(0))+prob
    assert sum(probs.values())==1
    return probs

def solve(A,b):
    n=len(A)
    for k in range(n):
        pivot=next(i for i in range(k,n) if A[i][k])
        A[k],A[pivot]=A[pivot],A[k]
        b[k],b[pivot]=b[pivot],b[k]
        z=A[k][k]
        A[k]=[x/z for x in A[k]]
        b[k]/=z
        for i in range(n):
            if i==k or A[i][k]==0:continue
            v=A[i][k]
            A[i]=[x-v*y for x,y in zip(A[i],A[k])]
            b[i]-=v*b[k]
    return b

def check():
    m=2**N-1
    A=[[F(int(i==j)) for j in range(m)] for i in range(m)]
    b=[F(1)]*m
    for mask in range(1,2**N):
        probs=row(mask)
        for nxt,p in probs.items():
            if nxt:A[mask-1][nxt-1]-=p
        d=mask.bit_count()
        ed=sum(p*nxt.bit_count() for nxt,p in probs.items())
        assert ed-d<=-DRIFT
    E=solve(A,b)
    assert all(t<=mask.bit_count()/DRIFT for mask,t in enumerate([F(0)]+E) if mask)
    assert E[-1]<=N/DRIFT
    print('Exact four-site all-wrong expected edits',str(E[-1]),'approximately',float(E[-1]))
    print('Path-class drift',str(DRIFT),'bound',str(F(N)/DRIFT))
    print('States',m,'and every conditional transition independently checked as exact rationals')
if __name__=='__main__':check()
