#!/usr/bin/env python3
"""Manufactured large-modulus exact counting for arbitrary nonresonant types.

For fixed J<t, return the original Boolean count modulo
M_J=prod_(i=0)^J(q^(t-i)-1).  There is no factoring/prime/order search and
no claim that the residue reconstructs the full count.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from collections import Counter
import sys,time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_norm_glue_agent','work_norm_frontier_agent',
    'work_norm_slice_agent','work_matrix_root')]
from nonresonant_primary_gaussian import NonresonantPrimaryGaussian
from arbitrary_operator_hall import hl_monomial_coefficient,n_stat,transpose_partition
from feedback_nilpotent_gaussians import shifted_trace_polynomial
from matrix_kloosterman import Field,charpoly,factor_polynomial,primary_columns


@lru_cache(None)
def bounded_partitions(n,rows,maximum=None):
    if n==0:return ((),)
    if rows==0:return ()
    maximum=n if maximum is None else min(n,maximum)
    result=[]
    for first in range(maximum,(n+rows-1)//rows-1,-1):
        result.extend((first,)+tail for tail in bounded_partitions(n-first,rows-1,first))
    return tuple(result)


def b_factor(shape,parameter):
    result=Fraction(1)
    for count in Counter(shape).values():
        for j in range(1,count+1):result*=1-parameter**j
    return result


@lru_cache(None)
def qbinom_mod(n,k,q,modulus):
    if k<0 or k>n:return 0
    k=min(k,n-k);row=[1]+[0]*k
    for i in range(1,n+1):
        for j in range(min(i,k),0,-1):
            row[j]=(row[j-1]+pow(q,j,modulus)*row[j])%modulus
    return row[k]%modulus


def submodule_number_mod(shape,subtype,Q,modulus):
    source=transpose_partition(shape);target=transpose_partition(subtype)+(0,)
    if len(target)-1>len(source):return 0
    result=1
    for j in range(len(target)-1):
        a,b=target[j],target[j+1]
        if a>source[j]:return 0
        result=result*pow(Q,b*(source[j]-a),modulus)%modulus
        result=result*qbinom_mod(source[j]-b,a-b,Q,modulus)%modulus
    return result%modulus


class BoundedRowProfile:
    """Finite-variable Hall-dual calculation with *exact* denominator clearing.

    No inverse modulo M is taken for the possibly nonunit factors q^j-1.
    Each rational calculation is completed over Q and checked integral
    coefficientwise before taking its residue. For fixed rows all tables
    have polynomial size; unbounded-partition tables are never built.
    """
    def __init__(self,q,ambient,rows,modulus):
        self.q=q;self.t=ambient;self.J=rows;self.M=modulus
        self.weights=[1]
        for j in range(rows):self.weights.append(self.weights[-1]*(1-q**(ambient-j)))
        self.moments={0:{():tuple([Fraction(1)]+[Fraction(0)]*rows)}}
        self.max_states=1;self.total_states=1;self.hl_coefficient_calls=0
        self.maximum_rational_bits=1

    def acquire_degree(self,degree):
        if degree in self.moments:return
        shapes=sorted(bounded_partitions(degree,self.J))
        values={}
        for shape in shapes:
            target=[Fraction(0)]*(self.J+1)
            odd=sum(x%2 for x in shape)
            target[odd]=Fraction(self.weights[len(shape)],b_factor(shape,Fraction(self.q)))
            for lower in shapes:
                if lower>=shape:break
                coefficient=hl_monomial_coefficient(shape,lower,Fraction(1,self.q))
                self.hl_coefficient_calls+=1
                if coefficient:
                    target=[x-coefficient*y for x,y in zip(target,values[lower])]
            for x in target:
                self.maximum_rational_bits=max(self.maximum_rational_bits,
                    x.numerator.bit_length(),x.denominator.bit_length())
            values[shape]=tuple(target)
        self.moments[degree]=values;self.total_states+=len(values)
        self.max_states=max(self.max_states,len(values))

    @lru_cache(None)
    def evaluate(self,shape,degree):
        shape=tuple(shape);m=sum(shape);c=degree*m
        if len(shape)>self.J:return (0,0,0,0)
        if c>self.t:raise ValueError('controlled dimension exceeds ambient size')
        self.acquire_degree(c)
        Q=self.q**degree
        factor=Fraction(Q)**(n_stat(shape)+m)*b_factor(shape,Fraction(1,Q))
        polynomial=[Fraction(0)]*(self.J+1)
        for mu in bounded_partitions(m,self.J):
            coefficient=hl_monomial_coefficient(shape,mu,Q)
            self.hl_coefficient_calls+=1
            if not coefficient:continue
            target=tuple(degree*x for x in mu)
            row=self.moments[c][target]
            polynomial=[x+factor*coefficient*y for x,y in zip(polynomial,row)]
        residues=[0]*4
        for odd,coefficient in enumerate(polynomial):
            if coefficient.denominator!=1:
                raise AssertionError('truncated integral symmetric-function kernel returned a fraction')
            if not coefficient:continue
            if (c-odd)%2:raise AssertionError('boundary parity mismatch')
            height=(c-odd)//2%4
            residues[height]=(residues[height]+coefficient.numerator)%self.M
        return tuple(residues)


def count_primary_modulo(shape,field_h,irreducible,beta,phi=(),eta=0,row_budget=2):
    begun=time.perf_counter();shape=tuple(shape);phi=set(phi)
    if not shape or any(type(x) is not int or x<=0 for x in shape) or tuple(sorted(shape,reverse=True))!=shape:
        raise ValueError('positive explicit primary block lengths required')
    E=NonresonantPrimaryGaussian(field_h,irreducible,beta,eta)
    F=E.F;q=F.q;d=E.d;m=sum(shape);t=d*m;J=row_budget
    if type(J) is not int or not 0<=J<t:raise ValueError('row budget must satisfy 0<=J<t')
    # Validate the trace ANF even if the manufactured modulus is trivial.
    E.gaussian(0,phi)
    modulus=1
    for i in range(J+1):modulus*=q**(t-i)-1
    profile=BoundedRowProfile(q,t,J,modulus)
    phase=F.trace(F.mul(beta,F.mul(eta,eta)))
    sources=[shifted_trace_polynomial(phi,F,eta if h%2 else 0,beta) for h in range(4)]
    residual_by_source={}
    for source in sources:
        key=frozenset(source)
        if key in residual_by_source:continue
        state=E.eight_state(source)
        initial=[x%modulus for x in state['initial']]
        multiplier=state['multiplier']%modulus
        values=[]
        for k in range(m+1):
            values.append(initial[k] if k<8 else values[k-8]*multiplier%modulus)
        residual_by_source[key]=values
    residual=[residual_by_source[frozenset(source)] for source in sources]
    Q=pow(q,d,modulus);normalized=0;types=0
    controlled_maximum=sum(shape[:J])
    for size in range(controlled_maximum+1):
        for alpha in bounded_partitions(size,J):
            if any(i>=len(shape) or x>shape[i] for i,x in enumerate(alpha)):continue
            multiplicity=submodule_number_mod(shape,alpha,Q,modulus)
            if not multiplicity:continue
            weights=profile.evaluate(alpha,d);types+=1
            normalized+=multiplicity*sum(weights[h]*residual[h][m-size]
                *(-1 if phase*(h*(h-1)//2)%2 else 1) for h in range(4))
            normalized%=modulus
    exponent=t*t+t*(t-1)//2
    gap=pow(q,exponent,modulus)*normalized%modulus
    N=3*F.a*t*t
    ones=(pow(2,N,modulus)-gap)*pow(2,-1,modulus)%modulus
    binary_divisor=F.a*exponent-1
    scaled_ones=(pow(2,N-F.a*exponent,modulus)-normalized)%modulus
    return dict(modulus=modulus,normalized_gap_residue=normalized,gap_residue=gap,
        satisfying_inputs_residue=ones,original_bits=N,matrix_size=t,
        known_satisfying_count_divisor_power_of_two=binary_divisor,
        scaled_satisfying_inputs_residue=scaled_ones,
        field_degree=F.a,residue_degree=d,primary_shape=shape,row_budget=J,
        supplied_primary_decomposition=True,
        stats=dict(controlled_types=types,total_finite_variable_states=profile.total_states,
            maximum_degree_states=profile.max_states,hl_coefficient_calls=profile.hl_coefficient_calls,
            maximum_profile_moment_rational_bits=profile.maximum_rational_bits,
            maximum_controlled_primary_size=controlled_maximum,
            distinct_quotient_response_sources=len(residual_by_source),
            manufactured_quotient_response_states=8*len(residual_by_source),
            modulus_bits=modulus.bit_length(),full_count_bits_upper_bound=N+1,
            normalized_gap_magnitude_bits_upper_bound=F.a*(3*t*t+t)//2+1,
            bit_time_bound='(a+1)^{O(1)} (t+1)^{O((J+1)^2)} for fixed J',
            uniform_polynomial_in_J=False,enumerated_full_partition_tables=False,
            prime_or_order_search=False,field_elements_enumerated=0,
            exact_count_reconstructed=False,seconds=time.perf_counter()-begun))


def count_literal_operator_modulo(D,field_h,beta,phi=(),eta=0,row_budget=2):
    begun=time.perf_counter()
    F=Field(field_h);D=[list(row) for row in D];t=len(D)
    if not t or any(len(row)!=t for row in D) or any(type(x) is not int or not 0<=x<F.q for row in D for x in row):
        raise ValueError('nonempty square matrix over the supplied field required')
    polynomial=charpoly(D,F);factors=factor_polynomial(polynomial,F)
    if len(factors)!=1:raise ValueError('a single primary operator is required')
    f,m=factors[0];cols=primary_columns(D,f,m,F)
    acquisition=time.perf_counter()-begun
    result=count_primary_modulo(transpose_partition(cols),field_h,f,beta,phi,eta,row_budget)
    result.update(supplied_primary_decomposition=False,
        acquired_characteristic_polynomial=polynomial,acquired_irreducible=f,
        acquired_primary_columns=cols,input_operator_field_elements=t*t,
        input_operator_bits=F.a*t*t)
    result['stats'].update(primary_acquisition_seconds=acquisition,
        total_seconds=time.perf_counter()-begun)
    return result


def count_acquired_operator_modulo(algebra,beta,D,phi=(),eta=0,row_budget=2):
    begun=time.perf_counter()
    polynomial,primary=algebra.primary_data(D)
    if len(primary)!=1:raise ValueError('a single primary operator is required')
    item=primary[0]
    acquisition=time.perf_counter()-begun
    result=count_primary_modulo(transpose_partition(item['jordan_columns']),algebra.h,
        item['irreducible'],beta,phi,eta,row_budget)
    result.update(supplied_primary_decomposition=False,
        acquired_characteristic_polynomial=polynomial,
        acquired_irreducible=item['irreducible'],acquired_primary_columns=item['jordan_columns'])
    result['stats'].update(primary_acquisition_seconds=acquisition,
        total_seconds=time.perf_counter()-begun)
    return result
