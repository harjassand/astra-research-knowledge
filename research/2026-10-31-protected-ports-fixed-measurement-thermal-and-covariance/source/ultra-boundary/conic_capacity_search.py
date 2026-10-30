"""Search actual scalar-Hessian fields with the exact conic ROC SDP.

All angular directions on the covariance face enter one 13x13 Gram.
A strict negative numerical result would still need exact rational Gram,
actual-field replay, and global ROC extension before any separation claim.
"""
from pathlib import Path
from itertools import product
import json,sys,time
import numpy as np
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import conic_capacity_model as cm
ss=(root/'work/actual_frontier_search.py').read_text();ns={'__file__':str(root/'work/actual_frontier_search.py'),'__name__':'actual_helpers'};exec(ss[:ss.index('rng=np.random')],ns);tensor=ns['tensor'];stats=ns['statistics'];F4=ns['F4'];C3=ns['C3'];Q2=np.array([tensor(P,2) for P in cm.Qext]);T=np.array(cm.T,float);start=time.perf_counter();mmax=3;gridn=16;freq=np.array([(x,y) for x,y in product(range(-mmax,mmax+1),repeat=2) if x>0 or x==0 and y>0],float);nf=len(freq);phases=np.array(list(product(np.arange(gridn)*2*np.pi/gridn,repeat=2)))@freq.T;HB=np.concatenate((-np.cos(phases)[:,:,None,None]*np.einsum('mi,mj->mij',freq,freq)[None,:,:,:],-np.sin(phases)[:,:,None,None]*np.einsum('mi,mj->mij',freq,freq)[None,:,:,:]),axis=1).transpose(0,2,3,1);N=gridn*gridn
def field(x,detail=False):
 co=x[:2*nf];B=x[2*nf:].reshape(2,2);H=np.einsum('pijm,m->pij',HB,co);Hx=np.einsum('ai,pab,bj->pij',B,H,B);G=np.einsum('ai,pij->paj',T,Hx).reshape(N,4);alpha=np.mean(np.sum(G*G,axis=1)**2)**.25;G=G/alpha
 return (G,H,B,alpha) if detail else G
def moments(G):
 f=float(np.mean(np.einsum('ijkl,pi,pj,pk,pl->p',F4,G,G,G,G)));ell=np.mean(np.einsum('sijk,pi,pj,pk->ps',C3,G,G,G),axis=0);qm=np.mean(np.einsum('sij,pi,pj->ps',Q2,G,G),axis=0);return f,ell,qm
def fg(x,C,Q):
 G,H,B,alpha=field(x,True)
 try:d,g=stats(G,C,Q,True)
 except np.linalg.LinAlgError:return 1e10,np.zeros_like(x)
 if d['a']<=0 or d['b']<=0 or d['ratio']<=0 or not np.isfinite(d['ratio']):return 1e10,np.zeros_like(x)
 corr=np.sum(g*G);gg=(g-corr*np.sum(G*G,axis=1)[:,None]*G/N).reshape(N,2,2)/alpha;K=np.einsum('ai,paj->pij',T,gg);Z=np.einsum('ai,pij,bj->pab',B,K,B);gc=np.einsum('pab,pabm->m',Z,HB);gb=np.einsum('pab,bi,pij->aj',H,B,K+K.transpose(0,2,1));return -np.log(d['ratio']),np.concatenate((gc,gb.ravel()))
rng=np.random.default_rng(20261031);solver=cm.Model();runs=[];best=None
# A meaningful derivative check against the independently admitted fixture.
xx=np.concatenate((rng.normal(size=2*nf)/np.tile(1+np.sum(freq*freq,axis=1),2),np.eye(2).ravel()));C0=tensor(cm.h.C,3);QQ=1859*np.eye(4);value,grad=fg(xx,C0,QQ)
for i in (0,3,2*nf,2*nf+1):
 dx=np.zeros_like(xx);dx[i]=1e-6;fd=(fg(xx+dx,C0,QQ)[0]-fg(xx-dx,C0,QQ)[0])/(2e-6);assert abs(fd-grad[i])<1e-4*(1+abs(fd)),(i,fd,grad[i])
print('analytic actual-field derivatives verified',flush=True)
for run in range(4):
 x=np.concatenate((rng.normal(size=2*nf)/np.tile(1+np.sum(freq*freq,axis=1),2),np.eye(2).ravel()+.15*rng.normal(size=4)))
 for iteration in range(12):
  G=field(x);f,ell,qm=moments(G)
  try:p=solver.solve(ell,qm)
  except Exception as err:print('conic fit failed',run,iteration,type(err).__name__,str(err),flush=True);break
  if p is None:break
  c=np.array(p['cubic_coordinates']);q=np.array(p['quadratic_coordinates']);C=np.einsum('s,sijk->ijk',c,C3);Q=np.einsum('s,sij->ij',q,Q2);before=stats(G,C,Q);opt=minimize(lambda x:fg(x,C,Q),x,jac=True,method='L-BFGS-B',options={'maxiter':400,'ftol':1e-12,'gtol':1e-6,'maxls':40});x=opt.x;after=stats(field(x),C,Q);record={'run':run,'iteration':iteration,'fit_energy':f+p['objective'],'before':before,'after':after,'parameters':x.tolist(),'polynomial':p,'optimizer_iterations':opt.nit,'optimizer_success':bool(opt.success)};runs.append(record)
  if after['a']>0 and after['b']>0 and (best is None or after['ratio']>best['after']['ratio']):best=record
  print(json.dumps({'run':run,'iteration':iteration,'fit_energy':record['fit_energy'],'ratio_before':before['ratio'],'ratio_after':after['ratio'],'Gram_min_eigenvalue':p['minimum_numerical_Gram_eigenvalue'],'coefficient_residual':p['maximum_numerical_coefficient_residual'],'seconds':time.perf_counter()-start}),flush=True)
  out={'scope':'Actual gradient numerical attack with a lossless conic ROC SDP. No globally ROC-admitted separation without exact conic and global extension checks.','T':[[str(v) for v in row] for row in cm.T],'frequencies':freq.tolist(),'quadrature_grid':gridn,'base_frequency_maximum':mmax,'runs':runs,'best':best,'seconds':time.perf_counter()-start};(root/'work/conic_capacity_search.json').write_text(json.dumps(out,indent=2)+'\n')
  if record['fit_energy']<-1e-5 or after['ratio']>1.0001:print('candidate requires exact conic Gram, actual field and global ROC extension',flush=True);break
 if best is not None and (best['fit_energy']<-1e-5 or best['after']['ratio']>1.0001):break
