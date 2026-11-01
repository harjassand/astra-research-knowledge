import numpy as np
from scipy.linalg import eigvals

def run(w,eta,reverse=1,kdump=1):
 g=1.;D=1/eta;nb=2*w;d=2*nb
 A=np.diag(np.full(w-1,D))+np.diag(np.ones(w-2),1)+np.diag(np.ones(w-2),-1)
 Ai=np.linalg.inv(A);J=-Ai[-1,0];shift=Ai[0,0];h=np.sqrt(reverse*abs(J)*kdump)/2
 H=np.zeros((d,d));jumps=[]
 for c in range(2):
  o=c*nb
  for j in range(1,w):H[o+j,o+j]=D
  H[o,o]=H[o+w,o+w]=shift
  for j in range(w):H[o+j,o+j+1]=H[o+j+1,o+j]=1
  H[o,o+w]=H[o+w,o]=-(-1)**c*J
  L=np.zeros((d,d));L[(1-c)*nb,o+w]=np.sqrt(abs(J));jumps.append(L)
  for j in range(1,w):
   dump=o+w+j;H[dump,dump]=D
   H[dump,o+j]=H[o+j,dump]=h
   L=np.zeros((d,d));L[o+j-1,dump]=np.sqrt(kdump);jumps.append(L)
 I=np.eye(d);K=-1j*(np.kron(I,H)-np.kron(H.T,I))
 for L in jumps:
  A=L.T@L;K+=np.kron(L,L)-.5*np.kron(I,A)-.5*np.kron(A.T,I)
 es=eigvals(K);rates=sorted([-x.real for x in es if -x.real>abs(J)*1e-9])
 M=K.copy();b=np.zeros(d*d,complex);M[0,:]=I.reshape(-1,order='F');b[0]=1
 rho=np.linalg.lstsq(M,b,rcond=None)[0].reshape((d,d),order='F')
 return dict(w=w,eta=eta,d=d,J=J,gap_over_J=rates[0]/abs(J),wrong_cache=np.trace(rho[nb:,nb:]).real,dump_flux_over_J=sum(kdump*rho[c*nb+w+j,c*nb+w+j].real for c in range(2) for j in range(1,w))/abs(J),zero_modes=int(sum(abs(es)<abs(J)*1e-8)))
if __name__=='__main__':
 import json
 for eta in [.03,.05,.1,.2]:print(json.dumps(run(4,eta)),flush=True)
