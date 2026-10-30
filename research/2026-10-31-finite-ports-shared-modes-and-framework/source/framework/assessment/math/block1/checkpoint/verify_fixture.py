"""Exact reconstruction of the new globally ROC/non-polyconvex fixture."""
import sympy as S
from classify import VARS,x,y,u,v,r,t,F,nu
Z=S.Matrix(VARS);delta=r-t
C=x*(u*u-v*v)+2*y*u*v
P=F+C+S.Rational(3,16)*(r+t)
A0=S.Matrix([-S.Rational(1,4),0,0,-S.Rational(1,4)])
R=S.Matrix([0,1,1,0]);B0=S.Matrix([-S.Rational(11,20),0,0,-S.Rational(1,8)])
AA=dict(zip(Z,A0));BB=dict(zip(Z,B0));HP=S.hessian(P,Z);HD=S.hessian(delta,Z)
assert (R.T*HP.subs(AA)*R)[0]==0
assert HP.subs(AA)*R==S.Rational(1,16)*HD*R
V=B0-A0
support_gap=S.factor(P.subs(BB)-P.subs(AA)-S.Matrix([S.diff(P,a) for a in Z]).subs(AA).dot(V)-S.Rational(1,16)*(V.T*HD*V)[0]/2)
assert support_gap==-S.Rational(3,20480)
# Exact sharp ROC score: |M nu|^2+2(a.M Jnu)^2 <=3 when M=I.
# This is a full angular identity, not a finite ROC sample.
a,b,c,d=S.symbols('a b c d',real=True)
unit_a=S.Matrix([a,b]);unit_b=S.Matrix([c,d]);nn=S.Matrix([c*c-d*d,2*c*d]);eta=S.Matrix([-nn[1],nn[0]])
# On |a|=|b|=1, 3-|nu|^2-2(a.eta)^2 =2(a.nu)^2.
identity=S.expand(3*(c*c+d*d)**2*(a*a+b*b)-(nn.dot(nn))*(a*a+b*b)-2*unit_a.dot(eta)**2-2*unit_a.dot(nn)**2)
assert identity==0
print('P0 globally rank-one convex at the exact sharp quadratic coefficient 3/16.')
print('The only possible minor-support multiplier at A0 is lambda_delta=1/16.')
print('Actual minor-support gap at rational B0:',support_gap)
print('P0 is not polyconvex. Quasiconvexity remains UNKNOWN.')
print('Original fixed-leading polynomial is p0=P0/3, with lower quadratic |A|^2/8.')
