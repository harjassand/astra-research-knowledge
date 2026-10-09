import numpy as np
from scipy.optimize import minimize
from search_pyramid_squash import masks,ent,h

def calc(x,ms):
 d,m,k,_=ms.shape;a=x[:m]+1j*x[m:];v=np.einsum('a,iajk->ijk',a,ms);v/=np.linalg.norm(v[0])
 rb=np.einsum('ijk,ilk->ijl',v,v.conj());re=np.einsum('ikj,ikl->ijl',v,v.conj());avge=np.mean([ent(r) for r in rb])
 cmi=2*np.log2(d)-ent(rb.mean(axis=0))-ent(re.mean(axis=0))+2*avge
 return cmi
rng=np.random.default_rng(551)
for d in [3,4,6,8,12,20,32]:
 ms=masks(d,True);ms-=ms.mean(axis=0)[None];m=ms.shape[1];target=h([1/d,1-1/d])+np.log2(d/(d-1))
 for it in range(12):
  x=rng.normal(size=2*m);res=minimize(lambda x:calc(x,ms),x,method='BFGS',options={'maxiter':200,'gtol':1e-7})
  print(d,it,res.fun,target,res.fun-target,flush=True)
