#!/usr/bin/env python3
"""Exact finite certificates for the Astra clock-lift research note.

Python 3.10+; numpy and scipy are needed only for the optional --search run.
No network access. Core counterexample checks use integer arithmetic only.
LP solutions are never treated as proofs without exact rational verification.
This program does NOT prove the universal cover-balance conjecture or novelty.

Usage:
  python astra_clock_lift_verify.py --output astra_clock_lift_results.json
  python astra_clock_lift_verify.py --search --trials 40 --scales 12 \
      --output astra_clock_lift_results.json
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import itertools
import json
from pathlib import Path
import random
import sys

P = 5
B = ((1,0,0,4,3),(0,1,0,1,1),(0,0,1,2,0))
A = ((1,4,3,1,0),(2,4,0,0,1))


def mv(a, x, p):
    return tuple(sum(ai*xi for ai,xi in zip(row,x)) % p for row in a)


def rowspace(b, p):
    return tuple(tuple(sum(cj*row[i] for cj,row in zip(c,b)) % p
                       for i in range(len(b[0])))
                 for c in itertools.product(range(p), repeat=len(b)))


def supports(vectors, x, p):
    good = [v for v in vectors
            if any(v) and all(vi in (0,xi,(-xi)%p) for vi,xi in zip(v,x))]
    return sorted(set(tuple(int(vi != 0) for vi in v) for v in good))


def core_checks():
    v = rowspace(B,P)
    assert len(set(v)) == 125
    assert all(mv(A,w,P)==(0,0) for w in v)
    for x in itertools.product((1,2), repeat=5):
        ss=supports(v,x,P)
        assert all(any(s[i] for s in ss) for i in range(5))
    s0=supports(v,(1,1,1,1,1),P)
    sp=supports(v,(2,2,2,2,1),P)
    sq=supports(v,(2,2,2,2,2),P)
    assert s0==[(0,1,0,1,1),(0,1,1,1,1),(1,1,0,0,1)]
    assert sp==[(1,0,0,1,1),(1,0,1,1,1),(1,1,1,0,1),(1,1,1,1,1)]
    assert sq==s0
    dual=(-1,1,0,-1,0)
    assert sum(dual)==-1
    assert all(sum(yi*si for yi,si in zip(dual,s))==0 for s in s0)
    assert all(s[0]==s[4] for s in sp)
    assert all(s[0]+s[3]==s[1]==s[4] for s in sq)
    # These identities force r_4=0 in the intersection of the two cones.
    # Even permitting a different fixed clock vector in each coset does not
    # repair this example: the two support types occur in the same coset.
    zp=(2,3,3,2,1)
    zq=(3,2,2,3,3)
    assert mv(A,zp,P)==mv(A,zq,P)==(0,2)
    assert supports(v,zp,P)==sp and supports(v,zq,P)==sq
    return {
        'field':P,'basis':B,'normal_matrix':A,'dimension':3,
        'versatility_sign_classes_checked':32,
        'unit_scale_supports':s0,'unit_balance_separator':dual,
        'first_scale':(2,2,2,2,1),'first_scale_supports':sp,
        'second_scale':(2,2,2,2,2),'second_scale_supports':sq,
        'same_coset_states':[zp,zq],'same_coset_syndrome':(0,2),
        'claims_exactly_checked':[
            'All 32 sign classes activate every coordinate.',
            'The displayed rational separator excludes unit balance.',
            'The two displayed cone identities exclude any common positive clock.',
            'The obstruction persists within a single coset.'
        ]
    }


def discover_certificate(a, x, p, ternary_cache):
    """Search with floating LP; accept only an EXACT nonnegative certificate."""
    import numpy as np
    from scipy.optimize import linprog
    aa=np.asarray(a,dtype=np.int64)
    xx=np.asarray(x,dtype=np.int64)
    n=aa.shape[1]
    if n not in ternary_cache:
        ternary_cache[n]=np.asarray(list(itertools.product((-1,0,1),repeat=n)),dtype=np.int64)
    eps=ternary_cache[n]
    vectors=(eps*xx)%p
    valid=(((vectors@aa.T)%p)==0).all(axis=1)&(eps!=0).any(axis=1)
    witnesses={}
    for w in vectors[valid]:
        s=tuple(int(t!=0) for t in w)
        witnesses.setdefault(s,tuple(int(t) for t in w))
    ss=sorted(witnesses)
    full=tuple([1]*n)
    if full in witnesses:
        active=[(full,Fraction(1))]
    else:
        if not ss:
            return {'status':'no_certificate_found','reason':'no legal directions'}
        sm=np.asarray(ss,dtype=np.int64)
        fit=linprog(np.zeros(len(ss)),A_eq=sm.T,b_eq=np.ones(n),bounds=(0,None),method='highs')
        if not fit.success:
            return {'status':'no_certificate_found','reason':str(fit.message)}
        active=[(s,Fraction(float(t)).limit_denominator(10**6))
                for s,t in zip(ss,fit.x) if t>1e-10]
    sums=[sum(t*s[i] for s,t in active) for i in range(n)]
    if sums != [Fraction(1)]*n or any(t<0 for s,t in active):
        raise ArithmeticError('Floating LP solution failed exact rational reconstruction.')
    entries=[]
    for s,t in active:
        w=witnesses[s]
        assert mv(a,w,p)==tuple([0]*len(a))
        assert all(wi in (0,xi,(-xi)%p) for wi,xi in zip(w,x))
        entries.append({'direction':w,'weight':[t.numerator,t.denominator]})
    return {'status':'exact_certificate','full_support_direction_exists':full in witnesses,
            'directions':entries}


def projective_vectors(p, d):
    return [v for v in itertools.product(range(p),repeat=d)
            if any(v) and next(t for t in v if t)!=0
            and next(t for t in v if t)==1]


def validate_cover(a, offsets, p):
    d=len(a); n=len(a[0]); private=[None]*n
    for u in itertools.product(range(p),repeat=d):
        hits=[i for i in range(n)
              if (sum(a[j][i]*u[j] for j in range(d))+offsets[i])%p==0]
        if not hits:
            raise AssertionError('Family does not cover the finite space.')
        if len(hits)==1:
            private[hits[0]]=u
    if any(u is None for u in private):
        raise AssertionError('Cover is not irredundant.')
    return private


def search_checks(trials, scale_count, seed):
    import numpy as np
    import scipy
    rng=random.Random(seed)
    cache={}
    pencil=((1,1,1,1,1,0),(0,1,2,3,4,1))
    pencil_tests=[]
    for x in itertools.product((1,2),repeat=6):
        cert=discover_certificate(pencil,x,P,cache)
        assert cert['status']=='exact_certificate'
        pencil_tests.append({'scale':x,**cert})
    records=[]
    summaries=[]
    for label,d,affine,max_n in [('affine_F5_squared',2,True,9),
                                  ('central_F5_cubed',3,False,10)]:
        normals=projective_vectors(P,d)
        hyperplanes=[(v,t) for v in normals for t in (range(P) if affine else (0,))]
        points=np.asarray(list(itertools.product(range(P),repeat=d)),dtype=np.int64)
        vv=np.asarray([v for v,t in hyperplanes],dtype=np.int64)
        tt=np.asarray([t for v,t in hyperplanes],dtype=np.int64)
        cover=(points@vv.T+tt)%P==0
        seen=set();sizes=Counter(); skipped=0; checked=0; cert_count=0
        for _ in range(trials):
            chosen=set(range(len(hyperplanes)))
            counts=cover.sum(axis=1)
            order=list(chosen);rng.shuffle(order)
            for i in order:
                if np.all(counts-cover[:,i]>=1):
                    counts-=cover[:,i];chosen.remove(i)
            ids=tuple(sorted(chosen))
            if ids in seen:continue
            seen.add(ids);sizes[len(ids)]+=1
            if len(ids)>max_n:
                skipped+=1;continue
            a=tuple(tuple(int(hyperplanes[i][0][j]) for i in ids) for j in range(d))
            offsets=tuple(int(hyperplanes[i][1]) for i in ids)
            private=validate_cover(a,offsets,P)
            n=len(ids)
            if n<=6:
                scales=list(itertools.product((1,2),repeat=n))
            else:
                scales=sorted(set(tuple(rng.choice((1,2)) for _ in range(n))
                                  for _ in range(scale_count)))
            tests=[]
            for x in scales:
                cert=discover_certificate(a,x,P,cache)
                if cert['status']!='exact_certificate':
                    return {'status':'search_found_unresolved_LP_case',
                            'failure':{'type':label,'A':a,'offsets':offsets,'scale':x,**cert}}
                cert_count+=1;tests.append({'scale':x,**cert})
            checked+=1
            records.append({'type':label,'A':a,'offsets':offsets,
                            'private_witnesses':private,'tests':tests})
        summaries.append({'type':label,'random_greedy_trials':trials,
                          'unique_covers':len(seen),'cover_size_counts':dict(sorted(sizes.items())),
                          'covers_checked':checked,'covers_skipped_by_size_cap':skipped,
                          'scale_certificates_checked':cert_count,'max_N':max_n})
    return {'status':'all_tested_cases_have_exact_certificates',
            'seed':seed,'trials_per_family':trials,'requested_scales_for_large_covers':scale_count,
            'numpy_version':np.__version__,'scipy_version':scipy.__version__,
            'pencil':{'A':pencil,'private_witnesses':validate_cover(pencil,(0,)*6,P),
                      'sign_classes_checked':64,
                      'classes_without_full_support_direction':sum(not t['full_support_direction_exists'] for t in pencil_tests),
                      'tests':pencil_tests},
            'random_cover_summary':summaries,'random_cover_certificates':records,
            'limitation':'Finite, nonexhaustive tests; no universal theorem or priority claim.'}


def replay_certificates(path):
    """Verify saved finite positive certificates with Python integer/Fraction arithmetic."""
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    core_checks()
    search=data.get('search',{})
    families=[]
    if 'pencil' in search:
        pencil=search['pencil']
        families.append({'A':pencil['A'],'offsets':[0]*len(pencil['A'][0]),
                         'tests':pencil['tests']})
    families += search.get('random_cover_certificates',[])
    count=0
    for family in families:
        a=family['A']; n=len(a[0]); d=len(a)
        validate_cover(a,family['offsets'],P)
        for test in family['tests']:
            x=test['scale']
            total=[Fraction(0) for _ in range(n)]
            for entry in test['directions']:
                w=entry['direction']; num,den=entry['weight']
                lam=Fraction(num,den)
                assert lam>=0 and any(w)
                assert mv(a,w,P)==tuple([0]*d)
                assert all(wi in (0,xi,(-xi)%P) for wi,xi in zip(w,x))
                for i,wi in enumerate(w):
                    if wi: total[i]+=lam
            assert total==[Fraction(1)]*n
            count+=1
    return {'core':'passed','positive_certificates_replayed_exactly':count,
            'covers_checked_in_replay':len(families),
            'arithmetic':'Python integers and fractions.Fraction; no numerical LP'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search',action='store_true')
    parser.add_argument('--replay',type=Path,help='Replay a saved JSON certificate file without numpy/scipy')
    parser.add_argument('--trials',type=int,default=40)
    parser.add_argument('--scales',type=int,default=12)
    parser.add_argument('--seed',type=int,default=20261012)
    parser.add_argument('--output',type=Path,default=Path('astra_clock_lift_results.json'))
    args=parser.parse_args()
    if args.replay:
        print(json.dumps(replay_certificates(args.replay),indent=2)); return
    if args.trials<0 or args.scales<1:
        parser.error('trials must be nonnegative and scales must be positive')
    data={'date':'2026-10-12','status':'internal_exact_checks_not_independent_review',
          'core':core_checks()}
    if args.search:data['search']=search_checks(args.trials,args.scales,args.seed)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    report={'core':'passed','output':str(args.output)}
    if args.search:
        report['search_status']=data['search']['status']
        report['pencil_classes']=data['search'].get('pencil',{}).get('sign_classes_checked')
        report['random_cover_summary']=data['search'].get('random_cover_summary')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
