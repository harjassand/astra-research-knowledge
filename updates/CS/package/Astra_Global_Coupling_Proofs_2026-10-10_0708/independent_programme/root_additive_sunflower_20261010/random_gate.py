from check_kernels import subspaces
from random import Random
import json
ss=[s for s in subspaces(5) if len(s)<=8]
planes=[s for s in ss if len(s)==4]
full=(1<<len(planes))-1
masks=[sum(1<<j for j,u in enumerate(planes) if len(s&u)==2)for s in ss]
rng=Random(20261010); found=None; checks=0
for _ in range(100000):
 inds=rng.sample(range(len(ss)),4); inter=set(range(32));mask=0
 for i in inds:inter.intersection_update(ss[i]);mask|=masks[i]
 if inter!={0}:continue
 checks+=1
 if mask==full:found=[sorted(ss[i])for i in inds];break
print(json.dumps({'m':5,'w':4,'seed':20261010,'draws_limit':100000,'jointly_injective_checks':checks,'kernels_cardinality_max':8,'planes':len(planes),'counterexample':found,'scope':'Random falsification only; no exhaustive claim.'},indent=2))
