"""Search genuine minor-support obstruction; a non-witness is inconclusive.

For each A, global polyconvex support requires one scalar kappa(A) with
P0(A,B)-kappa(A)*det(B-A)>=0 for every B. A certified lower bound from one
negative determinant and upper bound from one positive determinant can
contradict this. Numerical findings must be rationalized and checked.
"""
import json,time
from pathlib import Path
import numpy as np

def invariants(z):
    a,b,c,d=np.moveaxis(np.asarray(z),-1,0)
    return a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c

def energy(z,tau=11.3):
    u,v,w,q=invariants(z)
    return u*u+v*v+3*w*w+tau*q*q+4*q*(u-v)

def gradient(z,tau=11.3):
    a,b,c,d=np.asarray(z);u,v,w,q=invariants(z)
    du,dv,dw,dq=2*u+4*q,2*v-4*q,6*w,2*tau*q+4*(u-v)
    return np.array([2*a*du+b*dw+d*dq,2*b*dv+a*dw-c*dq,
                     2*c*du+d*dw-b*dq,2*d*dv+c*dw+a*dq])

def interval(A,B,tau):
    X=B-A;q=invariants(X)[3]
    p=energy(B,tau)-energy(A,tau)-X@gradient(A,tau)
    ratio=np.divide(p,q,out=np.full_like(p,np.nan),where=np.abs(q)>1e-7)
    lows=np.where(q< -1e-7,ratio,-np.inf);ups=np.where(q>1e-7,ratio,np.inf)
    j,k=int(np.argmax(lows)),int(np.argmin(ups))
    return float(lows[j]),float(ups[k]),B[j],B[k]

def main():
    start=time.monotonic();rng=np.random.default_rng(20261027);tau=11.3
    raw=rng.normal(size=(50000,4));raw/=np.linalg.norm(raw,axis=1)[:,None]
    radii=np.exp(rng.uniform(np.log(.03),np.log(5),size=len(raw)));raw*=radii[:,None]
    backgrounds=[]
    for a in (.2,.5,1,2,5):
        for d in (-1,1):
            for b in (0,.3,1):backgrounds.append(np.array([a,b,0,d])/np.sqrt(a*a+b*b+d*d))
    for _ in range(120):
        a,b,d=rng.normal(size=3);a=abs(a);v=np.array([a,b,0,d]);backgrounds.append(v/np.linalg.norm(v))
    best=None
    for A in backgrounds:
        B=np.concatenate((raw,A+raw),axis=0)
        low,up,Blo,Bhi=interval(A,B,tau);gap=low-up
        if best is None or gap>best['gap']:
            best={'A':A.tolist(),'B_lower':Blo.tolist(),'B_upper':Bhi.tolist(),
                  'lower':low,'upper':up,'gap':gap}
    result={'status':'NUMERICAL_SEARCH_ONLY','energy_tau':tau,'backgrounds':len(backgrounds),
            'B_points_per_background':len(raw)*2,'best':best,'wall_seconds':time.monotonic()-start,
            'interpretation':'Positive exact-rationalized gap would obstruct PC; no sign here is a theorem'}
    Path('support_search.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
