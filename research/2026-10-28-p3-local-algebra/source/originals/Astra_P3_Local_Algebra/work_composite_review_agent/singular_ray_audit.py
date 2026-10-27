#!/usr/bin/env python3
"""Independent local character sums and projective coverage for singular rays."""
from pathlib import Path
import itertools,json,random,sys
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_chain_root','work_stationary_prior_agent'):
    sys.path.insert(0,str(ROOT/folder))
from homogeneous_chain_counter import *
from field_descent import extract_anf
from top_digit_deflation_audit import brute_sum


def run():
    rng=random.Random(728192);transverse=[];radial=[];coverage=[]
    for h,e in [(3,2),(3,3),(3,4),(3,8),(7,3),(7,5),(11,3),(11,4)]:
        R=ChainRing(h,e);q=1<<R.d;mask=(1<<R.m)-1
        for trial in range(4):
            coefficients=[rng.randrange(mask+1) for _ in range(7)]
            A,B,C,D,E,F,c=coefficients
            mu=(rng.randrange(mask+1)&~R.mask)^rng.randrange(1,q)
            r=(rng.randrange(mask+1)&~R.mask)^rng.randrange(1,q)
            P={(0,0):c,(2,0):A,(1,1):mu,(0,2):B,
               (3,0):C,(2,1):D,(1,2):E,(0,3):F}
            r3=R.mul(r,R.mul(r,r));width=R.d*(e-1)
            def phase(x):
                u=(x&((1<<width)-1))<<R.d
                v=(x>>width)<<R.d
                return R.functional(R.mul(r3,ring_polynomial(R,P,[u,v])))
            raw=extract_anf(phase,2*width)
            assert all(term.bit_count()<=2 for term in raw)
            actual=brute_sum(raw,2*width)
            inv=gf_pow(mu&R.mask,q-2,h)
            arf=gf_trace(gf_mul(gf_mul(A&R.mask,B&R.mask,h),gf_mul(inv,inv,h),h),h)
            expected=q**e
            if (e&1) and arf:expected=-expected
            if R.functional(R.mul(r3,c)):expected=-expected
            assert actual==expected,(h,e,trial,P,r,actual,expected)
            transverse.append(dict(h=h,d=R.d,e=e,trial=trial,ring_coefficients=coefficients,
                mixed_quadratic_coefficient=mu,radial_unit=r,arf_bit=arf,
                exact_sum=actual,enumerated_points=1<<(2*width)))
        values=[0]
        for valuation in sorted(set([0,max(0,e-2),e-1])):
            value=rng.randrange(1,q)<<(R.d*valuation)
            for j in range(valuation+1,e):value^=rng.randrange(q)<<(R.d*j)
            values.append(value)
        for c in values:
            direct=sum(1-2*R.functional(R.mul(c,R.mul(r,R.mul(r,r))))
                       for r in range(mask+1) if r&R.mask)
            fast=unit_radial_sum(h,e,c)
            assert direct==fast
            radial.append(dict(h=h,d=R.d,e=e,c=c,exact_sum=direct,
                enumerated_units=(q-1)*q**(e-1)))
    cubics=[(i,j,3-i-j) for i in range(4) for j in range(4-i)]
    for h in (7,11,19):
        F=ChainRing(h,1);q=1<<F.d
        b=next(v for v in range(q) if gf_trace(v,h))
        polys=[{(1,1,1):1},
               {(2,0,1):1,(1,1,1):1,(0,2,1):b},
               {(3,0,0):1,(0,3,0):1,(1,1,1):1},
               {(2,0,1):1,(0,3,0):1,(0,0,3):1,(1,1,1):1}]
        for _ in range(4):
            P={ex:rng.randrange(q) for ex in cubics};P[(1,1,1)]=rng.randrange(1,q)
            polys.append({ex:c for ex,c in P.items() if c})
        for P in polys:
            gradients=[derivative(P,i) for i in range(3)]
            direct=[]
            for chart in range(3):
                for lower in itertools.product(range(q),repeat=chart):
                    point=list(lower)+[1]+[0]*(2-chart)
                    if not any(ring_polynomial(F,g,point) for g in gradients):direct.append(tuple(point))
            found=[tuple(p['residue']) for p in critical_rays(h,P)]
            assert sorted(found)==sorted(direct) and len(found)<=3
            coverage.append(dict(h=h,d=F.d,polynomial=[dict(exponents=list(ex),coefficient=c) for ex,c in P.items()],
                                 exact_projective_rays=found,enumerated_projective_points=q*q+q+1))
    result=dict(status='all exact assertions passed',transverse_cases=transverse,
                radial_cases=radial,coverage_cases=coverage,
                scope='independent transverse truth tables, direct unit sums, and exhaustive projective coverage; no full-counter suite repetition')
    Path(__file__).with_name('singular_ray_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    result=run();print(json.dumps(dict(status=result['status'],transverse=len(result['transverse_cases']),
        radial=len(result['radial_cases']),projective_coverage=len(result['coverage_cases']))))
