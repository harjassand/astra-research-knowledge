"""Exact local checks of interfaces, not universal DPRM verification."""
import itertools
import sympy as s
from sympy.functions.combinatorial.numbers import stirling
th,k,t,v,z,lam,mu,H,eta=s.symbols('theta k t v z lambda mu H eta')
xs=(k,t,v)
fs=(k-v*v-1,t-k*k)
St=th**2*(th*(k+1)-1)**2+th**4*sum(f*f for f in fs)
P=s.Poly(s.expand(8*St-th**4),*xs)
coeff={b:0 for b in itertools.product(range(5),repeat=3) if sum(b)<=4}
for powers,c in P.terms():
    for b in itertools.product(*(range(p+1) for p in powers)):
        coeff[b]+=c*s.prod(stirling(p,q,kind=2) for p,q in zip(powers,b))
coeff={b:s.expand(c) for b,c in coeff.items()}
bs={b:2+sum(abs(c) for c in s.Poly(q,th).all_coeffs()) for b,q in coeff.items()}
ff=lambda x,j:s.prod(x-i for i in range(j))
fall=lambda b:s.prod(ff(x,j) for x,j in zip(xs,b))
reconstructed=s.expand(sum(c*fall(b) for b,c in coeff.items()))
assert s.expand(reconstructed-P.as_expr())==0
assert max(s.degree(c,th) for c in coeff.values() if c!=0)<=4
assert all(s.Poly(c,th).domain==s.ZZ for c in coeff.values())
for b,q in coeff.items():
    for x in (0,s.Rational(1,17),s.Rational(2,3),1):
        assert 2 <= bs[b]+q.subs(th,x) <= 2+2*(bs[b]-2)
# Source harmonic generator identity, checked independently.
b=eta+lam*z*(z-1)+H*z*(z-1)**2
d=mu*z*(z-1)+H*z*(z-1)**2
assert s.simplify(b/z-d/(z-1)-((lam-mu-H)*(z-1)-mu+eta/z))==0
r=s.sqrt(2)/4
assert s.simplify(1/(k+1-r)-1/(k+1+r)-2*r/((k+1)**2-r**2))==0
checks=0
for a in range(1,10):
    for shift in (-s.Rational(1,4),0,s.Rational(1,4)):
        theta=1/(a+shift+1)
        for kv in range(1,12):
            for vv in range(4):
                for tv in (0,kv**2,kv**2+1):
                    val=(th**4-8*St).subs({th:theta,k:kv,t:tv,v:vv})
                    expected=(kv==vv**2+1 and tv==kv**2 and 8*(kv-a-shift)**2<1)
                    assert bool(val>0)==expected
                    checks+=1
for j in range(1,40):
    out=s.factorial(j)*sum(1/s.factorial(i) for i in range(j+1))
    prev=s.factorial(j-1)*sum(1/s.factorial(i) for i in range(j))
    assert out==1+j*prev
print(f'PASS: {len(coeff)} factorial coefficients, positive-envelope checks, {checks} exact toy witness-band checks, harmonic identity, band width, 39 passage recurrences.')
print('Toy relation is k=v^2+1, t=k^2. This is not a universal halting network.')
