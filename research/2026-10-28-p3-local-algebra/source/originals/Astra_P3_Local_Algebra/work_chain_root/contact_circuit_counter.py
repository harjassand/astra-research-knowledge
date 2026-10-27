#!/usr/bin/env python3
"""Actual gate frontend for the unbounded-module-rank contact compiler."""
from acquired_contact_counter import *
from chain_circuit_counter import RingBuilder
from circuit_field_counter import evaluate_circuit
from live_circuit_anf import circuit_to_cubic_live
from field_kloosterman import gf_trace
import random


def circuit_from_contact(case):
    n=case['original_variables'];b=case['planted_module_rank']
    R=ChainRing(case['planted_field_modulus'],case['planted_chain_length'])
    builder=RingBuilder(n);columns=case['planted_binary_columns'];offset=case['planted_binary_offset']
    y=[builder.xor([i for i in range(n) if columns[i]>>j&1]+([builder.one] if offset>>j&1 else []))
       for j in range(n)]
    variables=[y[R.m*i:R.m*(i+1)] for i in range(b)]
    zero=(0,)*b;cache={zero:[builder.one]+[builder.zero]*(R.m-1)}
    for i in range(b):
        cache[tuple(int(j==i) for j in range(b))]=variables[i]
        # Frobenius squaring is an exact binary-linear circuit.
        square=[[] for _ in range(R.m)]
        for bit in range(R.m):
            for out in bits(R.mul(1<<bit,1<<bit)):square[out].append(variables[i][bit])
        cache[tuple(2*int(j==i) for j in range(b))]=[builder.xor(row) for row in square]
    def monomial(exponent):
        exponent=tuple(exponent)
        if exponent not in cache:
            i=next(j for j in range(b) if exponent[j]);lower=list(exponent);lower[i]-=1
            cache[exponent]=builder.ring_mul(monomial(lower),variables[i],R)
        return cache[exponent]
    total=builder.ring_add([builder.ring_scale(monomial(row['exponents']),row['coefficient'],R)
                           for row in case['planted_polynomial']],R)
    terms=[total[R.d*(R.e-1)+i] for i in range(R.d) if gf_trace(1<<i,R.h)]
    if case['seed']&1:terms.append(builder.one)
    factors=case['planted_error_factors']
    for u,v in zip(factors[::2],factors[1::2]):
        terms.append(builder.gate('AND',builder.xor(y[i] for i in bits(u)),builder.xor(y[i] for i in bits(v))))
    return dict(n=n,gates=builder.gates,output=builder.xor(terms))


def count_contact_circuit(circuit,*,term_budget=None,terminal_bit_budget=24):
    started=time.perf_counter();poly,front=circuit_to_cubic_live(circuit,term_budget=term_budget)
    result=compile_contact(poly,circuit['n'],terminal_bit_budget=terminal_bit_budget)
    result.update(gate_compilation=front,complete_seconds=time.perf_counter()-started)
    return result,poly


def validation():
    case=next(c for c in json.loads(Path(__file__).with_name('contact_counter_results.json').read_text())['raw_cases']
              if c['module_dimension']==9)
    circuit=circuit_from_contact(case);path=Path(__file__).with_name('contact_72_bit_circuit.json')
    path.write_text(json.dumps(circuit,separators=(',',':'))+'\n')
    print(json.dumps(dict(stage='compile actual contact gate program',n=72,gates=len(circuit['gates']))),flush=True)
    result,poly=count_contact_circuit(circuit)
    raw=json.loads(Path(__file__).with_name(case['raw_input_file']).read_text())
    assert poly==set(raw['polynomial']) and result['signed_count']==case['signed_count']
    rng=random.Random(726292)
    for _ in range(1024):
        x=rng.randrange(1<<72);assert evaluate_circuit(circuit,x)==polynomial_value(poly,x)
    result.update(exact_raw_coefficient_identity=True,original_input_checks=1024,
        circuit_file=path.name,description_bytes=path.stat().st_size,practical_speed_claim=False)
    Path(__file__).with_name('contact_circuit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['original_variables','signed_count','zero_count',
        'gate_compilation','complete_seconds']}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path,nargs='?')
    parser.add_argument('--output',type=Path);parser.add_argument('--term-budget',type=int)
    parser.add_argument('--terminal-bit-budget',type=int,default=24);args=parser.parse_args()
    if args.input:
        result,_=count_contact_circuit(json.loads(args.input.read_text()),term_budget=args.term_budget,
                                       terminal_bit_budget=args.terminal_bit_budget)
        text=json.dumps(result,indent=2)+'\n'
        if args.output:args.output.write_text(text)
        else:print(text,end='')
    else:validation()
