import numpy as np
from scipy.sparse import csc_matrix,eye,kron
from scipy.sparse.linalg import spsolve
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);Id=np.eye(4)
P=[[np.kron(Z,I),np.kron(I,Z)],[np.kron(X,I),np.kron(I,X)]];phi=np.array([1,0,0,1])/np.sqrt(2)
Q=[[Id,p[0],p[1]@p[0],Id] for p in P]
states=[(a,b) for a in range(8) for b in range(8)];n=len(states)
G=[Q[0][a%4]@Q[1][b%4] for a,b in states]
def scalar(m,B,j):return (phi@G[m].T@B@G[j]@phi).real

def run(eta,poisson=False):
 D=1/eta;J=-1/D;shift=1/D;kappa=abs(J);kdump=1;h=np.sqrt(abs(J)*kdump)/2
 H=np.zeros((n,n));jumps=[]
 for a in range(2):
  for c in range(2):
   L=np.zeros((n,n));R=np.zeros((n,n))
   for j,r in enumerate(states):
    if r[a]//4!=c:continue
    q=r[a]%4
    H[j,j]+=D if q in [1,3] else shift
    if q<2:
     rr=list(r);rr[a]+=1;m=states.index(tuple(rr));x=scalar(m,P[a][q],j)
     H[m,j]+=x;H[j,m]+=x
    if q==0:
     rr=list(r);rr[a]+=2;m=states.index(tuple(rr));x=-(-1)**c*J*scalar(m,Id,j)
     H[m,j]+=x;H[j,m]+=x
    if q==2:
     rr=list(r);rr[a]=(1-c)*4;m=states.index(tuple(rr));L[m,j]=np.sqrt(kappa)*scalar(m,Id,j)
    if q==1:
     rr=list(r);rr[a]+=2;m=states.index(tuple(rr));x=h*scalar(m,P[a][0],j)
     H[m,j]+=x;H[j,m]+=x
    if q==3:
     rr=list(r);rr[a]=c*4;m=states.index(tuple(rr));R[m,j]=np.sqrt(kdump)*scalar(m,Id,j)
   jumps.extend([L,R])
 H=csc_matrix(H);Eye=eye(n,format='csc');K=-1j*(kron(Eye,H)-kron(H.T,Eye))
 for l in jumps:
  L=csc_matrix(l);A=L.T@L;K+=kron(L,L)-.5*kron(Eye,A)-.5*kron(A.T,Eye)
 KK=K.tocsc().copy()
 K=K.tolil();b=np.zeros(n*n,complex);K[0,:]=np.eye(n).reshape(-1,order='F');b[0]=1
 rho=spsolve(K.tocsc(),b).reshape((n,n),order='F');probs=np.diag(rho).real
 result=dict(eta=eta,bad1=sum(p for p,r in zip(probs,states) if r[0]//4==1),bad2=sum(p for p,r in zip(probs,states) if r[1]//4==1),intermediate=sum(p*((r[0]%4==1)+(r[1]%4==1)) for p,r in zip(probs,states)),dump_flux_over_J=sum(p*((r[0]%4==3)+(r[1]%4==3)) for p,r in zip(probs,states))/abs(J),minprob=min(probs),trace=np.trace(rho).real)
 if poisson:
  F=np.diag([int(r[0]//4==1)+int(r[1]//4==1) for r in states]);f=np.trace(rho@F).real
  A=(KK.conj().T/abs(J)).tolil();rhs=-(F-f*np.eye(n)).reshape(-1,order='F');A[0,:]=rho.T.reshape(-1,order='F');rhs[0]=0
  zz=spsolve(A.tocsc(),rhs).reshape((n,n),order='F');zz=(zz+zz.conj().T)/2;ev=np.linalg.eigvalsh(zz)
  result.update(cache_poisson_range=float(ev[-1]-ev[0]),cache_poisson_min=float(ev[0]),cache_poisson_max=float(ev[-1]))
 return result
if __name__=='__main__':
 import json
 for eta in [.03,.05,.1,.2]:print(json.dumps(run(eta)),flush=True)
