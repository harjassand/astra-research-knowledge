"""Monte Carlo stress test with exact exponential-fiber geometry.
Importance sampling absorbs exp(2 alpha X_1), so alpha near 1/2 is stable.
Directional Gaussian G is normalized implicitly; 64-point conditional quadrature.
No external dependencies beyond NumPy/SciPy. Seed fixed; not a proof.
"""
import json
import numpy as np
from scipy.special import roots_legendre
from pathlib import Path

rng=np.random.default_rng(20261010)
r,w=roots_legendre(64); r=(r+1)/2; w=w/2

def trial(n,alpha,samples=50000,batch=2000):
    values=[]; unbounded=0
    for st in range(0,samples,batch):
        b=min(batch,samples-st)
        g=rng.normal(size=(b,n)); g1=g[:,0]; norm2=(g*g).sum(1); T=g.sum(1)
        sp=np.maximum(g[:,1:],0).sum(1); sm=np.maximum(-g[:,1:],0).sum(1)
        A=np.divide(rng.exponential(size=b),sp,out=np.full(b,np.inf),where=sp>0)
        B=np.divide(rng.exponential(size=b),sm,out=np.full(b,np.inf),where=sm>0)
        x1=rng.exponential(scale=1/(1-2*alpha),size=b)
        A=np.minimum(A,np.divide(x1,g1,out=np.full(b,np.inf),where=g1>0))
        B=np.minimum(B,np.divide(x1,-g1,out=np.full(b,np.inf),where=g1<0))
        a=-A; upper=B; bounded=np.isfinite(A+B); q=np.zeros(b)
        if bounded.any():
            j=bounded; L=(A+B)[j]; midpoint=(upper+a)[j]/2
            weights=w[None,:]*np.exp(-T[j,None]*L[:,None]*(r[None,:]-(T[j,None]<0)))
            weights/=weights.sum(1,keepdims=True)
            er=(weights*r).sum(1); vr=(weights*(r-er[:,None])**2).sum(1)
            z=np.expm1(alpha*g1[j,None]*L[:,None]*(r[None,:]-.5))
            ez=(weights*z).sum(1); vz=(weights*(z-ez[:,None])**2).sum(1)
            q[j]=np.exp(2*alpha*g1[j]*midpoint)*vz/(L*L*vr*norm2[j])
        if (~bounded).any():
            # In an unbounded fiber, s=endpoint +/- Exp(abs(T)).
            j=~bounded; unbounded+=int(j.sum())
            endpoint=np.where(np.isfinite(a[j]),a[j],upper[j]); rate=T[j]; k=alpha*g1[j]
            # Algebraically stable variance of exp(k s):
            # rate/(rate-2k) - (rate/(rate-k))^2
            varfac=rate*k*k/((rate-2*k)*(rate-k)**2)
            q[j]=np.exp(2*k*endpoint)*varfac*rate*rate/norm2[j]
        values.extend(n*(1-alpha)**2/alpha**2*q)
    v=np.array(values)
    return {'n':n,'alpha':alpha,'samples':samples,'ratio_mean':float(v.mean()),'mc_se':float(v.std(ddof=1)/np.sqrt(len(v))),'local_limit':(1-alpha)**2,'unbounded_fibers':unbounded}

out=[]
for n in [2,3,5,10,20,50,100,500]:
    for alpha in [.25,.49]:
        z=trial(n,alpha); out.append(z); print(json.dumps(z),flush=True)
Path(__file__).with_name('product_exponential_results.json').write_text(json.dumps(out,indent=2)+'\n')
