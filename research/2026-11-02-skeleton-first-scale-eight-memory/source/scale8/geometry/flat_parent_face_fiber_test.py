"""Relative cohomology of the flat doubled two-rib disk under NAIVE parent-face assignment.
This is a subdivision-invariant topological test, not a Hamming-isometric identification.
Boundary sheet edges and vertical rib endpoints are excluded (belong to old boundary).
"""
from collections import defaultdict
import json

def rank(cols):
 d={}
 for x in cols:
  while x:
   p=x.bit_length()-1
   if p in d:x^=d[p]
   else:d[p]=x;break
 return len(d)
faces=[]
# Compact each of the three intervals separated by ribs to a single edge.
for z in [0,1]:
 for x in range(3):
  for y in range(3):faces.append([(x,y,z),(x+1,y,z),(x+1,y+1,z),(x,y+1,z)])
for x in [1,2]:
 for y in range(3):faces.append([(x,y,0),(x,y+1,0),(x,y+1,1),(x,y,1)])
for y in [1,2]:
 for x in range(3):faces.append([(x,y,0),(x+1,y,0),(x+1,y,1),(x,y,1)])
inc=defaultdict(list)
for j,p in enumerate(faces):
 for a,b in zip(p,p[1:]+p[:1]):inc[tuple(sorted((a,b)))].append(j)
def on_boundary(v):return v[0] in [0,3] or v[1] in [0,3]
# A whole edge is in the old boundary iff it lies on one outer side.
def boundary_edge(e):
 a,b=e
 return any(a[j]==b[j] and a[j] in [0,3] for j in [0,1])
edges=[e for e in sorted(inc) if not boundary_edge(e)]
D1=[sum(1<<f for f in inc[e]) for e in edges]
vertices=[(x,y,z) for z in [0,1] for x in [1,2] for y in [1,2]]
D0=[sum(1<<j for j,e in enumerate(edges) if v in e) for v in vertices]
for c in D0:
 image=0
 for j,d in enumerate(D1):
  if c>>j&1:image^=d
 assert image==0
r0,r1=rank(D0),rank(D1)
result=dict(scope=__doc__,C0=len(D0),C1=len(D1),C2=len(faces),rankD0=r0,rankD1=r1,H0=len(D0)-r0,H1=len(D1)-r0-r1,H2=len(faces)-r1,degree3_sheet_columns=sum(len(inc[e])==3 for e in edges),degree4_vertical_columns=sum(len(inc[e])==4 for e in edges),D0=D0,D1=D1)
assert (result['H0'],result['H1'],result['H2'])==(0,0,10)
print(json.dumps(result,indent=2))
