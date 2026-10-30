"""Actual constrained-field search after exact transverse-corrector elimination.

Searches the necessary tangent QC coefficient for the exceptional square.
Every underlying field is T Hess(psi), hence L(G)=0 exactly in the
analytic representation. Numerical values are diagnostics until exact
moments, a strict transverse construction, and global ROC are received.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product,permutations
import sys,json,time,math
import numpy as np,scipy.linalg as la
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import heat_model as h
start=time.perf_counter();data=np.load(root/'work/sharp_square_model.npz');ell=data['ell'];fac=data['fac'];T=np.linalg.inv(ell.reshape(2,2).T)@np.array([[0.,-1.],[1.,0.]]);J=np.array([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]],float)
F4=np.zeros((4,4,4,4))
for pw,co in h.F.items():
 ids=tuple(i for i,p in enumerate(pw) for _ in range(p));perms=set(permutations(ids))
 for ii in perms:F4[ii]=float(co)/len(perms)
freq=np.array([(i,j) for i,j in product(range(-3,4),repeat=2) if i>0 or i==0 and j>0]);N=16**2;grid=np.array(list(product(np.arange(16)*2*np.pi/16,repeat=2)));bh=[]
for k in freq:
 H=np.outer(k,k)/(k@k)
 for wave in (np.cos(grid@k),np.sin(grid@k)):bh.append(wave[:,None,None]*H)
bh=np.array(bh).transpose(1,0,2,3);ncoef=bh.shape[1]
def evaluate(x,cubic,withgrad=True):
 co=x[:ncoef];B=x[ncoef:].reshape(2,2);H=np.einsum('nkij,k->nij',bh,co);raw=np.einsum('ia,ba,nbc,cj->nij',T,B,H,B).reshape(N,4);sigma=np.mean(np.sum(raw*raw,axis=1)**2)**.25
 if sigma<1e-12:return 0.,np.zeros_like(x),None
 G=raw/sigma;f=float(np.einsum('ijkl,ni,nj,nk,nl->',F4,G,G,G,G,optimize=True)/N);v=4*np.einsum('ijkl,nj,nk,nl->i',F4,G,G,G,optimize=True)/N;HH=12*np.einsum('ijkl,nk,nl->ij',F4,G,G,optimize=True)/N
 m=cubic[:4];lam=cubic[4];P=2*np.outer(ell,m)+lam*J;PG=G@P.T;det=np.einsum('ni,ij,nj->n',G,J,G)/2;features=np.column_stack([PG,lam*det]);NN=features.T@features/N;AA=np.block([[HH/2,v[:,None]/2],[v[None,:]/2,np.array([[f]])]])
 try:vals,vec=la.eigh(NN,AA,check_finite=False)
 except la.LinAlgError:return -1e10,np.zeros_like(x),None
 eig=float(vals[-1]);nu=eig/4;mv=vec[:4,-1];zv=float(vec[4,-1]);psi=features@vec[:,-1]
 if withgrad:
  gn=2*psi[:,None]*(P.T@mv+lam*zv*(G@J));gd=12*np.einsum('ijkl,nj,k,l->ni',F4,G,mv,mv,optimize=True)+12*zv*np.einsum('ijkl,nj,nk,l->ni',F4,G,G,mv,optimize=True)+4*zv*zv*np.einsum('ijkl,nj,nk,nl->ni',F4,G,G,G,optimize=True);gg=(gn-eig*gd)/(4*N)
  gg=(gg-np.sum(gg*G)*np.sum(G*G,axis=1)[:,None]*G/N)/sigma;gk=np.einsum('ia,nij->naj',T,gg.reshape(N,2,2));gh=np.einsum('ia,nab,jb->nij',B,gk,B);gc=np.einsum('nij,nkij->k',gh,bh);gb=np.einsum('nia,ab,nbj->ij',H,B,gk+gk.transpose(0,2,1));grad=np.r_[gc,gb.ravel()]
 else:grad=None
 state={'nu_tangent':nu,'covariance_eigenvalues':np.linalg.eigvalsh(G.T@G/N).tolist(),'leading_a':float(2*f-v@np.linalg.solve(HH,v)),'generalized_eigenvector':vec[:,-1].tolist(),'mean_G_L2_square':float(np.mean((G@ell)**2)),'normalization':float(sigma),'domain_matrix':B.tolist(),'coefficients':co.tolist()}
 return nu,grad,state
rng=np.random.default_rng(1913031);x0=np.r_[rng.normal(size=ncoef),np.eye(2).ravel()];cub=fac[0];val,grad,_=evaluate(x0,cub)
checks=[]
for k in (0,11,ncoef,ncoef+1,ncoef+3):
 xp=x0.copy();xm=x0.copy();xp[k]+=1e-5;xm[k]-=1e-5;fd=(evaluate(xp,cub,False)[0]-evaluate(xm,cub,False)[0])/2e-5;checks.append((k,fd,float(grad[k])));assert abs(fd-grad[k])<1e-5*(1+abs(fd)),checks
print('independent derivative checks',checks,flush=True)
angles=list(np.linspace(0,np.pi,17,endpoint=False));best=[];globalbest=None;previous=[]
for ia,angle in enumerate(angles):
 cubic=np.array([np.cos(angle),np.sin(angle)])@fac;row=None
 for restart in range(5):
  if restart==0 and previous:xstart=previous[-1].copy()
  else:
   coeff=rng.normal(size=ncoef)/(1+np.repeat(np.linalg.norm(freq,axis=1),2))**.7;B=np.eye(2)+rng.normal(size=(2,2))*.35;xstart=np.r_[coeff,B.ravel()]
  opt=minimize(lambda x:(-evaluate(x,cubic)[0],-evaluate(x,cubic)[1]),xstart,jac=True,method='L-BFGS-B',options={'maxiter':350,'ftol':1e-12,'gtol':1e-7,'maxls':30});vv,_,state=evaluate(opt.x,cubic,False)
  if row is None or vv>row['nu_tangent']:row={'cubic_angle':float(angle),'restart':restart,'optimizer_success':bool(opt.success),'iterations':int(opt.nit),**state};xx=opt.x.copy()
 previous.append(xx);best.append(row);roc=json.loads((root/'work/sharp_square_explore.json').read_text())['directional_ROC_boundary_proposals'][ia]['necessary_nu_numerical'];row['sampled_ROC_necessary_nu']=roc;row['tangent_to_sampled_ROC_ratio']=row['nu_tangent']/roc
 print(json.dumps({k:row[k] for k in ('cubic_angle','nu_tangent','sampled_ROC_necessary_nu','tangent_to_sampled_ROC_ratio','leading_a','covariance_eigenvalues')}),flush=True)
 out={'derivative_checks':checks,'directional_results':best,'seconds':time.perf_counter()-start,'scope':__doc__};(root/'work/square_tangent_search.json').write_text(json.dumps(out,indent=2)+'\n')
