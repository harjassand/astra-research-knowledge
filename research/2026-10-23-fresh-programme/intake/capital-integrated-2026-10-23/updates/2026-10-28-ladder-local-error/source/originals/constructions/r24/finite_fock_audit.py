#!/usr/bin/env python3
"""Independent local-memory finite-Fock comparison with spectral reduction."""
import json, math
import numpy as np
from scipy.linalg import eigh, eigh_tridiagonal
from scipy.optimize import brentq

G=.2

def spectrum(n, parity):
    lam=math.sqrt(2)*G if parity==1 else G
    diag=np.r_[3., np.full(n, 5. if parity==1 else 1.)]
    off=np.r_[lam, np.full(n-1,-.5)]
    vals,U=eigh_tridiagonal(diag,off)
    return vals,U[0,:]**2

def spectral(n, eps):
    xp,wp=spectrum(n,1); ym,wm=spectrum(n,-1)
    ip=np.argmin(abs(xp-3)); im=np.argmin(abs(ym-3))
    def L(x,w,E): return np.sum(np.outer(w,w)/(x[:,None]+x[None,:]-E))
    E=brentq(lambda E:L(xp,wp,E)+L(ym,wm,E),2*xp[ip]+1e-10,2*ym[im]-1e-10,xtol=1e-14)
    D=sum(np.sum(np.outer(w,w)/(x[:,None]+x[None,:]-E)**2) for x,w in [(xp,wp),(ym,wm)])
    A=(wp[None,:]/(xp[:,None]+xp[None,:]-E)).sum(axis=1)
    C=(wm[None,:]/(ym[:,None]+ym[None,:]-E)).sum(axis=1)
    F=A[:,None]+C[None,:]
    s=xp[:,None]+ym[None,:]
    W=np.outer(wp,wm)
    R=1/(s-E-1j*eps)
    Q=np.sum(W*F*R)/np.sum(W*R)
    rho=(2/D/math.pi)*np.sum(W*eps/((s-E)**2+eps**2)*abs(F-Q)**2)
    source_norm=(2/D)*np.sum(W*F*F)
    return E,float(rho),float(source_norm)

def fock(n, eps):
    d=2+2*n
    h=np.diag(np.r_[3.,3.,np.full(n,5.),np.full(n,1.)])
    for i,v in [(0,G),(1,G)]: h[i,2]=h[2,i]=v
    for i,v in [(0,G/math.sqrt(2)),(1,-G/math.sqrt(2))]: h[i,2+n]=h[2+n,i]=v
    for start in [2,2+n]:
        for j in range(n-1): h[start+j,start+j+1]=h[start+j+1,start+j]=-.5
    pairs=[(i,j) for i in range(d) for j in range(i,d) if not (i==j and i in (0,1))]
    where={a:i for i,a in enumerate(pairs)}
    H=np.zeros((len(pairs),len(pairs)))
    for idx,(i,j) in enumerate(pairs):
        H[idx,idx]=h[i,i]+h[j,j]
        if i==j:
            for k in range(d):
                if k==i or h[k,i]==0: continue
                target=tuple(sorted((i,k)))
                if target in where: H[where[target],idx]+=math.sqrt(2)*h[k,i]
        else:
            for site,other in [(i,j),(j,i)]:
                for k in range(d):
                    if k==site or h[k,site]==0: continue
                    target=tuple(sorted((k,other)))
                    if target in where:
                        H[where[target],idx]+=(math.sqrt(2) if k==other else 1)*h[k,site]
    assert np.linalg.norm(H-H.T)<1e-12
    vals,U=eigh(H)
    pair=where[(0,1)]
    ev_idx=np.argmax(U[pair,:]**2)
    E=vals[ev_idx]
    psi=U[:,ev_idx]
    diag=np.array([(i==0)+(j==0)-(i==1)-(j==1) for i,j in pairs],float)
    f=diag*psi
    assert np.isfinite(U).all() and np.isfinite(f).all()
    coeff=np.einsum("ij,i->j",U,f,optimize=False)
    rho=np.sum(coeff**2 * eps/((vals-E)**2+eps**2))/math.pi
    return E,float(rho),float(f@f),len(pairs)

if __name__=='__main__':
    out=[]
    for n in [4,8,12]:
        for eps in [.1,.01,.001]:
            fE,fr,fn,dim=fock(n,eps)
            sE,sr,sn=spectral(n,eps)
            out.append(dict(n=n,dimension=dim,epsilon=eps,E_direct=fE,E_reduced=sE,
                rho_direct=fr,rho_reduced=sr,relative_error=abs(fr-sr)/fr,
                norm_direct=fn,norm_reduced=sn))
            assert abs(fE-sE)<2e-11 and abs(fr-sr)<max(2e-13,fr*2e-7)
            assert abs(fn-sn)<2e-11
    print(json.dumps(out,indent=2))
