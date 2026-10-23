import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,time,json
from scipy.linalg import expm
from scipy.optimize import minimize
from itertools import permutations
st=time.perf_counter();cpu=time.process_time();rng=np.random.default_rng(33442)
q=8
Ge=np.zeros((q,q))
for j in range(q):
 for bit in range(3):
  Ge[j,j]+=.5;Ge[j,j^(1<<bit)]+=.5
perms=np.array(list(permutations(range(q))),dtype=np.int8)
Gps=Ge[perms[:,:,None],perms[:,None,:]].reshape(-1,64)

def gram(U):
 G=np.zeros((8,8))
 for bit in range(3):
  r=[]
  for j in range(q):
   f=np.moveaxis(U[:,j].reshape(2,2,2),bit,0).reshape(2,4)
   r.append(f.conj().T@f)
  r=np.array(r).reshape(8,16)
  G+=.5*(r.conj()@r.T).real
 return G
best=-1e3;bestdata=None;cases=0
# Test Ky Fan and rank-one support violations; budget <20cpu seconds.
for k in range(2000):
 z=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));h=z+z.conj().T
 U=expm(1j*(.005,.03,.1,.3,1)[k%5]*h)
 G=gram(U);eg=np.linalg.eigvalsh(G)[::-1];e0=np.linalg.eigvalsh(Ge)[::-1]
 diff=np.cumsum(eg)-np.cumsum(e0)
 if np.max(diff[1:-1])>1e-6:
  print('SPECTRAL',k,diff);bestdata=(U,G);break
 # 8 vector probes, bound via all labelled cubes (840 distinct graphs).
 uniq=Gps[::1] if False else None
 for trial in range(2):
  c=rng.normal(size=8);c-=np.mean(c);c/=np.linalg.norm(c)
  val=c@G@c-np.max(Gps@(np.outer(c,c).reshape(-1)))
  if val>best:best=val;bestdata=(U,G)
  if val>1e-6:
   print('RANKONE',k,val);break
 cases+=1
 if best>1e-6 or time.process_time()-cpu>18:break
print(json.dumps({'cases':cases,'rankone_best':best,'wall':time.perf_counter()-st,'cpu':time.process_time()-cpu}))
np.savez(os.path.join(os.path.dirname(__file__),'q8_best.npz'),U=bestdata[0],G=bestdata[1])
