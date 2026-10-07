"""Bounded exact algebra fixtures for the checked Newton/birth identity."""
from fractions import Fraction as F
from pathlib import Path
import json
cases=0
base=F(3,4)  # a=log(4/3), all displayed exponentials are rational.
for N in (2,4,6,8):
    for k in range(N+1):
        x=(k-N//2)**2
        for m in range(1,7):
            A=[(N//2+r)**2 for r in range(1,m+1)]
            values=[base**a for a in A]
            dd=values[:];newton=F(0);product=F(1)
            for ell in range(m):
                assert (-1)**ell*dd[0]>0
                newton+=dd[0]*product
                product*=x-A[ell]
                dd=[(dd[j+1]-dd[j])/(A[j+ell+1]-A[j]) for j in range(len(dd)-1)]
            rates=[a-x for a in A]
            survival=F(0)
            for i,lam in enumerate(rates):
                coeff=F(1)
                for j,other in enumerate(rates):
                    if i!=j:coeff*=F(other,other-lam)
                survival+=base**lam*coeff
            assert newton==base**x*survival
            assert 0<survival<1
            cases+=1
z=F(6,5)
sin_lower=z-z**3/6;cos_upper=1-z*z/2+z**4/24
assert sin_lower/cos_upper>2*z
assert F(18,25)<F(3,4)
out={'status':'EXACT_NEWTON_SURVIVAL_FIXTURES_PASS','fixture_count':cases,
     'N':[2,4,6,8],'m':'1..6','a_exact':'log(4/3)',
     'delta1_rate_upper':'18/25<3/4','scope':'Fixtures support identities; proof14 supplies general probabilistic and analytic derivations.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
