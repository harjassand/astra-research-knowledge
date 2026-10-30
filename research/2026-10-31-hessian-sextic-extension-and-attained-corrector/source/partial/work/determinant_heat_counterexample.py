"""Search actual scalar Hessians where ordinary heat increases det^2 energy.

det^2 is known polyconvex. A strict received example would rule out
universal ordinary-heat monotonicity, not quasiconvexity or capacity.
"""
from pathlib import Path
from itertools import product
import sys,time,json
import numpy as np
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];start=time.perf_counter();freq=np.array([(i,j) for i,j in product(range(-3,4),repeat=2) if i>0 or i==0 and j>0]);N=256;grid=np.array(list(product(np.arange(16)*2*np.pi/16,repeat=2)));basis=[]
for k in freq:
 r=np.array([k[0]**2,k[0]*k[1],k[1]**2],float)/(k@k)
 for w in (np.cos(grid@k),np.sin(grid@k)):basis.append(w[:,None]*r)
basis=np.array(basis).transpose(1,0,2);weights=np.repeat(np.sum(freq*freq,axis=1),2);D=np.array([[0,0,1],[0,-2,0],[1,0,0]],float);W=np.array([1,2,1]);nc=basis.shape[1]
def value(c):
 raw=np.einsum('nka,k->na',basis,c);norm=np.mean(np.sum(raw*raw*W,axis=1)**2)**.25;A=raw/norm;At=-np.einsum('nka,k->na',basis,weights*c)/norm;adj=A@D;det=np.einsum('na,na->n',A,adj)/2;dt=np.einsum('na,na->n',adj,At);obj=float(np.mean(2*det*dt));ga=2*(adj*dt[:,None]+det[:,None]*(At@D));gt=2*det[:,None]*adj;grad=(np.einsum('na,nka->k',ga,basis)-weights*np.einsum('na,nka->k',gt,basis))/N/norm;grad-=4*obj*np.einsum('na,nka->k',np.sum(A*A*W,axis=1)[:,None]*A*W,basis)/N/norm;return obj,grad
rng=np.random.default_rng(8997);c=rng.normal(size=nc);v,g=value(c);checks=[]
for k in (0,5,20):
 cp=c.copy();cm=c.copy();cp[k]+=1e-5;cm[k]-=1e-5;fd=(value(cp)[0]-value(cm)[0])/2e-5;checks.append((k,fd,float(g[k])));assert abs(fd-g[k])<1e-7,checks
print('independent derivatives',checks,flush=True);best=(-1e99,None)
for i in range(80):
 c=rng.normal(size=nc)/(1+np.repeat(np.linalg.norm(freq,axis=1),2));opt=minimize(lambda x:(-value(x)[0],-value(x)[1]),c,jac=True,method='L-BFGS-B',options={'maxiter':400,'ftol':1e-13,'gtol':1e-8});vv=value(opt.x)[0]
 if vv>best[0]:best=(vv,opt.x.copy());print('heat energy derivative proposal',i,vv,flush=True)
 if vv>1e-4:break
out={'heat_energy_derivative':best[0],'frequencies':freq.tolist(),'hessian_amplitude_coefficients':best[1].tolist(),'seconds':time.perf_counter()-start,'scope':__doc__};(root/'work/determinant_heat_counterexample.json').write_text(json.dumps(out,indent=2)+'\n');print('final',best[0],flush=True)
