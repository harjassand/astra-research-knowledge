"""Joint two-rib reduced T module. Declared-module proof, not whole-family F identification.
Each nonzero quotient label has physical minimum weight1 for d=3 old blue/red F.
"""
from itertools import product
import json
# Vertices 0,A,B,D0,D1; eight face-block ports.
edges=[(0,1),(1,3),(1,4),(0,2),(2,3),(2,4),(0,3),(3,4)]
reports={}
for color,nlabels in [('blue',4),('red',2)]:
 table={};matched=0
 for vals in product(range(nlabels),repeat=8):
  boundary=[0]*5
  for q,(u,v) in zip(vals,edges):boundary[u]^=q;boundary[v]^=q
  key=tuple(boundary[1:]);weight=sum(q!=0 for q in vals)
  if key not in table or (weight,vals)<table[key]:table[key]=(weight,vals)
  if key[:3]==(0,0,0):
   matched+=1
   s=key[3]
   assert weight>=2*(s!=0)
   target=(0,0,0,0,0,0,s,s)
   # Explicit solve using the four actual attaching triangles.
   diff=[a^b for a,b in zip(vals,target)]
   cycles=[(0,1,6),(1,2,7),(3,4,6),(4,5,7)]
   # Kill a− then a+ then b− then b+; remaining cycle-edge entries vanish.
   for pivot,cycle in [(0,cycles[0]),(2,cycles[1]),(3,cycles[2]),(5,cycles[3])]:
    q=diff[pivot]
    for j in cycle:diff[j]^=q
   assert not any(diff)
 for s in range(nlabels):assert table[(0,0,0,s)][0]==2*(s!=0)
 reports[color]=dict(all_input_quotient_patterns=nlabels**8,relative_classes=len(table),matched_patterns=matched,coarse_minima=[table[(0,0,0,s)][0] for s in range(nlabels)],passed=True,table=[dict(charges=k,min_weight=v[0],representative=v[1]) for k,v in sorted(table.items())])
print(json.dumps(reports,indent=2))
