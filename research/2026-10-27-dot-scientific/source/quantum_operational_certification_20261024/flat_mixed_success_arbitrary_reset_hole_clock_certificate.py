"""Exact finite Bernstein receiver for the three proven Schmidt-allocation endpoints.
No floats enter construction or assertions. The analytic reduction to these endpoints
is in flat_mixed_success_arbitrary_reset_hole_theorem.md.
"""
import sympy as S
from math import comb
import json
from pathlib import Path
x,beta=S.symbols('x beta');cap=S.Rational(3,2)
rows=[];total=0
for rank,lam in [(1,[S.Integer(1),S.Integer(0),S.Integer(0)]),(2,[S.Rational(1,2),S.Rational(1,2),S.Integer(0)]),(3,[S.Rational(1,3)]*3)]:
 ratio=(1+x)**6*(1+3*x)/((1+(x+beta)/3)**3*(1+x/3)**15)
 for l in lam:ratio*=(1+x+beta*(1-l)/2)**2/(1+3*x+beta*l)
 num,den=S.fraction(S.factor(ratio));poly=S.Poly(S.expand(num-den),beta)
 assert all(v>=0 for v in S.Poly(den,x,beta).coeffs()) and den.subs({x:0,beta:0})>0
 endpoint=[]
 for (power,),p in poly.terms():
  P=S.Poly(p,x);n=P.degree();co=list(reversed(P.all_coeffs()))
  transformed=[sum(co[i]*cap**i*comb(n-i,j-i) for i in range(j+1)) for j in range(n+1)]
  assert all(v>=0 for v in transformed)
  assert p.subs(x,cap)>=0
  if power==0:
   assert any(v>0 for v in transformed) and p.subs(x,cap)>0
  total+=len(transformed)
  endpoint.append({'beta_power':power,'x_degree':n,'bernstein_substitution_coefficients':[str(v) for v in transformed]})
 print('rank',rank,'all exact transformed coefficients nonnegative; strict beta0 row for x>0',flush=True)
 rows.append({'flat_schmidt_rank':rank,'rows':endpoint})
# Algebra behind the actual allocation minimum, not a generic endpoint rule.
A,B,z,u,v=S.symbols('A B z u v')
gp=lambda q:-2*z/(A-z*q)-2*z/(B+2*z*q)
N=-2*A*A+B*B+2*z*(A+B)*(u+v)+2*z*z*u*v
assert S.factor(gp(u)-gp(v)+2*z*z*(u-v)*N/((A-z*u)*(A-z*v)*(B+2*z*u)*(B+2*z*v)))==0
assert S.factor(S.diff(N.subs(v,1-2*u),u)+2*z*(A+B-z+4*z*u))==0
# Exact radial endpoint guards at a=2/3.
a=S.symbols('a');L1=5*S.log(1+3*a)-6*S.log(1+a)-6*S.log(1+2*a/3)
assert S.factor(S.diff(L1,a)+3*(14*a*a+13*a-5)/((a+1)*(2*a+3)*(3*a+1)))==0
assert 3**23>5**6*13**6 and 250000>216513
out=Path(__file__).with_suffix('.json');out.write_text(json.dumps({'domain':'0<x<=3/2, beta>=0','substitution':'x=(3/2)u/(1+u)','total_exact_coefficients':total,'endpoints':rows},indent=2))
print('PASS:',total,'exact coefficients; allocation derivative and radial endpoint identities.')
