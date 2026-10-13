"""Search smaller witnesses. Discovery arithmetic is floating point."""
from pathlib import Path
import itertools,json,time
import numpy as np
from search_policy_counterexamples import one_step,ratio
ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(1400262)
start=time.time();best_ad=None;best_r2=None
for case in range(100000):
    n=2 if case<30000 else 3
    edges=[(i,-1) for i in range(n)]+[(i,j) for i in range(n) for j in range(i+1,n)]
    ds=np.zeros((len(edges),n))
    for e,(i,j) in enumerate(edges):
        ds[e,i]=1
        if j>=0: ds[e,j]=-1
    lo=np.array([2.**int(rng.integers(-4,5)) for e in edges])
    hi=lo+np.array([2.**int(rng.integers(-3,8)) for e in edges])
    m=np.array([2.**int(rng.integers(-3,5)) for i in range(n)])
    base={'case':case,'edges':edges,'lo':lo.tolist(),'hi':hi.tolist(),'m':m.tolist()}
    for first in range(len(edges)):
        vals=[]
        for theta in [0.,.125,.25,.5,.75,1.]:
            ll=lo.copy();hh=hi.copy();ll[first]=hh[first]=lo[first]+theta*(hi[first]-lo[first])
            score,second=one_step(ds,ll,hh,m,{first}); vals.append((theta,score,second))
        bound=max(vals[0][1],vals[-1][1]); peak=max(v[1] for v in vals);gap=peak/bound-1
        if gap>1e-4 and (best_ad is None or gap>best_ad['gap']):
            best_ad={**base,'first':first,'grid_values':vals,'gap':gap};print('AD',json.dumps(best_ad),flush=True)
    if best_r2 is None:
        for batch in itertools.combinations(range(len(edges)),2):
            vals=[]
            for theta in [0.,.125,.25,.5,.75,1.]:
                ll=lo.copy();hh=hi.copy()
                for e in batch: ll[e]=hh[e]=lo[e]+theta*(hi[e]-lo[e])
                vals.append((theta,ratio(ds,ll,hh,m)))
            if max(v[1] for v in vals)>max(vals[0][1],vals[-1][1])*(1+1e-3):
                best_r2={**base,'batch':batch,'grid_values':vals};print('R2',json.dumps(best_r2),flush=True);break
    if case%1000==0:
        (ROOT/'small_search_results.json').write_text(json.dumps({'cases':case,'seconds':time.time()-start,'adaptive':best_ad,'rank_two':best_r2},indent=2))
    if best_ad is not None and n==2 and best_ad['gap']>.05:break
    if time.time()-start>50:break
(ROOT/'small_search_results.json').write_text(json.dumps({'cases':case+1,'seconds':time.time()-start,'adaptive':best_ad,'rank_two':best_r2},indent=2))
