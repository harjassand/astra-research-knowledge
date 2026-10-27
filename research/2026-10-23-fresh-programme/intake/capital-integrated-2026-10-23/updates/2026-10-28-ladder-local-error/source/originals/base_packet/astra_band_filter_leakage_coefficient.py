#!/usr/bin/env python3
"""Parity-resolved spectral-band leakage: analytic positive two-photon shell.
Ideal + emitter couples only upper chain, - only lower. Added wrong-band
couplings of amplitude delta*g retain parity but open same-parity two-photon channels.
Outputs are exact leading g->0 radiative coefficients, not finite-g decay tests.
"""
import numpy as np, math, json
from scipy.integrate import quad
sqrt3=math.sqrt(3)
a=4-2*sqrt3
b=4/sqrt3-2
Jexact=16/(27*math.pi**2)

def spectral_density(E,c):
    t=E-c
    return (2/math.pi)*math.sqrt(max(0,1-t*t)) if abs(t)<=1 else 0.

def nu(E,delta,parity):
    if parity==1:
        upper=2.;lower=delta**2
    else:
        upper=delta**2;lower=1.
    return (upper*spectral_density(E,5)+lower*spectral_density(E,1))/(E-3)**2

def coefficient(delta):
    arr=[]
    for parity in (1,-1):
        res=0.
        for lo,hi in [(0,2),(4,6)]:
            res+=quad(lambda E:nu(E,delta,parity)*nu(6-E,delta,parity),lo,hi,epsabs=1e-14)[0]
        arr.append(res)
    c=sum(arr)/2
    deltaF=-(3-2*delta**2)*a
    deltaFp=-b
    predicted_c=3*delta**2*Jexact
    gamma=math.pi*deltaF**2*c
    return dict(delta=delta,parity_plus_shell=arr[0],parity_minus_shell=arr[1],
                c_numerical=c,c_exact=predicted_c,c_abs_diff=abs(c-predicted_c),
                connected_shift_coef=-(3-2*delta**2)*a*b,
                radiative_amplitude_width_coef=gamma,
                gamma_closed_formula=16*a*a*(3-2*delta**2)**2*delta**2/(9*math.pi),
                gamma_error=abs(gamma-16*a*a*(3-2*delta**2)**2*delta**2/(9*math.pi)))

if __name__=='__main__':
    out=dict(ideal_decoupling_leakage_zero=True,J_exact=Jexact,
       leakage_leading_gamma_over_g8_delta2=16*a*a/math.pi,
       cases=[coefficient(z) for z in (0.,.01,.05,.1,.2,.4,1.)])
    assert max(x['c_abs_diff'] for x in out['cases'])<1e-12
    assert max(x['gamma_error'] for x in out['cases'])<1e-12
    with open('/mnt/data/astra_band_filter_leakage_coefficient_results.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))
