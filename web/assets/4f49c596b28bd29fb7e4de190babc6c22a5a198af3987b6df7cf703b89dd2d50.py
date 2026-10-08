#!/usr/bin/env python3
"""Exact rational marginal chi-square for the selected nu=0 state.

Uses the proved Schur generating polynomial. This is a scoped exact finite
calculation, independent of the double-precision density-matrix diagnostics.
It is not a formal/all-size proof of the generating-polynomial theorem.
"""
from math import comb, factorial
from fractions import Fraction
from pathlib import Path
import json


def falling(n,k):
    ans=1
    for q in range(k): ans*=n-q
    return ans


def count_triples(w):
    for a in range(w+1):
        for b in range(w-a+1):
            yield a,b,w-a-b


def coefficients(n,maxweight):
    # F(x,y,z)=sum_M w_M(1-x²-y²-z²)^((N-M)/2)(1-z)^M.
    sector=[]
    for m in range(n%2,n+1,2):
        low=(n-m)//2
        mult=comb(n,low)-(comb(n,low-1) if low else 0)
        sector.append((m,low,(m+1)*mult))
    assert sum(x[2] for x in sector)==2**n
    result={}
    for w in range(1,maxweight+1):
        for a,b,c in count_triples(w):
            if a%2 or b%2:
                result[a,b,c]=Fraction(0)
                continue
            aa,bb=a//2,b//2
            numerator=0
            for m,l,wnum in sector:
                inner=0
                for cc in range(c//2+1):
                    h=c-2*cc
                    k=aa+bb+cc
                    if k>l or h>m: continue
                    multinom=comb(l,aa)*comb(l-aa,bb)*comb(l-aa-bb,cc)
                    sign=-1 if (k+h)%2 else 1
                    inner+=sign*multinom*comb(m,h)
                numerator+=wnum*inner
            # Convert generating polynomial coefficient into Pauli correlator.
            result[a,b,c]=Fraction(numerator*factorial(a)*factorial(b)*factorial(c),
                                    2**n*falling(n,w))
    return result


def exact_chi(n,r):
    cs=coefficients(n,r)
    chi=Fraction(0)
    weights=[]
    for w in range(1,r+1):
        term=Fraction(0)
        for a,b,c in count_triples(w):
            copies=Fraction(falling(r,w),factorial(a)*factorial(b)*factorial(c))
            assert copies.denominator==1
            term+=copies*cs[a,b,c]**2
        chi+=term
        weights.append(str(term))
    bound=Fraction(50000*r,n)
    assert chi<=bound
    return dict(N=n,r=r,chi_square_exact=str(chi),
                chi_square_float=float(chi),N_over_r_times_chi=float(n*chi/r),
                theorem_bound_exact=str(bound),per_pauli_weight_exact=weights,
                inequality_exact_rational=True)


if __name__=='__main__':
    cases=[(128,1),(256,2),(512,4),(1024,8)]
    rows=[exact_chi(n,r) for n,r in cases]
    record=dict(status='exact_finite_rational_not_all_size_proof',
                initial_state='I/2^N',selected_stationary_occupation=0,
                method='Schur generating polynomial, all Pauli coefficients through r',
                results=rows)
    path=Path(__file__).resolve().parent/'exact_purity.json'
    path.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in x.items() if not k.endswith('_exact')}
                      for x in rows],indent=2))
