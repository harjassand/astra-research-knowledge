#!/usr/bin/env python3
"""Truth-table checks for singular cubic phases with dense quotient noise."""
from homogeneous_chain_counter import *
from field_descent import extract_anf,random_invertible
from quotient_height_boundary import signed_sum
from homogeneous_chain_checks import MONOMIALS
import itertools,json,random,time

def toggle(poly,term):
    if term in poly:poly.remove(term)
    else:poly.add(term)

def quotient_noise(R,height,rng):
    m=3*R.d*height;rank=m-m%2;rows=random_invertible(m,rng)
    columns=[];mask=(1<<(R.d*height))-1
    for row in rows[:rank]:
        columns.append(sum(((row>>(i*R.d*height))&mask)<<(R.m*i) for i in range(3)))
    Q={0} if rng.randrange(2) else set()
    for a,b in zip(columns[::2],columns[1::2]):
        aa=[i for i in range(3*R.m) if (a>>i)&1]
        bb=[i for i in range(3*R.m) if (b>>i)&1]
        for i in aa:
            for j in bb:toggle(Q,(1<<i)|(1<<j))
    return Q,rank

def run():
    rng=random.Random(593106);cases=[]
    specifications=[(3,e) for e in range(2,9)]+[(7,e) for e in (2,3,4)]+[(11,2)]
    for h,e in specifications:
        R=ChainRing(h,e);n=3*R.m;mask=(1<<R.m)-1;height=(e+1)//3
        residue_polynomials=[{(1,1,1):1},{(2,0,1):1,(1,1,1):1,(0,2,1):1},
            {(3,0,0):1,(0,3,0):1,(1,1,1):1},
            {(2,0,1):1,(0,3,0):1,(0,0,3):1,(1,1,1):1}]
        for residue in residue_polynomials:
            for nilpotent in (False,True):
                P={a:residue.get(a,0)^(rng.randrange(1<<(R.m-R.d))<<R.d if nilpotent else 0) for a in MONOMIALS}
                P={a:c for a,c in P.items() if c};Q,rank=quotient_noise(R,height,rng)
                start=time.perf_counter();value,certificate=weighted_homogeneous_sum(h,e,P,Q)
                def phase(x):return R.functional(ring_polynomial(R,P,[(x>>(R.m*i))&mask for i in range(3)]))^polynomial_value(Q,x)
                raw=extract_anf(phase,n);brute=signed_sum(raw,n)
                assert value==brute,(h,e,P,Q,value,brute,certificate)
                cases.append(dict(h=h,e=e,n=n,quotient_height=height,quadratic_rank=rank,
                    polynomial=[dict(exponents=a,coefficient=c) for a,c in P.items()],quadratic_anf=sorted(Q),
                    nilpotent_coefficients_randomized=nilpotent,signed_count=value,truth_count=brute,
                    truth_points=1<<n,ray_count=len(certificate['rays']),certificate=certificate,
                    seconds=time.perf_counter()-start))
        print(json.dumps(dict(h=h,e=e,n=n,completed=len(cases))),flush=True)
    R=ChainRing(0x1009,2);q=1<<R.d;Q,rank=quotient_noise(R,1,rng);P={(1,1,1):1}
    start=time.perf_counter();value,certificate=weighted_homogeneous_sum(R.h,R.e,P,Q,terminal_bit_budget=0)
    # Independent highest-digit orthogonality for XYZ at depth two leaves the three residue axes.
    axis=[quadratic_sum(lambda x,i=i:polynomial_value(Q,x<<(i*R.m)),R.d) for i in range(3)]
    reference=q**3*(sum(axis)-2*(1-2*int(0 in Q)))
    assert value==reference
    large=dict(h=R.h,e=R.e,n=3*R.m,quadratic_rank=rank,quotient_height=1,quadratic_anf=sorted(Q),
        signed_count=value,reference=reference,axis_gaussians=axis,certificate=certificate,
        seconds=time.perf_counter()-start)
    output=dict(status='all assertions passed',cases=cases,large_case=large,
        total_truth_points=sum(c['truth_points'] for c in cases),practical_speed_claim=False)
    Path(__file__).with_name('weighted_homogeneous_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status=output['status'],cases=len(cases),truth_points=output['total_truth_points'],
        large_n=large['n'],large_rank=rank,large_signed_count=value)))

if __name__=='__main__':run()
