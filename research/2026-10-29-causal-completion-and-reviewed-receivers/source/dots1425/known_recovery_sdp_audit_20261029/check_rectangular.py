import sympy as S,json,itertools,numpy as np
from pathlib import Path
I=S.I
def vec(A):return S.Matrix([A[i,j] for j in range(A.cols) for i in range(A.rows)])
def hh(n,z):
 v=S.Matrix([S.Rational(j+1,z+j+1)+I*S.Rational(z+j,2*z+j+1) for j in range(n)])
 return (S.eye(n)-2*v*v.H/(v.H*v)[0]).applyfunc(S.simplify)
def ptr(J,d,k):return S.Matrix(d,d,lambda i,j:sum(J[i*k+a,j*k+a] for a in range(k)))
rows=[]
for z in [1,2,3]:
 for k,d in [(2,3),(3,2)]:
  U=hh(3,z);V=hh(2,z+1)
  if k==2:
   K=[S.Rational(3,5)*U[:,:2]*V,S.Rational(4,5)*U[:,1:]*V]
   L=[V.H*U.H[:2,:],S.Matrix([[0],[1]])*U.H[2:,:]]
  else:
   K=[V*U.H[:2,:],S.Matrix([[0],[1]])*U.H[2:,:]]
   L=[U[:,:2]*V.H]
  K=[A.applyfunc(S.simplify) for A in K];L=[A.applyfunc(S.simplify) for A in L]
  assert sum((A.H*A for A in K),S.zeros(k)).applyfunc(S.simplify)==S.eye(k)
  assert sum((A.H*A for A in L),S.zeros(d)).applyfunc(S.simplify)==S.eye(d)
  C=sum((vec(A)*vec(A).H/k for A in K),S.zeros(k*d)).applyfunc(S.simplify)
  P=S.zeros(k*d)
  for i in range(k):
   for a in range(d):P[a*k+i,i*d+a]=1
  W=(P*C.T*P.H/k).applyfunc(S.simplify)
  direct=sum((vec(A.H)*vec(A.H).H/k**2 for A in K),S.zeros(k*d)).applyfunc(S.simplify)
  assert W==direct and S.trace(W)==S.Rational(1,k)
  J=sum((vec(A)*vec(A).H for A in L),S.zeros(k*d)).applyfunc(S.simplify)
  Fe=sum(S.Abs(S.trace(A*B))**2/k**2 for A in L for B in K)
  assert S.simplify(S.trace(W*J)-Fe)==0
  xi=S.Rational(1,101);X=S.zeros(d);X[0,1]=X[1,0]=1;Z=S.zeros(k);Z[0,0]=1;Z[1,1]=-1
  H=S.kronecker_product(X,Z);Jn=J+xi*H;Jp=(Jn+xi*S.eye(k*d))/(1+k*xi)
  assert ptr(Jp,d,k).applyfunc(S.simplify)==S.eye(d)
  # J is PSD by its explicit Kraus Gram; I+H PSD by eigenvalues, so Jp PSD exactly.
  assert all(ev>=0 for ev in (S.eye(k*d)+H).eigenvals())
  drop=S.simplify(S.trace(W*(Jn-Jp)));assert drop<=2*d*xi
  rows.append(dict(k=k,d=d,seed=z,exact_fidelity=str(S.simplify(Fe)),repair_drop=str(drop)))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(cases=rows,scope='Exact rectangular complex CPTP/Choi objective and physical repair checks; no generic SDP solver'),indent=2)+'\n');print('passed',len(rows))
