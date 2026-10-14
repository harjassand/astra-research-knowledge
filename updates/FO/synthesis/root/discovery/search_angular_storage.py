"""Exploratory homogeneous rational storage search, not a positivity proof.

Own derivation of the opposite-carrier averaged quartic; finite angular/velocity
LP constraints and bounded differential-evolution countertests are discovery.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import linprog,differential_evolution
OUT=Path(__file__).resolve().parent
START=time.monotonic()

def lagrangian(theta,p,q):
 r,s=np.cos(theta),np.sin(theta)
 eu2=p**4+q**4+4*p*p*q*q
 ev2=r**4+s**4+4*r*r*s*s
 euv=(p*p+q*q)*(r*r+s*s)-2*r*s*p*q
 ew2=(r*q+s*p)**2/2
 eju=r*p**3-s*q**3-2*s*p*p*q+2*r*p*q*q
 ejv=r**3*p-s**3*q-2*r*r*s*q+2*s*s*r*p
 L=(107/24)*eu2+3*ev2+19*euv-13*ew2-(29/2)*eju-12*ejv
 N=eu2+ev2+2*euv
 return L,N

def feature(theta,p,q,K):
 rho=np.cos(theta)*p+np.sin(theta)*q
 omega=np.cos(theta)*q-np.sin(theta)*p
 return np.stack([4*np.cos(2*k*theta)*rho-2*k*np.sin(2*k*theta)*omega for k in range(K+1)],axis=-1)

tt,rr,aa=np.meshgrid(np.linspace(0,np.pi/2,33),np.r_[np.linspace(0,4,17),8,16],np.linspace(0,2*np.pi,33)[:-1],indexing='ij')
theta=tt.ravel();p=(rr*np.cos(aa)).ravel();q=(rr*np.sin(aa)).ravel()
L,N=lagrangian(theta,p,q)
rows=[]
for K in [2,3,4,6,8]:
 f=feature(theta,p,q,K);A=np.c_[f,N];b=L.copy();history=[]
 for iteration in range(10):
  lp=linprog(np.r_[np.zeros(K+1),-1],A_ub=A,b_ub=b,bounds=[(-100,100)]*(K+1)+[(-3,1)],method='highs')
  if not lp.success:
   history.append(dict(iteration=iteration,lp_status=lp.message));break
  coeff,eta=lp.x[:-1],lp.x[-1]
  def margin(x):
   th,pp,qq=x;ll,nn=lagrangian(th,pp,qq)
   return float(ll-feature(th,pp,qq,K)@coeff-eta*nn)
  opt=differential_evolution(margin,[(0,np.pi/2),(-12,12),(-12,12)],seed=20261015+K+iteration,popsize=12,maxiter=140,tol=1e-10,polish=True,workers=1)
  history.append(dict(iteration=iteration,eta=float(eta),coefficients=coeff.tolist(),minimum_found=float(opt.fun),candidate=opt.x.tolist(),lp_sample_count=len(b)))
  print(json.dumps(dict(K=K,iteration=iteration,eta=float(eta),minimum_found=float(opt.fun))),flush=True)
  if opt.fun>=-1e-7:break
  th,pp,qq=opt.x;ll,nn=lagrangian(th,pp,qq)
  A=np.vstack([A,np.r_[feature(th,pp,qq,K),nn]]);b=np.r_[b,ll]
 rows.append(dict(harmonic_degree=K,history=history))
report=dict(scope='Finite sampled discovery only; no global positivity,PSD,all-width or quasiconvexity certificate. Angular ansatz P=R^4 sum c_k cos(2k theta),quarticpolynomials atK<=2 and rationalhomogeneous candidates above.',seed_base=20261015,initial_samples=len(L),velocity_box_countertest=12,seconds=time.monotonic()-START,cases=rows)
(OUT/'ANGULAR_STORAGE_SEARCH.json').write_text(json.dumps(report,indent=2)+'\n')
print('Saved exploratory angular storage search',flush=True)
