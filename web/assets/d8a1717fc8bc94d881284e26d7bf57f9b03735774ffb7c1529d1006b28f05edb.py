#!/usr/bin/env python3
"""Exact Petz chi-square versus the matched one-qubit product reference.

Selected nu=0 model only. Computes axial orthonormal centered coefficients in
the basis sigma_+, sigma_-, sigma_z-bI, then compares small cases to matrices.
Finite arithmetic is scoped evidence, not all-size or external validation.
"""
from fractions import Fraction
from math import comb,factorial
from pathlib import Path
import json
import sys
import numpy as np
from exact_purity import falling
from check_local_access import bottom_density


def axial_coeffs(n,r):
    sectors=[]
    for m in range(n%2,n+1,2):
        low=(n-m)//2
        mult=comb(n,low)-(comb(n,low-1) if low else 0)
        sectors.append((m,low,(m+1)*mult))
    b=Fraction(-sum(m*wnum for m,l,wnum in sectors),n*2**n)
    raw={}
    for p in range(r//2+1):
        for k in range(r-2*p+1):
            w=2*p+k
            if w==0:
                raw[p,k]=Fraction(1)
                continue
            total=0
            for m,l,wnum in sectors:
                if p>l: continue
                inner=0
                for j in range(k//2+1):
                    h=k-2*j
                    if j>l-p or h>m: continue
                    sign=-1 if (p+j+h)%2 else 1
                    inner+=sign*comb(l,p)*comb(l-p,j)*comb(m,h)
                total+=wnum*inner
            raw[p,k]=Fraction(total*factorial(p)**2*factorial(k),
                               2**n*falling(n,w))
    centered={}
    for (p,k),value in raw.items():
        centered[p,k]=sum((comb(k,h)*(-b)**(k-h)*raw[p,h]
                            for h in range(k+1)),Fraction(0))
    assert centered[0,1]==0
    return b,centered


def exact_chi(n,r):
    b,cs=axial_coeffs(n,r)
    chi=Fraction(0)
    parts=[]
    for w in range(1,r+1):
        term=Fraction(0)
        for p in range(w//2+1):
            k=w-2*p
            multiplicity=Fraction(falling(r,w),factorial(p)**2*factorial(k))
            assert multiplicity.denominator==1
            term+=multiplicity*cs[p,k]**2*4**p/(1-b*b)**(p+k)
        chi+=term
        parts.append(str(term))
    return dict(N=n,r=r,one_qubit_bloch_z_exact=str(b),
                petz_chi_square_exact=str(chi),petz_chi_square_float=float(chi),
                N2_over_r2_times_chi=float(n*n*chi/(r*r)),
                per_weight_exact=parts,coefficient_norm_basis='tau-weighted sigma+/sigma-/centered z',
                arithmetic='exact rational')


def matrix_check(n,r,reference):
    rho=bottom_density(n)
    d=2**r
    red=np.trace(rho.reshape(d,2**(n-r),d,2**(n-r)),axis1=1,axis2=3)
    b=float(Fraction(reference['one_qubit_bloch_z_exact']))
    diag=np.array([((1+b)/2)**(r-i.bit_count())
                   *((1-b)/2)**i.bit_count() for i in range(d)])
    direct=float(np.sum((red@red).diagonal()/diag)-1)
    assert abs(direct-reference['petz_chi_square_float'])<2e-11
    return dict(N=n,r=r,matrix_petz_chi_square=direct,
                exact_petz_chi_square=reference['petz_chi_square_float'],
                difference=direct-reference['petz_chi_square_float'])


if __name__=='__main__':
    # Trusted, locally constructed exact fractions exceed Python's default
    # decimal-display limit; computation itself is bounded by N=1024,r=8.
    sys.set_int_max_str_digits(50000)
    small=[]
    for n in range(2,9):
        for r in range(1,min(n,4)+1):
            x=exact_chi(n,r)
            small.append(matrix_check(n,r,x))
    cases=[(128,1),(128,2),(256,2),(512,4),(1024,8)]
    large=[exact_chi(n,r) for n,r in cases]
    for row in large:
        assert Fraction(row['petz_chi_square_exact'])<=Fraction(2*10**9*row['r']**2,row['N']**2)
    record=dict(status='exact_finite_arithmetic_with_small_matrix_cross_check',
                model='nu=0 selected stationary state with white Schur weights',
                small_matrix_checks=small,exact_cases=large,
                warning='Not formal proof replay or specialist validation.')
    (Path(__file__).resolve().parent/'exact_centered_purity.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(matrix_fixtures=len(small),cases=[{k:v for k,v in x.items()
                      if k in ['N','r','petz_chi_square_float','N2_over_r2_times_chi']}
                      for x in large]),indent=2))
