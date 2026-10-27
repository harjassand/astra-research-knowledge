#!/usr/bin/env python3
"""Nonsplit nodal residues and adaptive residuals above the quotient bound."""
from homogeneous_chain_counter import *
from weighted_homogeneous_checks import quotient_noise
from quotient_height_boundary import polynomial,signed_sum
from field_descent import extract_anf
from homogeneous_chain_checks import MONOMIALS
import json,random

def run():
    rng=random.Random(80123);nodal=[];tails=[]
    # At (0,0,1) the tangent cone x^2+xy+y^2 is nonsplit over F_(2^odd).
    residue={(2,0,1):1,(1,1,1):1,(0,2,1):1,(3,0,0):1}
    for h,e in [(3,2),(3,3),(3,5),(3,8),(11,2)]:
        R=ChainRing(h,e);n=3*R.m;mask=(1<<R.m)-1
        for random_tail in [False,True]:
            P={a:residue.get(a,0)^(rng.randrange(1<<(R.m-R.d))<<R.d if random_tail else 0) for a in MONOMIALS}
            P={a:c for a,c in P.items() if c};Q,rank=quotient_noise(R,(e+1)//3,rng)
            value,cert=weighted_homogeneous_sum(h,e,P,Q)
            assert len(cert['rays'])==1 and cert['rays'][0]['arf_sign']==-1
            def phase(x):return R.functional(ring_polynomial(R,P,[(x>>(i*R.m))&mask for i in range(3)]))^polynomial_value(Q,x)
            brute=signed_sum(extract_anf(phase,n),n);assert value==brute
            nodal.append(dict(h=h,e=e,n=n,random_nilpotent_coefficients=random_tail,rank=rank,
                polynomial=[dict(exponents=a,coefficient=c) for a,c in P.items()],quadratic_anf=sorted(Q),
                signed_count=value,truth_count=brute,truth_points=1<<n,certificate=cert))
    smooth={(2,0,1):1,(0,3,0):1,(0,0,3):1,(1,1,1):1}
    for e in range(1,9):
        h0=(e+1)//3;R=ChainRing(3,e);n=3*e
        variables=(0,2) if e%3==1 else (0,1)
        extra=(1<<(variables[0]*e+h0))|(1<<(variables[1]*e+h0));Q={extra}
        value,cert=weighted_homogeneous_sum(3,e,smooth,Q,residual_bit_budget=15)
        raw=polynomial(e)
        if extra in raw:raw.remove(extra)
        else:raw.add(extra)
        brute=signed_sum(raw,n);assert value==brute
        assert cert.get('residual_variables',0)<=15
        tails.append(dict(e=e,n=n,height=h0+1,signed_count=value,truth_count=brute,
            truth_points=1<<n,certificate=cert))
    out=dict(status='all assertions passed',nonsplit_nodal_cases=nodal,above_height_cases=tails,
        total_truth_points=sum(c['truth_points'] for c in nodal+tails),practical_speed_claim=False)
    Path(__file__).with_name('critical_ray_extension_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],nonsplit_nodal_cases=len(nodal),above_height_cases=len(tails),
        truth_points=out['total_truth_points'],maximum_residual_variables=max(c['certificate']['residual_variables'] for c in tails))))

if __name__=='__main__':run()
