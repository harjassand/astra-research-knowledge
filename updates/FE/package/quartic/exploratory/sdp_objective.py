"""Exploratory ADMM on the exact acoustic Gram cone; NOT an exact certificate."""
import numpy as np
from scipy.linalg import null_space
from objective_quartic import M11,M12,M22,pars
n=8
ix=np.triu_indices(n); weights=np.where(ix[0]==ix[1],1.,np.sqrt(2))
def sv(M):return M[ix]*weights
def sm(v):
 M=np.zeros((n,n));M[ix]=v/weights; M[(ix[1],ix[0])]=v/weights;return M
Bs=[]
for p in pars:
 ms=[np.array(M.diff(p)).astype(float) for M in [M11,M12,M22]]
 Bs.append(np.block([[ms[0],ms[1]],[ms[1],ms[2]]]))
for i in range(4):
 for j in range(i+1,4):
  k=np.zeros((4,4));k[i,j]=1;k[j,i]=-1
  Bs.append(np.block([[np.zeros((4,4)),k],[-k,np.zeros((4,4))]]))
B=np.column_stack([sv(m) for m in Bs]); Bpin=np.linalg.pinv(B)
# Subspace projection and unit trace slice.
from scipy.linalg import qr
U=np.linalg.qr(B)[0]
Proj=U@U.T
tr=sv(np.eye(n));t=Proj@tr; tt=t@t
x0=t/tt
P=Proj-np.outer(t,t)/tt

def solve(m, steps=10000,tol=1e-9,rho=1.,init=None):
 """Minimize m.p subject acoustic Gram PSD, trace=1."""
 obj=np.r_[m,np.zeros(6)];c=Bpin.T@obj
 if init is None:y=x0.copy();z=np.zeros_like(y)
 else:y,z=init
 for it in range(steps):
  x=x0+P@(y-z-c/rho)
  lam,vec=np.linalg.eigh(sm(x+z));yp=sv((vec*np.maximum(lam,0))@vec.T)
  z+=x-yp
  primal=np.linalg.norm(x-yp);dual=rho*np.linalg.norm(yp-y);y=yp
  if it%100==0 and primal<tol and dual<tol:break
 p=Bpin@x
 return dict(p=p[:9],k=p[9:],Q=sm(x),min_eig=np.linalg.eigvalsh(sm(x))[0],value=float(m@p[:9]),primal=primal,dual=dual,it=it,state=(y,z))

if __name__=='__main__':
 rng=np.random.default_rng(20261014)
 for z in range(5):
  m=rng.normal(size=9);r=solve(m)
  print(z,r['value'],r['min_eig'],r['primal'],r['dual'],r['it'],np.round(r['p'],5),flush=True)
