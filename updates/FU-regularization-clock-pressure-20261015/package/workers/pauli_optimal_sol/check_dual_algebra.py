"""Exact symbolic/rational checks supporting, not replacing, the analytic audit."""
from pathlib import Path
import json
import sympy as S

r,s,c,ell,ell2,J,F=S.symbols('r s c ell ell2 J F',positive=True)
f=r*(2+c-3*r+r*r)-2*c*r*ell+c*J
ellprime=(ell2-3*ell)/(2*r)
Jprime=ell2+S.Symbol('ell_minus')
fprime=S.diff(f,r)+S.diff(f,ell)*ellprime+S.diff(f,J)*Jprime
Rprime=f+8*c*r*ell+4*c*r*r*ellprime
assert S.simplify(Rprime-(r*(2+c-3*r+r*r)+c*J+2*c*r*ell2))==0
Gprime=-f-2*r*fprime
target=r*(-6-3*c+15*r-7*r*r-c*(J/r+2*S.Symbol('ell_minus')))
assert S.simplify(Gprime-target)==0

u=S.symbols('u',real=True)
poly=u*u/2+2*u+S.Rational(2,3)+c/3
kappa=S.Rational(23,3)-2*c/3
Tpoly=2*r*poly.subs(u,r)-S.integrate(poly,(u,r,r+2))
assert S.simplify(Tpoly+4*c/3-((r+1)**3-kappa*(r+1)))==0
central=-S.integrate(poly,(u,1-s,1+s))-(s**3-kappa*s)
assert S.simplify(central-S.Rational(4,3)*(s*(1-s*s)-c*s))==0

sqrt_pi_upper=S.Rational(1773,1000)
assert sqrt_pi_upper**2>S.Rational(22,7)
Mbound=S.Rational(68,25)/2*(1+3*sqrt_pi_upper/4)
assert Mbound<S.Rational(16,5)
assert S.Rational(5,2)*S.Rational(1,8)*S.Rational(16,5)==1

out={'status':'PASS','scope':'exact algebra and rational constants only','checks':['U cancellation derivative (17)','V derivative (18)','outer polynomial adjoint (21)','central polynomial adjoint correction','rational bound M1 < 16/5','strict positivity threshold product = 1'], 'rational_M1_upper':str(Mbound)}
(Path(__file__).parent/'dual_algebra_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
