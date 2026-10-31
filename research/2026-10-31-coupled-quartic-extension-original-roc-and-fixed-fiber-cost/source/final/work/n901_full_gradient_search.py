"""Actual full-gradient attack on UNMODIFIED J_r using all-mean elimination.

Every field is an actual periodic vector gradient. Quartic means are
eliminated analytically, and a covariance barrier prevents immediate
single-wave collapse. The numerical grid is exactly dealiased for the
stated Fourier support. Negative proposals require exact field receipt
and the universal ROC proof; no finite search certifies QC.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product,permutations
import sys,json,time
import numpy as np
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/quartic_coupling'));import receive as m
start=time.perf_counter();rng=np.random.default_rng(316472);freq=np.array([(i,j) for i,j in product(range(-3,4),repeat=2) if i>0 or i==0 and j>0]);side=16;grid=np.array(list(product(np.arange(side)*2*np.pi/side,repeat=2)));N=len(grid);basis=[]
for k in freq:
 unit=k/np.linalg.norm(k)
 for trig in (np.cos(grid@k),np.sin(grid@k)):
  for component in range(2):
   field=np.zeros((N,4));field[:,2*component:2*component+2]=trig[:,None]*unit;basis.append(field)
basis=np.array(basis);nc=len(basis)
def tensor(P):
 out=np.zeros((4,)*4)
 for pw,c in P.items():
  ids=tuple(i for i,n in enumerate(pw) for _ in range(n));perm=set(permutations(ids))
  for ix in perm:out[ix]=float(c)/len(perm)
 return out
def evaluate(co,TT,beta,grad=True):
 raw=np.einsum('k,kni->ni',co,basis);sigma=np.mean(np.sum(raw*raw,axis=1)**2)**.25
 if sigma<1e-14:return 1e10,np.zeros_like(co),None
 G=raw/sigma;S=G.T@G/N;sev=np.linalg.eigvalsh(S)
 if sev[0]<1e-13:return 1e10,np.zeros_like(co),None
 f=float(np.einsum('ijkl,ni,nj,nk,nl->',TT,G,G,G,G,optimize=True)/N);v=4*np.einsum('ijkl,nj,nk,nl->i',TT,G,G,G,optimize=True)/N;HH=12*np.einsum('ijkl,nk,nl->ij',TT,G,G,optimize=True)/N
 try:M=-np.linalg.solve(HH,v)
 except np.linalg.LinAlgError:return 1e10,np.zeros_like(co),None
 if np.linalg.norm(M)>1e6 or f<=1e-18:return 1e10,np.zeros_like(co),None
 energy=float(f+v@M+M@HH@M/2);ratio=energy/f;obj=ratio-beta*np.linalg.slogdet(S)[1]
 if grad:
  gf=4*np.einsum('ijkl,nj,nk,nl->ni',TT,G,G,G,optimize=True)/N;ga=gf+12*np.einsum('ijkl,nj,nk,l->ni',TT,G,G,M,optimize=True)/N+12*np.einsum('ijkl,nj,k,l->ni',TT,G,M,M,optimize=True)/N;gG=(ga-ratio*gf)/f-2*beta*(G@np.linalg.inv(S))/N;graw=(gG-np.sum(gG*G)*np.sum(G*G,axis=1)[:,None]*G/N)/sigma;gg=np.einsum('ni,kni->k',graw,basis)
 else:gg=None
 return obj,gg,{'normalized_gap':ratio,'energy_gap':energy,'quartic_moment':f,'mean':M.tolist(),'covariance_eigenvalues':sev.tolist(),'normal_curl_L2':float(np.mean((G[:,1]-G[:,2])**2)),'gradient_L4_normalization':float(sigma)}
history=[];best=None;derivative_checks=[]
for rr in (R(3,4),R(1),R(2),R(1,10),R(10)):
 F,H=m.n901(rr);TT=tensor(F);local=None
 for restart in range(3):
  co=rng.normal(size=nc)/np.repeat(1+np.linalg.norm(freq,axis=1),4)**.6
  if restart==0:
   # A real Hessian seed with an actual normal component, rather than
   # a free matrix law or an imposed zero-mean determinant surrogate.
   co*=.1
   for k in ((1,0),(0,1),(1,1)):
    idx=next(i for i,x in enumerate(freq) if tuple(x)==k);co[4*idx:4*idx+2]+=np.array(k,dtype=float)/np.linalg.norm(k)
  co/=np.linalg.norm(co)
  if not derivative_checks:
   val,g,_=evaluate(co,TT,1e-3);steps=[]
   for j in (0,7,21,57,89):
    xx=co.copy();yy=co.copy();xx[j]+=1e-5;yy[j]-=1e-5;fd=(evaluate(xx,TT,1e-3,False)[0]-evaluate(yy,TT,1e-3,False)[0])/2e-5;assert abs(fd-g[j])<2e-5*(1+abs(fd));steps.append([j,float(fd),float(g[j])])
   derivative_checks=steps;print('analytic envelope gradients checked',flush=True)
  for beta in (1e-3,1e-5,0.):
   opt=minimize(lambda x:evaluate(x,TT,beta)[:2],co,jac=True,method='SLSQP',constraints=[{'type':'eq','fun':lambda x:float(x@x-1),'jac':lambda x:2*x}],options={'maxiter':350,'ftol':1e-12});co=opt.x/np.linalg.norm(opt.x);_,_,state=evaluate(co,TT,beta,False)
   if state is None:continue
   rec={'r':str(rr),'restart':restart,'barrier':beta,'iterations':int(opt.nit),'solver_success':bool(opt.success),'solver_message':str(opt.message),'coefficient_norm':float(np.linalg.norm(co)),**state};history.append(rec)
   if local is None or state['normalized_gap']<local['normalized_gap']:local={'normalized_gap':state['normalized_gap'],'coefficients':co.tolist(),'row':rec}
   if best is None or state['normalized_gap']<best['normalized_gap']:best={'r':str(rr),**local}
   print(json.dumps(rec),flush=True)
   (root/'work/n901_full_gradient_search.json').write_text(json.dumps({'history':history,'best':best,'frequencies':freq.tolist(),'grid_side':side,'highest_quartic_coordinate_frequency':12,'field_real_coefficients':nc,'coefficient_norm_constraint':'Euclidean sphere, enforced by SLSQP','analytic_gradient_checks':derivative_checks,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
   if state['normalized_gap']<-1e-6:raise SystemExit('Strict numerical candidate: exact actual-field receipt required.')
