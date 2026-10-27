#!/usr/bin/env python3
from singular_ray_quadratic import *
from smooth_ring_checks import raw_from,serial
from pathlib import Path
import random,json

def main():
    rng=random.Random(202610280111); rows=[]; large=[]
    for h,e,reps in [(3,2,12),(3,3,12),(3,5,8),(7,2,8),(7,3,2),(11,2,2)]:
        R=ChainRing(h,e); depth=(e+1)//3; n=3*R.d*e
        for rep in range(reps):
            if rep%3==0: H={(1,1,1):R.one}
            else:
                H={m:tuple(rng.randrange(R.q) for _ in range(e)) for m in CUBICS}
                H[(1,1,1)]=(rng.randrange(1,R.q),)+H[(1,1,1)][1:]
                H={m:c for m,c in H.items() if any(c)}
            ids=[i for i in range(n) if quotient_bitmask(R,depth)>>i&1]
            Q={0} if rng.randrange(2) else set()
            for i in ids:
                if rng.randrange(2): Q.add(1<<i)
            for i,j in combinations(ids,2):
                if rng.randrange(2): Q.add((1<<i)|(1<<j))
            ans,ev=homogeneous_quotient_sum(R,H,Q,details=True)
            raw=raw_from(R,H,Q); brute=sum(1-2*polynomial_value(raw,x) for x in range(1<<n))
            assert ans==brute,(h,e,rep,H,Q,ans,brute,ev)
            rows.append(dict(h=h,e=e,n=n,H=serial(H),Q=sorted(Q),signed_count=ans,evidence=ev))
        print('passed',h,e,reps,flush=True)
    for h,e in [(11,11),(11,12),(19,11),(19,12)]:
        R=ChainRing(h,e); H={(1,1,1):R.one}; ans,ev=homogeneous_quotient_sum(R,H,set(),details=True)
        expected=pow(R.q,2*e)+e*(R.q-1)*pow(R.q,2*e-1)
        assert ans==expected
        large.append(dict(h=h,e=e,n=3*R.d*e,signed_count=ans,independent_xyz_formula=expected,evidence=ev))
    out=dict(full_comparisons=len(rows),rows=rows,large_xyz=large)
    Path(__file__).with_name('singular_ray_quadratic_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('saved',len(rows),'full comparisons and',len(large),'large cases')
if __name__=='__main__': main()
