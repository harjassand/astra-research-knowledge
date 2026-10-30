import sympy as s
q,k,l=s.symbols('q k l',real=True)
x,y,u,v=s.symbols('x y u v',real=True);V=s.Matrix([x,y,u,v]);rr=x*x+y*y;tt=u*u+v*v
P=tt*tt+2*rr*tt+x*(u*u-v*v)+2*y*u*v+s.Rational(3,16)*(rr+tt)
H=s.hessian(P,V).subs({x:-s.Rational(1,4),y:q,u:-q/2,v:-s.Rational(1,4)})
B=s.Matrix([[k+l,-k+l],[k-l,k+l],[k+l,k-l],[-k+l,k+l]])/s.sqrt(2)
O=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
D=(O.T*B.T*H*B*O).applyfunc(s.simplify)
expected=s.Matrix([[3*l*l*(4*q*q+3),l*(4*q*q*k+12*q*l-3*k)],[l*(4*q*q*k+12*q*l-3*k),12*q*q*k*k+32*q*q*l*l-24*q*k*l+k*k+4*l*l]])/2
assert s.simplify(D-expected)==s.zeros(2)
A=32*q**4+36*q*q;B0=-48*q**3-18*q;C=96*q**4+48*q*q+9
assert s.factor(D.det()-l*l*(A*k*k+2*B0*k*l+C*l*l))==0
assert s.factor(A*C-B0*B0-96*q**4*(4*q*q+3)*(8*q*q+1))==0
assert s.factor(D.det().subs(q,0)-9*l**4)==0
z=-s.Rational(1,4)+s.I*q;w=-q/2-s.I/4
assert s.simplify(z*s.conjugate(w)**2-(1+12*q*q)/64-s.I*q**3/4)==0
h=s.symbols('h',real=True)
# Distance between L_{exp(+ih)} and L_{exp(-ih)}.
d1=-s.sin(2*h)/2;d2=s.sin(h)/2;v1=2*s.cos(2*h);v2=-s.cos(h)
assert s.trigsimp(d1*v2-d2*v1-s.sin(h)**3)==0
print('PASS: characteristic invariants, unique null parametrization, exact cusp acoustic orders and line-distance numerator')
