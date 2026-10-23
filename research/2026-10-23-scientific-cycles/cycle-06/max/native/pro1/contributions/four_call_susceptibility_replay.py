#!/usr/bin/env python3
"""Exact leading beta^2 susceptibility averaged over uniform deep prefixes.
This is a finite algebraic diagnostic, never a long-time dynamics certificate.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations
import argparse,json,time,resource
from four_call_representation import history,charge


def susceptibility(n):
    start=time.perf_counter();words=list(product((0,1,2),repeat=n)); index={w:i for i,w in enumerate(words)}
    masks=[0]+[1<<j for j in range(n)]+[(1<<j)|(1<<k) for j,k in combinations(range(n),2)]
    H=defaultdict(int)
    for bath in product((1,2),repeat=n):
        groups=defaultdict(list)
        for i,x in enumerate(words):
            for mask in masks:
                y,seed,w,r=history(x,0,bath,mask)
                groups[(charge(x),y,seed,w)].append((i,r))
        for (q,y,seed,w),paths in groups.items():
            delta=len(w)-n
            if not delta:continue
            for i,r in paths:
                for j,s in paths:
                    if r+s!=2:continue
                    phase=1 if r==s else -1
                    H[i,j]+=phase*delta
    for i,w in enumerate(words):H[i,i]-=(n-1)*(2*charge(w)-n)*(1<<n)
    H={key:v for key,v in H.items() if v}
    assert all(i!=j for i,j in H)
    assert all(H[i,j]==H.get((j,i),0) for i,j in H)
    numer=sum(v*v*(1<<(n-charge(words[i]))) for (i,j),v in H.items())
    var=F(numer,1<<(4*n))
    return {'n':n,'variance':str(var),'variance_per_call':str(var/n),'nonzero_entries':len(H),'wall_seconds':time.perf_counter()-start,'max_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},words,H

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--max-n',type=int,default=5);ap.add_argument('--output',default='four_call_susceptibility_scaling.json');args=ap.parse_args()
    results=[]
    for n in range(2,args.max_n+1):
        r,words,H=susceptibility(n);results.append(r);print(json.dumps(r),flush=True)
        if n==4:
            prev=json.load(open(__file__.replace('_replay.py','.json')))
            want={(i,j):F(v) for i,j,v in prev['sparse_matrix']}
            assert want=={ij:F(v,1<<n) for ij,v in H.items()}
    open(args.output,'w').write(json.dumps({'scope':'Uniform prefix average only; no capacity or large-n theorem','results':results},indent=2)+'\n')
