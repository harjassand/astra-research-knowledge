import json,time
import numpy as np
from fragment_inverse import (endpoint,invert,uniformized_forward,fit_uniformized,
                              fit_endpoint,forward_recurrence)
from test_fragment_inverse import make_kernel

def main():
    rng=np.random.default_rng(745108)
    n=40;q=.92;t=2.;k=np.r_[0.,rng.dirichlet(np.ones(n-1))]
    exact=endpoint(k,q,t);d=rng.normal(size=n)
    pred,g=uniformized_forward(k,q,t,gradient=d)
    gf=[]
    for j in range(1,n):
        e=np.zeros(n);e[j]=1e-6
        gf.append(d@(endpoint(k+e,q,t)-endpoint(k-e,q,t))/(2e-6))
    result={'seed':745108,'uniformized_forward_error':float(max(abs(exact-pred))),
        'uniformized_gradient_error':float(max(abs(g[1:]-gf))),
        'matched_noise':[],'scale':[],'general_initial':[]}
    for t in [.5,2.,4.]:
      n=49;h=.08;q=np.exp(-1.3*h);k=make_kernel(n,h);f=endpoint(k,q,t)
      for samples in [10000,100000]:
        values=[]
        for rep in range(20):
            obs=rng.poisson(f*samples)/samples;obs[0]=f[0]
            st=time.perf_counter();raw,w=invert(obs,q,t);dt=time.perf_counter()-st
            clipped=np.maximum(raw,0)
            st=time.perf_counter();kh,res,calls=fit_uniformized(obs,q,t,x0=clipped);ft=time.perf_counter()-st
            # Baseline gets the proposed inverse as warm start. This is a strong
            # comparison for numerical likelihood accuracy, not claimed independent.
            values.append([sum(abs(clipped-k)),sum(abs(kh-k)),dt,ft,calls,res.success])
        values=np.array(values)
        result['matched_noise'].append({'t':t,'samples':samples,'replicates':20,
          'direct_l1_mean':float(values[:,0].mean()),'fit_l1_mean':float(values[:,1].mean()),
          'direct_sec_median':float(np.median(values[:,2])),
          'fit_sec_median':float(np.median(values[:,3])),
          'fit_calls_mean':float(values[:,4].mean()),'fit_successes':int(values[:,5].sum())})
        print(result['matched_noise'][-1],flush=True)
    # Absolute cost at larger resolution, exact lattice truth from a classical
    # matrix-free forward solver, no dense matrix or suggested inverse involved.
    for n in [65,129,257,513,1025]:
        h=4/(n-1);q=np.exp(-1.3*h);t=2.;k=make_kernel(n,h)
        f=uniformized_forward(k,q,t)
        obs=rng.poisson(f*100000)/100000;obs[0]=f[0]
        st=time.perf_counter();raw,w=invert(obs,q,t);dt=time.perf_counter()-st
        clipped=np.maximum(raw,0)
        st=time.perf_counter();kh,res,calls=fit_uniformized(obs,q,t,x0=clipped);ft=time.perf_counter()-st
        result['scale'].append({'n':n,'direct_sec':dt,'fit_sec':ft,'fit_calls':calls,
          'fit_success':bool(res.success),'direct_l1':float(sum(abs(clipped-k))),
          'fit_l1':float(sum(abs(kh-k))),'Wmax':float(max(w))})
        print(result['scale'][-1],flush=True)
    with open('fast_baseline_results.json','w') as fh:json.dump(result,fh,indent=2)

if __name__=='__main__':main()
