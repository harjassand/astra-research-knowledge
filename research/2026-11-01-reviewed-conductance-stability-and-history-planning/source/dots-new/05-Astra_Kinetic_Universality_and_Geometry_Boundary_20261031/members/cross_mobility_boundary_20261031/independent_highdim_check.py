#!/usr/bin/env python3
"""Exact algebra and rational finite consequences of HIGH_DIMENSIONAL_COROLLARY.md."""
from fractions import Fraction as Q
import json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
y,S,m=sp.symbols('y S m', real=True)
v=1+(1-y*y)**2
# S = ||z||^2 and homogeneity z.grad_z(F)=v*S, in every fiber dimension.
euler=(y*sp.diff(v,y)/2+v)*S
assert sp.expand(2*euler-(6*(y*y-sp.Rational(2,3))**2+sp.Rational(4,3))*S)==0
lyapunov=2*(m+1)-2*euler
assert sp.expand(lyapunov-(2*(m+1)-(6*(y*y-sp.Rational(2,3))**2+sp.Rational(4,3))*S))==0
# Exact H3 exponents and an all-m decay check.
assert sp.expand((m-2*m*m).subs(m,m+1)-(m-2*m*m))==-4*m-1
assert sp.expand((-2*m-10).subs(m,m+1)-(-2*m-10))==-2
rows=[]
for dim in [1,2,4,8,16]:
    eps=Q(1,2**(3*dim+10));k=16*dim
    exponent=k*k//128
    assert exponent==2*dim*dim
    cap_upper=36*eps+Q(1800,2**exponent)
    ratio_upper=8*2**dim*cap_upper
    h3=Q(288,2**(2*dim+10))+Q(14400*2**dim,2**(2*dim*dim))
    assert ratio_upper==h3
    gamma=Q(k*k)/(1-eps)
    condition_lower=gamma/eps
    assert condition_lower>256*dim*dim*2**(3*dim+10)
    rows.append({'m':dim,'epsilon':str(eps),'k':k,'ratio_upper_rational':str(h3),
                 'ratio_upper_float_diagnostic':float(h3)})
result={'status':'PASS','checks':[
    'Euler and Lyapunov identities with symbolic dimension and squared fiber norm',
    'exact rational H3 coefficients/exponents at five dimensions',
    'first H3 term decreases by factor 1/4 per dimension',
    'second H3 term decreases by factor 2^(-4m-1), at most 1/32 for m>=1',
    'condition-number lower growth scale'],
    'examples':rows,
    'scope':'Analytic conditional-Gaussian tail and shoulder arguments are reviewed in INDEPENDENT_REVIEW.md; no numerical PDE.'}
(HERE/'independent_highdim_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
