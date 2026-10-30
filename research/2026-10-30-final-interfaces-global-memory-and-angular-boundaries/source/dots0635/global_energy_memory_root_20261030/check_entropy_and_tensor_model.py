"""Finite operator diagnostics only, not a Tanner/native-graph simulation."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(3102026)
def random_u(d):
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); q,r=np.linalg.qr(z); return q@np.diag(np.diag(r)/np.abs(np.diag(r)))
def state(d,trace=1.):
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); r=z@z.conj().T; return trace*r/np.trace(r)
def diss(k,o):
 p=k.conj().T@k; return k.conj().T@o@k-(p@o+o@p)/2
def sop(fun,d):
 out=[]
 for j in range(d*d):
  e=np.zeros(d*d,complex);e[j]=1;out.append(fun(e.reshape(d,d)).reshape(-1))
 return np.stack(out,axis=1)
# Noncommuting state/CP map; E commutes G, as required by actual scalar proof.
s=.7; E=np.kron(np.diag([0,1]),np.eye(3))+np.kron(np.eye(2),np.diag([0,0,2]))
Gc=expm(np.array([[.2,.13,0],[.13,.1,0],[0,0,.3]],complex));G=np.kron(np.eye(2),Gc)
VG=G@expm(s*E);gN=float(np.log(np.linalg.eigvalsh(G).max()))
Us=[random_u(6) for _ in range(3)];pr=np.array([.2,.3,.5])
T=lambda o:sum((p*u.conj().T@o@u for p,u in zip(pr,Us)),np.zeros_like(o))
F=T(VG); EV=T(E@VG)
slacks=[]
for _ in range(100):
 rho=state(12,float(rng.uniform(.05,1)))
 x=float(np.trace(np.kron(F,np.eye(2))@rho).real)
 y=float(np.trace(np.kron(EV,np.eye(2))@rho).real)
 rhs=x*(np.log(x)-gN)/s
 slacks.append(y-rhs)
assert min(slacks)>-1e-11
# Exact finite-rate three-phase controller, two independent cells plus common bath.
g=.3;kap=.7;H=np.array([[0,g,0],[g,0,g],[0,g,0]],complex)
a=np.zeros((3,3),complex);a[0,2]=np.sqrt(kap);A=a.conj().T@a
kill=lambda o:1j*(H@o-o@H)-(A@o+o@A)/2
R=np.linalg.solve(sop(kill,3),-np.eye(3).reshape(-1)).reshape(3,3);R=(R+R.conj().T)/2
Rmax=2*np.linalg.eigvalsh(R).max();beta=.3/Rmax;S=(1-beta*Rmax)*np.eye(3)+beta*R
U=np.diag([0,1]);V=np.diag([1,np.exp(s)]);d=V-np.eye(2)
Fi=np.eye(6)+np.kron(d,S);TiEV=np.kron(np.exp(s)*U,S)
Hi=np.kron(np.eye(2),H); Ks=[np.array([[1,0],[0,0]],complex),np.array([[0,1],[0,0]],complex)]
Ji=[np.kron(k,a) for k in Ks]
FG=np.kron(Fi,Fi); TEG=np.kron(TiEV,Fi)+np.kron(Fi,TiEV)
Htot=np.kron(Hi,np.eye(6))+np.kron(np.eye(6),Hi)
Jtot=[np.kron(j,np.eye(6)) for j in Ji]+[np.kron(np.eye(6),j) for j in Ji]
LF=1j*(Htot@FG-FG@Htot)+sum((diss(j,FG) for j in Jtot),np.zeros_like(FG))
lam=beta*(1-np.exp(-s)); max_clean=float(np.linalg.eigvalsh((LF+lam*TEG+ (LF+lam*TEG).conj().T)/2).max())
assert max_clean<1e-10
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);Xcell=np.kron(X,np.eye(3));eta=.001
Hnoise=eta*np.kron(np.kron(Xcell,np.eye(6))+np.kron(np.eye(6),Xcell),Z)
Fb=np.kron(FG,np.eye(2)); Nb=1j*(Hnoise@Fb-Fb@Hnoise)
C=2*np.exp(s/2); residual=np.kron(LF+lam*TEG,np.eye(2))+Nb-C*eta*2*Fb
max_noisy=float(np.linalg.eigvalsh((residual+residual.conj().T)/2).max());assert max_noisy<1e-10
report={'scope':'scalar entropy and exact tensor-clock operator checks; not a native Tanner proof','jensen_samples':100,'minimum_jensen_slack':min(slacks),'gramian_residual':float(np.linalg.norm(kill(R)+np.eye(3))),'lambda':float(lam),'two_cell_clean_max_eigenvalue':max_clean,'common_bath_bound_max_eigenvalue':max_noisy}
Path(__file__).with_name('entropy_and_tensor_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
