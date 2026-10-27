import sympy as s
r,e,t=s.symbols('r e t',real=True)
H=s.Matrix([[0,-1,2],[-1,0,2],[2,2,0]])
N=s.Matrix.hstack(s.Matrix([1,-1,0])/s.sqrt(2),s.Matrix([1,1,2])/s.sqrt(6),s.Matrix([1,1,-1])/s.sqrt(3))
assert N.T*N==s.eye(3)
assert s.simplify(N.T*H*N)==s.Matrix([[1,0,0],[0,s.Rational(7,3),s.sqrt(2)/3],[0,s.sqrt(2)/3,-s.Rational(10,3)]])
V=s.Matrix([[1,1,-1],[1,1,-1],[-1,-1,1]])
assert s.expand((V+t*H).det()-t*t*(7-8*t))==0
def d(x):return s.Matrix([1-x,x*x-x,x])
def q(z):return z[0]*z[1]+z[0]*z[2]+z[1]*z[2]
assert s.expand(q(d(r)))==0
assert s.factor(s.Matrix.hstack(d(2),d(2+e),d(2-e)).det())==-2*e**3
print('PASS: vertex compression, exact cubic, null direction family, spanning determinant.')
