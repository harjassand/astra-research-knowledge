#!/usr/bin/env python3
"""Polynomial exact counting for primary Jordan blocks of length at most two.

Multiplicities and irreducible degree may grow. Pair moments and the integer
triangular inversion are manufactured, with every original input retained.
"""
from pathlib import Path
from functools import lru_cache
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_norm_slice_agent'),str(ROOT/'work_norm_frontier_agent')]
from cyclic_primary_pfaffian import kernel_primary_boundary,kernel_primary_refined_character,_integer_interpolate
from two_block_primary_pfaffian import _symmetric_coefficients
from krylov_square_source import Field,companion,quadratic_anf_sum,factor_polynomial
from simple_operator_quadratic import matrix_source_anf
from feedback_nilpotent_gaussians import shifted_trace_polynomial,qbinom
from cyclic_quadratic_primary_counter import polynomial_product

@lru_cache(None)
def two_semisimple_weights(t,d,q,refined=True,method='characters'):
    if t<1 or d<1 or t%d:raise ValueError('positive divisible ambient size required')
    if method not in ('characters','interpolation'):raise ValueError('unknown boundary refinement method')
    if refined and method=='characters':
        n=t//d;Q=q**d;evaluations=[];records=[]
        for v in range(n//2+1):
            values,record=kernel_primary_refined_character(t,d,q,n,semisimple=True,pair_alphabet=v)
            evaluations.append(values);record=dict(record);record.pop('formal_q_polynomials',None);records.append(record)
        weights={}
        for size in range(n+1):
            residues=[_symmetric_coefficients([row[size][h] for row in evaluations],size) for h in range(4)]
            for j in range(size+1):
                row=[];normalizer=qbinom(size,j,Q)
                for h in range(4):
                    quotient,remainder=divmod(residues[h][j],normalizer)
                    if remainder:raise AssertionError('semisimple pair normalization is not integral')
                    row.append(quotient)
                weights[size-j,j]=row
        return weights,dict(route='two semisimple alphabets and four manufactured phase characters',
            pfaffian_evaluations=records,second_alphabet_evaluations=n//2+1,
            boundary_evaluations=4,uniform_polynomial_time=True)
    n=t//d;Q=q**d;boundaries=range(t+1) if refined else (1,)
    tables=[];meta=[]
    for boundary in boundaries:
        evaluations=[]
        for v in range(n//2+1):
            values,record=kernel_primary_boundary(t,d,boundary,q,n,semisimple=True,pair_alphabet=v)
            evaluations.append(values);record=dict(record);record.pop('formal_q_polynomials',None);meta.append(record)
        pairs={}
        for size in range(n+1):
            coefficients=_symmetric_coefficients([row[size] for row in evaluations],size)
            for j,value in enumerate(coefficients):
                quotient,remainder=divmod(value,qbinom(size,j,Q))
                if remainder:raise AssertionError('semisimple pair normalization is not integral')
                pairs[size-j,j]=quotient
        tables.append(pairs)
    weights={}
    for i in range(n+1):
        for j in range(n+1-i):
            if not refined:weights[i,j]=[tables[0][i,j],0,0,0];continue
            coefficients=_integer_interpolate([table[i,j] for table in tables]);row=[0]*4;c=d*(i+j)
            for k,value in enumerate(coefficients):
                if k>c or (c-k)%2:
                    if value:raise AssertionError('invalid H-residue degree')
                else:row[((c-k)//2)%4]+=value
            weights[i,j]=row
    return weights,dict(route='two semisimple alphabets, Gaussian normalization and exact interpolation',
        pfaffian_evaluations=meta,second_alphabet_evaluations=n//2+1,
        boundary_evaluations=t+1 if refined else 1,uniform_polynomial_time=True)

def semisimple_product_coefficient(i,j,k,Q):
    if not 0<=k<=min(i,j):return 0
    value=Q**(k*(k-1)//2)*qbinom(i,k,Q)
    for h in range(k):value*=Q**(j-h)-1
    return value

def acquire_two_column_weights(t,d,q,refined=True):
    pairs,metadata=two_semisimple_weights(t,d,q,refined);n=t//d;Q=q**d;weights={}
    for size in range(n+1):
        for i in range(size//2+1):
            j=size-i;row=[Q**(i*j)*x for x in pairs[i,j]]
            for k in range(i):
                coefficient=semisimple_product_coefficient(i,j,k,Q)
                for residue in range(4):row[residue]-=coefficient*weights[k,size-2*k][residue]
            diagonal=semisimple_product_coefficient(i,j,i,Q);out=[]
            for value in row:
                quotient,remainder=divmod(value,diagonal)
                if remainder:raise AssertionError('two-column triangular division is not exact')
                out.append(quotient)
            weights[i,size-2*i]=out
    return weights,metadata

def two_column_hall_pairs(r,u,Q):
    for a in range(r+1):
        for c in range(r-a+1):
            z=r-a-c
            for j in range(u+1):
                number=qbinom(r,a,Q)*qbinom(r-a,c,Q)*qbinom(u,j,Q)*Q**(a*c+c*j+a*(u-j))
                yield (a,z+j),(c,z+u-j),number

def _operator(f,F,r,u):
    blocks=[companion(polynomial_product(f,f,F)) for _ in range(r)]+[companion(f) for _ in range(u)]
    n=sum(map(len,blocks));D=[[0]*n for _ in range(n)];offset=0
    for B in blocks:
        for i,row in enumerate(B):D[offset+i][offset:offset+len(B)]=row
        offset+=len(B)
    return D

def two_column_primary_gap(r,u,field_h,irreducible,beta,phi,eta=0):
    started=time.perf_counter();F=Field(field_h);q=F.q;f=list(irreducible);d=len(f)-1;phi=set(phi)
    if any(type(x) is not int or x<0 for x in (r,u)) or not r+u:
        raise ValueError('positive explicit module dimension required')
    if d<1 or f[-1]!=1 or any(type(x) is not int or not 0<=x<q for x in f) or factor_polynomial(f,F)!=[(f,1)]:
        raise ValueError('canonical monic irreducible polynomial required')
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('field coefficients and a Boolean quadratic trace source required')
    n=2*r+u;t=d*n;Q=q**d;weights,kernel=acquire_two_column_weights(t,d,q,refined=bool(eta))
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));answer=0;gaussians={};terms=[]
    for alpha,residual,number in two_column_hall_pairs(r,u,Q):
        c=d*(2*alpha[0]+alpha[1]);b=t-c
        if residual not in gaussians:
            D=_operator(f,F,*residual);G=[]
            for parity in range(2 if eta else 1):
                shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,beta)
                G.append(quadratic_anf_sum(matrix_source_anf(D,F,beta,shifted,eta),F.a*b*b))
            gaussians[residual]=G
        G=gaussians[residual];row=weights[alpha]
        value=sum(row[h]*(-1 if phase*(h*(h-1)//2)%2 else 1)*G[h%len(G)] for h in range(4))
        contribution=number*q**(c*(c-1)//2+c*b)*value;answer+=contribution
        terms.append(dict(span_twos_ones=alpha,quotient_twos_ones=residual,
            submodule_multiplicity=number,profile_weights=row,residual_gaussians=G,contribution=contribution))
    return q**(t*t)*answer,dict(route='two-column primary, semisimple pair Pfaffian and triangular inversion',
        matrix_size=t,field_modulus=field_h,primary_degree=d,twos=r,ones=u,
        original_bits=3*F.a*t*t,irreducible=f,beta=beta,eta=eta,phi=sorted(phi),
        terms=terms,profile_backend=kernel,residual_gaussian_types=len(gaussians),
        uniform_polynomial_time=True,enumerated_field_elements=0,enumerated_subspaces=0,
        enumerated_profiles=0,enumerated_original_assignments=0,seconds=time.perf_counter()-started)

def count_acquired_two_column_primary(algebra,beta,D,phi,eta=0):
    polynomial,primary=algebra.primary_data(D)
    if len(primary)!=1 or not primary[0]['jordan_columns'] or len(primary[0]['jordan_columns'])>2:
        raise ValueError('the operator is not one primary with blocks of length at most two')
    item=primary[0];columns=item['jordan_columns'];r=columns[1] if len(columns)>1 else 0;u=columns[0]-r
    gap,metadata=two_column_primary_gap(r,u,algebra.h,item['irreducible'],beta,phi,eta)
    metadata.update(acquired_reduced_charpoly=polynomial,acquired_primary_data=primary,
        supplied_primary_decomposition=False,supplied_matrix_units=False)
    return gap,metadata
