#!/usr/bin/env python3
"""Beta=0 counting with arbitrarily many equal-degree simple primaries.

Distinct source factors have one common degree d, which may grow. The profile
kernel is L(p_d^j), manufactured by the exponential Pfaffian. A trace-zero
centralizer translation kills every quotient of dimension greater than two.
"""
from pathlib import Path
import sys,itertools
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_matrix_root'),str(ROOT/'work_norm_frontier_agent')]
from krylov_square_source import Field,companion,quadratic_anf_sum,factor_polynomial
from simple_operator_quadratic import matrix_source_anf
from feedback_nilpotent_gaussians import shifted_trace_polynomial
from exponential_pfaffian_kernel import exponential_kernel,exponential_kernel_refined


def squarefree_equidegree_gap(field_h,factors,phi,eta=0):
    F=Field(field_h);factors=[list(f) for f in factors];phi=set(phi)
    if not factors:raise ValueError('positive explicit matrix size required')
    d=len(factors[0])-1;r=len(factors);t=d*r
    if d<1 or len({tuple(f) for f in factors})!=r:
        raise ValueError('distinct positive-degree irreducibles required')
    if any(not f or f[-1]!=1 or any(type(c) is not int or not 0<=c<F.q for c in f) for f in factors):
        raise ValueError('monic polynomials in canonical field coordinates required')
    if any(len(f)!=d+1 or factor_polynomial(f,F)!=[(f,1)] for f in factors):
        raise ValueError('all factors must be monic irreducibles of the same degree')
    if not 0<=eta<F.q or any(type(m) is not int or m<0 or
            m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('field eta and Boolean quadratic trace source required')
    if eta:weights,kernel=exponential_kernel_refined(t,F.q,d)
    else:
        unrefined,kernel=exponential_kernel(t,F.q,d=d)
        weights=[[value,0,0,0] for value in unrefined]
    answer=0;terms=[];gaussian_calls=0
    for number in range(min(r,2//d)+1):
        b=d*number;c=t-b;sum_gaussians=[0]*4
        for selected in itertools.combinations(range(r),number):
            D=[[0]*b for _ in range(b)]
            for block,index in enumerate(selected):
                A=companion(factors[index])
                for i in range(d):
                    for j in range(d):D[d*block+i][d*block+j]=A[i][j]
            parity_values=[]
            for parity in range(2 if eta else 1):
                shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,0)
                G=quadratic_anf_sum(matrix_source_anf(D,F,0,shifted,eta),F.a*b*b)
                parity_values.append(G);gaussian_calls+=1
            for residue in range(4):sum_gaussians[residue]+=parity_values[residue%len(parity_values)]
        contribution=F.q**(c*(c-1)//2+c*b)*sum(
            weights[r-number][h]*sum_gaussians[h] for h in range(4))
        answer+=contribution
        terms.append(dict(quotient_dimension=b,controlled_dimension=c,
            full_profile_weights=weights[r-number],sum_quotient_gaussians=sum_gaussians,
            contribution=contribution))
    gap=F.q**(t*t)*answer
    return gap,dict(route='squarefree equal-degree factors, exponential Pfaffian and small quotients',
        original_bits=3*F.a*t*t,matrix_size=t,field_modulus=field_h,
        primary_degree=d,distinct_primary_factors=factors,beta=0,eta=eta,
        trace_polynomial=sorted(phi),profile_backend=kernel,terms=terms,
        residual_gaussian_calls=gaussian_calls,maximum_quotient_dimension=2,
        uniform_polynomial_time=True,enumerated_profiles=0,enumerated_subspaces=0,
        enumerated_field_elements=0,enumerated_original_assignments=0)


def count_acquired_squarefree_equidegree(algebra,beta,D,phi,eta=0):
    if beta:raise ValueError('the squarefree equidegree route requires beta=0')
    polynomial,primary=algebra.primary_data(D)
    if not primary or any(p['multiplicity']!=1 or p['jordan_columns']!=[1] for p in primary):
        raise ValueError('source is not squarefree')
    if len({len(p['irreducible'])-1 for p in primary})!=1:
        raise ValueError('source factors do not have one common degree')
    gap,metadata=squarefree_equidegree_gap(algebra.h,[p['irreducible'] for p in primary],phi,eta)
    metadata.update(source_reduced_charpoly=polynomial,acquired_primary_data=primary,
        supplied_primary_decomposition=False,supplied_matrix_units=False)
    return gap,metadata
