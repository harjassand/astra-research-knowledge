import sympy as s
from functools import lru_cache
u,v,w,t,eta=s.symbols('u v w t eta', real=True)
@lru_cache(None)
def mom(a,b,c):
    ans=s.S.Zero
    for l in range(c//2+1):
        aa=a+c-2*l; bb=b+c-2*l
        if aa%2 or bb%2: continue
        ra=aa//2; rb=bb//2
        ans+=s.binomial(c,2*l)*s.rf(eta+s.Rational(1,2),l)*s.rf(s.Rational(1,2),l)*s.rf(s.Rational(1,2),ra)*s.rf(s.Rational(1,2),rb)/(s.rf(eta+1,ra+l)*s.rf(eta+1,rb+l))
    return s.factor(ans.subs(eta,1/t-1))
def expectation(poly):
    return s.factor(sum(coeff*mom(*powers) for powers,coeff in s.Poly(s.expand(poly),u,v,w).terms()))
q=u*v+u*w+v*w; S=u+v+w; H=q-S
for k in range(1,7):
    m=expectation(H**k)
    print(k, m, 'derivative at1:', s.diff(m,t).subs(t,1))
