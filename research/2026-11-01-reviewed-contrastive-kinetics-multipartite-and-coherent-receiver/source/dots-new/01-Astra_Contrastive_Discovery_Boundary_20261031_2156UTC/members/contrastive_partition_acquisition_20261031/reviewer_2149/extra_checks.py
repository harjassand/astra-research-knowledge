from fractions import Fraction as F
from pathlib import Path
import sys,json,random
import sympy as s
p=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(p));import construct as c
rng=random.Random(901);checks=0;refusals=0
for n,r in [(6,3),(8,4)]:
 k=n//r;order=list(range(n));rng.shuffle(order);parts=[order[g*k:(g+1)*k] for g in range(r)]
 Z=s.zeros(n,r)
 for g,pg in enumerate(parts):
  for i in pg:Z[i,g]=1
 W=Z.T/k;P=Z*W;J=s.ones(n)/n;Q=s.eye(n)-P;Jc=s.eye(n)-J
 perm=s.zeros(r)
 for g in range(r):perm[g,(g+1)%r]=1
 for sign in [-1,1]:
  D=sign*s.Rational(1,2)*(perm-s.ones(r)/r);C0=Z*D*W;beta=F(1,8192)
  E=Jc*s.Matrix(n,n,lambda i,j:s.Rational(rng.randrange(-1,2),8192*100*n*n))*Jc
  C=C0+E;rec=c.filter_projector(C,beta);pp=c.greedy_partition(rec)
  assert rec['rank']==r;checks+=1
  assert sorted(sorted(x) for x in pp['parts'])==sorted(sorted(x) for x in parts);checks+=1
  assert F(rec['roundoff_upper'])<=F(rec['nu'])/8;checks+=1
  Fmat=s.Matrix(rec['numerators'])/rec['denominator'];bound=4*r*s.Rational(1,8192)**2/(s.Rational(1,2)-s.Rational(1,8192))**2+2*n*s.Rational(rec['nu'])**2
  assert sum(x*x for x in Fmat-P)<=bound;checks+=1
  assert sum(x*x for x in E)<=s.Rational(1,8192)**2;checks+=1
 # Actual leakage receiving with reducing K=J, balanced P, small row-centered residual.
 for trial in range(12):
  R=s.Matrix(n,n,lambda i,j:s.Rational(rng.randrange(-2,3),100*n));R=R*Jc
  A=J+R;assert min(A)>=0 and A*s.ones(n,1)==s.ones(n,1);checks+=1
  eta=max(sum(abs(x) for x in R.row(i)) for i in range(n));rho2=sum(x*x for x in R)
  ci=max(sum(abs(x) for x in (A*Z-Z*W*A*Z).row(i))/2 for i in range(n))
  e2=max(n*sum(x*x for x in (W*A*Q).row(g)) for g in range(r))
  assert ci<=eta and e2<=r*rho2;checks+=1
# Expected proposal binding and malformed/insufficient count refusals.
toy={'status':'PARTITION_PROPOSAL','parts':[[0],[1]],'which':[0,1]}
for kw in [dict(expected_beta=True,expected_confidence=F(1,100),expected_proposal_sha256='x'),dict(expected_beta=F(1,4096),expected_confidence=F(1,100),expected_proposal_sha256='x')]:
 try:c.cleanup_from_counts([[1,0],[0,1]],[[0,1],[1,0]],toy,**kw)
 except (AssertionError,ValueError,TypeError):refusals+=1
 else:raise AssertionError('bad cleanup accepted')
base=dict(expected_n=2,expected_beta=F(1,4096),expected_column_confidence=F(1,100),expected_spectral_confidence=F(1,100))
for columns,rows in [([[True,1],[1,1]],[[[1,0],[0,1]],[[0,1],[1,0]]]),([[1,1],[1,2]],[[[1,0],[0,1]],[[0,1],[1,0]]]),([[1,1],[1,1]],[[[1,0],[0,2]],[[0,1],[1,0]]])]:
 try:c.proposal_from_counts(columns,rows,**base)
 except (AssertionError,ValueError,TypeError):refusals+=1
 else:raise AssertionError('bad count accepted')
print(json.dumps({'checks':checks,'additional_refusals':refusals,'new_source_observations':0,'scope':'Exact nonsymmetric/sign-reversed contrast, rank/clustering/filter precision and explicit receiving-norm inequalities; no sampled experiment.'},indent=2))
