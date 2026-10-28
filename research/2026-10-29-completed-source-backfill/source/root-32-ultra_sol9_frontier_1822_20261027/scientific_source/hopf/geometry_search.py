#!/usr/bin/env python3
"""Diagnostic search of the exact Hopf support geometry; no SOS ansatz.

Finite numerical outcomes are diagnostics only. The associated proof note
derives the continuum formulas. Every acquired K and optimized pair is saved.
"""
import json, time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, differential_evolution

OUT=Path(__file__).resolve().parent

def sigma(K,n):
    n=np.asarray(n)
    f=np.einsum('...i,ij,...j->...',n,K,n)
    g=f*np.trace(K)-np.einsum('...i,ij,...j->...',n,K@K,n)
    disc=np.maximum(0,g*g-4*np.linalg.det(K)*f)
    return 2*np.linalg.det(K)/(g+np.sqrt(disc))

def acoustic_r(theta,B,d):
    e=np.stack((np.cos(theta),np.sin(theta)),axis=-1)
    H=2*np.linalg.det(B)*np.eye(2)-B@B-np.outer(d,d)
    t=np.array([[0,1],[-1,0]])@(np.linalg.det(B)*np.linalg.solve(B,d))
    h=np.einsum('...i,ij,...j->...',e,H,e)
    k=np.einsum('...i,ij,...j->...',e,B,e)
    return (np.einsum('...i,ij,...j->...',e,B@B+3*np.outer(d,d),e)
            +4*(e@t)**2/h)/(2*k)

def make_K(b,rho,phi,margin=1e-8):
    B=np.diag([1.,b])
    d=np.sqrt([2*b-1,b*(2-b)])*rho*np.array([np.cos(phi),np.sin(phi)])
    grid=np.linspace(0,np.pi,257,endpoint=False)
    vals=acoustic_r(grid,B,d)
    ids=np.where((vals>=np.roll(vals,1))&(vals>=np.roll(vals,-1)))[0]
    r=0.
    for i in ids:
        rr=minimize(lambda x:-float(acoustic_r(x[0],B,d)),[grid[i]],method='BFGS',
                    options={'gtol':1e-10})
        r=max(r,-rr.fun)
    r=r*(1+margin)+margin
    return np.block([[B,d[:,None]],[d[None,:],np.array([[r]])]])

def sphere(x):
    return np.stack((np.cos(x[...,0])*np.cos(x[...,1]),
                     np.sin(x[...,0])*np.cos(x[...,1]),np.sin(x[...,1])),axis=-1)

def pair_ratio(K,x):
    x=np.asarray(x)
    n,p=sphere(x[...,:2]),sphere(x[...,2:])
    sn,sp=sigma(K,n),sigma(K,p)
    un=n@K/sn[...,None]-n
    up=p@K/sp[...,None]-p
    zn,zp=n[...,2]/sn,p[...,2]/sp
    w=(zp[...,None]*un-zn[...,None]*up)/(zn+zp)[...,None]
    return np.linalg.norm(w,axis=-1)

def main():
    start=time.perf_counter();rng=np.random.default_rng(871728)
    records=[]
    pars=[(1.,.99,0.),(1.5,.99,0.),(1.5,.99,np.pi/2),
          (1.5,.99,np.pi/4),(1.9,.99,np.pi/4),(1.1,.999,np.pi/4)]
    pars += [(rng.uniform(1,1.99),rng.uniform(.05,.999),rng.uniform(0,np.pi/2))
             for _ in range(64)]
    for idx,(b,rho,phi) in enumerate(pars):
        K=make_K(b,rho,phi)
        def obj(x):return -float(pair_ratio(K,x))
        xx=np.empty((12000,4));xx[:,[0,2]]=rng.uniform(0,2*np.pi,(12000,2))
        xx[:,[1,3]]=np.arcsin(rng.uniform(.001,1.,(12000,2)))
        val=pair_ratio(K,xx)
        best=None
        for j in np.argpartition(val,-6)[-6:]:
            fit=minimize(obj,xx[j],method='L-BFGS-B',
                         bounds=[(0,2*np.pi),(1e-5,np.pi/2)]*2,
                         options={'maxiter':250,'ftol':1e-13,'gtol':1e-8})
            if best is None or fit.fun<best.fun:best=fit
        record={'index':idx,'b':b,'rho':rho,'phi':phi,'K':K.tolist(),
                'best_pair_ratio':-best.fun,'angles':best.x.tolist(),
                'elapsed_seconds':time.perf_counter()-start}
        records.append(record)
        print(json.dumps(record),flush=True)
        (OUT/'GEOMETRY_SEARCH.json').write_text(json.dumps(
            {'scope':'NUMERICAL_DIAGNOSTIC_ONLY','records':records,
             'elapsed_seconds':time.perf_counter()-start},indent=2)+'\n')

if __name__=='__main__':main()
