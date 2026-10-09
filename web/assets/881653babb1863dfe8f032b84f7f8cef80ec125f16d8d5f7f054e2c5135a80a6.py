"""Exact finite-cone derivation and rational PSD certificates. No solver."""
from itertools import combinations
from functools import reduce
from math import gcd
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
L=[s.Matrix(v) for v in [(8,0,0),(2,6,0),(0,6,3),(0,0,12)]]
e=[s.Matrix(v) for v in [(1,0,0),(0,1,0),(0,0,1)]]
rays=set()
cone_rays=[]
for a in range(4):
 normals=e+[L[a]-L[b] for b in range(4) if b!=a]
 found=set()
 for n,m in combinations(normals,2):
  cross=n.cross(m)
  if cross==s.zeros(3,1): continue
  for v in [cross,-cross]:
   if all(v.dot(k)>=0 for k in normals):
    ints=[int(q) for q in v]
    common=reduce(gcd, [abs(q) for q in ints])
    found.add(tuple(q//common for q in ints))
 cone_rays.append(sorted(found)); rays.update(found)
expected={(1,0,0),(0,1,0),(0,0,1),(1,1,0),(3,0,2),(0,3,2),(3,3,2)}
assert rays==expected,(rays,expected)
I=s.eye(3)
k3=lambda A,B,C:s.kronecker_product(A,B,C)
WX=s.zeros(27); WY=s.zeros(27)
for i,j in combinations(range(3),2):
 X=s.zeros(3); X[i,j]=X[j,i]=1
 Y=s.zeros(3); Y[i,j]=s.I; Y[j,i]=-s.I
 WX+=k3(X.T,X,I)+k3(X.T,I,X)
 WY+=k3(Y.T,Y,I)+k3(Y.T,I,Y)
WD=s.diag(*[3*(int(a==b)+int(a==c))-2
              for a in range(3) for b in range(3) for c in range(3)])
def exact_psd(M):
 M=[list(row) for row in M.tolist()]
 positive=[]; zero=[]
 for k in range(27):
  p=M[k][k]
  assert p.is_Rational and p>=0,(k,p)
  if p==0:
   assert all(M[i][k]==M[k][i]==0 for i in range(k+1,27)),k
   zero.append(k); continue
  positive.append(str(p))
  for i in range(k+1,27):
   for j in range(k+1,27):
    M[i][j]-=M[i][k]*M[k][j]/p
 return {'positive_pivots':positive,'zero_pivot_indices':zero}
cert=[]
for ray in sorted(rays):
 x,y,z=map(s.Rational,ray)
 V=2*(x+y+z)
 k=max(s.Rational(4,3)*x,x/3+y,y+z/2,2*z)
 W=x*WX+y*WY+z*WD
 upper=V+k
 pivots=exact_psd(upper*s.eye(27)-W)
 cert.append({'ray':ray,'V':str(V),'k':str(k),'star_upper_bound':str(upper),**pivots})
report={'status':'EXACT_PASS','unique_ray_count':len(rays),
        'ray_list':sorted(rays),'cones':cone_rays,'ray_psd_certificates':cert,
        'scope':'Seven cone generators exhaust all nonnegative sector weights. Rational LDL proves W <= (V+k) I on each generator, hence all weights by conic linearity inside each support cone. A full-domain common-map conclusion additionally requires the channel itself to be signed-permutation covariant.'}
(OUT/'seven_ray_cone_replay.json').write_text(json.dumps(report,indent=2)+'\n')
print('EXACT_PASS: seven distinct rays, all rational PSD certificates.')
print('Ray list:',sorted(rays))
