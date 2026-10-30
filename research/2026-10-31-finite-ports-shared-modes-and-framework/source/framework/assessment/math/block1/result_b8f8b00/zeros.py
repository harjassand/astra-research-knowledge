import sympy as S
s=S.sqrt(3);r=S.symbols('r',real=True)
u=-(2+s)/(6*(r-1));x=(1+s)/(6*r)-2*u/r
expr=S.factor(r*(4*u*u-x*x)/(2*u)+S.Rational(1,3),extension=s)
print('u x',S.simplify(u),S.factor(x,extension=s));print('eq',expr);print(S.solve(expr,r))
