"""Rank-one updated Gibbs baseline; exact invariant law in ideal arithmetic.
No claim that the finite burn-in is a certified mixing bound.
"""
import numpy as np
from numba import njit

@njit(cache=True)
def _rebuild(X,choice):
    d=X.shape[1]; B=np.eye(d)
    for i in range(len(choice)):
        v=X[2*i+choice[i]]
        for a in range(d):
            for b in range(d):B[a,b]+=v[a]*v[b]
    return np.linalg.inv(B)

@njit(cache=True)
def run_feature_gibbs(X,nsamples,thin,burn,seed,refresh=256):
    np.random.seed(seed); n=X.shape[0]//2; d=X.shape[1]
    choice=np.zeros(n,np.int64); R=_rebuild(X,choice)
    samples=np.empty((nsamples,n),np.int64); count=0; acc=0; rebuilds=1
    total=burn+nsamples*thin
    for it in range(total):
        i=np.random.randint(n); old=X[2*i+choice[i]]; new=X[2*i+1-choice[i]]
        ro=R@old; rn=R@new
        lo=old@ro; ln=new@rn; cross=old@rn
        ratio=(1.-lo)*(1.+ln)+cross*cross
        if ratio<=0. or not np.isfinite(ratio):
            R=_rebuild(X,choice); rebuilds+=1
            ro=R@old; rn=R@new; lo=old@ro; ln=new@rn; cross=old@rn
            ratio=(1.-lo)*(1.+ln)+cross*cross
        if np.random.random()<ratio/(1.+ratio):
            # Sherman--Morrison twice; periodic recomputation charges numerical stabilization.
            denom=1.-lo
            if denom>1e-10:
                for a in range(d):
                    for b in range(d): R[a,b]+=ro[a]*ro[b]/denom
                rn=R@new; denom2=1.+new@rn
                for a in range(d):
                    for b in range(d): R[a,b]-=rn[a]*rn[b]/denom2
                choice[i]=1-choice[i]
            else:
                choice[i]=1-choice[i]; R=_rebuild(X,choice); rebuilds+=1
            acc+=1
            if acc%refresh==0:R=_rebuild(X,choice); rebuilds+=1
        if it>=burn and (it-burn+1)%thin==0:
            samples[count]=choice; count+=1
    return samples,total,acc,rebuilds
