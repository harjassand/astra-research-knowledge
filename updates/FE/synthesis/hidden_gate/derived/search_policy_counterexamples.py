"""Bounded floating discovery only; selected witnesses require exact replay.

Find possible failures of extending the rank-one one-step endpoint rule to
(i) two adaptive queries and (ii) a common scalar controlling two edges.
"""
from pathlib import Path
import itertools, json, time
import numpy as np

ROOT = Path(__file__).resolve().parent
rng = np.random.default_rng(140026)

def F(ds, c, m):
    a = np.einsum('e,ei,ej->ij', c, ds, ds)
    return float(m @ np.linalg.solve(a,m))

def ratio(ds, lo, hi, m):
    return F(ds,lo,m)/F(ds,hi,m)

def one_step(ds, lo, hi, m, excluded):
    scores=[]
    for e in range(len(lo)):
        if e in excluded or hi[e] == lo[e]: continue
        worst=0.
        for t in [lo[e],hi[e]]:
            ll=lo.copy(); hh=hi.copy(); ll[e]=hh[e]=t
            worst=max(worst,ratio(ds,ll,hh,m))
        scores.append((worst,e))
    return min(scores) if scores else (1.,-1)

def run(limit=20000):
    start=time.time(); found={}; checks=0
    for case in range(limit):
        n=int(rng.integers(2,5))
        edges=[(i,-1) for i in range(n)]
        edges += [(i,j) for i in range(n) for j in range(i+1,n) if rng.random()<.65]
        ds=np.zeros((len(edges),n))
        for e,(i,j) in enumerate(edges):
            ds[e,i]=1
            if j>=0: ds[e,j]=-1
        # Rational inputs with varied scales. Lower star guarantees SPD.
        lo=np.array([float(2.**int(rng.integers(-4,5))) for e in edges])
        hi=lo+np.array([float(2.**int(rng.integers(-3,8))) for e in edges])
        m=np.array([float(2.**int(rng.integers(-3,4))) for i in range(n)])
        base={'case':case,'edges':edges,'lo':lo.tolist(),'hi':hi.tolist(),'m':m.tolist()}
        if 'adaptive' not in found:
            for first in range(len(edges)):
                vals=[]
                for theta in [0.,.125,.25,.375,.5,.625,.75,.875,1.]:
                    ll=lo.copy();hh=hi.copy();ll[first]=hh[first]=lo[first]+theta*(hi[first]-lo[first])
                    score,second=one_step(ds,ll,hh,m,{first})
                    vals.append((theta,score,second))
                bound=max(vals[0][1],vals[-1][1]); best=max(vals,key=lambda x:x[1])
                if best[1]>bound*(1+1e-5):
                    found['adaptive']={**base,'first':first,'endpoint_bound':bound,'grid_values':vals}
                    print('FOUND adaptive',json.dumps(found['adaptive']),flush=True)
                    break
        if 'rank_two' not in found:
            for batch in itertools.combinations(range(len(edges)),2):
                # Rank-two query varying two coordinates together by common fraction.
                vals=[]
                for theta in [0.,.125,.25,.375,.5,.625,.75,.875,1.]:
                    ll=lo.copy();hh=hi.copy()
                    for e in batch:ll[e]=hh[e]=lo[e]+theta*(hi[e]-lo[e])
                    vals.append((theta,ratio(ds,ll,hh,m)))
                bound=max(vals[0][1],vals[-1][1]);best=max(vals,key=lambda x:x[1])
                if best[1]>bound*(1+1e-5):
                    found['rank_two']={**base,'batch':batch,'endpoint_bound':bound,'grid_values':vals}
                    print('FOUND rank_two',json.dumps(found['rank_two']),flush=True)
                    break
        checks=case+1
        if len(found)==2:break
        if case%500==0: print('cases',case,flush=True)
    result={'scope':'floating witness search; not proof','seed':140026,'cases':checks,'seconds':time.time()-start,'found':found}
    (ROOT/'policy_search_results.json').write_text(json.dumps(result,indent=2))
    return result

if __name__=='__main__':run()
