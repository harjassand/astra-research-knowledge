"""Ordinary empirical-Bernstein, Hoeffding and bounded-KL intervals.
No file/data/model access. See PROOF.md for the exact IID scope.
"""
import math
import numpy as np


def interval(x,B,t=14.):
    n=len(x);mean=float(np.mean(x));var=float(np.var(x,ddof=1))
    assert np.min(x)>=-1e-12 and np.max(x)<=B+1e-12
    bern=math.sqrt(2*var*t/n)+7*B*t/(3*(n-1))
    hoeff=B*math.sqrt(t/(2*n))
    rad=min(bern,hoeff)
    q=mean/B
    def kl(p):
        return (q*math.log(q/p) if q else 0.)+((1-q)*math.log((1-q)/(1-p)) if q<1 else 0.)
    # Ordinary bounded-variable KL-Chernoff inversion, not a Bernoulli
    # observation assumption. exp(s x)<=1+x(exp(s)-1) on[0,1].
    if q==0:kl_lo=0.
    else:
        lo=0.;hi=q
        for _ in range(65):
            mid=(lo+hi)/2
            if kl(mid)>t/n:lo=mid
            else:hi=mid
        kl_lo=lo*B
    if q>=1:kl_hi=B
    else:
        lo=q;hi=1.
        for _ in range(65):
            mid=(lo+hi)/2
            if mid==1 or kl(mid)>t/n:hi=mid
            else:lo=mid
        kl_hi=hi*B
    # This is a binary64 numerical application of the ideal IID theorem.
    # No formal libm/PRNG/native-model certificate is claimed.
    return dict(mean=mean,variance=var,radius=rad,empirical_Bernstein_radius=bern,
                Hoeffding_radius=hoeff,KL_Chernoff_interval=[kl_lo,kl_hi],
                lower=max(mean-rad,kl_lo),upper=min(mean+rad,kl_hi))

