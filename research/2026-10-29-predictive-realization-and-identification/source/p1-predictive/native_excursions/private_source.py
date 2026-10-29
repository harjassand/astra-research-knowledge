"""Private synthetic source. No constructor output enters the consumer."""
from fractions import Fraction as F
import numpy as np

def source(kind='original'):
    wb=[F(1),F(5,4),F(3,4),F(3,2)]
    if kind=='macro': wb+=[F(1),F(9,8)]
    m=len(wb);weights=wb+[F(1,2)]*(2*m)
    C=[[F(0) for _ in weights] for _ in weights]
    def edge(i,j,v):
        C[i][j]+=v; C[j][i]+=v
    for i in range(m):
        edge(i,(i+1)%m,F(1,8))
        for k in range(2): edge(i,m+2*i+k,(weights[i]-F(1,4))/2)
    if kind=='macro':
        for region in range(3):
            for k in range(4):edge(m+4*region+k,m+4*region+(k+1)%4,F(1,16))
    else:
        for i in range(2*m):edge(m+i,m+(i+1)%(2*m),F(1,16))
    L=[[(-C[i][j] if i!=j else sum(C[i])) for j in range(3*m)] for i in range(3*m)]
    rates=np.array([[float(C[i][j]/weights[i]) for j in range(3*m)] for i in range(3*m)])
    lambdas=rates.sum(axis=1)
    assert all(sum(C[i])/weights[i]==1 for i in range(m))
    assert all(sum(C[i][:m])/weights[i]>=F(1,2) for i in range(m,3*m))
    return weights,L,rates,lambdas

def sample_port(port,n,seed,horizon=24.0,tick_scale=2**20,kind='original'):
    """Actual individual trajectories, stopped on next port or censor time.

    Hidden states drive the backend but are never emitted to inference.
    One native initial hold and initial jump per independently reset trial.
    Hidden jumps are simulated individually in vectorized batches, not by
    sampling an aggregate endpoint/time law.
    """
    _,_,rates,lambdas=source(kind);m=len(rates)//3
    rng=np.random.Generator(np.random.PCG64(seed))
    probs=rates/lambdas[:,None]
    cdf=np.cumsum(probs,axis=1); cdf[:,-1]=1.0
    holds=rng.exponential(1/lambdas[port],n)
    states=np.searchsorted(cdf[port],rng.random(n),side='right')
    elapsed=np.zeros(n)
    endpoint=np.where(states<m,states,-1).astype(np.int16)
    active=np.flatnonzero(states>=m)
    event_count=n
    censored_internal_waits=0
    while len(active):
        dt=rng.exponential(1/lambdas[states[active]])
        end=elapsed[active]+dt
        cens=end>=horizon
        if np.any(cens):
            ci=active[cens]; elapsed[ci]=horizon
            censored_internal_waits+=len(ci)
        vi=active[~cens]
        elapsed[vi]=end[~cens]
        if not len(vi): break
        uv=rng.random(len(vi))
        nxt=(uv[:,None]>=cdf[states[vi]]).sum(axis=1)
        states[vi]=nxt
        event_count+=len(vi)
        hit=nxt<m
        endpoint[vi[hit]]=nxt[hit]
        active=vi[~hit]
    ticks=np.floor(elapsed*tick_scale).astype(np.uint32)
    # Only public endpoints and timestamps, not hidden-state traces, leave.
    return endpoint,ticks,{
        'preparations':n,'initial_jumps':n,'total_native_jumps':int(event_count),
        'censored_interior_holds':int(censored_internal_waits),
        'elapsed_native_time':float(holds.sum()+elapsed.sum()),
        'initial_holding_time':float(holds.sum()),
        'terminal_boundary_or_pending_reports':n,
        'initial_departure_reports':n,
    }
