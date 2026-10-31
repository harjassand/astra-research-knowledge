"""Small finite-matrix diagnostics, not a compiler implementation."""
import numpy as np, json
from scipy.linalg import expm, eigvalsh
from pathlib import Path
r,L=2,3
occ=[(i,j) for i in range(L+1) for j in range(L+1-i)]
d=len(occ); idx={x:i for i,x in enumerate(occ)}
a=[]
for mode in range(r):
 x=np.zeros((d,d),complex)
 for j,n in enumerate(occ):
  if n[mode]:
   m=list(n);m[mode]-=1;x[idx[tuple(m)],j]=np.sqrt(n[mode])
 a.append(x)
I=np.eye(2);sx=np.array([[0,1],[1,0]],complex);sm=np.array([[0,1],[0,0]],complex)
F=[.7*sx,.9*sm];g2=sum(np.linalg.norm(f,2)**2 for f in F)
N=np.kron(I,np.diag([sum(n) for n in occ])); D=2*d
R=sum(np.kron(f,x.conj().T) for f,x in zip(F,a))
# Mode removal retains its Kraus index; compare its aggregate norm.
V=np.vstack([np.kron(I,x) for x in a])
inv=np.diag([1/np.sqrt(x) if x else 0 for x in np.diag(N)])
Vm=V@inv
P=(N!=0).astype(float)
stack_error=np.linalg.norm(Vm.conj().T@Vm-P,2)
sector=[]
for n in range(L):
 ids=np.where(np.diag(N)==n)[0]
 sector.append(float(np.linalg.norm(R[:,ids],2)/(np.sqrt(g2*(n+1)))))
number=np.diag([n[0] for n in occ]); hopping=a[0].conj().T@a[1]+a[1].conj().T@a[0]
Hf=np.kron(.3*sx,np.eye(d))+np.kron(I,.8*number@(number-np.eye(d))+.4*hopping)
H=Hf+R+R.conj().T;lam=5.;T=.3;theta=.4
J=[2*np.sqrt(lam)*np.kron(I,x) for x in a]
Id=np.eye(D)
Gen=-1j*(np.kron(Id,H)-np.kron(H.T,Id))
for j in J:
 jj=j.conj().T@j
 Gen+=np.exp(theta)*np.kron(j.conj(),j)-.5*(np.kron(Id,jj)+np.kron(jj.T,Id))
rho=np.zeros((D,D),complex);rho[0,0]=1
out=(expm(T*Gen)@rho.reshape(-1,order='F')).reshape(D,D,order='F')
mgf=float(np.trace(out).real); bound=float(np.exp(g2/lam*T*(np.exp(theta)-1)))
result={'model':'2 modes,total cutoff3,non-Hermitian noncommuting system couplings,Kerr and hopping','removal_isometry_error':float(stack_error),'raising_sector_norm_ratios':sector,'max_eigenvalue_RRdagger_minus_g2N':float(eigvalsh(R@R.conj().T-g2*N)[-1]),'free_number_commutator_norm':float(np.linalg.norm(Hf@N-N@Hf,2)),'tilted_count_mgf':mgf,'count_bound':bound,'passed':bool(stack_error<1e-12 and max(sector)<=1+1e-12 and mgf<=bound+1e-12)}
print(json.dumps(result,indent=2));Path(__file__).with_name('graded_sector_bounds.json').write_text(json.dumps(result,indent=2)+'\n')
