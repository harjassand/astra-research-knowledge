import numpy as np
from scipy.optimize import minimize
P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])];basis=np.array([np.kron(x,y)/2 for i,x in enumerate(P) for j,y in enumerate(P) if i+j]);bb=np.trace(basis.reshape(15,2,2,2,2),axis1=2,axis2=4);ee=np.trace(basis.reshape(15,2,2,2,2),axis1=1,axis2=3)
def metric(r,Ds,sld=False):
 w,u=np.linalg.eigh(r);w=np.maximum(w,1e-14); ws=w[:,None];wt=w[None,:]
 if sld:g=2/(ws+wt)
 else:
  dw=ws-wt;g=np.divide(np.log(ws)-np.log(wt),dw,out=2/(ws+wt),where=abs(dw)>1e-12)
 z=np.einsum('ia,xij,jb->xab',u.conj(),Ds,u)
 return np.einsum('xij,ij,yij->xy',z.conj(),g,z).real

def calc(v,ret=False):
 z=v[:16]+1j*v[16:];z=z.reshape(4,4);r=z@z.conj().T;r/=np.trace(r);b=np.trace(r.reshape(2,2,2,2),axis1=1,axis2=3);e=np.trace(r.reshape(2,2,2,2),axis1=0,axis2=2)
 K=metric(b,bb)+metric(e,ee)-metric(r,basis)-metric(r,basis,True)
 w,u=np.linalg.eigh(K)
 return (w[-1],r,u[:,-1]) if ret else -w[-1]
for j in range(100):
 v=np.random.randn(32);a=calc(v)
 r=minimize(calc,v,method='BFGS',options={'maxiter':500,'gtol':1e-6})
 print(j,-r.fun,flush=True)
 if r.fun < -1e-5:
  w,rho,d=calc(r.x,True);np.savez('/workspace/shared/broadcast_inequality/metric_counter.npz',rho=rho,D=np.einsum('x,xij->ij',d,basis),w=w);print('FOUND',flush=True);break
