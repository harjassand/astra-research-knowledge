"""Exact IID Schur-program count lower bounds via disjoint full decreasing subsequences."""
from fractions import Fraction as F
from pathlib import Path
import json

def completed_probability(steps,weights,den,k):
 rates=list(weights)*k;m=len(rates);v=[1]+[0]*m
 for _ in range(steps):
  new=[0]*(m+1)
  for j in range(m):new[j]+=(den-rates[j])*v[j];new[j+1]+=rates[j]*v[j]
  new[m]+=den*v[m];v=new
 return F(v[-1],den**steps)
rows=[]
for model,weights,den,steps in [('uniform_minus',[1]*8,8,[32,64,128,256]),('two_axis_minus',[1,1,1,2,2,3,3,3],16,[32,64,128,256]),('two_axis_source_calls',[1,1,1,2,2,3,3,3],36,[128,256,512,576,1024])]:
 for N in steps:
  for k in [1,2,4]:
   p=completed_probability(N,weights,den,k);rows.append(dict(model=model,steps=N,k=k,probability=str(p),probability_float=float(p),interpretation='Exact Schur event probability for k1; rigorous lower bound for k>1 via k disjoint decreasing subsequences'))
root=Path(__file__).parent;root.joinpath('exact_renewal_bound.json').write_text(json.dumps(dict(scope='IID exact arithmetic distribution bound, not arbitrary-memory completeness or hardware evidence',rows=rows),indent=2)+'\n')
for r in rows:
 if r['model']=='two_axis_source_calls':print(r['steps'],r['k'],r['probability_float'])
