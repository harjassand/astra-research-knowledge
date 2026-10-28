#!/usr/bin/env python3
"""Evaluate an original-domain pencil response on its acquired actual support.

This is a separate adapter; the original full-field Walsh evaluator remains
available as a reference. Field scanning and program evaluation have distinct,
explicit budgets. No field elements or program values are enumerated by default
unless a nonzero point list has already been manufactured.
"""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_norm_slice_agent','work_matrix_root',
    'work_norm_frontier_agent','work_norm_glue_agent')]
from sparse_trace_response import canonical_sparse_spec,acquire_sparse_response_support
from equidegree_trace_program import validate_trace_program


def count_response_sparse_spec(response):
    """Translate the compiler's point/Walsh encoding without changing weights."""
    a=response['field_degree'];points=[];characters=[]
    for item in response['response']:
        pair=[item['argument'],item['coefficient']]
        if item['kind']=='point':points.append(pair)
        elif item['kind']=='walsh':characters.append(pair)
        else:raise ValueError('only certified point or binary-Walsh terms are accepted')
    return canonical_sparse_spec(dict(output_bits=a,
        field_polynomial=response['field_polynomial'],output_boolean_quadratic=[],
        points=points,characters=characters))


def prepared_program(program,inputs):
    """Validate once and prepare O(inputs + gates) evaluation per support point."""
    n,gates,output=validate_trace_program(program,inputs)
    instructions=[]
    for gate in gates:
        op=gate['op'];args=gate.get('args',())
        instructions.append((op,tuple(args),gate.get('value')))
    def evaluate(point):
        if type(point) is not int or point<0 or point.bit_length()>n:
            raise ValueError('trace input is outside its binary domain')
        # Convert the packed point once, rather than making n large shifts.
        packed=point.to_bytes((n+7)//8,'little')
        wires=[(packed[i>>3]>>(i&7))&1 for i in range(n)]
        for op,args,value in instructions:
            if op=='const':bit=value
            elif op=='not':bit=1^wires[args[0]]
            elif op=='and':bit=wires[args[0]]&wires[args[1]]
            elif op=='or':bit=wires[args[0]]|wires[args[1]]
            else:bit=wires[args[0]]^wires[args[1]]
            wires.append(bit)
        return wires[output]
    return evaluate,n+len(gates),len(gates)


def evaluate_trace_count_response_sparse(response,program,
        maximum_field_evaluations=0,maximum_program_evaluations=None):
    """Count exactly if actual response support fits both explicit budgets.

    The default accepts an already acquired point-only response without a
    scan. With character terms, the uncertainty bound may certify large
    support with zero scans, but any complete scan needs an explicit numerical
    field budget. The program is called exactly s times only after its entire
    response support of size s has been acquired.
    """
    if type(maximum_field_evaluations) is not int or maximum_field_evaluations<0:
        raise ValueError('nonnegative explicit field-evaluation budget required')
    if maximum_program_evaluations is not None and (
        type(maximum_program_evaluations) is not int or maximum_program_evaluations<0):
        raise ValueError('nonnegative explicit program-evaluation budget required')
    spec=count_response_sparse_spec(response)
    evaluate,L,gates=prepared_program(program,spec['output_bits'])
    budget=(max(maximum_field_evaluations,len(spec['points']))
            if maximum_program_evaluations is None else maximum_program_evaluations)
    support=acquire_sparse_response_support(spec,budget,
        maximum_field_scan=maximum_field_evaluations)
    common=dict(original_independent_bits=response['original_independent_bits'],
        counted_domain_size=response['counted_domain_size'],
        full_matrix_domain=response['full_matrix_domain'],
        rank_cap=None if response['full_matrix_domain'] else response['rank_cap'],
        trace_program_gates=gates,trace_program_size=L,
        trace_program_anf_expanded=False,auxiliary_independent_inputs=0,
        remaining_walsh_terms=len(spec['characters']),
        field_evaluation_budget=maximum_field_evaluations,
        program_evaluation_budget=budget,support_certificate=support,
        response_field_evaluations=support['enumerated_field_elements'])
    if support['status']!='support_acquired':
        return dict(**common,status=support['status'],gap=None,ones=None,
            zeros_on_counted_domain=None,trace_program_evaluations=0,
            circuit_boolean_operation_bound=0,evaluated_points=[])
    gap=0;points=[]
    for point,coefficient in support['support']:
        gap+=coefficient*(1-2*evaluate(point));points.append(point)
    domain=response['counted_domain_size']
    if type(domain) is not int or domain<0 or abs(gap)>domain or (domain-gap)%2:
        raise AssertionError('invalid reconstructed original-domain count')
    return dict(**common,status='counted',gap=gap,ones=(domain-gap)//2,
        zeros_on_counted_domain=(domain+gap)//2,
        trace_program_evaluations=len(points),
        circuit_boolean_operation_bound=len(points)*L,evaluated_points=points)
