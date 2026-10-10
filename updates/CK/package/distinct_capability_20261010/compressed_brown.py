"""Compressed Brown/Cox clock. Numerical experiment, not interval-certified arithmetic.
The default per-stratum threshold implements the proved Bernstein bound.
"""
import math, json, time
import numpy as np
from scipy.stats import kstest
from poisson_clock import ProductClock, finite_cdf

class CompressedBrown(ProductClock):
    def __init__(self,pi,lam):
        super().__init__(pi,lam)
        prefix=np.r_[0.,np.cumsum((1-self.pi[:-1])*self.lam[:-1])]
        self.kappa=1+prefix/self.lam
    def increments(self,i,m,rng):
        rates=np.full(m,self.lam[i])
        for j in range(i): rates+=self.lam[j]*(rng.random(m)<1-self.pi[j])
        return rng.exponential(1/rates)
    def sample(self,rng,relative=.5,failure=.1,threshold_override=None):
        h=relative/(2+relative)
        R=np.ceil(6*self.kappa/h**2*math.log(4*self.n/failure)).astype(int)
        if threshold_override is not None:R[:]=threshold_override
        W=rng.exponential()/self.q
        H=0.;draws=0;large=0;small=0
        for i in range(self.n):
            r=self.w[i]*W
            if r<R[i]:
                c=int(rng.poisson(r));draws+=c;small+=1
                if c:H+=float(self.increments(i,c,rng).sum())
            else:
                m=int(R[i]);draws+=m;large+=1
                H+=r*float(self.increments(i,m,rng).mean())
        return H,draws,large,small
    def brown_exact(self,rng):
        k=int(rng.geometric(self.q))-1
        if k==0:return 0.
        counts=rng.multinomial(k,self.w/(1-self.q));ans=0.
        for i,c in enumerate(counts):
            if c:ans+=float(self.increments(i,int(c),rng).sum())
        return ans

def main():
    rng=np.random.default_rng(10102026)
    results=[]
    # Full-state reference small heterogeneous case, transformed law evaluated via expm.
    n=3;pi=np.array([.3,.55,.7]);lam=np.array([.4,1.3,2.7]);p=CompressedBrown(pi,lam)
    mu=p.mean_reference();trials=20000
    samples=np.array([p.sample(rng,threshold_override=25)[0] for _ in range(trials)])
    exact=np.array([p.brown_exact(rng) for _ in range(trials)])
    checks=[]
    for scale in [.001,.01,.1,.3,1,3,10]:
        t=scale*mu
        checks.append(dict(t_over_mean=scale,full_state_cdf=finite_cdf(pi,lam,t),
                           compressed_empirical=float(np.mean(samples<=t)),brown_empirical=float(np.mean(exact<=t))))
    results.append(dict(test='small_full_state',n=n,q=p.q,mean=mu,trials=trials,threshold=25,
                        certificate='Empirical threshold only; lower than conservative theoretical threshold.',cdf=checks))
    # Conservative certified-threshold algorithm; huge horizons, no full-state enumeration.
    for n in [12,40,80]:
        pi=np.linspace(.35,.65,n);lam=np.geomspace(.3,3,n);p=CompressedBrown(pi,lam)
        start=time.perf_counter();ans=p.sample(rng,relative=.5,failure=.1)
        results.append(dict(test='theoretical_threshold',n=n,q=p.q,log2_inverse_q=-math.log2(p.q),
                            relative=.5,failure=.1,sample=ans[0],increment_draws=ans[1],large_strata=ans[2],small_strata=ans[3],seconds=time.perf_counter()-start))
    # Deliberately multiscale counterexample to using only one mean-scale Poisson clock.
    n=3;pi=np.array([.999999,.5,.5]);lam=np.array([1e-12,1.,3.]);p=CompressedBrown(pi,lam)
    trials=20000;start=time.perf_counter()
    vals=np.array([p.sample(rng,threshold_override=100)[0] for _ in range(trials)])
    refs=np.array([p.brown_exact(rng) for _ in range(trials)])
    results.append(dict(test='multiscale',q=p.q,trials=trials,threshold=100,
                        empirical_quantiles=np.quantile(vals,[.1,.5,.9,.99]).tolist(),
                        exact_brown_quantiles=np.quantile(refs,[.1,.5,.9,.99]).tolist(),seconds=time.perf_counter()-start))
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
