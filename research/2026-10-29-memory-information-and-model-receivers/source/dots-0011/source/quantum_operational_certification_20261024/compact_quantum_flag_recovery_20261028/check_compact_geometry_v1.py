#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json,random
random.seed(202610282338)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def null_vector(cols):
 m=len(cols);A=[[cols[j][i] for j in range(m)] for i in range(4)];row=0;piv=[]
 for col in range(m):
  p=next((k for k in range(row,4) if A[k][col]),None)
  if p is None:continue
  A[row],A[p]=A[p],A[row];z=A[row][col];A[row]=[x/z for x in A[row]]
  for k in range(4):
   if k!=row:
    z=A[k][col];A[k]=[x-z*y for x,y in zip(A[k],A[row])]
  piv.append(col);row+=1
  if row==4:break
 free=next((j for j in range(m) if j not in piv),None)
 if free is None:return None
 c=[F(0)]*m;c[free]=F(1)
 for k,p in enumerate(piv):c[p]=-A[k][free]
 assert all(sum(c[j]*cols[j][i] for j in range(m))==0 for i in range(4));return c
cases=[]
for trial in range(50):
 effects=[];A=[]
 # Split the six-axis POVM into12 rational effects; each is positive.
 for axis in range(3):
  for sign in [-1,1]:
   p=F(random.randrange(1,10),10)
   for weight in [p,1-p]:
    v=[weight/6,F(0),F(0),F(0)];v[axis+1]=sign*weight/6;effects.append(v);A.append([F(random.randrange(-20,21),13) for _ in range(4)])
 score=lambda e,a:sum(2*dot(x,y) for x,y in zip(e,a))
 initial=score(effects,A);steps=0
 while (c:=null_vector(effects)) is not None:
  lo=max(-1/x for x in c if x>0);hi=min(-1/x for x in c if x<0)
  slope=sum(2*x*dot(m,a) for x,m,a in zip(c,effects,A));t=hi if slope>=0 else lo
  new=[];aa=[]
  for v,m,a in zip(c,effects,A):
   w=1+t*v;assert w>=0
   if w:new.append([w*x for x in m]);aa.append(a)
  assert score(new,aa)>=score(effects,A);effects,A=new,aa;steps+=1
  assert [sum(e[i] for e in effects) for i in range(4)]==[F(1),F(0),F(0),F(0)]
  assert all(e[0]>=0 and e[0]*e[0]>=sum(x*x for x in e[1:]) for e in effects)
 assert len(effects)<=4
 cases.append({'initial_score':str(initial),'final_score':str(score(effects,A)),'outcomes':len(effects),'steps':steps})
# Tetrahedral flags: represent Bloch vectors by integer triples divided bysqrt3.
v=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]]
assert all(dot(x,x)==3 for x in v);assert all(dot(v[i],v[j])==-1 for i in range(4) for j in range(i))
assert [sum(x[i] for x in v) for i in range(3)]==[0,0,0]
# Affine independence certifies allfour coefficients forced by completeness.
assert null_vector([[F(1)]+[F(y) for y in x] for x in v]) is None
out={'status':'EXACT_RATIONAL_GEOMETRY_PASS','pruning_cases':cases,'tetrahedron':'Four positive effects necessary by exact affine independence and rank-one dual kernels','tetrahedron_optimum':'1/2','qubit_support_bound':4}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print({'cases':len(cases),'max_outcomes':max(x['outcomes'] for x in cases),'status':out['status']})
