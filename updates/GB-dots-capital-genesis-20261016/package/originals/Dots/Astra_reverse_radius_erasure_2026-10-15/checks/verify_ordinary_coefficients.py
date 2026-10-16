import sympy as s
x,y=s.symbols('x y',positive=True);z=1-x-y;p=s.Matrix([x,y,z]);Q=s.Matrix([[1,0],[0,1],[-1,-1]])
s2=x*y+x*z+y*z
M=Q.T*(s.diag(1/x,1/y,1/z)-2*s.eye(3)-2*p*p.T/(1-(p.T*p)[0]))*Q
assert s.factor(M.det()-1/s2)==0
assert s.factor(M[0,0]-y*(x+z)*(x+z-3*x*z)/(x*z*s2))==0
print('PASS: exact ordinary SLD determinant and positive leading-minor identities.')
a=s.Rational(3,5)
assert a*a/2<s.Rational(6,25)
assert a*a/(2-a*a)<s.Rational(6,25)<2*a*a/(3-a*a)
print('PASS: q=6/25 separates ordinary RLD and SLD thresholds from complete threshold.')
