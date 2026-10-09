import json,time
import numpy as np
from scipy.linalg import expm,expm_frechet
from scipy.stats import beta
from fragment_inverse import generator,endpoint,invert,fit_endpoint


def make_kernel(n,h=0.08,a=3.):
    # Symmetric binary daughter law 2 Beta(a,a); mass-weighted tagged
    # daughter is Beta(a+1,a), hence these are log-jump bin probabilities.
    edges=np.exp(-h*(np.arange(n)+.5))
    edges=np.r_[1.,edges]
    k=beta.cdf(edges[:-1],a+1,a)-beta.cdf(edges[1:],a+1,a)
    # Top interval is not a no-jump event: exclude and report it explicitly.
    k[0]=0
    return k


def run():
    rng=np.random.default_rng(92715)
    out={'model':'mass-weighted lattice, known power-law rates',
         'seed':92715,'correctness':[],'matched_noise':[],'truncation':[]}
    # Exhaustive on many small, unrelated kernels and rates, compared with
    # a generic matrix exponential. Test repeated/no fragmentation limits.
    for n in [8,23,51]:
      for q in [.5,.93,.999]:
       for t in [.05,1.,4.]:
        k=np.r_[0.,rng.dirichlet(np.ones(n-1)*2)]
        f=endpoint(k,q,t)
        kh,w=invert(f,q,t,dtype=np.longdouble)
        err=float(np.max(abs(kh-k)))
        out['correctness'].append({'n':n,'q':q,'t':t,'maxerr':err,'Wmax':float(max(w))})
    # Verify the analytic Frechet adjoint gradient independently.
    n=12;q=.91;t=1.2
    k=np.r_[0.,rng.dirichlet(np.ones(n-1))]
    y=endpoint(k,q,t);target=y+rng.normal(0,.01,n)
    A=t*generator(k,q);e0=np.eye(n)[:,0];d=y-target;d[0]=0
    G=expm_frechet(A.T,np.outer(d,e0),compute_expm=False)
    ga=np.array([t*np.dot(q**np.arange(n-j),G[np.arange(j,n),np.arange(n-j)])
                 for j in range(1,n)])
    gf=[]
    for j in range(1,n):
        e=np.zeros(n);e[j]=1e-6
        yp=endpoint(k+e,q,t);ym=endpoint(k-e,q,t)
        gf.append((np.sum((yp[1:]-target[1:])**2)-np.sum((ym[1:]-target[1:])**2))/(4e-6))
    out['gradient_maxerr']=float(np.max(abs(ga-gf)))
    # Kernel observation range only: unknown fine-fragment tail; no artificial
    # equality normalization for either method. Match data/model and noise.
    n=49;h=.08;q=np.exp(-1.3*h);k=make_kernel(n,h)
    for t in [.15,.5,1.,2.,4.]:
      f=endpoint(k,q,t)
      for sample in [10_000,100_000,1_000_000]:
       # Poissonized mass-fraction sampling, conditioning on known intact atom.
       obs=rng.poisson(f*sample)/sample;obs[0]=f[0]
       st=time.perf_counter();raw,w=invert(obs,q,t);directtime=time.perf_counter()-st
       clipped=np.maximum(raw,0)
       st=time.perf_counter()
       fit,res,calls=fit_endpoint(obs,q,t,x0=clipped,maxiter=350)
       fit_time=time.perf_counter()-st
       first=obs/(t);first[0]=0
       # Improved single-generation estimator includes exact survival factors.
       single=np.zeros(n)
       den=np.exp(-t*q**np.arange(1,n))-np.exp(-t)
       single[1:]=obs[1:]*(1-q**np.arange(1,n))/den
       out['matched_noise'].append({'t':t,'samples':sample,
          'raw_l1':float(sum(abs(raw-k))),
          'clipped_l1':float(sum(abs(clipped-k))),
          'fit_l1':float(sum(abs(fit-k))),
          'short_time_l1':float(sum(abs(first-k))),
          'single_gen_l1':float(sum(abs(single-k))),
          'direct_sec':directtime,'fit_sec':fit_time,'fit_calls':calls,
          'fit_success':bool(res.success),'fit_message':str(res.message),
          'fit_loss':float(res.fun),'Wmax':float(max(w))})
       print(out['matched_noise'][-1],flush=True)
    # Prefix truncation exactness: unknown lower fragments never affect larger.
    k=np.r_[0.,rng.dirichlet(np.ones(149))];q=.96;t=2.5
    f=endpoint(k,q,t)
    for n in [10,30,80]:
        kh,_=invert(f[:n],q,t)
        out['truncation'].append({'n':n,'maxerr':float(max(abs(kh-k[:n]))),
            'unobserved_kernel_mass':float(k[n:].sum())})
    with open('test_results.json','w') as fh:json.dump(out,fh,indent=2)
    print('correctness worst',max(x['maxerr'] for x in out['correctness']))
    print('gradient',out['gradient_maxerr'])


if __name__=='__main__':run()
