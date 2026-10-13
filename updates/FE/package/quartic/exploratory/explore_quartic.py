import numpy as np
from scipy.optimize import linprog
from itertools import product
from pathlib import Path

# Entries of a 2x2 matrix are ordered (11,12,21,22).
exponents=np.array([e for e in product(range(5), repeat=4) if sum(e)==4])
assert len(exponents)==35

def monomials(x):
    x=np.asarray(x)
    return np.prod(x[...,None,:]**exponents,axis=-1)

def hessian_constraints(A,R):
    A=np.asarray(A); R=np.asarray(R)
    out=np.zeros((len(A),len(exponents)))
    for i in range(4):
        for j in range(4):
            coef=exponents[:,i]*(exponents[:,j]-(i==j))
            keep=coef>0
            ee=exponents[keep].copy(); ee[:,i]-=1;ee[:,j]-=1
            out[:,keep]+=R[:,i,None]*R[:,j,None]*coef[keep]*np.prod(A[:,None,:]**ee,axis=-1)
    return out

def random_constraints(n, rng):
    A=rng.normal(size=(n,4)); A/=np.linalg.norm(A,axis=1)[:,None]
    ab=rng.uniform(0,2*np.pi,size=(n,2))
    a=np.stack((np.cos(ab[:,0]),np.sin(ab[:,0])),axis=-1)
    b=np.stack((np.cos(ab[:,1]),np.sin(ab[:,1])),axis=-1)
    R=np.einsum('ni,nj->nij',a,b).reshape(-1,4)
    return hessian_constraints(A,R)

def mean_gaussian():
    table=np.array([1.,0.,1.,0.,3.])
    return np.prod(table[exponents],axis=-1)

def gradient_moments(k,a,phases=None,A0=None,N=64):
    k=np.asarray(k);a=np.asarray(a)
    xx,yy=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij')
    pts=np.stack((xx.ravel(),yy.ravel()),axis=-1)
    if phases is None:phases=np.zeros(len(k))
    if A0 is None:A0=np.zeros(4)
    waves=np.cos(pts@k.T+np.asarray(phases))
    R=np.einsum('ni,nj->nij',a,k).reshape(-1,4)
    X=waves@R+A0
    return np.mean(monomials(X),axis=0)-monomials(A0)

def run():
    rng=np.random.default_rng(20261014)
    cons=random_constraints(20000,rng)
    norm=mean_gaussian()
    scenarios=[np.array([[1,0],[0,1],[1,2],[-2,-3]]),
               np.array([[1,0],[0,1],[1,1],[1,-1]]),
               np.array([[1,0],[0,1],[1,1],[1,-1],[2,1],[1,2]])]
    best=None
    for z in range(12):
        k=scenarios[z%3]
        a=rng.normal(size=(len(k),2))/np.linalg.norm(k,axis=1)[:,None]
        ph=rng.uniform(0,2*np.pi,len(k))
        A0=rng.normal(size=4)*(.7 if z%2 else 0)
        obj=gradient_moments(k,a,ph,A0)
        out=linprog(obj,A_ub=-cons,b_ub=np.zeros(len(cons)),A_eq=norm[None,:],b_eq=[1.],bounds=[(None,None)]*35,method='highs')
        if out.success:
            test=random_constraints(10000,rng)@out.x
            print(z,'energy',out.fun,'min heldout acoustic',test.min(),flush=True)
            if best is None or out.fun<best[0]:best=(out.fun,out.x,k,a,ph,A0)
        else:print(z,out.message,flush=True)
    if best:
        np.savez(Path(__file__).with_name('quartic_lp_best.npz'),value=best[0],coef=best[1],k=best[2],a=best[3],ph=best[4],A0=best[5],exponents=exponents)
if __name__=='__main__':run()
