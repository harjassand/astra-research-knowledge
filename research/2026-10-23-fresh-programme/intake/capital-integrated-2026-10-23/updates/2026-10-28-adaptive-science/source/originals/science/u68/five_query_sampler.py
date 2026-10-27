"""Literal five-value positive correction and matched five-value averaging.

The theorem is FIVE_QUERY_POSITIVE_CORRECTION.md. Floating diagnostics below
check mean/covariance and bounded characteristic tests, never continuous TV.
"""
import json
import math
from pathlib import Path
import numpy as np


class CosSource:
    def __init__(self,lam): self.lam=lam;self.queries=0
    def __call__(self,x):
        self.queries+=len(x)
        return self.lam*np.cos(x)


def heat_action(g,c,v,s,rng):
    n,d=v.shape
    nv=np.linalg.norm(v,axis=1)
    u=v/np.where(nv>0,nv,1)[:,None]
    z=rng.normal(size=(n,d));zp=z-np.sum(z*u,axis=1)[:,None]*u
    rad=np.linalg.norm(rng.normal(size=(n,3)),axis=1)
    s=np.broadcast_to(s,(n,))
    center=c+s[:,None]*zp
    plus=g(center+(s*rad)[:,None]*u)
    minus=g(center-(s*rad)[:,None]*u)
    return (nv/(2*s*rad))[:,None]*(plus-minus)


def dh_action(g,c,v,a,b,rng):
    return b*heat_action(g,b*c,v,a,rng)


def k_action(g,c,v,b,rng):
    rho=b*rng.random(len(c))
    return b*heat_action(g,rho[:,None]*c,v,np.sqrt(1-rho*rho),rng)


def gamma_action(g,c,v,a,b,rng):
    # A single fair scalar coin per execution, not per coordinate.
    choice=rng.integers(0,2,len(v))
    # Masked batches retain exactly four source-value queries per execution.
    ans=np.zeros_like(v)
    for mode in (0,1):
        idx=np.flatnonzero(choice==mode)
        if not len(idx):continue
        if mode==0:
            mid=dh_action(g,c[idx],v[idx],a,b,rng)
            ans[idx]=k_action(g,c[idx],mid,b,rng)
        else:
            mid=k_action(g,c[idx],v[idx],b,rng)
            ans[idx]=dh_action(g,c[idx],mid,a,b,rng)
    return ans


def sample(g,n,d,a,eta,rng):
    b=math.sqrt(1-a*a)
    G=rng.normal(size=(n,d));H=rng.normal(size=(n,d))
    Z=rng.normal(size=(n,d));W=rng.normal(size=(n,d))
    V=rng.normal(size=(n,d));T=np.sqrt(rng.random(n))
    C=T[:,None]*G+np.sqrt(1-T*T)[:,None]*W
    U=-.5*gamma_action(g,C,Z,a,b,rng)
    return g(b*G+a*H)+Z+U+eta*V


def diagnose(lam,d,n=160000,a=.01,eta=.5):
    rng=np.random.default_rng(700000+d*10+int(lam*100))
    g=CosSource(lam)
    stats=[]
    # Bounded characteristic tests use fixed, known projections.
    direction=np.ones(d)/math.sqrt(d)
    freqs=np.array([.5,1.,2.])
    mu=lam*math.exp(-.5)
    for mode in ('five_query_correction','five_query_average'):
        sm=np.zeros(d);ss=np.zeros(d);cf=np.zeros(3,dtype=complex)
        startq=g.queries
        for start in range(0,n,4000):
            nn=min(4000,n-start)
            if mode=='five_query_correction':
                y=sample(g,nn,d,a,eta,rng)
            else:
                vals=np.zeros((nn,d))
                for _ in range(5):vals+=g(rng.normal(size=(nn,d)))/5
                y=vals+math.sqrt(1+eta*eta)*rng.normal(size=(nn,d))
            sm+=np.sum(y,axis=0);ss+=np.sum((y-mu)**2,axis=0)
            q=(y-mu)@direction
            cf+=np.sum(np.exp(1j*q[:,None]*freqs[None,:]),axis=0)
        assert g.queries-startq==5*n
        target=np.exp(-.5*(1+eta*eta)*freqs*freqs)
        stats.append(dict(method=mode,queries=g.queries-startq,
            query_count_per_execution=5,
            maximum_coordinate_mean_error=float(np.max(np.abs(sm/n-mu))),
            average_second_moment_about_true_mean=float(np.mean(ss/n)),
            characteristic_error_abs=np.abs(cf/n-target).tolist(),
            characteristic_sampling_se_upper=1/math.sqrt(n)))
    b=math.sqrt(1-a*a)
    Ceta=math.sqrt(2)/2*math.log(1+eta**-2)
    bound=min(1,Ceta*(b**3*lam**3*math.sqrt(d)/math.sqrt(2)+.5*b**4*lam**4*d)
        +math.sqrt(2)*b**4*lam**4*d/(8*eta**2)
        +a*lam*math.sqrt(d)/(2*eta))
    proxy_ratio=lam*lam/(5*(1+eta*eta))
    if proxy_ratio<1:
        exp_arg=-d/2*math.log1p(-proxy_ratio**2)
        averaging_bound=min(1,.5*math.sqrt(math.expm1(exp_arg)))
    else:averaging_bound=1.
    return dict(lam=lam,d=d,n=n,a=a,eta=eta,
        proved_TV_upper=bound,
        five_query_averaging_TV_upper=averaging_bound,
        covariance_excess_op_upper=a*a*lam*lam+b**4*lam**4/4,
        diagnostics=stats,
        scope='Moment and bounded-test diagnostics only; theorem supplies TV bound')


def main():
    out=[]
    for lam,d,a in ((.1,1,.01),(.3,1,.01),(.5,1,.01),(.1,8,.01),
                    (.3,8,.01),(.1,64,.01),(.01,64,1e-7)):
        r=diagnose(lam,d,a=a);out.append(r);print(json.dumps(r),flush=True)
    Path(__file__).with_name('five_query_results.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
