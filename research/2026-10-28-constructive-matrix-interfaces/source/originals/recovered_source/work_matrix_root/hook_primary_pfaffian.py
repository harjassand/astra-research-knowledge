#!/usr/bin/env python3
"""Exact primary counter for one arbitrary block and arbitrarily many simples.

The hook Hall table is manufactured by projection and graph maps. The
profile weights come from one cyclic and one semisimple alphabet. Neither
the row count nor the column count of the Jordan type is bounded.
"""
from pathlib import Path
from functools import lru_cache
from collections import defaultdict
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_norm_slice_agent'),str(ROOT/'work_norm_frontier_agent')]
from cyclic_primary_pfaffian import kernel_primary_boundary,kernel_primary_refined_character,_integer_interpolate
from krylov_square_source import Field,companion,quadratic_anf_sum,factor_polynomial
from simple_operator_quadratic import matrix_source_anf
from feedback_nilpotent_gaussians import shifted_trace_polynomial,qbinom
from cyclic_quadratic_primary_counter import polynomial_product


def hook_shape(length,simples):
    if any(type(x) is not int or x<0 for x in (length,simples)):
        raise ValueError('nonnegative hook parameters required')
    return tuple(([length] if length else [])+[1]*simples)


def canonical_hook(shape):
    """Use (0,u) for a semisimple module, otherwise (S,u) with S>=2."""
    shape=tuple(shape)
    if not shape:return 0,0
    if shape[0]<1 or any(x!=1 for x in shape[1:]):raise ValueError('a hook partition is required')
    if shape[0]==1:return 0,len(shape)
    return shape[0],len(shape)-1


@lru_cache(None)
def hook_hall_pairs(length,simples,Q):
    """All exact submodule/quotient pairs, without listing partitions/subspaces."""
    S=length;U=simples
    if type(S) is not int or S<1 or type(U) is not int or U<0 or type(Q) is not int or Q<2:
        raise ValueError('positive long-block length and valid simple multiplicity required')
    table=defaultdict(int)
    for j in range(U+1):
        choose=qbinom(U,j,Q)
        table[hook_shape(0,j),hook_shape(S,U-j)]+=choose
        for A in range(1,S+1):
            k=S-A;alpha=hook_shape(A,j)
            table[alpha,hook_shape(k,U-j)]+=choose
            if U>j:
                table[alpha,hook_shape(k+1,U-j-1)]+=choose*(Q**(U-j)-1)
    return tuple((alpha,rho,number) for (alpha,rho),number in sorted(table.items()) if number)


@lru_cache(None)
def mixed_cyclic_semisimple_weights(t,d,q,refined=True):
    """Return L(h_i[p_d] F_(1^j)[p_d]), refined by H mod 4."""
    if t<1 or d<1 or t%d:raise ValueError('positive divisible ambient size required')
    n=t//d;Q=q**d;evaluations=[];records=[]
    for v in range(n+1):
        if refined:
            values,record=kernel_primary_refined_character(t,d,q,n,hybrid_alphabet=v)
        else:
            ordinary,record=kernel_primary_boundary(t,d,1,q,n,hybrid_alphabet=v)
            values=[[x,0,0,0] for x in ordinary]
        evaluations.append(values);record=dict(record);record.pop('formal_q_polynomials',None);records.append(record)
    pochhammer=[1]
    for j in range(1,n+1):pochhammer.append(pochhammer[-1]*(1-Q**j))
    weights={}
    for size in range(n+1):
        coefficients=[_integer_interpolate([row[size][h] for row in evaluations[:size+1]]) for h in range(4)]
        for j in range(size+1):
            divisor,remainder=divmod(pochhammer[size],pochhammer[j])
            if remainder:raise AssertionError('Pochhammer clearing factor is not integral')
            row=[]
            for h in range(4):
                value,remainder=divmod(coefficients[h][j],divisor)
                if remainder:raise AssertionError('mixed-alphabet normalization is not integral')
                row.append(value)
            weights[size-j,j]=row
    return weights,dict(route='one cyclic and one semisimple alphabet, exact coefficient recovery',
        alphabet_evaluations=n+1,boundary_evaluations=4 if refined else 1,
        pfaffian_evaluations=records,uniform_polynomial_time=True,
        enumerated_profiles=0,enumerated_subspaces=0,enumerated_field_elements=0)


def hooks_from_mixed_products(products,n,Q):
    """Q^u h_s F_(1^u)=F_(s,1^u)+(Q^u-1)F_(s+1,1^(u-1))."""
    weights={():[1,0,0,0]}
    for size in range(1,n+1):
        for u in range(size):
            s=size-u;row=[Q**u*x for x in products[s,u]]
            if u:
                previous=weights[hook_shape(s+1,u-1)]
                for h in range(4):row[h]-=(Q**u-1)*previous[h]
            weights[hook_shape(s,u)]=row
        if weights[(1,)*size]!=products[0,size]:
            raise AssertionError('independent semisimple endpoint failed to agree')
    return weights


@lru_cache(None)
def acquire_hook_weights(t,d,q,refined=True):
    products,metadata=mixed_cyclic_semisimple_weights(t,d,q,refined)
    return hooks_from_mixed_products(products,t//d,q**d),metadata


def _hook_operator(f,F,length,simples):
    blocks=[]
    if length:
        power=[1]
        for _ in range(length):power=polynomial_product(power,f,F)
        blocks.append(companion(power))
    blocks.extend(companion(f) for _ in range(simples))
    t=sum(map(len,blocks));D=[[0]*t for _ in range(t)];offset=0
    for B in blocks:
        for i,row in enumerate(B):D[offset+i][offset:offset+len(B)]=row
        offset+=len(B)
    return D


def hook_primary_gap(length,simples,field_h,irreducible,beta,phi,eta=0):
    started=time.perf_counter();F=Field(field_h);q=F.q;f=list(irreducible);phi=set(phi)
    S=length;U=simples;d=len(f)-1
    if type(S) is not int or S<1 or type(U) is not int or U<0:
        raise ValueError('one positive block and nonnegative simple multiplicity required')
    if d<1 or f[-1]!=1 or any(type(x) is not int or not 0<=x<q for x in f) or factor_polynomial(f,F)!=[(f,1)]:
        raise ValueError('a canonical monic irreducible polynomial is required')
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('field coefficients and a Boolean quadratic trace source required')
    t=d*(S+U);Q=q**d;weights,kernel=acquire_hook_weights(t,d,q,refined=bool(eta))
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));answer=0;gaussians={};terms=[]
    for alpha,rho,number in hook_hall_pairs(S,U,Q):
        c=d*sum(alpha);b=t-c
        if rho not in gaussians:
            D=_hook_operator(f,F,*canonical_hook(rho));G=[]
            for parity in range(2 if eta else 1):
                shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,beta)
                G.append(quadratic_anf_sum(matrix_source_anf(D,F,beta,shifted,eta),F.a*b*b))
            gaussians[rho]=G
        row=weights[alpha];G=gaussians[rho]
        value=sum(row[h]*(-1 if phase*(h*(h-1)//2)%2 else 1)*G[h%len(G)] for h in range(4))
        contribution=number*q**(c*(c-1)//2+c*b)*value;answer+=contribution
        terms.append(dict(span_type=alpha,quotient_type=rho,submodule_multiplicity=number,
            profile_weights=row,residual_gaussians=G,contribution=contribution))
    return q**(t*t)*answer,dict(route='unbounded hook primary, mixed-alphabet finite Pfaffian',
        matrix_size=t,field_modulus=field_h,primary_degree=d,long_block=S,simple_blocks=U,
        original_bits=3*F.a*t*t,irreducible=f,beta=beta,eta=eta,phi=sorted(phi),
        terms=terms,profile_backend=kernel,residual_gaussian_types=len(gaussians),
        uniform_polynomial_time=True,enumerated_field_elements=0,enumerated_subspaces=0,
        enumerated_profiles=0,enumerated_original_assignments=0,seconds=time.perf_counter()-started)


def count_acquired_hook_primary(algebra,beta,D,phi,eta=0):
    polynomial,primary=algebra.primary_data(D)
    if len(primary)!=1:raise ValueError('one primary factor is required')
    item=primary[0];columns=item['jordan_columns']
    if not columns or any(x!=1 for x in columns[1:]):
        raise ValueError('the acquired primary partition is not a hook')
    S=len(columns);U=columns[0]-1
    gap,metadata=hook_primary_gap(S,U,algebra.h,item['irreducible'],beta,phi,eta)
    metadata.update(acquired_reduced_charpoly=polynomial,acquired_primary_data=primary,
        supplied_primary_decomposition=False,supplied_matrix_units=False)
    return gap,metadata
