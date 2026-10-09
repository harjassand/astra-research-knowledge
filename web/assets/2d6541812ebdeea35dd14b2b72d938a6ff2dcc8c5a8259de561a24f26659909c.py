"""Floating-point adversarial conditional BKM probe; NOT a proof."""
import numpy as np
from scipy.linalg import eigh, null_space
from bsc_quantum_probe import bkm, BASIS

def conditional_ratio(blocks, w):
    k,d,_=blocks.shape; r=len(BASIS)
    out=np.einsum('xy,xij->yij',w,blocks)
    gs=bkm(blocks.sum(axis=0))
    gin=np.zeros((k*r,k*r)); gout=np.zeros_like(gin)
    gx=[bkm(a) for a in blocks]; gy=[bkm(a) for a in out]
    for i in range(k):
        for j in range(k):
            gin[i*r:(i+1)*r,j*r:(j+1)*r]=(gx[i] if i==j else 0)-gs
            gout[i*r:(i+1)*r,j*r:(j+1)*r]=sum(w[i,y]*w[j,y]*gy[y] for y in range(w.shape[1]))-gs
    trace=np.tile([1.,0,0,0],k)[None,:]
    Q=null_space(trace)
    gi=Q.T@gin@Q; go=Q.T@gout@Q
    eig,vec=eigh(gi)
    keep=eig>max(1e-8,1e-9*eig.max())
    if not keep.any(): return np.nan,None,eig
    T=vec[:,keep]/np.sqrt(eig[keep])
    vals,vs=eigh(T.T@go@T)
    return vals[-1],Q@T@vs[:,-1],eig

if __name__=='__main__':
    W=(np.ones((3,3))-np.eye(3))/2
    theta=np.arange(3)*2*np.pi/3
    for rad in [.1,.5,.9,.99,.9999,1-1e-8]:
        blocks=np.array([(np.eye(2)+rad*(np.sin(t)*BASIS[1]+np.cos(t)*BASIS[3])*np.sqrt(2))/6 for t in theta])
        val,d,eig=conditional_ratio(blocks,W)
        print('trine',rad,val,flush=True)
    rng=np.random.default_rng(20261009)
    best=(0,None)
    for iteration in range(10000):
        pri=rng.dirichlet(np.ones(3))
        b=[]
        for i in range(3):
            direction=rng.normal(size=3); direction/=np.linalg.norm(direction)
            rad=1-10**rng.uniform(-5,0)
            b.append(pri[i]*(np.eye(2)+rad*np.einsum('a,aij->ij',direction,BASIS[1:])*np.sqrt(2))/2)
        b=np.array(b)
        val,d,eig=conditional_ratio(b,W)
        if np.isfinite(val) and best[0]<val<1.001:
            best=(val,(b,d,eig))
            if val>.51: print('new best',iteration,val,flush=True)
    print('BEST',best[0],flush=True)
    np.savez('/mnt/data/adaptive_foundational_research_20261009/triangle_probe_best.npz',ratio=best[0],blocks=best[1][0],direction=best[1][1],input_eigenvalues=best[1][2],channel=W)
