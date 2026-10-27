#!/usr/bin/env python3
"""End-to-end raw inputs, independent brute oracles, and representation checks."""
from acquired_chain_counter import *
from field_descent import extract_anf,random_invertible
from field_rank_decoder import quadratic_value
import random

def fixture(h,e,seed,rank=0,mode='zero'):
    R=ChainRing(h,e);n=3*R.m;rng=random.Random(seed)
    mask=(1<<R.m)-1;lam=rng.randrange(mask+1)|1
    P={(1,1,1):lam}
    if mode=='unit':P.update({(1,0,0):1,(0,1,0):1,(0,0,1):lam})
    if mode=='generic':
        for exponent in [(1,1,0),(1,0,1),(0,1,1),(1,0,0),(0,1,0),(0,0,1),(0,0,0)]:
            P[exponent]=rng.randrange(mask+1)
    columns=random_invertible(n,rng);offset=rng.randrange(1<<n)
    factors=[]
    while len(factors)<rank:
        f=rng.randrange(1,1<<n)
        if len(span(factors+[f]))>len(factors):factors.append(f)
    def hidden(x):
        value=R.functional(ring_polynomial(R,P,[(x>>(R.m*i))&mask for i in range(3)]))
        for j in range(rank//2):
            value^=((factors[2*j]&x).bit_count()&1)*((factors[2*j+1]&x).bit_count()&1)
        return value
    def raw_eval(x):return hidden(linear_apply(columns,x)^offset)
    raw=extract_anf(raw_eval,n)
    # Reference uses the planted factors, never the acquired coordinate system.
    numerator=0;gram_solver=Solver(R.gram());identity=[[int(i==j) for i in range(3)] for j in range(3)]
    for selector in range(1<<rank):
        parity=linear_apply(factors,selector)
        sign=(-1)**sum(((selector>>(2*j))&3)==3 for j in range(rank//2))
        numerator+=sign*balanced_count(R,shifted_polynomial(R,P,identity,parity,gram_solver))
    denominator=1<<(rank//2);assert numerator%denominator==0
    reference=numerator//denominator
    if mode=='zero' and not rank:
        q=1<<R.d;assert reference==q**(2*e-1)*(q+e*(q-1))
    return raw,n,raw_eval,reference,dict(h=h,e=e,rank=rank,mode=mode,seed=seed,
        planted_polynomial=[dict(exponents=list(a),coefficient=b) for a,b in sorted(P.items())],
        planted_binary_columns=columns,planted_binary_offset=offset,planted_error_factors=factors)

def run():
    cases=[]
    specifications=[(0b1011,2,101,0,'zero'),(0b1011,3,102,0,'unit'),
        (0b1011,4,103,0,'zero'),(0b10011,3,104,0,'generic'),
        (0b1011,5,105,0,'zero'),(0b10000011,2,106,2,'unit'),
        (0b10000011,3,107,2,'zero')]
    for h,e,seed,rank,mode in specifications:
        raw,n,evaluate,reference,metadata=fixture(h,e,seed,rank,mode)
        result=compile_chain(raw,n);assert result['signed_count']==reference
        assert result['acquired_defect_rank']==rank
        checks=0;exhaustive=0
        if n<=18:
            brute=sum(1-2*evaluate(x) for x in range(1<<n));assert brute==reference
            exhaustive=1<<n
        R=ChainRing(result['field_modulus'],result['chain_length'])
        P={tuple(x['exponents']):x['coefficient'] for x in result['polynomial']}
        rng=random.Random(seed+100000);mask=(1<<R.m)-1
        for _ in range(1024):
            y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y)
            value=R.functional(ring_polynomial(R,P,[(y>>(R.m*i))&mask for i in range(3)]))
            value^=quadratic_value(result['acquired_defect'],y)
            assert value==evaluate(x);checks+=1
        result.update(metadata,pointwise_checks=checks,exhaustive_assignments=exhaustive,
                      raw_polynomial=sorted(raw),reference=reference)
        cases.append(result)
        print(json.dumps({k:result[k] for k in ['original_variables','chain_length','field_degree',
            'acquired_defect_rank','signed_count','zero_count','seconds']}),flush=True)
        Path(__file__).with_name('chain_counter_results.json').write_text(json.dumps(dict(
            status='all completed assertions passed',cases=cases,practical_speed_claim=False),indent=2)+'\n')
    return cases

if __name__=='__main__':run()
