#!/usr/bin/env python3
"""Exact finite phase-product, raw-program and IQP-prefix checks.

The leaf sums are exhaustive. This validates identities, not a speed claim.
"""
import itertools
import json
import random
from pathlib import Path


def root_vector(exponent, q):
    d = q//2
    exponent %= q
    z = [0]*d
    z[exponent % d] = 1 if exponent < d else -1
    return z


def add(a,b,mod=None):
    z = [x+y for x,y in zip(a,b)]
    return z if mod is None else [x%mod for x in z]


def mul(a,b,mod=None):
    d = len(a)
    z = [0]*d
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            t = i+j
            z[t%d] += x*y*(1 if t<d else -1)
    return z if mod is None else [x%mod for x in z]


def conjugate(a):
    d = len(a)
    z = [0]*d
    z[0] = a[0]
    for i in range(1,d):
        z[d-i] = -a[i]
    return z


def gate_phase(gate,x):
    mask = sum(x[v]<<j for j,v in enumerate(gate['support']))
    return gate['table'][mask]


def exact_phase_sum(n,q,gates):
    z = [0]*(q//2)
    for x in itertools.product((0,1),repeat=n):
        z = add(z,root_vector(sum(gate_phase(g,x) for g in gates),q))
    return z


def truncated_phase_sum(n,q,gates):
    p = n+2
    ell = (q//2)*p
    modulus = 1<<p
    d = q//2
    total = [0]*d
    max_discarded_residue = 0
    for x in itertools.product((0,1),repeat=n):
        coeff = [[0]*d for _ in range(ell)]
        coeff[0][0] = 1
        for j,g in enumerate(gates):
            delta = root_vector(gate_phase(g,x),q)
            delta[0] -= 1
            for t in range(min(j+1,ell-1),0,-1):
                coeff[t] = add(coeff[t],mul(coeff[t-1],delta,modulus),modulus)
        value = [0]*d
        for c in coeff:
            value = add(value,c,modulus)
        total = add(total,value,modulus)
    centered = [v if v < modulus//2 else v-modulus for v in total]
    return centered


def prefix_program(n,q,gates,a,z):
    # A is the first a input/output coordinates; B is shared.
    result = []
    for g in gates:
        result.append(dict(support=list(g['support']),table=list(g['table'])))
        support = [n+v if v<a else v for v in g['support']]
        result.append(dict(support=support,table=[(-c)%q for c in g['table']]))
    for v in range(a):
        if z>>v & 1:
            result.append(dict(support=[v],table=[0,q//2]))
            result.append(dict(support=[n+v],table=[0,q//2]))
    return n+a,result


def compile_program(n,q,gates,k):
    polys = [{frozenset([i]):1} for i in range(n)]
    degrees = [1]*n
    for g in gates:
        op = g['op']
        if op == 'const':
            poly = {frozenset():g['value']%q}
            degree = 0
        elif op == 'add':
            degree = max(degrees[v] for v in g['args'])
            poly = {}
            for v in g['args']:
                for s,c in polys[v].items():
                    poly[s] = (poly.get(s,0)+c)%q
        elif op == 'mul':
            u,v = g['args']
            degree = degrees[u]+degrees[v]
            poly = {}
            for s,c in polys[u].items():
                for t,e in polys[v].items():
                    st = s|t
                    poly[st] = (poly.get(st,0)+c*e)%q
        else:
            raise ValueError(op)
        assert degree<=k
        polys.append({s:c for s,c in poly.items() if c})
        degrees.append(degree)
    return polys[-1]


def eval_program(x,q,gates):
    values = list(x)
    for g in gates:
        if g['op']=='const':
            value=g['value']
        elif g['op']=='add':
            value=sum(values[v] for v in g['args'])
        else:
            u,v=g['args']
            value=values[u]*values[v]
        values.append(value%q)
    return values[-1]


def polynomial_phase_gates(poly,q,scale=1):
    gates=[]
    for support,c in poly.items():
        c=c*scale%q
        if not c:
            continue
        support=sorted(support)
        table=[0]*(1<<len(support))
        table[-1]=c
        gates.append(dict(support=support,table=table))
    return gates


def main():
    rng=random.Random(20261027)
    truncation=[]
    for q in (2,4,8):
        for n in range(1,6):
            for trial in range(2):
                # Force the number of factors above the truncation order.
                m=(q//2)*(n+2)+7+trial
                gates=[]
                for _ in range(m):
                    support=sorted(rng.sample(range(n),rng.randint(0,min(3,n))))
                    gates.append(dict(support=support,
                                      table=[rng.randrange(q) for _ in range(1<<len(support))]))
                direct=exact_phase_sum(n,q,gates)
                restored=truncated_phase_sum(n,q,gates)
                assert direct==restored,(n,q,trial,direct,restored)
                truncation.append(dict(n=n,root_order=q,gates=m,
                                       truncation_order=(q//2)*(n+2),sum=direct))
    raw=[]
    for q in (2,4,8):
        for n in (3,4,5):
            for trial in range(2):
                k=3
                gates=[]
                degrees=[1]*n
                for j in range(28):
                    pairs=[(u,v) for u in range(n+j) for v in range(n+j)
                           if degrees[u]+degrees[v]<=k]
                    if pairs and rng.random()<0.4:
                        u,v=rng.choice(pairs)
                        gates.append(dict(op='mul',args=[u,v]))
                        degrees.append(degrees[u]+degrees[v])
                    else:
                        args=rng.sample(range(n+j),rng.randint(1,min(4,n+j)))
                        gates.append(dict(op='add',args=args))
                        degrees.append(max(degrees[u] for u in args))
                poly=compile_program(n,q,gates,k)
                counts=[0]*q
                for x in itertools.product((0,1),repeat=n):
                    value=eval_program(x,q,gates)
                    expanded=sum(c for s,c in poly.items() if all(x[v] for v in s))%q
                    assert value==expanded
                    counts[value]+=1
                character_sums=[truncated_phase_sum(n,q,polynomial_phase_gates(poly,q,a))
                                for a in range(q)]
                for target in range(q):
                    filtered=[0]*(q//2)
                    for a,z in enumerate(character_sums):
                        filtered=add(filtered,mul(root_vector(-a*target,q),z))
                    assert filtered==[q*counts[target]]+[0]*(q//2-1)
                raw.append(dict(n=n,root_order=q,states=len(gates),
                                discovered_monomials=len(poly),output_counts=counts))
    multiple_outputs=[]
    for q in (2,4,8):
        b=q.bit_length()-1
        for n in (3,4):
            # Two raw low-degree outputs, with overlapping original supports.
            program=[dict(op='mul',args=[0,1]),
                     dict(op='add',args=[n,2]),
                     dict(op='mul',args=[1,2]),
                     dict(op='add',args=[n+2,0])]
            polys=[compile_program(n,q,program[:2],2),
                   compile_program(n,q,program,2)]
            target=[rng.randrange(q),rng.randrange(q)]
            if n==3:
                target=[sum(poly.values())%q for poly in polys]
            desired=0
            for x in itertools.product((0,1),repeat=n):
                values=[sum(c for s,c in poly.items() if all(x[v] for v in s))%q
                        for poly in polys]
                desired+=int(values==target)
            phase_gates=[]
            for i,poly in enumerate(polys):
                for h in range(b):
                    v=n+i*b+h
                    for support,c in poly.items():
                        st=sorted(support|{v})
                        table=[0]*(1<<len(st))
                        table[-1]=(c*(1<<h))%q
                        phase_gates.append(dict(support=st,table=table))
                    phase_gates.append(dict(support=[v],table=[0,(-target[i]*(1<<h))%q]))
            np=n+2*b
            z=exact_phase_sum(np,q,phase_gates)
            assert z==[q*q*desired]+[0]*(q//2-1)
            if q<=4:
                assert truncated_phase_sum(np,q,phase_gates)==z
            multiple_outputs.append(dict(n=n,root_order=q,outputs=2,character_bits=2*b,
                                         target=target,preimage_count=desired,phase_sum=z))
    prefixes=[]
    for q in (2,4,8):
        for n in range(1,5):
            gates=[]
            for _ in range(3*n+4):
                support=sorted(rng.sample(range(n),rng.randint(1,min(3,n))))
                gates.append(dict(support=support,
                                  table=[rng.randrange(q) for _ in range(1<<len(support))]))
            numerators=[]
            for y in range(1<<n):
                phases=list(gates)+[dict(support=[v],table=[0,q//2])
                                    for v in range(n) if y>>v&1]
                z=exact_phase_sum(n,q,phases)
                numerators.append(mul(z,conjugate(z)))
            for a in range(n+1):
                for target in range(1<<a):
                    left=[0]*(q//2)
                    for y in range(1<<n):
                        if y% (1<<a)==target:
                            left=add(left,numerators[y])
                    np,pg=prefix_program(n,q,gates,a,target)
                    phase=exact_phase_sum(np,q,pg)
                    right=[(1<<(n-a))*v for v in phase]
                    assert left==right,(n,q,a,target,left,right)
                    prefixes.append(dict(n=n,root_order=q,prefix_length=a,target=target,
                                         phase_sum=phase))
    out=dict(status='all assertions passed',
             method='Exact cyclotomic integer vectors; exhaustive input sums',
             truncation_cases=len(truncation),raw_program_cases=len(raw),
             multiple_output_cases=len(multiple_outputs),prefix_cases=len(prefixes),
             truncation=truncation,raw_programs=raw,multiple_outputs=multiple_outputs,prefixes=prefixes,
             limitation='The asymptotic replacement solver is not implemented or benchmarked.')
    Path(__file__).with_name('phase_product_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('truncation','raw_programs','multiple_outputs','prefixes')},indent=2))


if __name__=='__main__':
    main()
