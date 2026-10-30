"""Broader actual-Hessian search with analytic mean elimination and a
covariance barrier to avoid the earlier single-wave collapse.

Rational Hessian seeds have exact ROC Grams. Square-tangent targets have
only proposed coefficients here and require separate ROC admission.
No numerical negative is called a separation before exact receipt.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product,permutations
import sys,json,time
import numpy as np,scipy.linalg as la
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import heat_model as h
start=time.perf_counter();rng=np.random.default_rng(441792);freq=np.array([(i,j) for i,j in product(range(-7,8),repeat=2) if i>0 or i==0 and j>0]);N=32**2;grid=np.array(list(product(np.arange(32)*2*np.pi/32,repeat=2)));bh=[]
for k in freq:
 HH=np.outer(k,k)/(k@k)
 for wave in (np.cos(grid@k),np.sin(grid@k)):bh.append(wave[:,None,None]*HH)
bh=np.array(bh).transpose(1,0,2,3);nc=bh.shape[1];metric=np.array([1,2,1])
def tensor(poly,dim):
 TT=np.zeros((dim,)*4)
 for pw,co in poly.items():
  ids=tuple(i for i,p in enumerate(pw) for _ in range(p));ps=set(permutations(ids))
  for ii in ps:TT[ii]=float(co)/len(ps)
 return TT
seeds=json.loads((root/'outputs/hessian_frontier/seeds.json').read_text());cases=[]
for rec in seeds['records']:cases.append((rec['name'],tensor({tuple(pw):R(v) for pw,v in zip(seeds['powers'],rec['quartic_coefficients'])},3),np.eye(3),True))
sq=np.load(root/'work/sharp_square_model.npz');ell,fac=sq['ell'],sq['fac'];T=np.linalg.inv(ell.reshape(2,2).T)@np.array([[0.,-1.],[1.,0.]]);W=np.array([[T[0,0],T[0,1],0],[0,T[0,0],T[0,1]],[T[1,0],T[1,1],0],[0,T[1,0],T[1,1]]]);AA=[h.b.var(4,i) for i in range(4)];L=h.b.add(*(h.b.scale(P,v) for P,v in zip(AA,ell)));det=h.b.add(h.b.mul(AA[0],AA[3]),h.b.scale(h.b.mul(AA[1],AA[2]),-1));roc=json.loads((root/'work/sharp_square_explore.json').read_text())['directional_ROC_boundary_proposals']
for idx in (0,16):
 angle=roc[idx]['cubic_angle'];co=np.array([np.cos(angle),np.sin(angle)])@fac;MM=h.b.add(*(h.b.scale(P,v) for P,v in zip(AA,co[:4])));q=h.b.add(h.b.scale(h.b.mul(L,MM),2),h.b.scale(det,co[4]));nu=roc[idx]['necessary_nu_numerical']*1.0001;poly=h.b.add(h.F,h.b.scale(h.b.mul(q,q),-1/(4*nu)));cases.append((f'square_tangent_{idx}',tensor(poly,4),W,False))
def evaluate(x,TT,embed,beta,grad=True):
 co=x[:nc];B=x[nc:].reshape(2,2);H=np.einsum('nkij,k->nij',bh,co);rawm=np.einsum('ai,nab,bj->nij',B,H,B);raw=np.column_stack([rawm[:,0,0],rawm[:,0,1],rawm[:,1,1]]);sigma=np.mean(np.sum(raw*raw*metric,axis=1)**2)**.25
 if sigma<1e-14:return 1e10,np.zeros_like(x),None
 rr=raw/sigma;G=rr@embed.T;S=rr.T@rr/N;sev=np.linalg.eigvalsh(S)
 if sev[0]<1e-15:return 1e10,np.zeros_like(x),None
 f=float(np.einsum('ijkl,ni,nj,nk,nl->',TT,G,G,G,G,optimize=True)/N);v=4*np.einsum('ijkl,nj,nk,nl->i',TT,G,G,G,optimize=True)/N;HH=12*np.einsum('ijkl,nk,nl->ij',TT,G,G,optimize=True)/N
 try:M=-la.solve(HH,v,assume_a='pos',check_finite=False)
 except la.LinAlgError:return 1e10,np.zeros_like(x),None
 if np.linalg.norm(M)>1e5:return 1e10,np.zeros_like(x),None
 val=float(f+v@M+M@HH@M/2);obj=val-beta*np.linalg.slogdet(S)[1]
 if grad:
  gG=(4*np.einsum('ijkl,nj,nk,nl->ni',TT,G,G,G,optimize=True)+12*np.einsum('ijkl,nj,nk,l->ni',TT,G,G,M,optimize=True)+12*np.einsum('ijkl,nj,k,l->ni',TT,G,M,M,optimize=True))/N;gr=gG@embed-2*beta*(rr@np.linalg.inv(S))/N;gr=(gr-np.sum(gr*rr)*np.sum(rr*rr*metric,axis=1)[:,None]*rr*metric/N)/sigma;gk=np.zeros((N,2,2));gk[:,0,0]=gr[:,0];gk[:,0,1]=gk[:,1,0]=gr[:,1]/2;gk[:,1,1]=gr[:,2];gH=np.einsum('ia,nab,jb->nij',B,gk,B);gc=np.einsum('nij,nkij->k',gH,bh);gb=np.einsum('nia,ab,nbj->ij',H,B,gk+gk.transpose(0,2,1));gg=np.r_[gc,gb.ravel()]
 else:gg=None
 return obj,gg,{'energy':val,'mean':M.tolist(),'covariance_eigenvalues':sev.tolist(),'quartic_moment':f,'domain_matrix':B.tolist()}
history=[];best=None
for name,TT,embed,admitted in cases:
 local=None
 for restart in range(7):
  coeff=rng.normal(size=nc)/(1+np.repeat(np.linalg.norm(freq,axis=1),2))**.75;B=np.eye(2)+rng.normal(size=(2,2))*.25;x=np.r_[coeff,B.ravel()]
  for beta in (1e-4,1e-5,0.):
   opt=minimize(lambda z:evaluate(z,TT,embed,beta)[:2],x,jac=True,method='L-BFGS-B',options={'maxiter':350,'ftol':1e-12,'gtol':2e-8,'maxls':30});x=opt.x;_,_,state=evaluate(x,TT,embed,beta,False)
   if state is None:continue
   rec={'case':name,'seed_has_exact_ROC_receipt':admitted,'restart':restart,'barrier':beta,'iterations':int(opt.nit),**state};history.append(rec)
   if local is None or state['energy']<local['energy']:local={'energy':state['energy'],'field_parameters':x.tolist(),'row':rec}
   if best is None or state['energy']<best['energy']:best={'case':name,**local}
   if state['energy']<-1e-6:
    (root/'work/dense_constrained_search.json').write_text(json.dumps({'history':history,'best':best,'frequencies':freq.tolist(),'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n');raise SystemExit('Strict numerical negative: exact compatible-field and global admission checks required.')
  print(json.dumps({'case':name,'restart':restart,'best_energy':None if local is None else local['energy'],'last_state':state}),flush=True)
  (root/'work/dense_constrained_search.json').write_text(json.dumps({'history':history,'best':best,'frequencies':freq.tolist(),'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
