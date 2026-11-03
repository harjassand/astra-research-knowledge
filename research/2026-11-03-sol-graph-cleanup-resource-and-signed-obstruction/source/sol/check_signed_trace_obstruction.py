#!/usr/bin/env python3
"""Exact full five-state signed-debt trace and asymptotic obstruction."""
from fractions import Fraction as F
from pathlib import Path
import sympy as S
import json

P=Path(__file__).resolve().parent

def solve(n,div):
    q4=12*n*n+8;t4=div(1,q4);p4=div(12*n*(n-1),q4)
    d4=div(12*n*n+36*n+22,q4)
    b4=div(9+54+12*n*16+1+12*n*(n-1),q4)
    q3=2*n+2;r3=2*(n-1)
    t3=div(1,q3)+div(r3,q3)*t4
    p3=div(r3,q3)*p4
    d3=div(1+r3*d4,q3);b3=div(1+r3*b4,q3)
    t2=F(1,2)+t3/2;p2=p3/2;d2=(1+d3)/2;b2=(1+b3)/2
    q1=48*n*(n+1)+24*(n+1)+10;r1=48*n*(n+1)
    t1=div(1,q1)+div(r1,q1)*t2;p1=div(r1,q1)*p2
    d1=div(144*n+192+r1*d2,q1)
    b1=div(9*25+24*(n+1)*36+9+r1*b2,q1)
    q0=6*n+5;r0=6*n
    t0=div(1,q0)+div(r0,q0)*t1;p0=div(r0,q0)*p1
    d0=div(8+r0*d1,q0);b0=div(16+r0*b1,q0)
    return t0,p0,d0,b0

def main():
    n=S.Symbol('n',integer=True,positive=True)
    expr=solve(n,lambda a,b:S.sympify(a)/b)
    limits=[S.limit(v,n,S.oo) for v in expr]
    assert limits[:3]==[S.Rational(1,2),S.Rational(1,2),1]
    assert limits[3]==1
    checks=[]
    for nn in (2,3,10,30,100,10**6):
        time,success,drift,second=solve(nn,F)
        assert time>0 and drift>0 and second>0 and 0<success<1
        zin=2*nn+12
        checks.append({'n':nn,'physical_time':str(time),'success_probability':str(success),
                       'mean_delta_Z':str(drift),'second_delta_Z':str(second),
                       'quadratic_change_plus_clock':str(2*zin*drift+second+time),
                       'float_mean_delta_Z':float(drift),'float_physical_time':float(time)})
    result={'scope':'Exact obstruction to this finite stop at every increasing receiver of Z. Not a recurrence counterexample.',
            'possible_endpoint_Z_increments':[0,1,2,3,4,5,6],
            'symbolic_limits_time_success_drift_second':[str(v) for v in limits],
            'exact_checks':checks}
    (P/'results/signed_trace_obstruction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'symbolic_limits':result['symbolic_limits_time_success_drift_second'],
                      'checks':[{'n':v['n'],'mean_delta_Z':v['float_mean_delta_Z'],'time':v['float_physical_time']} for v in checks]},indent=2))

if __name__=='__main__':main()
