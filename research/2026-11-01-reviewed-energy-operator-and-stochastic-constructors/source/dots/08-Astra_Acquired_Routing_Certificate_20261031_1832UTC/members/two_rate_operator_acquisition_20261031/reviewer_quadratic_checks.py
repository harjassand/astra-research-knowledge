"""Independent exact mathematics checks; does not overwrite author outputs."""
import itertools, random, json, sys
from pathlib import Path
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parent))
from quadratic_leakage import R,incoming_stat,outgoing_stat,upper_squared,sqrt_up
from retained_large_acquisition import compression,eb_radius,clog2

def run():
 checks=0
 def ck(x):
  nonlocal checks
  assert x;checks+=1
 rng=random.Random(837)
 # Uniform-H recurrence, nonuniform blocks, nonstationary true operators,
 # perturbed stochastic coarse actions, both signs of task/output coefficients.
 for n,parts in [(3,[[0],[1,2]]),(4,[[0,1],[2,3]]),(4,[[0],[1],[2,3]])]:
  r=len(parts);Z=s.zeros(n,r);W=s.zeros(r,n)
  for g,p in enumerate(parts):
   for i in p:Z[i,g]=1;W[g,i]=R(1,len(p))
  P=Z*W;Q=s.eye(n)-P
  A=[];B=[]
  for a in range(2):
   rows=[]
   for i in range(n):
    z=[rng.randrange(1,8) for _ in range(n)];rows.append([R(v,sum(z)) for v in z])
   M=s.Matrix(rows);A.append(M);K=W*M*Z
   B.append(R(9,10)*K+s.ones(r,r)/(10*r))
  ein=max(sqrt_up(sum(v*v for v in Q*M*P)) for M in A)
  eout=max(sqrt_up(n*sum(v*v for v in (W*M*Q).row(g))) for M in A for g in range(r))
  alpha=max(sqrt_up(sum(v*v for v in Q*M*Q)) for M in A)
  d=max(sum(abs(v) for v in (W*M*Z-N).row(g)) for M,N in zip(A,B) for g in range(r))
  ub=s.Matrix([(-1)**g for g in range(r)]);b=Z*ub
  ell=(s.Matrix([[R((-1)**g,r) for g in range(r)]])*W)
  M=max(abs(v) for v in b);C=sum(abs(v) for v in ell)
  for L in range(5):
   bound=C*M*(L*d+compression(ein,eout,alpha,L))
   for word in itertools.product(range(2),repeat=L):
    x=b;y=ub
    for a in word:x=A[a]*x;y=B[a]*y
    ck(abs((ell*x-ell*Z*y)[0])<=bound)
 # Unequal block masses and row laws: exact incoming variance decomposition.
 for parts in [[[0],[1,2]],[[0,1],[2]]]:
  n=3;r=2;probs=[[R(1,5),R(4,5)],[R(2,3),R(1,3)],[R(3,7),R(4,7)]]
  P=s.zeros(n)
  for p in parts:
   for i in p:
    for j in p:P[i,j]=R(1,len(p))
  Q=s.eye(n)-P;D=s.diag(*[s.sqrt(R(n,len(p))) for p in parts]);M=s.Matrix(probs)*D
  covs=[D*(s.diag(*p)-s.Matrix(p)*s.Matrix(p).T)*D for p in probs]
  cov=s.diag(*covs);Qbig=s.kronecker_product(Q,s.eye(r));v=s.simplify((M.T*Q*M).trace()/n)
  mean=R(0);second=R(0)
  for seq in itertools.product(range(r),repeat=2*n):
   pr=s.prod(probs[i][seq[i]]*probs[i][seq[n+i]] for i in range(n))
   left=[[int(seq[i]==g) for g in range(r)] for i in range(n)]
   right=[[int(seq[n+i]==g) for g in range(r)] for i in range(n)]
   val=incoming_stat(left,right,parts);mean+=pr*val;second+=pr*val*val
  QM=Q*M;linear=R(2,n*n)*sum((QM.row(i)*covs[i]*QM.row(i).T)[0] for i in range(n));bilinear=(Qbig*cov*Qbig*cov).trace()/n**2
  sigma=max(C.trace() for C in covs);T=sum(C.trace() for C in covs)
  ck(mean==v);ck(s.simplify(second-mean**2-linear-bilinear)==0);ck(s.simplify(second-mean**2)<=2*sigma*v/n+sigma*T/n**2)
 # Exact probability coverage for Bernoulli empirical Bernstein radii.
 for N in [2,10,50,100]:
  for p in [R(1,20),R(1,2),R(19,20)]:
   delta=R(1,10);K=clog2(4/delta);bad=R(0)
   for c in range(N+1):
    rad=eb_radius(c,N,K)
    if abs(p-R(c,N))>rad:bad+=s.binomial(N,c)*p**c*(1-p)**(N-c)
   ck(bad<=delta)
 delta=R(1,1000)
 for rounds in range(1,10):
  spent=4*delta/8+sum(2*delta/(4*(t+1)*(t+2)) for t in range(rounds))
  ck(spent<=delta)
 return {'status':'PASS','checks':checks,'scope':'Exact finite algebra/probability checks, not proof of provenance or a statistical coverage simulation.'}
if __name__=='__main__':
 out=run();Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
