#!/usr/bin/env python3
"""Absorb a quadratic trace observable before taking the trace-algebra quotient.

For all-even acquired primary degrees, use F_x=(-1)^(p(x)+p(0))*E_x.
The resulting cocycle is C=B+polar(p), and only its observable radical
is retained: K=rad(C|R) intersect ker(C(eta, .)).
"""
from pathlib import Path
from fractions import Fraction
import itertools,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_multiprimary_audit','work_matrix_root',
    'work_norm_frontier_agent','work_norm_slice_agent','work_partition_free_agent')]
from nonzero_beta_trace_algebra import (Field,charpoly,factor_polynomial,primary_columns,
    transpose_partition,binary_span,resonance_orbits,add_scaled,hall_pairs,
    quotient_matrix,invariant_flag_power,power_multiply,matrix_source_anf,
    quadratic_anf_sum,RefinedProfileFunctional)
from matrix_kloosterman import kernel

def boolean_value(phi,x):return sum((x&m)==m for m in phi)%2

def remainder(value,basis):
    for vector in basis:
        if value>>(vector.bit_length()-1)&1:value^=vector
    return value

def span_vector(basis,coordinates):
    value=0
    for x,bit in zip(basis,coordinates):
        if bit:value^=x
    return value

def acquire_gauged_trace_quotient(primary,F,beta,eta,phi):
    if any(item['degree']%2 for item in primary):
        raise ValueError('gauged point quotient requires even acquired primary degrees')
    p0=boolean_value(phi,0);invbeta=F.inv(beta)
    generators=[F.mul(invbeta,F.pow(item['trace_coefficient']^
        (beta if item['degree']//2%2 else 0),F.q//2)^F.mul(eta,item['trace_coefficient']))
        for item in primary]
    R=binary_span(generators);r=len(R)
    B=lambda x,y:F.trace(F.mul(beta,F.mul(x,y)))
    P=lambda x,y:boolean_value(phi,x^y)^boolean_value(phi,x)^boolean_value(phi,y)^p0
    C=lambda x,y:B(x,y)^P(x,y)
    matrix=[[C(x,y) for x in R] for y in R]
    quadratic_rank=r-len(kernel(matrix,Field(3),r))
    matrix.append([C(x,eta) for x in R])
    K=binary_span([span_vector(R,z) for z in kernel(matrix,Field(3),r)])
    if any(C(k,x) for k in K for x in R+[eta]):
        raise AssertionError('gauged observable radical certificate failed')
    return dict(point_generators=generators,point_span_basis=R,point_span_rank=r,
        gauged_pairing_rank=quadratic_rank,kernel_basis=K,kernel_dimension=len(K),
        effective_trace_rank=r-len(K),quotient_dimension_bound=1<<(r-len(K)),
        quadratic_gauge_applied=True,source_constant=p0),C

def count_quadratic_gauged_trace(D,field_h,beta,phi=(),eta=0,
                                 maximum_effective_rank=None,profile_backend='shared_modes'):
    started=time.perf_counter();F=Field(field_h);q=F.q;t=len(D);phi=set(phi)
    if not t or any(len(row)!=t or any(type(x)is not int or not 0<=x<q for x in row) for row in D):
        raise ValueError('literal nonempty square matrix required')
    if not 0<beta<q or not 0<=eta<q:raise ValueError('field beta must be nonzero; eta must be a field element')
    if any(type(m)is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('explicit Boolean quadratic required')
    if profile_backend not in ('shared_modes','partition'):raise ValueError('unknown profile backend')
    characteristic=charpoly(D,F);primary=[]
    for f,m in factor_polynomial(characteristic,F):
        columns=primary_columns(D,f,m,F)
        primary.append(dict(irreducible=f,degree=len(f)-1,multiplicity=m,
            trace_coefficient=f[-2],jordan_columns=columns,rows=transpose_partition(tuple(columns))))
    quotient,C=acquire_gauged_trace_quotient(primary,F,beta,eta,phi)
    if maximum_effective_rank is not None and quotient['effective_trace_rank']>maximum_effective_rank:
        raise ValueError('acquired gauged quotient exceeds the effective-rank budget')
    K=quotient['kernel_basis'];p0=quotient['source_constant'];orbits=resonance_orbits(primary,beta,F)
    combined={0:{():Fraction(1)}};records=[];calls=0;invbeta=F.inv(beta)
    for orbit in orbits:
        options=[hall_pairs(primary[i]['rows'],q**primary[i]['degree']) for i in orbit]
        local={};cache={}
        for selected in itertools.product(*options):
            rho=tuple(item[1] for item in selected)
            if rho not in cache:
                A=quotient_matrix([primary[i] for i in orbit],rho,F);b=len(A);tau=0
                if b%2:raise AssertionError('odd quotient in even-degree source')
                for j,row in enumerate(A):tau^=row[j]
                actual=F.mul(invbeta,F.pow(tau^(beta if b//2%2 else 0),q//2)^F.mul(eta,tau))
                if remainder(actual,quotient['point_span_basis']):raise AssertionError('local point escaped acquired span')
                G=quadratic_anf_sum(matrix_source_anf(A,F,beta,(),eta),F.a*b*b);calls+=1
                gauge=1-2*(boolean_value(phi,actual)^p0)
                cache[rho]=(remainder(actual,K),Fraction(gauge*G,q**(b*(b-1)//2)))
            x,amplitude=cache[rho]
            if not amplitude:continue
            polynomial={():Fraction(1)};population=1
            for i,(alpha,residual,number) in zip(orbit,selected):
                polynomial=power_multiply(polynomial,dict(invariant_flag_power(alpha,q**primary[i]['degree'],primary[i]['degree'])))
                population*=number
            local[x]=add_scaled(local.get(x,{}),polynomial,population*amplitude)
        output={}
        for x,alpha in combined.items():
            for y,rho in local.items():
                target=remainder(x^y,K);sign=1-2*C(x,y)
                output[target]=add_scaled(output.get(target,{}),power_multiply(alpha,rho),sign)
        combined={x:poly for x,poly in output.items() if poly}
        records.append(dict(primary_indices=orbit,quotient_gaussians=len(cache),
            quotient_symbols=len(combined),power_coordinates=sum(map(len,combined.values()))))
    modes=tuple(sorted({item['degree']*j for item in primary for j in range(1,item['multiplicity']+1)}))
    if profile_backend=='shared_modes':
        from bounded_mode_beta_zero_counter import PowerModeProfileFunctional
        functional=PowerModeProfileFunctional(q,t,modes);evaluate=functional.evaluate_rational;metadata=functional.metadata
    else:
        functional=RefinedProfileFunctional(q,t);metadata=None
        evaluate=lambda poly:[sum((c*functional.power[rho][h] for rho,c in poly.items()),Fraction(0)) for h in range(4)]
    total=Fraction(0);outer=F.trace(F.mul(beta,F.mul(eta,eta)));profile_vectors=[]
    for x,polynomial in combined.items():
        weights=evaluate(polynomial)
        profile_vectors.append(dict(index=x,weights=[[w.numerator,w.denominator] for w in weights]))
        for h,weight in enumerate(weights):
            delta=eta if h%2 else 0
            phase=boolean_value(phi,delta)^C(x,delta)^(outer*(h*(h-1)//2)%2)
            total+=weight*(1-2*phase)
    total*=q**(t*t+t*(t-1)//2);n=3*F.a*t*t
    if total.denominator!=1 or abs(total)>1<<n or total.numerator%2:
        raise AssertionError('invalid full original-domain count')
    gap=total.numerator
    return dict(original_independent_bits=n,gap=gap,ones=((1<<n)-gap)//2,
        source_operator=D,field_polynomial=field_h,beta=beta,eta=eta,trace_quadratic_anf=sorted(phi),
        acquired_characteristic=characteristic,acquired_primary=primary,
        acquired_gauged_quotient=quotient,resonance_orbits=orbits,orbit_records=records,
        final_quotient_symbols=len(combined),local_gaussian_calls=calls,
        acquired_power_modes=modes,profile_backend=profile_backend,profile_kernel=metadata,
        profile_vectors=profile_vectors,full_original_domain=True,
        computed_full_trace_histogram=False,quotient_depends_on_requested_quadratic=True,
        enumerated_field_elements=0,auxiliary_independent_inputs=0,
        bit_time_bound='2^O(rho)*poly(a,t,M)',seconds=time.perf_counter()-started)

if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--partition-reference',action='store_true')
    args=parser.parse_args();source=json.loads(args.source.read_text())
    result=count_quadratic_gauged_trace(source['D'],source['h'],source['beta'],source.get('phi',()),source.get('eta',0),
        profile_backend='partition' if args.partition_reference else 'shared_modes')
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')
