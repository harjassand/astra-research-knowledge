from pathlib import Path
import random,sys,itertools,json
import sympy as s
sys.path.insert(0,'robust_operator_reuse_20261031/finite_observation')
from robust_replay import sqrt_up
R=s.Rational;rng=random.Random(9103);checks=0
# Arbitrary subset variance envelope, including unrelated empirical and pooled rows.
for _ in range(100):
 r=4;raw=[rng.randrange(1,12) for _ in range(r)];b=[R(v,sum(raw)) for v in raw]
 N=rng.randrange(2,50);cs=[0]*r
 for j in range(N):cs[rng.randrange(r)]+=1
 p=[R(x,N) for x in cs];tau=sum(abs(x-y) for x,y in zip(b,p))/2
 bm=max(b);vb=bm*(1-bm) if bm>=R(1,2) else R(1,4);cap=min(R(1,4),vb+tau)
 for mask in range(1<<r):
  x=sum(p[j] for j in range(r) if mask>>j&1);assert x*(1-x)<=cap;checks+=1
# Exact complete block-record laws under genuinely different child-history actions.
n=5;parts=[[0,1],[2,3,4]];Z=s.zeros(n,2);W=s.zeros(2,n)
for g,pg in enumerate(parts):
 for i in pg:Z[i,g]=1;W[g,i]=R(1,len(pg))
P=Z*W;Q=s.eye(n)-P;A=[]
for a in range(2):
 rows=[]
 for i in range(n):
  raw=[rng.randrange(1,10) for _ in range(n)];rows.append([R(v,sum(raw))/10+R(9,10*n) for v in raw])
 A.append(s.Matrix(rows))
B=[W*M*Z for M in A]
c=max(sum(abs(x) for x in (A[a]*Z-Z*B[a]).row(i))/2 for a in range(2) for i in range(n))
e=max(sqrt_up(n*sum(x*x for x in (W*M*Q).row(g))) for M in A for g in range(2))
z=R(0);E=[R(0)]
for L in range(1,5):E.append(E[-1]+e*z);z=min(1,c+(1+e)*z)
for L in range(1,5):
 for trial in range(12):
  policy={hist:rng.randrange(2) for depth in range(1,L+1) for hist in itertools.product(range(2),repeat=depth)}
  for init in range(2):
   current={(init,):(W.row(init),R(1))}
   for t in range(L):
    nxt={}
    for hist,(law,mass) in current.items():
     action=policy[hist];step=law*A[action]
     for h,pg in enumerate(parts):
      restricted=s.zeros(1,n)
      for j in pg:restricted[j]=step[j]
      nxt[hist+(h,)]=(restricted,mass*B[action][hist[-1],h])
    current=nxt
   tv=sum(abs(sum(law)-mass) for law,mass in current.values())/2
   assert tv<=E[L];checks+=1
   assert sum(sum(law) for law,mass in current.values())==1;checks+=1
print(json.dumps({'checks':checks,'scope':'Exact subset variance envelopes and complete block-history record TV for unequal blocks; independent of sampled fixture and no statistical provenance claim.'},indent=2))
