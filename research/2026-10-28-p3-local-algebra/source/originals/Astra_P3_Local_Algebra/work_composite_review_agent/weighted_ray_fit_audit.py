#!/usr/bin/env python3
"""Independent weighted transverse tests and complete quotient-fit kernel audit."""
from pathlib import Path
import itertools,json,random,sys
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_chain_root','work_stationary_prior_agent'):
    sys.path.insert(0,str(ROOT/folder))
from homogeneous_chain_counter import *
from quotient_homogeneous_compiler import ordinary_quadratic_models,monomials_of_degree
from field_descent import extract_anf,kernel_columns,bits
from top_digit_deflation_audit import brute_sum


def kernel_audit(h,e,height):
    R=ChainRing(h,e);n=3*R.m
    exponents=[a for total in range(4) for a in monomials_of_degree(total)
               if a!=(1,1,1) and not(total==2 and 2 in a)]
    models,labels=ordinary_quadratic_models(R,exponents)
    low=sum(((1<<(R.d*height))-1)<<(R.m*i) for i in range(3))
    protected=sorted({term for model in models for term in model if term&~low})
    position={term:i for i,term in enumerate(protected)}
    columns=[sum(1<<position[term] for term in model if term in position) for model in models]
    relations=kernel_columns(columns)
    forbidden=(1<<(R.d*(e-height)))-1
    witnesses=[]
    for relation in relations:
        P={}
        for i in bits(relation):
            exponent,coefficient=labels[i];P[exponent]=P.get(exponent,0)^coefficient
        bad={ex:c for ex,c in P.items() if sum(ex)>0 and c&forbidden}
        if bad:witnesses.append([dict(exponents=list(ex),coefficient=c) for ex,c in bad.items()])
    return dict(h=h,d=R.d,e=e,height=height,model_columns=len(columns),
        protected_rows=len(protected),kernel_dimension=len(relations),
        predicted_dimension=15*R.d*height+R.m,valuation_violations=witnesses)


def run():
    rng=random.Random(210883);transverse=[]
    for h,e in [(3,3),(3,4),(3,7),(7,3),(7,4),(7,5),(11,3)]:
        R=ChainRing(h,e);q=1<<R.d;mask=(1<<R.m)-1;depth=e//2
        ids=[i*R.m+j for i in range(3) for j in range(R.d*depth)]
        for trial in range(2):
            A,B,C,D,E,F,c=[rng.randrange(mask+1) for _ in range(7)]
            mu=(rng.randrange(mask+1)&~R.mask)^rng.randrange(1,q)
            radial=(rng.randrange(mask+1)&~R.mask)^rng.randrange(1,q)
            critical=[rng.randrange(mask+1),rng.randrange(mask+1),1]
            P={(0,0):c,(2,0):A,(1,1):mu,(0,2):B,
               (3,0):C,(2,1):D,(1,2):E,(0,3):F}
            Q={0} if rng.randrange(2) else set()
            for i in ids:
                if rng.randrange(2):Q.add(1<<i)
            for i,j in itertools.combinations(ids,2):
                if rng.randrange(2):Q.add((1<<i)|(1<<j))
            r3=R.mul(radial,R.mul(radial,radial));width=R.d*(e-1)
            def phase(x):
                u=(x&((1<<width)-1))<<R.d;v=(x>>width)<<R.d
                coordinates=[critical[0]^u,critical[1]^v,1]
                ambient=sum(R.mul(radial,z)<<(R.m*i) for i,z in enumerate(coordinates))
                return R.functional(R.mul(r3,ring_polynomial(R,P,[u,v])))^polynomial_value(Q,ambient)
            raw=extract_anf(phase,2*width);actual=brute_sum(raw,2*width)
            inv=gf_pow(mu&R.mask,q-2,h)
            arf=gf_trace(gf_mul(gf_mul(A&R.mask,B&R.mask,h),gf_mul(inv,inv,h),h),h)
            ambient=sum(R.mul(radial,z)<<(R.m*i) for i,z in enumerate(critical))
            parity=R.functional(R.mul(r3,c))^polynomial_value(Q,ambient)^((e&1)*arf)
            expected=(1-2*parity)*q**e
            assert actual==expected
            transverse.append(dict(h=h,d=R.d,e=e,local_allowed_height=depth,trial=trial,
                exact_sum=actual,enumerated_points=1<<(2*width),arf_bit=arf,
                quotient_Q=sorted(Q),radial_unit=radial,critical_vector=critical))
    h,e=7,3;R=ChainRing(h,e);q=1<<R.d;width=R.d*(e-1)
    def cancelled(x):
        u=(x&((1<<width)-1))<<R.d;v=(x>>width)<<R.d
        Q=gf_trace(gf_mul((u>>R.d)&R.mask,(v>>R.d)&R.mask,h),h)
        return R.functional(R.mul(u,v))^Q
    failure_sum=brute_sum(extract_anf(cancelled,2*width),2*width)
    assert failure_sum==q**4 and failure_sum!=q**3
    boundary=dict(d=R.d,e=e,allowed_height=1,perturbation_height=2,
                  actual_transverse_sum=failure_sum,incorrect_extracted_weight_sum=q**3)
    revival=[]
    for h in (11,19):
        R=ChainRing(h,5);q=1<<R.d;c=1<<(3*R.d)
        P={(1,1,1):1,(0,0,3):c}
        small=extract_anf(lambda z:R.functional(R.mul(c,R.mul(z,R.mul(z,z)))),2*R.d)
        Q={term<<(2*R.m) for term in small}
        value,cert=weighted_homogeneous_sum(h,5,P,Q,terminal_bit_budget=0)
        expected=q**9*(q+5*(q-1));assert value==expected
        ray=next(r for r in cert['rays'] if r['residue']==[0,0,1])
        unweighted=unit_radial_sum(h,5,ray['critical_value'])
        weighted,_=weighted_radial_sum(R,ray,Q)
        assert unweighted==0 and weighted==(q-1)*q**4
        revival.append(dict(d=R.d,e=5,n=3*R.m,c=c,quotient_Q=sorted(Q),
            unweighted_radial=unweighted,weighted_radial=weighted,
            exact_count=value,known_XYZ_count=expected))
    kernels=[]
    for h,e,height in [(11,2,0),(11,2,1),(11,3,1),(11,5,2),(19,4,1),(11,5,3),(11,3,3)]:
        result=kernel_audit(h,e,height)
        assert not result['valuation_violations'] and result['kernel_dimension']==result['predicted_dimension']
        kernels.append(result)
    small_field=kernel_audit(7,2,0)
    assert small_field['valuation_violations']
    bounds=[]
    for e in range(2,101):
        for height in range(e+1):
            delta=max(0,height-(e+1)//3);current=e;current_height=height
            while current>=4 and 2*current_height<=current:
                current-=3;current_height=max(0,current_height-1)
            residual=current if (current>=2 and 2*current_height>current) or current==1 else 0
            claimed=min(e,max(1,6*delta-1))
            assert residual<=claimed
            if residual and (e%3==2 or (e,height)==(4,2)):
                bounds.append(dict(e=e,height=height,delta=delta,residual_depth=residual,claimed_bound=claimed))
    output=dict(status='all exact assertions passed',weighted_transverse_cases=transverse,
        sharp_local_height_failure=boundary,revived_rays=revival,
        quotient_fit_kernel_cases=kernels,small_field_alias_failure=small_field,
        adaptive_depth_bound_cases_checked=sum(e+1 for e in range(2,101)),
        selected_adaptive_bound_cases=bounds)
    Path(__file__).with_name('weighted_ray_fit_audit_results.json').write_text(json.dumps(output,indent=2)+'\n')
    return output


if __name__=='__main__':
    out=run();print(json.dumps(dict(status=out['status'],weighted_transverse=len(out['weighted_transverse_cases']),
        revived_rays=len(out['revived_rays']),complete_kernel_cases=len(out['quotient_fit_kernel_cases']),
        bound_pairs=out['adaptive_depth_bound_cases_checked'],failures=2)))
