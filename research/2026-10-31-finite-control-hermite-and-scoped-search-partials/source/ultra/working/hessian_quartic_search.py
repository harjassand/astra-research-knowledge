"""Actual scalar-Hessian search over the whole homogeneous quartic ROC cone.

All cone fits use one lossless 9x9 PSD matrix, without angular sampling.
Numerical fit status is not a global admission or counterexample receipt.
"""
from pathlib import Path
from itertools import product,permutations
import sys,time,json
import numpy as np
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import hessian_quartic_cone as m
start=time.perf_counter();rng=np.random.default_rng(997314);freq=np.array([(i,j) for i,j in product(range(-3,4),repeat=2) if i>0 or i==0 and j>0]);N=256;grid=np.array(list(product(np.arange(16)*2*np.pi/16,repeat=2)));bh=[]
for k in freq:
 H=np.outer(k,k)/(k@k)
 for wave in (np.cos(grid@k),np.sin(grid@k)):bh.append(wave[:,None,None]*H)
bh=np.array(bh).transpose(1,0,2,3);ncoef=bh.shape[1];PP=np.array(m.powers,int)
def field(x):
 co=x[:ncoef];B=x[ncoef:ncoef+4].reshape(2,2);mean=x[-3:];H=np.einsum('nkij,k->nij',bh,co);raw=np.einsum('ai,nab,bj->nij',B,H,B);rr=np.column_stack([raw[:,0,0],raw[:,0,1],raw[:,1,1]]);norm=np.mean((rr[:,0]**2+2*rr[:,1]**2+rr[:,2]**2)**2)**.25
 return H,B,mean,rr/norm,norm
def moments(x):
 _,_,mean,G,_=field(x);A=G+mean;return np.mean(np.prod(A[:,None,:]**PP[None,:,:],axis=2),axis=0)-np.prod(mean[None,:]**PP,axis=1)
def tensor(coeff):
 TT=np.zeros((3,3,3,3))
 for pw,co in zip(PP,coeff):
  ids=tuple(i for i,p in enumerate(pw) for _ in range(p));perm=set(permutations(ids))
  for ii in perm:TT[ii]=co/len(perm)
 return TT
def value_grad(x,TT):
 H,B,mean,G,norm=field(x);A=G+mean;f=np.einsum('ijkl,ni,nj,nk,nl->',TT,A,A,A,A,optimize=True)/N-np.einsum('ijkl,i,j,k,l',TT,mean,mean,mean,mean,optimize=True);dA=4*np.einsum('ijkl,nj,nk,nl->ni',TT,A,A,A,optimize=True)/N;gm=np.sum(dA,axis=0)-4*np.einsum('ijkl,j,k,l->i',TT,mean,mean,mean,optimize=True)
 wg=G*np.array([1,2,1]);graw=(dA-np.sum(dA*G)*np.sum(wg*G,axis=1)[:,None]*wg/N)/norm;gk=np.zeros((N,2,2));gk[:,0,0]=graw[:,0];gk[:,0,1]=gk[:,1,0]=graw[:,1]/2;gk[:,1,1]=graw[:,2];gh=np.einsum('ia,nab,jb->nij',B,gk,B);gc=np.einsum('nij,nkij->k',gh,bh);gb=np.einsum('nia,ab,nbj->ij',H,B,gk+gk.transpose(0,2,1));return float(f),np.r_[gc,gb.ravel(),gm]
model=m.Model();history=[];best=None
for restart in range(12):
 co=rng.normal(size=ncoef)/(1+np.repeat(np.linalg.norm(freq,axis=1),2));B=np.eye(2)+rng.normal(size=(2,2))*.25;mean=rng.normal(size=3)*(.3 if restart%2 else 1.);x=np.r_[co,B.ravel(),mean]
 for iteration in range(12):
  fit=model.solve(moments(x));TT=tensor(fit['coefficients'])
  if restart==0 and iteration==0:
   vv,grad=value_grad(x,TT);checks=[]
   for k in (0,13,ncoef,ncoef+1,ncoef+4,ncoef+6):
    xp=x.copy();xm=x.copy();xp[k]+=1e-5;xm[k]-=1e-5;fd=(value_grad(xp,TT)[0]-value_grad(xm,TT)[0])/2e-5;checks.append((k,fd,float(grad[k])));assert abs(fd-grad[k])<1e-6*(1+abs(fd)),checks
   print('independent gradients checked',checks,flush=True)
  opt=minimize(lambda z:value_grad(z,TT),x,jac=True,method='L-BFGS-B',options={'maxiter':250,'ftol':1e-13,'gtol':1e-8,'maxls':30});x=opt.x;val,_=value_grad(x,TT);_,BB,MM,G,_=field(x);rec={'restart':restart,'iteration':iteration,'fit_energy':fit['objective'],'optimized_energy':val,'Gram_minimum_eigenvalue':fit['Gram_minimum_eigenvalue'],'covariance_eigenvalues':np.linalg.eigvalsh(G.T@G/N).tolist(),'mean':MM.tolist(),'domain_matrix':BB.tolist()};history.append(rec)
  if best is None or val<best['energy']:best={'energy':val,'field_parameters':x.tolist(),'fit':fit,'history_row':rec}
  print(json.dumps(rec),flush=True)
  (root/'work/hessian_quartic_search.json').write_text(json.dumps({'powers':m.powers,'history':history,'best':best,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
  if val<-1e-7:raise SystemExit('Strict numerical negative candidate: exact Gram and actual-field receipt required next.')
