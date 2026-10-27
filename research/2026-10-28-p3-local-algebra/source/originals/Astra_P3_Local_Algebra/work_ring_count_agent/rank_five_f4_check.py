#!/usr/bin/env python3
"""Independent complete raw truth table for rank five over F4[t]/t^2."""
from rank_five_stationary import *
import numpy as np


def run():
    R=ChainRing(7,2);b=5;n=b*R.m;rng=random.Random(9521);alpha=2
    beta=gf_pow(alpha,2,R.h)
    P={(0,0,0,0,3):1,(1,1,0,0,1):1,(0,0,1,1,1):1,
       (2,1,0,0,0):1,(1,2,0,0,0):beta,
       (0,0,2,1,0):1,(0,0,1,2,0):beta}
    for exponent in degree_monomials(5,3):
        P[exponent]=P.get(exponent,0)^(rng.randrange(4)<<2)
    P={a:c for a,c in P.items() if c}
    forms=random_invertible(10,rng)
    factors=[sum(((a>>(2*i))&3)<<(R.m*i) for i in range(b)) for a in forms]
    noise=set()
    for a,c in zip(factors[::2],factors[1::2]):
        for i in bits(a):
            for j in bits(c):noise.symmetric_difference_update({(1<<i)|(1<<j)})
    assert len(span(quadratic_matrix_from_anf(noise,n)))==10
    columns=random_invertible(n,rng);offset=rng.randrange(1<<n);constant=1
    def hidden(x):
        values=[(x>>(R.m*i))&((1<<R.m)-1) for i in range(b)]
        return R.functional(ring_polynomial(R,P,values))^polynomial_value(noise,x)^constant
    def evaluate(x):return hidden(linear_apply(columns,x)^offset)
    raw=extract_anf(evaluate,n)
    source=Path(__file__).with_name('rank_five_20_input.json')
    source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),separators=(',',':'))+'\n')
    result=compile_fixed_rank_stationary(raw,n)
    table=np.zeros(1<<n,dtype=np.uint8);table[list(raw)]=1
    for i in range(n):
        view=table.reshape(-1,2,1<<i);view[:,1,:]^=view[:,0,:]
    truth=(1<<n)-2*int(table.sum())
    assert result['module_dimension']==5 and result['field_degree']==2
    assert result['chain_length']==2 and result['centroid_dimension']==4
    assert result['signed_count']==truth==-(4**5)
    assert result['zero_count']==int((table==0).sum())
    for x in range(1<<n):
        # The full table verifies the counter. Only a small deterministic set
        # additionally cross-checks the separately specified planted evaluator.
        if x<256:assert int(table[x])==evaluate(x)
    result.update(full_truth_assignments=1<<n,truth_signed_count=truth,
        planted_noise_rank=10,planted_field_modulus=R.h,
        planted_polynomial=[dict(exponents=list(a),coefficient=c) for a,c in sorted(P.items())],
        planted_noise=sorted(noise),planted_binary_columns=columns,
        planted_binary_offset=offset,planted_constant=constant,raw_input_file=source.name,
        practical_speed_claim=False)
    target=Path(__file__).with_name('rank_five_f4_results.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['original_variables','field_degree','module_dimension',
        'centroid_dimension','signed_count','zero_count','full_truth_assignments','seconds']}),flush=True)
    return result


if __name__=='__main__':run()
