"""Exploratory reconstruction of the constant quadratic heat correction."""
exec(open(__file__.replace('quadratic_heat.py','heat_probe.py')).read().split('E=s.factor')[0])
from itertools import combinations
ks=s.symbols('k:6'); O=s.zeros(4)
for n,(i,j) in enumerate(combinations(range(4),2)):
    O[i,j]=ks[n]; O[j,i]=-ks[n]
expr=s.expand((B1.T*O*B2)[0]).subs(subs,simultaneous=True).expand()
target=16*(3*(t*t+u*u)-(p*p+q*q)-2*(r*r+v*v))
print(s.linsolve(s.Poly(s.expand(expr-target),p,q,r,v,t,u).coeffs(),ks))
