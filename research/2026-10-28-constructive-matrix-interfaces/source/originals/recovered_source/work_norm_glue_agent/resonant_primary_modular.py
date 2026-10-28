#!/usr/bin/env python3
"""All-shape resonant primary counts modulo the manufactured M_J.

A fixed-depth skew Hall--Littlewood transfer sums quotient types without
listing them. The structured trace program is used only at zero and eta.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_norm_glue_agent','work_norm_frontier_agent',
    'work_norm_slice_agent','work_matrix_root')]
from resonant_primary_gaussian import ResonantPrimaryGaussian
from nonresonant_primary_gaussian import value
from nonresonant_primary_modular import BoundedRowProfile
from arbitrary_operator_hall import transpose_partition,n_stat
from matrix_kloosterman import Field,charpoly,factor_polynomial,primary_columns


def skew_quotient_sum(shape,variables,Q):
    """All rho sum Q_(shape/rho)(Y;1/Q), as ordinary monomials.

    Each column has variables binary strip drops. Adjacent columns give
    every interlacing constraint and one-variable Q branching factor.
    """
    shape=tuple(shape);heights=transpose_partition(shape)+(0,);J=variables
    tau=Fraction(1,Q);states=list(product((0,1),repeat=J));zero=(0,)*J
    prefixes={s:tuple(sum(s[:i]) for i in range(J+1)) for s in states}
    allowed=lambda h:[s for s in states if sum(s)<=h]
    dynamic={s:{s:Fraction(1)} for s in allowed(heights[0])}
    max_terms=sum(len(x) for x in dynamic.values());transitions=0
    for column in range(len(heights)-1):
        h,hn=heights[column:column+2];next_states=allowed(hn);new={}
        for current,polynomial in dynamic.items():
            left=prefixes[current]
            for following in next_states:
                right=prefixes[following]
                if any(h-left[k]<hn-right[k] for k in range(J+1)):continue
                factor=Fraction(1)
                for k in range(J):
                    if current[k] and not following[k]:
                        multiplicity=(h-left[k])-(hn-right[k])
                        factor*=1-tau**multiplicity
                if not factor:continue
                transitions+=1;target=new.setdefault(following,{})
                for exponent,c in polynomial.items():
                    e=tuple(a+b for a,b in zip(exponent,following))
                    target[e]=target.get(e,Fraction(0))+factor*c
        dynamic=new;max_terms=max(max_terms,sum(len(x) for x in dynamic.values()))
    polynomial=dynamic.get(zero,{})
    for exponent,c in polynomial.items():
        if polynomial.get(tuple(sorted(exponent,reverse=True)))!=c:
            raise AssertionError('horizontal-strip sum is not symmetric')
    canonical={tuple(x for x in exponent if x):c for exponent,c in polynomial.items()
        if exponent==tuple(sorted(exponent,reverse=True))}
    return canonical,dict(local_column_states=len(states),largest_transfer_terms=max_terms,
        realized_column_transitions=transitions,ordinary_monomials=len(polynomial),
        symmetric_monomials=len(canonical),enumerated_quotient_partitions=False)


def count_resonant_primary_modulo(shape,field_h,irreducible,beta,phi=(),eta=0,
                                 row_budget=2,trace_program=None):
    begun=time.perf_counter();shape=tuple(shape);phi=set(phi)
    if not shape or any(type(x) is not int or x<=0 for x in shape) or tuple(sorted(shape,reverse=True))!=shape:
        raise ValueError('positive explicit primary block lengths required')
    E=ResonantPrimaryGaussian(field_h,irreducible,beta,eta);F=E.F
    q=F.q;d=E.d;m=sum(shape);t=d*m;J=row_budget
    if type(J) is not int or not 0<=J<t:raise ValueError('0<=J<t required')
    if any(type(x) is not int or x<0 or x.bit_length()>F.a for x in phi):
        raise ValueError('trace ANF outside the field coordinates')
    evaluate=(lambda x:value(phi,x)) if trace_program is None else trace_program
    observations={x:evaluate(x) for x in sorted({0,eta})}
    if any(x not in (0,1) for x in observations.values()):raise ValueError('trace program must return a Boolean bit')
    M=1
    for i in range(J+1):M*=q**(t-i)-1
    profile=BoundedRowProfile(q,t,J,M);Q=q**d
    polynomial,transfer=skew_quotient_sum(shape,J,Q)
    scale=Q**(n_stat(shape)+m);boundaries={}
    for mu,c in polynomial.items():
        size=sum(mu);degree=d*size;profile.acquire_degree(degree)
        row=profile.moments[degree][tuple(d*x for x in mu)]
        target=boundaries.setdefault(size,[Fraction(0)]*(J+1))
        for odd,x in enumerate(row):target[odd]+=scale*c*x
    normalized=0;phase=F.trace(F.mul(beta,F.mul(eta,eta)))
    for size,row in boundaries.items():
        remaining=m-size;support=E.trace_support(remaining);base=E.periodic_sign(remaining)
        for odd,c in enumerate(row):
            if c.denominator!=1:raise AssertionError('resonant truncated kernel did not return integers')
            if not c:continue
            degree=d*size
            if (degree-odd)%2:raise AssertionError('boundary parity mismatch')
            h=(degree-odd)//2%4;delta=eta if h%2 else 0
            point=support^delta
            if point not in observations:raise AssertionError('resonant trace escaped the two-point support')
            sign=base*(1-2*observations[point])
            if F.trace(F.mul(F.mul(beta,delta),support)):sign=-sign
            if phase*(h*(h-1)//2)%2:sign=-sign
            normalized=(normalized+c.numerator*sign)%M
    K=t*t+t*(t-1)//2;N=3*F.a*t*t;gap=pow(q,K,M)*normalized%M
    ones=(pow(2,N,M)-gap)*pow(2,-1,M)%M
    return dict(modulus=M,normalized_gap_residue=normalized,gap_residue=gap,
        satisfying_inputs_residue=ones,original_bits=N,matrix_size=t,field_degree=F.a,
        residue_degree=d,primary_shape=shape,row_budget=J,supplied_primary_decomposition=True,
        known_satisfying_count_divisor_power_of_two=F.a*K-1,
        scaled_satisfying_inputs_residue=(pow(2,N-F.a*K,M)-normalized)%M,
        trace_program_values=observations,
        stats=dict(**transfer,trace_program_evaluations=len(observations),
            maximum_controlled_primary_size=sum(shape[:J]),
            total_finite_variable_states=profile.total_states,
            maximum_profile_moment_rational_bits=profile.maximum_rational_bits,
            modulus_bits=M.bit_length(),exact_count_reconstructed=False,
            bit_time_bound='(a+1)^{O(1)} (t+1)^{O((J+1)^2)} for fixed J, plus two trace-program evaluations',
            uniform_polynomial_in_J=False,prime_or_order_search=False,
            field_elements_enumerated=0,seconds=time.perf_counter()-begun))


def count_literal_resonant_modulo(D,field_h,beta,phi=(),eta=0,row_budget=2,trace_program=None):
    begun=time.perf_counter();F=Field(field_h);D=[list(row) for row in D];t=len(D)
    if not t or any(len(row)!=t for row in D) or any(type(x) is not int or not 0<=x<F.q for row in D for x in row):
        raise ValueError('nonempty square operator over the supplied field required')
    polynomial=charpoly(D,F);factors=factor_polynomial(polynomial,F)
    if len(factors)!=1:raise ValueError('a single primary operator is required')
    f,m=factors[0];cols=primary_columns(D,f,m,F);acquisition=time.perf_counter()-begun
    result=count_resonant_primary_modulo(transpose_partition(cols),field_h,f,beta,phi,eta,row_budget,trace_program)
    result.update(supplied_primary_decomposition=False,acquired_characteristic_polynomial=polynomial,
        acquired_irreducible=f,acquired_primary_columns=cols,input_operator_bits=F.a*t*t)
    result['stats'].update(primary_acquisition_seconds=acquisition,total_seconds=time.perf_counter()-begun)
    return result
