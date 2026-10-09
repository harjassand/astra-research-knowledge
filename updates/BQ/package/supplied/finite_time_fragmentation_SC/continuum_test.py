"""Independent off-lattice tagged-fragment simulation and sensitivity checks."""
import json,time
import numpy as np
from scipy.stats import beta
from fragment_inverse import endpoint,invert,invert_mp,fit_endpoint
from test_fragment_inverse import make_kernel


def simulate_continuous(samples,t,gamma,a,rng,initial_sigma=0.):
    # Each independent mass tag has jump ratio Beta(a+1,a), from binary
    # number-daughter distribution 2 Beta(a,a). No lattice forward model.
    s=np.maximum(0,rng.normal(0,initial_sigma,samples)) if initial_sigma else np.zeros(samples)
    initial=s.copy()
    timeleft=np.full(samples,t)
    live=np.arange(samples)
    generations=np.zeros(samples,dtype=np.int16)
    while len(live):
        wait=rng.exponential(size=len(live))*np.exp(gamma*s[live])
        jump=wait<timeleft[live]
        ix=live[jump]
        timeleft[ix]-=wait[jump]
        s[ix]-=np.log(rng.beta(a+1,a,len(ix)))
        generations[ix]+=1
        live=ix
    return s,generations,initial


def main():
    rng=np.random.default_rng(80164)
    result={'seed':80164,'continuous_mc':[],'rate_error':[],'replicated_noise':[],
            'precision_repair':[],'unknown_rate_alias':[]}
    t=2.;gamma=1.3;a=3.;samples=4_000_000
    st=time.perf_counter()
    s,g,_=simulate_continuous(samples,t,gamma,a,rng)
    result['mc_seconds']=time.perf_counter()-st
    result['mc_multigeneration_fraction']=float(np.mean(g>=2))
    for h in [.16,.08,.04,.02]:
        n=round(4/h)+1;q=np.exp(-gamma*h)
        idx=np.floor(s/h+.5).astype(int)
        f=np.bincount(idx,minlength=n)[:n]/samples
        f[0]=np.exp(-t) # Known intact atom; exclude sub-resolution jump bin.
        k=make_kernel(n,h,a)
        kh,w=invert(f,q,t)
        first=f/t;first[0]=0
        result['continuous_mc'].append({'h':h,'n':n,'l1':float(sum(abs(kh-k))),
            'positive_l1':float(sum(abs(np.maximum(kh,0)-k))),
            'short_time_l1':float(sum(abs(first-k))),
            'unresolved_jump_mass':float(1-beta.cdf(np.exp(-h/2),a+1,a)),
            'Wmax':float(max(w))})
    # Rate uncertainty is a separate, material source of error.
    h=.08;n=49;q=np.exp(-gamma*h);k=make_kernel(n,h,a);f=endpoint(k,q,t)
    for relative in [-.1,-.02,.02,.1]:
        kh,w=invert(f,np.exp(-(1+relative)*gamma*h),t)
        result['rate_error'].append({'gamma_relative_error':relative,
             'kernel_l1':float(sum(abs(kh-k))),'min_recovered':float(min(kh))})
    # Dense positive prefix plus an unobserved tail gives exact gamma aliases.
    k=np.r_[0.,rng.dirichlet(np.ones(59)*2)*.8]
    q=.93;f=endpoint(k,q,t)
    for qr in [.925,.93,.935]:
        kh,w=invert(f,qr,t)
        pred=endpoint(kh,qr,t)
        result['unknown_rate_alias'].append({'q':qr,'min_kernel':float(min(kh[1:])),
            'prefix_mass':float(sum(kh)),'forward_residual':float(max(abs(pred-f)))})
    # Test both normal and adverse representation-conditioning cases.
    for q in [.9,.99,.999]:
        k=np.r_[0.,rng.dirichlet(np.ones(50))];f=endpoint(k,q,4.)
        kh,w=invert(f,q,4.)
        km,wm=invert_mp(f,q,4.,dps=100)
        result['precision_repair'].append({'q':q,'double_error':float(max(abs(kh-k))),
          'high_precision_error':float(max(abs(km-k))),'Wmax':wm})
    # Replicates at realistic Poissonized count scales, same exact forward model
    # and data for direct inversion and a constrained full-likelihood baseline.
    h=.08;n=49;gamma=1.3;q=np.exp(-gamma*h);k=make_kernel(n,h,a)
    for t in [.5,2.,4.]:
      f=endpoint(k,q,t)
      for samples in [10_000,100_000]:
        metrics=[]
        for rep in range(20):
            obs=rng.poisson(f*samples)/samples;obs[0]=f[0]
            st=time.perf_counter();raw,w=invert(obs,q,t);directtime=time.perf_counter()-st
            direct=np.maximum(raw,0)
            st=time.perf_counter()
            fit,res,calls=fit_endpoint(obs,q,t,x0=direct,maxiter=350,likelihood='poisson')
            fittime=time.perf_counter()-st
            first=obs/t;first[0]=0
            metrics.append([sum(abs(direct-k)),sum(abs(fit-k)),sum(abs(first-k)),
                 directtime,fittime,calls,float(res.success)])
        metrics=np.array(metrics)
        result['replicated_noise'].append({'t':t,'samples':samples,'replicates':20,
          'direct_l1_mean':float(metrics[:,0].mean()),
          'fit_l1_mean':float(metrics[:,1].mean()),
          'short_time_l1_mean':float(metrics[:,2].mean()),
          'direct_l1_sd':float(metrics[:,0].std()),
          'fit_l1_sd':float(metrics[:,1].std()),
          'direct_sec_median':float(np.median(metrics[:,3])),
          'fit_sec_median':float(np.median(metrics[:,4])),
          'fit_calls_mean':float(metrics[:,5].mean()),
          'fit_success_count':int(metrics[:,6].sum())})
        print(result['replicated_noise'][-1],flush=True)
    with open('continuum_results.json','w') as fh:json.dump(result,fh,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='replicated_noise'},indent=2))

if __name__=='__main__':main()
