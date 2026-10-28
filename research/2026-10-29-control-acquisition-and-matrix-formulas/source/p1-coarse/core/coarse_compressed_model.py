"""Fit a small positive model, certify it through the acquired prefix cover.

The proposal uses familiar two-dimensional moment realization. Its assumed
dimension is not a source promise: the finite cover checks every future word.
No new source observations are requested.
"""
from fractions import Fraction as F
from pathlib import Path
from math import sqrt
import json

ROOT=Path(__file__).resolve().parents[1]

def propose(raw):
    data=raw['balanced_tapes']['counts_by_prefix']
    f=lambda w: data[w]['survived']/data[w]['assigned_trials']
    maps=[]
    cross=f('01')-f('0')*f('1')
    for i in ('0','1'):
        a=f(i); b2=f(i*2)-a*a
        assert b2>0
        b=sqrt(b2)*(1 if i=='0' or cross>=0 else -1)
        c=(f(i*3)-a**3-2*a*b2)/b2
        kernel=[[(a+c)/2+b,(a-c)/2],[(a-c)/2,(a+c)/2-b]]
        maps.append([[F(round(x*10**6),10**6) for x in row] for row in kernel])
    return maps

def probability(maps,word):
    p=[F(1,2),F(1,2)]
    for i in word:
        a=maps[int(i)]
        p=[sum(a[j][k]*p[k] for k in range(2)) for j in range(2)]
    return sum(p)

def run():
    raw=json.loads((ROOT/'results'/'COARSE_SWITCHING_RAW_RECEIPTS.json').read_text())
    acquired=json.loads((ROOT/'results'/'COARSE_SWITCHING_COVER.json').read_text())
    maps=propose(raw)
    for a in maps:
        assert a[0][1]==a[1][0]
        assert all(x>=0 for row in a for x in row)
        assert all(sum(row)<=1 for row in a)
    target=F(acquired['cover']['all_word_error'])
    checks=[]
    total_bound=F(0)
    branch_bound=F(0)
    for word,node in acquired['cover']['nodes'].items():
        prediction=probability(maps,word)
        lo,hi=map(F,node['interval'])
        if node['kind']=='terminal':
            bound=max(hi,prediction)
        else:
            bound=max(abs(lo-prediction),abs(hi-prediction))
            branch_bound=max(branch_bound,bound)
        assert bound<=target,(word,bound,target)
        total_bound=max(total_bound,bound)
        checks.append(dict(word=word,kind=node['kind'],prediction=str(prediction),
                           error_or_all_extension_bound=str(bound)))
    result=dict(maps=[[[str(x) for x in row] for row in a] for a in maps],
                model_initial_distribution=['1/2','1/2'],model_readout='total survival',
                finite_model_dimension=2,hidden_source_dimension_upper_bound=None,
                uniform_all_switching_error=str(total_bound),
                uniform_all_switching_error_float=float(total_bound),
                retained_branch_error_bound=str(branch_bound),
                retained_branch_error_bound_float=float(branch_bound),
                future_word_checks=checks,new_source_queries=0,
                source_confidence_event_unchanged=True,
                proof='Every word either ends at a saved branch or extends a terminal prefix. Finite interval checks cover the former. Both the actual absorbing process and the positive substochastic candidate have nonincreasing total survival, so the latter error is at most the larger prefix survival upper. Empty word is exact.',
                scope='A certified two-state approximation, not identification of a two-state source. Known moment realization and positive model fitting supply the proposal; the acquired finite prefix cover supplies its all-word certificate.')
    (ROOT/'results'/'COARSE_COMPRESSED_MODEL.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='future_word_checks'},indent=2))

if __name__=='__main__':run()
