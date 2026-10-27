#!/usr/bin/env python3
"""Exact bounded-size symbolic gate compiler feeding the acquired field counter.

Input: n independent bits, topologically ordered CONST/XOR/AND/NOT gates,
output wire. Internal wires are never introduced as independent inputs.
High-degree sparse intermediate states are allowed. A term budget is checked
after exact cancellation at each gate; only the output must be cubic.
The compiler never silently truncates polynomials.
"""
import argparse,json,math,random,time
from pathlib import Path
from field_rank_decoder import *


def circuit_to_cubic(circuit,*,term_budget=None):
    n=circuit['n']; gates=circuit['gates']; output=circuit['output']
    if not isinstance(n,int) or n<1: raise ValueError('invalid independent input count')
    if term_budget is None: term_budget=sum(math.comb(n,i) for i in range(min(n,3)+1))
    if not isinstance(term_budget,int) or term_budget<1: raise ValueError('invalid ANF term budget')
    polys=[frozenset([1<<i]) for i in range(n)]
    maximum=1; maximum_degree=1; counts={}
    for index,gate in enumerate(gates):
        wire=n+index; op=gate[0]; counts[op]=counts.get(op,0)+1
        if op=='CONST':
            if len(gate)!=2 or gate[1] not in (0,1): raise ValueError('invalid constant gate')
            result=frozenset([0]) if gate[1] else frozenset()
        else:
            arity={'NOT':1,'XOR':2,'AND':2}.get(op)
            if arity is None or len(gate)!=arity+1 or any(not isinstance(j,int) or not 0<=j<wire for j in gate[1:]):
                raise ValueError('invalid gate or noncausal wire reference')
            a=polys[gate[1]]
            if op=='NOT': result=a^frozenset([0])
            else:
                b=polys[gate[2]]
                if op=='XOR': result=a^b
                else:
                    products=sorted(x|y for x in a for y in b)
                    surviving=[]; at=0
                    while at<len(products):
                        end=at+1
                        while end<len(products) and products[end]==products[at]:end+=1
                        if (end-at)&1:surviving.append(products[at])
                        at=end
                    if len(surviving)>term_budget:
                        raise ValueError('exact intermediate ANF term budget exceeded at wire '+str(wire))
                    result=frozenset(surviving)
        if len(result)>term_budget:
            raise ValueError('exact intermediate ANF term budget exceeded at wire '+str(wire))
        maximum_degree=max(maximum_degree,max((mask.bit_count() for mask in result),default=0))
        maximum=max(maximum,len(result)); polys.append(result)
    if not isinstance(output,int) or not 0<=output<len(polys): raise ValueError('invalid output wire')
    if any(mask.bit_count()>3 for mask in polys[output]):
        raise ValueError('exact output Boolean degree exceeds three')
    return set(polys[output]),dict(independent_inputs=n,internal_gates=len(gates),
        maximum_intermediate_anf_terms=maximum,gate_types=counts,
        maximum_intermediate_degree=maximum_degree,anf_term_budget=term_budget,
        degree_certificate='every gate computed exactly; final cubic degree verified',
        output_anf_terms=len(polys[output]))


def evaluate_circuit(circuit,x):
    values=[(x>>i)&1 for i in range(circuit['n'])]
    for gate in circuit['gates']:
        op=gate[0]
        if op=='CONST':z=gate[1]
        elif op=='NOT':z=1^values[gate[1]]
        elif op=='XOR':z=values[gate[1]]^values[gate[2]]
        elif op=='AND':z=values[gate[1]]&values[gate[2]]
        else:raise ValueError(op)
        values.append(z)
    return values[circuit['output']]


def count_circuit(circuit,*,term_budget=None):
    start=time.perf_counter(); poly,certificate=circuit_to_cubic(circuit,term_budget=term_budget)
    result=compile_rank_perturbed(poly,circuit['n'])
    result['gate_compilation']=certificate; result['complete_seconds']=time.perf_counter()-start
    return result


class Builder:
    def __init__(self,n):
        self.n=n; self.gates=[]; self.zero=self.gate('CONST',0); self.one=self.gate('CONST',1)
    def gate(self,op,*args):
        wire=self.n+len(self.gates);self.gates.append([op,*args]);return wire
    def xor(self,terms):
        terms=list(terms)
        if not terms:return self.zero
        out=terms[0]
        for term in terms[1:]:out=self.gate('XOR',out,term)
        return out
    def word_add(self,words,d):return [self.xor(word[i] for word in words) for i in range(d)]
    def word_scale(self,a,c,h):
        d=len(a); images=[gf_mul(1<<j,c,h) for j in range(d)]
        return [self.xor(a[j] for j in range(d) if images[j]>>i&1) for i in range(d)]
    def word_mul(self,a,b,h):
        d=len(a); terms=[[] for _ in range(d)]
        for i in range(d):
            for j in range(d):
                wire=self.gate('AND',a[i],b[j]); target=gf_mul(1<<i,1<<j,h)
                for k in bits(target):terms[k].append(wire)
        return [self.xor(t) for t in terms]


def fixture_from_saved(case):
    """Generate a gate-only fixture from a separately preserved planted model."""
    n=case['original_variables']; h=case['planted_modulus'];d=h.bit_length()-1
    builder=Builder(n); disguise=case['planted_affine_columns'];offset=case['planted_affine_offset']
    y=[builder.xor([i for i in range(n) if disguise[i]>>j&1]+([builder.one] if offset>>j&1 else [])) for j in range(n)]
    X,Y,Z=[y[d*i:d*(i+1)] for i in range(3)]
    XY=builder.word_mul(X,Y,h); XZ=builder.word_mul(X,Z,h); YZ=builder.word_mul(Y,Z,h)
    XYZ=builder.word_mul(XY,Z,h)
    monomials={(1,1,1):XYZ,(1,1,0):XY,(1,0,1):XZ,(0,1,1):YZ,
        (1,0,0):X,(0,1,0):Y,(0,0,1):Z,(0,0,0):[builder.one]+[builder.zero]*(d-1)}
    words=[builder.word_scale(monomials[tuple(t['exponents'])],t['coefficient'],h) for t in case['planted_polynomial']]
    total=builder.word_add(words,d)
    out=builder.xor(total[i] for i in range(d) if gf_trace(1<<i,h))
    forms,linear=symplectic_factors(case['planted_defect'])
    error=[]
    for a,b in zip(forms[::2],forms[1::2]):
        ua=builder.xor(bits(a));ub=builder.xor(bits(b));error.append(builder.gate('AND',ua,ub))
    error.append(builder.xor(bits(linear)));out=builder.xor([out]+error)
    return dict(n=n,gates=builder.gates,output=out)


def validation():
    source=json.loads(Path(__file__).with_name('field_rank_results.json').read_text())['cases']
    results=[]
    for case in [source[0],source[-1]]:
        circuit=fixture_from_saved(case); n=circuit['n']
        print(json.dumps(dict(stage='count_gate_program',n=n,gates=len(circuit['gates']))),flush=True)
        result=count_circuit(circuit)
        assert set(result['raw_polynomial'])==set(case['raw_polynomial'])
        assert result['signed_count']==case['signed_count']
        rng=random.Random(n+902)
        for _ in range(1024):
            x=rng.randrange(1<<n)
            assert evaluate_circuit(circuit,x)==polynomial_value(result['raw_polynomial'],x)
        input_file=Path(__file__).with_name('example_'+str(n)+'_bit_circuit.json')
        input_file.write_text(json.dumps(circuit,separators=(',',':'))+'\n')
        result.update(circuit_input_file=input_file.name,exact_raw_coefficient_identity=True,
            original_coordinate_checks=1024,explicit_circuit_description_bytes=input_file.stat().st_size)
        results.append(result)
        print(json.dumps({k:result[k] for k in ['original_variables','acquired_defect_rank','signed_count','complete_seconds','gate_compilation']}),flush=True)
    return dict(status='all exact assertions passed',cases=results,
        statement='gate propagation is established machinery; the acquired field-counting interface supplies the class-specific bound')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path,nargs='?');parser.add_argument('--output',type=Path)
    parser.add_argument('--term-budget',type=int)
    args=parser.parse_args()
    if args.input:
        data=count_circuit(json.loads(args.input.read_text()),term_budget=args.term_budget)
        text=json.dumps(data,indent=2)+'\n'
        if args.output:args.output.write_text(text)
        else:print(text,end='')
    else:
        data=validation();Path(__file__).with_name('circuit_field_results.json').write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps(dict(status=data['status'],cases=len(data['cases']))))
