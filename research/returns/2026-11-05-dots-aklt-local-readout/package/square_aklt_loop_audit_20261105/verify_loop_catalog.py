"""Independent orbit/embedding and local-pairing checks of the exported catalog."""
import json
from collections import Counter
from fractions import Fraction as F
rows=json.load(open('loop_catalog_through12.json'))

def norm_route(seq):
 x0=min(x for x,y in seq);y0=min(y for x,y in seq)
 seq=[(x-x0,y-y0) for x,y in seq]
 choices=[]
 for p in [seq,seq[::-1]]:
  choices.extend(tuple(p[k:]+p[:k]) for k in range(len(p)))
 return min(choices)

def edge(a,b):return tuple(sorted((a,b)))
summary={}
for r in rows:
 seq=[tuple(p) for p in r['cyclic_vertices']];n=r['length']
 assert len(seq)==n
 es={edge(seq[i],seq[(i+1)%n]) for i in range(n)}
 assert len(es)==n
 assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in es)
 visits=Counter(seq);assert all(v in [1,2] for v in visits.values())
 crossings=sum(v==2 for v in visits.values());assert crossings==r['degree4_vertices']
 assert F(r['activity'])==F(3,3**n)*F(3,5)**crossings
 orbits=set()
 for reflect in [False,True]:
  for rot in range(4):
   p=[]
   for x,y in seq:
    if reflect:x=-x
    for _ in range(rot):x,y=-y,x
    p.append((x,y))
   orbits.add(norm_route(p))
 embeddings=0
 for p in orbits:
  edges={edge(p[i],p[(i+1)%n]) for i in range(n)}
  embeddings+=sum(a[1]==b[1] for a,b in edges)
 assert embeddings==r['fixed_directed_edge_embeddings'],(r,embeddings)
 summary.setdefault(n,Counter())[crossings]+=embeddings
print('All',len(rows),'classes passed independent orientation/translation embedding checks.')
for n,c in summary.items():print(n,dict(c))
