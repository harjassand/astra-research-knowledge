"""Construct self-compatibility certificate for Pauli+classical-flag channels.
R_fg >=0, sum_g diag R_fg = w_f p_f, sum_f diag(H R_fg H)=w_g p_g.
Uses real rank-four PSD factors; feasibility is diagnostic until exact residual and PSD checks.
"""
import os;os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json,sys,time
from scipy.optimize import least_squares
P=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
phi=np.eye(2)/np.sqrt(2)
W=np.zeros((8,8),complex);V=np.zeros((8,8),complex)
for i in range(4):
 bell=phi@P[i].T
 for s in range(2):
  W[:,2*i+s]=np.einsum('ab,c->abc',bell,P[i][:,s]).ravel()
  V[:,2*i+s]=np.einsum('ac,b->abc',bell,P[i][:,s]).ravel()
H=(V.conj().T@W).reshape(4,2,4,2)[:,0,:,0].real
assert np.max(abs(V.conj().T@W-np.kron(H,np.eye(2))))<1e-14
assert np.max(abs(H@H-np.eye(4)))<1e-14

def margins(R):
  p=np.einsum('fgii->fi',R)
  RH=np.einsum('ij,fgjk,kl->fgil',H,R,H)
  q=np.einsum('fgii->gi',RH)
  return p,q

def solve(target,seed=0,max_nfev=2000):
 B=len(target);rng=np.random.default_rng(seed);shape=(B,B,4,4)
 L=rng.normal(size=shape)/np.sqrt(16*B*B)
 def fun(x):
  L=x.reshape(shape);R=L@L.swapaxes(-1,-2);p,q=margins(R)
  return np.r_[(p-target).ravel(),(q-target).ravel()]
 def jac(x):
  L=x.reshape(shape);HL=np.einsum('ij,fgjk->fgik',H,L)
  J=np.zeros((2,B,4,B,B,4,4))
  for f in range(B):
   for g in range(B):
    for i in range(4):
     J[0,f,i,f,g,i,:]=2*L[f,g,i,:]
     J[1,g,i,f,g,:,:]=2*H[i,:,None]*HL[f,g,i,None,:]
  return J.reshape(8*B,-1)
 t=time.time();opt=least_squares(fun,L.ravel(),jac=jac,ftol=1e-13,gtol=1e-13,xtol=1e-13,max_nfev=max_nfev,method='trf')
 L=opt.x.reshape(shape);R=L@L.swapaxes(-1,-2)
 return dict(residual_max=float(np.max(abs(fun(opt.x)))),residual_norm=float(np.linalg.norm(fun(opt.x))),min_eig=float(np.linalg.eigvalsh(R).min()),R=R.tolist(),seconds=time.time()-t,nfev=opt.nfev,success=bool(opt.success))
if __name__=='__main__':
 records=[]
 data=json.load(open(os.path.dirname(os.path.dirname(__file__))+'/highnoise_jointflags_results.json'))
 for a in data:
  t=np.array(a['w'])[:,None]*np.array(a['pauli'])
  res=solve(t,seed=10,max_nfev=500)
  res.update(v=a['v'],r=a['r'],K=a['K'],target=t.tolist(),H=H.tolist());records.append(res)
  print({k:res[k] for k in ['v','r','K','residual_max','min_eig','seconds','nfev']},flush=True)
  json.dump(records,open(sys.argv[1],'w'),indent=2)
