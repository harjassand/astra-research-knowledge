#!/usr/bin/env python3
"""Acquire a translated homogeneous cubic modulo quotient quadratics."""
from stationary_chain_counter import *

def ordinary_quadratic_models(R,exponents):
    n=3*R.m;gram=R.gram();models=[];labels=[]
    for exponent in exponents:
        support=[i for i in range(n) if exponent[i//R.m]]
        columns=[set() for _ in range(R.m)]
        zero=monomial(R,exponent,[0,0,0]);singles={}
        for j in bits(linear_apply(gram,zero)):columns[j].add(0)
        for i in support:
            point=[0]*3;point[i//R.m]=1<<(i%R.m)
            singles[i]=monomial(R,exponent,point)^zero
            for j in bits(linear_apply(gram,singles[i])):columns[j].add(1<<i)
        for i,k in itertools.combinations(support,2):
            point=[0]*3;point[i//R.m]^=1<<(i%R.m);point[k//R.m]^=1<<(k%R.m)
            polar=monomial(R,exponent,point)^zero^singles[i]^singles[k]
            for j in bits(linear_apply(gram,polar)):columns[j].add((1<<i)|(1<<k))
        models.extend(columns);labels.extend((exponent,1<<j) for j in range(R.m))
    return models,labels

def fit_homogeneous_quotient(acquired,*,height=None):
    R=ChainRing(acquired['h'],acquired['e']);n=3*R.m
    if acquired['module_dimension']!=3 or R.d<3:
        raise ValueError('complete quotient fitter requires rank three and residue degree>=3')
    if height is None:height=(R.e+1)//3
    if not 0<=height<=R.e:raise ValueError('invalid quotient height')
    lowmask=sum(((1<<(R.d*height))-1)<<(R.m*i) for i in range(3))
    remainder=set(acquired['quadratic_remainder']);mu=acquired['cubic'][0]['coefficient']
    exponents=[a for total in range(4) for a in monomials_of_degree(total)
               if a!=(1,1,1) and not(total==2 and 2 in a)]
    models,labels=ordinary_quadratic_models(R,exponents)
    rows=[sum(1<<i for i in pair) for degree in (1,2)
          for pair in itertools.combinations(range(n),degree)]
    positions={mask:i for i,mask in enumerate(mask for mask in rows if mask&~lowmask)}
    def vector(anf):return sum(1<<positions[m] for m in anf if m in positions)
    columns=[vector(model) for model in models];target=vector(remainder)
    solution=solve(columns,target)
    if solution is None:raise ValueError('no ordinary cubic lift modulo the acquired quotient')
    P={(1,1,1):mu}
    for j in bits(solution):
        exponent,coefficient=labels[j];P[exponent]=P.get(exponent,0)^coefficient
    H={a:c for a,c in P.items() if c and sum(a)==3};inverse=ring_inv(R,mu)
    center=[R.mul(inverse,P.get(a,0)) for a in ((0,1,1),(1,0,1),(1,1,0))]
    encoded=sum(a<<(R.m*i) for i,a in enumerate(center));mask=(1<<R.m)-1
    def residual(x):
        shifted=[((x>>(R.m*i))&mask)^center[i] for i in range(3)]
        return state_value(R,mu,remainder,x)^R.functional(ring_polynomial(R,H,shifted))
    noise=quadratic_coefficients(residual,n)
    if any(term&~lowmask for term in noise):
        raise ValueError('fitted translation leaves a term outside the acquired quotient')
    centered_noise=quadratic_coefficients(lambda x:polynomial_value(noise,x^encoded),n)
    assert all(not(term&~lowmask) for term in centered_noise)
    certificate=dict(quotient_height=height,quotient_binary_variables=3*R.d*height,
        fit_columns=len(columns),fit_rank=len(span(columns)),fit_constraints=len(positions),
        acquired_center=center,exact_third_tensor_identity=True,
        exact_quadratic_and_affine_identity=True,verified_quotient_support=True,
        uncentered_noise=sorted(noise),centered_noise=sorted(centered_noise))
    return H,centered_noise,certificate

def acquired_from_stationary_result(result):
    return dict(h=result['field_modulus'],e=result['chain_length'],n=result['original_variables'],
        module_dimension=3,cubic=result['canonical_cubic'],quadratic_remainder=result['quadratic_remainder'])

def acquire_minimum_quotient(acquired):
    """Monotone exact fits acquire the smallest possible quotient height."""
    if acquired['module_dimension']!=3 or acquired['h'].bit_length()-1<3:
        raise ValueError('minimum-height completeness requires rank three and d>=3')
    low,high=0,acquired['e'];accepted={};trials=[]
    while low<high:
        middle=(low+high)//2
        try:accepted[middle]=fit_homogeneous_quotient(acquired,height=middle)
        except ValueError as exc:
            trials.append(dict(height=middle,accepted=False,reason=str(exc)));low=middle+1
        else:
            trials.append(dict(height=middle,accepted=True));high=middle
    if low not in accepted:accepted[low]=fit_homogeneous_quotient(acquired,height=low)
    H,Q,certificate=accepted[low]
    certificate.update(minimum_height_certified=True,fit_search=trials)
    return H,Q,certificate

def validation():
    cases=[]
    for source in json.loads(Path(__file__).with_name('stationary_counter_results.json').read_text())['cases']:
        acquired=acquired_from_stationary_result(source);R=ChainRing(acquired['h'],acquired['e'])
        H,noise,certificate=fit_homogeneous_quotient(acquired)
        center=sum(a<<(R.m*i) for i,a in enumerate(certificate['acquired_center']))
        n=3*R.m;mask=(1<<R.m)-1
        import random
        rng=random.Random(7000+n+R.d)
        for _ in range(1024):
            x=rng.randrange(1<<n);z=x^center
            rhs=R.functional(ring_polynomial(R,H,[(z>>(R.m*i))&mask for i in range(3)]))
            rhs^=polynomial_value(noise,z)
            assert rhs==state_value(R,acquired['cubic'][0]['coefficient'],set(acquired['quadratic_remainder']),x)
        case=dict(original_variables=n,field_degree=R.d,chain_length=R.e,
            homogeneous_cubic=[dict(exponents=list(a),coefficient=c) for a,c in H.items()],
            certificate=certificate,pointwise_checks=1024)
        cases.append(case)
        Path(__file__).with_name('quotient_homogeneous_results.json').write_text(json.dumps(dict(
            status='all completed assertions passed',cases=cases),indent=2)+'\n')
        print(n,R.d,R.e,certificate['quotient_binary_variables'],flush=True)

if __name__=='__main__':validation()
