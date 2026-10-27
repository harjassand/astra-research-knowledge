#!/usr/bin/env python3
"""Recursive raw rank-five count plus exact rejection-boundary checks."""
from rank_five_stationary import *


def quadratic_noise(R,b,height,seed):
    rng=random.Random(seed);qn=b*R.d*height;rank=qn-qn%2
    forms=random_invertible(qn,rng);factors=[];Q=set()
    for a in forms[:rank]:
        factors.append(sum(((a>>(R.d*height*i))&((1<<(R.d*height))-1))<<(R.m*i)
                           for i in range(b)))
    for a,c in zip(factors[::2],factors[1::2]):
        for i in bits(a):
            for j in bits(c):Q.symmetric_difference_update({(1<<i)|(1<<j)})
    polar=quadratic_matrix_from_anf(Q,b*R.m)
    assert len(span(polar))==rank
    return Q,rank


def coefficient_state(e,seed,*,translate=True,noise=True):
    R=ChainRing(11,e);b=5;n=b*R.m;rng=random.Random(seed)
    P=smooth_rank_five_polynomial(R,rng=rng)
    cubic={tuple(i for i,a in enumerate(ex) if a):c for ex,c in P.items()
           if max(ex)==1}
    error,rank=quadratic_noise(R,b,(e+1)//3,seed+7) if noise else (set(),0)
    offset=rng.randrange(1<<n) if translate else 0;mask=(1<<R.m)-1
    def phase(x):
        y=x^offset
        return R.functional(ring_polynomial(R,P,[(y>>(R.m*i))&mask for i in range(b)]))^polynomial_value(error,y)^(seed&1)
    Q=quadratic_coefficients(lambda x:phase(x)^rank_state_value(R,cubic,set(),x,b),n)
    for _ in range(256):
        x=rng.randrange(1<<n)
        assert rank_state_value(R,cubic,Q,x,b)==phase(x)
    exponent=2*b*(e//3)+(b if e%3==2 else 0)
    reference=(1<<(R.d*exponent))*(1-2*(seed&1))
    return R,cubic,Q,reference,dict(n=n,e=e,seed=seed,noise_rank=rank,offset=offset,
        polynomial=[dict(exponents=list(a),coefficient=c) for a,c in sorted(P.items())])


def run():
    root=Path(__file__).parent;target=root/'rank_five_stationary_results.json'
    data=json.loads(target.read_text());data.setdefault('recursive_raw_cases',[])
    e=5;seed=9505;t=time.perf_counter()
    raw,n,evaluate,reference,metadata=rank_five_fixture(e,seed)
    source=root/f'rank_five_{n}_input.json'
    source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),separators=(',',':'))+'\n')
    print(json.dumps(dict(stage='recursive raw centroid compiler',n=n,terms=len(raw),
                         fixture_seconds=time.perf_counter()-t)),flush=True)
    result=compile_fixed_rank_stationary(raw,n)
    assert result['module_dimension']==5 and result['centroid_dimension']==15
    assert result['signed_count']==reference
    assert [a['depth'] for a in result['certificate']['stages']]==[5,2]
    assert result['certificate']['stages'][0]['discarded_free_bits']==30
    R=ChainRing(result['field_modulus'],e);cubic=normalize_cubic(result['canonical_cubic'])
    rng=random.Random(seed+1000000)
    for _ in range(1024):
        y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y)
        assert rank_state_value(R,cubic,set(result['quadratic_remainder']),y,5)==evaluate(x)
    result.update(metadata,reference=reference,pointwise_checks=1024,raw_input_file=source.name,
                  practical_speed_claim=False)
    data['recursive_raw_cases'].append(result);target.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['original_variables','module_dimension','centroid_dimension',
                                         'signed_count','zero_count','seconds']}),flush=True)
    R,cubic,Q,reference,metadata=coefficient_state(8,9608)
    signed,certificate=stationary_fixed_rank_state(R.h,R.e,cubic,Q,5)
    assert signed==reference
    assert [a['depth'] for a in certificate['stages']]==[8,5,2]
    data['recursive_state_cases']=[dict(**metadata,signed_count=signed,reference=reference,
                                      quadratic_remainder=sorted(Q),certificate=certificate)]
    rejected=[]
    R,cubic,Q,_,_=coefficient_state(3,9700,translate=False,noise=False)
    bad=set(Q);bad.symmetric_difference_update({1<<(2*R.d)})
    try:stationary_fixed_rank_state(R.h,R.e,cubic,bad,5)
    except ValueError as exc:rejected.append(dict(case='noncritical affine gradient',reason=str(exc)))
    else:raise AssertionError('inconsistent constant gradient accepted')
    R,cubic,Q,_,_=coefficient_state(5,9702,translate=False,noise=False)
    bad=set(Q);bad.symmetric_difference_update({1<<(R.d*(R.e-2))})
    try:stationary_fixed_rank_state(R.h,R.e,cubic,bad,5)
    except ValueError as exc:rejected.append(dict(case='nonzero discarded-layer coefficient',reason=str(exc)))
    else:raise AssertionError('used discarded layer accepted')
    R=ChainRing(11,2);P=smooth_rank_five_polynomial(R);P.pop((0,0,0,0,3))
    cubic={tuple(i for i,a in enumerate(ex) if a):c for ex,c in P.items() if max(ex)==1}
    def phase(x):return R.functional(ring_polynomial(R,P,[(x>>(R.m*i))&((1<<R.m)-1) for i in range(5)]))
    Q=quadratic_coefficients(lambda x:phase(x)^rank_state_value(R,cubic,set(),x,5),5*R.m)
    try:stationary_fixed_rank_state(R.h,R.e,cubic,Q,5)
    except ValueError as exc:rejected.append(dict(case='singular homogeneous gradient',reason=str(exc)))
    else:raise AssertionError('singular projective gradient accepted')
    assert len(rejected)==3
    data['rejections']=rejected;target.write_text(json.dumps(data,indent=2)+'\n')
    print('recursive state and all three rejection checks passed',flush=True)


if __name__=='__main__':run()
