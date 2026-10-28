#!/usr/bin/env python3
"""Acquired full beta-zero operator counts and certified two-point programs."""
from pathlib import Path
import json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_multiprimary_audit',
    'work_norm_frontier_agent','work_norm_slice_agent')]
from matrix_kloosterman import Field,charpoly,factor_polynomial
from arbitrary_beta_zero_hall_aggregate import arbitrary_beta_zero_count,even_only_trace_response
from mixed_degree_squarefree_counter import mixed_degree_squarefree_count,compile_mixed_squarefree_trace_response

def count_beta_zero_operator(D,field_h,phi=(),eta=0):
    F=Field(field_h);factors=factor_polynomial(charpoly(D,F),F)
    if all(m==1 for f,m in factors):
        result=mixed_degree_squarefree_count(D,field_h,phi,eta)
        result['selected_backend']='integral mixed-degree divided powers'
    else:
        result=arbitrary_beta_zero_count(D,field_h,phi,eta)
        result['selected_backend']='even-block Hall aggregation with at most two active factors'
    return result

def compile_beta_zero_trace_response(D,field_h,eta=0):
    """Manufacture support {0,eta} after checking odd-block annihilation."""
    F=Field(field_h);t=len(D);factors=factor_polynomial(charpoly(D,F),F)
    if not 0<=eta<F.q:raise ValueError('field eta required')
    eta2=F.mul(eta,eta)
    if any(len(f)==2 or (len(f)==3 and F.mul(eta2,f[1])==1) for f,m in factors):
        raise ValueError('the acquired spectrum allows a nonzero odd-row quotient')
    if all(len(f)>=4 for f,m in factors):
        if all(m==1 for f,m in factors):return compile_mixed_squarefree_trace_response(D,field_h,eta)
        return even_only_trace_response(D,field_h,eta)
    # The same proved support test includes nonresonant degree-two factors.
    # Two full Gaussian evaluations reconstruct the two exact integer weights.
    first=count_beta_zero_operator(D,field_h,(),eta);total=first['gap'];points={0:total}
    probes=1
    if eta:
        coordinate=eta&-eta
        second=count_beta_zero_operator(D,field_h,(coordinate,),eta);difference=second['gap'];probes+=1
        assert (total+difference)%2==0
        points={0:(total+difference)//2,eta:(total-difference)//2}
    points={x:y for x,y in points.items() if y}
    return dict(field_polynomial=field_h,field_degree=F.a,matrix_size=t,
        beta=0,eta=eta,rank_cap=t,padding=t,full_matrix_domain=True,
        original_independent_bits=3*F.a*t*t,counted_domain_size=F.q**(3*t*t),
        response=[dict(kind='point',argument=x,coefficient=y) for x,y in sorted(points.items())],
        remaining_walsh_terms=0,manufactured_point_terms=len(points),
        acquired_factors=factors,odd_row_cancellation_verified=True,
        exact_full_counter_probes=probes,auxiliary_independent_inputs=0,
        compiled_without_field_enumeration=True,
        bit_time_bound='exp(O(sqrt(t)))*poly(a,t), plus at most two program evaluations')

def compile_raw_beta_zero(poly,n):
    from minimal_polynomial_compiler import acquire_raw_minimal_source
    from arbitrary_operator_hall import quotient_matrix,transpose_partition
    begun=time.perf_counter();acquired=acquire_raw_minimal_source(poly,n,allow_zero_beta=True)
    if acquired['beta']:raise ValueError('this backend requires acquired beta=0')
    algebra=acquired['algebra'];polynomial,primary=algebra.primary_data(acquired['D'])
    D=quotient_matrix(primary,[transpose_partition(x['jordan_columns']) for x in primary],algebra.F)
    result=count_beta_zero_operator(D,algebra.h,acquired['phi'],acquired['eta'])
    if result['original_independent_bits']!=n:raise AssertionError('raw input domain changed')
    result.update(raw_cubic_input=True,source_acquisition=acquired['stats'],
        source_unit_and_primary_decomposition_supplied=False,
        acquisition_seconds=acquired['acquisition_seconds'],total_seconds=time.perf_counter()-begun)
    return result

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--trace-response',action='store_true')
    args=parser.parse_args();data=json.loads(args.source.read_text())
    if 'anf' in data:result=compile_raw_beta_zero(data['anf'],data['n'])
    elif args.trace_response:result=compile_beta_zero_trace_response(data['D'],data['h'],data.get('eta',0))
    else:result=count_beta_zero_operator(data['D'],data['h'],data.get('phi',()),data.get('eta',0))
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')
