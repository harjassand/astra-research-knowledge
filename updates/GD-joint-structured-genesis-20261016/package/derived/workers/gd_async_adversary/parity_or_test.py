"""Sampled entire-map test including exact gap reflection parities."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize


def feat(x,y):
    x,y=np.broadcast_arrays(x,y)
    s,c=np.sin(x).ravel(),np.cos(x).ravel()
    t,d=np.sin(y).ravel(),np.cos(y).ravel()
    return np.c_[s,s*d],np.c_[t,t*c],(s*t)[:,None]


def mv(a,v):
    return np.einsum('ij,j->i',a,v,optimize=False)


def vals(fs,v):
    return [mv(fs[0],v[:2]),mv(fs[1],v[2:4]),mv(fs[2],v[4:])]


def main():
    grid=np.linspace(-np.pi,np.pi,161)
    fs=feat(grid[:,None],grid[None,:])
    ft=feat(.35,.35)
    def value(v,features=ft):
        return sum(z*z for z in vals(features,v))
    def cons(v):
        return 1-value(v,fs)
    def cj(v):
        z=vals(fs,v)
        return -2*np.c_[z[0][:,None]*fs[0],z[1][:,None]*fs[1],z[2][:,None]*fs[2]]
    def oj(v):
        z=vals(ft,v)
        return -2*np.r_[z[0][0]*ft[0][0],z[1][0]*ft[1][0],z[2][0]*ft[2][0]]
    rows=[]
    rng=np.random.default_rng(2026101603)
    for k in range(8):
        v=np.array([0,1,0,1,1.],float) if k==0 else rng.normal(0,.4,5)
        v/=max(1.,np.sqrt(np.max(value(v,fs))))
        res=minimize(lambda v:-value(v)[0],v,jac=oj,method='SLSQP',
                     constraints=[dict(type='ineq',fun=cons,jac=cj)],
                     options=dict(maxiter=400,ftol=1e-13))
        q=1-np.cos(.35)**4
        row=dict(start=k,value=float(value(res.x)[0]),Q=float(q),
                 ratio=float(value(res.x)[0]/q),coefficients=res.x.tolist(),
                 success=bool(res.success),message=str(res.message))
        rows.append(row)
        print(json.dumps(row),flush=True)
    (Path(__file__).resolve().parent/'parity_or_receipt.json').write_text(json.dumps(dict(
        family='five coefficient real parity-reflection-equivariant trigonometric maps',
        warning='finite sampled constraints; no global theorem',results=rows),indent=2)+'\n')


if __name__=='__main__':
    main()
