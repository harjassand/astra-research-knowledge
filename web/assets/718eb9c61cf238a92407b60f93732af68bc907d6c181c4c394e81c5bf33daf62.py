"""Executed exact-rational time-one normal-map simulation for Sol.

This implements first-order Euler plus proved scalar error enclosures.
It is a restricted benchmark, not a generic interval ODE package.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import time

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c1',ROOT/'c1_certificate.py')
c1=importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)


def main():
    start=time.perf_counter()
    al,au=c1.initial.log_cat_bounds()
    scale=10**12
    al=c1.rational_floor(al,scale)
    au=c1.rational_floor(au,scale)+F(1,scale)
    rl,ru=c1.initial.sqrt_bounds(5,72)
    ll,lu=(3+rl)/2,(3+ru)/2
    il,iu=1/lu,1/ll
    n=128
    assert au<n
    plus_lower=(1+al/n)**n
    plus_euler_upper=(1+au/n)**n
    plus_remainder=lu*au*au/(2*n)
    plus_upper=plus_euler_upper+plus_remainder
    minus_lower=(1-au/n)**n
    minus_euler_upper=(1-al/n)**n
    minus_remainder=iu*au*au/(2*n*(1-au/n))
    minus_upper=minus_euler_upper+minus_remainder
    m=c1.rational_floor(plus_lower)
    cert=c1.step_cone(plus_lower,0,0,minus_upper,1,m)
    z=(m-1)/(m+1)
    log_lower=sum(2*z**(2*k+1)/(2*k+1) for k in range(64))
    rate=c1.rational_floor(log_lower)
    checks={
        'lambda_enclosed':plus_lower<=ll and lu<=plus_upper,
        'inverse_lambda_enclosed':minus_lower<=il and iu<=minus_upper,
        'normal_map_plus_width_lt_001':plus_upper-plus_lower<F(1,100),
        'normal_map_minus_width_lt_0002':minus_upper-minus_lower<F(1,500),
        'cone_from_executed_simulation':cert['status']=='CERTIFIED',
        'scalar_euler_positive':1-au/n>0,
        'positive_exact_log_entropy_lower':rate>0 and rate<=log_lower,
    }
    result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
            'steps':n,'a_lower':str(al),'a_upper':str(au),
            'plus_interval':list(map(str,(plus_lower,plus_upper))),
            'minus_interval':list(map(str,(minus_lower,minus_upper))),
            'display_plus_interval':list(map(float,(plus_lower,plus_upper))),
            'display_minus_interval':list(map(float,(minus_lower,minus_upper))),
            'cone_certificate':cert,'certified_entropy_lower':str(rate),
            'display_entropy_lower':float(rate),'elapsed_seconds':time.perf_counter()-start,
            'limits':'Executed scalar normal-map Euler benchmark with exact error bounds; no general flow, chart, net, or actuator implementation.'}
    (ROOT/'sol_interval_simulation_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','checks','steps','display_plus_interval','display_minus_interval','cone_certificate','display_entropy_lower','elapsed_seconds']},indent=2))
    if result['status']!='PASS':raise SystemExit(1)


if __name__=='__main__':main()
