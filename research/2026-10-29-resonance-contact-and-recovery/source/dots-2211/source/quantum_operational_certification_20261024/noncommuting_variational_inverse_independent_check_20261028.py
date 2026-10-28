"""Independent exact algebra challenge of symmetric operator-block variational certificate."""
from pathlib import Path
import sympy as s,json
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z];B=[s.kronecker_product(x,I) for x in P]
p0=s.diag(1,0);pp=s.ones(2)/2
u=s.Matrix([s.Rational(3,5),0,s.Rational(4,5)])
T0=s.diag(s.Rational(4,5),s.Rational(4,5),s.Rational(16,25));T1=s.Rational(4,5)*s.eye(3)-s.Rational(4,25)*u*u.T
coef=[[s.kronecker_product(I,(T0[j,k]*p0+T1[j,k]*pp)/4) for k in range(3)] for j in range(3)]
Tb=s.BlockMatrix(coef).as_explicit();tau=s.Rational(1,25)
# T>=tau I from T_a>=16/25 I and p0+pp>=1/4 I.
assert (p0+pp-s.eye(2)/4).is_positive_definite
assert (T0-s.eye(3)*s.Rational(16,25)).is_positive_semidefinite
assert (T1-s.eye(3)*s.Rational(16,25)).is_positive_semidefinite
C=[sum((B[k]*coef[k][j] for k in range(3)),s.zeros(4)) for j in range(3)]
assert any(coef[j][k]*coef[l][m]!=coef[l][m]*coef[j][k] for j in range(3) for k in range(3) for l in range(3) for m in range(3))
def f(A,C):return s.expand(sum(s.trace(a*c) for a,c in zip(A,C)))
def expectation(A,M):return (M+sum((a*M*a for a in A),s.zeros(4)))/4
def fitted(A,C):
 raw=[[expectation(A,(A[k]*C[j]+C[j]*A[k])/2) for j in range(3)] for k in range(3)]
 return [[(raw[j][k]+raw[k][j])/2 for k in range(3)] for j in range(3)]
assert fitted(B,C)==coef
count=0; positivefits=0
for m in [2,3,5,10,20]:
 # rational entangling competitor, tending to identity as m increases.
 c=s.Rational(m*m-1,m*m+1);v=s.Rational(2*m,m*m+1)
 U=s.eye(4);U[0,0]=U[3,3]=c;U[0,3]=v;U[3,0]=-v
 A=[U*b*U.H for b in B];D=[a-b for a,b in zip(A,B)]
 Q=sum((s.trace(D[j]*coef[j][k]*D[k]) for j in range(3) for k in range(3)),s.S.Zero)
 d2=sum(s.trace(d*d) for d in D)
 assert s.simplify(Q-2*(f(B,C)-f(A,C)))==0
 assert s.simplify(Q-tau*d2)>=0
 Sf=fitted(A,C); Sb=s.BlockMatrix(Sf).as_explicit()
 assert all(A[l]*Sf[j][k]==Sf[j][k]*A[l] for l in range(3) for j in range(3) for k in range(3))
 Cfit=[sum((A[k]*Sf[k][j] for k in range(3)),s.zeros(4)) for j in range(3)]
 # Certify fixed rational kappa via exact leading principal minors.
 kap=s.Rational(1,100)
 if all((Sb-kap*s.eye(12))[:i,:i].det()>0 for i in range(1,13)):
  res2=sum(s.trace((x-y)**2) for x,y in zip(Cfit,C))
  assert s.simplify(kap*kap*d2-4*res2)<=0
  positivefits+=1
 count+=1
# One exact rational nonzero-data-error feasibility witness.
a=s.Rational(1,10**6);kap=s.Rational(1,100);delta=s.Rational(1,10)
Chat=[C[0]+a*s.kronecker_product(Z,X),C[1]+a*s.kronecker_product(X,Z),C[2]+a*s.kronecker_product(Y,X)]
S=fitted(B,Chat);Sblock=s.BlockMatrix(S).as_explicit()
assert all((Sblock-kap*s.eye(12))[:i,:i].det()>0 for i in range(1,13))
Cfit=[sum((B[k]*S[k][j] for k in range(3)),s.zeros(4)) for j in range(3)]
r2=sum(s.trace((x-y)**2) for x,y in zip(Cfit,Chat))
assert r2<=kap**2*delta**2/16
assert 12*a*a<=kap**2*delta**2/16
r={'status':'PASS_INDEPENDENT_EXACT_VARIATIONAL_AND_FIT_IDENTITIES','noncommuting_coefficient_blocks':True,'competitor_triples':count,'strict_positive_fitted_certificates':positivefits,'known_true_block_lower_bound':'1/25','candidate_tested_lower_bound':'1/100','exact_true_coefficient_reacquisition':True,'nonzero_error_algebraic_feasibility_witnesses':1,'source_calls':0,'scope':'Exact algebra diagnostics and candidate proof review; no global optimization, statistical acquisition, or hardware execution.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
