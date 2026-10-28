#!/usr/bin/env python3
"""Acquire a Boolean trace program's affine information and project its response.

This separate path may count a full-support original response. Small dimension
is never assumed: exact affine cuts of the actual DAG supply a verified span.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_norm_slice_agent','work_matrix_root',
    'work_norm_frontier_agent','work_norm_glue_agent')]
from equidegree_trace_program import validate_trace_program
from pencil_trace_response_evaluator import count_response_sparse_spec,prepared_program
from sparse_trace_response import canonical_sparse_spec,acquire_sparse_response_support


class BinarySpan:
    def __init__(self):self.pivots={}
    def add(self,vector,payload):
        v=vector;c=payload
        while v:
            i=v.bit_length()-1
            if i not in self.pivots:self.pivots[i]=(v,c);return True
            w,d=self.pivots[i];v^=w;c^=d
        return False
    def coordinates(self,vector):
        value=0;v=vector
        while v:
            i=v.bit_length()-1
            if i not in self.pivots:return None
            w,d=self.pivots[i];v^=w;value^=d
        return value


def apply_binary(columns,value):
    out=0
    while value:
        bit=value&-value;out^=columns[bit.bit_length()-1];value^=bit
    return out


def affine_product(left,right):
    if left==(0,0) or right==(0,0):return (0,0)
    if left==(0,1):return right
    if right==(0,1):return left
    if left is None or right is None:return None
    if left[0]==right[0]:return left if left[1]==right[1] else (0,0)
    return None


def acquire_program_affine_span(program):
    """Certify P(x)=R(Bx) by exact affine cuts, without a high-degree ANF."""
    n=program.get('inputs',program.get('n'));n,gates,output=validate_trace_program(program,n)
    forms=[(1<<i,0) for i in range(n)]
    for gate in gates:
        op=gate['op'];args=gate.get('args',[]);values=[forms[i] for i in args]
        if op=='const':value=(0,int(gate['value']))
        elif op=='not':value=None if values[0] is None else (values[0][0],values[0][1]^1)
        elif op=='xor':
            value=(0,0) if args[0]==args[1] else None if None in values else (
                values[0][0]^values[1][0],values[0][1]^values[1][1])
        elif op=='and':value=affine_product(*values)
        else:
            complements=[None if x is None else (x[0],x[1]^1) for x in values]
            product=affine_product(*complements)
            value=None if product is None else (product[0],product[1]^1)
        forms.append(value)
    needed=set();cuts={};pending=[output]
    while pending:
        current=pending.pop()
        if current in needed:continue
        needed.add(current)
        if forms[current] is not None:cuts[current]=forms[current]
        else:pending.extend(gates[current-n].get('args',[]))
    span=BinarySpan();rows=[]
    for wire,(mask,constant) in sorted(cuts.items()):
        if span.add(mask,1<<len(rows)):rows.append(mask)
    r=len(rows);columns=[sum(((row>>i)&1)<<j for j,row in enumerate(rows)) for i in range(n)]
    section_solver=BinarySpan()
    for i,column in enumerate(columns):section_solver.add(column,1<<i)
    section=[section_solver.coordinates(1<<i) for i in range(r)]
    assert all(x is not None for x in section)
    assert all(apply_binary(columns,column)==1<<i for i,column in enumerate(section))
    bindings=[dict(wire=wire,mask=mask,constant=constant,
        summary_frequency=span.coordinates(mask)) for wire,(mask,constant) in sorted(cuts.items())]
    assert all(item['summary_frequency'] is not None for item in bindings)
    return dict(original_program_inputs=n,original_program_gates=len(gates),
        summary_bits=r,row_masks=rows,summary_columns=columns,section_columns=section,
        affine_cut_bindings=bindings,affine_cut_count=len(cuts),
        retained_nonlinear_nodes=len(needed)-len(cuts),
        exact_DAG_factorization_verified=True,original_input_assignments_enumerated=0)


def pushforward_response_to_program_span(response,span):
    spec=count_response_sparse_spec(response);a=spec['output_bits'];r=span['summary_bits']
    if a!=span['original_program_inputs']:raise ValueError('program and response input widths disagree')
    solver=BinarySpan()
    for i,row in enumerate(span['row_masks']):assert solver.add(row,1<<i)
    points={};characters={};discarded=0
    for point,coefficient in spec['points']:
        y=apply_binary(span['summary_columns'],point);points[y]=points.get(y,0)+coefficient
    for frequency,coefficient in spec['characters']:
        target=solver.coordinates(frequency)
        if target is None:discarded+=1;continue
        characters[target]=characters.get(target,0)+(coefficient<<(a-r))
    projected=canonical_sparse_spec(dict(output_bits=r,output_boolean_quadratic=[],
        points=list(points.items()),characters=list(characters.items())))
    projected.update(original_trace_bits=a,binary_fiber_dimension=a-r,
        discarded_character_terms=discarded,scanned_original_field_elements=0)
    return projected


def evaluate_trace_response_program_span(response,program,
        maximum_summary_evaluations=0,maximum_program_evaluations=None):
    if type(maximum_summary_evaluations) is not int or maximum_summary_evaluations<0:
        raise ValueError('nonnegative explicit summary-scan budget required')
    if maximum_program_evaluations is not None and (
        type(maximum_program_evaluations) is not int or maximum_program_evaluations<0):
        raise ValueError('nonnegative explicit program-evaluation budget required')
    span=acquire_program_affine_span(program);projected=pushforward_response_to_program_span(response,span)
    evaluate,L,gates=prepared_program(program,span['original_program_inputs'])
    budget=(max(maximum_summary_evaluations,len(projected['points']))
        if maximum_program_evaluations is None else maximum_program_evaluations)
    support=acquire_sparse_response_support(projected,budget,maximum_summary_evaluations)
    common=dict(program_span_certificate=span,projected_response=projected,
        summary_support_certificate=support,summary_evaluation_budget=maximum_summary_evaluations,
        program_evaluation_budget=budget,scanned_original_field_elements=0,
        summary_response_evaluations=support['enumerated_field_elements'],
        original_independent_bits=response['original_independent_bits'],
        counted_domain_size=response['counted_domain_size'],full_matrix_domain=response['full_matrix_domain'],
        trace_program_size=L,trace_program_gates=gates,
        trace_program_anf_expanded=False,auxiliary_independent_inputs=0)
    if support['status']!='support_acquired':
        status=('summary_scan_budget_insufficient' if support['status']=='field_scan_budget_insufficient'
            else support['status'])
        return dict(**common,status=status,gap=None,ones=None,trace_program_evaluations=0,
            circuit_boolean_operation_bound=0,evaluated_program_inputs=[])
    gap=0;representatives=[]
    for point,coefficient in support['support']:
        x=apply_binary(span['section_columns'],point)
        gap+=coefficient*(1-2*evaluate(x));representatives.append(x)
    domain=response['counted_domain_size']
    if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid original-domain projected count')
    return dict(**common,status='counted',gap=gap,ones=(domain-gap)//2,
        zeros_on_counted_domain=(domain+gap)//2,trace_program_evaluations=len(representatives),
        circuit_boolean_operation_bound=len(representatives)*L,evaluated_program_inputs=representatives)
