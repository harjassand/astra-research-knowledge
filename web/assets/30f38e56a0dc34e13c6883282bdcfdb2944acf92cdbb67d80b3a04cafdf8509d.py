import numpy as np
rng=np.random.default_rng(77)
def h(x):
 x=np.clip(x,1e-15,1-1e-15);return -(x*np.log2(x)+(1-x)*np.log2(1-x))
def S(x):
 x=np.linalg.eigvalsh(x);x=x[x>1e-15];return -x@np.log2(x)
def eval(L,K):
 r=L@L.T;r/=np.trace(r);s=K@K.T;s/=np.trace(s)
 a,U=np.linalg.eigh(r);b,V=np.linalg.eigh(s);a=np.maximum(a,1e-15);b=np.maximum(b,1e-15);O=(U.T@V)**2
 c=np.sum(np.sqrt(a[:,None]*b[None,:])*O)
 j=.5*np.sum(O*(a[:,None]*np.log2(2*a[:,None]/(a[:,None]+b[None,:]))+b[None,:]*np.log2(2*b[None,:]/(a[:,None]+b[None,:]))))
 js=S((r+s)/2)-(S(r)+S(s))/2
 return 2*js-h((1+c)/2)-j
best=-1
for d in [2,3,4,8,16]:
 for k in range(1000):
  L=rng.normal(size=(d,d));K=rng.normal(size=(d,d))
  v=eval(L,K)
  if v>best:best=v
  if v>1e-8:print('VIOLATION',d,k,v);break
 print(d,best,flush=True)
from scipy.optimize import minimize
for d in [2,3,4]:
 for k in range(20):
  x=rng.normal(size=2*d*d)
  out=minimize(lambda x:-eval(*x.reshape(2,d,d)),x,method='BFGS',options={'maxiter':200,'gtol':1e-7})
  print('opt',d,k,-out.fun,flush=True)
  if -out.fun>1e-7:
   np.savez('/workspace/shared/broadcast_inequality/spectral_measurement_violation.npz',x=out.x,d=d,v=-out.fun)
   raise SystemExit
