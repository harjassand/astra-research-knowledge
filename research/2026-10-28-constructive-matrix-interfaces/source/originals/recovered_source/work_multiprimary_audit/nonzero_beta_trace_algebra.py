#!/usr/bin/env python3
"""Nonzero-beta resonance-orbit Hall aggregation.

Time 2^O(r+sqrt(t))*poly(a,t), with a manufactured binary trace-index
span of rank r. No Cartesian product over all primary types is listed.
"""
from pathlib import Path
from fractions import Fraction
import itertools,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent','work_norm_slice_agent',
                                 'work_partition_free_agent')]
from matrix_kloosterman import Field,charpoly,factor_polynomial,primary_columns
from arbitrary_operator_hall import (RefinedProfileFunctional,power_multiply,
    quotient_matrix,hall_pairs,invariant_flag_power,transpose_partition)
from simple_operator_quadratic import matrix_source_anf
from krylov_square_source import quadratic_anf_sum

def add_scaled(out,poly,scale):
    for rho,value in poly.items():out[rho]=out.get(rho,Fraction(0))+scale*value
    return {rho:value for rho,value in out.items() if value}

def field_character_mask(F,gamma):
    return sum(F.trace(F.mul(gamma,1<<j))<<j for j in range(F.a))

def linear_anf(mask):return {1<<j for j in range(mask.bit_length()) if mask>>j&1}

def shift_polynomial(f,beta,F):
    out=[0]*len(f);powers=[1]
    for _ in range(len(f)-1):powers.append(F.mul(powers[-1],beta))
    for j,c in enumerate(f):
        for k in range(j+1):
            if not k&~j:out[k]^=F.mul(c,powers[j-k])
    return out

def resonance_orbits(primary,beta,F):
    lookup={tuple(item['irreducible']):i for i,item in enumerate(primary)}
    used=set();orbits=[]
    for i,item in enumerate(primary):
        if i in used:continue
        shifted=shift_polynomial(item['irreducible'],beta,F)
        assert shift_polynomial(shifted,beta,F)==item['irreducible']
        j=lookup.get(tuple(shifted));orbit=(i,) if j is None or j==i else (i,j)
        if any(k in used for k in orbit):raise AssertionError('translation orbit overlap')
        used.update(orbit);orbits.append(orbit)
    return orbits

def binary_span(vectors):
    pivots={}
    for value in vectors:
        x=value
        while x:
            j=x.bit_length()-1
            if j not in pivots:pivots[j]=x;break
            x^=pivots[j]
    return [pivots[j] for j in sorted(pivots,reverse=True)]

def in_span(x,basis):
    for value in basis:
        if x>>(value.bit_length()-1)&1:x^=value
    return x==0

def trace_symbol_product(left,right,F,beta,u):
    """E_x is a point mass; O_x(s)=(-1)^Tr(beta*x*s)."""
    p,x=left;r,y=right
    if not p and not r:
        target=(0,x^y);scalar=1;phase=F.trace(F.mul(beta,F.mul(x,y)))
    elif p and r:
        z=x^y^u;target=(0,z);scalar=F.q
        phase=F.trace(F.mul(beta,F.mul(y,z)))
    else:
        point,char=(x,y) if not p else (y,x)
        target=(1,x^y);scalar=1
        phase=F.trace(F.mul(beta,F.mul(point,point^char)))
    return target,scalar*(1-2*phase)

def multiply_trace_polynomials(A,B,F,beta,u):
    out={}
    for left,alpha in A.items():
        for right,rho in B.items():
            target,scale=trace_symbol_product(left,right,F,beta,u)
            out[target]=add_scaled(out.get(target,{}),power_multiply(alpha,rho),scale)
    return {key:poly for key,poly in out.items() if poly}

def compile_nonzero_beta_trace_response(D,field_h,beta,eta=0,maximum_trace_rank=None,profile_backend='partition'):
    begun=time.perf_counter();F=Field(field_h);q=F.q;t=len(D)
    if not t or any(len(row)!=t or any(type(v)is not int or not 0<=v<q for v in row) for row in D):
        raise ValueError('literal nonempty square matrix required')
    if not 0<beta<q or not 0<=eta<q:raise ValueError('nonzero field beta and field eta required')
    if profile_backend not in ('partition','shared_modes'):raise ValueError('unknown exact profile backend')
    characteristic=charpoly(D,F);primary=[]
    for f,m in factor_polynomial(characteristic,F):
        columns=primary_columns(D,f,m,F)
        primary.append(dict(irreducible=f,jordan_columns=columns,
            rows=transpose_partition(tuple(columns)),degree=len(f)-1,multiplicity=m,
            trace_coefficient=f[-2]))
    invbeta=F.inv(beta);u=F.pow(invbeta,q//2)
    generators=[u]+[F.mul(invbeta,F.pow(item['trace_coefficient'],q//2)^
        F.mul(eta,item['trace_coefficient'])) for item in primary]
    basis=binary_span(generators);rank=len(basis)
    if maximum_trace_rank is not None and rank>maximum_trace_rank:
        raise ValueError('acquired trace-index rank exceeds the specified family budget')
    orbits=resonance_orbits(primary,beta,F);combined={(0,0):{():Fraction(1)}}
    orbit_records=[];local_gaussian_calls=0
    for orbit in orbits:
        options=[hall_pairs(primary[i]['rows'],q**primary[i]['degree']) for i in orbit]
        cache={};local={};leaves=0
        for selected in itertools.product(*options):
            leaves+=1;rho=tuple(item[1] for item in selected)
            if rho not in cache:
                residual=quotient_matrix([primary[i] for i in orbit],rho,F);b=len(residual)
                tau=0
                for j,row in enumerate(residual):tau^=row[j]
                x=F.mul(invbeta,F.pow(tau^(beta if b*(b-1)//2%2 else 0),q//2)^F.mul(eta,tau))
                if not in_span(x,basis):raise AssertionError('local trace index escaped manufactured span')
                phase=linear_anf(field_character_mask(F,F.mul(beta,x))) if b%2 else ()
                G=quadratic_anf_sum(matrix_source_anf(residual,F,beta,phase,eta),F.a*b*b)
                denominator=q**(b*(b-1)//2+b%2)
                cache[rho]=((b%2,x),Fraction(G,denominator));local_gaussian_calls+=1
            symbol,amplitude=cache[rho]
            if not amplitude:continue
            flag={():Fraction(1)};population=1
            for i,(alpha,residual,number) in zip(orbit,selected):
                flag=power_multiply(flag,dict(invariant_flag_power(alpha,q**primary[i]['degree'],primary[i]['degree'])))
                population*=number
            local[symbol]=add_scaled(local.get(symbol,{}),flag,population*amplitude)
        combined=multiply_trace_polynomials(combined,local,F,beta,u)
        orbit_records.append(dict(primary_indices=orbit,local_Hall_leaves=leaves,
            quotient_Gaussians=len(cache),local_trace_symbols=len(local),
            accumulated_trace_symbols=len(combined),
            accumulated_power_coordinates=sum(map(len,combined.values()))))
    modes=tuple(sorted({item['degree']*j for item in primary for j in range(1,item['multiplicity']+1)}))
    if profile_backend=='partition':
        functional=RefinedProfileFunctional(q,t);profile_kernel=None
        partition_states=len(functional.power)
        evaluate_profile=lambda poly:[sum((value*functional.power[rho][h] for rho,value in poly.items()),Fraction(0)) for h in range(4)]
    else:
        from bounded_mode_beta_zero_counter import PowerModeProfileFunctional
        functional=PowerModeProfileFunctional(q,t,modes);profile_kernel=functional.metadata
        partition_states=0;evaluate_profile=functional.evaluate_rational
    scale=q**(t*t+t*(t-1)//2)
    phase_eta=F.trace(F.mul(beta,F.mul(eta,eta)));points={};walsh={};profiles=[]
    for (parity,x),poly in combined.items():
        weights=evaluate_profile(poly)
        profiles.append(dict(kind='character' if parity else 'point',index=x,
            profile_weights=[[v.numerator,v.denominator] for v in weights]))
        for h,weight in enumerate(weights):
            delta=eta if h%2 else 0;outer=phase_eta*(h*(h-1)//2)%2
            if not parity:
                target=x^delta;phase=outer^F.trace(F.mul(beta,F.mul(delta,x)))
                points[target]=points.get(target,Fraction(0))+scale*weight*(1-2*phase)
            else:
                gamma=F.mul(beta,x^delta);target=field_character_mask(F,gamma)
                phase=outer^F.trace(F.mul(gamma,delta))
                walsh[target]=walsh.get(target,Fraction(0))+scale*weight*(1-2*phase)
    response=[]
    for kind,data in [('point',points),('walsh',walsh)]:
        for argument,value in sorted(data.items()):
            if not value:continue
            if value.denominator!=1:raise AssertionError('full response coefficient is not integral')
            response.append(dict(kind=kind,argument=argument,coefficient=value.numerator))
    all_even=all(item['degree']%2==0 for item in primary)
    if all_even and any(item['kind']=='walsh' for item in response):raise AssertionError('even-degree source produced a character')
    return dict(field_polynomial=field_h,field_degree=F.a,matrix_size=t,beta=beta,eta=eta,
        original_independent_bits=3*F.a*t*t,counted_domain_size=q**(3*t*t),
        full_matrix_domain=True,rank_cap=t,padding=t,response=response,
        acquired_characteristic=characteristic,acquired_primary=primary,
        acquired_trace_index_generators=generators,acquired_trace_index_basis=basis,
        trace_index_rank=rank,trace_algebra_dimension_bound=2**(rank+1),
        scalar_translation=u,resonance_orbits=orbits,orbit_records=orbit_records,
        local_quotient_Gaussian_calls=local_gaussian_calls,final_trace_symbols=len(combined),
        profile_backend=profile_backend,explicit_partition_states=partition_states,
        acquired_power_modes=modes,power_mode_count=len(modes),profile_kernel=profile_kernel,
        enumerated_global_unrestricted_partitions=profile_backend=='partition',profile_vectors=profiles,
        remaining_walsh_terms=sum(x['kind']=='walsh' for x in response),
        manufactured_point_terms=sum(x['kind']=='point' for x in response),
        all_primary_degrees_even=all_even,source_primary_decomposition_supplied=False,
        cartesian_all_primary_type_enumeration=False,enumerated_field_elements=0,
        compiled_without_field_enumeration=True,trace_program_anf_expanded=False,
        auxiliary_independent_inputs=0,
        bit_time_bound=('2^O(r+sqrt(t))*poly(a,t), acquired trace-index rank r' if profile_backend=='partition'
            else '2^O(r)*poly(a,t,M), acquired trace rank r and weighted mode dimension M'),
        generic_polynomial_counter=False,seconds=time.perf_counter()-begun)

def nonzero_beta_quadratic_count(D,field_h,beta,phi=(),eta=0,maximum_trace_rank=None,profile_backend='partition'):
    F=Field(field_h);phi=set(phi)
    if any(type(v)is not int or v<0 or v.bit_length()>F.a or v.bit_count()>2 for v in phi):
        raise ValueError('explicit Boolean quadratic trace source required')
    response=compile_nonzero_beta_trace_response(D,field_h,beta,eta,maximum_trace_rank,profile_backend)
    gap=0
    for item in response['response']:
        if item['kind']=='point':value=1-2*(sum((item['argument']&m)==m for m in phi)%2)
        else:value=quadratic_anf_sum(phi^linear_anf(item['argument']),F.a)
        gap+=item['coefficient']*value
    domain=response['counted_domain_size']
    if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid full original-domain count')
    return dict(original_independent_bits=response['original_independent_bits'],gap=gap,
        ones=(domain-gap)//2,trace_quadratic_anf=sorted(phi),manufactured_response=response,
        full_original_domain=True)

def compile_bounded_mode_nonzero_beta_trace_response(D,field_h,beta,eta=0,maximum_trace_rank=None):
    return compile_nonzero_beta_trace_response(D,field_h,beta,eta,maximum_trace_rank,'shared_modes')

def bounded_mode_nonzero_beta_count(D,field_h,beta,phi=(),eta=0,maximum_trace_rank=None):
    return nonzero_beta_quadratic_count(D,field_h,beta,phi,eta,maximum_trace_rank,'shared_modes')

if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--response',action='store_true')
    parser.add_argument('--shared-modes',action='store_true')
    args=parser.parse_args();data=json.loads(args.source.read_text())
    backend='shared_modes' if args.shared_modes else 'partition'
    if args.response:result=compile_nonzero_beta_trace_response(data['D'],data['h'],data['beta'],data.get('eta',0),profile_backend=backend)
    else:result=nonzero_beta_quadratic_count(data['D'],data['h'],data['beta'],data.get('phi',()),data.get('eta',0),profile_backend=backend)
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')
