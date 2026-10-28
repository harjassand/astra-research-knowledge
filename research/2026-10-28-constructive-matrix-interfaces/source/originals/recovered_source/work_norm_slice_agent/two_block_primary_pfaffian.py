#!/usr/bin/env python3
"""Exact polynomial backend for a primary operator with two equal blocks.

Only two-alphabet coefficient interpolation and O(s^2) Smith types are used.
No field elements, subspaces, profiles, or arbitrary partition lists are used.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_matrix_root'),str(ROOT/'work_norm_frontier_agent')]
from krylov_square_source import Field,companion,quadratic_anf_sum,factor_polynomial
from simple_operator_quadratic import matrix_source_anf
from feedback_nilpotent_gaussians import shifted_trace_polynomial
from cyclic_quadratic_primary_counter import polynomial_product
from cyclic_primary_pfaffian import kernel_primary_boundary,kernel_primary_refined_character,_integer_interpolate


def _symmetric_coefficients(values,degree):
    """Coefficients c_j=c_(degree-j), from values at 0,...,floor(degree/2)."""
    n=degree//2+1
    if len(values)<n:raise ValueError('insufficient palindromic evaluations')
    A=[]
    for v in range(n):
        row=[Fraction(v**j if 2*j==degree else v**j+v**(degree-j))
             for j in range(n)]
        A.append(row+[Fraction(values[v])])
    for column in range(n):
        pivot=next((i for i in range(column,n) if A[i][column]),None)
        if pivot is None:raise AssertionError('palindromic evaluation matrix singular')
        A[column],A[pivot]=A[pivot],A[column]
        leading=A[column][column];A[column]=[x/leading for x in A[column]]
        for i in range(n):
            if i!=column and A[i][column]:
                coefficient=A[i][column]
                A[i]=[x-coefficient*y for x,y in zip(A[i],A[column])]
    out=[0]*(degree+1)
    for j in range(n):
        value=A[j][-1]
        if value.denominator!=1:raise AssertionError('nonintegral pair-alphabet coefficient')
        out[j]=out[degree-j]=value.numerator
    return out


@lru_cache(None)
def two_cyclic_weights_interpolation(t,d,q,refined=True):
    """Preserved ordinary-boundary interpolation reference for pair moments."""
    if t<1 or d<1 or t%d:raise ValueError('positive divisible ambient dimension required')
    e=t//d;boundaries=range(t+1) if refined else (1,)
    boundary_values=[];metas=[]
    for boundary in boundaries:
        evaluations=[]
        for v in range(e//2+1):
            values,meta=kernel_primary_boundary(t,d,boundary,q,e,pair_alphabet=v)
            evaluations.append(values)
            meta=dict(meta);meta.pop('formal_q_polynomials',None);metas.append(meta)
        pairs={}
        for degree in range(e+1):
            coefficients=_symmetric_coefficients([row[degree] for row in evaluations],degree)
            for j,value in enumerate(coefficients):pairs[degree-j,j]=value
        boundary_values.append(pairs)
    out={}
    for i in range(e+1):
        for j in range(e+1-i):
            if not refined:out[i,j]=[boundary_values[0][i,j],0,0,0];continue
            c=d*(i+j)
            polynomial=_integer_interpolate([row[i,j] for row in boundary_values]);weights=[0]*4
            for k,value in enumerate(polynomial):
                if k>c or (c-k)%2:
                    if value:raise AssertionError('boundary parity/degree mismatch')
                else:weights[((c-k)//2)%4]+=value
            out[i,j]=weights
    return out,dict(route='two cyclic alphabets in finite Schur Pfaffian',
        ambient_size=t,primary_degree=d,pfaffian_evaluations=metas,
        second_alphabet_evaluations=e//2+1,boundary_evaluations=t+1 if refined else 1,
        uniform_polynomial_time=True,enumerated_profiles=0,enumerated_subspaces=0)


@lru_cache(None)
def two_cyclic_weights(t,d,q,refined=True):
    """Return pair moments, using four characters before alphabet interpolation."""
    if not refined:return two_cyclic_weights_interpolation(t,d,q,False)
    if t<1 or d<1 or t%d:raise ValueError('positive divisible ambient dimension required')
    e=t//d;evaluations=[];records=[];projections=[]
    for v in range(e//2+1):
        values,meta=kernel_primary_refined_character(t,d,q,e,pair_alphabet=v)
        evaluations.append(values);projection=dict(meta)
        records.extend(projection.pop('normalized_character_evaluations'))
        projections.append(projection)
    out={}
    for degree in range(e+1):
        for j in range(degree+1):out[degree-j,j]=[0]*4
        for residue in range(4):
            coefficients=_symmetric_coefficients([row[degree][residue] for row in evaluations],degree)
            for j,value in enumerate(coefficients):out[degree-j,j][residue]=value
    return out,dict(route='two cyclic alphabets with four-character profile refinement',
        ambient_size=t,primary_degree=d,pfaffian_evaluations=records,character_projections=projections,
        second_alphabet_evaluations=e//2+1,boundary_evaluations=4,
        total_pfaffian_evaluations=4*(e//2+1),
        ordinary_interpolation_reference='two_cyclic_weights_interpolation',
        uniform_polynomial_time=True,enumerated_profiles=0,enumerated_subspaces=0)


def _quotient_matrix(powers,first,second):
    blocks=[companion(powers[k]) for k in (first,second) if k]
    n=sum(len(B) for B in blocks);D=[[0]*n for _ in range(n)];offset=0
    for B in blocks:
        for i,row in enumerate(B):D[offset+i][offset:offset+len(B)]=row
        offset+=len(B)
    return D


def two_block_primary_gap(length,field_h,irreducible,beta,phi,eta=0):
    """Full-domain gap for the source with Jordan type (length,length)."""
    begun=time.perf_counter();F=Field(field_h);q=F.q;f=list(irreducible);d=len(f)-1;phi=set(phi)
    if type(length) is not int or length<1:raise ValueError('positive explicit block length required')
    if d<1 or f[-1]!=1 or any(type(c) is not int or not 0<=c<q for c in f) or factor_polynomial(f,F)!=[(f,1)]:
        raise ValueError('a canonical monic irreducible polynomial is required')
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('field coefficients and a Boolean quadratic trace source required')
    s=length;t=2*s*d;Q=q**d
    weights,kernel=two_cyclic_weights(t,d,q,refined=bool(eta))
    powers=[[1]]
    for _ in range(s):powers.append(polynomial_product(powers[-1],f,F))
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));answer=0;terms=[];gaussian_calls=0
    for A in range(s+1):
        for B in range(A+1):
            # Q^B h_A h_B + sum_(k=1)^B (Q^(B-k)-Q^(B-k+1)) h_(A+k)h_(B-k).
            row=[Q**B*x for x in weights[A,B]]
            for k in range(1,B+1):
                coefficient=Q**(B-k)-Q**(B-k+1)
                for r in range(4):row[r]+=coefficient*weights[A+k,B-k][r]
            c=d*(A+B);b=t-c;D=_quotient_matrix(powers,s-B,s-A)
            G=[]
            for parity in range(2 if eta else 1):
                shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,beta)
                G.append(quadratic_anf_sum(matrix_source_anf(D,F,beta,shifted,eta),F.a*b*b));gaussian_calls+=1
            number=1 if A==B else (Q+1)*Q**(A-B-1)
            value=sum(row[r]*(-1 if phase*(r*(r-1)//2)%2 else 1)*G[r%len(G)] for r in range(4))
            contribution=number*q**(c*(c-1)//2+c*b)*value;answer+=contribution
            terms.append(dict(controlled_type=[A,B],quotient_type=[s-B,s-A],
                submodule_multiplicity=number,controlled_dimension=c,
                profile_weights=row,residual_gaussians=G,contribution=contribution))
    gap=q**(t*t)*answer
    return gap,dict(route='two equal primary blocks, Smith types and two-alphabet Pfaffian',
        original_bits=3*F.a*t*t,matrix_size=t,field_modulus=field_h,
        primary_degree=d,block_length=s,irreducible=f,beta=beta,eta=eta,phi=sorted(phi),
        terms=terms,profile_backend=kernel,residual_gaussian_calls=gaussian_calls,
        uniform_polynomial_time=True,enumerated_profiles=0,enumerated_subspaces=0,
        enumerated_field_elements=0,enumerated_original_assignments=0,
        seconds=time.perf_counter()-begun)


def count_acquired_two_equal_blocks(algebra,beta,D,phi,eta=0):
    polynomial,primary=algebra.primary_data(D)
    if len(primary)!=1 or not primary[0]['jordan_columns'] or any(x!=2 for x in primary[0]['jordan_columns']):
        raise ValueError('the operator is not one primary with two equal blocks')
    item=primary[0]
    gap,meta=two_block_primary_gap(len(item['jordan_columns']),algebra.h,item['irreducible'],beta,phi,eta)
    meta.update(acquired_reduced_charpoly=polynomial,acquired_primary_data=primary,
        supplied_primary_decomposition=False,supplied_matrix_units=False)
    return gap,meta


@lru_cache(None)
def _two_variable_hl(shape,Q):
    """P_shape(x,y;Q^-1), encoded by the exponent of y, with <=2 rows."""
    if len(shape)>2:raise ValueError('at most two rows required')
    a=shape[0] if shape else 0;b=shape[1] if len(shape)>1 else 0
    if a<b or b<0:raise ValueError('a partition is required')
    n=a+b;out=[Fraction(0)]*(n+1)
    if a==b:out[a]=Fraction(1)
    else:
        out[b]=out[a]=Fraction(1)
        for i in range(b+1,a):out[i]=1-Fraction(1,Q)
    return tuple(out)


@lru_cache(None)
def two_variable_hall(alpha,beta,Q):
    """All <=2-row Hall coefficients, from their exact two-variable quotient."""
    left=_two_variable_hl(alpha,Q);right=_two_variable_hl(beta,Q);n=len(left)+len(right)-2
    residual=[Fraction(0)]*(n+1)
    for i,x in enumerate(left):
        if x:
            for j,y in enumerate(right):
                if y:residual[i+j]+=x*y
    result=[];na=alpha[1] if len(alpha)>1 else 0;nb=beta[1] if len(beta)>1 else 0
    for b in range(n//2+1):
        a=n-b;coefficient=residual[b]
        if not coefficient:continue
        shape=(a,b) if b else ((a,) if a else ())
        polynomial=_two_variable_hl(shape,Q)
        for i,x in enumerate(polynomial):residual[i]-=coefficient*x
        number=coefficient*Fraction(Q)**(b-na-nb)
        if number.denominator!=1 or number<0:raise AssertionError('invalid two-row Hall coefficient')
        if number:result.append((shape,number.numerator))
    if any(residual):raise AssertionError('two-variable Hall decomposition failed')
    return tuple(result)


@lru_cache(None)
def two_row_hall_pairs(rows,Q):
    """Submodule/quotient pairs of a <=2-row primary module, polynomial list."""
    if not rows or len(rows)>2 or any(type(x) is not int or x<1 for x in rows) or tuple(sorted(rows,reverse=True))!=rows:
        raise ValueError('one or two positive decreasing block lengths required')
    n=sum(rows);out=[]
    for k in range(n+1):
        for b in range(k//2+1):
            a=k-b
            if a>rows[0] or b>(rows[1] if len(rows)>1 else 0):continue
            alpha=(a,b) if b else ((a,) if a else ())
            for d in range((n-k)//2+1):
                c=n-k-d
                if c>rows[0] or d>(rows[1] if len(rows)>1 else 0):continue
                beta=(c,d) if d else ((c,) if c else ())
                number=dict(two_variable_hall(alpha,beta,Q)).get(rows,0)
                if number:out.append((alpha,beta,number))
    return tuple(out)


def two_row_primary_gap(rows,field_h,irreducible,beta,phi,eta=0):
    """Uniform polynomial exact counter for any one- or two-block primary."""
    begun=time.perf_counter();rows=tuple(rows);F=Field(field_h);q=F.q;f=list(irreducible);d=len(f)-1;phi=set(phi)
    if not rows or len(rows)>2 or any(type(x) is not int or x<1 for x in rows) or tuple(sorted(rows,reverse=True))!=rows:
        raise ValueError('one or two positive decreasing block lengths required')
    if d<1 or f[-1]!=1 or any(type(c) is not int or not 0<=c<q for c in f) or factor_polynomial(f,F)!=[(f,1)]:
        raise ValueError('a canonical monic irreducible polynomial is required')
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('field coefficients and a Boolean quadratic trace source required')
    n=sum(rows);t=d*n;Q=q**d;weights,kernel=two_cyclic_weights(t,d,q,refined=bool(eta))
    powers=[[1]]
    for _ in range(rows[0]):powers.append(polynomial_product(powers[-1],f,F))
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));answer=0;terms=[];gaussians={};flags={}
    for alpha,residual,number in two_row_hall_pairs(rows,Q):
        if alpha not in flags:
            A=alpha[0] if alpha else 0;B=alpha[1] if len(alpha)>1 else 0
            row=[Q**B*x for x in weights[A,B]]
            for k in range(1,B+1):
                coefficient=Q**(B-k)-Q**(B-k+1)
                for r in range(4):row[r]+=coefficient*weights[A+k,B-k][r]
            flags[alpha]=row
        row=flags[alpha];c=d*sum(alpha);b=t-c
        if residual not in gaussians:
            D=_quotient_matrix(powers,residual[0] if residual else 0,residual[1] if len(residual)>1 else 0);G=[]
            for parity in range(2 if eta else 1):
                shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,beta)
                G.append(quadratic_anf_sum(matrix_source_anf(D,F,beta,shifted,eta),F.a*b*b))
            gaussians[residual]=G
        G=gaussians[residual]
        value=sum(row[r]*(-1 if phase*(r*(r-1)//2)%2 else 1)*G[r%len(G)] for r in range(4))
        contribution=number*q**(c*(c-1)//2+c*b)*value;answer+=contribution
        terms.append(dict(controlled_type=alpha,quotient_type=residual,submodule_multiplicity=number,
            controlled_dimension=c,profile_weights=row,residual_gaussians=G,contribution=contribution))
    gap=q**(t*t)*answer
    return gap,dict(route='at most two primary blocks, two-variable Hall and two-alphabet Pfaffian',
        original_bits=3*F.a*t*t,matrix_size=t,field_modulus=field_h,
        primary_degree=d,block_lengths=rows,irreducible=f,beta=beta,eta=eta,phi=sorted(phi),
        terms=terms,profile_backend=kernel,residual_gaussian_types=len(gaussians),
        uniform_polynomial_time=True,enumerated_profiles=0,enumerated_subspaces=0,
        enumerated_field_elements=0,enumerated_original_assignments=0,
        seconds=time.perf_counter()-begun)


def count_acquired_two_row_primary(algebra,beta,D,phi,eta=0):
    polynomial,primary=algebra.primary_data(D)
    if len(primary)!=1 or not primary[0]['jordan_columns'] or primary[0]['jordan_columns'][0]>2:
        raise ValueError('the operator is not one primary with at most two blocks')
    item=primary[0];columns=item['jordan_columns']
    rows=tuple(sum(c>j for c in columns) for j in range(columns[0]))
    gap,meta=two_row_primary_gap(rows,algebra.h,item['irreducible'],beta,phi,eta)
    meta.update(acquired_reduced_charpoly=polynomial,acquired_primary_data=primary,
        supplied_primary_decomposition=False,supplied_matrix_units=False)
    return gap,meta
