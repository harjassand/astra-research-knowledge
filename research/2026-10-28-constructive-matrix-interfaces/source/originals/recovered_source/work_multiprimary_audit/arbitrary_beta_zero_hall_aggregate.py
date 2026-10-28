#!/usr/bin/env python3
"""Full beta-zero counts for every literal source operator.

The local all-even Hall sums are multiplied in an explicit power-sum
partition basis, rather than enumerating Cartesian quotient type tuples.
Only zero, one or two low-degree active primary factors are exceptional.
The charged bound is exp(O(sqrt(t)))*poly(a,t), not polynomial generally.
"""
from pathlib import Path
from fractions import Fraction
import itertools,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent','work_norm_slice_agent')]
from matrix_kloosterman import Field,charpoly,factor_polynomial,primary_columns
from arbitrary_operator_hall import (RefinedProfileFunctional,power_multiply,
    quotient_matrix,hall_pairs,invariant_flag_power,n_stat,transpose_partition)
from simple_operator_quadratic import matrix_source_anf
from krylov_square_source import quadratic_anf_sum
from feedback_nilpotent_gaussians import shifted_trace_polynomial

def add_scaled(out,poly,scale):
    for rho,value in poly.items():out[rho]=out.get(rho,Fraction(0))+scale*value
    return {rho:value for rho,value in out.items() if value}

def parity_product(A,B):
    out=[{},{}]
    for i in range(2):
        for j in range(2):out[i^j]=add_scaled(out[i^j],power_multiply(A[i],B[j]),1)
    return out

def acquire_local_aggregates(D,field_h):
    F=Field(field_h);q=F.q;t=len(D)
    if not t or any(len(row)!=t or any(type(v)is not int or not 0<=v<q for v in row) for row in D):
        raise ValueError('literal nonempty square matrix required')
    characteristic=charpoly(D,F);primary=[];local=[]
    for f,m in factor_polynomial(characteristic,F):
        columns=primary_columns(D,f,m,F);rows=transpose_partition(tuple(columns));d=len(f)-1;Q=q**d
        item=dict(irreducible=f,jordan_columns=columns,rows=rows,degree=d,multiplicity=m)
        primary.append(item);even=[{},{}];odd=[];even_count=0;pairs=hall_pairs(rows,Q)
        for alpha,rho,number in pairs:
            flag=dict(invariant_flag_power(alpha,Q,d))
            if any(part%2 for part in rho):
                odd.append(dict(alpha=alpha,rho=rho,population=number,flag=flag))
            else:
                parity=(d*sum(rho)//2)%2
                even[parity]=add_scaled(even[parity],flag,number*Q**(sum(rho)+n_stat(rho)))
                even_count+=1
        local.append(dict(even=even,odd=odd,all_local_pairs=len(pairs),even_pairs=even_count))
    return F,primary,local,characteristic

def multiply_outside(local,exceptional):
    answer=[{():Fraction(1)},{}]
    for i,item in enumerate(local):
        if i not in exceptional:answer=parity_product(answer,item['even'])
    return answer

def even_only_trace_response(D,field_h,eta=0):
    """Arbitrary-program response when every acquired factor degree >=3."""
    begun=time.perf_counter();F,primary,local,characteristic=acquire_local_aggregates(D,field_h)
    if not 0<=eta<F.q:raise ValueError('field eta required')
    if any(item['degree']<3 for item in primary):
        raise ValueError('this two-point interface requires all factor degrees at least three')
    t=len(D);functional=RefinedProfileFunctional(F.q,t);combined=multiply_outside(local,())
    points={};scale=F.q**(t*t+t*(t-1)//2)
    for epsilon,poly in enumerate(combined):
        if not poly:continue
        weights=functional.evaluate(poly)
        for h,value in enumerate(weights):
            point=eta if (h+epsilon)%2 else 0
            points[point]=points.get(point,0)+scale*value
    points={s:value for s,value in points.items() if value}
    return dict(field_polynomial=field_h,field_degree=F.a,matrix_size=t,beta=0,eta=eta,
        rank_cap=t,padding=t,full_matrix_domain=True,
        original_independent_bits=3*F.a*t*t,counted_domain_size=F.q**(3*t*t),
        response=[dict(kind='point',argument=s,coefficient=value) for s,value in sorted(points.items())],
        remaining_walsh_terms=0,manufactured_point_terms=len(points),
        acquired_characteristic=characteristic,acquired_primary=primary,
        source_primary_decomposition_supplied=False,original_domain_preserved=True,
        auxiliary_independent_inputs=0,trace_program_anf_expanded=False,
        compiled_without_field_enumeration=True,
        explicit_partition_states=len(functional.power),
        bit_time_bound='exp(O(sqrt(t)))*poly(a,t), plus at most two program evaluations',
        seconds=time.perf_counter()-begun)

def arbitrary_beta_zero_count(D,field_h,phi=(),eta=0):
    begun=time.perf_counter();F,primary,local,characteristic=acquire_local_aggregates(D,field_h)
    q=F.q;t=len(D);phi=set(phi)
    if not 0<=eta<q or any(type(v)is not int or v<0 or v.bit_length()>F.a or v.bit_count()>2 for v in phi):
        raise ValueError('field eta and explicit Boolean quadratic trace source required')
    functional=RefinedProfileFunctional(q,t)
    eligible=[i for i,item in enumerate(primary) if item['degree']<=2]
    linear=[i for i,item in enumerate(primary) if item['degree']==1]
    exceptional_sets=[()]+[(i,) for i in eligible]+list(itertools.combinations(linear,2))
    answer=0;terms=[];gaussians={};outside_sizes=[]
    for exceptional in exceptional_sets:
        outside=multiply_outside(local,exceptional)
        outside_sizes.append(dict(exceptional_factors=exceptional,
            power_basis_states=[len(poly) for poly in outside]))
        for selected in itertools.product(*(local[i]['odd'] for i in exceptional)):
            flag={():Fraction(1)};population=1;rho=[]
            for item in selected:
                flag=power_multiply(flag,item['flag']);population*=item['population'];rho.append(item['rho'])
            key=(exceptional,tuple(rho))
            if key not in gaussians:
                residual=quotient_matrix([primary[i] for i in exceptional],rho,F);b=len(residual)
                denominator=q**(b*(b-1)//2);G=[]
                for parity in range(2 if eta else 1):
                    shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,0)
                    value=quadratic_anf_sum(matrix_source_anf(residual,F,0,shifted,eta),F.a*b*b)
                    G.append(Fraction(value,denominator))
                gaussians[key]=G
            G=gaussians[key];subtotal=0;vectors=[]
            for epsilon,poly in enumerate(outside):
                weights=functional.evaluate(power_multiply(poly,flag));vectors.append(weights)
                subtotal+=sum(weights[h]*G[(h+epsilon)%len(G)] for h in range(4))
            contribution=population*subtotal;answer+=contribution
            terms.append(dict(exceptional_factors=exceptional,
                exceptional_controlled_types=[item['alpha'] for item in selected],
                exceptional_quotient_types=rho,population=population,
                parity_profile_weights=vectors,
                normalized_quotient_gaussians=[[x.numerator,x.denominator] for x in G],
                contribution=[contribution.numerator,contribution.denominator]))
    gap=answer*q**(t*t+t*(t-1)//2);n=3*F.a*t*t
    if gap.denominator!=1:raise AssertionError('full gap is not integral')
    gap=gap.numerator
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    return dict(original_independent_bits=n,gap=gap,ones=((1<<n)-gap)//2,
        source_operator=D,field_polynomial=field_h,beta=0,eta=eta,trace_quadratic_anf=sorted(phi),
        acquired_characteristic=characteristic,acquired_primary=primary,
        supplied_primary_decomposition=False,full_original_domain=True,
        local_Hall_pair_counts=[item['all_local_pairs'] for item in local],
        local_all_even_pair_counts=[item['even_pairs'] for item in local],
        exceptional_factor_sets=len(exceptional_sets),exceptional_Hall_leaves=len(terms),
        exceptional_quotient_gaussians=len(gaussians),outside_aggregate_sizes=outside_sizes,
        explicit_partition_states=len(functional.power),terms=terms,
        general_Jordan_partitions_allowed=True,cartesian_all_primary_type_enumeration=False,
        enumerated_subspaces=0,enumerated_original_assignments=0,
        bit_time_bound='exp(O(sqrt(t)))*poly(a,t)',seconds=time.perf_counter()-begun)

if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--trace-response',action='store_true')
    args=parser.parse_args();data=json.loads(args.source.read_text())
    if args.trace_response:result=even_only_trace_response(data['D'],data['h'],data.get('eta',0))
    else:result=arbitrary_beta_zero_count(data['D'],data['h'],data.get('phi',()),data.get('eta',0))
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')
