#!/usr/bin/env python3
"""Executed universality and Fourier-support boundary for constrained leaves.
Small fixtures alone search for an irreducible polynomial by trial; the
polynomial-time theorem uses Shoup's deterministic fixed-characteristic
construction, not this convenience fixture generator.
"""
from pathlib import Path
import sys,json,random,itertools
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'work_field_root'))
from field_kloosterman import gf_mul,gf_trace,irreducible_binary
from field_descent import solve,nullspace_rows,polynomial_value,span


def fixture_modulus(d):
    for low in range(1,1<<d,2):
        h=(1<<d)|low
        if irreducible_binary(h): return h
    raise AssertionError('irreducible polynomial missing')


def parity_embedding(poly,m,h):
    d=h.bit_length()-1
    if d<m*m or not irreducible_binary(h): raise ValueError('need a field of degree at least m squared')
    if any(not mask or mask>>m or mask.bit_count()>3 for mask in poly):
        raise ValueError('zero-constant cubic ANF required')
    A=[1<<i for i in range(m)]; B=[1<<(m*j) for j in range(m)]
    # All A_i B_j are the distinct basis monomials alpha^(i+m*j).
    products=[gf_mul(A[i],B[j],h) for j in range(m) for i in range(m)]
    assert products==[1<<k for k in range(m*m)]
    trace_columns=[sum(gf_trace(gf_mul(v,1<<bit,h),h)<<k for k,v in enumerate(products))
                   for bit in range(d)]
    targets=[0]*m
    for mask in poly:
        ids=[i for i in range(m) if mask>>i&1]
        if len(ids)==1: i=j=k=ids[0]
        elif len(ids)==2: i,j=ids; i,j,k=i,i,j
        else: i,j,k=ids
        targets[k]^=1<<(i+m*j)
    C=[solve(trace_columns,v) for v in targets]
    assert all(x is not None for x in C)
    columns=[A[i]|(B[i]<<d)|(C[i]<<(2*d)) for i in range(m)]
    constraints=nullspace_rows(columns,3*d)
    assert len(span(columns))==m and len(constraints)==3*d-m
    kernel=nullspace_rows(constraints,3*d)
    assert len(kernel)==m
    return dict(h=h,m=m,d=d,A=A,B=B,C=C,columns=columns,
                constraints=constraints,kernel=kernel,polynomial=sorted(poly))


def lin(columns,bits):
    ans=0
    for i,c in enumerate(columns):
        if bits>>i&1: ans^=c
    return ans


def xyz_trace(v,d,h):
    mask=(1<<d)-1
    x,y,z=v&mask,(v>>d)&mask,(v>>(2*d))&mask
    return gf_trace(gf_mul(gf_mul(x,y,h),z,h),h)


def phase_from_circuit(n,gates,output):
    # Wires 0..n-1 are inputs; gate i gets wire n+i. Multiplier variables
    # begin after all input and gate-value variables, one per equation.
    g=len(gates)+1; mult_start=n+len(gates); poly=set()
    equations=[]
    for i,(op,args) in enumerate(gates):
        terms={1<<(n+i)}
        if op=='AND': terms.symmetric_difference_update({(1<<args[0])|(1<<args[1])})
        elif op=='XOR':
            for a in args: terms.symmetric_difference_update({1<<a})
        elif op=='NOT': terms.symmetric_difference_update({0,1<<args[0]})
        else: raise ValueError(op)
        equations.append(terms)
    equations.append({0,1<<output})
    for j,eq in enumerate(equations):
        for term in eq: poly.symmetric_difference_update({term|(1<<(mult_start+j))})
    return poly,mult_start+g,g


def circuit_accepts(bits,n,gates,output):
    values=[bits>>i&1 for i in range(n)]
    for op,args in gates:
        if op=='AND': val=values[args[0]]&values[args[1]]
        elif op=='XOR': val=values[args[0]]^values[args[1]]
        else: val=values[args[0]]^1
        values.append(val)
    return values[output]


def fwht(v):
    out=list(v); step=1
    while step<len(out):
        for i in range(0,len(out),2*step):
            for j in range(step):
                a,b=out[i+j],out[i+j+step]
                out[i+j],out[i+j+step]=a+b,a-b
        step*=2
    return out


def main():
    rng=random.Random(202610272057); rows=[]; point_checks=0; moduli={}
    for m in range(3,7):
        h=fixture_modulus(m*m); moduli[m*m]=h
        monomials=[sum(1<<i for i in S) for k in (1,2,3) for S in itertools.combinations(range(m),k)]
        for rep in range(10):
            poly={v for v in monomials if rng.randrange(2)}
            emb=parity_embedding(poly,m,h)
            for u in range(1<<m):
                v=lin(emb['columns'],u)
                assert all(not ((c&v).bit_count()&1) for c in emb['constraints'])
                assert xyz_trace(v,emb['d'],h)==polynomial_value(poly,u)
                point_checks+=1
            raw=sum(1-2*polynomial_value(poly,u) for u in range(1<<m))
            constrained=sum(1-2*xyz_trace(lin(emb['kernel'],u),emb['d'],h) for u in range(1<<m))
            assert raw==constrained
            emb.update(raw_phase_sum=raw,constrained_phase_sum=constrained)
            rows.append(emb)
        print('embedded',m,'variables in field degree',m*m,flush=True)
    circuit_rows=[]
    fixtures=[(2,[('AND',(0,1))],2),(2,[('XOR',(0,1))],2),
              (1,[('NOT',(0,))],1),(3,[('AND',(0,1)),('XOR',(3,2))],4)]
    for n,gates,output in fixtures:
        p,m,g=phase_from_circuit(n,gates,output)
        accepted=sum(circuit_accepts(x,n,gates,output) for x in range(1<<n))
        Z=sum(1-2*polynomial_value(p,u) for u in range(1<<m))
        assert Z==(1<<g)*accepted
        h=moduli.get(m*m) or fixture_modulus(m*m)
        emb=parity_embedding(p,m,h)
        constrained=sum(1-2*xyz_trace(lin(emb['kernel'],u),emb['d'],h) for u in range(1<<m))
        assert Z==constrained
        circuit_rows.append(dict(n=n,gates=gates,output=output,equations=g,phase_variables=m,
                                 field_degree=m*m,accepted=accepted,phase_sum=Z,embedding=emb))
    support_rows=[]
    for n in range(2,11):
        for rank in range(0,n+1,2):
            linear=rng.randrange(1<<n); constant=rng.randrange(2)
            vals=[]
            for x in range(1<<n):
                bit=constant^((linear&x).bit_count()&1)
                for j in range(rank//2): bit^=(x>>(2*j)&1)&(x>>(2*j+1)&1)
                vals.append(1-2*bit)
            W=fwht(vals); support=[i for i,v in enumerate(W) if v]
            assert len(support)==1<<rank
            assert all(abs(W[i])==1<<(n-rank//2) for i in support)
            support_rows.append(dict(n=n,rank=rank,linear=linear,constant=constant,
                                     support_size=len(support),walsh_magnitude=1<<(n-rank//2)))
    out=dict(cubic_embeddings=rows,pointwise_identities=point_checks,
             gate_reductions=circuit_rows,quadratic_fourier_support=support_rows)
    path=Path(__file__).with_name('parity_constraint_obstruction_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print('passed',len(rows),'embeddings;',point_checks,'pointwise identities;',len(circuit_rows),'gate reductions;',len(support_rows),'Fourier support cases')
if __name__=='__main__': main()
