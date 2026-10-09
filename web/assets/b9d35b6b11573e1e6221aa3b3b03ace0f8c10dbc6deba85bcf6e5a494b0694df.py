"""Numerical check of fixed-marginal conditional contraction, not proof."""
import numpy as np
from scipy.linalg import null_space,eigh
from bsc_quantum_probe import BASIS,bkm

def ratio(blocks,w):
 k=len(blocks);r=4;Q=null_space(np.tile(np.eye(r),(1,k)))
 gs=[bkm(x) for x in blocks];out=np.einsum('xy,xij->yij',w,blocks);gy=[bkm(x) for x in out]
 gi=np.zeros((k*r,k*r));go=np.zeros_like(gi)
 for i in range(k):
  gi[i*r:(i+1)*r,i*r:(i+1)*r]=gs[i]
  for j in range(k):go[i*r:(i+1)*r,j*r:(j+1)*r]=sum(w[i,y]*w[j,y]*gy[y] for y in range(w.shape[1]))
 val,vec=eigh(Q.T@go@Q,Q.T@gi@Q)
 return val[-1],Q@vec[:,-1]
if __name__=='__main__':
 rng=np.random.default_rng(77234);W=(np.ones((3,3))-np.eye(3))/2;best=(0,None)
 for it in range(10000):
  p=rng.dirichlet(np.ones(3)*.5);blocks=[]
  for j in range(3):
   n=rng.normal(size=3);n/=np.linalg.norm(n);rad=1-10**rng.uniform(-7,0)
   blocks.append(p[j]*(np.eye(2)+rad*np.einsum('a,aij->ij',n,BASIS[1:])*np.sqrt(2))/2)
  blocks=np.array(blocks)
  val,d=ratio(blocks,W)
  if best[0]<val<1.001:best=(val,blocks)
 print('best fixed marginal ratio',best[0]);np.savez('/mnt/data/adaptive_foundational_research_20261009/fixed_marginal_best.npz',ratio=best[0],blocks=best[1])
