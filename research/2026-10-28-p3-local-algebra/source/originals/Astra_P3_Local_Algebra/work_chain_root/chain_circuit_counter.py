#!/usr/bin/env python3
"""Exact symbolic gate front end for the acquired chain counter."""
from acquired_chain_counter import *
from circuit_field_counter import Builder,circuit_to_cubic,evaluate_circuit
from field_kloosterman import gf_trace
import random

class RingBuilder(Builder):
    def ring_add(self,words,R):return self.word_add(words,R.m)
    def ring_mul(self,a,b,R):
        out=[]
        for k in range(R.e):
            words=[self.word_mul(a[R.d*i:R.d*(i+1)],b[R.d*(k-i):R.d*(k-i+1)],R.h)
                   for i in range(k+1)]
            out.extend(self.word_add(words,R.d))
        return out
    def ring_scale(self,a,c,R):
        out=[]
        for k in range(R.e):
            words=[self.word_scale(a[R.d*i:R.d*(i+1)],(c>>(R.d*(k-i)))&R.mask,R.h)
                   for i in range(k+1)]
            out.extend(self.word_add(words,R.d))
        return out

def circuit_from_case(case):
    n=case['original_variables'];R=ChainRing(case['h'],case['e']);builder=RingBuilder(n)
    columns=case['planted_binary_columns'];offset=case['planted_binary_offset']
    y=[builder.xor([i for i in range(n) if columns[i]>>j&1]+([builder.one] if offset>>j&1 else []))
       for j in range(n)]
    X,Y,Z=[y[R.m*i:R.m*(i+1)] for i in range(3)]
    XY=builder.ring_mul(X,Y,R);XZ=builder.ring_mul(X,Z,R);YZ=builder.ring_mul(Y,Z,R)
    XYZ=builder.ring_mul(XY,Z,R)
    monomials={(1,1,1):XYZ,(1,1,0):XY,(1,0,1):XZ,(0,1,1):YZ,
        (1,0,0):X,(0,1,0):Y,(0,0,1):Z,(0,0,0):[builder.one]+[builder.zero]*(R.m-1)}
    total=builder.ring_add([builder.ring_scale(monomials[tuple(t['exponents'])],t['coefficient'],R)
                            for t in case['planted_polynomial']],R)
    terms=[total[R.d*(R.e-1)+i] for i in range(R.d) if gf_trace(1<<i,R.h)]
    factors=case['planted_error_factors']
    for a,b in zip(factors[::2],factors[1::2]):
        terms.append(builder.gate('AND',builder.xor(y[i] for i in bits(a)),builder.xor(y[i] for i in bits(b))))
    return dict(n=n,gates=builder.gates,output=builder.xor(terms))

def count_circuit(circuit,*,term_budget=None,error_decoder='auto'):
    start=time.perf_counter();poly,certificate=circuit_to_cubic(circuit,term_budget=term_budget)
    result=compile_chain(poly,circuit['n'],error_decoder=error_decoder)
    result.update(gate_compilation=certificate,complete_seconds=time.perf_counter()-start)
    return result,poly

def validation():
    cases=json.loads(Path(__file__).with_name('chain_counter_results.json').read_text())['cases']
    source=next(c for c in cases if c['original_variables']==42)
    circuit=circuit_from_case(source)
    path=Path(__file__).with_name('example_42_bit_chain_circuit.json')
    path.write_text(json.dumps(circuit,separators=(',',':'))+'\n')
    print(json.dumps(dict(stage='compile actual ring gate program',n=42,gates=len(circuit['gates']))),flush=True)
    result,poly=count_circuit(circuit)
    assert poly==set(source['raw_polynomial']) and result['signed_count']==source['signed_count']
    rng=random.Random(456734)
    for _ in range(1024):
        x=rng.randrange(1<<42)
        assert evaluate_circuit(circuit,x)==polynomial_value(poly,x)
    result.update(exact_raw_coefficient_identity=True,original_input_checks=1024,
                  circuit_file=path.name,description_bytes=path.stat().st_size,practical_speed_claim=False)
    Path(__file__).with_name('chain_circuit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['original_variables','signed_count','zero_count','gate_compilation','complete_seconds']}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path,nargs='?')
    parser.add_argument('--output',type=Path);parser.add_argument('--term-budget',type=int)
    parser.add_argument('--error-decoder',choices=['auto','gabidulin','sylvester','nilpotent'],default='auto')
    args=parser.parse_args()
    if args.input:
        data,_=count_circuit(json.loads(args.input.read_text()),term_budget=args.term_budget,error_decoder=args.error_decoder)
        text=json.dumps(data,indent=2)+'\n'
        if args.output:args.output.write_text(text)
        else:print(text,end='')
    else:validation()
