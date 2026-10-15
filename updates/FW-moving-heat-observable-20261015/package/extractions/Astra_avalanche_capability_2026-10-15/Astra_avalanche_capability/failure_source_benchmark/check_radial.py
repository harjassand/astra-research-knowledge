"""Classical Gamma/Dirichlet Rao-Blackwell identity on actual avalanche model.
Pilot threshold selection is independent of reported production samples.
"""
import json,time
import numpy as np
from scipy.special import gammainc
from pathlib import Path
from verify_avalanche_clock import clock
rows=[]
for n,M,pilot in [(100,50000,5000),(1000,10000,2000)]:
 h=np.sort(np.random.RandomState(0).uniform(size=n));f0=.175;T=.15
 invlambda=np.exp(h/T);rng=np.random.default_rng(2026101503+n)
 p=np.array([clock(h,f0,T,E=rng.exponential(size=n)*invlambda)[0] for _ in range(pilot)])
 deadline=float(np.quantile(p,.01))
 rng=np.random.default_rng(2026101504+n)
 plain=[];rb=[];err=0.
 a=time.perf_counter()
 for j in range(M):
  X=rng.exponential(size=n);R=X.sum();t,_=clock(h,f0,T,E=X*invlambda)
  plain.append(float(t<=deadline))
  # Positive homogeneity: tau(V/lambda)=tau(X/lambda)/R.
  rb.append(float(gammainc(n,deadline*R/t)) if t>0 else 1.)
 elapsed=time.perf_counter()-a
 plain=np.array(plain);rb=np.array(rb)
 # Timing separates core path kernel from added special-function cost.
 r2=np.random.default_rng(1712);a=time.perf_counter()
 for j in range(1000):clock(h,f0,T,E=r2.exponential(size=n)*invlambda)
 plain_elapsed=time.perf_counter()-a
 a=time.perf_counter()
 for j in range(1000):
  X=r2.exponential(size=n);R=X.sum();t,_=clock(h,f0,T,E=X*invlambda);gammainc(n,deadline*R/t)
 rb_elapsed=time.perf_counter()-a
 # Check homogeneity explicitly on independently selected paths.
 for j in range(30):
  X=r2.exponential(size=n);R=X.sum();t,_=clock(h,f0,T,E=X*invlambda);v,_=clock(h,f0,T,E=X/R*invlambda)
  err=max(err,abs(t-R*v)/max(1,t))
 vp=float(plain.var(ddof=1));vr=float(rb.var(ddof=1))
 rows.append({'n':n,'f0':f0,'T':T,'strength_seed':0,'pilot_n':pilot,'pilot_quantile':.01,'deadline':deadline,'N':M,'plain_mean':float(plain.mean()),'rb_mean':float(rb.mean()),'plain_SE':(vp/M)**.5,'rb_SE':(vr/M)**.5,'variance_reduction':vp/vr,'plain_1000_seconds':plain_elapsed,'rb_1000_seconds':rb_elapsed,'matched_cost_efficiency':vp*plain_elapsed/(vr*rb_elapsed),'production_seconds':elapsed,'homogeneity_max_relative_error':err})
 print(rows[-1],flush=True)
 Path(__file__).with_name('radial_results.json').write_text(json.dumps(rows,indent=2))
