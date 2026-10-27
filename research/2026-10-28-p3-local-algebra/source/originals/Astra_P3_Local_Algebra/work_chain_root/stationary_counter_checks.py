#!/usr/bin/env python3
"""Raw affine-disguised smooth cubics, quotient noise, and exact count checks."""
from stationary_chain_counter import *
from field_descent import extract_anf,random_invertible
import random

def smooth_fixture(h,e,seed):
    R=ChainRing(h,e);n=3*R.m;rng=random.Random(seed)
    # Smooth over every characteristic-two field, including F2 and F4.
    residue={(2,0,1):1,(0,3,0):1,(0,0,3):1,(1,1,1):1}
    P={a:residue.get(a,0)^(rng.randrange(1<<(R.m-R.d))<<R.d)
       for a in monomials_of_degree(3)}
    P={a:c for a,c in P.items() if c}
    height=(e+1)//3;quotient_n=3*R.d*height
    error_rank=quotient_n-quotient_n%2
    quotient_columns=random_invertible(quotient_n,rng) if quotient_n else []
    factors=[]
    for column in quotient_columns[:error_rank]:
        factors.append(sum(((column>>(R.d*height*i))&((1<<(R.d*height))-1))
                           <<(R.m*i) for i in range(3)))
    constant=seed&1;mask=(1<<R.m)-1
    columns=random_invertible(n,rng);offset=rng.randrange(1<<n)
    def hidden(x):
        value=R.functional(ring_polynomial(R,P,[(x>>(R.m*i))&mask for i in range(3)]))^constant
        for j in range(error_rank//2):
            value^=((factors[2*j]&x).bit_count()&1)*((factors[2*j+1]&x).bit_count()&1)
        return value
    def evaluate(x):return hidden(linear_apply(columns,x)^offset)
    raw=extract_anf(evaluate,n)
    q=1<<R.d
    if e%3==0:reference=q**(2*e)
    elif e%3==2:reference=q**(2*e-1)
    else:
        F=ChainRing(h,1)
        reference=q**(2*(e-1))*sum(1-2*F.functional(ring_polynomial(F,residue,
            [(x>>(R.d*i))&(q-1) for i in range(3)])) for x in range(q**3))
    reference*=1-2*constant
    return raw,n,evaluate,reference,dict(seed=seed,planted_field_modulus=h,
        planted_chain_length=e,planted_polynomial=[dict(exponents=list(a),coefficient=c)
        for a,c in sorted(P.items())],planted_binary_columns=columns,
        planted_binary_offset=offset,quotient_height=height,planted_error_rank=error_rank,
        planted_error_factors=factors,planted_constant=constant)

def truth_sum(poly,n):
    import numpy as np
    values=np.zeros(1<<n,dtype=np.uint8);values[list(poly)]=1
    for i in range(n):
        view=values.reshape(-1,2,1<<i);view[:,1,:]^=view[:,0,:]
    return (1<<n)-2*int(values.sum())

def run():
    cases=[]
    specifications=[(0b1011,2,6002),(0b1011,3,6003),(0b1011,4,6004),
        (0b1011,5,6005),(0b1011,8,6008),(0x1009,2,6012),(0b1011,12,6024)]
    for h,e,seed in specifications:
        raw,n,evaluate,reference,metadata=smooth_fixture(h,e,seed)
        source=Path(__file__).with_name(f'stationary_{n}_d{h.bit_length()-1}_input.json')
        source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),separators=(',',':'))+'\n')
        print(json.dumps(dict(stage='raw compiler',n=n,e=e,d=h.bit_length()-1,
                              rank=metadata['planted_error_rank'],terms=len(raw))),flush=True)
        result=compile_stationary(raw,n)
        assert result['signed_count']==reference,(result['signed_count'],reference)
        assert result['certificate']['walsh_leaves']==0
        R=ChainRing(result['field_modulus'],result['chain_length']);rng=random.Random(seed+500000)
        for _ in range(1024):
            y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y)
            assert state_value(R,result['canonical_cubic'][0]['coefficient'],
                set(result['quadratic_remainder']),y)==evaluate(x)
        exhaustive=0
        if n<=24:assert truth_sum(raw,n)==reference;exhaustive=1<<n
        result.update(metadata,reference=reference,pointwise_checks=1024,
                      exhaustive_assignments=exhaustive,raw_input_file=source.name)
        cases.append(result)
        Path(__file__).with_name('stationary_counter_results.json').write_text(json.dumps(dict(
            status='all completed assertions passed',cases=cases,practical_speed_claim=False),indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ['original_variables','field_degree','chain_length',
            'planted_error_rank','signed_count','zero_count','seconds']}),flush=True)
    return cases

if __name__=='__main__':run()
