"""Exact small-dimensional check of universal-resultant derivatives and Bezout extraction.
NOT the unimplemented four-cubic quaternion template.
"""
import sympy as s,json,time
from pathlib import Path
x,y,t,l=s.symbols('x y t l');a=s.symbols('a0:4');b=s.symbols('b0:4');U=s.resultant(sum(a[i]*t**i for i in range(4)),sum(b[i]*t**i for i in range(4)),t)
F=3*x**4+2*x**3*y-x*x*y*y+5*x*y**3+7*y**4;Q=x*x+y*y
H=[s.diff(F,x)/4-l*Q*x,s.diff(F,y)/4-l*Q*y]
subs={}
for syms,h in zip([a,b],H):
 for i,c in enumerate(syms):subs[c]=s.expand(h.subs(x,1)).coeff(y,i)
R=s.Poly(U.subs(subs),l,domain=s.QQ);assert R.degree()==4 and s.gcd(R,R.diff()).degree()==0
As=[s.Poly(s.diff(U,syms[0]).subs(subs),l,domain=s.QQ) for syms in [a,b]]
Bs=[s.Poly(s.diff(U,syms[1]).subs(subs),l,domain=s.QQ) for syms in [a,b]]
# Multi-polynomial Bezout, tracked coefficients modulo R.
g=R;weights=[s.Poly(0,l,domain=s.QQ),s.Poly(0,l,domain=s.QQ)]
for i,A in enumerate(As):
 u,v,d=s.gcdex(g,A);weights=[(u*w).rem(R) for w in weights];weights[i]=(weights[i]+v).rem(R);g=d
assert g==s.Poly(1,l,domain=s.QQ)
assert sum((weights[i]*As[i] for i in range(2)),s.Poly(0,l,domain=s.QQ)).rem(R)==s.Poly(1,l,domain=s.QQ)
X=sum((weights[i]*Bs[i] for i in range(2)),s.Poly(0,l,domain=s.QQ)).rem(R)
for h in H:assert s.Poly(h.subs({x:1,y:X.as_expr()}),l,domain=s.QQ).rem(R).is_zero
assert s.Poly((F-l*Q**2).subs({x:1,y:X.as_expr()}),l,domain=s.QQ).rem(R).is_zero
assert s.gcd(R,s.Poly(1+X.as_expr()**2,l)).degree()==0
out={'scope':'Executed binary two-cubic universal template only; validates exact derivative extractor, not four-variable implementation','universal_resultant_terms':len(s.Poly(U,*a,*b).terms()),'restricted_R':str(R.as_expr()),'degree':R.degree(),'squarefree':True,'coordinate_polynomial':str(X.as_expr()),'both_original_H_residuals_zero_modR':True,'normalized_objective_equals_lambda_modR':True,'normalization_denominator_coprime_toR':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
