#!/usr/bin/env python3
"""Independent exact tests of liveness, fanout, cancellation, and dead gates."""
from live_circuit_anf import circuit_to_cubic_live
from contact_circuit_counter import circuit_to_cubic_live as production_frontend
from circuit_field_counter import circuit_to_cubic,evaluate_circuit
from field_descent import polynomial_value
from pathlib import Path
import json,random


def run():
    rng=random.Random(772600);cases=[];rejected=0;truth_points=0
    for trial in range(80):
        n=2+trial%7;gates=[]
        for j in range(50):
            op=rng.choice(['AND','XOR','NOT','CONST']);wire=n+j
            if op=='CONST':gate=[op,rng.randrange(2)]
            elif op=='NOT':gate=[op,rng.randrange(wire)]
            else:gate=[op,rng.randrange(wire),rng.randrange(wire)]
            gates.append(gate)
        circuit=dict(n=n,gates=gates,output=rng.randrange(n+len(gates)))
        try:old,_=circuit_to_cubic(circuit,term_budget=1<<n)
        except ValueError as exc:
            assert 'degree exceeds three' in str(exc)
            try:circuit_to_cubic_live(circuit,term_budget=1<<n)
            except ValueError as other:assert 'degree exceeds three' in str(other)
            else:raise AssertionError('invalid high-degree output accepted')
            rejected+=1;continue
        new,certificate=production_frontend(circuit,term_budget=1<<n);assert old==new
        for x in range(1<<n):assert polynomial_value(new,x)==evaluate_circuit(circuit,x)
        truth_points+=1<<n;cases.append(certificate)
    # Shared AND, high-degree cancellation, and irrelevant quartic states.
    special=dict(n=4,gates=[['AND',0,1],['AND',4,2],['AND',5,3],
        ['AND',6,6],['XOR',7,6],['XOR',8,0],['NOT',1]],output=9)
    poly,certificate=circuit_to_cubic_live(special,term_budget=16)
    assert poly=={1} and certificate['maximum_intermediate_degree']==4
    assert certificate['unreachable_gates']==1
    for x in range(16):assert evaluate_circuit(special,x)==(x&1)
    invalid=dict(n=2,gates=[['AND',7,0]],output=0)
    try:circuit_to_cubic_live(invalid)
    except ValueError:pass
    else:raise AssertionError('unreachable noncausal gate was not rejected')
    result=dict(random_cases=len(cases),high_degree_outputs_rejected=rejected,
        original_assignments_checked=truth_points+16,special_cancellation=certificate,
        invalid_dead_gate_rejected=True,cases=cases)
    Path(__file__).with_name('live_circuit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','special_cancellation')}))


if __name__=='__main__':run()
