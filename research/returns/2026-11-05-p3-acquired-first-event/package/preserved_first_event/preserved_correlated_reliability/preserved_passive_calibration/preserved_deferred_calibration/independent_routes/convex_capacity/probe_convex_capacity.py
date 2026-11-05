"""Exploratory numerical channel capacity, not a certified continuum result."""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.special import xlogy
import json,time

def channel(x,V,t):
    dx=x[1]-x[0]; u=np.diff(V)
    def B(z):
        out=np.empty_like(z); small=np.abs(z)<1e-6
        out[small]=1-z[small]/2+z[small]**2/12
        out[~small]=z[~small]/np.expm1(z[~small])
        return out
    upper=B(u)/dx**2; lower=B(-u)/dx**2
    Q=np.diag(upper,1)+np.diag(lower,-1)
    Q[np.diag_indices_from(Q)]=-Q.sum(axis=1)
    W=expm(t*Q); W=np.maximum(W,0);W/=W.sum(axis=1,keepdims=True)
    return W

def BA(W,c,s,niter=3000):
    lW=np.log(W+1e-300); ent=np.sum(W*lW,axis=1)
    p=np.exp(-s*c);p/=p.sum()
    for i in range(niter):
        out=p@W
        D=ent-W@np.log(out+1e-300)
        logp=np.log(p+1e-300)+D-s*c
        pnew=np.exp(logp-logp.max());pnew/=pnew.sum()
        if np.linalg.norm(pnew-p,1)<1e-10:break
        p=pnew
    out=p@W;D=ent-W@np.log(out+1e-300)
    return p@D,p@c,p,i

def capacity(W,x,P):
    z=BA(W,x*x,0)
    if z[1]<=P:return z
    high=1.
    while BA(W,x*x,high)[1]>P:high*=2
    s=brentq(lambda q:BA(W,x*x,q)[1]-P,0,high,xtol=1e-7)
    return BA(W,x*x,s)
if __name__=='__main__':
    st=time.time(); x=np.linspace(-5,5,161)
    pots={'quad':x*x/2,'quartic01':x*x/2+.1*x**4,'quartic1':x*x/2+x**4,'asym10':x*x/2+10*np.maximum(x,0)**2,'soft_wall':x*x/2+20*np.maximum(np.abs(x)-1,0)**2}
    rows=[]
    for name,V in pots.items():
        for t in [.1,.5,1.]:
            W=channel(x,V,t)
            for P in [.1,1.,4.]:
                I,c,p,it=capacity(W,x,P)
                bound=.5*np.log1p(P/np.expm1(2*t))
                row=dict(potential=name,t=t,P=P,I=I,OU=bound,excess=I-bound,mean=float(p@x),var=float(p@(x*x)-(p@x)**2),iterations=it)
                rows.append(row);print(json.dumps(row),flush=True)
    json.dump(rows,open('/workspace/scratch/2958277fc089/next_constructive_alternatives/convex_capacity_probe.json','w'),indent=2)
    print('runtime',time.time()-st)
