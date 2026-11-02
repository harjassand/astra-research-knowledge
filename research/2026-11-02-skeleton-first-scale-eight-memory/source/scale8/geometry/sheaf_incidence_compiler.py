"""Compile genuine polygon/edge-code data to CSS columns over GF(2).
A caller must supply COMPLETE abstract cofaces. Coordinates are never used.
The compiler checks algebra, not the honesty/completeness of input incidence.
"""
from collections import defaultdict
import json

def echelon(columns):
 d={}
 for j,x in enumerate(columns):
  y=1<<j
  while x:
   k=x.bit_length()-1
   if k in d:x^=d[k][0];y^=d[k][1]
   else:d[k]=(x,y);break
 return d

def solve(d,x):
 y=0
 while x:
  k=x.bit_length()-1
  if k not in d:raise ValueError('not in column space')
  a,b=d[k];x^=a;y^=b
 return y

def nullspace(rows,n):
 # Row echelon with highest-bit pivots; free variable lifting.
 d={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in d:x^=d[p]
   else:d[p]=x;break
 free=[j for j in range(n) if j not in d]
 out=[]
 for j in free:
  x=1<<j
  for p,row in sorted(d.items()):
   if (row&x).bit_count()%2:x^=1<<p
  assert all((row&x).bit_count()%2==0 for row in rows)
  out.append(x)
 return out

def compile_sheaf(polygons,colors,complete_incidence=False):
 if not complete_incidence:raise ValueError('Full abstract incidence must be explicitly certified by caller')
 edges=defaultdict(list);vf=defaultdict(set);ve=defaultdict(set)
 for f,poly in enumerate(polygons):
  for v in poly:vf[v].add(f)
  for a,b in zip(poly,poly[1:]+poly[:1]):
   edge=tuple(sorted((a,b)));edges[edge].append(f);ve[a].add(edge);ve[b].add(edge)
 D1=[];edge_data={}
 for edge,fs in sorted(edges.items()):
  d=len(fs);color=colors.get(edge, 'degree2' if d==2 else None)
  if color is None:raise ValueError(('missing edge sheaf color',edge,d))
  if color in ['blue','degree2']:basis=[(1<<d)-1]
  elif color=='red':basis=[1|(1<<j) for j in range(1,d)]
  else:raise ValueError(color)
  start=len(D1)
  for x in basis:D1.append(sum(1<<fs[j] for j in range(d) if x>>j&1))
  edge_data[edge]=(fs,basis,start,echelon(basis))
 D0=[]
 for v,face_set in sorted(vf.items()):
  fs=sorted(face_set);pos={f:j for j,f in enumerate(fs)};constraints=[]
  for edge in ve[v]:
   ef,basis,_,_=edge_data[edge]
   for h in nullspace(basis,len(ef)):
    constraints.append(sum(1<<pos[ef[j]] for j in range(len(ef)) if h>>j&1))
  for u in nullspace(constraints,len(fs)):
   col=0
   for edge in ve[v]:
    ef,basis,start,solver=edge_data[edge]
    restriction=sum(((u>>pos[f])&1)<<j for j,f in enumerate(ef))
    col^=solve(solver,restriction)<<start
   image=0
   for q,c in enumerate(D1):
    if col>>q&1:image^=c
   assert image==0
   D0.append(col)
 r0=len(echelon(D0));r1=len(echelon(D1))
 return dict(C0=len(D0),C1=len(D1),C2=len(polygons),rank_delta0=r0,rank_delta1=r1,k=len(D1)-r0-r1,D0=D0,D1=D1,metachecks=nullspace(D1,len(polygons)))

if __name__=='__main__':
 # Exact §6.2.2 base case: single square, opposite blue/red boundaries.
 seed=compile_sheaf([['A','B','C','D']],{('A','B'):'blue',('B','C'):'red',('C','D'):'blue',('A','D'):'red'},True)
 assert seed['k']==1
 # Sphere sanity check: constant sheaf, six cube faces, H1=0.
 cube=[['000','100','110','010'],['001','101','111','011'],['000','100','101','001'],['010','110','111','011'],['000','010','011','001'],['100','110','111','101']]
 sphere=compile_sheaf(cube,{},True)
 assert sphere['k']==0 and len(sphere['metachecks'])==1
 print(json.dumps(dict(seed=seed,sphere=sphere),indent=2))
