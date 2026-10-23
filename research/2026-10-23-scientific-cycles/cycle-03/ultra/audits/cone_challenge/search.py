import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import time,json
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize
st=time.perf_counter();cpu=time.process_time()
rng=np.random.default_rng(33441)
H=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/2

def gram(U):
  a=[];b=[]
  for j in range(4):
    f=U[:,j].reshape(2,2)
    a.append(f@f.conj().T);b.append(f.conj().T@f)
  return np.array([[np.trace(a[j]@a[k]).real+np.trace(b[j]@b[k]).real for k in range(4)]for j in range(4)])/2

def gap(T):
  A=np.eye(3)-T
  def obj(x):return np.linalg.eigvalsh(np.diag(x)-A)[-1]
  r=minimize(obj,np.ones(3)/3,method='SLSQP',bounds=[(0,1)]*3,constraints=[{'type':'eq','fun':lambda x:sum(x)-1}],options={'maxiter':70,'ftol':1e-10})
  return r.fun,r.x
best=(-1,None);cases=0
for k in range(400):
  z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));h=z+z.conj().T
  scale=(.001,.01,.1,.3,1,3)[k%6]
  U=expm(1j*scale*h)
  G=gram(U);T=H.T@G@H
  g,w=gap(T);cases+=1
  if g>best[0]:
    best=(g,(U,G,T,w));print(k,g,flush=True) if g>1e-5 else None
  if g>1e-4:
    np.savez(os.path.join(os.path.dirname(__file__),'candidate.npz'),U=U,G=G,T=T,w=w)
    break
print(json.dumps({'cases':cases,'best':best[0],'wall':time.perf_counter()-st,'cpu':time.process_time()-cpu}))
