#!/usr/bin/env python3
"""Independent exact scalar identities for the universal/QC budget corollaries."""
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
x1,x2,h1,h2=s.symbols('x1 x2 h1 h2',real=True)
xx=x1*x1+x2*x2; hh=h1*h1+h2*h2; dot=x1*h1+x2*h2
bregman=(xx+2*dot+hh)**2-xx**2-4*xx*dot
assert s.expand(bregman-hh**2/3
    -6*(dot+hh/3)**2-2*(x1*h2-x2*h1)**2)==0
a,b,c,d,r,t,alpha=s.symbols('a b c d r t alpha',real=True)
partial_abs2=((a+d)**2+(c-b)**2)/4
barpartial_abs2=((a-d)**2+(c+b)**2)/4
assert s.expand(a*a+b*b+c*c+d*d-2*(partial_abs2+barpartial_abs2))==0
u,v,j=a*a+c*c,b*b+d*d,a*d-b*c
H=(u+v-2*j)**2
astar=3*r/(8*(r+2))
J=astar*H+r*(r-1)*u*u/6+j*j+r*u*j
support_gap=J-(r+2)*j-s.Rational(2,3)*r*(r+2)*a+(r+2)*(r+1)/2
curve=s.expand(support_gap.subs({a:1+t,b:0,c:0,d:1-(r+1)*t}))
assert all(s.simplify(curve.coeff(t,i))==0 for i in range(3))
assert s.simplify(curve.coeff(t,3)+r*(r+2)/3)==0

transform_bound_squared=F(24)
gradient_squared_norm_factor=2*(transform_bound_squared+1)/4
gradient_fourth_norm_factor=gradient_squared_norm_factor**2
assert gradient_squared_norm_factor==F(25,2)
assert gradient_fourth_norm_factor==F(625,4)
nu_G=F(3)-F(15,8)
new_gamma=nu_G/3/gradient_fourth_norm_factor
old_gamma=F(1,2500000)
assert new_gamma==F(3,1250) and new_gamma/old_gamma==6000
M=F(120)*(1+F(2,3)+F(1,5))
assert M==224
R4=(2*M+1)/new_gamma
E_star=2*M/new_gamma
N=10**17
eps=F(1,1000)
assert R4==F(561250,3) and R4<21**4
assert E_star==F(560000,3)
# No irrational numerical evaluation: fourth power of source horizon test.
assert (F(6960)*E_star/eps)**4 <= (N-1)**3
receipt={'status':'EXACT_PASS','Bregman_constant':'1/3',
    'complex_Beurling_L4_bound_squared':'24',
    'gradient_squared_norm_factor':str(gradient_squared_norm_factor),
    'gradient_fourth_norm_factor':str(gradient_fourth_norm_factor),
    'G_nu':str(nu_G),'G_new_gamma':str(new_gamma),
    'G_old_gamma':str(old_gamma),'ratio':str(new_gamma/old_gamma),
    'M':str(M),'R4':str(R4),'E_star':str(E_star),'N':N,
    'horizon_epsilon':str(eps),'horizon_test_exact':True,
    'sharp_support_cubic':'-r(r+2)/3',
    'scope':'Exact identities/arithmetic; source Beurling theorem and heat/QC analysis audited separately.'}
(ROOT/'continuation_corollaries_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
