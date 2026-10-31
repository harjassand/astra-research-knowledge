"""Finite sanity checks of the deterministic path perturbation bound.
Not an implementation of the coherent oracle or a substitute for its proof.
"""
import json
import numpy as np

rng = np.random.default_rng(713031)

def tree(n, delta):
    if n == 1:
        return np.ones(1), np.ones(1), 0
    left = n // 2
    z = rng.beta(left, n-left)
    zz = np.clip(z + rng.uniform(-delta, delta), 0, 1)
    x, xx, d1 = tree(left, delta)
    y, yy, d2 = tree(n-left, delta)
    return np.r_[z*x, (1-z)*y], np.r_[zz*xx, (1-zz)*yy], 1+max(d1,d2)

rows=[]
for n in [2,3,4,17,128,1025,4096]:
    for delta in [1e-8,1e-4,.03]:
        for rep in range(5):
            np_, nm = (n+1)//2, n//2
            z=rng.beta(np_,nm)
            zz=np.clip(z+rng.uniform(-delta,delta),0,1)
            p, pp, d1=tree(np_,delta)
            m, mm, d2=tree(nm,delta)
            x=np.empty(n);xx=np.empty(n)
            x[::2]=z*p;xx[::2]=zz*pp
            x[1::2]=(1-z)*m;xx[1::2]=(1-zz)*mm
            tx=np.r_[0,np.cumsum(x)];ty=np.r_[0,np.cumsum(xx)]
            sx=np.r_[0,np.cumsum(x*((-1.)**np.arange(n)))]
            sy=np.r_[0,np.cumsum(xx*((-1.)**np.arange(n)))]
            grid=np.unique(np.r_[tx,ty,np.linspace(0,1,2049)])
            err=np.max(np.abs(np.interp(grid,tx,sx)-np.interp(grid,ty,sy)))
            bound=4*(max(d1,d2)+1)*delta
            assert err<=bound+1e-12,(n,delta,err,bound)
            rows.append(dict(intervals=n,delta=delta,error=float(err),bound=bound))
print(json.dumps({'seed':713031,'checks':len(rows),'max_error_to_bound':max(r['error']/r['bound'] for r in rows),'scope':'c=T=1; floating sanity check only','rows':rows},indent=2))
