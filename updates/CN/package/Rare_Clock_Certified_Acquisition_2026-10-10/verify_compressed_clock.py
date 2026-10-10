import math,json,time
import numpy as np
from compressed_brown import CompressedBrown
from poisson_clock import finite_cdf

rng=np.random.default_rng(314159265)
res={}
# A full-state reference where compression genuinely activates.
p=CompressedBrown([.03,.05,.07,.09],[.4,.8,1.7,3.])
mu=p.mean_reference();trials=5000
start=time.perf_counter();a=np.array([p.sample(rng,relative=.5,failure=.1)[:3] for _ in range(trials)])
res['compressed_vs_full_state']={'n':p.n,'q':p.q,'mean':mu,'trials':trials,'seconds':time.perf_counter()-start,'average_marks':float(a[:,1].mean()),'average_large_strata':float(a[:,2].mean()),'checks':[]}
for f in [.001,.01,.1,.3,1,3,10]:
    truth=finite_cdf(p.pi,p.lam,f*mu);emp=float(np.mean(a[:,0]<=f*mu))
    res['compressed_vs_full_state']['checks'].append({'time_over_mean':f,'truth':truth,'empirical':emp,'error':emp-truth})
# Explicit same-W coupling, exact large-stratum compound Poisson versus compressed output.
p=CompressedBrown([.04,.05,.05],[.7,1.,2.]);eps=.5;delta=.1;h=eps/(2+eps)
R=np.ceil(6*p.kappa/h**2*math.log(4*p.n/delta)).astype(int)
trials=1000;errors=[];large_count=0;exactdraws=0
start=time.perf_counter()
for _ in range(trials):
    W=rng.exponential()/p.q;truth=est=0.
    for i in range(p.n):
        r=p.w[i]*W;c=int(rng.poisson(r));exactdraws+=c
        raw=float(p.increments(i,c,rng).sum()) if c else 0.
        truth+=raw
        if r<R[i]:est+=raw
        else:
            large_count+=1;est+=r*float(p.increments(i,int(R[i]),rng).mean())
    errors.append(abs(est-truth)/truth if truth else (0 if est==0 else math.inf))
res['explicit_coupling']={'n':p.n,'q':p.q,'relative_bound':eps,'failure_bound':delta,'thresholds':R.tolist(),'trials':trials,'large_strata':large_count,'exact_reference_marks':exactdraws,'empirical_failure_fraction':float(np.mean(np.array(errors)>eps)),'relative_error_quantiles':np.quantile(errors,[.5,.9,.99,1.]).tolist(),'seconds':time.perf_counter()-start}
print(json.dumps(res,indent=2))
