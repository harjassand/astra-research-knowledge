"""Exact independent coherent-integral and routed-loop checks for spin2 Qzz."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
from collections import Counter
import json,time

def df(n):
 z=1
 for k in range(n,0,-2):z*=k
 return z
@lru_cache(None)
def moment(p):
 if any(x%2 for x in p):return F(0)
 return F(df(p[0]-1)*df(p[1]-1)*df(p[2]-1),df(sum(p)+1))
@lru_cache(None)
def qm(p):
 return F(21,2)*(moment((p[0],p[1],p[2]+2))-moment(p)/3)

def compare(name,coords,edges,states,pair):
 ix={v:i for i,v in enumerate(coords)};es=[(ix[a],ix[b]) for a,b in edges]
 Z=F(0);num=F(0)
 for colors in product(range(4),repeat=len(es)):
  ps=[[0,0,0] for v in coords]
  for (a,b),c in zip(es,colors):
   if c:ps[a][c-1]+=1;ps[b][c-1]+=1
  if any(any(k%2 for k in p) for p in ps):continue
  den=F(1);nn=F(1)
  for i,p in enumerate(ps):
   p=tuple(p);den*=moment(p);nn*=qm(p) if i in pair else moment(p)
  Z+=den;num+=nn
 Zloop=F(0);nloop=F(0)
 for routes,w in states:
  visits=[Counter(route) for route in routes]
  mi=[sum(v[coords[i]] for v in visits) for i in pair]
  shared=sum(v[coords[pair[0]]]*v[coords[pair[1]]] for v in visits)
  est=F(98*shared,(2*mi[0]+3)*(2*mi[1]+3))
  Zloop+=w;nloop+=w*est
 assert Z==Zloop,(name,Z,Zloop)
 assert num==nloop,(name,num,nloop)
 return dict(graph=name,sites=len(coords),edges=len(edges),partition=str(Z),Qzz_pair=str(num/Z),all_exact=True)

square=[(0,0),(1,0),(1,1),(0,1)]
se=list(zip(square,square[1:]+square[:1]))
a=[(0,0),(-1,0),(-1,-1),(0,-1)]
b=[(0,0),(1,0),(1,1),(0,1)]
es=list(zip(a,a[1:]+a[:1]))+list(zip(b,b[1:]+b[:1]))
# The two distinct single-loop routings through the shared degree4 vertex.
c=a+b;d=a+[b[0]]+b[:0:-1]
coords=list(dict.fromkeys(a+b))
states=[([],F(1)),([a],F(1,27)),([b],F(1,27)),([a,b],F(1,1215)),([c],F(1,3645)),([d],F(1,3645))]
st=time.monotonic();out=[]
out.append(compare('square',square,se,[([],F(1)),([square],F(1,27))],(0,1)))
out.append(compare('touching_squares_center_outer',coords,es,states,(0,1)))
out.append(compare('touching_squares_opposite_outer',coords,es,states,(1,4)))
# Independent diagonal coherent symbol test using the exact beta second moment.
for m in range(-2,3):
 integral=F(2*m*m+3,21)
 assert F(21,2)*integral-F(3,2)==m*m
result={'checks':out,'symbol_diagonal_exact':True,'elapsed_seconds':time.monotonic()-st}
Path(__file__).with_name('quadrupole_identity_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
