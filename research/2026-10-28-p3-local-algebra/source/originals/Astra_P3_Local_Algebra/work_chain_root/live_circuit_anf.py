#!/usr/bin/env python3
"""Exact pure-Boolean gate propagation with reachability and wire liveness.

Dead gates are still syntax-validated. No polynomial is truncated. Fanout and
the exact original independent-input count are preserved.
"""
import math


def circuit_to_cubic_live(circuit,*,term_budget=None):
    n=circuit['n'];gates=circuit['gates'];output=circuit['output'];total=n+len(gates)
    if not isinstance(n,int) or n<1:raise ValueError('invalid independent input count')
    if not isinstance(output,int) or not 0<=output<total:raise ValueError('invalid output wire')
    if term_budget is None:term_budget=sum(math.comb(n,i) for i in range(min(n,3)+1))
    if not isinstance(term_budget,int) or term_budget<1:raise ValueError('invalid ANF term budget')
    dependencies=[[] for _ in range(total)];counts={}
    for index,gate in enumerate(gates):
        wire=n+index
        if not isinstance(gate,list) or not gate:raise ValueError('invalid gate')
        op=gate[0];counts[op]=counts.get(op,0)+1
        if op=='CONST':
            if len(gate)!=2 or gate[1] not in (0,1):raise ValueError('invalid constant')
        else:
            arity={'XOR':2,'AND':2,'NOT':1}.get(op)
            if arity is None or len(gate)!=arity+1 or any(not isinstance(j,int) or not 0<=j<wire for j in gate[1:]):
                raise ValueError('invalid gate or noncausal reference')
            dependencies[wire]=gate[1:]
    needed=[False]*total;stack=[output]
    while stack:
        wire=stack.pop()
        if needed[wire]:continue
        needed[wire]=True;stack.extend(dependencies[wire])
    remaining=[0]*total;remaining[output]=1
    for wire in range(n,total):
        if needed[wire]:
            for j in dependencies[wire]:remaining[j]+=1
    polys=[None]*total;live_terms=0;live_wires=0
    for i in range(n):
        if needed[i]:polys[i]=frozenset([1<<i]);live_terms+=1;live_wires+=1
    peak_terms=live_terms;peak_wires=live_wires;maximum=1;max_degree=1;evaluated=0
    for index,gate in enumerate(gates):
        wire=n+index
        if not needed[wire]:continue
        evaluated+=1;op=gate[0]
        if op=='CONST':result=frozenset([0]) if gate[1] else frozenset()
        else:
            a=polys[gate[1]]
            if a is None:raise AssertionError('consumed a released wire')
            if op=='NOT':result=a^frozenset([0])
            else:
                b=polys[gate[2]]
                if b is None:raise AssertionError('consumed a released wire')
                if op=='XOR':result=a^b
                elif gate[1]==gate[2]:result=a
                else:
                    products=set()
                    for x in a:
                        for y in b:
                            term=x|y
                            if term in products:products.remove(term)
                            else:products.add(term)
                    result=frozenset(products)
        if len(result)>term_budget:raise ValueError('exact intermediate ANF budget exceeded at wire '+str(wire))
        maximum=max(maximum,len(result));max_degree=max(max_degree,max((m.bit_count() for m in result),default=0))
        polys[wire]=result;live_terms+=len(result);live_wires+=1
        peak_terms=max(peak_terms,live_terms);peak_wires=max(peak_wires,live_wires)
        for j in dependencies[wire]:
            remaining[j]-=1
            if not remaining[j]:
                live_terms-=len(polys[j]);live_wires-=1;polys[j]=None
    result=polys[output]
    if result is None:raise AssertionError('output was released')
    if any(term.bit_count()>3 for term in result):raise ValueError('exact output degree exceeds three')
    return set(result),dict(independent_inputs=n,internal_gates=len(gates),
        evaluated_gates=evaluated,unreachable_gates=len(gates)-evaluated,gate_types=counts,
        maximum_intermediate_anf_terms=maximum,maximum_intermediate_degree=max_degree,
        peak_live_anf_terms=peak_terms,peak_live_wires=peak_wires,anf_term_budget=term_budget,
        degree_certificate='all output ancestors computed exactly; all gates syntax-validated; final degree verified',
        output_anf_terms=len(result),liveness_derived_from_all_references=True)
