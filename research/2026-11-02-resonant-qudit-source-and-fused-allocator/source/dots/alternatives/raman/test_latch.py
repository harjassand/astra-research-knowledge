import numpy as np
from scipy.linalg import eigvals

def latch(w,eta,kfactor=1,cleanup=0,s=1,poisson=False):
 g=1.;D=g/eta;d=2*(w+1)
 A=np.diag(np.full(w-1,D))+np.diag(np.full(w-2,g),1)+np.diag(np.full(w-2,g),-1)
 Ai=np.linalg.inv(A);J=-g*g*Ai[-1,0];shift=g*g*Ai[0,0]
 H=np.zeros((d,d));jumps=[]
 for c in range(2):
  o=c*(w+1)
  for j in range(1,w):H[o+j,o+j]=D
  H[o,o]=H[o+w,o+w]=shift
  for j in range(w):H[o+j,o+j+1]=H[o+j+1,o+j]=g*(s if j==w-1 else 1)
  H[o,o+w]=H[o+w,o]=-(-1)**c*J
  L=np.zeros((d,d));L[(1-c)*(w+1),o+w]=np.sqrt(kfactor*abs(J));jumps.append(L)
  for j in range(1,w):
   L=np.zeros((d,d));L[o,o+j]=np.sqrt(cleanup*abs(J));jumps.append(L)
 I=np.eye(d);K=-1j*(np.kron(I,H)-np.kron(H.T,I))
 for L in jumps:
  A=L.T@L;K+=np.kron(L,L)-.5*np.kron(I,A)-.5*np.kron(A.T,I)
 es=eigvals(K);rates=sorted([-x.real for x in es if -x.real>abs(J)*1e-9]);zeros=sum(abs(es)<abs(J)*1e-8)
 # stationarity via augmented least squares
 M=K.copy();b=np.zeros(d*d,complex);M[0,:]=np.eye(d).reshape(-1,order='F');b[0]=1
 rho=np.linalg.lstsq(M,b,rcond=None)[0].reshape((d,d),order='F')
 bad=sum(rho[j,j].real for j in range(w+1,d)) if s==1 else sum(rho[j,j].real for j in range(w+1))
 inter=sum(rho[c*(w+1)+j,c*(w+1)+j].real for c in range(2) for j in range(1,w))
 result=dict(w=w,eta=eta,J=J,kappa_over_J=kfactor,cleanup_over_J=cleanup,zero_modes=int(zeros),gap_over_J=rates[0]/abs(J),bad_cache=bad,intermediate_occupation=inter)
 if poisson:
  F=np.diag([cleanup if j%(w+1) in range(1,w) else 0 for j in range(d)])
  f=np.trace(rho@F).real
  Kadj=K.conj().T/abs(J);rhs=-(F-f*np.eye(d)).reshape(-1,order='F')
  # center by stationary state expectation, using augmented equation
  MM=np.vstack([Kadj,rho.T.reshape(-1,order='F')]);bb=np.r_[rhs,0]
  zz=np.linalg.lstsq(MM,bb,rcond=None)[0];zz=zz.reshape((d,d),order='F');zz=(zz+zz.conj().T)/2
  ev=np.linalg.eigvalsh(zz)
  result.update(poisson_range=float(ev[-1]-ev[0]),poisson_min=float(ev[0]),poisson_max=float(ev[-1]),poisson_residual=float(np.linalg.norm(Kadj@zz.reshape(-1,order='F')-rhs)))
 return result
if __name__=='__main__':
 import json
 for eta in [.1,.2,.3]:
  for k in [1,10]:
   for r in [0,.01]:print(json.dumps(latch(4,eta,k,r)))
