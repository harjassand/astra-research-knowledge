#!/usr/bin/env python3
"""Exact finite checks; analytic proofs are in HEAT_TO_CRITICAL_TRACE.md."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parent
ASTRA = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-compensation-exchange')
EXPECTED_PIN = '00631610750c708263d5cf6d812ebbb8edc77335'


def main() -> None:
    actual_pin = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ASTRA, text=True).strip()
    assert actual_pin == EXPECTED_PIN
    a, b, c, d, w, q, s, t, h = sp.symbols('a b c d w q s t h', real=True)
    A = sp.Matrix([[a, b], [c, d]])
    u, v = a*a+c*c, b*b+d*d
    ww, qq = a*b+c*d, A.det()
    f = u*u+v*v+4*ww*ww+sp.Rational(7, 2)*qq*qq-sp.Rational(29, 10)*qq*(u+v)
    assert sp.expand(u*v-ww*ww-qq*qq) == 0
    rewrite = (u+v)**2+2*ww**2+sp.Rational(3, 2)*qq**2-sp.Rational(29, 10)*qq*(u+v)
    assert sp.expand(f-rewrite) == 0
    assert f.subs({a:1,b:0,c:0,d:1}) == -sp.Rational(3, 10)
    assert sp.expand(f.subs({a:-a,b:-b,c:-c,d:-d})-f) == 0

    # Envelope signs hold on -1/2 <= t <= 1/2 because the factors below
    # are nonnegative there. They do not rely on sampled eigenvalues.
    lower = 1+sp.Rational(3,2)*t*t-sp.Rational(29,10)*t
    upper = sp.Rational(3,2)-sp.Rational(1,2)*t*t-sp.Rational(29,10)*t
    assert sp.expand(lower+sp.Rational(3,40)-(sp.Rational(1,2)-t)*(sp.Rational(43,20)-sp.Rational(3,2)*t)) == 0
    assert sp.expand(sp.Rational(113,40)-upper-(t+sp.Rational(1,2))*(sp.Rational(53,20)+sp.Rational(1,2)*t)) == 0

    # R_H(B,A) with |A|=1, B=t A+Bperp and |Bperp|=h.
    rem = 6*t*t+2*h*h+4*t+1
    completion = sp.Rational(23,4)*(t+sp.Rational(8,23))**2+sp.Rational(7,4)*h*h+sp.Rational(5,92)
    assert sp.expand(rem-sp.Rational(1,4)*(t*t+h*h+1)-completion) == 0

    # Circular profile: the y average is already constant pointwise.
    x, r, p = sp.symbols('x r p', real=True)
    radial = p**4+r**4+sp.Rational(7,2)*p*p*r*r-sp.Rational(29,10)*p*r*(p*p+r*r)
    ramp = sp.integrate(radial.subs({r:x/2,p:sp.Rational(1,2)}), (x,0,1))
    assert ramp == sp.Rational(23,1920)
    exponential = sp.integrate(radial.subs(p,r)/r, (r,sp.Rational(1,2),1))
    assert exponential == -sp.Rational(9,128)
    entry = ramp+exponential
    assert entry == -sp.Rational(7,120)
    assert sp.expand(radial.subs({p:-p,r:-r})-radial) == 0

    rho = sp.Rational(1,500)
    epsilon = rho/24
    assert epsilon == sp.Rational(1,12000)
    M = sp.Rational(113,40)
    K1 = sp.Rational(4)+4+sp.Rational(7,2)+sp.Rational(29,5)
    assert K1 == sp.Rational(173,10)
    assert 2*M/epsilon == 67800
    assert sp.Rational(1,1000)/24 == sp.Rational(1,24000)

    # Critical profile/strip scaling and vanishing background terms.
    amplitude = -sp.Rational(3,4)
    gradient = amplitude+1
    assert 4*gradient-1 == 0
    assert 3*gradient-1 == -sp.Rational(1,4)
    assert 2*gradient-1 == -sp.Rational(1,2)
    # In the Hardy-BMO disjoint-bump obstruction in 2D, bulk quartic
    # energy is invariant and the squared-gradient BMO norm grows 1/r.
    assert 4*(sp.Rational(1,2)-1)+2 == 0
    assert 2*(sp.Rational(1,2)-1) == -1

    source_verifier = ASTRA/'updates/FE/synthesis/quartic/checks/verify_closed_heat.py'
    source = subprocess.run([sys.executable,str(source_verifier)],cwd=source_verifier.parent,capture_output=True,text=True,check=True)
    (ROOT/'source_heat_replay.stdout.json').write_text(source.stdout)
    (ROOT/'source_heat_replay.stderr.txt').write_text(source.stderr)
    source_result=json.loads(source.stdout)
    assert source_result['status']=='PASS'
    assert source_result['exact_gram_margin']=='1/500'

    result={
        'status':'PASS',
        'scope':'exact finite identities and source algebra replay; analytic claims proved in report, not formalized',
        'astra_pin':actual_pin,
        'Fstar_I':str(-sp.Rational(3,10)),
        'growth_M':str(M),
        'gradient_bound_K1':str(K1),
        'epsilon':str(epsilon),
        'near_minimizer_fourth_power_factor':str(2*M/epsilon),
        'ramp_action':str(ramp),
        'exponential_action':str(exponential),
        'total_entry_action':str(entry),
        'source_heat_certificate_sha256':source_result['certificate_sha256'],
        'source_replay_scope':source_result['scope'],
        'strict_trace_continuity':'analytic proof in HEAT_TO_CRITICAL_TRACE.md Sections 2-7',
        'full_nine_coefficient_cone':'OPEN',
        'finite_evaluation_algorithm':'NOT SUPPLIED',
        'historical_novelty':'UNKNOWN',
        'external_mathematical_review':'UNKNOWN',
    }
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
