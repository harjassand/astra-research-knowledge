#!/usr/bin/env python3
"""Exact arithmetic admission checks for the collective posterior obstruction.
No receiver optimality or asymptotic theorem is inferred from these fixtures.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import json
from pathlib import Path

checks=[]
for D in (2,3,4):
    q=D*D
    for L in range(2,6):
        c=F(q-1,q**L-1)
        mins=[]
        for j in range(1,L+1):
            posterior=[F(q**k,sum(q**h for h in range(1,j+1))) for k in range(1,j+1)]
            assert sum(posterior)==1
            assert posterior[0]>=c
            mins.append(posterior[0])
        assert min(mins)==c
        # Product binary effect P has zero probability at n=1, >=alpha at n>=2.
        alpha=F(D-1,D)
        ps=[1-F(1,D**(n-1)) for n in range(1,L+1)]
        assert ps[0]==0 and all(p>=alpha for p in ps[1:])
        # Exhaustive small profile mixtures: selected flag set never includes K=1.
        for K in product(range(1,L+1),repeat=2):
            for N in product(*(range(1,k+1) for k in K)):
                for selected in product((False,True),repeat=2):
                    prob=F(1)
                    for n,s in zip(N,selected):
                        pn=ps[n-1]
                        prob*=pn if s else 1-pn
                    if any(s and k==1 for s,k in zip(selected,K)):
                        assert prob==0
        checks.append({'D':D,'L':L,'c_L':str(c),'alpha':str(alpha),'posterior_min':str(min(mins))})

# Exact no-access event probability under a worst posterior, with |S|=s.
for D,L,r in ((2,2,3),(2,3,4),(3,2,3)):
    q=D*D
    probs=[F(q**k,sum(q**h for h in range(1,L+1))) for k in range(1,L+1)]
    c=probs[0]
    for s in range(1,r+1):
        actual=sum((__import__('functools').reduce(lambda x,y:x*y,(probs[k-1] for k in ks),F(1))
                    for ks in product(range(2,L+1),repeat=s)),F(0))
        assert actual==(1-c)**s

out={'status':'PASS','scope':'exact finite posterior/flag checks, not theorem or optimality validation','checks':checks}
path=Path(__file__).with_name('analytic_checks.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','fixtures':len(checks),'output':str(path.resolve())}))
