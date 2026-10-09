import numpy as np
from scipy.optimize import minimize
from scipy.linalg import sqrtm
from search import S,h

def obj(v):
 z=v[:32]+1j*v[32:]; z=z.reshape(2,4,4); r=z@z.conj().transpose(0,2,1);r/=np.trace(r,axis1=1,axis2=2)[:,None,None];
 b=np.trace(r.reshape(2,2,2,2,2),axis1=2,axis2=4);e=np.trace(r.reshape(2,2,2,2,2),axis1=1,axis2=3)
 delta=S(b.mean(0))+S(e.mean(0))-S(r.mean(0))-sum(S(t) for t in b)/2-sum(S(t) for t in e)/2+sum(S(t) for t in r)/2
 w,u=np.linalg.eigh(r[0]);sq=(u*np.sqrt(np.maximum(w,0)))@u.conj().T
 f=sum(np.sqrt(np.maximum(np.linalg.eigvalsh(sq@r[1]@sq),0)));f=min(1,f)
 acc=1-h((1-np.sqrt(max(0,1-f*f)))/2)
 return -(delta-acc)
for j in range(100):
 v=np.random.randn(64);r=minimize(obj,v,method='BFGS',options={'maxiter':300,'gtol':1e-7})
 print(j,-r.fun,flush=True)
 if r.fun < -1e-7: np.save('/workspace/shared/broadcast_inequality/mixed_counter.npy',r.x);print('FOUND',flush=True);break
