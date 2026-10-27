#!/usr/local/bin/python3
"""Finite-volume algebra checks against the direct physical local ladder.
These do not establish the infinite-volume classification (see PROOF.md).
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, eigh_tridiagonal
from scipy.optimize import brentq


def direct_ladder(n,g):
    d=2+2*n
    h=np.diag(np.full(d,3.))
    t=(1+math.sqrt(2))*g/2
    s=(math.sqrt(2)-1)*g/2
    a,b=2,2+n
    for i,j,v in [(0,a,t),(1,b,t),(0,b,s),(1,a,s)]: h[i,j]=h[j,i]=v
    for j in range(n): h[a+j,b+j]=h[b+j,a+j]=2.
    for j in range(n-1):
        for start in (a,b): h[start+j,start+j+1]=h[start+j+1,start+j]=-.5
    basis=[(i,j) for i in range(d) for j in range(i,d) if (i,j) not in [(0,0),(1,1)]]
    lookup={v:i for i,v in enumerate(basis)}
    H=np.zeros((len(basis),len(basis)))
    for col,(i,j) in enumerate(basis):
        H[col,col]=h[i,i]+h[j,j]
        if i==j:
            for k in range(d):
                if k!=i and h[k,i]!=0:
                    H[lookup[tuple(sorted((i,k)))],col]+=math.sqrt(2)*h[k,i]
        else:
            for src,other in ((i,j),(j,i)):
                for k in range(d):
                    if k==src or h[k,src]==0: continue
                    dest=tuple(sorted((k,other)))
                    if dest in lookup:
                        H[lookup[dest],col]+=(math.sqrt(2) if k==other else 1)*h[k,src]
    assert np.linalg.norm(H-H.T)<1e-13
    vdiag=np.array([(i==0)+(j==0)-(i==1)-(j==1) for i,j in basis],float)
    return H,basis,vdiag


def check(n,g=.2):
    specs=[]
    for center,lam in [(5,math.sqrt(2)*g),(1,g)]:
        diag=np.r_[3.,np.full(n,center)]
        off=np.r_[lam,np.full(n-1,-.5)]
        e,u=eigh_tridiagonal(diag,off)
        w=u[0]**2
        atom=e[np.argmax(w)]
        specs.append((e,w,atom))
    def L(z,s):
        e,w,_=s
        return np.sum(w[:,None]*w[None,:]/(e[:,None]+e[None,:]-z))
    def Lp(z,s):
        e,w,_=s
        return np.sum(w[:,None]*w[None,:]/(e[:,None]+e[None,:]-z)**2)
    Ep=brentq(lambda z:L(z,specs[0])+L(z,specs[1]),2*specs[0][2]+1e-10,2*specs[1][2]-1e-10,xtol=1e-14)
    D=sum(Lp(Ep,s) for s in specs)
    C=math.sqrt(2/D)
    ep,wp,_=specs[0]
    em,wm,_=specs[1]
    Ap=np.sum(wp[None,:]/(ep[:,None]+ep[None,:]-Ep),axis=1)
    Am=np.sum(wm[None,:]/(em[:,None]+em[None,:]-Ep),axis=1)
    f=C*(Ap[:,None]+Am[None,:])
    weights=wp[:,None]*wm[None,:]
    H,basis,Vdiag=direct_ladder(n,g)
    evals,U=eigh(H)
    idx=int(np.argmax(U[basis.index((0,1))]**2))
    Ephysical=evals[idx]
    source=Vdiag*U[:,idx]
    assert np.isfinite(U).all() and np.isfinite(source).all()
    fhat=np.einsum("ij,i->j",U,source)
    assert np.isfinite(fhat).all()
    observations=[]
    for epsilon in [.1,.03,.01]:
        z=Ep+1j*epsilon
        denominator=ep[:,None]+em[None,:]-z
        K=np.sum(weights/denominator)
        J=np.sum(weights*f/denominator)
        Q=np.sum(weights*f*f/denominator)
        from_formula=Q-J*J/K
        from_physical=np.sum(fhat*fhat/(evals-z))
        observations.append(dict(epsilon=epsilon,physical_real=float(from_physical.real),physical_imag=float(from_physical.imag),
            rank_one_real=float(from_formula.real),rank_one_imag=float(from_formula.imag),absolute_error=float(abs(from_formula-from_physical))))
    return dict(n=n,dimension=len(basis),pair_energy_physical=float(Ephysical),pair_energy_formula=float(Ep),
        pair_energy_error=float(abs(Ephysical-Ep)),source_norm_physical=float(source@source),
        source_norm_formula=float(np.sum(weights*f*f)),q_orthogonality=float(np.sum(weights*f)),resolvents=observations)

if __name__=='__main__':
    data=[check(n) for n in (4,8,12)]
    for run in data:
        assert run['pair_energy_error']<1e-11
        assert abs(run['source_norm_physical']-run['source_norm_formula'])<1e-11
        assert abs(run['q_orthogonality'])<1e-10
        assert max(r['absolute_error'] for r in run['resolvents'])<1e-11
    Path(__file__).with_name('finite_volume_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
