import sympy as s
exec(open(__file__.replace('c4_cone.py','explore_c4.py')).read().split("print('det='")[0])
p=s.Poly(s.expand(M.det()),x,y)
a0=p.coeff_monomial(x**8);a1=p.coeff_monomial(x**6*y**2)-4*a0;a2=p.coeff_monomial(x**4*y**4)-6*a0-2*a1
print('coef 0',s.factor(a0));print('coef 1',s.factor(a1));print('coef 2',s.factor(a2))
print('at diag',s.factor(a0+a1/4+a2/16))
