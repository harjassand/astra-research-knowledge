#!/usr/bin/env python3
"""Full beta-zero counts for every acquired squarefree source operator.

No bound is imposed on the number or degrees of irreducible factors.
Time is polynomial in prod_d(m_d+1), hence exp(O(sqrt(t)))*poly(a,t).
For any fixed number of acquired distinct degrees it is polynomial.
"""
from pathlib import Path
from collections import Counter
import itertools,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent','work_norm_slice_agent')]
from matrix_kloosterman import Field,charpoly,factor_polynomial,companion
from mixed_cycle_kernel import mixed_cycle_profile_weights
from simple_operator_quadratic import matrix_source_anf
from krylov_square_source import quadratic_anf_sum
from feedback_nilpotent_gaussians import shifted_trace_polynomial


def mixed_degree_squarefree_count(D,field_h,phi=(),eta=0):
    begun=time.perf_counter();F=Field(field_h);q=F.q;t=len(D);phi=set(phi)
    if not t or any(len(row)!=t or any(type(v) is not int or not 0<=v<q for v in row) for row in D):
        raise ValueError('nonempty literal square matrix required')
    if not 0<=eta<q or any(type(v) is not int or v<0 or v.bit_length()>F.a or v.bit_count()>2 for v in phi):
        raise ValueError('field eta and explicit Boolean quadratic trace source required')
    characteristic=charpoly(D,F);factorization=factor_polynomial(characteristic,F)
    if any(m!=1 for f,m in factorization):raise ValueError('characteristic polynomial is not squarefree')
    factors=[f for f,m in factorization];degree_counts=Counter(len(f)-1 for f in factors)
    degrees=sorted(degree_counts);weights,kernel=mixed_cycle_profile_weights(t,q,degree_counts)
    eligible=[i for i,f in enumerate(factors) if len(f)<=3]
    selections=[()]+[(i,) for i in eligible]
    selections.extend(pair for pair in itertools.combinations(eligible,2)
        if sum(len(factors[i])-1 for i in pair)<=2)
    answer=0;terms=[];calls=0
    for selected in selections:
        b=sum(len(factors[i])-1 for i in selected);c=t-b
        state=list(degree_counts[d] for d in degrees)
        for i in selected:state[degrees.index(len(factors[i])-1)]-=1
        residual=[[0]*b for _ in range(b)];offset=0
        for i in selected:
            block=companion(factors[i]);size=len(block)
            for j,row in enumerate(block):residual[offset+j][offset:offset+size]=row
            offset+=size
        G=[]
        for parity in range(2 if eta else 1):
            shifted=shifted_trace_polynomial(phi,F,eta if parity else 0,0)
            G.append(quadratic_anf_sum(matrix_source_anf(residual,F,0,shifted,eta),F.a*b*b));calls+=1
        row=weights[tuple(state)]
        value=q**(c*(c-1)//2+c*b)*sum(row[h]*G[h%len(G)] for h in range(4))
        answer+=value
        terms.append(dict(quotient_factors=selected,quotient_dimension=b,
            controlled_degree_counts=state,profile_weights=row,quotient_gaussians=G,contribution=value))
    n=3*F.a*t*t;gap=q**(t*t)*answer
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid full original-domain count')
    return dict(original_independent_bits=n,ones=((1<<n)-gap)//2,gap=gap,
        matrix_size=t,field_polynomial=field_h,source_operator=D,beta=0,eta=eta,
        trace_quadratic_anf=sorted(phi),acquired_characteristic=characteristic,
        acquired_factors=factors,acquired_degree_counts=sorted(degree_counts.items()),
        supplied_primary_decomposition=False,full_original_domain=True,
        profile_kernel=kernel,terms=terms,residual_gaussian_calls=calls,
        quotient_dimension_cap=2,maximum_factor_degree_fixed=False,
        enumerated_original_assignments=0,enumerated_subspaces=0,
        bit_time_bound='poly(a,t,prod_d(m_d+1)) <= exp(O(sqrt(t)))*poly(a,t)',
        polynomial_for_fixed_distinct_degree_count=True,seconds=time.perf_counter()-begun)


def compile_mixed_squarefree_trace_response(D,field_h,eta=0):
    """At most two point weights when every actual factor degree is >=3."""
    F=Field(field_h);t=len(D)
    if not t or any(len(row)!=t or any(type(v) is not int or not 0<=v<F.q for v in row) for row in D):
        raise ValueError('nonempty literal square matrix required')
    if not 0<=eta<F.q:raise ValueError('field eta required')
    polynomial=charpoly(D,F);factors=factor_polynomial(polynomial,F)
    if any(m!=1 or len(f)<4 for f,m in factors):
        raise ValueError('squarefree factors of degree at least three required')
    counts=Counter(len(f)-1 for f,m in factors)
    weights,metadata=mixed_cycle_profile_weights(t,F.q,counts)
    row=weights[tuple(counts[d] for d in sorted(counts))]
    scale=F.q**(t*t+t*(t-1)//2);points={}
    for h,value in enumerate(row):
        point=eta if h%2 else 0
        points[point]=points.get(point,0)+scale*value
    return dict(field_polynomial=field_h,field_degree=F.a,matrix_size=t,
        beta=0,eta=eta,rank_cap=t,padding=t,full_matrix_domain=True,
        original_independent_bits=3*F.a*t*t,counted_domain_size=F.q**(3*t*t),
        response=[dict(kind='point',argument=x,coefficient=y) for x,y in sorted(points.items()) if y],
        acquired=dict(characteristic_polynomial=polynomial,degree_counts=sorted(counts.items()),
            minimal_polynomial_degree=t,supplied_primary_decomposition=False),
        profile_kernel=metadata,remaining_walsh_terms=0,manufactured_point_terms=len(points),
        compiled_without_field_enumeration=True,auxiliary_independent_inputs=0,
        bit_time_bound='exp(O(sqrt(t)))*poly(a,t) and at most two program evaluations')


def compile_raw_mixed_squarefree(poly,n):
    from minimal_polynomial_compiler import acquire_raw_minimal_source
    from arbitrary_operator_hall import quotient_matrix
    from fat_hook_hall import transpose
    acquired=acquire_raw_minimal_source(poly,n,allow_zero_beta=True)
    if acquired['beta']:raise ValueError('the mixed-degree squarefree route requires beta=0')
    algebra=acquired['algebra'];polynomial,primary=algebra.primary_data(acquired['D'])
    D=quotient_matrix(primary,[transpose(tuple(x['jordan_columns'])) for x in primary],algebra.F)
    result=mixed_degree_squarefree_count(D,algebra.h,acquired['phi'],acquired['eta'])
    if result['original_independent_bits']!=n:raise AssertionError('raw input count changed')
    result.update(raw_cubic_input=True,source_acquisition=acquired['stats'],
        source_unit_and_primary_decomposition_supplied=False,
        acquisition_seconds=acquired['acquisition_seconds'])
    return result


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    data=json.loads(args.source.read_text())
    if 'anf' in data:result=compile_raw_mixed_squarefree(data['anf'],data['n'])
    else:result=mixed_degree_squarefree_count(data['D'],data['h'],data.get('phi',()),data.get('eta',0))
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')
