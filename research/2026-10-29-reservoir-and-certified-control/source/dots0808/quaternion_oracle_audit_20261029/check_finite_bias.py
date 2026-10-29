"""Exact rational scalar edge cases for FTPL constants and finite perturbation."""
from fractions import Fraction as F
import json,random
from pathlib import Path
rng=random.Random(629)
def potential(w,R):
 if w<=-R:return w
 if w>=R:return F(0)
 return -(R-w)**2/(4*R)
def derivative(w,R):
 if w<=-R:return F(1)
 if w>=R:return F(0)
 return (R-w)/(2*R)
rows=[]
for k in range(100):
 R=F(rng.randrange(1,20),7);w=F(rng.randrange(-20,21),11);g=F(rng.randrange(-20,21),13)
 residual=derivative(w,R)*g-(potential(w+g,R)-potential(w,R))
 assert residual<=g*g/(4*R)
 rows.append({'R':str(R),'w':str(w),'g':str(g),'stability_gap':str(g*g/(4*R)-residual)})
# K={0,1}, choose action1 whenever perturb z<=epsilon: epsilon-argmin.
R=F(1,1000);eps=F(1,1000000);bias=eps/(2*R)
assert bias>eps
# Finite midpoint perturbation; continuous z in a cell differs <=R/M.
M=16; eps=F(1,30);R=F(2)
for i in range(M):
 zbar=-R+(2*i+1)*R/M
 action=F(int(zbar<=eps))
 for z in [zbar-R/M,zbar+R/M]:
  actual=z*action-min(F(0),z)
  assert actual<=eps+R/M
out={'scope':'Exact scalar stability and midpoint contracts, not full online quantum deployment','stability_cases':rows,'naive_T_epsilon_counterexample':{'R':'1/1000','epsilon':'1/1000000','actual_expected_action_bias':str(bias),'ratio_to_epsilon':str(bias/F(1,1000000))},'finite_midpoint_boundary_cases':2*M}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print('100 stability cases; 32 midpoint boundaries; epsilon-only bias fails by factor500')
