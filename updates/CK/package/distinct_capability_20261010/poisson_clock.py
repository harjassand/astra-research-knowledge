"""Proof-of-mechanism simulator, using floating point RNGs (not a certified bit implementation)."""
import json, math, time
import numpy as np
from scipy.linalg import expm

class ProductClock:
    def __init__(self, pi, lam):
        order=np.argsort(lam)
        self.pi=np.asarray(pi,dtype=float)[order]
        self.lam=np.asarray(lam,dtype=float)[order]
        self.n=len(pi)
        # Max active index i: i active, all larger indices inactive; lower free.
        self.w=(1-self.pi)*np.r_[np.cumprod(self.pi[:0:-1])[::-1],1.]
        self.q=float(np.prod(self.pi))
        self.M0=float(np.sum(self.w/self.lam))
        assert abs(self.w.sum()+self.q-1)<1e-12
    def tilted(self,s,rng):
        masses=np.r_[self.q,s*self.w/(s+self.lam)]
        probs=masses/masses.sum()
        attempts=0
        while True:
            attempts+=1
            i=int(rng.choice(self.n+1,p=probs))-1
            if i<0:return 0.,attempts
            active=rng.random(i)<1-self.pi[:i]
            z=self.lam[i]+float(np.sum(self.lam[:i][active]))
            if rng.random()<(s+self.lam[i])/(s+z):return z,attempts
    def count(self,s,rng):
        count=attempts=cycles=0
        while True:
            lam,a=self.tilted(s,rng);attempts+=a;cycles+=1
            if lam==0:return count,attempts,cycles
            count+=int(rng.geometric(lam/(s+lam)))
    def spectral(self):
        weights=np.array([1.]);rates=np.array([0.])
        for p,l in zip(self.pi,self.lam):
            weights=np.r_[weights*p,weights*(1-p)]
            rates=np.r_[rates,rates+l]
        return weights,rates
    def mean_reference(self):
        w,l=self.spectral();return float(np.sum(w[1:]/l[1:])/self.q)
    def laplace_reference(self,u):
        w,l=self.spectral();r=np.sum(w[1:]/(u+l[1:]));return self.q/(self.q+u*r)

def finite_cdf(pi,lam,t):
    n=len(pi);N=1<<n;Q=np.zeros((N,N));stationary=np.ones(N)
    for x in range(N):
        for i in range(n):
            bit=(x>>i)&1
            # State 0 is target; pi is probability target bit 0.
            rate=lam[i]*(pi[i] if bit else 1-pi[i])
            Q[x,x^(1<<i)]=rate;Q[x,x]-=rate
            stationary[x]*=(1-pi[i] if bit else pi[i])
    return 1-float(stationary[1:]@expm(Q[1:,1:]*t)@np.ones(N-1))

def main():
    rng=np.random.default_rng(241017)
    rows=[]
    for n in [3,8,20,40,80]:
        pi=np.linspace(.35,.65,n)
        lam=np.geomspace(.3,3,n)
        p=ProductClock(pi,lam)
        eps=.3
        s=p.n*p.q/(eps*eps*p.M0)
        trials=3000 if n<=8 else 500
        start=time.perf_counter()
        arr=np.array([p.count(s,rng) for _ in range(trials)],dtype=float)
        row=dict(n=n,q=p.q,log2_inverse_q=-math.log2(p.q),s=s,trials=trials,
                 avg_proposals=float(arr[:,1].mean()),avg_cycles=float(arr[:,2].mean()),
                 max_cycles=int(arr[:,2].max()),seconds=time.perf_counter()-start,
                 sample_mean_times_s=float(arr[:,0].mean()),cycle_bound=1+n/eps**2)
        if n<=8:
            mu=p.mean_reference();row['true_mean_times_s']=s*mu
            # Empirical count pgf should equal exact hitting-time Laplace at s(1-z).
            row['pgf_checks']=[dict(z=z,empirical=float(np.mean(z**arr[:,0])),truth=p.laplace_reference(s*(1-z))) for z in [.8,.95,.99]]
            row['mean_CV_gate']=dict(mu=mu,lower=p.M0/(p.n*p.q),upper=p.M0/p.q)
            if n==3:
                row['cdf_at_mean']=finite_cdf(pi,lam,mu)
        rows.append(row)
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
