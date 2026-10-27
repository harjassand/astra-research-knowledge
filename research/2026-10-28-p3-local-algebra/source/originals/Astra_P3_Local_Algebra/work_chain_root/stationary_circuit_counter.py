#!/usr/bin/env python3
"""Manufacture raw ANF from actual gates, then acquire stationary ring structure."""
from stationary_chain_counter import *
from chain_circuit_counter import RingBuilder
from circuit_field_counter import circuit_to_cubic,evaluate_circuit
from field_kloosterman import gf_trace
import random

def circuit_from_smooth_case(case):
    n=case['original_variables'];R=ChainRing(case['planted_field_modulus'],case['planted_chain_length'])
    b=RingBuilder(n);columns=case['planted_binary_columns'];offset=case['planted_binary_offset']
    y=[b.xor([i for i in range(n) if columns[i]>>j&1]+([b.one] if offset>>j&1 else []))
       for j in range(n)]
    variables=[y[R.m*i:R.m*(i+1)] for i in range(3)]
    cache={(0,0,0):[b.one]+[b.zero]*(R.m-1)}
    for i in range(3):cache[tuple(int(j==i) for j in range(3))]=variables[i]
    def monomial(exponent):
        exponent=tuple(exponent)
        if exponent not in cache:
            i=next(j for j in range(3) if exponent[j]);lower=list(exponent);lower[i]-=1
            cache[exponent]=b.ring_mul(monomial(lower),variables[i],R)
        return cache[exponent]
    total=b.ring_add([b.ring_scale(monomial(t['exponents']),t['coefficient'],R)
                     for t in case['planted_polynomial']],R)
    terms=[total[R.d*(R.e-1)+i] for i in range(R.d) if gf_trace(1<<i,R.h)]
    if case['planted_constant']:terms.append(b.one)
    factors=case['planted_error_factors']
    for a,c in zip(factors[::2],factors[1::2]):
        terms.append(b.gate('AND',b.xor(y[i] for i in bits(a)),b.xor(y[i] for i in bits(c))))
    return dict(n=n,gates=b.gates,output=b.xor(terms))

def count_stationary_circuit(circuit,*,term_budget=None,terminal_bit_budget=24):
    started=time.perf_counter();poly,front=circuit_to_cubic(circuit,term_budget=term_budget)
    result=compile_stationary(poly,circuit['n'],terminal_bit_budget=terminal_bit_budget)
    result.update(gate_compilation=front,complete_seconds=time.perf_counter()-started)
    return result,poly

def validation():
    source=next(c for c in json.loads(Path(__file__).with_name('stationary_counter_results.json').read_text())['cases']
                if c['original_variables']==45)
    circuit=circuit_from_smooth_case(source)
    path=Path(__file__).with_name('stationary_45_bit_circuit.json')
    path.write_text(json.dumps(circuit,separators=(',',':'))+'\n')
    result,poly=count_stationary_circuit(circuit)
    raw=json.loads(Path(__file__).with_name(source['raw_input_file']).read_text())
    assert poly==set(raw['polynomial']) and result['signed_count']==source['signed_count']
    rng=random.Random(600545)
    for _ in range(1024):
        x=rng.randrange(1<<45);assert evaluate_circuit(circuit,x)==polynomial_value(poly,x)
    result.update(exact_raw_coefficient_identity=True,original_input_checks=1024,
        circuit_file=path.name,description_bytes=path.stat().st_size,practical_speed_claim=False)
    Path(__file__).with_name('stationary_circuit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['original_variables','signed_count','zero_count',
        'gate_compilation','complete_seconds']}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path,nargs='?')
    parser.add_argument('--output',type=Path);parser.add_argument('--term-budget',type=int)
    parser.add_argument('--terminal-bit-budget',type=int,default=24);args=parser.parse_args()
    if args.input:
        result,_=count_stationary_circuit(json.loads(args.input.read_text()),term_budget=args.term_budget,
                                         terminal_bit_budget=args.terminal_bit_budget)
        text=json.dumps(result,indent=2)+'\n'
        if args.output:args.output.write_text(text)
        else:print(text,end='')
    else:validation()
