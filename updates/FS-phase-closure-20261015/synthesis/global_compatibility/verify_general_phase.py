#!/usr/bin/env python3
"""Exact finite checks for general averaging failure and coupled product map."""
import json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
zx,zy=s.symbols("zx zy",nonzero=True)
eps=s.symbols("eps",real=True)
I=s.I
def mean(f):
 out=0
 for term in s.Add.make_args(s.expand(f)):
  p=term.as_powers_dict()
  if p.get(zx,0)==0 and p.get(zy,0)==0:out+=term
 return s.simplify(out)
def conj(f):
 return s.conjugate(f).subs({s.conjugate(zx):1/zx,s.conjugate(zy):1/zy})
cy=(zy+zy**-1)/2;c2=(zy**2+zy**-2)/2;sy2=(zy**2-zy**-2)/(2*I)
r=1+eps*c2;ry=-2*eps*sy2
energy=mean((ry**2+r*r*cy**2)**2)
averaged=mean(r**4)*s.Rational(3,8)
diff=s.factor(energy-averaged)
assert diff==eps*(209*eps**3+56*eps**2+70*eps+32)/32
strict=diff.subs(eps,-s.Rational(1,100))
assert strict==-s.Rational(31305391,3200000000)<0
zt=(zx+zx**-1)/2+(zx**3-zx**-3)/2
wt=1+zy/2
X=I*zx*s.diff(zt,zx)*wt
Y=zt*I*zy*s.diff(wt,zy)
u=s.expand(X*conj(X));v=s.expand(Y*conj(Y))
q=s.expand((conj(X)*Y-X*conj(Y))/(2*I))
G=3*(u+v-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u
EG=mean(G);norm=mean((u+v)**2)
assert EG>norm/20>0
assert s.expand(zt.subs(zx,-zx)+zt)==0
out={"status":"PASS","groups":2,"checks":{
 "illegal_general_density_average":{"exact_difference":str(diff),"epsilon_minus_1_over_100":str(strict)},
 "coupled_product_example":{"G_energy":str(EG),"gradient_fourth_norm":str(norm),
   "energy_to_norm_ratio":str(EG/norm),"antipodal_shift":"x->x+pi",
   "scope":"Full theorem is analytic; finite example is not universal certification"}}}
(ROOT/"general_phase_checks.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
