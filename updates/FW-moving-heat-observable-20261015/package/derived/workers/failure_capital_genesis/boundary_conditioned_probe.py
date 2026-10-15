"""Independent floating exploration of exact boundary-conditioned avalanche law.

No source imports. This is a real-arithmetic sampler derivation diagnostic, not
a finite-bit certificate or physical-model validation. N is fixed per probe.
"""
import argparse, json, math, time
from pathlib import Path
import numpy as np


def largest_stable(s, F, present):
    return max([0] + [k for k in range(1, len(s)+1)
                     if np.count_nonzero(present & (s*k > F)) >= k])


def lifetime(s, F, temp, E):
    n = len(s)
    alive = np.ones(n, dtype=bool)
    order = np.argsort(E, kind='stable')
    weak, scan, k, internal, physical = n-1, 0, n, 0., 0.
    def close(weak, k):
        while weak >= 0:
            if not alive[weak]:
                weak -= 1
                continue
            if s[weak]*k > F:
                break
            alive[weak] = False
            k -= 1
            weak -= 1
            if not k:
                break
        return weak, k
    weak, k = close(weak, k)
    while k:
        while not alive[order[scan]]:
            scan += 1
        i = order[scan]
        scan += 1
        physical += (E[i]-internal)*math.exp(-F/(k*temp))
        internal = E[i]
        alive[i] = False
        k -= 1
        if k:
            weak, k = close(weak, k)
    return physical


def prepare(s, F, temp, deadline, m=None):
    s = np.sort(np.asarray(s))[::-1]
    n = len(s)
    deficit = [np.count_nonzero(s*k > F)-k+1 for k in range(1,n+1)]
    if m is None:
        m = int(np.argmax(deficit))+1
    u = deadline*math.exp(F/(m*temp))
    lam = np.exp(-s/temp)
    failed = -np.expm1(-lam*u)
    present = np.exp(-lam*u)
    h = np.ones((n+1,n+1))
    gate = np.ones((n,n+1),dtype=bool)
    c = np.arange(n+1)
    for j in range(n-1,-1,-1):
        gate[j] = (c < m) | (s[j]*c <= F)
        weighted = h[j+1]*gate[j]
        h[j] = failed[j]*weighted
        h[j,:-1] += present[j]*weighted[1:]
    assert h[0,0] > 0
    return dict(s=s,F=F,temp=temp,deadline=deadline,m=m,u=u,lam=lam,
                failed=failed,present=present,h=h,gate=gate,
                event_probability=float(h[0,0]),rstar=int(max(deficit)))


def sample(model,rng):
    n=len(model['s']); c=0; bits=np.zeros(n,dtype=bool)
    for j in range(n):
        denominator=model['h'][j,c]
        numerator=(model['present'][j]*model['gate'][j,c+1]
                   *model['h'][j+1,c+1])
        assert denominator>0 and -1e-14<=numerator/denominator<=1+1e-14
        if rng.random()<numerator/denominator:
            bits[j]=True;c+=1
    U=rng.random(n)
    E=np.empty(n)
    E[bits]=model['u']-np.log(U[bits])/model['lam'][bits]
    E[~bits]=-np.log1p(-U[~bits]*model['failed'][~bits])/model['lam'][~bits]
    return bits,E


def run(n,deadline,N,seed,m=None):
    s=np.random.RandomState(0).rand(n)
    F=7*n/40;temp=3/20
    start=time.perf_counter();model=prepare(s,F,temp,deadline,m)
    prep=time.perf_counter()-start
    rng=np.random.default_rng(seed);hits=0;times=[];maxk=0
    start=time.perf_counter()
    for i in range(N):
        bits,E=sample(model,rng)
        if i<20:
            kk=largest_stable(model['s'],F,bits)
            assert kk<model['m'];maxk=max(maxk,kk)
        value=lifetime(model['s'],F,temp,E)
        times.append(value);hits+=value<=deadline
    elapsed=time.perf_counter()-start
    accept=hits/N
    return dict(scope='Uncertified binary64 exploration; no exact sampling claim',
                n=n,F=F,temp=temp,deadline=deadline,m=model['m'],rstar=model['rstar'],
                u=model['u'],boundary_probability=model['event_probability'],
                samples_fixed=N,seed=seed,hits=int(hits),acceptance=accept,
                probability_estimate=model['event_probability']*accept,
                relative_second_moment_empirical=(1/accept if accept else None),
                minimum_tau=min(times),median_tau=float(np.median(times)),
                prepare_seconds=prep,sampling_seconds=elapsed,
                h_storage_bytes=model['h'].nbytes,
                conditional_sample_max_checked_K=int(maxk))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=100)
    p.add_argument('--deadline',type=float,default=.1)
    p.add_argument('--N',type=int,default=10000);p.add_argument('--seed',type=int,default=2026101501)
    p.add_argument('--m',type=int);p.add_argument('--out',type=Path)
    a=p.parse_args();result=run(a.n,a.deadline,a.N,a.seed,a.m)
    if a.out:a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
