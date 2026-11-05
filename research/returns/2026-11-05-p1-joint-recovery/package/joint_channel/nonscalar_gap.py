import numpy as np
from scipy.sparse.linalg import LinearOperator,eigsh
from pathlib import Path
HERE=Path(__file__).resolve().parent
from math import sin,cos
import argparse,time
src=(HERE / 'yangian_gap.py').read_text().split('for n in map(int,sys.argv')[0]
exec(src)

def data(n,theta):
 d=2**n; full=2*d; W=np.eye(full,dtype=complex)
 for j in range(1,n+1):
  perm=np.arange(full)
  for k in range(full):
   if ((k>>n)&1)!=((k>>(n-j))&1):perm[k]=k^(1<<n)^(1<<(n-j))
  W=cos(theta)*W+1j*sin(theta)*W[perm,:]
 K=[W[a*d:(a+1)*d,b*d:(b+1)*d]/np.sqrt(2) for a in range(2) for b in range(2)]
 Q,G=schur(n); js=sorted(set(j for j,m in G))
 def P(X):
  A=Q.T@X@Q; B=np.zeros_like(A)
  for j in js:
   C=sum(A[np.ix_(G[j,m],G[j,m])] for m in range(-j,j+1,2))/(j+1)
   for m in range(-j,j+1,2): B[np.ix_(G[j,m],G[j,m])]=C
  return Q@B@Q.T
 def T(X):return sum(k@X@k.conj().T for k in K)
 def TS(X):return sum(k.conj().T@X@k for k in K)
 def H(X):return X-T(TS(X))
 def f(v):
  X=v.reshape(d,d)
  return (H(X)+2*P(X)).reshape(-1)
 return LinearOperator((d*d,d*d),matvec=f,dtype=complex),H,P

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,nargs='+',default=[2,3,4,5,6]);p.add_argument('--theta',type=float,nargs='+',default=[.1,.2,.5,.8,1.2]);args=p.parse_args()
 for th in args.theta:
  for n in args.n:
   now=time.time();L,H,P=data(n,th)
   vals,V=eigsh(L,k=3,which='SA',tol=1e-10,maxiter=5000)
   i=np.argmin(vals);X=V[:,i].reshape(2**n,2**n)
   print('n',n,'theta',th,'beta',min(vals),'beta/theta2',min(vals)/(th*th),'scalar_error',np.linalg.norm(P(X)),'sec',time.time()-now,flush=True)
