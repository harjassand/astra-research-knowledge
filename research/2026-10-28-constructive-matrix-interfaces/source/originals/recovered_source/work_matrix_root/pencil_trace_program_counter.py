#!/usr/bin/env python3
"""Manufacture a point/Walsh response for a Boolean matrix-trace program.

The source program is never expanded into ANF. A response containing
only points is evaluated in polynomially many program evaluations.
Nonzero Walsh terms are exposed and require an explicit field-domain
evaluation budget; they are not treated as free summaries.
"""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_slice_agent',
    'work_norm_frontier_agent','work_norm_glue_agent')]
from minimal_polynomial_counter import (Field,minimal_polynomial_types,
    ManufacturedHomEpi,opposite_moments,rank_restricted_cubic_count)
from primary_rank_moments import gaussian_binomial
from quadratic_trace_pushforward import pencil_trace_response,response_value
from equidegree_trace_program import validate_trace_program,evaluate_trace_program


def add_scaled(target,source,scale):
    if not scale:return
    for key,value in source.items():
        target[key]=target.get(key,0)+scale*value
        if not target[key]:del target[key]


def encoded(response):
    return [dict(kind=kind,argument=argument,coefficient=value)
            for (kind,argument),value in sorted(response.items())]


def compile_trace_count_response(D,field_h,beta,eta=0,rank_cap=None,padding=None):
    """Exact response on the ORIGINAL independent matrix-input domain."""
    begun=time.perf_counter();F=Field(field_h);q=F.q;t=len(D)
    r=t if rank_cap is None else rank_cap;T=t if padding is None else padding
    if type(r) is not int or not 0<=r<=t or type(T) is not int or T<0:
        raise ValueError('explicit valid rank depth and rectangular width required')
    if not t or any(len(row)!=t or any(type(x) is not int or not 0<=x<q for x in row) for row in D):
        raise ValueError('explicit square source operator required')
    if not 0<=beta<q or not 0<=eta<q:raise ValueError('field-valued source coefficients required')
    types,acquired=minimal_polynomial_types(D,F,r)
    backend=ManufacturedHomEpi(D,field_h,r,types)
    # This acquires the populations with the already independently audited
    # implementation. Its unrefined moment values also check the response.
    base=opposite_moments(D,field_h,beta,(),eta,r,backend)
    moment_responses=[{} for _ in range(r+1)];records=[]
    for R,population in zip(types,base['manufactured_pencil_types']):
        number=population['subspaces']
        if not number:continue
        response=pencil_trace_response(R,field_h,beta,eta)
        scale=number*q**(R.u*(t-R.c));kind=response['field_response_kind']
        if kind=='zero':term={}
        elif kind=='point':
            point=response['field_response_point'];term={('point',point):scale*response_value(response,point)}
        else:
            frequency=response['base_character_binary_frequency']
            term={('walsh',frequency):scale*response['amplitude']*(1-2*response['base_character_constant'])}
        add_scaled(moment_responses[R.u],term,1)
        records.append(dict(pencil=repr(R.label),domain=R.u,codomain=R.c,subspaces=number,
            response_kind=kind,support_cardinality=response['support_cardinality'],
            trace_point=response.get('field_response_point'),
            binary_frequency=response.get('base_character_binary_frequency'),
            amplitude=response['amplitude'],sign=response['sign_anf']))
    for i,response in enumerate(moment_responses):
        at_zero_program=sum(c if kind=='point' else q*c if argument==0 else 0
            for (kind,argument),c in response.items())
        if at_zero_program!=base['opposite_kernel_moments'][i]:raise AssertionError('unrefined trace response mismatch')
    layer_responses=[]
    for i,response in enumerate(moment_responses):
        layer=dict(response)
        for j,previous in enumerate(layer_responses):add_scaled(layer,previous,-gaussian_binomial(t-j,i-j,q))
        layer_responses.append(layer)
    whole={}
    for j,response in enumerate(layer_responses):add_scaled(whole,response,q**(2*t*T-T*j))
    domain=rank_restricted_cubic_count(base,T)
    return dict(field_polynomial=field_h,field_degree=F.a,matrix_size=t,beta=beta,eta=eta,
        rank_cap=r,padding=T,full_matrix_domain=r==t,
        original_independent_bits=F.a*(t*t+2*t*T),counted_domain_size=domain['restricted_domain_size'],
        response=encoded(whole),moment_responses=[encoded(x) for x in moment_responses],
        rank_layer_responses=[encoded(x) for x in layer_responses],pencil_responses=records,
        acquired=acquired,hom_table_statistics=base['hom_table_statistics'],
        remaining_walsh_terms=sum(kind=='walsh' for kind,argument in whole),
        manufactured_point_terms=sum(kind=='point' for kind,argument in whole),
        trace_program_anf_expanded=False,auxiliary_independent_inputs=0,
        compiled_without_field_enumeration=True,seconds=time.perf_counter()-begun)


def evaluate_trace_count_response(response,program,maximum_field_evaluations=0):
    a=response['field_degree'];q=1<<a;_,gates,_=validate_trace_program(program,a)
    if type(maximum_field_evaluations) is not int or maximum_field_evaluations<0:
        raise ValueError('nonnegative explicit field-evaluation budget required')
    walsh=[x for x in response['response'] if x['kind']=='walsh'];cache={};spectrum=None
    if walsh:
        if q>maximum_field_evaluations:
            raise ValueError('manufactured response retains Walsh coefficients; field-domain evaluation budget is insufficient')
        spectrum=[]
        for point in range(q):
            bit=evaluate_trace_program(program,point,a);cache[point]=bit;spectrum.append(1-2*bit)
        step=1
        while step<q:
            for start in range(0,q,2*step):
                for j in range(step):
                    u=spectrum[start+j];v=spectrum[start+j+step]
                    spectrum[start+j]=u+v;spectrum[start+j+step]=u-v
            step*=2
    gap=0
    for item in response['response']:
        point=item['argument']
        if item['kind']=='walsh':value=spectrum[point]
        else:
            if point not in cache:cache[point]=evaluate_trace_program(program,point,a)
            value=1-2*cache[point]
        gap+=item['coefficient']*value
    domain=response['counted_domain_size']
    if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid reconstructed original-domain count')
    return dict(gap=gap,ones=(domain-gap)//2,zeros_on_counted_domain=(domain+gap)//2,
        original_independent_bits=response['original_independent_bits'],
        counted_domain_size=domain,full_matrix_domain=response['full_matrix_domain'],
        rank_cap=None if response['full_matrix_domain'] else response['rank_cap'],
        trace_program_gates=len(gates),trace_program_evaluations=len(cache),
        trace_program_anf_expanded=False,auxiliary_independent_inputs=0,
        evaluated_points=sorted(cache),remaining_walsh_terms=len(walsh),
        field_evaluation_budget=maximum_field_evaluations)
