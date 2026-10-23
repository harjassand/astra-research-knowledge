"""Bounded random-time destructive-pair identification; NumPy only.
All observations are fresh synthetic independent families, not physical measurements.
"""
from pathlib import Path
from fractions import Fraction
import json,time,numpy as np
ROOT=Path(__file__).resolve().parent
J=np.array([[0.,-1.],[1.,0.]])

def sample(N,a,omega,L,rng,clock='uniform'):
 if clock=='uniform':t=rng.uniform(0,L,N)
 else:
  parts=[];left=N
  while left:
   x=rng.uniform(0,L,max(2*left,64));z=x[rng.uniform(size=len(x))<np.sin(np.pi*x/L)**2][:left];parts.append(z);left-=len(z)
  t=np.concatenate(parts)
 G0=np.array([[.8,.1],[-.05,.7]])
 u=rng.normal(size=(N,2));v0=u@G0.T+rng.normal(size=(N,2))@np.linalg.cholesky(np.eye(2)-G0@G0.T).T
 co,si=np.cos(omega*t),np.sin(omega*t);rot=np.column_stack([co*v0[:,0]+si*v0[:,1],-si*v0[:,0]+co*v0[:,1]])
 v=np.exp(-a*t)[:,None]*rot+np.sqrt(1-np.exp(-2*a*t))[:,None]*rng.normal(size=(N,2))
 return t,u+rng.normal(size=(N,2))*np.sqrt([.1,.2]),v+rng.normal(size=(N,2))*np.sqrt([.2,.1])

def sigma_lower_stored(M):
 q=[[Fraction.from_float(float(x)) for x in r] for r in M];det=q[0][0]*q[1][1]-q[0][1]*q[1][0];f=sum(x*x for r in q for x in r)
 if det==0:return 0.
 s=Fraction.from_float(float(abs(det))/float(np.sqrt(float(f)))*(1-1e-12))
 while s*s*f>det*det:s/=2
 return float(s)

def weak(t,u,v,L,clock='uniform',confidence=False):
 if clock=='uniform':w0=2*np.sin(np.pi*t/L)**2;w1=(2*np.pi/L)*np.sin(2*np.pi*t/L)
 else:w0=np.ones(len(t));w1=(2*np.pi/L)/np.tan(np.pi*t/L)
 start=max(1000,len(t)//10) if confidence else 0
 M0=(w0[start:,None]*v[start:]).T@u[start:]/(len(t)-start);M1=(w1[start:,None]*v[start:]).T@u[start:]/(len(t)-start)
 try:F=M1@np.linalg.inv(M0)
 except np.linalg.LinAlgError:return None,{'decision':'ABSTAIN; singular matrix'}
 detail={'sigma0_float':float(np.linalg.svd(M0,compute_uv=False)[-1]),'M0':M0.tolist(),'M1':M1.tolist()}
 if confidence:
  alpha_p,alpha_m=.01,.04;n=2;delta=np.sqrt(8*np.log(4*n/alpha_p)/start)
  if delta>=1:return F,{**detail,'decision':'ABSTAIN; pilot too small'}
  umax=float(np.max(np.mean(u[:start]**2,axis=0))/(1-delta));vmax=float(np.max(np.mean(v[:start]**2,axis=0))/(1-delta));N=len(t)-start;h=np.log(4*n*n/alpha_m)
  base=np.sqrt(umax*vmax)*(np.sqrt(6*h/N)+2*h/N);e0=n*2*base;e1=n*(2*np.pi/L)*base;s=sigma_lower_stored(M0)
  residual=float(np.linalg.norm(F@M0-M1,'fro'))
  radius=(residual+e1+np.linalg.norm(F,2)*e0)/(s-e0) if s>e0 else None
  detail.update(decision='PASS_CONDITIONAL_MODEL_BOUND' if radius is not None else 'ABSTAIN',radius_F=radius,epsilon0=e0,epsilon1=e1,sigma_lower_stored_binary=s,pilot_pairs=start,total_pairs=len(t),u_variance_upper=umax,v_variance_upper=vmax,coverage='Analytic 95% under known zero means, iid families jointly Gaussian conditional on time, stationary Gaussian marginal laws independent of time, exact clock and linear conditional mean. Stored matrix singular lower checked with exact binary-rational determinant; Gaussian simulation and moment arithmetic are floating diagnostics, not formal verification.')
 return F,detail

def conventional(t,u,v):
 """Variable-projection timestamp regression, same aI+omegaJ model for both fits.
 Coarse multistart uses a subset; final refinement uses every pair. No true F or G0 supplied.
 """
 evaluations=0
 def objective(a,w,tt,uu,vv):
  nonlocal evaluations;evaluations+=1
  q=np.exp(-a*tt);co,si=np.cos(w*tt),np.sin(w*tt);y=np.column_stack([co*vv[:,0]-si*vv[:,1],si*vv[:,0]+co*vv[:,1]])
  Q=(q[:,None]*uu);N=Q.T@Q;R=y.T@Q
  try:G=np.linalg.solve(N,R.T).T
  except np.linalg.LinAlgError:return np.inf
  return float(np.sum(vv*vv)-np.sum(R*G))
 ix=np.linspace(0,len(t)-1,min(1500,len(t)),dtype=int);tt,uu,vv=t[ix],u[ix],v[ix]
 best=(np.inf,None,None)
 for a in np.linspace(.05,2,9):
  for w in np.linspace(-12,12,49):
   f=objective(a,w,tt,uu,vv)
   if f<best[0]:best=(f,a,w)
 a,w=best[1:];da,dw=.25,.5;f=objective(a,w,t,u,v)
 for _ in range(20):
  options=[(a,w),(max(.05,a-da),w),(min(2,a+da),w),(a,max(-12,w-dw)),(a,min(12,w+dw))];vals=[objective(x,y,t,u,v) for x,y in options];i=int(np.argmin(vals))
  if i==0:da*=.5;dw*=.5
  else:a,w=options[i];f=vals[i]
 return a*np.eye(2)+w*J,{'evaluations':evaluations,'a':a,'omega':w,'assumptions':'Known class F=aI+omegaJ, .05<=a<=2, |omega|<=12; unknown inherited response G fitted from the same data; conditional-mean nonlinear least squares, not an efficient likelihood claim.'}

def project(F):return np.clip(np.trace(F)/2,.05,2)*np.eye(2)+np.clip((F[1,0]-F[0,1])/2,-12,12)*J

def main():
 rng=np.random.default_rng(23102622);begin=time.perf_counter();rows=[]
 for omega in [1.5,8.]:
  true=.7*np.eye(2)+omega*J
  for N in [5000,50000]:
   rr=[]
   for k in range(6):
    t,u,v=sample(N,.7,omega,1.,rng);F,d=weak(t,u,v,1.,confidence=True);conv,cd=conventional(t,u,v)
    ts,us,vs=sample(N,.7,omega,1.,rng,'sine');score,sd=weak(ts,us,vs,1.,'sine')
    err=float(np.linalg.norm(F-true));rad=d.get('radius_F')
    rr.append({'weak_F_error':err,'weak_projected_error':float(np.linalg.norm(project(F)-true)),'conditional_regression_error':float(np.linalg.norm(conv-true)),'sine_score_projected_error':float(np.linalg.norm(project(score)-true)),'weak_confidence':d,'conditional_regression':cd,'confidence_covers_true':None if rad is None else bool(err<=rad)})
   row={'omega':omega,'a':.7,'pairs_per_protocol':N,'state_reads_per_protocol':2*N,'max_late_delay':1.,'expected_late_delay':.5,'replicates':rr,'RMS_weak_projected':float(np.sqrt(np.mean([x['weak_projected_error']**2 for x in rr]))),'RMS_conventional':float(np.sqrt(np.mean([x['conditional_regression_error']**2 for x in rr]))),'RMS_sine_score_projected':float(np.sqrt(np.mean([x['sine_score_projected_error']**2 for x in rr]))),'bound_passes':sum(x['weak_confidence']['decision'].startswith('PASS') for x in rr)};rows.append(row)
   print(json.dumps({k:v for k,v in row.items() if k!='replicates'}),flush=True)
 out={'status':'synthetic independently sampled destructive families; no physical assay','seed':23102622,'rows':rows,'wall_seconds':time.perf_counter()-begin,'known_means':'Both observed means supplied as zero for analytic confidence construction and both estimators. Unknown-mean extension requires cross-fit centering or independent-family differences.','important_limit':'Nonlinear/hidden state, inherited-rank failure, time-dependent selection, clock error and biological growth are not certified by a good fit.'};(ROOT/'paired_assay_results.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
