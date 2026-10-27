"""Exact symbolic identities supporting the operator proof; no quadrature."""
import sympy as s
u,h,A,B,C,E,z=s.symbols('u h A B C E z', positive=True)
D=lambda t:t*t+A*t+B
N=lambda t:C*t+E
R=lambda t:(1+h/t)*D(t)+N(t)
L=lambda t:2*D(t)+N(t)
assert s.expand(R(2*u)-L(u)-(2*u*u+(C+2*h)*u+h*A-B+h*B/(2*u)))==0
f=(z*z-1)*(z*z+4*z+1)/(2*z*(z*z+z+1))-2*s.log(z)
assert s.factor(s.diff(f,z))==(z-1)**4*(z+1)**2/(2*z**2*(z*z+z+1)**2)
delta=2-s.sqrt(3)
assert s.simplify(delta**2-4*delta+1)==0
assert s.simplify((1-delta)**2-2*delta)==0
assert 4*delta>1
sigma,n=s.symbols('sigma n')
assert s.factor(1/(sigma-n)-1/sigma-n/sigma**2-n*n/(sigma*sigma*(sigma-n)))==0
T,V=s.symbols('T V',positive=True)
q=u*u+T*u+V
primitive=-2*(2*u+T)/((T*T-4*V)*s.sqrt(q))
assert s.simplify(s.diff(primitive,u)-q**s.Rational(-3,2))==0
integral=2*(T/s.sqrt(V)-2)/(T*T-4*V)
assert s.simplify(integral-2/(s.sqrt(V)*(T+2*s.sqrt(V))))==0
# Rationalized curvature threshold solves the unsquared quadratic.
w=s.symbols('w',positive=True)
hc=B/(A+C+w)
quad=(A*A-4*B)*hc*hc-2*B*(A+C)*hc+B*B
assert s.factor(quad)==B**2*(-2*A*C+ w**2-C**2-4*B)/(A+C+w)**2
print('PASS: transport, scalar log bound derivative, delta identity, reciprocal tangent, determinant integral, threshold quadratic')
