#!/usr/bin/env python3
"""Exact constants and receiving algebra only; r,v,j remain unacquired."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
NAME='FINITE_CLOCK_ENDPOINT_RECEIVER.md'
EXPECTED='0018c24de9dfa6cf2757a42cbfd3d1b8cb7d37369f46cf2fa5e0f9fac9228919'
actual=hashlib.sha256((ROOT/NAME).read_bytes()).hexdigest()
assert actual==EXPECTED
l,w=s.symbols('l w',positive=True)
inverse_bound=s.integrate(1/(2*(l+s.Rational(3,4)*w*w)**2),(w,0,s.oo))
assert s.simplify(inverse_bound-s.pi/(4*s.sqrt(3))*l**s.Rational(-3,2))==0
assert 2*70**2<100**2
Ebar=8*400**3
assert Ebar==512000000
assert F(2,400)<F(1,100)
startup_ratio=F(Ebar**2,400*10**20)
assert startup_ratio<2
assert F(10**16,20000)>1
cap_square_margin=3000000**2-2*(2000200**2)
assert cap_square_margin>0
assert F(2000200)*F(10,7)<3000000

H,j,v=s.symbols('H j v',nonnegative=True)
m=j*H/3+s.sqrt(2*v*H+(j*H/3)**2)
assert s.simplify(m*m-2*H*(v+j*m/3))==0

t,z=s.symbols('t z',nonnegative=True)
# This coefficient certificate proves no early threshold crossing for all T>=1e4.
poly=s.Poly(s.expand((t**5-192*t-30).subs(t,z+10000)),z)
assert all(c>0 for c in poly.all_coeffs())
assert F(12,10**16)<F(1,16)
assert F(199,200)*F(1,20000)==F(199,4000000)>F(1,1000000)
assert F(13,16)<F(15,16)

result={
 'status':'PASS_CONDITIONAL_RECEIVER_NO_REPAIR',
 'source_sha256':{NAME:actual},
 'inverse_flow_clock_upper_integral':str(inverse_bound),
 'corrector_rational_comparison_margin':100**2-2*70**2,
 'Ebar':Ebar,'startup_ratio_upper_bound_at_N_min':str(startup_ratio),
 'cap_square_comparison_margin':cap_square_margin,
 'freedman_quadratic_residual':'0',
 'no_early_clearance_polynomial_coefficients':[str(c) for c in poly.all_coeffs()],
 'seed_lower_fraction_of_N':'199/4000000',
 'r_v_j_acquired':False,
 'all_assertions_passed':True,
}
(HERE/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
