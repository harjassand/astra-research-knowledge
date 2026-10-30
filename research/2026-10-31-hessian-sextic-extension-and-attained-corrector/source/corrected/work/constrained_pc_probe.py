"""Search for incompatible minor supports inside the actual constraint plane.

This is only a pointwise comparator; a non-PC cut is not a QC obstruction.
"""
from pathlib import Path
from itertools import product,permutations
import json,sys,time
import numpy as np
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];ss=(root/'work/square_tangent_search.py').read_text();ns={'__file__':str(root/'work/square_tangent_search.py'),'__name__':'tensor_helpers'};exec(ss[:ss.index('rng=np.random')],ns);globals().update({k:v for k,v in ns.items() if k not in ('__file__','__name__','__doc__')});start=time.perf_counter();Z=np.array([[-ell[1],0,-ell[3]],[1,0,0],[0,1,0],[0,0,1]],float);D=Z.T@J@Z/2;ev,O=np.linalg.eigh(D);pids=np.where(ev>0)[0];nids=np.where(ev<0)[0];assert len(pids)==2 and len(nids)==1;V=Z@O[:,list(pids)+list(nids)]/np.sqrt(abs(ev[list(pids)+list(nids)]))[None,:]
def ray(theta,t,sign):
 if sign>0:w=np.array([np.cos(theta)*np.cosh(t),np.sin(theta)*np.cosh(t),np.sinh(t)])
 else:w=np.array([np.cos(theta)*np.sinh(t),np.sin(theta)*np.sinh(t),np.cosh(t)])
 return V@w
def support(R):
 f=np.einsum('ijkl,i,j,k,l',F4,R,R,R,R);v=4*np.einsum('ijkl,j,k,l->i',F4,R,R,R);H=12*np.einsum('ijkl,k,l->ij',F4,R,R);return (H/2-np.outer(v,v)/(4*f))/(R@J@R/2)
def value(x,ret=False):
 rp=ray(x[0],x[1],1);rm=ray(x[2],x[3],-1);E=support(rm)-support(rp);eig,vec=np.linalg.eigh(E);return (float(eig[-1]),vec[:,-1],rp,rm) if ret else float(eig[-1])
rng=np.random.default_rng(75121);best=(-1e99,None)
for i in range(60):
 xx=[rng.uniform(0,2*np.pi),rng.uniform(-2,2),rng.uniform(0,2*np.pi),rng.uniform(-2,2)];opt=minimize(lambda x:-value(x),xx,method='L-BFGS-B',bounds=[(0,2*np.pi),(-3,3),(0,2*np.pi),(-3,3)],options={'maxiter':200,'ftol':1e-14,'gtol':1e-8});v=value(opt.x)
 if v>best[0]:best=(v,opt.x.copy())
val,M,rp,rm=value(best[1],True);out={'incompatible_support_gap':val,'mean':M.tolist(),'Rplus':rp.tolist(),'Rminus':rm.tolist(),'constraint_on_Rplus':float(ell@rp),'constraint_on_Rminus':float(ell@rm),'parameters':best[1].tolist(),'seconds':time.perf_counter()-start,'scope':__doc__};(root/'work/constrained_pc_probe.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
