import os;os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json,math,numpy as np
from scipy.optimize import differential_evolution,minimize
from schur_channel import entropy
from rectangle_flags import rectangle
Ps=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)

def ic_bloch(b,w,ps):
 r=np.linalg.norm(b)
 if r>1:return -10*(r-1)
 rho=(Ps[0]+b[0]*Ps[1]+b[1]*Ps[2]+b[2]*Ps[3])/2
 e,U=np.linalg.eigh(rho);A=(U*np.sqrt(np.maximum(e,0)))@U.conj().T
 vec=np.einsum('ab,kcb->kac',A,Ps).reshape(4,4)
 Ys=np.einsum('ki,kj->kij',vec,vec.conj())
 Y=np.einsum('hk,kij->hij',ps,Ys)
 X=np.einsum('hknkm->hnm',Y.reshape(len(w),2,2,2,2))
 return float(w@(entropy(X)-entropy(Y)))

if __name__=='__main__':
 records=[]
 for v in [1/math.e+1e-5,.3681,.369,.37]:
  for aspect in [1,2,2.75,3.5,5]:
   info=rectangle(v,aspect,24,24);w=np.array(info['weights']);ps=np.array(info['paulis'])
   vals=[]
   for axis in range(3):
    for mag in [.0,.5,.9,.99,.999]:
     b=np.zeros(3);b[axis]=mag;vals.append((ic_bloch(b,w,ps),b.tolist()))
   best=max(vals)
   opt=differential_evolution(lambda z:-ic_bloch(z,w,ps),[(-1,1)]*3,seed=10,popsize=6,maxiter=30,tol=1e-6,polish=True)
   row=dict(v=v,aspect=aspect,flags=len(w),maxmixed=info['one_use_ic'],grid_best=best,optimized=-opt.fun,bloch=opt.x.tolist());records.append(row);print(json.dumps(row),flush=True)
   json.dump(records,open(sys.argv[1],'w'),indent=2)
