import numpy as np
from sdp_objective import solve

def basis(x):
 a,b,c,d=np.moveaxis(x,-1,0)
 u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
 return np.array([u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]).T

def moments(k, amps, phase, A0, N=48):
 pts=np.indices((N,N)).reshape(2,-1).T*2*np.pi/N
 R=np.einsum('ni,nj->nij',amps,k).reshape(-1,4)
 X=np.cos(pts@k.T+phase)@R+A0.reshape(4)
 return basis(X).mean(axis=0)-basis(A0.reshape(4))

if __name__=='__main__':
 rng=np.random.default_rng(77321)
 sets=[np.array([[1,0],[0,1],[1,2],[-2,-3]]),np.array([[1,0],[0,1],[1,1],[1,-1]]),np.array([[1,0],[0,1],[1,1],[1,-1],[2,1],[1,2]])]
 best=None
 for i in range(24):
  k=sets[i%3];amps=rng.normal(size=(len(k),2))/np.linalg.norm(k,axis=1)[:,None]
  phase=rng.uniform(0,6.28,len(k));A0=rng.normal(size=(2,2))*(i%3)
  m=moments(k,amps,phase,A0);r=solve(m,steps=15000,tol=1e-8)
  print(i,round(r['value'],8),r['min_eig'],r['primal'],r['dual'],r['it'],flush=True)
  if best is None or r['value']<best['value']:
   best=r;np.savez('/mnt/data/astra_meta_genesis/objective_field_best.npz',p=r['p'],K=r['k'],m=m,k=k,amps=amps,phase=phase,A0=A0,Q=r['Q'])
