import numpy as np
from scipy.linalg import eigvals
from scipy.sparse import csc_matrix, eye, kron
from scipy.sparse.linalg import spsolve
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);Id=np.eye(4)
P=[[np.kron(Z,I),np.kron(I,Z)],[np.kron(X,I),np.kron(I,X)]]
S=[p[1]@p[0] for p in P];phi=np.array([1,0,0,1])/np.sqrt(2)
Q=[[Id,p[0],p[1]@p[0]] for p in P]
states=[(a,b) for a in range(6) for b in range(6)];n=len(states)
G=[Q[0][a%3]@Q[1][b%3] for a,b in states]
def scalar(m,B,j):return (phi@G[m].T@B@G[j]@phi).real

def run(eta,cleanup):
 assert cleanup == 0, "Intermediate cleanup changes stabilizer sector; fixed-sector reduction is invalid for it."
 D=1/eta;J=-1/D;shift=1/D;kappa=abs(J)
 H=np.zeros((n,n));jumps=[]
 for a in range(2):
  for c in range(2):
   L=np.zeros((n,n));Rs=[np.zeros((n,n))]
   for j,r in enumerate(states):
    if r[a]//3!=c:continue
    q=r[a]%3
    H[j,j]+=D if q==1 else shift
    if q<2:
     rr=list(r);rr[a]+=1;m=states.index(tuple(rr));x=scalar(m,P[a][q],j)
     H[m,j]+=x;H[j,m]+=x
    if q==0:
     rr=list(r);rr[a]+=2;m=states.index(tuple(rr));x=-(-1)**c*J*scalar(m,Id,j)
     H[m,j]+=x;H[j,m]+=x
    if q==2:
     rr=list(r);rr[a]=(1-c)*3;m=states.index(tuple(rr));L[m,j]=np.sqrt(kappa)*scalar(m,Id,j)
    if q==1:
     rr=list(r);rr[a]=c*3;m=states.index(tuple(rr));Rs[0][m,j]=np.sqrt(cleanup*kappa)*scalar(m,Id,j)
   jumps.extend([L]+Rs)
 H=csc_matrix(H);Eye=eye(n,format='csc');K=-1j*(kron(Eye,H)-kron(H.T,Eye))
 for l in jumps:
  L=csc_matrix(l);A=L.T@L;K+=kron(L,L)-.5*kron(Eye,A)-.5*kron(A.T,Eye)
 K=K.tolil();b=np.zeros(n*n,complex);K[0,:]=np.eye(n).reshape(-1,order='F');b[0]=1
 rho=spsolve(K.tocsc(),b).reshape((n,n),order='F')
 probs=np.diag(rho).real
 return dict(eta=eta,cleanup=cleanup,bad1=sum(p for p,r in zip(probs,states) if r[0]//3==1),bad2=sum(p for p,r in zip(probs,states) if r[1]//3==1),intermediate=sum(p*((r[0]%3==1)+(r[1]%3==1)) for p,r in zip(probs,states)),minprob=min(probs),trace=np.trace(rho).real)
if __name__=='__main__':
 import json
 for eta in [.05,.1,.2,.3]:
  for r in [0]:print(json.dumps(run(eta,r)),flush=True)
