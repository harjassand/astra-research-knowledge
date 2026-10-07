from fractions import Fraction as Q
from itertools import product
import json

c = Q(1, 4)

def F(x, a):
    return x*x+a*x+c*a*a

checks = 0
for ps in ([Q(1)], [Q(1,2)]*2, [Q(1,3)]*3,
           [Q(1,10),Q(2,10),Q(7,10)], [Q(1,100),Q(99,100)]):
    s2 = sum(p*p for p in ps)
    s3 = sum(p*p*p for p in ps)
    for ls in product([Q(1),Q(9,10),Q(3,4),Q(1,2),Q(1,100)], repeat=len(ps)):
        for x in [Q(1,100),Q(1),Q(100)]:
            for a in [Q(0),x/100,x,x*100]:
                delta = sum(p*F(p*x/l**2, l*(a+(1-p)*x)) for p,l in zip(ps,ls))-F(x,a)
                ideal = -(1-2*c)*(1-s2)*a*x-((1-s2)-c*(1-2*s2+s3))*x*x
                error = sum(p*p*(1/l-1)*x*(a+(1-p)*x)-c*p*(1-l*l)*(a+(1-p)*x)**2+p**3*(l**-4-1)*x*x for p,l in zip(ps,ls))
                assert delta == ideal+error
                energy = sum(p*(1-l**4)*(p*x/l**2)**2 for p,l in zip(ps,ls))
                bound = -Q(1,2)*(1-s2)*a*x-Q(3,4)*(1-s2)*x*x+Q(9,8)*energy
                assert delta <= bound
                checks += 1

print(json.dumps({'exact_transition_and_lyapunov_fixtures':checks, 'all_passed':True}))
