"""Reproducible cost benchmark: exact static envelope scan vs mutable update.

Measures setup and 1,000 local state proposals on identical random paths. The
static reference is vectorized NumPy (C loops), while the online prototype uses
Python lazy segment trees; this is a conservative implementation comparison.
"""
import json, os, sys, time, tracemalloc
import numpy as np
sys.path.insert(0,os.path.dirname(__file__))
from online_entropy import MutableHopfLax, Query


def direct_many(breaks,states,queries,left=.15,right=-.12):
    widths=np.diff(breaks)
    c=np.r_[0.,np.cumsum(states*widths)]
    out=np.empty(len(queries))
    l,r=breaks[0],breaks[-1]
    for qi,q in enumerate(queries):
        x,t=q.x,q.t
        y=x-t*states
        vals=np.where(y<breaks[:-1],c[:-1]+(x-breaks[:-1])**2/(2*t),
             np.where(y>breaks[1:],c[1:]+(x-breaks[1:])**2/(2*t),
                      c[:-1]+states*(x-breaks[:-1])-.5*t*states**2))
        yl=x-t*left
        vl=(left*(x-l)-.5*t*left**2 if yl<=l else (x-l)**2/(2*t))
        yr=x-t*right
        vr=(c[-1]+right*(x-r)-.5*t*right**2 if yr>=r else c[-1]+(x-r)**2/(2*t))
        out[qi]=min(vl,vr,float(np.min(vals)))
    return out


def one_run(n=1024,m=64,updates=1000,seed=5):
    rng=np.random.default_rng(seed)
    breaks=np.linspace(-2,2,n+1)
    state=rng.uniform(-.8,.8,n)
    # M interval-average sensors at irregular positions and four acquisition times.
    centers=rng.uniform(-1.8,1.8,m)
    widths=rng.uniform(.015,.08,m)
    times=rng.choice([.05,.12,.25,.5],size=m)
    queries=[]; intervals=[]
    for x,w,t in zip(centers,widths,times):
        li=len(queries); queries += [Query(x-w/2,t),Query(x+w/2,t)]
        intervals.append((li,li+1,w))
    edits=[(int(rng.integers(n)),float(rng.uniform(-.8,.8))) for _ in range(updates)]

    tracemalloc.start()
    tic=time.perf_counter()
    eng=MutableHopfLax(breaks,state,queries,left_state=.15,right_state=-.12)
    setup=time.perf_counter()-tic
    _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    tree_bytes=sum(t.mn.nbytes+t.arg.nbytes+t.lazy.nbytes for t in eng.trees)

    # Online updates, root minima are exact sensor endpoint potentials.
    online_state=state.copy(); checksum=0.
    tic=time.perf_counter()
    for j,v in edits:
        tx=eng.update_cell(j,v)
        checksum += sum(t.minimum for t in eng.trees)
        tx.commit(); online_state[j]=v
    online=time.perf_counter()-tic

    # Full recomputation from scratch for every proposed state. Each endpoint is
    # evaluated by vectorized O(N) scan; includes O(N) primitive construction.
    scan_state=state.copy(); checkscan=0.
    tic=time.perf_counter()
    for j,v in edits:
        scan_state[j]=v
        checkscan += float(np.sum(direct_many(breaks,scan_state,queries,.15,-.12)))
    scan=time.perf_counter()-tic
    # Check final exact states and all endpoint potentials.
    ref=direct_many(breaks,scan_state,queries,.15,-.12)
    got=np.array([eng.potential(k) for k in range(len(queries))])
    assert np.max(np.abs(ref-got))<2e-10
    assert np.array_equal(online_state,scan_state)
    return {
      'N_cells':n,'M_interval_sensors':m,'Q_endpoints':len(queries),
      'local_proposals':updates,'setup_seconds_online':setup,
      'online_seconds_proposals':online,'scan_seconds_proposals':scan,
      'scan_over_online_proposal_speedup':scan/online,
      'online_total_setup_plus_updates_seconds':setup+online,
      'scan_total_seconds':scan,
      'amortized_total_speedup_including_setup':scan/(setup+online),
      'tree_storage_MiB':tree_bytes/2**20,
      'python_peak_tracemalloc_MiB':peak/2**20,
      'final_max_abs_envelope_error':float(np.max(np.abs(ref-got))),
      'checksum_delta':float(abs(checksum-checkscan)),
      'status':'pass'}


if __name__=='__main__':
    cases=[]
    for n,m,r in [(256,32,400),(1024,64,500),(4096,64,300)]:
        cases.append(one_run(n,m,r))
    print(json.dumps(cases,indent=2))
