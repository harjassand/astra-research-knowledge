from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import hashlib,json

def eye(k):return [[F(i==j) for j in range(k)] for i in range(k)]
def mul(a,b):return [[sum(a[i][r]*b[r][j] for r in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def trans(a):return list(map(list,zip(*a)))
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def sc(s,a):return [[s*x for x in r] for r in a]
def sub(a,b):return add(a,sc(-1,b))
def fro(a):return sum(x*x for r in a for x in r)
def diag(v):return [[v[i] if i==j else F(0) for j in range(len(v))] for i in range(len(v))]
def det(a):
 if not a:return F(1)
 return sum(((-1)**j)*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))
def psd(a):
 k=len(a)
 return all(det([[a[i][j] for j in ix] for i in ix])>=0 for r in range(1,k+1) for ix in combinations(range(k),r))
def block(A,B,D):
 return [a+b for a,b in zip(A,B)]+[b+d for b,d in zip(trans(B),D)]
count=0
for k in [2,3,4]:
 Q=eye(k);Q[0][0]=Q[1][1]=F(3,5);Q[0][1]=F(-4,5);Q[1][0]=F(4,5)
 assert mul(trans(Q),Q)==eye(k)
 for shift in range(4):
  vals=[F(0),F(9,25),F(16,25),F(1)]
  es=[vals[(i+shift)%4] for i in range(k)]
  roots={F(0):F(0),F(9,25):F(3,5),F(16,25):F(4,5),F(1):F(1)}
  cv=lambda z:mul(mul(Q,diag(z)),trans(Q))
  A=cv(es);D=sub(eye(k),A);Ar=cv([roots[x] for x in es]);Dr=cv([roots[1-x] for x in es])
  PA=cv([F(x>0) for x in es]);PD=cv([F(x<1) for x in es])
  Ari=cv([1/roots[x] if x else F(0) for x in es]);Dri=cv([1/roots[1-x] if x<1 else F(0) for x in es])
  den=1
  import math
  for row in A+D:
   for x in row:den=math.lcm(den,x.denominator)
  mu=F(1,den**k)
  assert all(x>=mu for x in es+[1-x for x in es] if x)
  K=[[F(j==(i+shift)%k) for j in range(k)] for i in range(k)]
  B=mul(mul(Ar,K),Dr);C=block(A,B,D)
  assert psd(C)
  ww=[[F((i+2*j+shift)%5-2,3) for j in range(2*k)] for i in range(2*k)]
  W=mul(ww,trans(ww));w=fro(W)
  op=[[F((2*i+j)%3-1,2) for j in range(2*k)] for i in range(2*k)];op=sc(F(1,2),add(op,trans(op)))
  aa=fro(op);cc=F(2,3);bnum=1+cc**2+2*k*aa
  N=lambda T:(cc+tr(mul(op,T)))**2
  for powr in [0,8,30]:
   m0=F(1,2**powr);t=min(F(1,4),m0/(1200*bnum),m0/(400*k*(1+w)));e=t*mu/4
   perturb=[[e/k for _ in range(k)] for _ in range(k)];assert fro(perturb)<=e*e
   Bfin=sc(1-t,mul(mul(PA,add(B,perturb)),PD));Cf=block(A,Bfin,D)
   Kn=mul(mul(Ari,Bfin),Dri)
   assert psd(sub(eye(k),mul(trans(Kn),Kn)))
   assert psd(Cf)
   assert add([r[:k] for r in Cf[:k]],[r[k:] for r in Cf[k:]])==eye(k)
   assert fro(sub(Cf,C))<=4*k*t*t
   u=m0+tr(mul(W,C));uf=m0+tr(mul(W,Cf))
   assert abs(uf-u)<=m0/400
   assert abs(N(Cf)-N(C))<=m0/200
   assert N(Cf)/uf>=F(99,100)*N(C)/u-F(1,100)
   count+=1
p=Path(__file__).with_name('ordinary_fixed_effect_rational_channel_completion_20261028.md')
out={'status':'PASS exact Fraction fixtures; independent receiving pending','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exact_fixed_slice_cases':count,'matrix_dimensions':[4,6,8],'source_calls':0,'scope':'Known rational effects with singular/zero/one eigenspaces, exact arithmetic support projectors and Choi principal-minor PSD, explicit denominator floor, cost/numerator transfer. No source data or general canonical polar approximation algorithm.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
