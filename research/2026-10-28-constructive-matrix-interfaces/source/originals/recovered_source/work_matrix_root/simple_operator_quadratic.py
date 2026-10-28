#!/usr/bin/env python3
"""Exact polynomial counting for a source operator of unbounded irreducible degree.

All beta and eta are supported in
Tr(tr(XYZ)+beta*e2(X)+tr(DX^2)+eta*tr(DX))+phi(tr X).
The supplied polynomial is verified irreducible; raw acquisition uses the
separate certified intrinsic frontend. No profiles or field elements are listed.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))
from krylov_square_source import (Field,companion,source_evaluator,
    quadratic_anf,quadratic_anf_sum,polynomial_value,factor_polynomial)
from two_invariant_quadratic_matrix import gaussian_rows


def matrix_source_anf(D,F,beta,phi,eta=0):
    """Manufacture the complete binary quadratic by coefficient contractions.

    Matrix products are expanded symbolically over the supplied field
    basis; no assignments or quadratic-oracle probes are used.
    """
    t=len(D);a=F.a;out=set();tables={}
    def toggle(m):
        if m in out:out.remove(m)
        else:out.add(m)
    def product(c,left,right):
        if not c:return
        if c not in tables:
            tables[c]=[(i,j) for i in range(a) for j in range(a)
                if F.trace(F.mul(c,F.mul(1<<i,1<<j)))]
        for i,j in tables[c]:toggle((1<<(a*left+i))|(1<<(a*right+j)))
    for i in range(t):
        for j in range(i+1,t):
            product(beta,i*t+i,j*t+j)
            product(beta,i*t+j,j*t+i)
    for i in range(t):
        for j in range(t):
            if D[i][j]:
                for k in range(t):product(D[i][j],j*t+k,k*t+i)
                coefficient=F.mul(eta,D[i][j])
                for bit in range(a):
                    if F.trace(F.mul(coefficient,1<<bit)):
                        toggle(1<<(a*(j*t+i)+bit))
    for monomial in phi:
        coordinates=[bit for bit in range(a) if monomial>>bit&1]
        if not coordinates:toggle(0)
        elif len(coordinates)==1:
            for i in range(t):toggle(1<<(a*(i*t+i)+coordinates[0]))
        else:
            for i in range(t):
                for j in range(t):toggle((1<<(a*(i*t+i)+coordinates[0]))|
                                         (1<<(a*(j*t+j)+coordinates[1])))
    return out

def simple_operator_gap(t,field_h,irreducible_polynomial,beta,phi,eta=0):
    F=Field(field_h);q=F.q;phi=set(phi);polynomial=list(irreducible_polynomial)
    if type(t) is not int or t<1 or not 0<=beta<q or not 0<=eta<q:
        raise ValueError('invalid explicit matrix size or field coefficient')
    if len(polynomial)!=t+1 or polynomial[-1]!=1 or any(type(x) is not int or not 0<=x<q for x in polynomial):
        raise ValueError('monic degree-t polynomial over the acquired field required')
    if factor_polynomial(polynomial,F)!=[(polynomial,1)]:
        raise ValueError('source polynomial is not irreducible')
    if any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('Boolean quadratic trace polynomial required')
    gaussian=gaussian_rows(t,q)
    # The same four-residue transfer as for a regular chain, with one
    # less q-power per remaining height from the irreducible profile formula.
    tail=[[[[0]*4 for _ in range(2)] for _ in range(t+1)] for _ in range(t+1)]
    for k in range(t+1):
        for e in range(2):tail[0][k][e][0]=1
    transitions=0
    for remaining in range(1,t+1):
        for previous in range(1,t+1):
            for height in range(1,min(previous,remaining)+1):
                weight=q**(height*(height-1)//2)*gaussian[previous][height]
                for level in range(2):
                    for residue in range(4):
                        tail[remaining][previous][level][(residue+level*height)%4] += \
                            weight*tail[remaining-height][height][1-level][residue]
                transitions+=1
    profiles=[0]*4;product=1
    for k in range(1,t+1):
        product*=q**(t-k+1)-1
        first,remainder=divmod(product*(q**t-1),q**k-1)
        if remainder:raise AssertionError('simple profile first-height weight is not integral')
        for residue in range(4):profiles[residue]+=first*tail[t-k][k][1][residue]
    # K=0 is one ordinary quadratic Gaussian on a*t^2 bits. This calculation
    # does not enumerate its assignments, even when the source degree grows.
    D=companion(polynomial);dimension=F.a*t*t
    source=matrix_source_anf(D,F,beta,phi,eta)
    free_gaussian=quadratic_anf_sum(source,dimension)
    phase=F.trace(F.mul(beta,F.mul(eta,eta)))
    signs=[1-2*(polynomial_value(phi,eta if r%2 else 0)^((phase*(r*(r-1)//2))%2))
           for r in range(4)]
    controlled=q**(t*(t-1)//2)*sum(w*s for w,s in zip(profiles,signs))
    gap=q**(t*t)*(free_gaussian+controlled)
    return gap,dict(route='irreducible source operator, four-residue profile aggregation',
        operator_class='unbounded irreducible degree',matrix_size=t,field_degree=F.a,
        field_modulus=field_h,source_polynomial=polynomial,beta=beta,eta=eta,
        trace_quadratic_anf=sorted(phi),profile_weights_by_even_height_mod4=profiles,
        free_quadratic_gaussian=free_gaussian,source_anf_terms=len(source),controlled_phase_signs=signs,
        profile_transitions=transitions,uniform_polynomial_time=True,
        enumerated_profiles=0,enumerated_subspaces=0,enumerated_field_elements=0,
        enumerated_original_assignments=0)

def count_acquired_simple_operator(algebra,beta,D,phi,eta=0):
    polynomial,primary=algebra.primary_data(D)
    if len(primary)!=1 or len(primary[0]['irreducible'])!=algebra.t+1 or \
            primary[0]['jordan_columns']!=[1]:
        raise ValueError('source operator does not have an irreducible degree-t polynomial')
    gap,backend=simple_operator_gap(algebra.t,algebra.h,polynomial,beta,phi,eta)
    backend.update(acquired_primary_data=primary)
    return gap,backend
