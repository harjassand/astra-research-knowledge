#!/usr/bin/env python3
"""Independent truth tables and split-product oracles for critical-ray counts."""
from homogeneous_chain_counter import *
from field_descent import extract_anf
from acquired_chain_counter import poly_mul
from quotient_height_boundary import signed_sum
import itertools,json,random,time

MONOMIALS=[(i,j,3-i-j) for i in range(4) for j in range(4-i)]

def run():
    cases=[];seed=28801;rng=random.Random(seed)
    specifications=[(3,e) for e in range(1,7)]+[(7,e) for e in (1,2,3)]+[(11,e) for e in (1,2)]
    for h,e in specifications:
        R=ChainRing(h,e);n=3*R.m;mask=(1<<R.m)-1;q=1<<R.d
        polynomials=[{(1,1,1):1},{(2,0,1):1,(1,1,1):1,(0,2,1):1},
            {(3,0,0):1,(0,3,0):1,(1,1,1):1}]
        for _ in range(5):
            P={a:rng.randrange(mask+1) for a in MONOMIALS};P[(1,1,1)]|=1
            polynomials.append({a:c for a,c in P.items() if c})
        for P in polynomials:
            start=time.perf_counter();value,certificate=homogeneous_sum(h,e,P)
            def phase(x):return R.functional(ring_polynomial(R,P,[(x>>(R.m*i))&mask for i in range(3)]))
            raw=extract_anf(phase,n);brute=signed_sum(raw,n)
            assert value==brute,(h,e,P,value,brute,certificate)
            if P=={(1,1,1):1}:assert value==q**(2*e-1)*(q+e*(q-1))
            cases.append(dict(h=h,e=e,n=n,polynomial=[dict(exponents=a,coefficient=c) for a,c in P.items()],
                signed_count=value,truth_count=brute,truth_points=1<<n,
                ray_count=len(certificate['rays']),certificate=certificate,seconds=time.perf_counter()-start))
        print(json.dumps(dict(h=h,e=e,n=n,completed=len(cases))),flush=True)
    large=[]
    for h,e in [(0x1009,2),(0x1009,5),(0x11b,8),(0x1009,32)]:
        R=ChainRing(h,e);q=1<<R.d;mask=(1<<R.m)-1
        rows=[[int(i==j) for j in range(3)] for i in range(3)]
        for _ in range(9):
            i,j=rng.sample(range(3),2);c=rng.randrange(mask+1)
            rows[i]=[a^R.mul(c,b) for a,b in zip(rows[i],rows[j])]
        P={(0,0,0):1}
        for row in rows:
            linear={tuple(int(j==i) for j in range(3)):c for i,c in enumerate(row) if c}
            P=poly_mul(R,P,linear)
        start=time.perf_counter();value,certificate=homogeneous_sum(h,e,P,terminal_bit_budget=0)
        oracle=q**(2*e-1)*(q+e*(q-1))
        assert value==oracle
        assert certificate['field_points_enumerated']==0
        large.append(dict(h=h,e=e,n=3*R.m,signed_count=value,reference=oracle,
            unit_determinant_factor_rows=rows,polynomial=[dict(exponents=a,coefficient=c) for a,c in P.items()],
            ray_count=len(certificate['rays']),certificate=certificate,seconds=time.perf_counter()-start))
        print(json.dumps(dict(stage='known split-product count',n=3*R.m,e=e,d=R.d,seconds=large[-1]['seconds'])),flush=True)
    output=dict(status='all assertions passed',cases=cases,large_cases=large,
        total_truth_points=sum(c['truth_points'] for c in cases),practical_speed_claim=False)
    Path(__file__).with_name('homogeneous_chain_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status=output['status'],cases=len(cases),large_cases=len(large),truth_points=output['total_truth_points'])))

if __name__=='__main__':run()
