#!/usr/bin/env python3
"""Exact constants for the post-sharp-certificate quartic Jensen margin."""
from pathlib import Path
import json
import sympy as s

P=Path(__file__).resolve().parent
x1,x2,h1,h2,r=s.symbols('x1 x2 h1 h2 r',real=True)
dot=x1*h1+x2*h2
xx=x1*x1+x2*x2
hh=h1*h1+h2*h2
bregman=((x1+h1)**2+(x2+h2)**2)**2-xx**2-4*xx*dot
rhs=6*(dot+hh/3)**2+2*(x1*h2-x2*h1)**2
assert s.expand(bregman-hh**2/3-rhs)==0
elliptic_factor=(2*(s.Integer(24)+1)/4)**2
assert elliptic_factor==s.Rational(625,4)
conversion=1/(3*elliptic_factor)
assert conversion==s.Rational(4,1875)
nuG=3-s.Rational(15,8)
assert nuG*conversion==s.Rational(3,1250)
assert (nuG*conversion)/s.Rational(1,2500000)==6000
astar=3*r/(8*(r+2))
assert s.factor(s.diff(astar,r)-3/(4*(r+2)**2))==0
assert astar.subs(r,-s.Rational(21,8))==s.Rational(63,40)
assert astar.subs(r,-s.Rational(5,2))==s.Rational(15,8)
receipt={
    'status':'EXACT_PASS','sympy_version':s.__version__,
    'bregman_nonnegative_two_square_identity':True,
    'primary_complex_Beurling_L4_bound_squared':'24',
    'primary_source':'https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf',
    'primary_theorem':'Theorem 1.1, complex-valued case',
    'elliptic_fourth_power_factor':'625/4',
    'H_coefficient_to_gradient_Jensen_factor':'4/1875',
    'G_H_remainder':'9/8','G_Jensen_constant':'3/1250',
    'source_interval_uniform_Jensen_constant':'3/1250',
    'factor_relative_to_old_constant':'6000',
    'scope':'Exact Bregman algebra and constant arithmetic; elliptic operator estimate is the cited primary theorem. Sharp QC dependence is separate.'
}
(P/'MARGIN_v0002_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('EXACT_PASS: Bregman identity, elliptic conversion, G margin3/1250, improvement factor6000')
