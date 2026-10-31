#!/usr/bin/env python3
"""An ordinary acquired mixing certificate falsifies long-word query advantage."""
import itertools
import json
from pathlib import Path
import random
import time
import sympy as sp
from robust_replay import centers,compile_integer_replay,integer_step,integer_output,rounded
from verify import matrix
from check_replay import noncommon_fixture,actual


def acquire(boxes,b,mu,L,tol,p=12):
    start=time.perf_counter();C=centers(boxes);n=len(b);h=sp.ones(n,1)/n
    assert all(x>=0 for x in mu) and sum(mu)==1
    d=min(A[i,j]/h[j] for A in C for i in range(n) for j in range(n))
    xi=max(sum(abs(x) for x in A.T*h-h) for A in C)
    eta=max(sum(max(A[i,j]-lo[i,j],up[i,j]-A[i,j]) for j in range(n)) for (lo,up),A in zip(boxes,C) for i in range(n))
    M=max(abs(x) for x in b);q=sp.Rational(1,2**(p+1));D=sum(abs(x) for x in mu-h)
    rules=[]
    for l in range(L+1):
        const=M*(l*eta+D)+q
        direct=M*l*eta+(l+2)*q
        mode='constant' if const<=tol else 'full_center'
        assert const<=tol or direct<=tol
        rules.append({'length':l,'mode':mode,'bound':str(const if mode=='constant' else direct)})
        D=min(2,(1-d)*D+xi)
    return {'operators':C,'right':b,'output':mu,'length':L,'precision':p,'constant':rounded((h.T*b)[0],p),
            'rules':rules,'minorization':d,'drift':xi,'eta_inf':eta,'acquisition_seconds':time.perf_counter()-start,
            'retained_center_entries':sum(A.rows*A.cols for A in C)}


def batch(model,words):
    start=time.perf_counter();compiled=None;cache={};answers=[];actions=0;constant_answers=0
    for word in words:
        if len(word)>model['length'] or any(type(a) is not int or not 0<=a<len(model['operators']) for a in word):raise ValueError('word')
        if model['rules'][len(word)]['mode']=='constant':
            answers.append(model['constant']);constant_answers+=1;continue
        if compiled is None:
            compiled=compile_integer_replay(model['operators'],model['right'],model['output'],model['precision'])
            cache[()]=compiled['initial_grid_state']
        key=()
        for a in word:
            nxt=key+(a,)
            if nxt not in cache:cache[nxt],_=integer_step(compiled['operators'][a],cache[key]);actions+=1
            key=nxt
        answers.append(integer_output(compiled,cache[key]))
    return answers,{'seconds_including_any_fallback_compilation':time.perf_counter()-start,'constant_answers':constant_answers,
                    'new_vector_products':actions,'retained_prefix_states':len(cache),'fallback_compiled':compiled is not None}


def run():
    raw=json.loads(Path('observation_fixture.json').read_text())
    boxes=[tuple(matrix(X) for X in pair) for pair in raw['boxes']]
    b=matrix(raw['b']);mu=matrix(raw['ell']);L=30;tol=sp.Rational(1,100)
    model=acquire(boxes,b,mu,L,tol);A,bb,ll=noncommon_fixture();assert bb==b and ll==mu
    rng=random.Random(8421);words=[[0]*L,[1]*L,[0,1]*15,[1,0]*15]+[[rng.randrange(2) for _ in range(L)] for _ in range(36)]
    answers,ledger=batch(model,words);errors=[abs(x-actual(A,b,mu,w)) for x,w in zip(answers,words)]
    assert ledger['constant_answers']==40 and ledger['new_vector_products']==0
    assert all(e<=sp.Rational(model['rules'][L]['bound']) for e in errors);checks=41
    short=[w for l in range(7) for w in itertools.product(range(2),repeat=l)]
    ans,shortledger=batch(model,short)
    for x,w in zip(ans,short):assert abs(x-actual(A,b,mu,w))<=sp.Rational(model['rules'][len(w)]['bound']);checks+=1
    for l in range(7,L+1):
        for w in ([0]*l,[1]*l,[i%2 for i in range(l)]):
            x=batch(model,[w])[0][0];assert abs(x-actual(A,b,mu,w))<=sp.Rational(model['rules'][l]['bound']);checks+=1
    return {'checks':checks,'minorization':str(model['minorization']),'reference_drift_l1':str(model['drift']),
            'eta_inf':str(model['eta_inf']),'constant_answer':str(model['constant']),
            'constant_lengths':[r['length'] for r in model['rules'] if r['mode']=='constant'],
            'all_horizon_rules':model['rules'],'acquisition_seconds':model['acquisition_seconds'],
            'retained_center_entries':model['retained_center_entries'],'long_word_batch':ledger,'short_word_batch':shortledger,
            'maximum_long_word_error':float(max(errors)),
            'scope':'Same observed intervals and admitted all-length task. Ordinary acquired mixing plus paid full-center fallback; no exact common stationarity assumed. This removes the apparent reduced-rank query advantage on the long-word batch.'}


if __name__=='__main__':
    out=run();Path('mixing_baseline_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
