#!/usr/bin/env python3
"""Numerical cone comparison; no feasibility outcome is an exact certificate.
The coefficient maps are built from Astra's retained closed-form interface.
"""
from pathlib import Path
import numpy as np
import json,sys,time
OUT=Path(__file__).parent

def acoustic_extreme(Q,rng):
    tr=np.trace(Q,axis1=1,axis2=2)
    _,_,V=np.linalg.svd(tr.reshape(1,-1),full_matrices=True)
    Z=V[1:].T
    norm=np.array([1,1,2,0,0,0,0,0,0,1,0,0,0,0,0],float)
    anchor=norm/(tr@norm)
    B=np.einsum('ia,ijk->ajk',Z,Q)
    cc=np.r_[rng.normal(size=9),np.zeros(6)]; cc/=np.linalg.norm(cc)
    linear=Z.T@cc; h=np.zeros(14)
    for mu in [1.,.2,.04,.008,.0016,.00032,.000064,.0000128]:
        for it in range(80):
            vv=anchor+Z@h; M=np.einsum('i,ijk->jk',vv,Q)
            inv=np.linalg.inv(M)
            g=-linear-mu*np.einsum('ij,aji->a',inv,B)
            ib=np.einsum('ij,ajk->aik',inv,B)
            H=mu*np.einsum('aij,bji->ab',ib,ib)
            step=np.linalg.solve(H,g); dec=float(g@step)
            if dec<1e-10:break
            old=-cc@vv-mu*np.linalg.slogdet(M)[1];scale=1.
            while scale>1e-13:
                hh=h-scale*step;vm=anchor+Z@hh
                MM=np.einsum('i,ijk->jk',vm,Q)
                if np.linalg.eigvalsh(MM)[0]>0:
                    val=-cc@vm-mu*np.linalg.slogdet(MM)[1]
                    if val<=old-.01*scale*dec:break
                scale*=.5
            h=hh
    return (anchor+Z@h)*100

def heat(d,p,steps=12000,margin=0.):
    ij=np.triu_indices(24);wt=np.where(ij[0]==ij[1],1.,np.sqrt(2.))
    def mat(v):
        a=np.zeros((24,24));a[ij]=v/wt;a[(ij[1],ij[0])]=v/wt
        return a
    def vech(a):return a[ij]*wt
    rhs=d['D']@d['E']@p;anchor=d['Ti']@rhs
    y=anchor.copy();dual=np.zeros(301)
    for it in range(steps):
        xx=anchor+d['Proj']@(y-dual)
        lam,V=np.linalg.eigh(mat(xx[:-1]+dual[:-1]))
        yp=np.r_[vech((V*np.maximum(lam,margin))@V.T),max(0.,xx[-1]+dual[-1])]
        dual+=xx-yp
        primal=np.linalg.norm(xx-yp);change=np.linalg.norm(yp-y);y=yp
        if primal<1e-9 and change<1e-9:break
    rec=dict(iterations=it,primal=float(primal),change=float(change),affine_gap=float(np.linalg.norm(d['T']@anchor-rhs)),gamma=float(xx[-1]),mineig=float(np.linalg.eigvalsh(mat(xx[:-1]))[0]))
    return rec,xx,dual

if __name__=='__main__':
    d=np.load(OUT/'interfaces.npz');rng=np.random.default_rng(20261027)
    results=[];tick=time.monotonic()
    for i in range(int(sys.argv[1]) if len(sys.argv)>1 else 20):
        v=acoustic_extreme(d['Q'],rng)
        rec,xx,dual=heat(d,v[:9])
        rec.update(index=i,p=v[:9].tolist(),k=v[9:].tolist(),acoustic_min=float(np.linalg.eigvalsh(np.einsum('i,ijk->jk',v,d['Q']))[0]),status='NUMERICAL_ONLY',seconds=time.monotonic()-tick)
        results.append(rec)
        np.savez(OUT/f'candidate_{i}.npz',p=v[:9],k=v[9:],heat=xx,dual=dual)
        (OUT/'cone_results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(rec),flush=True)
