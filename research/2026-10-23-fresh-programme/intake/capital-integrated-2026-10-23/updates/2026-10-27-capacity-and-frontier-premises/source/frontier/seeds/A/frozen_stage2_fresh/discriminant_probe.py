"""Unrestricted complex variational probe of the exact global obligation.

Analytically eliminates the nonnegative third-row scale. This is a local
search, not a positivity certificate. Every block remains an arbitrary
complex N-by-two factor; the initial zero family is not a support constraint.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize


def out(a,b):return np.einsum('ia,ja->ij',a,b.conj(),optimize=False)


def l(c,m):
    a=c.reshape((3,)*(2*m)).copy()
    for k in range(m):
        z=np.moveaxis(a,(k,m+k),(0,1));tr=np.trace(z,axis1=0,axis2=1)
        z=z-.5*np.eye(3).reshape((3,3)+(1,)*(2*m-2))*tr
        a=np.moveaxis(z,(0,1),(k,m+k))
    return a.reshape(c.shape)


def q(c,m):return np.vdot(c,l(c,m)).real


def coeff(z,m):
    N=3**m;z=z[:12*N]+1j*z[12*N:]
    z=z.reshape(6,N,2).copy();z[:4]/=np.linalg.norm(z[:4]);z[4:]/=np.linalg.norm(z[4:])
    U=z[:2];V=z[2:4];X,Y=z[4:]
    A=out(U[0],V[0])+out(U[1],V[1])
    a=sum(q(out(U[i],V[j]),m) for i in range(2) for j in range(2))-.5*q(A,m)
    d=q(out(X,Y),m)
    T=sum(q(out(U[i],Y),m)+q(out(X,V[i]),m) for i in range(2))-np.vdot(A,l(out(X,Y),m)).real
    return float(a),float(T),float(d),z


def probe(m,seed,maxiter):
    rng=np.random.default_rng(seed);N=3**m
    def rand(shape):return rng.normal(size=shape)+1j*rng.normal(size=shape)
    u=rand(N);v=rand(N);u/=np.linalg.norm(u);v/=np.linalg.norm(v)
    # An explicit orthonormal plane with third row nonzero.
    plane=np.array([[1/np.sqrt(2),1/np.sqrt(6)],[-1/np.sqrt(2),1/np.sqrt(6)],[0,-2/np.sqrt(6)]])
    U=np.einsum('ia,j->ija',plane,u,optimize=False)
    V=np.einsum('ia,j->ija',plane,v,optimize=False)
    z=np.concatenate((U[:2],V[:2],U[2:],V[2:]))
    z+=.08*rand(z.shape)/np.sqrt(N)
    x0=np.r_[z.real.ravel(),z.imag.ravel()]
    best=[np.inf,None]
    calls=[0]
    def f(x):
        a,T,d,z=coeff(x,m);calls[0]+=1
        if not np.isfinite([a,T,d]).all():return 1e6
        if min(a,d)<1e-10:return 100+1e-10/max(min(a,d),1e-30)
        value=T/np.sqrt(2*a*d)
        if value<best[0]:best[:]=[value,x.copy()]
        return value
    start=f(x0)
    res=minimize(f,x0,method='L-BFGS-B',options={'maxiter':maxiter,'maxfun':60000,'ftol':1e-12,'gtol':1e-7,'maxls':30})
    a,T,d,z=coeff(best[1],m)
    if T<0:
        scale=np.sqrt(-T/d)
        U=np.concatenate((z[:2],scale*z[4:5])).reshape(3*N,2)
        V=np.concatenate((z[2:4],scale*z[5:6])).reshape(3*N,2)
        C=out(U,V);direct=q(C,m+1);split=a-T*T/(2*d)
        if abs(direct-split)>1e-9:raise AssertionError('independent same-copy split')
    else:direct=None;split=None
    if best[0]<-1-1e-7:
        np.savez(Path(__file__).with_name(f'discriminant_candidate_{seed}.npz'),factors=z,m=m,a=a,T=T,d=d,C=C)
    return {'scope':'unrestricted complex local descent, no certified optimum',
            'm':m,'seed':seed,'initial_ratio':start,'best_T_over_sqrt_2ad':best[0],
            'a':a,'T':T,'d':d,'direct_optimized_q':direct,'split_optimized_q':split,
            'iterations':int(res.nit),'function_calls':calls[0],
            'success':bool(res.success),'message':str(res.message)}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,default=2)
    ap.add_argument('--count',type=int,default=2);ap.add_argument('--maxiter',type=int,default=100)
    args=ap.parse_args()
    for k in range(args.count):
        print(json.dumps(probe(args.m,20261027+k,args.maxiter)),flush=True)
