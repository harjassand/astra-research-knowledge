#!/usr/bin/env python3
"""Raw, hidden-coordinate validation of the wider acquired field representation."""
from field_bandwidth import *
from field_rank_checks import random_defect,congruence
from field_kloosterman import irreducible_binary


def first_modulus(d):
    return next(h for h in range((1<<d)|1,1<<(d+1),2) if irreducible_binary(h))


def run():
    cases=[]
    for d,b,s,r,seed in [(7,3,2,0,7320),(9,3,2,2,9322),(11,3,3,2,11332),(7,5,1,2,7512),(9,5,2,2,9522)]:
        h=first_modulus(d); q=1<<d; n=d*b; rng=random.Random(seed)
        base={}
        for j in range(1,b,2):
            e=[0]*b; e[0]=e[j]=e[j+1]=1; base[tuple(e)]=rng.randrange(1,q)
        for i in range(b):
            for j in range(b):
                for t in range(1,s+1):
                    e=[0]*b; e[i]+=1; e[j]+=1<<t
                    base[tuple(e)]=rng.randrange(q)
            e=tuple(int(i==j) for j in range(b)); base[e]=rng.randrange(q)
        base[(0,)*b]=rng.randrange(q)
        disguise=random_invertible(n,rng); offset=rng.randrange(1<<n)
        def evaluate(x):
            y=linear_apply(disguise,x)^offset
            xs=[(y>>(d*i))&(q-1) for i in range(b)]
            return gf_trace(field_polynomial_value(base,xs,h),h)
        raw=extract_anf(evaluate,n); defect=random_defect(n,r,rng)
        for i in range(n):
            for j in range(i+1,n):
                if defect[i]>>j&1:
                    term=(1<<i)|(1<<j)
                    if term in raw: raw.remove(term)
                    else: raw.add(term)
        print(json.dumps(dict(stage='acquisition',n=n,b=b,bandwidth=s,defect_rank=r)),flush=True)
        acquired=acquire_trace_form(raw,n,bandwidth=s)
        assert acquired['field_extension_degree']==d and acquired['module_dimension']==b
        expected=congruence(defect,acquired['coordinate_columns'])
        assert acquired['acquired_defect']==expected and acquired['acquired_defect_rank']==r
        representation={tuple(t['exponents']):t['coefficient'] for t in acquired['field_polynomial']}
        hh=acquired['field_modulus']
        def reconstructed(y):
            ys=[(y>>(d*i))&(q-1) for i in range(b)]
            return gf_trace(field_polynomial_value(representation,ys,hh),hh)^quadratic_value(expected,y)
        checks=0
        for _ in range(1024):
            y=rng.randrange(1<<n); x=linear_apply(acquired['coordinate_columns'],y)
            assert polynomial_value(raw,x)==reconstructed(y); checks+=1
        # Full coefficient identity, not random sampling, on the first wider fixture.
        coefficient_check=0
        if seed==7320:
            transformed=extract_anf(lambda y:polynomial_value(raw,linear_apply(acquired['coordinate_columns'],y)),n)
            integrated=extract_anf(reconstructed,n)
            assert transformed==integrated
            coefficient_check=sum(__import__('math').comb(n,i) for i in range(4))
        acquired.update(planted_modulus=h,planted_disguise=disguise,planted_offset=offset,
            planted_polynomial=[dict(exponents=list(e),coefficient=c) for e,c in sorted(base.items())],
            planted_defect=defect,pointwise_checks=checks,complete_coefficient_checks=coefficient_check,
            count_backend_executed=False)
        cases.append(acquired)
        print(json.dumps(dict(n=n,acquired_rank=r,degree_certificate=acquired['certified_field_degree'],seconds=acquired['seconds'])),flush=True)
    return dict(status='all exact assertions passed',cases=cases,
        distinction='general representation acquisition executed; general point-count backend is a cited theorem')


if __name__=='__main__':
    data=run(); Path(__file__).with_name('field_bandwidth_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status=data['status'],cases=len(data['cases']))))
