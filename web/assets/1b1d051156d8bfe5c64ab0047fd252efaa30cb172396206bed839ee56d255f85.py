import numpy as np
from scipy.special import xlogy
from scipy.optimize import minimize
import json
from pathlib import Path

def h(x):
 x=np.maximum(np.asarray(x),0);return -np.sum(xlogy(x,x))/np.log(2)
def ent(r):return h(np.linalg.eigvalsh(r))
def cf(p,d):
 q=(1+(d-1)*p)/d
 if q<=1/d:return 0.0
 if d>2 and q>=4*(d-1)/d**2:return ((q-1)*d*np.log2(d-1)/(d-2)+np.log2(d))
 t=(np.sqrt(q)+np.sqrt((d-1)*(1-q)))**2/d
 return h([t,1-t])+(1-t)*np.log2(d-1)
def masks(d,extra):
 k=d+extra;ms=np.zeros((d,10 if extra else 5,k,k))
 for i in range(d):
  for j in range(k):
   for l in range(k):
    if j==d or l==d:
     if j==l:idx=5
     elif j==d:idx=6 if l==i else 7
     else:idx=8 if j==i else 9
    elif j==i and l==i:idx=0
    elif j==i:idx=1
    elif l==i:idx=2
    elif j==l:idx=3
    else:idx=4
    ms[i,idx,j,l]=1
 return ms

def calc(x,ms):
 d,m,k,_=ms.shape
 a=x[:m]+1j*x[m:]
 v=np.einsum('a,iajk->ijk',a,ms);v/=np.linalg.norm(v[0])
 g=np.einsum('ijk,ljk->il',v,v.conj())/d
 p=(np.trace(g@np.ones((d,d))).real-1)/(d-1)
 rb=np.einsum('ijk,ilk->ijl',v,v.conj());re=np.einsum('ikj,ikl->ijl',v,v.conj())
 avge=np.mean([ent(r) for r in rb])
 excess=ent(rb.mean(axis=0))+ent(re.mean(axis=0))-2*avge-ent(g)
 acc=np.log2(d)-cf(p,d)
 return excess-acc,p,excess,acc,avge

if __name__=='__main__':
 rng=np.random.default_rng(20261009);best=(-1e9,None)
 for d in [3,4,6,8,12]:
  ms=masks(d,True);m=ms.shape[1]
  for it in range(25):
   x=rng.normal(size=2*m)
   res=minimize(lambda z:-calc(z,ms)[0],x,method='BFGS',options={'maxiter':250,'gtol':1e-7})
   val=calc(res.x,ms)
   print(d,it,val,flush=True)
   if val[0]>best[0]:
    best=(val[0],(d,res.x.tolist(),val))
    Path('/workspace/shared/broadcast_inequality/pyramid_best.json').write_text(json.dumps(best))
