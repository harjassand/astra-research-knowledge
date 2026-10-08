"""Independent finite-spectrum/continuum-trial diagnostic, not an asymptotic proof."""
from pathlib import Path
import json,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigh
from scipy.optimize import minimize
out=Path(__file__).with_name('ground_xxz_spectrum.json')
J=1.; cases=[(5.,18.),(0.,25.),(20.,18.)]; grid=256
x=np.arange(1,grid)/grid; dx=1/grid
trials={}
for kap,lam in cases:
 def fg(t):
  z=np.r_[0,t,0]; rho=np.sin(t/2)**2
  f=J/2*np.sum(np.diff(z)**2)/dx-dx*np.sum(kap*rho**2+lam*rho)
  g=J*(2*t-z[:-2]-z[2:])/dx-dx*(2*kap*rho+lam)*np.sin(t)/2
  return f,g
 fits=[minimize(fg,A*np.sin(np.pi*x),jac=True,bounds=[(0,np.pi)]*len(x),method='L-BFGS-B',options={'ftol':1e-14,'gtol':1e-9,'maxiter':8000}) for A in [0.,.3,1.,2.,3.1]]
 best=min(fits,key=lambda r:r.fun)
 trials[(kap,lam)]={'theta':best.x,'grid_trial_energy':float(best.fun),'optimizer_success':bool(best.success),'grid':grid,'starts':len(fits)}
rows=[];start=time.time()
for L in [6,8,10,12,14]:
 S=L-1;dim=1<<S; idx=np.arange(dim,dtype=np.int64)
 bits=((idx[:,None]>>np.arange(S))&1).astype(float)
 number=bits.sum(axis=1); contact=(bits[:,:-1]*bits[:,1:]).sum(axis=1)
 diag=2*J*(bits[:,0]+bits[:,-1]); ii=[];jj=[];vv=[]
 for k in range(S-1):
  eligible=idx[bits[:,k]!=bits[:,k+1]];diag[eligible]+=2*J
  ii.extend(eligible.tolist());jj.extend((eligible^((1<<k)|(1<<(k+1)))).tolist());vv.extend([-2*J]*len(eligible))
 for kap,lam in cases:
  d=diag-(kap*contact+lam*number)/L**2
  H=coo_matrix((np.r_[vv,d],(np.r_[ii,idx],np.r_[jj,idx])),shape=(dim,dim)).tocsr()
  # Full-space Lanczos missed the exactly disconnected vacuum in the initial run.
  # Resolve each conserved-number block and include all one-dimensional sectors exactly.
  sectors=[]
  for m in range(S+1):
   inds=np.flatnonzero(number==m); block=H[inds][:,inds]
   if len(inds)==1:
    E=float(block[0,0]);v=np.ones(1)
   elif len(inds)<=128:
    vals,vecs=eigh(block.toarray(),subset_by_index=(0,0));E=float(vals[0]);v=vecs[:,0]
   else:
    vals,vecs=eigsh(block,k=1,which='SA',tol=1e-11,maxiter=50000,v0=np.ones(len(inds)));E=float(vals[0]);v=vecs[:,0]
   if v.sum()<0:v=-v
   residual=float(np.linalg.norm(block@v-E*v))
   sectors.append({'m':m,'energy':E,'residual':residual,'min_ground_component':float(v.min()),'dimension':len(inds)})
  winning=min(sectors,key=lambda z:z['energy']);E=winning['energy'];res=winning['residual']
  t=trials[(kap,lam)]; theta=np.interp(np.arange(1,L)/L,np.r_[0,x,1],np.r_[0,t['theta'],0]);rho=np.sin(theta/2)**2
  coherent=J*np.sum(1-np.cos(np.diff(theta)))+2*J*(rho[0]+rho[-1])-(kap*np.sum(rho[:-1]*rho[1:])+lam*np.sum(rho))/L**2
  rows.append({'L':L,'kappa':kap,'lambda':lam,'L_times_lowest_ritz':L*E,'ritz_residual':res,'mean_N_over_L':winning['m']/L,'L_times_coherent_trial':float(L*coherent),'continuum_grid_trial':t['grid_trial_energy'],'variational_order_pass':bool(E<=coherent+1e-8),'sectors':sectors})
  print(json.dumps({k:v for k,v in rows[-1].items() if k!='sectors'}),flush=True)
record={'scope':'Independent finite number-block sparse/dense diagonalization including exact vacuum and full sectors and continuum discretized trial optimization. Ritz values/residuals are numerical diagnostics, not certified lowest-eigenvalue bounds; continuum local optimization is a trial upper, not certified global minimization. No asymptotic proof or novelty validation.','J':J,'rows':rows,'max_ritz_residual':max(r['ritz_residual'] for r in rows),'all_variational_orders_pass':all(r['variational_order_pass'] for r in rows),'elapsed_seconds':time.time()-start,'continuum_trials':[{k:v for k,v in trials[c].items() if k!='theta'}|{'kappa':c[0],'lambda':c[1]} for c in cases]}
out.write_text(json.dumps(record,indent=2)+'\n')
print('Saved',out,flush=True)
