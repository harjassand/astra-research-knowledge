#!/usr/bin/env python3
"""Exact integer-matrix tests; K,D normalizations factored out."""
import json, random
import numpy as np
n=4;D=16;I=np.eye(D,dtype=np.int64)
def par(x):return x.bit_count()&1
def P(x,z):
    a=np.zeros((D,D),dtype=np.int64)
    for j in range(D):a[j^x,j]=-1 if par(j&z) else 1
    return a
def syn(x,z):return par(z)|(par(x)<<1)
ps={(x,z):P(x,z) for x in range(D) for z in range(D)}
gs=[P(15,0),P(0,15)]
qs={s:(I+(-1 if s&1 else 1)*gs[0])@(I+(-1 if s&2 else 1)*gs[1]) for s in range(4)}
cases=0
for s in range(4):
 for t in range(4):
  for label,p in ps.items():
   out=p@qs[s]@p.T@qs[t]
   target=4*qs[t] if s^t==syn(*label) else np.zeros((D,D),dtype=np.int64)
   assert np.array_equal(out,target)
   cases+=1
single=[(0,0)]+[(1<<j,0) for j in range(4)]+[(0,1<<j) for j in range(4)]+[(1<<j,1<<j) for j in range(4)]
rng=random.Random(20261030)
for _ in range(8192):
 s=rng.randrange(4);pkey=rng.choice(list(ps));p=ps[pkey]
 ei=rng.choice(single);eb=rng.choice(single);t=s^syn(*pkey)^syn(*ei)
 out=p@ps[eb]@qs[s]@p.T@ps[ei]@qs[t]
 target=4*ps[eb]@ps[ei]@qs[t]
 assert np.array_equal(out,target) or np.array_equal(out,-target)
print(json.dumps({'code':'[[4,2,2]] CSS','exact_unknown_input_operator_cases':cases,
 'incoming_and_resource_error_cases':8192,'passed':True},indent=2))
