#!/usr/bin/env python3
"""Polynomial-size circuit-to-cubic representation, NOT a polynomial #SAT solver.

The optional reference counter explicitly enumerates the original inputs.
Output algebraic normal forms are never expanded by the compiler.
"""
from pathlib import Path
import argparse,json,random

def toggle(poly,m):
    if m in poly:poly.remove(m)
    else:poly.add(m)

def anf_value(poly,x):return sum((x&m)==m for m in poly)&1

def gate_anf(gate,wire):
    if not isinstance(gate,list) or not gate:raise ValueError('invalid gate record')
    op=gate[0]
    if op=='CONST':
        if len(gate)!=2 or type(gate[1]) is not int or gate[1] not in (0,1):raise ValueError('invalid constant')
        return {0} if gate[1] else set()
    arity={'NOT':1,'AND':2,'XOR':2,'OR':2,'NAND':2,'NOR':2,'XNOR':2,'TT':2}.get(op)
    if arity is None:raise ValueError('unknown gate')
    arguments=gate[2:] if op=='TT' else gate[1:]
    if len(arguments)!=arity or any(type(a) is not int or not 0<=a<wire for a in arguments):
        raise ValueError('invalid arity or noncausal wire')
    if op=='NOT':return {0,1<<arguments[0]}
    tables={'AND':8,'XOR':6,'OR':14,'NAND':7,'NOR':1,'XNOR':9}
    table=gate[1] if op=='TT' else tables[op]
    if type(table) is not int or not 0<=table<16:raise ValueError('invalid binary truth table')
    values=[(table>>i)&1 for i in range(4)]
    coefficients=[values[0],values[0]^values[1],values[0]^values[2],sum(values)&1]
    a,b=arguments;monomials=[0,1<<a,1<<b,(1<<a)|(1<<b)];poly=set()
    for c,m in zip(coefficients,monomials):
        if c:toggle(poly,m)
    return poly

def compile_circuit_phase(circuit):
    """Z(phase)=2^(g+1)*#accepted inputs; N=n+2g+1, at most 5g+2 terms."""
    n=circuit['n'];gates=circuit['gates'];output=circuit['output']
    if type(n) is not int or n<0 or not isinstance(gates,list):raise ValueError('invalid input inventory')
    g=len(gates);primal=n+g
    if type(output) is not int or not 0<=output<primal:raise ValueError('invalid output wire')
    equations=[];phase=set()
    for index,gate in enumerate(gates):
        wire=n+index;equation=gate_anf(gate,wire);toggle(equation,1<<wire);equations.append(equation)
    equations.append({0,1<<output})
    for index,equation in enumerate(equations):
        multiplier=1<<(primal+index)
        for monomial in equation:toggle(phase,monomial|multiplier)
    assert max((m.bit_count() for m in phase),default=0)<=3 and len(phase)<=5*g+2
    return dict(original_inputs=n,internal_gates=g,constraints=g+1,
        phase_variables=n+2*g+1,phase_anf=sorted(phase),constraint_anf=[sorted(p) for p in equations],
        multiplier_variables=list(range(primal,primal+g+1)),
        exact_reconstruction_denominator=1<<(g+1),description_monomials=len(phase),
        output_anf_expanded=False,general_polynomial_counter=False)

def circuit_value(circuit,x):
    n=circuit['n'];packed=x
    for index,gate in enumerate(circuit['gates']):
        wire=n+index
        if anf_value(gate_anf(gate,wire),packed):packed|=1<<wire
    return (packed>>circuit['output'])&1

def exact_reference_count(circuit,*,input_bit_budget=20):
    compiled=compile_circuit_phase(circuit);n=circuit['n']
    if n>input_bit_budget:raise ValueError('explicit original-input scan exceeds budget')
    count=sum(circuit_value(circuit,x) for x in range(1<<n))
    return dict(satisfying_inputs=count,original_inputs_enumerated=1<<n,
        reference_backend='exhaustive original-input evaluation',
        implied_phase_signed_count=count*compiled['exact_reconstruction_denominator'],
        phase_signed_count_independently_evaluated=False)

def check():
    rng=random.Random(104281);cases=[]
    fixtures=[dict(n=2,gates=[['AND',0,1]],output=2),
        dict(n=3,gates=[['TT',7,0,1],['TT',14,3,2]],output=4),
        dict(n=0,gates=[['CONST',1]],output=0),
        dict(n=3,gates=[['XOR',0,0],['OR',1,2],['AND',3,4]],output=5)]
    for trial in range(32):
        n=1+trial%4;g=1+trial%5;gates=[]
        for index in range(g):
            bound=n+index;gates.append(['TT',rng.randrange(16),rng.randrange(bound),rng.randrange(bound)])
        fixtures.append(dict(n=n,gates=gates,output=n+g-1))
    for circuit in fixtures:
        compiled=compile_circuit_phase(circuit);N=compiled['phase_variables'];reference=exact_reference_count(circuit)
        gap=sum(1-2*anf_value(compiled['phase_anf'],x) for x in range(1<<N))
        assert gap==reference['implied_phase_signed_count']
        cases.append(dict(circuit=circuit,compiled=compiled,original_satisfying_inputs=reference['satisfying_inputs'],
            phase_signed_count=gap,phase_assignments_exhaustively_checked=1<<N))
    n=128;gates=[['OR',0,1]]
    for i in range(2,n):gates.append(['OR',n+len(gates)-1,i])
    large=dict(n=n,gates=gates,output=n+len(gates)-1);compressed=compile_circuit_phase(large)
    assert compressed['description_monomials']==4*(n-1)+2
    rejected=0
    for bad in [dict(n=1,gates=[['AND',0,1]],output=1),dict(n=1,gates=[['TT',16,0,0]],output=1)]:
        try:compile_circuit_phase(bad)
        except ValueError:rejected+=1
        else:raise AssertionError('invalid circuit accepted')
    result=dict(status='all assertions passed',small_cases=cases,
        phase_assignments_exhaustively_checked=sum(c['phase_assignments_exhaustively_checked'] for c in cases),
        large_or_fixture=dict(circuit=large,compiled=compressed,mathematically_known_output_anf_terms=(1<<n)-1,
            known_count=(1<<n)-1,count_computed_by_general_algorithm=False),
        invalid_gate_cases_rejected=rejected,polynomial_time_counting_claim=False)
    Path(__file__).with_name('universal_circuit_phase_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],cases=len(cases),phase_assignments=result['phase_assignments_exhaustively_checked'],
        large_circuit_inputs=n,large_phase_variables=compressed['phase_variables'],large_phase_monomials=compressed['description_monomials'])),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',nargs='?',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--checks',action='store_true');args=parser.parse_args()
    if args.checks:check()
    elif args.input:
        result=compile_circuit_phase(json.loads(args.input.read_text()));text=json.dumps(result,indent=2)+'\n'
        if args.output:args.output.write_text(text)
        else:print(text,end='')
    else:parser.error('provide an input circuit or --checks')
