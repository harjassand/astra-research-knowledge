#!/usr/bin/env python3
"""Full E/O trace algebra after absorbing an explicit quadratic observable.

For every literal D, quotient R by R intersect rad(C on the whole field),
where C(x,y)=Tr(beta*x*y)+polar(p)(x,y). No even-degree condition.
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
    quadratic_anf_sum,RefinedProfileFunctional,field_character_mask,linear_anf)
from matrix_kloosterman import kernel
from quadratic_gauged_trace_counter import boolean_value,remainder,span_vector

def subtrace_value(F,x):
    total=second=0;current=x
    for _ in range(F.a):
        second^=F.mul(total,current);total^=current;current=F.mul(current,current)
    if second not in (0,1):raise AssertionError('absolute subtrace escaped F2')
    return second

def canonical_subtrace_anf(F,beta):
    root=F.pow(beta,F.q//2)
    ell=[F.trace(F.mul(root,1<<j)) for j in range(F.a)]
    result={1<<j for j in range(F.a) if subtrace_value(F,F.mul(root,1<<j))}
    for i in range(F.a):
        for j in range(i):
            if F.trace(F.mul(beta,F.mul(1<<i,1<<j)))^(ell[i]*ell[j]):
                result.add((1<<i)|(1<<j))
    return result

def acquire_full_gauged_quotient(primary,F,beta,eta,phi):
    invbeta=F.inv(beta);u=F.pow(invbeta,F.q//2);p0=boolean_value(phi,0)
    generators=[u]+[F.mul(invbeta,F.pow(item['trace_coefficient'],F.q//2)^
        F.mul(eta,item['trace_coefficient'])) for item in primary]
    R=binary_span(generators);r=len(R)
    B=lambda x,y:F.trace(F.mul(beta,F.mul(x,y)))
    P=lambda x,y:boolean_value(phi,x^y)^boolean_value(phi,x)^boolean_value(phi,y)^p0
    C=lambda x,y:B(x,y)^P(x,y)
    standard=[1<<j for j in range(F.a)];F2=Field(3)
    ambient=[[C(x,y) for x in standard] for y in standard]
    ambient_rank=F.a-len(kernel(ambient,F2,F.a))
    restrictions=[[C(x,y) for x in R] for y in standard]
    K=binary_span([span_vector(R,z) for z in kernel(restrictions,F2,r)])
    if any(C(k,x) for k in K for x in standard):
        raise AssertionError('ambient gauged radical certificate failed')
    if any(B(k,k) or P(k,u) for k in K):
        raise AssertionError('mixed E/O quotient descent certificate failed')
    rho=r-len(K)
    if rho>ambient_rank:raise AssertionError('restricted quotient rank exceeds ambient pairing rank')
    return dict(trace_generators=generators,trace_span_basis=R,trace_span_rank=r,
        ambient_gauged_pairing_rank=ambient_rank,kernel_basis=K,kernel_dimension=len(K),
        effective_trace_rank=rho,quotient_dimension_bound=1<<(rho+1),
        scalar_translation=u,source_constant=p0,full_EO_gauge=True),B,P,C

def gauged_symbol_product(left,right,F,beta,u,phi,p0,B,P,C):
    p,x=left;r,y=right;phase=C(x,y);scalar=1
    if p and r:
        target=(0,x^y^u);scalar=F.q
        phase^=boolean_value(phi,u)^p0^P(x^y,u)
    else:
        target=(p^r,x^y)
        if p^r:
            point=y if p else x;phase^=B(point,point)
    return target,scalar*(1-2*phase)

def count_full_gauged_trace(D,field_h,beta,phi=(),eta=0,
                            maximum_effective_rank=None,profile_backend='shared_modes'):
    started=time.perf_counter();F=Field(field_h);q=F.q;t=len(D);phi=set(phi)
    if not t or any(len(row)!=t or any(type(x)is not int or not 0<=x<q for x in row) for row in D):
        raise ValueError('literal nonempty square matrix required')
    if not 0<beta<q or not 0<=eta<q:raise ValueError('nonzero beta and field eta required')
    if any(type(m)is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('explicit Boolean quadratic required')
    if profile_backend not in ('partition','shared_modes','defect'):raise ValueError('unknown exact profile backend')
    characteristic=charpoly(D,F);primary=[]
    for f,m in factor_polynomial(characteristic,F):
        columns=primary_columns(D,f,m,F)
        primary.append(dict(irreducible=f,degree=len(f)-1,multiplicity=m,
            trace_coefficient=f[-2],jordan_columns=columns,rows=transpose_partition(tuple(columns))))
    quotient,B,P,C=acquire_full_gauged_quotient(primary,F,beta,eta,phi)
    if maximum_effective_rank is not None and quotient['effective_trace_rank']>maximum_effective_rank:
        raise ValueError('acquired full gauged quotient exceeds the effective-rank budget')
    K=quotient['kernel_basis'];u=quotient['scalar_translation'];p0=quotient['source_constant']
    invbeta=F.inv(beta);orbits=resonance_orbits(primary,beta,F)
    combined={(0,0):{():Fraction(1)}};records=[];calls=0
    for orbit in orbits:
        options=[hall_pairs(primary[i]['rows'],q**primary[i]['degree']) for i in orbit]
        local={};cache={}
        for selected in itertools.product(*options):
            rho=tuple(item[1] for item in selected)
            if rho not in cache:
                A=quotient_matrix([primary[i] for i in orbit],rho,F);b=len(A);tau=0
                for j,row in enumerate(A):tau^=row[j]
                actual=F.mul(invbeta,F.pow(tau^(beta if b*(b-1)//2%2 else 0),q//2)^F.mul(eta,tau))
                if remainder(actual,quotient['trace_span_basis']):raise AssertionError('quotient point escaped acquired trace span')
                linear=linear_anf(field_character_mask(F,F.mul(beta,actual))) if b%2 else ()
                G=quadratic_anf_sum(matrix_source_anf(A,F,beta,linear,eta),F.a*b*b);calls+=1
                gauge=1-2*(boolean_value(phi,actual)^p0)
                cache[rho]=((b%2,remainder(actual,K)),Fraction(gauge*G,q**(b*(b-1)//2+b%2)))
            symbol,amplitude=cache[rho]
            if not amplitude:continue
            polynomial={():Fraction(1)};population=1
            for i,(alpha,residual,number) in zip(orbit,selected):
                polynomial=power_multiply(polynomial,dict(invariant_flag_power(alpha,q**primary[i]['degree'],primary[i]['degree'])))
                population*=number
            local[symbol]=add_scaled(local.get(symbol,{}),polynomial,population*amplitude)
        output={}
        for left,alpha in combined.items():
            for right,rho in local.items():
                (parity,x),scale=gauged_symbol_product(left,right,F,beta,u,phi,p0,B,P,C)
                target=(parity,remainder(x,K))
                output[target]=add_scaled(output.get(target,{}),power_multiply(alpha,rho),scale)
        combined={s:poly for s,poly in output.items() if poly}
        records.append(dict(primary_indices=orbit,quotient_gaussians=len(cache),
            quotient_symbols=len(combined),power_coordinates=sum(map(len,combined.values()))))
    modes=tuple(sorted({item['degree']*j for item in primary for j in range(1,item['multiplicity']+1)}))
    if profile_backend in ('shared_modes','defect'):
        if profile_backend=='shared_modes':
            from bounded_mode_beta_zero_counter import PowerModeProfileFunctional
            functional=PowerModeProfileFunctional(q,t,modes)
        else:
            from multiplicity_defect_profile import DefectProfileFunctional
            functional=DefectProfileFunctional(q,t,primary)
        evaluate=functional.evaluate_rational;metadata=functional.metadata
    else:
        functional=RefinedProfileFunctional(q,t);metadata=None
        evaluate=lambda poly:[sum((c*functional.power[rho][h] for rho,c in poly.items()),Fraction(0)) for h in range(4)]
    total=Fraction(0);outer=B(eta,eta);profile_vectors=[];walsh_cache={}
    for (parity,x),polynomial in combined.items():
        weights=evaluate(polynomial)
        profile_vectors.append(dict(parity=parity,index=x,weights=[[w.numerator,w.denominator] for w in weights]))
        for h,weight in enumerate(weights):
            delta=eta if h%2 else 0;phase=outer*(h*(h-1)//2)%2
            if not parity:
                phase^=boolean_value(phi,delta)^C(x,delta);amplitude=1
            else:
                phase^=boolean_value(phi,x)^p0^B(x^delta,delta)
                mask=field_character_mask(F,F.mul(beta,x^delta))
                if mask not in walsh_cache:
                    walsh_cache[mask]=quadratic_anf_sum(phi^linear_anf(mask),F.a)
                amplitude=walsh_cache[mask]
            total+=weight*amplitude*(1-2*phase)
    total*=q**(t*t+t*(t-1)//2);n=3*F.a*t*t
    if total.denominator!=1 or abs(total)>1<<n or total.numerator%2:
        raise AssertionError('invalid full original-domain count')
    gap=total.numerator
    return dict(original_independent_bits=n,gap=gap,ones=((1<<n)-gap)//2,
        source_operator=D,field_polynomial=field_h,beta=beta,eta=eta,trace_quadratic_anf=sorted(phi),
        acquired_characteristic=characteristic,acquired_primary=primary,
        acquired_full_gauged_quotient=quotient,resonance_orbits=orbits,orbit_records=records,
        final_quotient_symbols=len(combined),local_gaussian_calls=calls,
        acquired_power_modes=modes,profile_backend=profile_backend,profile_kernel=metadata,
        profile_vectors=profile_vectors,walsh_evaluations=len(walsh_cache),
        full_original_domain=True,computed_full_trace_histogram=False,
        quotient_depends_on_requested_quadratic=True,enumerated_field_elements=0,
        auxiliary_independent_inputs=0,bit_time_bound='2^O(rho)*poly(a,t,M)',
        seconds=time.perf_counter()-started)

if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--partition-reference',action='store_true')
    group.add_argument('--defect',action='store_true')
    args=parser.parse_args();source=json.loads(args.source.read_text())
    result=count_full_gauged_trace(source['D'],source['h'],source['beta'],source.get('phi',()),source.get('eta',0),
        profile_backend='defect' if args.defect else 'partition' if args.partition_reference else 'shared_modes')
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')
