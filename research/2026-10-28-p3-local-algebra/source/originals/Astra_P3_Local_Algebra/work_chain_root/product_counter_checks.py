#!/usr/bin/env python3
from acquired_product_counter import *
from field_descent import extract_anf,random_invertible
from field_rank_decoder import quadratic_value
import random

def run():
    cases=[]
    for h,lengths,rank,seed in [(0b1011,[1,1],2,401),(0b1011,[1,3],4,402),
                                (0b1011,[2,3],4,403)]:
        rng=random.Random(seed);rings=[ChainRing(h,e) for e in lengths]
        widths=[3*R.m for R in rings];n=sum(widths);offsets=[0,widths[0]]
        polynomials=[{(1,1,1):1} for R in rings];factors=[]
        for j in range(rank//2):
            factors.extend([rng.randrange(1,1<<widths[i])<<offsets[i] for i in range(2)])
        assert len(span(factors))==rank
        def hidden(x):
            value=0
            for R,P,offset,width in zip(rings,polynomials,offsets,widths):
                local=(x>>offset)&((1<<width)-1);mask=(1<<R.m)-1
                value^=R.functional(ring_polynomial(R,P,[(local>>(R.m*i))&mask for i in range(3)]))
            for j in range(rank//2):value^=((factors[2*j]&x).bit_count()&1)*((factors[2*j+1]&x).bit_count()&1)
            return value
        columns=random_invertible(n,rng);affine=rng.randrange(1<<n)
        def evaluate(x):return hidden(linear_apply(columns,x)^affine)
        raw=extract_anf(evaluate,n);numerator=0;identity=[[int(i==j) for i in range(3)] for j in range(3)]
        for selector in range(1<<rank):
            parity=linear_apply(factors,selector)
            product=(-1)**sum(((selector>>(2*j))&3)==3 for j in range(rank//2))
            for R,P,offset,width in zip(rings,polynomials,offsets,widths):
                local=(parity>>offset)&((1<<width)-1)
                product*=balanced_count(R,shifted_polynomial(R,P,identity,local,Solver(R.gram())))
            numerator+=product
        assert numerator%(1<<(rank//2))==0;reference=numerator//(1<<(rank//2))
        result=compile_product(raw,n);assert result['signed_count']==reference
        assert result['acquired_defect_rank']==rank and result['component_count']==2
        if n<=18:assert sum(1-2*evaluate(x) for x in range(1<<n))==reference
        components=result['components']
        for _ in range(1024):
            y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y)
            value=quadratic_value(result['acquired_defect'],y)
            for c in components:
                R=ChainRing(c['field_modulus'],c['chain_length']);mask=(1<<R.m)-1
                z=y>>c['bit_offset'];P={tuple(a['exponents']):a['coefficient'] for a in c['polynomial']}
                value^=R.functional(ring_polynomial(R,P,[(z>>(R.m*i))&mask for i in range(3)]))
            assert value==evaluate(x)
        result.update(seed=seed,raw_polynomial=sorted(raw),reference=reference,pointwise_checks=1024,
                      exhaustive_assignments=(1<<n) if n<=18 else 0)
        cases.append(result)
        print(json.dumps({k:result[k] for k in ['original_variables','component_count','acquired_defect_rank',
            'signed_count','zero_count','seconds']}),flush=True)
        Path(__file__).with_name('product_counter_results.json').write_text(json.dumps(dict(
            status='all completed exact assertions passed',cases=cases,practical_speed_claim=False),indent=2)+'\n')
    return cases

if __name__=='__main__':run()
