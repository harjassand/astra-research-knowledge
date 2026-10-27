#!/usr/bin/env python3
"""Exact checks for the causal-kernel and triangular-replacement obstructions.
Standard library only, including exact rational matrix rank.
No timing or asymptotic speed claim is made.
"""
from fractions import Fraction as F
from itertools import product
import json
import random
from pathlib import Path


def evaluate_circuit(bits, gates):
    values = list(bits)
    for op, a, b in gates:
        u, v = values[a], values[b]
        if op == 'and': z = u & v
        elif op == 'or': z = u | v
        elif op == 'xor': z = u ^ v
        elif op == 'nand': z = 1 - (u & v)
        else: raise ValueError(op)
        values.append(z)
    return values[-1]


def kernel(y, p):
    return p if y else 1-p


def deformed_count(m, gates, t):
    a = 1-F(t, 2)
    ans = F(0)
    # Only x is an original independent input. All y coordinates are gate states.
    for x in (0, 1):
        for y in product((0, 1), repeat=m):
            weight = F(1)
            for bit in y:
                weight *= kernel(bit, a*x)
            ans += weight * evaluate_circuit(y, gates)
    return ans


def random_fixture(m, rng):
    gates = []
    for j in range(2*m+1):
        available = m+j
        gates.append((rng.choice(('and', 'or', 'xor', 'nand')),
                      rng.randrange(available), rng.randrange(available)))
    return gates


def causal_checks():
    rng = random.Random(1077)
    rows=[]
    for m in range(2, 10):
        for k in range(6):
            gates = random_fixture(m, rng)
            count = sum(evaluate_circuit(y, gates) for y in product((0,1),repeat=m))
            zero = evaluate_circuit((0,)*m, gates)
            one = evaluate_circuit((1,)*m, gates)
            h0 = deformed_count(m, gates, 0)
            h1 = deformed_count(m, gates, 1)
            h2 = deformed_count(m, gates, 2)
            assert h0 == zero+one
            assert h1 == zero+F(count, 2**m)
            assert h2 == 2*zero
            # Normalization including negative signed transition probabilities.
            for t in (0,1,2,3,4):
                for x in (0,1):
                    p=(1-F(t,2))*x
                    assert kernel(0,p)+kernel(1,p)==1
            rows.append({'m':m,'fixture':k,'G_count':count,
                         'H0':str(h0),'H1':str(h1),'H2':str(h2)})
    return rows


def matrix_rank(a):
    a = [[F(v) for v in row] for row in a]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank,len(a)) if a[i][col]),None)
        if pivot is None: continue
        a[rank],a[pivot]=a[pivot],a[rank]
        scale=a[rank][col]
        a[rank]=[v/scale for v in a[rank]]
        for i in range(rank+1,len(a)):
            scale=a[i][col]
            if scale:
                a[i]=[v-scale*w for v,w in zip(a[i],a[rank])]
        rank+=1
    return rank


def triangular_check():
    Q,R,r=3,2,2
    labels=list(product(range(r),repeat=2*Q))
    positions={u:i for i,u in enumerate(labels)}
    D=len(labels)
    # M=V*(I-2W)=V*((1-Q)I+sum_s Pi_s).
    M=[[0]*D for _ in range(D)]
    for i,u in enumerate(labels):
        v=list(u[Q:]+u[:Q])
        M[i][positions[tuple(v)]]+=1-Q
        for s in range(Q):
            w=v[:]
            w[s],w[Q+s]=w[Q+s],w[s]
            M[i][positions[tuple(w)]]+=1
    def mismatch(u,v):
        return sum(v[s]!=u[Q+s] for s in range(Q))
    bad=[i for i,u in enumerate(labels) if mismatch(u,u)>=R]
    support_violations=[]
    for i,u in enumerate(labels):
        for j,v in enumerate(labels):
            if M[i][j]!=0 and mismatch(u,v)>=R:
                support_violations.append((i,j))
    assert not support_violations
    actual_rank=matrix_rank([[int(i==j)-M[i][j] for j in range(D)]
                            for i in range(D)])
    assert actual_rank==10
    assert len(bad)==32
    # Diagonal T with T_ii=0 on bad rows, 1 otherwise attains the bound.
    causal_rank=len(bad)
    return {'Q':Q,'R':R,'r':r,'D':D,'bad_diagonal_rows':len(bad),
            'noncausal_measurement_rank':actual_rank,
            'minimum_triangular_rank_by_proved_bound':len(bad),
            'attained_diagonal_rank':causal_rank,
            'support_violations':len(support_violations)}


def main():
    checks=causal_checks()
    result={'causal_fixtures_passed':len(checks),'causal_checks':checks,
            'triangular_fixture':triangular_check()}
    out=Path(__file__).with_name('causal_obstructions_results.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'causal_fixtures_passed':len(checks),
                      'triangular_fixture':result['triangular_fixture']},indent=2))

if __name__=='__main__': main()
