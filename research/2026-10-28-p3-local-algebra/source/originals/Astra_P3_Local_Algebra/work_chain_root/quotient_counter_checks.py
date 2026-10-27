#!/usr/bin/env python3
"""Raw acquisition with smooth, nodal, and three-ray residue cubics."""
from acquired_quotient_counter import *
from stationary_counter_checks import truth_sum
from field_descent import extract_anf,random_invertible
import random

def fixture(h,e,seed,residue,*,nilpotent=True,height=None,residual_bit_budget=None):
    R=ChainRing(h,e);n=3*R.m;mask=(1<<R.m)-1;rng=random.Random(seed)
    P={a:residue.get(a,0)^((rng.randrange(1<<(R.m-R.d))<<R.d) if nilpotent else 0)
       for a in monomials_of_degree(3)};P={a:c for a,c in P.items() if c}
    if height is None:height=(e+1)//3
    qn=3*R.d*height;rank=qn-qn%2
    quotient_columns=random_invertible(qn,rng) if qn else []
    factors=[sum(((u>>(R.d*height*i))&((1<<(R.d*height))-1))<<(R.m*i)
                  for i in range(3)) for u in quotient_columns[:rank]]
    constant=seed&1
    def noise(x):
        return constant^sum(((a&x).bit_count()&1)*((b&x).bit_count()&1)
            for a,b in zip(factors[::2],factors[1::2]))%2
    Q=quadratic_coefficients(noise,n)
    reference,ref_certificate=weighted_homogeneous_sum(h,e,P,Q,residual_bit_budget=residual_bit_budget)
    columns=random_invertible(n,rng);offset=rng.randrange(1<<n)
    def evaluate(x):
        y=linear_apply(columns,x)^offset
        return R.functional(ring_polynomial(R,P,[(y>>(R.m*i))&mask for i in range(3)]))^noise(y)
    raw=extract_anf(evaluate,n)
    return raw,n,evaluate,reference,dict(seed=seed,planted_field_modulus=h,
        planted_chain_length=e,planted_error_rank=rank,planted_constant=constant,
        planted_quotient_height=height,
        planted_polynomial=[dict(exponents=list(a),coefficient=c) for a,c in sorted(P.items())],
        planted_binary_columns=columns,planted_binary_offset=offset,
        planted_error_factors=factors,reference_certificate=ref_certificate)

def run():
    smooth={(2,0,1):1,(0,3,0):1,(0,0,3):1,(1,1,1):1}
    nodal={(3,0,0):1,(2,0,1):1,(0,2,1):1,(1,1,1):1}
    triangle={(1,1,1):1}
    cases=[]
    specifications=[(11,2,8102,smooth,True),(11,2,8103,nodal,True),
        (11,2,8104,triangle,True),(11,3,8105,nodal,True),
        (11,4,8106,triangle,True),(11,5,8107,nodal,True),
        (0x1009,2,8112,triangle,False)]
    for h,e,seed,residue,nilpotent in specifications:
        raw,n,evaluate,reference,metadata=fixture(h,e,seed,residue,nilpotent=nilpotent)
        source=Path(__file__).with_name(f'quotient_raw_{n}_{seed}.json')
        source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),separators=(',',':'))+'\n')
        print(json.dumps(dict(stage='raw quotient compiler',n=n,d=h.bit_length()-1,e=e,
                              rank=metadata['planted_error_rank'],terms=len(raw))),flush=True)
        result=compile_quotient(raw,n);assert result['signed_count']==reference
        assert result['count_certificate']['walsh_leaves']==0
        H={tuple(t['exponents']):t['coefficient'] for t in result['homogeneous_cubic']}
        R=ChainRing(result['field_modulus'],e);mask=(1<<R.m)-1
        center=sum(a<<(R.m*i) for i,a in enumerate(result['fit']['acquired_center']))
        Q=set(result['quotient_quadratic']);rng=random.Random(seed+100000)
        for _ in range(1024):
            y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y);z=y^center
            answer=R.functional(ring_polynomial(R,H,[(z>>(R.m*i))&mask for i in range(3)]))
            assert answer^polynomial_value(Q,z)==evaluate(x)
        exhaustive=0
        if n<=24:assert truth_sum(raw,n)==reference;exhaustive=1<<n
        result.update(metadata,reference=reference,pointwise_checks=1024,
                      exhaustive_assignments=exhaustive,raw_input_file=source.name)
        cases.append(result)
        Path(__file__).with_name('quotient_counter_results.json').write_text(json.dumps(dict(
            status='all completed assertions passed',cases=cases,practical_speed_claim=False),indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ['original_variables','field_degree','chain_length',
            'planted_error_rank','signed_count','zero_count','seconds']}),flush=True)
    return cases

if __name__=='__main__':run()
