#!/usr/bin/env python3
"""Author replay and exact algebra checks; not independent mathematical review."""
import hashlib,json,random
from fractions import Fraction as F
from pathlib import Path
import validated_clock as vc
ROOT=Path(__file__).resolve().parent

def check_contains(iv,x): assert F(iv.lo,vc.Q)<=x<=F(iv.hi,vc.Q)

def random_interval_checks():
    rng=random.Random(20261101)
    checked=0
    for _ in range(1000):
        aa=sorted([F(rng.randrange(-10000,10001),rng.randrange(1,100)) for _ in range(2)])
        bb=sorted([F(rng.randrange(-10000,10001),rng.randrange(1,100)) for _ in range(2)])
        a,b=vc.IV.bounds(*aa),vc.IV.bounds(*bb)
        for x in [aa[0],sum(aa)/2,aa[1]]:
            for y in [bb[0],sum(bb)/2,bb[1]]:
                check_contains(a+b,x+y);check_contains(a*b,x*y)
                if b.lo>0 or b.hi<0: check_contains(a/b,x/y)
                checked+=1
    return checked

def main():
    assert vc.selftest()
    samples=random_interval_checks()
    for x in [F(k,7) for k in range(1001)]:
        assert 1-2*x <= 1/(1+x)**2 <= 1-2*x+3*x*x
        assert 1/(1+x)**2-(1-2*x)==(3*x*x+2*x**3)/(1+x)**2
        assert 1-2*x+3*x*x-1/(1+x)**2==(4*x**3+3*x**4)/(1+x)**2
    results=[]
    intervals=[]
    for name in ['CERTIFICATE.json','CERTIFICATE_FINE.json']:
        saved=json.loads((ROOT/name).read_text())
        assert saved['code_sha256']==hashlib.sha256((ROOT/'validated_clock.py').read_bytes()).hexdigest()
        for k in vc.OPS: vc.OPS[k]=0
        assert vc.selftest()
        rerun=vc.solve(saved['taylor_order'],saved['grid_power'],int(saved['terminal_e']),saved['startup']['polynomial_degree'])
        ignored={'wall_nanoseconds_nonproof','arithmetic_selftest_pass','code_sha256'}
        for k,v in saved.items():
            if k not in ignored: assert rerun[k]==v,(name,k)
        lower,upper=map(F,[saved['s_star_lower'],saved['s_star_upper']])
        assert lower<=upper
        assert F(saved['s_star_decimal_outward'][0])<=lower
        assert upper<=F(saved['s_star_decimal_outward'][1])
        assert F(saved['startup_width'])+F(saved['inverse_taylor_and_rounding_width'])+F(saved['tail_width'])==upper-lower
        assert upper-lower<=F(saved['total_width_decimal_upper'])
        assert F(saved['sum_local_interval_widths'])<=F(saved['inverse_taylor_and_rounding_width'])
        intervals.append((lower,upper))
        results.append({'certificate':name,'exact_replay':True,'decimal_outward':True,'additive_error_ledger':True,'code_hash_matched':True})
    assert intervals[0][0]<=intervals[1][0]<=intervals[1][1]<=intervals[0][1]
    assert intervals[1][1]-intervals[1][0]<F(19,10**17)
    out={'status':'PASS_AUTHOR_SELF_CHECK_NOT_INDEPENDENT_REVIEW','random_endpoint_and_midpoint_combinations':samples,
         'exact_tail_identity_samples':1001,'coarse_contains_fine':True,'checks':results}
    (ROOT/'VERIFY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
