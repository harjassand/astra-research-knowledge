"""Finite channel-plumbing checks; NOT an actual-family thermal-phase test."""
import numpy as np,scipy.linalg as la,json
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=dict(I=I,X=X,Y=Y,Z=Z)
def kron(*xs):
 a=np.array([[1.]])
 for b in xs:a=np.kron(a,b)
 return a
def word(w):return kron(*(P[a] for a in w))
def reduced(rho,keep,n):
 keep=list(keep);drop=[i for i in range(n) if i not in keep];d=2**len(keep);e=2**len(drop)
 a=rho.reshape([2]*(2*n)).transpose(keep+drop+[n+i for i in keep]+[n+i for i in drop]).reshape(d,e,d,e)
 return np.trace(a,axis1=1,axis2=3)
def power(a,z):
 ev,U=la.eigh(a);return (U*np.exp(z*np.log(ev)))@U.conj().T
def tn(a):return float(la.svdvals(a).sum())
terms=[(.7,'ZIII'),(.5,'IZII'),(.3,'IIZI'),(.6,'IIIZ'),(.2,'XXII'),(.17,'IZZI'),(.13,'IIXX'),(.09,'YIYI')]
H=sum(c*word(w) for c,w in terms);beta=1.7;rho=la.expm(-beta*H);rho/=np.trace(rho)
sigma=reduced(rho,[0,1,2],4);sigmahat=.999*sigma+.001*np.eye(8)/8;marg=reduced(sigmahat,[2],3)
Ks=[];times=[-2.,-.5,0.,.5,2.];weights=np.array([1/(np.cosh(np.pi*t)+1) for t in times]);weights/=weights.sum()
for t,wt in zip(times,weights):
 left=power(sigmahat,.5-1j*t);right=power(marg,-.5+1j*t)
 for j in range(4):
  insert=np.kron(np.eye(4)[:,j:j+1],np.eye(2));Ks.append(np.sqrt(wt)*left@insert@right)
tpres=la.norm(sum(k.conj().T@k for k in Ks)-np.eye(2));choi=sum(np.outer(k.flatten('F'),k.flatten('F').conj()) for k in Ks)
# If B is estimated inconsistently, TP generally fails.
wrong=marg+.01*Z;assert min(la.eigvalsh(wrong))>0
badKs=[]
for j in range(4):badKs.append(power(sigmahat,.5)@np.kron(np.eye(4)[:,j:j+1],I)@power(wrong,-.5))
wrongtp=la.norm(sum(k.conj().T@k for k in badKs)-I)
# Scalar Jensen/Weyl reduced-state eigenvalue bound, with actual touch norm.
Htouch=sum(c*word(w) for c,w in terms if any(a!='I' for a in w[:3]));touch_norm=la.norm(Htouch,2);lower=np.exp(-2*beta*touch_norm)/8
mineig=float(min(la.eigvalsh(sigma)))
# Commuting disjoint maps do not justify pulling trace bounds backward.
corr=np.diag([.5,0,0,.5]);resetA=lambda r:kron(np.diag([1,0]),reduced(r,[1],2));resetB=lambda r:kron(reduced(r,[0],2),I/2)
post=resetA(corr);seq=tn(resetB(post)-post);common=tn(resetB(corr)-corr)
res=dict(scope='finite four-spin Petz/precision and two-bit layer-bookkeeping test only',petz_trace_preservation_residual=float(tpres),petz_choi_min_eigenvalue=float(min(la.eigvalsh(choi))),inconsistent_marginal_TP_failure=float(wrongtp),actual_reduced_min_eigenvalue=mineig,proved_scalar_lower_bound=float(lower),sequential_prefix_reset_error=seq,common_layer_prefix_reset_error=common)
assert tpres<1e-12 and min(la.eigvalsh(choi))>-1e-12 and wrongtp>1e-5 and mineig>=lower and seq<1e-12 and common>.9
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
