#!/usr/bin/env python3
"""Gate-program front end for the acquired weighted critical-ray counter."""
from acquired_quotient_counter import *
from stationary_circuit_counter import circuit_from_smooth_case
from circuit_field_counter import circuit_to_cubic,evaluate_circuit
import random

def count_quotient_circuit(circuit,*,term_budget=None,terminal_bit_budget=24):
    started=time.perf_counter();poly,front=circuit_to_cubic(circuit,term_budget=term_budget)
    result=compile_quotient(poly,circuit['n'],terminal_bit_budget=terminal_bit_budget)
    result.update(gate_compilation=front,complete_seconds=time.perf_counter()-started)
    return result,poly

def validation():
    source=next(c for c in json.loads(Path(__file__).with_name('quotient_counter_results.json').read_text())['cases']
                if c['original_variables']==72)
    circuit=circuit_from_smooth_case(source)
    path=Path(__file__).with_name('quotient_72_bit_circuit.json')
    path.write_text(json.dumps(circuit,separators=(',',':'))+'\n')
    result,poly=count_quotient_circuit(circuit)
    raw=json.loads(Path(__file__).with_name(source['raw_input_file']).read_text())
    assert poly==set(raw['polynomial']) and result['signed_count']==source['signed_count']
    rng=random.Random(877272)
    for _ in range(1024):
        x=rng.randrange(1<<72);assert evaluate_circuit(circuit,x)==polynomial_value(poly,x)
    result.update(exact_raw_coefficient_identity=True,original_input_checks=1024,
        circuit_file=path.name,description_bytes=path.stat().st_size,practical_speed_claim=False)
    Path(__file__).with_name('quotient_circuit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['original_variables','signed_count','zero_count',
        'gate_compilation','complete_seconds']}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path,nargs='?')
    parser.add_argument('--output',type=Path);parser.add_argument('--term-budget',type=int)
    parser.add_argument('--terminal-bit-budget',type=int,default=24);args=parser.parse_args()
    if args.input:
        result,_=count_quotient_circuit(json.loads(args.input.read_text()),term_budget=args.term_budget,
                                       terminal_bit_budget=args.terminal_bit_budget)
        text=json.dumps(result,indent=2)+'\n'
        if args.output:args.output.write_text(text)
        else:print(text,end='')
    else:validation()
