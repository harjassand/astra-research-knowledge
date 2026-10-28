"""Execute the stronger ordinary adaptive-prefix baseline on the same source.

Fresh data only, with the separately proved midpoint-terminal theorem.
No lifetime pilot or old receipt is used by the acquisition policy.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import deque
from math import ceil
import json,sys
import numpy as np
from coarse_switching_cover import PrivateInstrument, fast_probability
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'branches'/'physical'))
from multiboundary_positive_events import log_bounds


def batch_size(j,eps=F(1,16),delta=F(1,1000)):
    multiplier=2/(eps*eps)
    # Float is unnecessary: upper rational logarithm fixes the paid batch.
    target=multiplier*log_bounds(2*j*(j+1)/delta)[1]
    n=(target.numerator+target.denominator-1)//target.denominator
    assert F(n)>=target
    return n


def query(inst,word,n):
    micro,level=inst.prepare(n)
    active=np.arange(n)
    live=[n];steps=0
    for i in word:
        steps+=len(active)
        active=inst.step(micro,level,active,np.full(len(active),int(i),dtype=np.int64))
        live.append(len(active))
    assert steps==sum(live[:-1])
    return dict(word=word,trials=n,survived=len(active),survivors_by_depth=live,
                primitive_applications=steps,coarse_observations=steps,
                fresh_preparations=n)


def node(r,eps=F(1,16)):
    center=F(r['survived'],r['trials']);radius=eps/2
    lo=max(F(0),center-radius);hi=min(F(1),center+radius)
    terminal=hi<=2*eps
    pred=hi/2 if terminal else (lo+hi)/2
    bound=hi/2 if terminal else (hi-lo)/2
    assert bound<=eps
    return dict(kind='terminal' if terminal else 'branch',
                interval=[str(lo),str(hi)],prediction=str(pred),
                error_bound=str(bound))


def acquire():
    inst=PrivateInstrument(seed=2026102905)
    queue=deque(['0','1']);receipts=[]
    while queue:
        word=queue.popleft();j=len(receipts)+1
        r=query(inst,word,batch_size(j));receipts.append(r)
        if node(r)['kind']=='branch':queue.extend([word+'0',word+'1'])
    return receipts


def infer(receipts):
    queue=deque(['0','1']);cover={}
    for j,r in enumerate(receipts,1):
        assert queue and r['word']==queue.popleft()
        assert r['trials']==batch_size(j)
        assert r['survivors_by_depth'][0]==r['trials']
        assert r['survivors_by_depth'][-1]==r['survived']
        assert r['primitive_applications']==sum(r['survivors_by_depth'][:-1])
        out=node(r);cover[r['word']]=out
        if out['kind']=='branch':queue.extend([r['word']+'0',r['word']+'1'])
    assert not queue
    for w,item in cover.items():
        if item['kind']=='branch':assert w+'0' in cover and w+'1' in cover
    return dict(nodes=cover,maximum_prefix_length=max(map(len,cover)),
                terminal_nodes=sum(x['kind']=='terminal' for x in cover.values()),
                branch_nodes=sum(x['kind']=='branch' for x in cover.values()),
                all_word_absolute_error='1/16',failure_probability_upper='1/1000',
                confidence='Conditional fixed-batch Hoeffding; node j spends delta/[j(j+1)]. All samples at that node are fresh after its word and batch size are fixed.',
                terminal_semantics='At a terminal prefix and every extension, predict half its survival upper. This bounded absolute-error predictor need not converge to zero at infinite length.')


def hidden_check(cover,levels=8):
    omitted=F(1,1024*(1<<levels));max_error=F(0)
    for w,item in cover['nodes'].items():
        true_lo=F(1023,1024)*fast_probability(w)
        for ell in range(levels):
            true_lo+=F(1,1024*(1<<(ell+1)))*fast_probability(w,ell)
        true_hi=true_lo+omitted
        lo,hi=map(F,item['interval'])
        assert lo<=true_lo<=true_hi<=hi
        prediction=F(item['prediction'])
        max_error=max(max_error,abs(prediction-true_lo),abs(prediction-true_hi))
    return dict(nodes_checked=len(cover['nodes']),
                maximum_node_error_upper=str(max_error),
                omitted_source_probability_upper=str(omitted),
                role='Private exact validation only; hidden source parameters do not enter acquisition or the confidence cover.')


def run(replay=False):
    p=ROOT/'results'/'ADAPTIVE_COARSE_RAW_RECEIPTS.json'
    raw=json.loads(p.read_text()) if replay else acquire()
    if not replay:p.write_text(json.dumps(raw,indent=2)+'\n')
    cover=infer(raw)
    costs={k:sum(r[k] for r in raw) for k in
           ('primitive_applications','coarse_observations','fresh_preparations')}
    result=dict(cover=cover,complete_costs=costs,private_check=hidden_check(cover),
                uses_prior_receipts=False,uses_lifetime_pilot=False,
                source='Same private countable reversible source as coarse_switching_cover.py, independent new seed and preparations.',
                comparison_scope='Same uniform absolute total-survival task and live/absorbed interface. This prefix predictor has a different representation and terminal extrapolation from the certified two-state model.')
    (ROOT/'results'/'ADAPTIVE_COARSE_COVER.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(costs=costs,cover={k:v for k,v in cover.items() if k!='nodes'},
                         private_check=result['private_check']),indent=2))

if __name__=='__main__':run('--replay' in sys.argv)
