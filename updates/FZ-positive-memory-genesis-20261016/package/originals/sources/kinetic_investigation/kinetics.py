"""Independent NumPy/Numba implementation of published spatial Schloegl dynamics.
No neural-network code is reproduced. Rates follow NNCME-2 system definition.
Target: first entry by T into every-site count <= threshold, not endpoint occupancy.
"""
from __future__ import annotations
import numpy as np
from numba import njit

C1,C2,C3,C4,D = 2.676,0.040,108.102,37.881,8.2207

def grid_edges(rows:int, cols:int)->np.ndarray:
    out=[]
    for i in range(rows):
        for j in range(cols):
            a=i*cols+j
            for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni,nj=i+di,j+dj
                if 0<=ni<rows and 0<=nj<cols:
                    out.append((a,ni*cols+nj))
    return np.asarray(out,dtype=np.int64).reshape(-1,2)

@njit(cache=True)
def evolve(states,times,edges,deadline,level,seed,cap=-1):
    """SSA to first interface hit or deadline; cap=-1 gives no population cutoff.
    cap>=0 suppresses reactions whose target count would exceed cap.
    Rates use falling factorials with published c_i (no additional factorials).
    """
    np.random.seed(seed)
    count,L=states.shape
    out=states.copy(); tout=times.copy(); ok=np.zeros(count,np.bool_)
    jumps=np.zeros(count,np.int64); peak=np.zeros(count,np.int64)
    rates=np.empty(2*L+len(edges))
    for k in range(count):
        x=out[k]
        t=times[k]
        nsteps=0; maximum=np.max(x)
        while True:
            mx=np.max(x)
            if mx<=level:
                ok[k]=True
                break
            if t>=deadline:
                break
            total=0.0
            for i in range(L):
                n=x[i]
                b=C1*n*(n-1)+C3
                a=C2*n*(n-1)*(n-2)+C4*n
                if cap>=0 and n>=cap: b=0.0
                rates[2*i]=b; rates[2*i+1]=a
                total+=b+a
            for e in range(len(edges)):
                a,b=edges[e]
                rate=D*x[a]
                if cap>=0 and x[b]>=cap: rate=0.0
                rates[2*L+e]=rate
                total+=rate
            dt=-np.log(np.random.random())/total
            if t+dt>deadline:
                t=deadline
                break
            t+=dt
            choose=np.random.random()*total
            r=0
            while r<len(rates)-1 and choose>=rates[r]:
                choose-=rates[r]; r+=1
            if r<2*L:
                i=r//2
                x[i]+=1 if r%2==0 else -1
            else:
                a,b=edges[r-2*L]
                x[a]-=1; x[b]+=1
            nsteps+=1
            if np.max(x)>maximum: maximum=np.max(x)
        tout[k]=t; jumps[k]=nsteps; peak[k]=maximum
    return out,tout,ok,jumps,peak


def splitting(rows=2,cols=4,particles=128,seed=1749,deadline=1.0,
              levels=(45,40,35,30,25,20,15),cap=-1):
    """Fixed-level sequential Monte Carlo. Whole-particle resampling only;
    original physical dynamics on every segment, with residual time retained.
    Product estimator targets a finite-horizon hitting event.
    Independent repetitions, not within-run binomial errors, assess uncertainty.
    """
    import time
    rng=np.random.default_rng(seed)
    x=np.full((particles,rows*cols),50,dtype=np.int64)
    t=np.zeros(particles); edges=grid_edges(rows,cols)
    p=1.0; records=[]
    for level in levels:
        start=time.perf_counter()
        x,t,ok,jumps,peak=evolve(x,t,edges,deadline,level,
                                int(rng.integers(0,2**31-1)),cap)
        n=int(ok.sum()); p*=n/particles
        records.append(dict(level=int(level),successes=n,particles=particles,
                            factor=n/particles,probability_product=p,
                            events=int(jumps.sum()),max_count=int(peak.max()),
                            mean_success_time=float(t[ok].mean()) if n else None,
                            wall_seconds=time.perf_counter()-start))
        if n==0: break
        keep=rng.choice(np.flatnonzero(ok),size=particles,replace=True)
        x=x[keep].copy(); t=t[keep].copy()
    return dict(seed=seed,shape=[rows,cols],particles=particles,deadline=deadline,
                levels=list(levels),cap=cap,estimate=p,stages=records,
                total_events=sum(r['events'] for r in records))

if __name__=='__main__':
    import argparse,json,time,sys
    parser=argparse.ArgumentParser(); parser.add_argument('--mode',choices=['ssa','split'],default='split')
    parser.add_argument('--particles',type=int,default=128);parser.add_argument('--seed',type=int,default=1749)
    parser.add_argument('--rows',type=int,default=2);parser.add_argument('--cols',type=int,default=4)
    parser.add_argument('--cap',type=int,default=-1);parser.add_argument('--output',default='result.json')
    a=parser.parse_args()
    warm=time.perf_counter()
    evolve(np.full((1,2),50,np.int64),np.zeros(1),grid_edges(1,2),1e-5,15,0,a.cap)
    warm=time.perf_counter()-warm
    start=time.perf_counter()
    if a.mode=='split':
        result=splitting(a.rows,a.cols,a.particles,a.seed,cap=a.cap)
    else:
        x,t,hit,jumps,peak=evolve(np.full((a.particles,a.rows*a.cols),50,np.int64),np.zeros(a.particles),grid_edges(a.rows,a.cols),1.,15,a.seed,a.cap)
        result=dict(shape=[a.rows,a.cols],particles=a.particles,deadline=1.,cap=a.cap,
                    seed=a.seed,hits=int(hit.sum()),estimate=float(hit.mean()),
                    total_events=int(jumps.sum()),max_count=int(peak.max()))
    result['wall_seconds']=time.perf_counter()-start
    result['jit_warmup_seconds']=warm
    with open(a.output,'w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
