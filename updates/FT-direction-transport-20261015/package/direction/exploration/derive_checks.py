import sympy as s
k,n=s.symbols('k n', positive=True)
e=s.Rational(1,100)
d=1-16*e
bound=1-29*e**2-s.Rational(189,8)*e**4+(16*e**2+4*e**4)/d+96*e**4/d**3
print('Rational trial bound:',bound,'decimal',s.N(bound,18),'one minus',s.factor(1-bound))
A=k*k*n*n/8; C=2*k**3*n; D=6*k*k*n*n
print('reduced mode Hessian:',s.factor(D-C*C/A))
# Exact energy as a rational expression in sqrt(1-a^2), by Laurent expansion after z=1-a cos(y).
z=s.symbols('z');a=16*e;c=(1-z)/a
expr=z*(1+e*c)**4+32*e**2*(1-c*c)*(1+e*c)**2/z+256*e**4*(1-c*c)**2/z**3
expr=s.expand(expr)
from math import comb
mom={-1:1/s.sqrt(1-a*a),-2:1/(1-a*a)**s.Rational(3,2),-3:(2+a*a)/(2*(1-a*a)**s.Rational(5,2))}
for j in range(6):
    mom[j]=sum(s.binomial(j,2*m)*a**(2*m)*s.Rational(comb(2*m,m),4**m) for m in range(j//2+1))
E=0
for term in s.Add.make_args(expr):
    powers=term.as_powers_dict(); power=powers.get(z,0)
    coef=term/z**power; E += coef*mom[int(power)]
print('Exact trial energy:',s.simplify(E),'decimal',s.N(E,20))
