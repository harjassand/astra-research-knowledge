"""Exact rational C1-generator and finite-step cone certificates.

Finite tests validate certificate arithmetic and exact benchmark identities.
No generic ODE solver, native field interval compiler, or physical device.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import math
import time
import sympy as z

PARENT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('initial_certificate', PARENT/'certificate_checks.py')
initial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(initial)


def arctan_bounds(x, terms):
    x = F(x)
    partial = sum((-1)**k * x**(2*k+1)/(2*k+1) for k in range(terms))
    next_term = (-1)**terms*x**(2*terms+1)/(2*terms+1)
    return min(partial, partial+next_term), max(partial, partial+next_term)


def pi_bounds(terms=36):
    lo5, hi5 = arctan_bounds(F(1,5), terms)
    lo239, hi239 = arctan_bounds(F(1,239), terms)
    return 16*lo5-4*hi239, 16*hi5-4*lo239


def rational_floor(x, denominator=10**12):
    x = F(x)
    return F((x.numerator*denominator)//x.denominator,denominator)


def full_cone(a_lower, delta_upper, alpha, rate):
    a, d, al, rate = map(F,(a_lower,delta_upper,alpha,rate))
    if min(a,d,al,rate) < 0 or a == 0 or al == 0:
        return {'status':'REJECTED_INPUT'}
    _, root_upper = initial.sqrt_bounds(1+al*al)
    passed = d*(1+al*al) <= a*al and 0 < rate <= a-d*root_upper
    return {'status':'CERTIFIED' if passed else 'UNKNOWN','a_lower':str(a),
            'generator_error_upper':str(d),'alpha':str(al),'entropy_lower':str(rate) if passed else None}


def step_cone(a_lower,b_upper,c_upper,d_upper,alpha,m):
    a,b,c,d,al,m=map(F,(a_lower,b_upper,c_upper,d_upper,alpha,m))
    if min(a,b,c,d,al)<0 or al==0:
        return {'status':'REJECTED_INPUT'}
    passed=(m>1 and m<=a-b*al and c+d*al<=al*(a-b*al))
    return {'status':'CERTIFIED' if passed else 'UNKNOWN',
            'expansion_lower':str(m) if passed else None,
            'entropy_lower':'log(expansion_lower)/T' if passed else None}


def main():
    start=time.perf_counter()
    a_lo,a_hi=initial.log_cat_bounds()
    pi_lo,pi_hi=pi_bounds()
    eps=F(1,100)
    _, delta_hi=initial.sqrt_bounds(eps*eps*(4*pi_hi*pi_hi+a_hi*a_hi))
    _, rt2=initial.sqrt_bounds(2)
    rate=rational_floor(a_lo-rt2*delta_hi)
    cert=full_cone(a_lo,delta_hi,1,rate)
    c1_noise=F(1,100)
    noisy_rate=rational_floor(a_lo-rt2*(delta_hi+c1_noise))
    noisy=full_cone(a_lo,delta_hi+c1_noise,1,noisy_rate)
    failed=full_cone(1,F(3,5),1,F(1,10))
    # Use simple rational enclosures of lambda and inverse lambda.
    rl,ru=initial.sqrt_bounds(5)
    lam_lo=(3+rl)/2
    lam_hi=(3+ru)/2
    inv_hi=1/lam_lo
    epsilon_map=F(1,2)
    m=rational_floor(lam_lo-2*epsilon_map)
    step=step_cone(lam_lo-epsilon_map,epsilon_map,epsilon_map,
                   inv_hi+epsilon_map,1,m)
    threshold=step_cone(F(5,2)-F(3,5),F(3,5),F(3,5),F(2,5)+F(3,5),1,F(11,10))
    # Directly check full-cone boundary inequality and benchmark matrix.
    a,g=z.symbols('a g',real=True)
    G=z.Matrix([[0,0,0],[g,a,0],[0,0,-a]])
    S=(G+G.T)/2
    lam=z.Symbol('lambda')
    u,v0,vs,al,de=z.symbols('u v0 vs alpha delta',real=True)
    norm_boundary=al*(1+al*al)*u*u
    checks={
        'inhomogeneous_triangular_characteristic':z.simplify(G.charpoly().as_expr()-lam*(lam-a)*(lam+a))==0,
        'inhomogeneous_strain_norm':z.simplify(z.trace(S*S)-2*a*a-g*g/2)==0,
        'cone_boundary_noise_product':z.simplify((al*al+al**4)*(1+al*al)-al*al*(1+al*al)**2)==0,
        'pi_enclosure_width':pi_hi-pi_lo<F(1,10**20),
        'sinusoidal_native_c1_certificate':cert['status']=='CERTIFIED',
        'additional_generator_noise_certificate':noisy['status']=='CERTIFIED',
        'excess_noise_stays_unknown':failed['status']=='UNKNOWN',
        'half_unit_map_error_certificate':step['status']=='CERTIFIED',
        'map_threshold_stays_unknown':threshold['status']=='UNKNOWN',
    }
    result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
            'sinusoidal_epsilon':str(eps),'certified_entropy_lower':str(rate),
            'display_entropy_lower':float(rate),'display_exact_entropy':float((a_lo+a_hi)/2),
            'additional_generator_noise':str(c1_noise),'noisy_entropy_lower':str(noisy_rate),
            'display_noisy_entropy_lower':float(noisy_rate),
            'sinusoidal_native_C1':cert,'additional_noise_C1':noisy,
            'finite_step':step,'pi_bounds':{'lower':str(pi_lo),'upper':str(pi_hi)},
            'elapsed_seconds':time.perf_counter()-start,
            'limits':'Admitted rational inequalities and exact Sol benchmark only; no general field acquisition or ODE simulation executed.'}
    (Path(__file__).parent/'c1_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','checks','display_entropy_lower','display_exact_entropy','display_noisy_entropy_lower','elapsed_seconds']},indent=2))
    if result['status']!='PASS':raise SystemExit(1)


if __name__=='__main__':main()
