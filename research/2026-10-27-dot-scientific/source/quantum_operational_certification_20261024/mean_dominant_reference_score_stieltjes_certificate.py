"""Exact source-ratio and two endpoint derivative certificates. No floats/cache."""
import sympy as S
z,a,b,r,k=S.symbols('z a b r k',nonnegative=True)
x=r/(a+z);m=(b+1)/(b+z)
g=2*(1-m)*(x+3*m)/((x+3)*(x+m+2)*(x+2*m+1))
q=r*z*g/(a+z)**2;q1=4*(z-1)/((z+1)*(z+3)*(3*z+1))
R=S.factor(q/q1)
expected=r*z*(z+1)*(z+3)*(3*z+1)*(3*a*b+3*a+b*r+3*b*z+r*z+3*z)/(2*(3*a+r+3*z)*(3*a*b+a*z+2*a+b*r+3*b*z+r*z+z*z+2*z)*(3*a*b+2*a*z+a+b*r+3*b*z+r*z+2*z*z+z))
assert S.cancel(R-expected)==0
n0,d0=S.fraction(S.factor(S.diff(R,z).subs(r,b+1+k)))
p0=S.Poly(n0,z,a,b,k)
assert len(p0.terms())==662 and min(p0.coeffs())==3
assert all(c>0 for c in p0.coeffs())
assert all(c>0 for c in S.Poly(d0,z,a,b,k).coeffs())
endpoint=S.diff(R,z)+b*(r-b-1)/(z*(r-1))*S.diff(R,b)
n1,d1=S.fraction(S.factor(endpoint.subs(r,b+1+k)))
p1=S.Poly(n1,z,a,b,k)
assert len(p1.terms())==850
assert [(m,c) for m,c in p1.terms() if c<0]==[((4,0,1,1),-4),((3,0,1,1),-82)]
sos=42*z*z*(b-k*z)**2+2*z**4*(b-k)**2
rest=S.Poly(S.expand(n1-sos),z,a,b,k)
assert len(rest.terms())==848 and min(rest.coeffs())==2
assert all(c>0 for c in rest.coeffs())
assert all(c>0 for c in S.Poly(d1,z,a,b,k).coeffs())
# Zero-area compensator acquisition.
assert S.cancel(q1-(-3/(3*z+1)-1/(z+3)+2/(z+1)))==0
assert S.integrate(q1,(z,0,S.oo))==0
print('PASS actual ratio; fixed endpoint662 positive coefficients; sharp endpoint2 explicit squares+848 positive coefficients; baseline integral0')
