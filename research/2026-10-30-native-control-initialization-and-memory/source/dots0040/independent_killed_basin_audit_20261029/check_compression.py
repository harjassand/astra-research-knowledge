import numpy as np,json
from scipy.linalg import expm
from pathlib import Path
rng=np.random.default_rng(2931);D=7;m=3
P=np.diag([1.]*m+[0.]*(D-m));Q=np.eye(D)-P
v=np.exp(np.arange(D)/4);V=np.diag(v);Vp=V[:m,:m]
A=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));H=(A+A.conj().T)/10
Ks=[(rng.normal(size=(D,D))+1j*rng.normal(size=(D,D)))/7 for _ in range(2)]
def adj(X):
 out=1j*(H@X-X@H)
 for K in Ks:
  R=K.conj().T@K;out+=K.conj().T@X@K-(R@X+X@R)/2
 return out
def gen(X):
 out=-1j*(H@X-X@H)
 for K in Ks:
  R=K.conj().T@K;out+=K@X@K.conj().T-(R@X+X@R)/2
 return out
def killed(X):
 Y=np.zeros((D,D),complex);Y[:m,:m]=X
 return gen(Y)[:m,:m]
def explicit(X):
 hp=H[:m,:m];out=-1j*(hp@X-X@hp)
 for K in Ks:
  kp=K[:m,:m];R=(K.conj().T@K)[:m,:m]
  out+=kp@X@kp.conj().T-(R@X+X@R)/2
 return out
err=0.;G=np.zeros((m*m,m*m),complex)
for i in range(m):
 for j in range(m):
  E=np.zeros((m,m),complex);E[i,j]=1
  err=max(err,np.linalg.norm(killed(E)-explicit(E)))
  G[:,i*m+j]=killed(E).reshape(-1)
T=expm(.3*G);J=np.zeros((m*m,m*m),complex);effect=np.zeros((m,m),complex)
for i in range(m):
 for j in range(m):
  E=np.zeros((m,m));E[i,j]=1
  out=T[:,i*m+j].reshape(m,m)
  J+=np.kron(E,out)/m;effect[j,i]=np.trace(out)
# L^*_P(Vp) = P L^*(V) P - sum P K† Q V Q K P.
kadj=1j*(H[:m,:m]@Vp-Vp@H[:m,:m])
for K in Ks:
 kp=K[:m,:m];R=(K.conj().T@K)[:m,:m]
 kadj+=kp.conj().T@Vp@kp-(R@Vp+Vp@R)/2
outgain=sum((K.conj().T@Q@V@Q@K)[:m,:m] for K in Ks)
drift_err=np.linalg.norm(kadj-adj(V)[:m,:m]+outgain)
assert err<1e-12 and drift_err<1e-12
assert np.linalg.eigvalsh(J).min()>-1e-12 and np.linalg.eigvalsh(np.eye(m)-effect).min()>-1e-12
result=dict(status='pass',compression_identity_error=err,drift_deletion_identity_error=drift_err,min_killed_Choi_eigenvalue=float(np.linalg.eigvalsh(J).min()),min_loss_effect_eigenvalue=float(np.linalg.eigvalsh(np.eye(m)-effect).min()),scope='Finite matrix compression/CP/drift identity regression only; not a weighted-drift or memory simulation')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
