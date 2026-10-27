#!/usr/bin/env python3
"""End-to-end raw scalar cubic acquisition beyond the block radius.

No field, code, input gauge or error support is passed to the public compiler.
Generic multivariate point counting is not executed by this finite validator.
"""
from sylvester_support_checks import *
from field_rank_checks import random_defect,congruence


def shear_anf(poly,i,j):
    # Substitute x_i <- x_i + x_j; exact Boolean quotient-ring arithmetic.
    # Different source terms can collide (e.g. x_i and x_i*x_j), so XOR them.
    extra=set()
    for term in poly:
        if term>>i&1:
            new=(term^(1<<i))|(1<<j)
            if new in extra: extra.remove(new)
            else: extra.add(new)
    return poly^extra


def fixture(d=12,b=9,r=8,seed=128908):
    rng=random.Random(seed); h=first_modulus(d); q=1<<d; n=d*b
    gram=trace_gram(h); poly=set(); cubic=[]
    products={(a,c):gf_mul(1<<a,1<<c,h) for a in range(d) for c in range(d)}
    for i,j,k in itertools.combinations(range(b),3):
        coefficient=rng.randrange(1,q); cubic.append((i,j,k,coefficient))
        for a in range(d):
            for c in range(d):
                trfunctional=linear_apply(gram,gf_mul(coefficient,products[a,c],h))
                for e in bits(trfunctional): poly.add((1<<(i*d+a))|(1<<(j*d+c))|(1<<(k*d+e)))
    base=random_base(h,b,1,rng)
    for i in range(n):
        for j in range(i+1,n):
            if base[i]>>j&1: poly.add((1<<i)|(1<<j))
        if rng.randrange(2): poly.add(1<<i)
    if rng.randrange(2): poly.add(0)
    shears=[]
    for _ in range(2*n):
        i,j=rng.sample(range(n),2); shears.append((i,j)); poly=shear_anf(poly,i,j)
    defect=random_defect(n,r,rng)
    for i in range(n):
        for j in range(i+1,n):
            if defect[i]>>j&1:
                term=(1<<i)|(1<<j)
                if term in poly: poly.remove(term)
                else: poly.add(term)
    return poly,n,defect,dict(planted_modulus=h,planted_cubic_coefficients=cubic,
        planted_shears=shears,seed=seed)


def run():
    raw,n,defect,metadata=fixture()
    Path(__file__).with_name('raw_108_input.json').write_text(json.dumps(dict(n=n,polynomial_masks=sorted(raw)))+'\n')
    print(json.dumps(dict(stage='raw acquired field and global support',n=n,terms=len(raw))),flush=True)
    acquired=acquire_sylvester_trace_form(raw,n,method='one_sided')
    expected=congruence(defect,acquired['coordinate_columns'])
    assert acquired['acquired_defect']==expected
    assert acquired['acquired_defect_rank']==8
    assert acquired['field_extension_degree']==12 and acquired['module_dimension']==9
    polynomial={tuple(term['exponents']):term['coefficient'] for term in acquired['field_polynomial']}
    rng=random.Random(222817); h=acquired['field_modulus']; d=12; q=1<<d
    for _ in range(1024):
        y=rng.getrandbits(n); x=linear_apply(acquired['coordinate_columns'],y)
        fieldpoint=[(y>>(d*i))&(q-1) for i in range(9)]
        predicted=gf_trace(field_polynomial_value(polynomial,fieldpoint,h),h)^quadratic_value(expected,y)
        assert polynomial_value(raw,x)==predicted
    try: acquire_quadratic_base(acquired['quadratic_matrix'],h)
    except ValueError as error: old_rejection=str(error)
    else: raise AssertionError('fixture should exceed old block decoder')
    acquired.update(metadata,planted_defect=defect,pointwise_identity_checks=1024,
        old_block_decoder_rejection=old_rejection,
        distinction='full raw acquisition executed; generic field point-count theorem is not executed')
    return acquired


if __name__=='__main__':
    result=run(); Path(__file__).with_name('sylvester_raw_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['original_variables','field_extension_degree','module_dimension','acquired_defect_rank','seconds']}))
