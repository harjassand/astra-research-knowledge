#!/usr/bin/env python3
"""Equally informed retaining methods share the same task/metric/certificate."""
import json
from pathlib import Path
import random
import time
import sympy as sp
from learn import (metric,residual,inner,measure,sum_kernel,acquire,encode,
                   evaluate,exact,fixture)
from verify import verify


def from_directions(mats,b,c,length,tolerance,directions):
    pi,adj,alpha=metric(mats);n=mats[0].rows;m=len(mats)
    basis=[];images=[[[] for _ in mats] for _ in range(2)];mvps=0
    for x in [sp.ones(n,1),b,c]+directions:
        v=residual(x,basis,pi)
        if v==sp.zeros(n,1):continue
        j=max(range(n),key=lambda i:abs(v[i]));v=v/v[j]
        basis.append(v)
        for side,ops in enumerate((mats,adj)):
            for a,A in enumerate(ops):images[side][a].append(A*v);mvps+=1
    (in2,out2),_=measure(basis,images,pi,m)
    bound=((in2+out2)/2)**2*sum_kernel(length,alpha)**2*inner(b,b,pi)*inner(c,c,pi)
    if bound>tolerance**2:return None,{'rank':len(basis),'certificate_pass':False,'verification_action_mvps':mvps}
    V=sp.Matrix.hstack(*basis);H=sp.diag(*pi);G=V.T*H*V
    model={'basis':V,'gram':G,'operators':[G.inv()*V.T*H*A*V for A in mats],
           'left':G.inv()*V.T*H*c,'right':G.inv()*V.T*H*b,'pi':pi,
           'alpha':alpha,'length':length,'tolerance':tolerance,'stopping':'quadratic',
           'quadratic_error_bound_squared':bound,
           'state_error_bound_squared':length**2*in2*inner(b,b,pi)*inner(c,c,pi),
           'rounds':[],'ledger':{'rank':len(basis)}}
    return model,{'rank':len(basis),'certificate_pass':True,'verification_action_mvps':mvps}


def randomized_joint_range(mats,b,c,length,tol):
    tic=time.perf_counter();pi,adj,_=metric(mats);n=len(b);m=len(mats)
    rng=random.Random(771)
    starts=[sp.Matrix([rng.choice([-1,1]) for _ in range(n)]) for _ in range(2)]
    current=starts;trials=[];construction_mvps=0;verification_mvps=0
    # A real retained power ladder. Every unsuccessful certificate is charged.
    for q in range(9):
        if q:
            current=[sum((adj[a]*mats[a]*x for a in range(m)),sp.zeros(n,1))/m for x in current]
            construction_mvps+=2*m*len(current)
        model,row=from_directions(mats,b,c,length,tol,current)
        row['power']=q;trials.append(row);verification_mvps+=row['verification_action_mvps']
        if model is not None:
            return model,{'acquisition_seconds':time.perf_counter()-tic,'power_ladder_mvps':construction_mvps,
                         'all_candidate_verification_mvps':verification_mvps,'trials':trials}
    return None,{'acquisition_seconds':time.perf_counter()-tic,'power_ladder_mvps':construction_mvps,
                 'all_candidate_verification_mvps':verification_mvps,'trials':trials,
                 'scope':'Budget exhausted, not proof of no useful subspace.'}


def retained_prefix_queries(operators,b,left,words):
    tic=time.perf_counter();cache={():b};answers=[];mvps=0
    for word in words:
        prefix=()
        for a in word:
            nxt=prefix+(a,)
            if nxt not in cache:cache[nxt]=operators[a]*cache[prefix];mvps+=1
            prefix=nxt
        answers.append((left.T*cache[prefix])[0])
    elapsed=time.perf_counter()-tic
    maxbits=max(max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for v in cache.values() for x in v)
    serialized=json.dumps([[[int(x.p),int(x.q)] for x in v] for v in cache.values()],separators=(',',':'))
    return answers,{'query_seconds':elapsed,'retained_prefixes':len(cache),'vector_products':mvps,
                    'retained_scalar_entries':sum(len(v) for v in cache.values()),
                    'max_retained_integer_bits':maxbits,'rational_state_payload_bytes':len(serialized.encode())}


def run():
    mats,b,c=fixture();length=30;tol=sp.Rational(1,100000)
    pi,_,_=metric(mats);H=sp.diag(*pi)
    rng=random.Random(8421)
    words=[[0]*length,[1]*length,[0,1]*15,[1,0]*15]+[[rng.randrange(2) for _ in range(length)] for _ in range(16)]
    truth,ordinary=retained_prefix_queries(mats,b,H*c,words)
    greedy=acquire(mats,b,c,length,tol)
    rg,random_ledger=randomized_joint_range(mats,b,c,length,tol)
    rows={'retained_full_space_prefix_method':ordinary}
    for label,model,acqledger in [('retained_bidirectional_Krylov',greedy,greedy['ledger']),
                                 ('retained_randomized_joint_normal_range',rg,random_ledger)]:
        if model is None:
            rows[label]={'admitted':False,'acquisition':acqledger};continue
        start=time.perf_counter();assert verify(mats,b,c,encode(model),expected_length=length,expected_tolerance=tol);check_seconds=time.perf_counter()-start
        out,ql=retained_prefix_queries(model['operators'],model['right'],model['gram']*model['left'],words)
        errs=[abs(x-y) for x,y in zip(out,truth)]
        assert all(e**2<=model['quadratic_error_bound_squared'] for e in errs)
        saving=(ordinary['query_seconds']-ql['query_seconds'])/len(words)
        cost=acqledger.get('acquisition_seconds',0)+check_seconds
        rows[label]={'admitted':True,'rank':model['basis'].cols,'acquisition':acqledger,
                     'extra_exact_verification_seconds':check_seconds,'queries':ql,
                     'maximum_actual_error_float':float(max(errs)),
                     'illustrative_break_even_query_count':None if saving<=0 else cost/saving,
                     'scope':'Same uniform quadratic certificate; not a distinct new learner or universal performance claim.'}
    return {'scope':'Small exact-rational falsification fixture. Every comparator retains prior work and sees identical raw kernels/task data. No strong-baseline superiority or consequential practical payoff is established.',
            'word_count':len(words),'horizon':length,'methods':rows}


if __name__=='__main__':
    out=run();Path('strong_comparison_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
