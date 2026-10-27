#!/usr/local/bin/python3
"""Independent finite Fock-space check of source normalization and odd resolvent.

This verifies the algebra. It is not used to infer the infinite spectral density.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parent

def channel(g,plus,n):
    eig,U=eigh_tridiagonal(np.r_[3.,np.full(n,5. if plus else 1.)],
                           np.r_[math.sqrt(2)*g if plus else g,np.full(n-1,-.5)])
    return eig,U[0]**2

def check(g=.2,n=6):
    # Physical memories L,R, plus/minus bath modes. No memory doubles allowed.
    d=2+2*n
    h=np.diag(np.r_[3.,3.,np.full(n,5.),np.full(n,1.)])
    for mem,sgn in [(0,1),(1,-1)]:
        h[mem,2]=h[2,mem]=g
        h[mem,2+n]=h[2+n,mem]=sgn*g/math.sqrt(2)
    for start in (2,2+n):
        for j in range(n-1):h[start+j,start+j+1]=h[start+j+1,start+j]=-.5
    basis=[(i,j) for i in range(d) for j in range(i,d) if not (i==j and i<2)]
    lookup={p:i for i,p in enumerate(basis)}
    H=np.zeros((len(basis),len(basis)))
    V=np.zeros(len(basis))
    for a,(i,j) in enumerate(basis):
        H[a,a]=h[i,i]+h[j,j]
        V[a]=int(i==0)+int(j==0)-int(i==1)-int(j==1)
        for old,other in ((i,j),(j,i)) if i!=j else ((i,j),):
            for k in range(d):
                if old==k or h[k,old]==0:continue
                new=tuple(sorted((k,other)))
                if new not in lookup:continue
                factor=math.sqrt(2) if (i==j or k==other) else 1.
                H[lookup[new],a]+=factor*h[k,old]
    assert np.linalg.norm(H-H.T)<1e-12
    vals,U=np.linalg.eigh(H)
    pindex=lookup[(0,1)]
    loc=np.argmax(U[pindex]**2)
    Ef=vals[loc]
    psi=U[:,loc]
    f=V*psi
    xp,wp=channel(g,True,n); xm,wm=channel(g,False,n)
    def one_m(z,x,w):return np.sum(w/(x-z))
    def L(z,x,w):return np.sum(w[:,None]*w[None,:]/(x[:,None]+x[None,:]-z))
    bp=xp[np.argmax(wp)];bm=xm[np.argmax(wm)]
    E=brentq(lambda z:L(z,xp,wp)+L(z,xm,wm),2*bp+1e-9,2*bm-1e-9,xtol=5e-15)
    deriv=sum(np.sum(w[:,None]*w[None,:]/(x[:,None]+x[None,:]-E)**2)
              for x,w in [(xp,wp),(xm,wm)])
    C=math.sqrt(2/deriv)
    F=np.array([one_m(E-x,xp,wp) for x in xp])
    G=np.array([one_m(E-y,xm,wm) for y in xm])
    source=C*(F[:,None]+G[None,:])
    measure=wp[:,None]*wm[None,:]
    source_norm=np.sum(measure*source**2)
    rows=[]
    for eps in [.2,.05,.01]:
        z=E+1j*eps
        denom=xp[:,None]+xm[None,:]-z
        D=np.sum(measure/denom)
        B=np.sum(measure*source/denom)
        A=np.sum(measure*source**2/denom)
        reduced=A-B*B/D
        direct=f@np.linalg.solve(H-z*np.eye(len(H)),f)
        rows.append({"epsilon":eps,"direct_real":direct.real,"direct_imag":direct.imag,
                     "reduced_real":reduced.real,"reduced_imag":reduced.imag,
                     "absolute_difference":abs(direct-reduced)})
    return {"g":g,"n":n,"pair_energy_fock":Ef,"pair_energy_reduction":E,
            "pair_energy_error":abs(E-Ef),"source_norm_fock":float(f@f),
            "source_norm_reduction":source_norm,"source_orthogonality":float(np.sum(measure*source)),
            "bare_pair_V_norm":V[pindex],"checks":rows}

if __name__=="__main__":
    out={"checks":[check(n=n) for n in [4,6,10]]}
    (ROOT/"fock_check_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
