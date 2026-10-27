#!/usr/bin/env python3
"""Exact checks for circuit residual coordinates. No asymptotic solver is claimed."""
from itertools import product
from random import Random
from pathlib import Path
import json

def rank2(rows):
    basis={}
    for row in rows:
        while row:
            b=row.bit_length()-1
            if b in basis: row ^= basis[b]
            else:
                basis[b]=row
                break
    return len(basis)

def gate_value(op, a, b):
    return {"AND":a&b,"OR":a|b,"XOR":a^b,"NAND":1-(a&b)}[op]

def trace_from_error(x, gates, errors):
    values=list(x)
    for i,(op,a,b) in enumerate(gates):
        values.append(gate_value(op,values[a],values[b]) ^ ((errors>>i)&1))
    return tuple(values[len(x):])

def error_from_trace(x, gates, trace):
    values=list(x)+list(trace)
    return sum((values[len(x)+i]^gate_value(op,values[a],values[b]))<<i
               for i,(op,a,b) in enumerate(gates))

def anf_degree(values, variables):
    coeff=list(values)
    for i in range(variables):
        for mask in range(1<<variables):
            if mask&(1<<i): coeff[mask]^=coeff[mask^(1<<i)]
    return max((m.bit_count() for m,c in enumerate(coeff) if c),default=-1),coeff

def run():
    rng=Random(20261027)
    cases=[]
    point_checks=0
    for n in range(1,5):
        for s in range(1,9):
            gates=[]
            for i in range(s):
                gates.append((rng.choice(["AND","OR","XOR","NAND"]),
                              rng.randrange(n+i),rng.randrange(n+i)))
            rows=[rng.randrange(1<<s) for _ in range(rng.randrange(s+2))]
            r=rank2(rows)
            per_input=[]
            for x in product((0,1), repeat=n):
                seen=set()
                accepted=0
                for e in range(1<<s):
                    y=trace_from_error(x,gates,e)
                    assert error_from_trace(x,gates,y)==e
                    seen.add(y)
                    point_checks+=1
                    if all((a&e).bit_count()%2==0 for a in rows): accepted+=1
                assert len(seen)==1<<s
                assert accepted==1<<(s-r)
                per_input.append(accepted)
            assert sum(per_input)==1<<(n+s-r)
            degree,coeff=anf_degree([int(e==0) for e in range(1<<s)],s)
            assert degree==s and all(coeff)
            cases.append({"n":n,"gates":s,"rank":r,"accepted_traces":sum(per_input),
                          "zero_selector_degree":degree})
    code=[e for e in range(4) if ((3&e).bit_count()%2)==0]
    false_output=sum((e>>1)&1 for e in code)
    assert code==[0,3] and false_output==1
    result={"status":"all exact assertions passed","circuit_cases":len(cases),
            "bijection_points_checked":point_checks,"cases":cases,
            "nonzero_residual_counterexample":{"code":code,"original_output_count":0,
                                                "filtered_output_count":false_output},
            "scope":"Finite checks of proved residual bijection and degree obstruction; not a speed benchmark."}
    Path(__file__).with_name("residual_fiber_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="cases"},indent=2))

if __name__=="__main__": run()
