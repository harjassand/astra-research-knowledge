"""Independent operator-level robustness and exact sampler-order checks."""
import numpy as np,json
from scipy.linalg import expm
from fractions import Fraction as F
from pathlib import Path
rng=np.random.default_rng(295553);I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]);pa=(X,Y,Z);D=4
S0=(np.eye(4)+sum(np.kron(p,p) for p in pa))/2

def E(ks,S):
 ss=np.kron(S,I);G=np.zeros((8,8),complex)
 for k in ks:
  comm=k@ss-ss@k;G+=comm.conj().T@comm
 return np.trace(G.reshape(4,2,4,2),axis1=0,axis2=2)/8

def channel():
 z=rng.normal(size=(32,8))+1j*rng.normal(size=(32,8));q,_=np.linalg.qr(z);return list(q.reshape(4,8,8))
maxidentity=0.;maxpositive=-1.;maxgamma=-1.;maxmixture=0.;maxcoherent=-1.
for j in range(50):
 ks=channel();z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));sig=z@z.conj().T;sig/=np.trace(sig)
 angle=.005+.1*rng.random();axis=rng.normal(size=3);axis/=np.linalg.norm(axis);u=expm(-.5j*angle*sum(axis[a]*pa[a] for a in range(3)))
 S=np.kron(u,I)@S0@np.kron(u.conj().T,I)
 C=np.array([[np.trace(pa[a]@u@pa[b]@u.conj().T).real/2 for b in range(3)] for a in range(3)])
 es=E(ks,S);e0=E(ks,S0);delta=np.trace(sig@es).real
 direct=1-np.trace(np.kron(S,I)@sum(k@np.kron(S,sig)@k.conj().T for k in ks)).real/4
 maxidentity=max(maxidentity,abs(delta-direct));maxpositive=max(maxpositive,-np.linalg.eigvalsh(es).min(),np.linalg.eigvalsh(es).max()-2)
 aa=4.5*np.linalg.norm(C-np.eye(3))**2
 for gamma in [.001,.01,.1,1,10]:maxgamma=max(maxgamma,np.linalg.eigvalsh(es-(1+gamma)*e0-(1+1/gamma)*aa*I).max())
 U0=expm(-.43j*np.kron((np.kron(Z,I)+np.kron(I,Z))/2,X))
 lam=F(j+1,100);mixed=[np.sqrt(1-float(lam))*U0]+[np.sqrt(float(lam))*k for k in ks]
 maxmixture=max(maxmixture,float(np.linalg.norm(E(mixed,S0)-float(lam)*e0)))
 A=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));H=(A+A.conj().T)/2;H/=np.linalg.norm(H,2)
 U=expm(-.04j*H)@U0;nu=np.linalg.norm(U-U0,2)
 maxcoherent=max(maxcoherent,np.linalg.eigvalsh(E([U],S0)-2*nu*nu*I).max())
assert maxidentity<1e-12 and maxpositive<1e-12 and maxgamma<1e-12 and maxmixture<1e-12 and maxcoherent<1e-12
# Two-attempt exact rejection sampler for weights1,2,3, total6 in3 bits.
w=[1,2,3];joint=[F(0)]*3;abort=F(0)
for a in range(8):
 for b in range(8):
  accepted=a if a<6 else (b if b<6 else None)
  if accepted is None:abort+=F(1,64);continue
  cat=0 if accepted<1 else (1 if accepted<3 else 2);joint[cat]+=F(1,64)
assert abort==F(1,16) and all(joint[j]==(1-abort)*F(w[j],6) for j in range(3))
# Role-specific post-role abort is NOT a neutral loss extension.
p=F(1,3);s=F(2,9);a=F(4,9);delta=F(1)
probe_mean=p*delta/p;actual_stopped_loss=(p+(s+a)/2)*delta
assert probe_mean!=actual_stopped_loss
# Prefetch neutral abort before role fixes equality.
neutral=F(1,4);prefetch_probe=(1-neutral)*p*delta/p;prefetch_loss=(1-neutral)*delta
assert prefetch_probe==prefetch_loss
out={'scope':'Independent floating operator fixtures plus exact rational sampler-order counterexample/fix; not hardware execution.','operator_fixtures':50,'adjoint_vs_commutator_residual':maxidentity,'effect_positivity_upper2_residual':maxpositive,'gamma_operator_bound_residual':maxgamma,'mixture_linearity_residual':maxmixture,'coherent_quadratic_operator_residual':maxcoherent,'candidate_sampler_exact':{'abort':str(abort),'joint_accept_candidates':[str(x) for x in joint]},'post_role_abort_counterexample':{'importance_probe_mean':str(probe_mean),'actual_stopped_loss':str(actual_stopped_loss)},'neutral_prefetch_fixed':{'importance_mean':str(prefetch_probe),'stopped_loss':str(prefetch_loss)}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
