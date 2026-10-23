import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,time,json
from scipy.linalg import expm,null_space
from scipy.special import logsumexp
from scipy.optimize import minimize
from itertools import permutations
st=time.perf_counter();cpu=time.process_time();rng=np.random.default_rng(33443);q=8
Ge=np.zeros((q,q))
for j in range(q):
 for bit in range(3):Ge[j,j]+=.5;Ge[j,j^(1<<bit)]+=.5
perms=np.array(list(permutations(range(q))),dtype=np.int8)
Gps=np.unique(Ge[perms[:,:,None],perms[:,None,:]].reshape(-1,64),axis=0).reshape(-1,8,8)
Q=null_space(np.ones((1,8)));Gs=np.einsum('ai,nab,bj->nij',Q,Gps,Q)
F=Gs.reshape(-1,49)
def gram(U):
 G=np.zeros((8,8))
 for bit in range(3):
  r=[]
  for j in range(q):
   f=np.moveaxis(U[:,j].reshape(2,2,2),bit,0).reshape(2,4);r.append(f.conj().T@f)
  r=np.array(r).reshape(8,16);G+=.5*(r.conj()@r.T).real
 return G
best=-10;cases=0
for k in range(60):
 z=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));h=z+z.conj().T
 U=expm(1j*(.005,.03,.1,.3,1)[k%5]*h);G=gram(U);A=Q.T@G@Q
 Y=rng.normal(size=(7,4));Y/=np.linalg.norm(Y)
 for temp in [.01,.001,.0001]:
  def obj(y):
   Y=y.reshape(7,4);n=np.sum(Y*Y);Z=Y@Y.T/n;s=F@Z.ravel();ls=logsumexp(s/temp);w=np.exp(s/temp-ls);val=np.sum(A*Z)-temp*ls
   M=A-(w@F).reshape(7,7);grad=2*(M-np.sum(M*Z)*np.eye(7))@Y/n
   return -val,-grad.ravel()
  res=minimize(obj,Y.ravel(),jac=True,method='L-BFGS-B',options={'maxiter':100,'ftol':1e-12,'gtol':1e-8});Y=res.x.reshape(7,4)
 Z=Y@Y.T/np.sum(Y*Y);gap=np.sum(A*Z)-np.max(F@Z.ravel());cases+=1
 if gap>best:
  best=gap;print(k,gap,flush=True)
  np.savez(os.path.join(os.path.dirname(__file__),'q8_dual_best.npz'),U=U,G=G,Z=Q@Z@Q.T,gap=gap)
 if gap>1e-5 or time.process_time()-cpu>23:break
print(json.dumps({'graphs':len(Gps),'cases':cases,'best':best,'wall':time.perf_counter()-st,'cpu':time.process_time()-cpu}))
