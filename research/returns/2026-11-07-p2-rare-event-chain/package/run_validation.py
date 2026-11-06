"""Independent finite comparisons plus a rare interacting-pattern computation.

The full generator below is used ONLY for the n=3 validation comparator.
The n=16 prediction uses no full-state list or generator.
"""
from chain_passage import *
from itertools import product
import json, time, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def serial(x):
    if isinstance(x,F):
        return str(x)
    if isinstance(x,C):
        return {'real':str(x.re),'imag':str(x.im)}
    if isinstance(x,Ball):
        return {'mid':serial(x.mid),'error':str(x.err)}
    if isinstance(x,dict):
        return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [serial(v) for v in x]
    return x


def save(name, value):
    (ROOT/name).write_text(json.dumps(serial(value),indent=2)+'\n')


def direct(chain, x, targets, s=F(0)):
    """EXACT full-state rational comparator. Never used by the predictor."""
    states=list(product((-1,1),repeat=chain.n)); ix={x:i for i,x in enumerate(states)}
    full=[[F(0) for _ in states] for _ in states]
    for k,v in enumerate(states):
        for i in range(chain.n):
            loc=(chain.a[i]*v[i-1] if i else 0)+(chain.b[i]*v[i+1] if i+1<chain.n else 0)
            rate=chain.lam[i]*(1-v[i]*loc)/2
            w=list(v);w[i]*=-1
            full[k][ix[tuple(w)]]+=rate;full[k][k]-=rate
    D=[v for v in states if v not in targets]
    M=[[C.make(s)*int(i==j)-full[ix[u]][ix[v]] for j,v in enumerate(D)] for i,u in enumerate(D)]
    inv=inverse_complex(M)
    row=inv[D.index(x)]
    h=[sum((row[j]*full[ix[v]][ix[a]] for j,v in enumerate(D)),C()) for a in targets]
    return h,sum(row,C()),len(states)


def competing_targets():
    bonds=[F(1,3),F(4,5)];clocks=[1,F(2,3),F(7,5)]
    x=(-1,1,-1);A=[(1,1,1),(-1,-1,-1)]
    data={'bonds':bonds,'clocks':clocks,'initial':x,'targets':A,'comparisons':{}}
    ch=Chain(bonds,clocks)
    s=C(F(2,5),F(3,7))
    t0=time.perf_counter();h,err,bank=passage_transform(ch,x,A,s,F(1,1<<12))
    elapsed=time.perf_counter()-t0
    truth,_,states=direct(ch,x,A,s)
    diffs=[(a-b).abs1() for a,b in zip(h,truth)]
    assert sum(diffs)<=err
    data['comparisons']['complex_transform']={'s':s,'prediction':h,'sum_error_bound':err,
        'exact':truth,'sum_complex_l1_discrepancy':sum(diffs),'kernel_records':len(bank.records),
        'seconds':elapsed,'stats':dict(ch.stats),'full_comparator_states':states}
    print('competing transform passed', 'seconds',round(elapsed,3),'nodes',len(bank.records),flush=True)
    save('competing_targets_record.json',data)
    ch=Chain(bonds,clocks)
    t0=time.perf_counter();rec=first_passage_mean(ch,x,A,F(1,256));elapsed=time.perf_counter()-t0
    q,exact,states=direct(ch,x,A)
    discrepancy=abs(rec['mid']-exact.re)
    assert discrepancy <= rec['error']
    data['comparisons']['mean']={**rec,'exact':exact.re,'discrepancy':discrepancy,'seconds':elapsed}
    print('competing mean passed',float(rec['mid']),'radius',float(rec['error']),'exact',str(exact.re),
          'seconds',round(elapsed,3),flush=True)
    save('competing_targets_record.json',data)
    ch=Chain(bonds,clocks)
    t0=time.perf_counter();ps=entrance_probabilities(ch,x,A,F(1,512));elapsed=time.perf_counter()-t0
    for rec,ex in zip(ps,q):
        assert abs(rec.mid.re-ex.re)<=rec.err
    data['comparisons']['entrance']={'prediction':ps,'exact':q,'seconds':elapsed,'stats':dict(ch.stats)}
    print('entrance passed',[float(r.mid.re) for r in ps],'seconds',round(elapsed,3),flush=True)
    save('competing_targets_record.json',data)
    return data


def rare_pattern():
    n=16
    bonds=([F(3,4),F(4,5),F(2,3)]*5)
    clocks=[1,F(2,3),F(7,5),F(5,4)]*4
    y=tuple(1 if i%2==0 else -1 for i in range(n))
    ch=Chain(bonds,clocks)
    t0=time.perf_counter();r=symmetric_mean(ch,y,F(1,1024));elapsed=time.perf_counter()-t0
    data={'n':n,'bonds':bonds,'clocks':clocks,'initial':tuple(-v for v in y),'target':y,
          'requested_relative':F(1,1024),'result':r,'seconds':elapsed,
          'full_state_count_not_constructed':1<<n,
          'g':ch.g,'G':ch.G,'mean_lower_bound':1/(ch.G*ch.stationary(y))}
    print('rare pattern', 'mean',float(r['mid']),'radius',float(r['error']),
          'stationary',str(r['stationary_target']),'seconds',round(elapsed,3),'stats',r['stats'],flush=True)
    save('rare_pattern_record.json',data)
    return data


if __name__=='__main__':
    which=sys.argv[1] if len(sys.argv)>1 else 'all'
    if which in ('competing','all'):
        competing_targets()
    if which in ('rare','all'):
        rare_pattern()
