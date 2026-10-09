"""Exploratory quantum-channel BKM probe. Numerical evidence only."""
import numpy as np
from scipy.linalg import eigh,null_space
from bsc_quantum_probe import BASIS as PB
BASIS=np.array([np.kron(x,y) for x in PB for y in PB])
TR=np.zeros((4,16))
for i in range(4):TR[i,4*i]=np.sqrt(2)
Q=np.eye(16)[:,1:]
Qfixed=null_space(TR)
def bkm4(a,basis=BASIS):
 lam,v=eigh(a)
 if lam.min()<=0:raise ValueError('Nonfaithful')
 d=lam[:,None]-lam[None,:]
 with np.errstate(divide='ignore',invalid='ignore'):f=(np.log(lam[:,None])-np.log(lam[None,:]))/d
 small=np.abs(d)<1e-9*np.maximum(lam[:,None],lam[None,:]);f[small]=(2/(lam[:,None]+lam[None,:]))[small]
 b=np.einsum('ij,bjk,kl->bil',v.conj().T,basis,v)
 return np.einsum('bij,ij,cij->bc',b.conj(),f,b).real

def ratio(a,lamb=-1/3,fixed=False):
 r=np.trace(a.reshape(2,2,2,2),axis1=1,axis2=3)
 out=lamb*a+(1-lamb)*np.kron(r,np.eye(2)/2)
 n=np.diag([1 if j%4==0 else lamb for j in range(16)])
 gr=TR.T@bkm4(r,PB)@TR
 gi=bkm4(a)-gr;go=n@bkm4(out)@n-gr
 q=Qfixed if fixed else Q
 gi=q.T@gi@q;go=q.T@go@q
 w,v=eigh(gi);keep=w>max(1e-9,1e-10*w.max())
 t=v[:,keep]/np.sqrt(w[keep]);val=eigh(t.T@go@t,eigvals_only=True)
 return val[-1]
if __name__=='__main__':
 rng=np.random.default_rng(559143);best=(0,None);bestc=0
 for it in range(4500):
  z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));u,_=np.linalg.qr(z)
  lam=10**rng.uniform(-8,0,size=4);lam/=lam.sum();a=(u*lam)@u.conj().T
  try:v=ratio(a);vc=ratio(a,fixed=True)
  except Exception:continue
  if best[0]<v<1.001:best=(v,a)
  if bestc<vc<1.001:bestc=vc
 print('universal NOT best conditional',best[0],'fixed',bestc)
 np.savez('/mnt/data/adaptive_foundational_research_20261009/quantum_depolarizing_best.npz',conditional_ratio=best[0],fixed_ratio=bestc,state=best[1])
