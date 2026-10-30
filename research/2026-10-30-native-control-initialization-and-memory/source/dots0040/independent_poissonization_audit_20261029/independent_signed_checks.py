import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(4817)
def choi(f,d):
 out=np.zeros((d*d,d*d),complex)
 for i in range(d):
  for j in range(d):
   E=np.zeros((d,d),complex);E[i,j]=1
   out+=np.kron(E,f(E))/d
 return out
def diss(K,X):
 R=K.conj().T@K
 return K@X@K.conj().T-(R@X+X@R)/2
rows=[]
for d in [2,3,4]:
 for trial in range(10):
  A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));h=(A+A.conj().T)*.01
  Ks=[.03*(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))) for _ in range(2)]
  eps=2*np.linalg.norm(h,2)+2*sum(np.linalg.norm(K,2)**2 for K in Ks)
  rate=d*d*eps
  N=lambda X:-1j*(h@X-X@h)+diss(Ks[0],X)-diss(Ks[1],X)
  dep=lambda X:np.trace(X)*np.eye(d)/d
  phi=lambda X:dep(X)+N(X)/rate
  J=choi(phi,d);lo=np.linalg.eigvalsh(J).min();err=0;tp=0
  for i in range(d):
   for j in range(d):
    E=np.zeros((d,d),complex);E[i,j]=1
    tp=max(tp,abs(np.trace(phi(E))-np.trace(E)))
    err=max(err,np.linalg.norm(N(E)+rate*(dep(E)-E)-rate*(phi(E)-E)))
  assert lo>=-1e-12 and tp<1e-12 and err<1e-12
  rows.append(dict(d=d,min_choi=float(lo),identity_error=float(err),tp_error=float(tp)))
# Negative generator difference -D[lower] is explicitly not GKSL, but cushions successfully.
K=np.array([[0,1],[0,0]],complex);N=lambda X:-diss(K,X)
phi=lambda X:np.trace(X)*np.eye(2)/2+N(X)/8
assert np.linalg.eigvalsh(choi(phi,2)).min()>0
# Counterexample to replacing JOINT depolarization by a sum of onsite channels.
X=np.array([[0,1],[1,0]],complex);I=np.eye(2);H=np.kron(X,X)
Paulis=[I,X,np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def onsite_dep(A,site):
 return sum((np.kron(P,I) if site==0 else np.kron(I,P))@A@(np.kron(P,I) if site==0 else np.kron(I,P)) for P in Paulis)/4
neg=[]
for Lambda in [10.,100.]:
 f=lambda A:A+(-1j*(H@A-A@H)+onsite_dep(A,0)+onsite_dep(A,1)-2*A)/Lambda
 lo=np.linalg.eigvalsh(choi(f,4)).min();assert lo< -1e-7
 neg.append(dict(rate=Lambda,min_choi=float(lo)))
out=dict(status='pass',signed_HP_TA_trials=len(rows),worst_identity_error=max(r['identity_error'] for r in rows),worst_TP_error=max(r['tp_error'] for r in rows),minimum_CP_eigenvalue=min(r['min_choi'] for r in rows),negative_dissipator_difference_cushioned=True,onsite_is_not_joint_counterexamples=neg,scope='Finite matrix regressions; general claims rest on analytic normalized-Choi bound')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
