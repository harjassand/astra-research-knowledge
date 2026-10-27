#!/usr/bin/env python3
"""Program used for minimum-height acquisition and residual checks."""
from quotient_counter_checks import *

def run():
    cases=[]
    for e,height,seed in [(2,2,8202),(4,2,8204),(7,3,8207)]:
        p,n,evaluate,reference,metadata=fixture(11,e,seed,{(1,1,1):1},
            height=height,residual_bit_budget=24)
        result=compile_quotient(p,n,residual_bit_budget=24)
        assert result['signed_count']==reference and result['fit']['quotient_height']==height
        if n<=24:assert truth_sum(p,n)==reference
        R=ChainRing(result['field_modulus'],e)
        H={tuple(t['exponents']):t['coefficient'] for t in result['homogeneous_cubic']}
        Q=set(result['quotient_quadratic']);a=sum(t<<(R.m*i) for i,t in enumerate(result['fit']['acquired_center']))
        rng=random.Random(seed+1000);mask=(1<<R.m)-1
        for _ in range(1024):
            y=rng.randrange(1<<n);z=y^a;x=linear_apply(result['coordinate_columns'],y)
            assert R.functional(ring_polynomial(R,H,[(z>>(R.m*i))&mask for i in range(3)]))^polynomial_value(Q,z)==evaluate(x)
        result.update(metadata,reference=reference,pointwise_checks=1024,
                      exhaustive_assignments=(1<<n if n<=24 else 0))
        cases.append(result)
        Path(__file__).with_name('adaptive_quotient_results.json').write_text(json.dumps(dict(
            status='all completed assertions passed',cases=cases),indent=2)+'\n')
        print(n,result['fit']['quotient_height'],result['count_certificate'].get('residual_variables'),reference,flush=True)
    return cases

if __name__=='__main__':run()
