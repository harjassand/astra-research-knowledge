"""Dependency-free positive cyclic resolvent for the fixed-grid diffusion.

For edge arrays a[i] (i -> i+1) and b[i] (i+1 -> i), Q is a column
generator and resolvent(a,b,s,rhs) returns (s I - Q)^(-1) rhs.
"""
from __future__ import annotations

import numpy as np


def bernoulli(z):
    """B(z)=z/expm1(z), including a stable expansion near zero."""
    z=np.asarray(z,dtype=float)
    out=np.empty_like(z)
    small=np.abs(z)<1e-4
    t=z[small]
    out[small]=1-t/2+t*t/12-t**4/720+t**6/30240
    out[~small]=z[~small]/np.expm1(z[~small])
    return out


def apply_generator(a,b,p):
    return np.roll(a*p,1)+b*np.roll(p,-1)-(a+np.roll(b,1))*p


def tridiagonal(lower,diag,upper,rhs):
    """Thomas solve; rhs may contain multiple columns."""
    d=np.asarray(diag,dtype=complex).copy()
    z=np.asarray(rhs,dtype=complex).copy()
    for i in range(1,len(d)):
        m=lower[i-1]/d[i-1]
        d[i]-=m*upper[i-1]
        z[i]-=m*z[i-1]
    z[-1]/=d[-1]
    for i in range(len(d)-2,-1,-1):
        z[i]=(z[i]-upper[i]*z[i+1])/d[i]
    return z


def resolvent(a,b,s,rhs):
    """Solve (s I-Q)x=rhs for the periodic nearest-neighbor generator."""
    n=len(a)
    d=s+a+np.roll(b,1)
    lo,up=-a[:-1],-b[:-1]
    U=np.zeros((n,2),dtype=complex)
    U[0,0],U[-1,1]=-a[-1],-b[-1]
    sol=tridiagonal(lo,d,up,np.column_stack((rhs,U)))
    y,Z=sol[:,0],sol[:,1:]
    small=np.eye(2)+Z[[-1,0],:]
    return y-Z@np.linalg.solve(small,y[[-1,0]])


def solver_check(seed=117,n=11):
    rng=np.random.default_rng(seed)
    a,b=np.exp(rng.normal(size=(2,n)))
    Q=np.column_stack([apply_generator(a,b,x) for x in np.eye(n)])
    rhs=rng.normal(size=n)+1j*rng.normal(size=n)
    s=.4+.7j
    own=resolvent(a,b,s,rhs)
    dense=np.linalg.solve(s*np.eye(n)-Q,rhs)
    return float(np.max(np.abs(own-dense)))
