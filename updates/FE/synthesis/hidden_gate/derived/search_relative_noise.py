"""Floating discovery search for multiplicative-measurement endpoint failure."""
from pathlib import Path
import json,time
import numpy as np
ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(1400263)
def f(c,m):
    a,b,g=c; x,y=m
    return (x*x*b+y*y*a+(x+y)**2*g)/(a*b+(a+b)*g)
start=time.time();out=None
for case in range(10000):
    lo=np.array([2.**int(rng.integers(-4,5)) for _ in range(3)])
    hi=lo+np.array([2.**int(rng.integers(-3,8)) for _ in range(3)])
    m=np.array([2.**int(rng.integers(-3,5)) for _ in range(2)])
    k=4.
    for e in range(3):
        if hi[e]<=k*lo[e]:continue
        vals=[]
        for theta in [0.,.125,.25,.375,.5,.625,.75,.875,1.]:
            a=lo[e]+theta*(hi[e]/k-lo[e]); b=k*a
            ll=lo.copy();hh=hi.copy();ll[e]=a;hh[e]=b
            vals.append((theta,a,f(ll,m)/f(hh,m),f(ll,m)-f(hh,m)))
        bnd=max(vals[0][2],vals[-1][2]); peak=max(v[2] for v in vals)
        if peak>bnd*1.001:
            out={'case':case,'lo':lo.tolist(),'hi':hi.tolist(),'m':m.tolist(),'queried_edge':e,'k':k,'grid_values':vals};break
    if out:break
result={'scope':'floating discovery, exact verification required','seed':1400263,'cases':case+1,'seconds':time.time()-start,'witness':out}
(ROOT/'relative_noise_search_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
