import sympy as s, random, sys, json
from pathlib import Path
sys.path.insert(0,'robust_operator_reuse_20261031/finite_observation')
from robust_replay import sqrt_up
R=s.Rational
rng=random.Random(271828);checks=0;caps=0
for n,parts in [(5,[[0],[1,2],[3,4]]),(6,[[0,1],[2,3,4],[5]])]:
 r=len(parts);Z=s.zeros(n,r);W=s.zeros(r,n)
 for g,pg in enumerate(parts):
  for i in pg:Z[i,g]=1;W[g,i]=R(1,len(pg))
 P=Z*W;Q=s.eye(n)-P
 A=[];C=[];B=[]
 for a in range(3):
  rows=[]
  for i in range(n):
   raw=[rng.randrange(1,9) for j in range(n)];rows.append([R(v,sum(raw)) for v in raw])
  M=s.Matrix(rows);A.append(M)
  C.append((M+s.ones(n)/n)/2)
  B.append((W*M*Z+s.ones(r)/r)/2)
 norm=lambda M:sqrt_up(sum(x*x for x in M))
 ein=max(norm(Q*M*P) for M in A)
 eout=max(sqrt_up(n*sum(x*x for x in (W*M*Q).row(g))) for M in A for g in range(r))
 t=max(norm(A[a]-C[a]) for a in range(3))
 d=max(sum(abs(x) for x in (W*A[a]*Z-B[a]).row(g)) for a in range(3) for g in range(r))
 U=s.Matrix(r,r,lambda g,h:max(norm((Q*C[a]*Q).extract(parts[g],parts[h])) for a in range(3)))
 c=max(ein*sqrt_up(R(n,len(pg))) for pg in parts)
 k=max(sum(sqrt_up(R(len(ph),len(pg)))*U[g,h] for h,ph in enumerate(parts))+t*sqrt_up(R(n,len(pg))) for g,pg in enumerate(parts))
 # Inflate valid bounds to force the cap and noncontractive regime independently.
 k=max(k,R(3,2));c=max(c,R(3,4));z=[R(0)];err=[R(0)]
 for depth in range(1,6):z.append(min(1,c+k*z[-1]));err.append(err[-1]+d+eout*z[-2]);caps+=int(z[-1]==1)
 reward=[R(1,5),R(1),R(0)]
 def tree(g,depth):
  global checks
  if depth==0:return s.ones(len(parts[g]),1)*reward[g],reward[g]
  children=[tree(h,depth-1) for h in range(r)]
  full=s.zeros(n,1)
  for h,pg in enumerate(parts):
   for j,i in enumerate(pg):full[i]=children[h][0][j]
  # Each tree node can choose a different history-dependent randomized action.
  weights=[rng.randrange(1,5) for _ in range(3)];weights=[R(x,sum(weights)) for x in weights]
  true=sum((weights[a]*(A[a]*full).extract(parts[g],[0]) for a in range(3)),s.zeros(len(parts[g]),1))
  coarse=sum(weights[a]*sum(B[a][g,h]*children[h][1] for h in range(r)) for a in range(3))
  avg=sum(true)/len(parts[g]);res=true-s.ones(len(parts[g]),1)*avg
  assert abs(avg-coarse)<=err[depth];checks+=1
  assert res.dot(res)/len(parts[g])<=z[depth]**2;checks+=1
  return true,coarse
 for g in range(r):tree(g,4)
print(json.dumps({'checks':checks,'capped_steps':caps,'scope':'Exact unequal three-block/three-action counterfactual trees with nonzero observation and coarse errors, randomized node choices, and deliberately noncontractive capped recurrence.'}))
