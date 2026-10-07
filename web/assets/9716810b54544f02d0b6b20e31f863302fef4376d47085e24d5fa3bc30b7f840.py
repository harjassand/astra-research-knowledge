from itertools import combinations
import numpy as np
rng=np.random.default_rng(817)
def cov(w,k):
 n=len(w); xs=np.zeros((len(list(combinations(range(n),k))),n))
 for t,S in enumerate(combinations(range(n),k)):xs[t,list(S)]=1
 logp=xs@np.log(w); p=np.exp(logp-logp.max());p/=p.sum()
 mean=p@xs; C=(xs.T*p)@xs-np.outer(mean,mean)
 d=np.diag(C);B=C/np.sqrt(d[:,None]*d[None,:])
 return mean,C,np.linalg.eigvalsh(B)
worst=(2,None)
for n in range(4,12):
 for k in range(2,n-1):
  for trial in range(100):
   w=np.exp(rng.uniform(-5,5,n))
   p,C,e=cov(w,k)
   if e[1]<worst[0]:worst=(e[1],(n,k,w,e))
print('min second eigenvalue',worst[0]); print(worst[1])
