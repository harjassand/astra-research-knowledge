"""Causal density-capped inversion and independent forward-defect diagnostics.

The O(m^2) count is arithmetic-operation complexity, not a fixed-precision or
bit-complexity guarantee. The diagnostic is not a formal interval certificate.
"""
import numpy as np
from fragment_inverse import uniformized_forward


def clipped_inverse(y,q,t,cap,dps=None):
    """cap = M*h for probability mass per positive log bin; zero is intact atom."""
    n=len(y)
    if dps is None:
        y=np.asarray(y)
        k=np.zeros(n);w=np.zeros(n);w[0]=1;p=np.zeros(n);p[0]=np.exp(-t)
        for i in range(1,n):
            z=-np.expm1(i*np.log(q));d=p[0]*np.expm1(t*z);A=d/z
            T=np.dot(k[1:i],w[i-1:0:-1]);S=np.dot(p[1:i],w[i-1:0:-1])
            raw=(y[i]+S)/A-T
            k[i]=np.clip(raw,0,cap)
            w[i]=(k[i]+T)/z
            p[i]=A*(k[i]+T)-S
        return k,p,float(np.max(np.abs(w)))
    import mpmath as mp
    with mp.workdps(dps):
        q=mp.mpf(float(q));t=mp.mpf(float(t));capmp=mp.mpf(float(cap))
        yy=[mp.mpf(float(z)) for z in y]
        k=[mp.mpf(0)]*n;w=[mp.mpf(0)]*n;w[0]=mp.mpf(1)
        p=[mp.mpf(0)]*n;p[0]=mp.exp(-t)
        for i in range(1,n):
            z=1-q**i;d=p[0]*mp.expm1(t*z);A=d/z
            T=mp.fsum(k[j]*w[i-j] for j in range(1,i))
            S=mp.fsum(p[j]*w[i-j] for j in range(1,i))
            raw=(yy[i]+S)/A-T
            k[i]=max(mp.mpf(0),min(capmp,raw))
            w[i]=(k[i]+T)/z
            p[i]=A*(k[i]+T)-S
        return np.array([float(z) for z in k]),np.array([float(z) for z in p]),float(max(abs(z) for z in w))


def numerical_defect(k,y,q,t,cap):
    """Ordinary floating diagnostic for the exact a-posteriori defect formula."""
    pred=uniformized_forward(k,q,t)
    residual=pred-y
    defect=residual.copy();defect[0]=0
    low=k==0;high=k==cap
    defect[low]=np.minimum(0,residual[low])
    defect[high]=np.maximum(0,residual[high])
    defect[0]=0
    return float(np.sum(abs(defect))),float(np.max(abs(defect))),pred


def recover_with_precision(y,q,t,cap,tolerance=1e-10,precisions=(None,40,80,160,320)):
    """Escalate precision against a stable classical-forward diagnostic.

    Returns an explicit success flag; never silently calls an inaccurate result
    validated. This uses float forward evaluation, not certified intervals.
    """
    attempts=[]
    for dps in precisions:
        k,p,wmax=clipped_inverse(y,q,t,cap,dps=dps)
        defect,sup,pred=numerical_defect(k,y,q,t,cap)
        attempts.append({'decimal_digits':dps,'defect_l1':defect,'defect_sup':sup,'Wmax':wmax})
        if np.isfinite(defect) and defect<=tolerance:
            return k,attempts,True
    return k,attempts,False


def repair_prefix_mass(k):
    return k/max(1.,float(np.sum(k)))
