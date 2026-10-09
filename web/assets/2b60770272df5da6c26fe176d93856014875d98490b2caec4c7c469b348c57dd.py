"""Numerical probe; no proof or independent validation."""
import numpy as np
from general_channel_probe import conditional_ratio,BASIS
rng=np.random.default_rng(934234)
channels=[(.6,.2),(.01,.495),(.1,.45),(.8,.1)]
for a,b in channels:
    W=b*np.ones((3,3))+(a-b)*np.eye(3)
    best=(0,None)
    for it in range(3500):
        pri=rng.dirichlet(np.ones(3)*.6)
        blocks=[]
        for i in range(3):
            v=rng.normal(size=3);v/=np.linalg.norm(v)
            rad=1-10**rng.uniform(-7,0)
            blocks.append(pri[i]*(np.eye(2)+rad*np.einsum('a,aij->ij',v,BASIS[1:])*np.sqrt(2))/2)
        blocks=np.array(blocks)
        try:r,d,e=conditional_ratio(blocks,W)
        except Exception:continue
        if best[0]<r<1.001:best=(r,blocks)
    print(a,b,'best',best[0],'classical',(a-b)**2/(a+b),'center',1-9/(1/a+2/b),flush=True)
