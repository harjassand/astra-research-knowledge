"""Sampled abstract entire-map test; not a receiving theorem or countermodel."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize


def features(x,y):
    xx,yy=np.broadcast_arrays(x,y)
    s,c=np.sin(xx).ravel(),np.cos(xx).ravel()
    t,d=np.sin(yy).ravel(),np.cos(yy).ravel()
    a=np.stack([s,s*d,s*t,1-c,(1-c)*d,(1-c)*t],axis=1)
    b=np.stack([t,t*c,t*s,1-d,(1-d)*c,(1-d)*s],axis=1)
    return a,b


def main():
    grid=np.linspace(-np.pi,np.pi,81)
    a,b=features(grid[:,None],grid[None,:])
    aa,bb=features(.35,.35)
    def obj(v):
        return -float((aa@v[:6])**2+(bb@v[6:])**2)
    def jac(v):
        return -2*np.r_[(aa@v[:6])*aa[0],(bb@v[6:])*bb[0]]
    def cons(v):
        return 1-(a@v[:6])**2-(b@v[6:])**2
    def con_jac(v):
        return -2*np.c_[((a@v[:6])[:,None]*a),((b@v[6:])[:,None]*b)]
    rng=np.random.default_rng(20261016)
    rows=[]
    for k in range(8):
        v=np.zeros(12)
        v[1]=v[6]=1
        if k:
            v+=rng.normal(0,.05,size=12)
            v/=max(1,np.sqrt(1-cons(v).min()))
        result=minimize(obj,v,jac=jac,method='SLSQP',
                        constraints=[dict(type='ineq',fun=cons,jac=con_jac)],
                        options=dict(maxiter=500,ftol=1e-12))
        # Dense checking is still a finite test.
        dense=np.linspace(-np.pi,np.pi,1001)
        ad,bd=features(dense[:,None],dense[None,:])
        sup=float(np.max((ad@result.x[:6])**2+(bd@result.x[6:])**2))
        q=1-np.cos(.35)**4
        row=dict(start=k,success=bool(result.success),value=-obj(result.x),Q=q,
                 ratio=-obj(result.x)/q,dense_sup_squared=sup,
                 coefficients=result.x.tolist(),iterations=int(result.nit))
        rows.append(row)
        print(json.dumps(row),flush=True)
    (Path(__file__).resolve().parent/'abstract_or_receipt.json').write_text(json.dumps(dict(
        family='real two-output bidegree-one trigonometric entire map; zero hyperplanes',
        warning='sampled constraints only; no rigorously established global contraction',results=rows),indent=2)+'\n')


if __name__=='__main__':
    main()
