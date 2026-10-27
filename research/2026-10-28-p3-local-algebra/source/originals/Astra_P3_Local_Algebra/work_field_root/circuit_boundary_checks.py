#!/usr/bin/env python3
"""High-degree state repair and failures of unverified truncation."""
from circuit_field_counter import *


def run():
    base=json.loads(Path(__file__).with_name('example_21_bit_circuit.json').read_text())
    extended=dict(n=base['n'],gates=[g[:] for g in base['gates']],output=base['output'])
    h=0
    for i in range(1,6):
        wire=extended['n']+len(extended['gates']);extended['gates'].append(['AND',h,i]);h=wire
    mixed=extended['n']+len(extended['gates']);extended['gates'].append(['XOR',extended['output'],h])
    extended['output']=extended['n']+len(extended['gates']);extended['gates'].append(['XOR',mixed,h])
    result=count_circuit(extended)
    assert result['signed_count']==128 and result['gate_compilation']['maximum_intermediate_degree']==6
    Path(__file__).with_name('example_sparse_high_degree_circuit.json').write_text(json.dumps(extended,separators=(',',':'))+'\n')
    and4=dict(n=4,gates=[['AND',0,1],['AND',4,2],['AND',5,3]],output=6)
    try:circuit_to_cubic(and4)
    except ValueError as error:reject_degree=str(error)
    else:raise AssertionError('quartic output accepted')
    actual=sum((-1)**evaluate_circuit(and4,x) for x in range(16));assert actual==14
    # Sparse high degree is accepted; a dense intermediate can still defeat the budget.
    n=6;b=Builder(n);factors=[b.gate('NOT',i) for i in range(n)];out=factors[0]
    for factor in factors[1:]:out=b.gate('AND',out,factor)
    out=b.gate('XOR',out,out);c=dict(n=n,gates=b.gates,output=out)
    try:circuit_to_cubic(c)
    except ValueError as error:reject_budget=str(error)
    else:raise AssertionError('term budget was silently exceeded')
    exact,certificate=circuit_to_cubic(c,term_budget=64);assert exact==set()
    return dict(status='all exact assertions passed',sparse_high_degree_program=dict(
        n=21,gates=len(extended['gates']),maximum_degree=6,signed_count=result['signed_count'],
        input_file='example_sparse_high_degree_circuit.json'),
        unverified_truncation=dict(input=and4,degree_rejection=reject_degree,
            true_signed_count=actual,false_truncated_signed_count=16),
        honest_budget_failure=dict(input=c,default_budget=42,rejection=reject_budget,
            repaired_budget=64,actual_output_anf=[],certificate=certificate))


if __name__=='__main__':
    data=run();Path(__file__).with_name('circuit_boundary_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status=data['status'],sparse_high_degree=data['sparse_high_degree_program'],false_truncation_count=data['unverified_truncation']['false_truncated_signed_count'])))
