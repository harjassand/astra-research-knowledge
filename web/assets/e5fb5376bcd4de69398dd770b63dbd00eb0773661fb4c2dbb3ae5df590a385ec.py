"""Exact rotational-coordinate check of can:identity; scoped algebra evidence."""
import sympy as s
r=s.symbols('r', nonzero=True)
a=s.Matrix(s.symbols('a1:4'))
u=s.Matrix(s.symbols('u1:4'))
b=s.Matrix(s.symbols('b1:4'))
at=s.Matrix(s.symbols('at1:4'))
n=s.Matrix([0,0,1])
d=1-n.dot(u)
D=1-n.dot(a)
e=1-a.dot(u)
qinv=1-u.dot(u)
qXinv=1-a.dot(a)
N0=(d/D)*(a-n)+n-u
np=N0/r
ap=at*d/D
rp=d/D-1
dp=-np.dot(u)-n.dot(b)
Dp=-np.dot(a)-n.dot(ap)
ep=-ap.dot(u)-a.dot(b)
k=u-e*n/D
kp=b-(ep/D-e*Dp/D**2)*n-e*np/D
primitive_derivative=kp/(r*d)-k*rp/(r**2*d)-k*dp/(r*d**2)
g=(u-n)/d
partial_u_g=b/d+(u-n)*n.dot(b)/d**2
H=s.eye(3)+n*a.T/D
lhs=-H*partial_u_g/r-H*g*qinv/(r**2*d)
rhs=-primitive_derivative+e*(n*qXinv/D-a)/(r**2*D**2)+n*at.dot(k)/(r*D**2)
res=[s.cancel(x) for x in lhs-rhs]
assert res == [0,0,0],res
print('Exact rational cancellation:',res)
print('Scope: arbitrary timelike a,u and arbitrary source and receiver accelerations, in n=e3 coordinates. Rotational covariance extends the identity to every unit n. This checks only can:identity, not analytic estimates.')
