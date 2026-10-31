"""Boundary-derived actual rank-three search on unmodified J_r.

Covariance-rank-three gradients with an invertible annihilator are
exactly T Hess psi. Output rotation and scale reduce T to a signed
SPD determinant-one matrix with two real parameters. The mean Hessian
is positive definite on this class even though the 4x4 covariance is
singular. No full-covariance barrier is imposed.
Numerical diagnostics only; any negative requires exact receipt.
normalized_gap means Delta_Jr(M_opt,G)/<J_r(G)> throughout.
The quartic_moment field is <J_r(G)>, not <|G|^4>.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product,permutations
import sys,json,time
import numpy as np
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/quartic_coupling'));import receive as m
rng=np.random.default_rng(721619);start=time.perf_counter();freq=np.array([(i,j) for i,j in product(range(-3,4),repeat=2) if i>0 or i==0 and j>0]);grid=np.array(list(product(np.arange(16)*2*np.pi/16,repeat=2)));N=len(grid);basis=[]
for k in freq:
 H=np.outer(k,k)/(k@k)
 for wave in (np.cos(grid@k),np.sin(grid@k)):basis.append(wave[:,None,None]*H)
basis=np.array(basis);nc=len(basis)
def tensor(P):
 out=np.zeros((4,)*4)
 for pw,c in P.items():
  ids=tuple(i for i,n in enumerate(pw) for _ in range(n));perms=set(permutations(ids))
  for idx in perms:out[idx]=float(c)/len(perms)
 return out
def evaluate(x,TT,orientation,beta,grad=True):
 co=x[:nc];tt,ss=x[-2:];et=np.exp(tt);P=np.array([[et,ss],[ss,(1+ss*ss)/et]]);D=np.diag([1.,float(orientation)]);T=D@P;H=np.einsum('k,knij->nij',co,basis);hh=np.column_stack([H[:,0,0],H[:,0,1],H[:,1,1]]);S=hh.T@hh/N;sev=np.linalg.eigvalsh(S)
 if sev[0]<1e-13:return 1e8,np.zeros_like(x),None
 raw=np.einsum('ij,njk->nik',T,H).reshape(N,4);sigma=np.mean(np.sum(raw*raw,axis=1)**2)**.25
 if sigma<1e-14:return 1e8,np.zeros_like(x),None
 G=raw/sigma;f=float(np.einsum('ijkl,ni,nj,nk,nl->',TT,G,G,G,G,optimize=True)/N);v=4*np.einsum('ijkl,nj,nk,nl->i',TT,G,G,G,optimize=True)/N;HH=12*np.einsum('ijkl,nk,nl->ij',TT,G,G,optimize=True)/N;he=np.linalg.eigvalsh(HH)
 if he[0]<=1e-14 or f<=1e-15:return 1e8,np.zeros_like(x),None
 M=-np.linalg.solve(HH,v)
 if np.linalg.norm(M)>1e8:return 1e8,np.zeros_like(x),None
 energy=float(f+v@M+M@HH@M/2);ratio=energy/f;obj=ratio-beta*np.linalg.slogdet(S)[1]
 if grad:
  gf=4*np.einsum('ijkl,nj,nk,nl->ni',TT,G,G,G,optimize=True)/N;ga=gf+12*np.einsum('ijkl,nj,nk,l->ni',TT,G,G,M,optimize=True)/N+12*np.einsum('ijkl,nj,k,l->ni',TT,G,M,M,optimize=True)/N;gg=(ga-ratio*gf)/f;graw=(gg-np.sum(gg*G)*np.sum(G*G,axis=1)[:,None]*G/N)/sigma;graw=graw.reshape(N,2,2);gh=np.einsum('ji,njk->nik',T,graw);gc=np.einsum('nij,knij->k',gh,basis);bar=-2*beta*(hh@np.linalg.inv(S))/N;gbarm=np.zeros_like(H);gbarm[:,0,0]=bar[:,0];gbarm[:,0,1]=gbarm[:,1,0]=bar[:,1]/2;gbarm[:,1,1]=bar[:,2];gc+=np.einsum('nij,knij->k',gbarm,basis);dT=[D@np.array([[et,0],[0,-(1+ss*ss)/et]]),D@np.array([[0,1],[1,2*ss/et]])];gt=[float(np.einsum('nij,ik,nkj->',graw,A,H)) for A in dT];gout=np.r_[gc,gt]
 else:gout=None
 return obj,gout,{'normalized_gap':ratio,'energy_gap':energy,'quartic_moment':f,'mean':M.tolist(),'Hessian_covariance_eigenvalues':sev.tolist(),'mean_matrix_eigenvalues':he.tolist(),'plane_parameters':[float(tt),float(ss)],'plane_matrix':T.tolist(),'coefficient_norm':float(np.linalg.norm(co))}
history=[];best=None;checks=[]
for rr in (R(3,4),R(1,10),R(2)):
 F=m.J(rr,[m.var(4,i) for i in range(4)]);TT=tensor(F)
 for orient in (1,-1):
  for restart in range(2):
   co=rng.normal(size=nc)/(1+np.repeat(np.linalg.norm(freq,axis=1),2));co/=np.linalg.norm(co);x=np.r_[co,[.5*np.log(float(rr+1)),0.] if restart==0 else rng.normal(size=2)*.6]
   if not checks:
    value,g,state=evaluate(x,TT,orient,1e-3);assert state is not None
    for j in (0,19,nc,nc+1):
     xp=x.copy();xm=x.copy();xp[j]+=1e-5;xm[j]-=1e-5;fd=(evaluate(xp,TT,orient,1e-3,False)[0]-evaluate(xm,TT,orient,1e-3,False)[0])/2e-5;checks.append([j,float(fd),float(g[j])]);assert abs(fd-g[j])<2e-5*(1+abs(fd)),checks
    print('rank-three analytic gradients checked',flush=True)
   for beta in (1e-3,1e-5,0.):
    opt=minimize(lambda z:evaluate(z,TT,orient,beta)[:2],x,jac=True,method='SLSQP',bounds=[(None,None)]*nc+[(-3,3),(-4,4)],constraints=[{'type':'eq','fun':lambda z:float(z[:nc]@z[:nc]-1),'jac':lambda z:np.r_[2*z[:nc],[0.,0.]]}],options={'maxiter':300,'ftol':1e-12});x=opt.x;x[:nc]/=np.linalg.norm(x[:nc]);_,_,state=evaluate(x,TT,orient,beta,False)
    if state is None:continue
    rec={'r':str(rr),'orientation':orient,'restart':restart,'barrier':beta,'iterations':int(opt.nit),'solver_success':bool(opt.success),'solver_message':str(opt.message),**state};history.append(rec)
    if best is None or state['normalized_gap']<best['normalized_gap']:best={'r':str(rr),'orientation':orient,'normalized_gap':state['normalized_gap'],'parameters':x.tolist(),'row':rec}
    print(json.dumps(rec),flush=True);(root/'work/n901_rank3_boundary_search.json').write_text(json.dumps({'history':history,'best':best,'frequencies':freq.tolist(),'scalar_coefficients':nc,'plane_shape_parameters':2,'analytic_gradient_checks':checks,'mean_inverse_admission':'actual covariance rank three implies positive definite mean matrix, by singular_mean/PROOF.txt','normalized_gap_definition':'Delta_Jr(M_opt,G) / <J_r(G)>','quartic_moment_definition':'<J_r(G)>; this field is not <|G|^4>','parameter_bounds':{'t':[-3,3],'s':[-4,4]},'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
    if state['normalized_gap']<-1e-6:raise SystemExit('Strict actual numerical candidate: exact receipt required.')
