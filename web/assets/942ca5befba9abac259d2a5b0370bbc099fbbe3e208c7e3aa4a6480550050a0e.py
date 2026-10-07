"""Exact polynomial checks for the rare-support saturated obstruction."""
from fractions import Fraction as F
import json, math
from pathlib import Path

def deriv(p): return [F(i)*p[i] for i in range(1,len(p))]
def mul(p,q):
    ans=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): ans[i+j]+=x*y
    return ans
def integral(p): return sum((x/F(i+1) for i,x in enumerate(p)),F(0))

phi=[F(0),F(0),F(1),F(-2),F(1)]
dphi=deriv(phi);ddphi=deriv(dphi)
c0=integral(mul(phi,phi));c1=integral(mul(dphi,dphi));c2=integral(mul(ddphi,ddphi))
assert (c0,c1,c2)==(F(1,630),F(2,105),F(4,5))
assert integral(mul(phi,dphi))==0
assert 4*c1/c0==48 and 16*c2/c0==8064
assert sum(phi)==sum(dphi)==0 and phi[0]==dphi[0]==0
alpha=math.erfc(1/math.sqrt(2))
assert alpha*(4-math.log(3))>=math.log(2)
fixtures=[]
for k in [16,32,64,128,256,512]:
    fixtures.append(dict(K=k,energy=str(1+48/F(k*k)),
                         squared_eigenfunction_defect=str(F(8064,k**4))))
out=dict(status="EXACT_FINITE_ALGEBRA_CHECKS",integrals=[str(c0),str(c1),str(c2)],
         energy_excess_coefficient=str(4*c1/c0),defect_coefficient=str(16*c2/c0),
         rare_support_scale_start=32,normal_event_probability=alpha,
         binary_KL_constant_margin=alpha*(4-math.log(3))-math.log(2),
         fixtures=fixtures,scope="Exact rational integral identities; normal constants floating; not KLS or MI quadrature")
Path(__file__).with_name('saturated_check.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
