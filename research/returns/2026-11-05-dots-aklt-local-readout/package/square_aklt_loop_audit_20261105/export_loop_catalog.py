"""Translation/D4 classes of single-loop pairings, including self-contacts.
A cyclic vertex sequence, modulo reversal, specifies the paired traversal.
"""
from weighted_trail_bound import enumerate_states,D
from collections import Counter
from fractions import Fraction as F
import json

def canonical(path):
 n=len(path);choices=[]
 for swap in [False,True]:
  for sx in [-1,1]:
   for sy in [-1,1]:
    p=[(sx*(y if swap else x),sy*(x if swap else y)) for x,y in path]
    for seq in [p,p[::-1]]:
     for k in range(n):
      q=seq[k:]+seq[:k];x0,y0=q[0]
      choices.append(tuple((x-x0,y-y0) for x,y in q))
 return min(choices)

rows=[]
for n in [4,6,8,10,12]:
 classes={}
 for ds in enumerate_states(n):
  ps=[(0,0)]
  for d in ds:ps.append((ps[-1][0]+D[d][0],ps[-1][1]+D[d][1]))
  if ps[-1]!=(0,0):continue
  can=canonical(ps[:-1])
  classes[can]=classes.get(can,0)+1
 for i,(path,count) in enumerate(sorted(classes.items())):
  visits=Counter(path);k=sum(v==2 for v in visits.values())
  assert max(visits.values())<=2
  rows.append(dict(length=n,class_index=i,cyclic_vertices=path,degree4_vertices=k,activity=str(F(3,3**n)*F(3,5)**k),fixed_directed_edge_embeddings=count))
 print(n,'D4/translation single-loop classes',len(classes),'crossed',sum(r['degree4_vertices']>0 for r in rows if r['length']==n),flush=True)
with open('loop_catalog_through12.json','w') as f:json.dump(rows,f,indent=2)
