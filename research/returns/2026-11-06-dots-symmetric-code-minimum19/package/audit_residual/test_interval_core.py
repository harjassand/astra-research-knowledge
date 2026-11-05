"""Independent exact endpoint tests, including nonzero-width intervals."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,time
from verify_interval_dual import B,Q,bsqrt
import numpy as np
start=time.perf_counter();checks=0
vals=[F(-7,3),F(-1,19),F(0),F(1,7),F(3,2),F(67,11)]
def contains(b,x):
 global checks
 assert F(int(b.m-b.r),Q)<=x<=F(int(b.m+b.r),Q);checks+=1
for x,y in product(vals,repeat=2):
 a=B.exact(x);b=B.exact(y)
 contains(a+b,x+y);contains(a-b,x-y);contains(a*b,x*y)
for mx,my,rx,ry in product([-3*Q//2,0,7*Q//3],[-2*Q,5*Q//9],[1,Q//17],[2,Q//23]):
 a=B(mx,rx);b=B(my,ry)
 for sx,sy in product([-1,1],repeat=2):
  x=F(mx+sx*rx,Q);y=F(my+sy*ry,Q)
  contains(a+b,x+y);contains(a-b,x-y);contains(a*b,x*y)
A=B([[Q//3,-Q//7],[2*Q,Q//11]],[[3,Q//31],[Q//17,2]])
C=B([[-Q//5,Q//2],[Q//3,-Q]],[[Q//29,2],[4,Q//19]])
D=A@C
for sa,sc in product(product([-1,1],repeat=4),repeat=2):
 a=np.array([F(int(m+s*r),Q) for m,r,s in zip(A.m.flat,A.r.flat,sa)],dtype=object).reshape(2,2)
 c=np.array([F(int(m+s*r),Q) for m,r,s in zip(C.m.flat,C.r.flat,sc)],dtype=object).reshape(2,2)
 v=a@c
 for i,j in product(range(2),repeat=2):contains(D[i,j],v[i,j])
for f in [F(0),F(1),F(2),F(1,3),F(99991,99877),F(1,2**400)]:
 b=bsqrt(f);lo=max(F(0),F(int(b.m-b.r),Q));hi=F(int(b.m+b.r),Q);assert lo*lo<=f<=hi*hi;checks+=1
out={'status':'PASS exact interval core endpoint tests','checks':checks,'includes_nonzero_input_radii':True,'matrix_endpoint_combinations':256,'elapsed_seconds':time.perf_counter()-start}
Path(__file__).with_name('interval_core_tests.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
