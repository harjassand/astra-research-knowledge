#!/usr/bin/env python3
"""Finite physical-Fock check of algebraic identities, not a continuum response.
Checks factors in the dressed source and odd compression at a NONREAL z.
"""
import json, math
from pathlib import Path
import numpy as np
from continuum_response import bisect

def run(n=6,g=.2):
    d=2+2*n
    h=np.eye(d)*3
    t=(1+math.sqrt(2))*g/2;s=(math.sqrt(2)-1)*g/2
    a,b=2,2+n
    for i,j,v in [(0,a,t),(1,b,t),(0,b,s),(1,a,s)]:h[i,j]=h[j,i]=v
    for j in range(n):h[a+j,b+j]=h[b+j,a+j]=2
    for j in range(n-1):
        for o in [a,b]:h[o+j,o+j+1]=h[o+j+1,o+j]=-.5
    states=[(i,j) for i in range(d) for j in range(i,d) if (i,j) not in [(0,0),(1,1)]]
    ind={p:k for k,p in enumerate(states)}
    H=np.zeros((len(states),len(states)))
    for col,(i,j) in enumerate(states):
        H[col,col]=h[i,i]+h[j,j]
        occ=np.bincount([i,j],minlength=d)
        for source in np.flatnonzero(occ):
            for target in np.flatnonzero(h[:,source]):
                if source==target:continue
                dest=occ.copy();dest[source]-=1
                factor=math.sqrt(occ[source])*math.sqrt(dest[target]+1)
                dest[target]+=1
                pair=tuple(np.repeat(np.arange(d),dest))
                if pair in ind:H[ind[pair],col]+=h[target,source]*factor
    E,U=np.linalg.eigh(H)
    bare=ind[(0,1)]
    idx=np.argmax(U[bare,:]**2)
    ep=E[idx];psi=U[:,idx]
    V=np.array([int(i==0)+int(j==0)-int(i==1)-int(j==1) for i,j in states])
    source=V*psi
    def one(plus):
        m=np.diag([3.]+[5. if plus else 1.]*n)
        of=[math.sqrt(2)*g if plus else g]+[-.5]*(n-1)
        for j,v in enumerate(of):m[j,j+1]=m[j+1,j]=v
        x,u=np.linalg.eigh(m)
        return x,u[0,:]**2
    xp,wp=one(True);xm,wm=one(False)
    def L(z,x,w,der=0):return np.sum(w[:,None]*w[None,:]/(x[:,None]+x[None,:]-z)**(1+der))
    ep_formula=bisect(lambda z:L(z,xp,wp)+L(z,xm,wm),2*xp[np.argmax(wp)]+1e-9,2*xm[np.argmax(wm)]-1e-9)
    N2=2/(L(ep_formula,xp,wp,1)+L(ep_formula,xm,wm,1))
    rp=np.sum(wp[None,:]/(xp[:,None]+xp[None,:]-ep_formula),axis=1)
    rm=np.sum(wm[None,:]/(xm[:,None]+xm[None,:]-ep_formula),axis=1)
    W=rp[:,None]+rm[None,:]
    wt=wp[:,None]*wm[None,:]
    z=5.9+.03j
    den=xp[:,None]+xm[None,:]-z
    D=np.sum(wt/den);A=np.sum(wt*W/den);B=np.sum(wt*W**2/den)
    formula=N2*(B-A*A/D)
    direct=source@np.linalg.solve(H-z*np.eye(len(H)),source)
    source_norm_formula=N2*np.sum(wt*W**2)
    result=dict(n=n,g=g,fock_dimension=len(H),nonreal_z=str(z),
        eigenvalue_error=float(abs(ep-ep_formula)),
        source_norm_error=float(abs(source@source-source_norm_formula)),
        resolvent_error=float(abs(direct-formula)),
        direct_resolvent=[float(direct.real),float(direct.imag)],
        spectral_formula_resolvent=[float(formula.real),float(formula.imag)],
        scope='Finite physical-ladder algebraic consistency at nonreal z only; not used to establish or estimate the infinite on-shell response.')
    assert result['eigenvalue_error']<1e-11
    assert result['source_norm_error']<1e-11
    assert result['resolvent_error']<1e-11
    return result

if __name__=='__main__':
    out=[run(4),run(6),run(8)]
    (Path(__file__).resolve().parent/'operator_identity_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
