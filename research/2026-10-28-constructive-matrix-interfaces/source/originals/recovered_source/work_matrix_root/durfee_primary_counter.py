#!/usr/bin/env python3
"""Exact primary counting in manufactured super-Hall coordinates.

Polynomial for each fixed number of mixed alphabet letters; that parameter
is charged when it grows. No unrestricted partition basis is constructed.
"""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_norm_frontier_agent'),str(ROOT/'work_norm_slice_agent')]
from fat_hook_hall import FatHookBasis,fat_shapes,smallest_fat_hook,n_stat,contained
from cyclic_primary_pfaffian import kernel_primary_boundary,kernel_primary_refined_character
from structured_pfaffian import kernel_structured_actual_q,kernel_structured_refined_actual_q
from krylov_square_source import Field,companion,quadratic_anf_sum,factor_polynomial
from simple_operator_quadratic import matrix_source_anf
from feedback_nilpotent_gaussians import shifted_trace_polynomial
from cyclic_quadratic_primary_counter import polynomial_product


@lru_cache(None)
def manufacture_primary_evaluation_plan(m,r,s,Q):
    bases=[FatHookBasis(j,r,s,Q) for j in range(m+1)]
    highest=bases[-1].evaluation_plan();points=highest['points']
    plans=[basis.evaluation_plan(points) for basis in bases]
    return bases,points,plans,dict(cyclic_alphabets=r,semisimple_alphabets=s,
        total_alphabets=r+s,highest_degree=m,highest_degree_dimension=len(points),
        simplex_candidates_tested=highest['candidates_tested'],evaluation_points=points,
        dimensions_by_degree=[len(b.entries) for b in bases],
        independent_rows_by_degree=[p['indices'] for p in plans],
        exact_evaluation_ranks_verified=True,highest_degree_rows_reused=True)


@lru_cache(None)
def primary_fat_hook_weights(t,d,q,r,s,refined=True,backend='structured_actual_q',maximum=None):
    if t<1 or d<1 or t%d or r+s<1:raise ValueError('positive dimensions and a nonempty alphabet required')
    if backend not in ('structured_actual_q','packed_reference'):raise ValueError('unknown exact kernel backend')
    m=t//d if maximum is None else maximum
    if type(m) is not int or not 0<=d*m<=t:raise ValueError('source degree exceeds the ambient dimension')
    Q=q**d;bases,points,plans,plan_metadata=manufacture_primary_evaluation_plan(m,r,s,Q)
    evaluations=[];records=[];begun=time.perf_counter()
    for point in points:
        alphabets=(tuple(point[:r]),tuple(point[r:]))
        if refined:
            kernel=kernel_structured_refined_actual_q if backend=='structured_actual_q' else kernel_primary_refined_character
            values,record=kernel(t,d,q,m,general_alphabets=alphabets)
        else:
            kernel=kernel_structured_actual_q if backend=='structured_actual_q' else kernel_primary_boundary
            ordinary,record=kernel(t,d,1,q,m,general_alphabets=alphabets)
            values=[[x,0,0,0] for x in ordinary]
        evaluations.append(values);record=dict(record);record.pop('formal_q_polynomials',None);records.append(record)
    weights={};normalizer=1
    for degree,(basis,plan) in enumerate(zip(bases,plans)):
        if s and degree:normalizer*=1-Q**degree
        for lead,shape,c,poly in basis.entries:weights[shape]=[0]*4
        for h in range(4 if refined else 1):
            values=[Fraction(evaluations[i][degree][h],normalizer) for i in plan['indices']]
            for shape,c in basis.decode_evaluations(values,plan).items():
                value=c*Q**n_stat(shape)
                if value.denominator!=1:raise AssertionError('reconstructed primary profile weight is not integral')
                weights[shape][h]=value.numerator
    if weights[()]!=[1,0,0,0]:raise AssertionError('empty profile weight mismatch')
    return weights,dict(route='manufactured super-Hall quotient and general finite Pfaffian',
        evaluation_plan=plan_metadata,pfaffian_evaluations=records,
        boundary_evaluations=(1 if backend=='structured_actual_q' or not refined else 4),kernel_calls=len(points),
        kernel_backend=backend,
        unrestricted_partitions_enumerated=0,manufactured_shapes=len(weights),
        arithmetic_bound='(m+1)^{O(r+s)} poly(a,t)',
        polynomial_for_fixed_alphabet_count=True,seconds=time.perf_counter()-begun)


def primary_fat_hook_pairs(rows,r,s,Q):
    m=sum(rows);basis=FatHookBasis(m,r,s,Q);out=[]
    for size in range(m+1):
        for alpha in fat_shapes(size,r,s):
            if not contained(alpha,rows):continue
            for rho in fat_shapes(m-size,r,s):
                if not contained(rho,rows):continue
                number=basis.hall_product(alpha,rho).get(rows,0)
                if number:out.append((alpha,rho,number))
    return tuple(out)


def _quotient_operator(f,F,rows):
    powers=[[1]]
    for _ in range(max(rows,default=0)):powers.append(polynomial_product(powers[-1],f,F))
    blocks=[companion(powers[j]) for j in rows];n=sum(map(len,blocks));D=[[0]*n for _ in range(n)];offset=0
    for B in blocks:
        for i,row in enumerate(B):D[offset+i][offset:offset+len(B)]=row
        offset+=len(B)
    return D


def primary_partition_gap(rows,field_h,irreducible,beta,phi,eta=0,max_alphabet_count=None,alphabet_sizes=None,backend='structured_actual_q'):
    started=time.perf_counter();rows=tuple(rows);F=Field(field_h);q=F.q;f=list(irreducible);d=len(f)-1;phi=set(phi)
    if not rows or any(type(x) is not int or x<1 for x in rows) or tuple(sorted(rows,reverse=True))!=rows:
        raise ValueError('a positive primary partition is required')
    if d<1 or f[-1]!=1 or any(type(x) is not int or not 0<=x<q for x in f) or factor_polynomial(f,F)!=[(f,1)]:
        raise ValueError('a canonical monic irreducible polynomial is required')
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('valid field coefficients and a Boolean quadratic trace source required')
    r,s=smallest_fat_hook(rows) if alphabet_sizes is None else alphabet_sizes
    if any(type(x) is not int or x<0 for x in (r,s)) or not r+s or (r<len(rows) and rows[r]>s):
        raise ValueError('the specified mixed alphabet does not contain the primary shape')
    if max_alphabet_count is not None and r+s>max_alphabet_count:
        raise ValueError('manufactured alphabet count exceeds the specified family bound')
    m=sum(rows);t=d*m;Q=q**d;weights,kernel=primary_fat_hook_weights(t,d,q,r,s,bool(eta),backend)
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));answer=0;gaussians={};terms=[]
    for alpha,rho,number in primary_fat_hook_pairs(rows,r,s,Q):
        c=d*sum(alpha);b=t-c
        if rho not in gaussians:
            D=_quotient_operator(f,F,rho);G=[]
            for parity in range(2 if eta else 1):
                shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,beta)
                G.append(quadratic_anf_sum(matrix_source_anf(D,F,beta,shifted,eta),F.a*b*b))
            gaussians[rho]=G
        row=weights[alpha];G=gaussians[rho]
        value=sum(row[h]*(-1 if phase*(h*(h-1)//2)%2 else 1)*G[h%len(G)] for h in range(4))
        contribution=number*q**(c*(c-1)//2+c*b)*value;answer+=contribution
        terms.append(dict(span_type=alpha,quotient_type=rho,submodule_multiplicity=number,
            profile_weights=row,residual_gaussians=G,contribution=contribution))
    durfee=sum(x>=i+1 for i,x in enumerate(rows))
    return q**(t*t)*answer,dict(route='primary super-Hall quotient, acquired mixed alphabet',
        matrix_size=t,field_modulus=field_h,primary_degree=d,primary_partition=rows,durfee_rank=durfee,
        cyclic_alphabets=r,semisimple_alphabets=s,total_alphabets=r+s,
        requested_alphabet_bound=max_alphabet_count,original_bits=3*F.a*t*t,
        irreducible=f,beta=beta,eta=eta,phi=sorted(phi),terms=terms,
        profile_backend=kernel,residual_gaussian_types=len(gaussians),
        polynomial_for_fixed_alphabet_count=True,uniform_in_growing_alphabet_count=False,
        bit_time_bound='(m+1)^{O(r+s)} poly(a,t)',
        enumerated_field_elements=0,enumerated_subspaces=0,enumerated_original_assignments=0,
        unrestricted_partitions_enumerated=0,seconds=time.perf_counter()-started)


def count_acquired_four_alphabet_primary(algebra,beta,D,phi,eta=0):
    """The fixed-budget polynomial frontend; four is a literal constant."""
    polynomial,primary=algebra.primary_data(D)
    if len(primary)!=1:raise ValueError('one primary factor is required')
    from fat_hook_hall import transpose
    item=primary[0];rows=transpose(tuple(item['jordan_columns']))
    gap,metadata=primary_partition_gap(rows,algebra.h,item['irreducible'],beta,phi,eta,max_alphabet_count=4)
    metadata.update(acquired_reduced_charpoly=polynomial,acquired_primary_data=primary,
        supplied_primary_decomposition=False,supplied_matrix_units=False,
        uniform_polynomial_time=True,fixed_alphabet_bound=4)
    return gap,metadata
