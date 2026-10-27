import sympy as s
a,b,c,z,t=s.symbols('a b c z t',positive=True)
g=-3/(a+3*z)-1/(a+b+c+z)+2/(a+b+2*z)+2/(a+c+2*z)
N=s.together(g).as_numer_denom()[0]
print('numerator:',s.Poly(s.expand(N),z))
assert s.Poly(N,z).degree()==2
assert s.simplify(g.subs(z,b)-(-1/(a+3*b)+1/(a+c+2*b)))==0
m,v=s.symbols('m v',real=True)
assert s.simplify(N.subs({b:m+v,c:m-v})-2*((a+3*m)*(z-m)*(a+m+2*z)+v*v*(2*a+3*m+3*z)))==0
q=s.Rational(9,16)-s.Rational(3,4)*(3*t+1)/2+t*(3*t+1)/(2*(t+1))
assert s.factor(q-(6*t*t-7*t+3)/(16*(t+1)))==0
print('root-order and reciprocal 3/4 certificate PASS')
