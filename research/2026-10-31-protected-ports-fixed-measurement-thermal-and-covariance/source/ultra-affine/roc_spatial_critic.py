"""Adaptive spatial ROC proposals with lossless output-angle Grams.

The output quantifier is represented exactly by 14-dimensional SOS.
Spatial searches below are numerical critics, not global admission.
"""
from pathlib import Path
from fractions import Fraction as R
import sys,time,json
import numpy as np,scipy.linalg as la,cvxpy as cp
from scipy.optimize import minimize_scalar
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import roc_output_sos as so
m=so.m
MP=[];GP=[];QP=[]
for side in (0,1):
 TOP,CC,QQ=m.charts[2*side];ma=np.zeros((4,4,3));ga=np.zeros((4,4,12,3));qa=np.zeros((3,9,3))
 for i,row in enumerate(TOP):
  for j,P in enumerate(row):
   for (u,t),v in P.items():
    if u==0:ma[i,j,t]=float(v)
 for c,col in enumerate(CC):
  for i,P in enumerate(col):
   for (u,t),v in P.items():ga[u,i,c,t]=float(v)
 for j,P in enumerate(QQ):
  for (u,t),v in m.divide_norm(P).items():qa[u,j,t]=float(v)
 MP.append(ma);GP.append(ga);QP.append(qa)

def atf(side,t):
 pp=np.array([1.,t,t*t]);return MP[side]@pp,GP[side]@pp,QP[side]@pp
def binary_minimum(p):
 pp=np.pad(p,(0,max(0,7-len(p))))[:7];der=np.polynomial.polynomial.polysub(np.polynomial.polynomial.polymul(np.polynomial.polynomial.polyder(pp),[1,0,1]),np.polynomial.polynomial.polymul(pp,[0,6]));der=np.trim_zeros(der,'b');roots=np.polynomial.polynomial.polyroots(der) if len(der)>1 else [];xs=[float(z.real) for z in roots if abs(z.imag)<1e-7*(1+abs(z.real))];vals=[(float(np.polynomial.polynomial.polyval(x,pp)/(1+x*x)**3),x) for x in xs]+[(float(pp[-1]),float('inf')),(float(pp[0]),0.)];return min(vals,key=lambda q:q[0])
def slack(side,t,c,q,detail=False):
 M,G,Q=atf(side,t);gg=np.einsum('kij,j->ki',G,c);qq=Q@q;Mi=la.inv(M);p=np.pad(np.polynomial.polynomial.polymul(qq,[1,0,2,0,1]),(0,0))
 for i in range(4):
  for j in range(4):p-=Mi[i,j]*np.polynomial.polynomial.polymul(gg[:,i],gg[:,j])
 val,u=binary_minimum(p);return (val/(1+t*t),u) if detail else val/(1+t*t)
def critic(c,q):
 candidates=[]
 for side in (0,1):
  ts=np.unique(np.concatenate((np.linspace(-1,1,129),[-.385371,.385371,-1/.385371 if False else 0])));vals=[slack(side,t,c,q) for t in ts]
  for i,t in enumerate(ts):
   if i in (0,len(ts)-1):candidates.append((vals[i],side,float(t),slack(side,t,c,q,True)[1]))
   elif vals[i]<=vals[i-1] and vals[i]<=vals[i+1]:
    opt=minimize_scalar(lambda x:slack(side,x,c,q),bounds=(float(ts[i-1]),float(ts[i+1])),method='bounded',options={'xatol':1e-12});candidates.append((float(opt.fun),side,float(opt.x),slack(side,opt.x,c,q,True)[1]))
 return min(candidates),sorted(candidates)

class Model:
 def __init__(self):
  self.c=cp.Variable(12);self.q=cp.Variable(9);self.ell=cp.Parameter(12);self.qmom=cp.Parameter(9);self.constraints=[cp.norm(self.c,'inf')<=1e6,cp.norm(self.q,'inf')<=1e9];self.points=set();self.states=[]
  for side in (0,1):
   for t in (-1.,-.75,-.5,-.385371,-.25,0.,.25,.5,.75,1.):self.add(side,R(str(t)))
 def add(self,side,t):
  t=R(t);key=(side,t)
  if key in self.points:return
  self.points.add(key);M,G,Q=so.at(side,t);con,state=so.gram(M,G,Q,self.c,self.q);self.constraints.append(con);self.states.append((side,t,state))
 def solve(self,ell,qmom,maxcuts=8):
  self.ell.value=np.array(ell,float);self.qmom.value=np.array(qmom,float);history=[]
  for iteration in range(maxcuts):
   prob=cp.Problem(cp.Minimize(self.ell@self.c+self.qmom@self.q),self.constraints);prob.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_gap_rel=1e-8,tol_feas=1e-9,max_iter=250)
   if self.c.value is None:return None
   c=np.array(self.c.value);q=np.array(self.q.value);worst,candidates=critic(c,q);hist={'cut_iteration':iteration,'points':len(self.points),'minimum_numerical_spatial_slack':worst[0],'side':worst[1],'t':worst[2],'output_projective_t':worst[3]};history.append(hist);print(json.dumps(hist),flush=True)
   out={'objective':float(prob.value),'cubic_coordinates':c.tolist(),'quadratic_coordinates':q.tolist(),'status':prob.status,'spatial_critic_history':history,'scope':'Spatial ROC is NOT rigorously admitted by this numerical critic. Output-angle SOS is lossless at every sampled spatial direction.'}
   if worst[0]>-1e-7:return out
   for val,side,t,u in candidates[:4]:
    if val<-1e-7:self.add(side,R(round(t*10**10),10**10))
  return out

if __name__=='__main__':
 # Load actual-gradient moment and derivative helpers without starting the
 # earlier coarse-cone experiment again.
 ss=(root/'work/actual_frontier_search.py').read_text();ns={'__file__':str(root/'work/actual_frontier_search.py'),'__name__':'actual_helpers'};exec(ss[:ss.index('rng=np.random')],ns)
 field,moments,stats,optimize=(ns[k] for k in ('field','moments','statistics','optimize'));C3,Q2=ns['C3'],ns['Q2'];old=json.loads((root/'work/actual_frontier_search.json').read_text());x=np.array(old['best']['parameters']);solver=Model();start=time.perf_counter();runs=[]
 for iteration in range(5):
  G=field(x);f,ell,qm=moments(G)
  try:p=solver.solve(ell,qm)
  except Exception as err:print('SOS fit failed',type(err).__name__,str(err),flush=True);break
  if p is None:break
  c=np.array(p['cubic_coordinates']);q=np.array(p['quadratic_coordinates']);C=np.einsum('s,sijk->ijk',c,C3);Q=np.einsum('s,sij->ij',q,Q2);before=stats(G,C,Q);opt=optimize(x,C,Q);x=opt.x;after=stats(field(x),C,Q);record={'iteration':iteration,'fit_energy':f+p['objective'],'before':before,'after':after,'parameters':x.tolist(),'polynomial':p,'optimizer_iterations':opt.nit};runs.append(record);(root/'work/roc_spatial_frontier_search.json').write_text(json.dumps({'runs':runs,'scope':'Numerical spatial-critic search. No globally ROC-admitted separation is claimed.','seconds':time.perf_counter()-start},indent=2)+'\n');print(json.dumps({'iteration':iteration,'fit_energy':record['fit_energy'],'ratio_before':before['ratio'],'ratio_after':after['ratio'],'seconds':time.perf_counter()-start}),flush=True)
  if after['ratio']>1.00001:print('possible candidate needs exact global ROC and direct actual-field validation',flush=True);break
