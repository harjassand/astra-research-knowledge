import numpy as np
from scipy.linalg import expm
import json

def ops(n):
 Z=np.diag([1.,-1.]);a=np.array([[0.,1.],[0.,0.]])
 out=[]
 for j in range(n):
  v=np.array([[1.]])
  for k in range(n):v=np.kron(v,Z if k<j else a if k==j else np.eye(2))
  out.append(v.astype(complex))
 return out

def gammas(a):return [g for c in a for g in (c+c.conj().T,-1j*(c-c.conj().T))]
def cov(g,psi):return np.array([[(1j*np.vdot(psi,gi@gj@psi)).real if i!=j else 0 for j,gj in enumerate(g)]for i,gi in enumerate(g)])
rng=np.random.default_rng(8);out=[]
for n in [1,2,3]:
 a=ops(n);g=gammas(a);aa=ops(2*n);gg=gammas(aa);dim=2**(2*n)
 vac=np.eye(2**n,dtype=complex)[:,0]
 bell=np.eye(dim,dtype=complex)[:,0]
 for j in range(n):bell=(bell+aa[j].conj().T@aa[n+j].conj().T@bell)/np.sqrt(2)
 C=np.kron(np.eye(n),-np.array([[0.,1.],[1.,0.]]));S=np.block([[np.eye(2*n),np.zeros((2*n,2*n))],[np.zeros((2*n,2*n)),C]])
 Nb=sum(c.conj().T@c for c in a);phase=expm(-1j*np.pi*Nb/2)
 for it in range(5):
  A=rng.normal(size=(2*n,2*n));A=(A-A.T)/2
  gen=sum(A[i,j]*g[i]@g[j]/4 for i in range(2*n)for j in range(2*n))
  psi=expm(gen)@vac;G=cov(g,psi)
  Ap=np.block([[np.zeros_like(G),-G],[-G,np.zeros_like(G)]])
  K=S.T@Ap@S*np.pi/4
  lift=sum(K[i,j]*gg[i]@gg[j]/4 for i in range(4*n)for j in range(4*n))
  prepared=expm(lift)@bell
  target=np.kron(psi,phase@psi.conj())
  ov=np.vdot(target,prepared)
  out.append({'n':n,'trial':it,'overlap_real':float(ov.real),'overlap_imag':float(ov.imag),'norm_error':float(np.linalg.norm(prepared-target))})
print(out)
json.dump(out,open('producer-workspace/root_gaussian_purification_check.json','w'),indent=2)
