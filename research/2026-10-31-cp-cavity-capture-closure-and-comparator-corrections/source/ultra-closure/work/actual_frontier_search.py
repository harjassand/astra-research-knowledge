"""Alternate actual Fourier-gradient variation and all-cubic ROC fitting.

The ROC fit uses a globally sufficient deflated Bernstein cone, rather
than sampled rank-one inequalities. Numerical solver output remains a
proposal until rational data pass an independent exact global receiver.
"""
from pathlib import Path
from itertools import product
from math import factorial
import json,time,sys
import numpy as np
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import roc_inner_model as model
h=model.h;F=h.F;CP=model.CP;QP=model.QP;start=time.perf_counter()
def tensor(P,n):
 out=np.zeros((4,)*n)
 for ids in product(range(4),repeat=n):
  pw=tuple(ids.count(i) for i in range(4));out[ids]=float(P.get(pw,0))*np.prod([factorial(v) for v in pw])/factorial(n)
 return out
F4=tensor(F,4);C3=np.array([tensor(P,3) for P in CP]);Q2=np.array([tensor(P,2) for P in QP]);mmax=2;gridn=12;freq=np.array([(x,y) for x,y in product(range(-mmax,mmax+1),repeat=2) if x>0 or x==0 and y>0],float);nm=len(freq);angle=np.array(list(product(np.arange(gridn)*2*np.pi/gridn,repeat=2)));phase=angle@freq.T;DP=np.concatenate((np.cos(phase)[:,:,None]*freq[None,:,:],-np.sin(phase)[:,:,None]*freq[None,:,:]),axis=1).transpose(0,2,1);npts=len(angle);nf=2*nm
def field(x,detail=False):
 co=x[:2*nf].reshape(2,nf);B=x[2*nf:].reshape(2,2);D=np.einsum('om,pxm->pox',co,DP);G=np.einsum('pox,xy->poy',D,B).reshape(npts,4);alpha=np.mean(np.sum(G*G,axis=1)**2)**.25;u=G/alpha
 return (u,D,B,alpha) if detail else u
def moments(G):
 f=float(np.mean(np.einsum('ijkl,pi,pj,pk,pl->p',F4,G,G,G,G)));ell=np.mean(np.einsum('sijk,pi,pj,pk->ps',C3,G,G,G),axis=0);qm=np.mean(np.einsum('sij,pi,pj->ps',Q2,G,G),axis=0);return f,ell,qm
def statistics(G,C,Q,derivative=False):
 DF=4*np.einsum('ijkl,pj,pk,pl->pi',F4,G,G,G);HF=12*np.einsum('ijkl,pk,pl->pij',F4,G,G);DC=3*np.einsum('ijk,pj,pk->pi',C,G,G);HC=6*np.einsum('ijk,pk->pij',C,G);f=np.mean(np.sum(DF*G,axis=1))/4;c=np.mean(np.sum(DC*G,axis=1))/3;q=np.mean(np.einsum('ij,pi,pj->p',Q,G,G));H=np.mean(HF,axis=0);v=np.mean(DF,axis=0);w=np.mean(DC,axis=0);a0=np.linalg.solve(H,v);b0=np.linalg.solve(H,w);a=2*f-v@a0;b=2*q-w@b0;r=c-v@b0;ratio=r*r/(a*b)
 data={'ratio':float(ratio),'a':float(a),'b':float(b),'r':float(r),'f':float(f),'q':float(q),'H_condition':float(np.linalg.cond(H)),'covariance_eigenvalues':np.linalg.eigvalsh(G.T@G/npts).tolist()}
 if not derivative:return data
 da=2*DF-2*np.einsum('pij,j->pi',HF,a0)+24*np.einsum('ijkl,j,k,pl->pi',F4,a0,a0,G);dr=DC-np.einsum('pij,j->pi',HF,b0)-np.einsum('pij,j->pi',HC,a0)+24*np.einsum('ijkl,j,k,pl->pi',F4,a0,b0,G);db=4*G@Q-2*np.einsum('pij,j->pi',HC,b0)+24*np.einsum('ijkl,j,k,pl->pi',F4,b0,b0,G);grad=-(2*dr/r-da/a-db/b)/npts
 return data,grad
def optimize(x,C,Q):
 def fg(x):
  G,D,B,alpha=field(x,True)
  try:d,g=statistics(G,C,Q,True)
  except np.linalg.LinAlgError:return 1e10,np.zeros_like(x)
  if d['a']<=0 or d['b']<=0 or d['ratio']<=0 or not np.isfinite(d['ratio']):return 1e10,np.zeros_like(x)
  correction=np.sum(g*G);gg=(g-correction*np.sum(G*G,axis=1)[:,None]*G/npts)/alpha;gg=gg.reshape(npts,2,2);gd=np.einsum('poy,xy->pox',gg,B);gc=np.einsum('pox,pxm->om',gd,DP);gb=np.einsum('pox,poy->xy',D,gg);grad=np.concatenate((gc.ravel(),gb.ravel()));return -np.log(d['ratio']),grad
 opt=minimize(fg,x,jac=True,method='L-BFGS-B',options={'maxiter':350,'ftol':1e-12,'gtol':1e-6,'maxls':40});return opt
rng=np.random.default_rng(20261031);solver=model.Model();runs=[];best=None
for run in range(6):
 co=rng.normal(size=(2,nf));co*=np.tile(1/(1+np.sum(freq*freq,axis=1)),2)[None,:];BB=np.eye(2)+.2*rng.normal(size=(2,2));x=np.concatenate((co.ravel(),BB.ravel()))
 for iteration in range(6):
  G=field(x);f,ell,qm=moments(G)
  try:p=solver.solve(ell,qm)
  except Exception as err:print('polynomial fit failed',run,iteration,type(err).__name__,str(err),flush=True);break
  if p is None:break
  cv=np.array(p['cubic_coordinates']);qv=np.array(p['quadratic_coordinates']);C=np.einsum('s,sijk->ijk',cv,C3);Q=np.einsum('s,sij->ij',qv,Q2);before=statistics(G,C,Q);opt=optimize(x,C,Q);x=opt.x;after=statistics(field(x),C,Q);record={'run':run,'iteration':iteration,'fit_energy':f+p['objective'],'before':before,'after':after,'cubic_coordinates':p['cubic_coordinates'],'quadratic_coordinates':p['quadratic_coordinates'],'least_numerical_Bernstein_slack':p['least_numerical_Bernstein_slack'],'parameters':x.tolist(),'optimizer_iterations':opt.nit,'optimizer_success':bool(opt.success)};runs.append(record)
  if after['a']>0 and after['b']>0 and (best is None or after['ratio']>best['after']['ratio']):best=record
  print(json.dumps({'run':run,'iteration':iteration,'fit_energy':record['fit_energy'],'ratio_before':before['ratio'],'ratio_after':after['ratio'],'least_numerical_Bernstein_slack':p['least_numerical_Bernstein_slack'],'seconds':time.perf_counter()-start}),flush=True)
  out={'scope':'Numerical alternating attack. Fields are genuine Fourier gradients, but polynomial coefficients and the sufficient global ROC Bernstein inequalities still require rational rigorous verification. No separation is admitted by solver status.','max_base_frequency':mmax,'quadrature_grid':gridn,'quadrature_exact_for_degree_at_most':4,'frequencies':freq.tolist(),'runs':runs,'best':best,'seconds':time.perf_counter()-start};(root/'work/actual_frontier_search.json').write_text(json.dumps(out,indent=2)+'\n')
  if after['ratio']>1.0001 and after['H_condition']<1e10:print('candidate requires exact field and ROC admission',flush=True);break
 if best is not None and best['after']['ratio']>1.0001:break
