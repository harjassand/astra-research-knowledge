import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,time,json
from scipy.linalg import expm,null_space
from scipy.special import logsumexp
from scipy.optimize import minimize
from itertools import permutations
st=time.perf_counter();cpu=time.process_time();rng=np.random.default_rng(33444);q=8
Ge=np.zeros((q,q))
for j in range(q):
 for bit in range(3):Ge[j,j]+=.5;Ge[j,j^(1<<bit)]+=.5
perms=np.array(list(permutations(range(q))),dtype=np.int8)
Gps=np.unique(Ge[perms[:,:,None],perms[:,None,:]].reshape(-1,64),axis=0).reshape(-1,8,8)
Q=null_space(np.ones((1,8)));Gs=np.einsum('ai,nab,bj->nij',Q,Gps,Q);F=Gs.reshape(-1,49)

def calc(U,Z=None):
 G=np.zeros((8,8));grad=np.zeros_like(U)
 for bit in range(3):
  fs=[np.moveaxis(U[:,j].reshape(2,2,2),bit,0).reshape(2,4) for j in range(q)]
  rr=np.array([f.T@f.conj() for f in fs]);r=rr.reshape(8,16);G+=.5*(r.conj()@r.T).real
  if Z is not None:
   Rs=(Z@r).reshape(8,4,4)
   for j in range(8):grad[:,j]+=np.moveaxis((2*fs[j]@Rs[j].T).reshape(2,2,2),0,bit).ravel()
 return G,grad

def optimizeZ(G,Y):
 A=Q.T@G@Q;temp=.0001
 def obj(y):
  Y=y.reshape(7,4);n=np.sum(Y*Y);Z=Y@Y.T/n;s=F@Z.ravel();ls=logsumexp(s/temp);w=np.exp(s/temp-ls);val=np.sum(A*Z)-temp*ls
  M=A-(w@F).reshape(7,7);grad=2*(M-np.sum(M*Z)*np.eye(7))@Y/n
  return -val,-grad.ravel()
 res=minimize(obj,Y.ravel(),jac=True,method='L-BFGS-B',options={'maxiter':100,'ftol':1e-12});Y=res.x.reshape(7,4);Z=Y@Y.T/np.sum(Y*Y)
 return Q@Z@Q.T,Y
best=-100;outer=0
for run in range(20):
 z=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));U=expm(1j*.3*(z+z.conj().T));Y=rng.normal(size=(7,4));Y/=np.linalg.norm(Y)
 for alt in range(10):
  G,_=calc(U);Z,Y=optimizeZ(G,Y);sup=np.max(Gps.reshape(-1,64)@Z.ravel())
  for it in range(80):
   G,grad=calc(U,Z);val=np.sum(G*Z);A=grad@U.conj().T-U@grad.conj().T
   if np.linalg.norm(A)<1e-7:break
   step=1
   for ls in range(12):
    Ut=expm(step*A)@U;Gt,_=calc(Ut);vt=np.sum(Gt*Z)
    if vt>val+1e-12:U=Ut;break
    step*=.5
   else:break
  G,_=calc(U);gap=np.sum(G*Z)-sup;outer+=1
  if gap>best:
   best=gap;print(run,alt,gap,flush=True);np.savez(os.path.join(os.path.dirname(__file__),'q8_alternating_best.npz'),U=U,G=G,Z=Z,gap=gap)
  if best>1e-5 or time.process_time()-cpu>22:break
 if best>1e-5 or time.process_time()-cpu>22:break
print(json.dumps({'alternations':outer,'best':best,'wall':time.perf_counter()-st,'cpu':time.process_time()-cpu}))
