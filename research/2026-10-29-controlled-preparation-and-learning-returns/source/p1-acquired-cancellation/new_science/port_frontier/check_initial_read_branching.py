#!/usr/bin/env python3
"""Exact new counterexample to treating an initial state read as free.

Checks only finite algebra for the review's observation-interface correction.
No previous fixture is rerun, no source data or physical operation is acquired.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def sub(a,b):
    return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def main():
    T1=[[F(1,4),0,F(3,8),F(3,8)],
        [0,F(3,4),F(1,8),F(1,8)],
        [F(3,8),F(1,8),F(1,2),0],
        [F(3,8),F(1,8),0,F(1,2)]]
    T2=[[F(1,2),0,F(3,8),F(1,8)],
        [0,F(1,2),F(3,8),F(1,8)],
        [F(3,8),F(3,8),F(1,4),0],
        [F(1,8),F(1,8),0,F(3,4)]]
    I=[[F(i==j) for j in range(4)] for i in range(4)]
    P=[[F(1,2) if i//2==j//2 else F(0) for j in range(4)] for i in range(4)]
    eps2=[]
    for T in [T1,T2]:
        assert all(sum(row)==1 and min(row)>=0 for row in T)
        assert all(T[i][j]==T[j][i] for i in range(4) for j in range(4))
        R=mm(mm(sub(I,P),T),P)
        RtR=mm(list(map(list,zip(*R))),R)
        e2=sum(RtR[i][i] for i in range(4))
        # RtR has one nonzero eigenvalue, established algebraically.
        assert mm(RtR,RtR)==[[e2*x for x in row] for row in RtR]
        assert e2==F(1,8)
        eps2.append(e2)
    f=[sum(T1[i][2:]) if i<2 else sum(T2[i][:2]) for i in range(4)]
    assert f==[F(3,4),F(1,4),F(3,4),F(1,4)]
    Pf=[row[0] for row in mm(P,[[x] for x in f])]
    omitted2=sum((x-y)**2 for x,y in zip(f,Pf))/4
    old2=eps2[0]/4
    corrected2=2*old2
    assert omitted2==F(1,16)>old2==F(1,32)
    assert omitted2==corrected2
    review=Path(__file__).with_name('FINITE_ERROR_PREPARATION_RECEIVING_REVIEW.md')
    receipt={
        'status':'PASS',
        'scope':'New exact observation-interface counterexample; no physical data.',
        'review_sha256':hashlib.sha256(review.read_bytes()).hexdigest(),
        'per_operation_leakage_squared':list(map(str,eps2)),
        'event_effect':list(map(str,f)),
        'true_omitted_effect_norm_squared':str(omitted2),
        'bound_without_initial_read_squared':str(old2),
        'corrected_initial_read_bound_squared':str(corrected2),
    }
    target=Path(__file__).with_name('INITIAL_READ_BRANCHING_EXACT_CHECKS.json')
    target.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    main()
