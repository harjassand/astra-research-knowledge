import numpy as np
import cvxpy as cp
from math import sin,cos
import argparse,time

def ptS(A,ds,dm):return np.einsum('aiaj->ij',A.reshape(ds,dm,ds,dm))
def power_psd(A,p,tol=1e-12):
 e,V=np.linalg.eigh((A+A.conj().T)/2)
 z=np.zeros_like(e);mask=e>tol;z[mask]=e[mask]**p
 return (V*z)@V.conj().T

def channel(k,theta):
 # sites: bus E first, source S second, receiver sites following
 n=k+1; d=2**n; W=np.eye(2*d,dtype=complex)
 for j in range(1,n+1):
  perm=np.arange(2*d)
  for b in range(2*d):
   if ((b>>n)&1)!=((b>>(n-j))&1):perm[b]=b^(1<<n)^(1<<(n-j))
  W=cos(theta)*W+1j*sin(theta)*W[perm,:]
 K=[W[a*d:(a+1)*d,b*d:(b+1)*d]/np.sqrt(2) for a in range(2) for b in range(2)]
 # row-major vectorization
 T=sum(np.kron(Ki,Ki.conj()) for Ki in K)
 return T

def initial(k,name):
 z=np.array([1,0],complex);x=np.array([1,1],complex)/np.sqrt(2);y=np.array([1,1j],complex)/np.sqrt(2)
 if name=='triad':seq=[z,x,y]
 elif name=='zx':seq=[z,x]
 elif name=='z':seq=[z]
 else:raise ValueError(name)
 psi=np.array([1.],complex)
 for i in range(k):psi=np.kron(psi,seq[i%len(seq)])
 return np.outer(psi,psi.conj())

def eval_channel(T,k,theta,N,name):
 m=2**k;d=2*m
 pauli=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
 sigma0=initial(k,name)
 A=np.stack([(np.kron(P/2,sigma0)).reshape(-1) for P in pauli],axis=1)
 Q=np.linalg.matrix_power(T,N)@A
 rho=[ptS(Q[:,mu].reshape(d,d),2,m) for mu in range(4)]
 inv=power_psd(rho[0],-.25)
 a=sum(np.linalg.norm(inv@r@inv,'fro')**2 for r in rho[1:])/3
 choi=sum(np.kron(P.T,r) for P,r in zip(pauli,rho))/2
 choi=(choi+choi.conj().T)/2
 Z=cp.Variable((m,m),hermitian=True)
 prob=cp.Problem(cp.Minimize(cp.real(cp.trace(Z))/2),[cp.kron(np.eye(2),Z)-choi>>0])
 prob.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=200)
 print('k',k,'theta',theta,'N',N,'Ntheta4',N*theta**4,'frame',name,'a',a,'Fe_opt',prob.value,'chmineig',np.linalg.eigvalsh(choi)[0],'trace',np.trace(choi).real,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--k',type=int,nargs='+',default=[2,3]);p.add_argument('--theta',type=float,nargs='+',default=[.2,.1,.05]);p.add_argument('--t',type=float,nargs='+',default=[.1,.3,1.,3.,10.]);p.add_argument('--frame',default='triad');a=p.parse_args()
 for k in a.k:
  for th in a.theta:
   T=channel(k,th)
   for t in a.t:
    N=round(t/th**4);eval_channel(T,k,th,N,a.frame)
