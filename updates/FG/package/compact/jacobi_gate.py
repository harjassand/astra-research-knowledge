"""Continuous kinetically gated Jacobi diffusion. Exact local polynomial algebra.
The continuum is never discretized into microscopic conformations.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import numpy as np,json,math,time
from generic_tensor import solve_generic


def local_basis(q:F,rho:F,maxdeg:int):
    alpha=q*rho
    moments=[F(1)]
    for k in range(2*maxdeg+3):moments.append(moments[-1]*(alpha+k)/(rho+k))
    def ip(a,b,shift=0):return sum(x*y*moments[i+j+shift] for i,x in enumerate(a) for j,y in enumerate(b))
    polys=[];norms=[];diag=[];bet=[]
    for j in range(maxdeg+1):
        v=[F(0)]*j+[F(1)]
        for p,h in zip(polys,norms):
            z=ip(v,p)/h
            for t,c in enumerate(p):v[t]-=z*c
        h=ip(v,v);assert h>0
        polys.append(v);norms.append(h);diag.append(ip(v,v,1)/h);bet.append(F(0) if j==0 else h/norms[-2])
    X=np.zeros((maxdeg+1,maxdeg+1),dtype=object)
    for j in range(maxdeg+1):
        X[j,j]=diag[j]
        if j<maxdeg:X[j+1,j]=F(1)
        if j>0:X[j-1,j]=bet[j]
    # Exact orthogonality/self-adjointness tests.
    for i in range(maxdeg+1):
        for j in range(maxdeg+1):
            assert norms[i]*X[i,j]==norms[j]*X[j,i]
    lam=[F(j)*(j-1+rho) for j in range(maxdeg+1)]
    return {'polys':polys,'norms':norms,'X':X,'lambda':lam,'moments':moments}


def build_mpo(n:int,q:F,rho:F,eps:F,degree:int):
    info=local_basis(q,rho,degree+1);d=degree+1
    h=np.diag([float(x) for x in info['lambda'][:d]])
    norms=np.array([float(x) for x in info['norms'][:d]])
    X=np.array(info['X'][:d,:d],float)*np.sqrt(norms[:,None]/norms[None,:])
    assert np.max(abs(X-X.T))<1e-12
    ef=float(eps);kappa=float(rho*q);I=np.eye(d);W=[]
    for i in range(n):
        w=np.zeros((3,3,d,d));w[0,0]=I;w[1,0]=h;w[2,2]=I
        w[2,1]=(1-ef)*X
        w[2,0]=(1. if i==0 else ef)*h
        if i==0:w[2,0]+=kappa*ef*I
        if i==n-1:w[2,0]+=kappa*(1-ef)*X
        if i==0:w=w[2:3]
        if i==n-1:w=w[:,0:1]
        W.append(w)
    return W,info

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=8);p.add_argument('--q',default='1/5');p.add_argument('--rho',default='1/10');p.add_argument('--eps',default='1/100');p.add_argument('--degree',type=int,default=2);p.add_argument('--rank',type=int,default=8);p.add_argument('--sweeps',type=int,default=3);p.add_argument('--out',default='jacobi')
    a=p.parse_args();t=time.perf_counter();W,info=build_mpo(a.n,F(a.q),F(a.rho),F(a.eps),a.degree);buildtime=time.perf_counter()-t
    cores,logs=solve_generic(W,rank=a.rank,sweeps=a.sweeps)
    np.savez(a.out+'.npz',**{f'a{i}':x for i,x in enumerate(cores)})
    meta=vars(a);meta.update({'build_seconds':buildtime,'logs':logs,'continuum_model':True})
    Path(a.out+'.json').write_text(json.dumps(meta,indent=2))
