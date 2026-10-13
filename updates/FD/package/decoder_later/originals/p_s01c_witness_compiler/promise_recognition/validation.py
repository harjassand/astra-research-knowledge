"""Validation ports; no source ranks, coordinates or source degree tests.

Exact chain/block validators recognize equality without degree assumptions.
Random prefix/tail validators require the TRUE degree bound as a supplied
promise. They do not recognize it. All source access is chosen-pair comparison.
"""
from __future__ import annotations
import math
from pathlib import Path
import random
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import witness_compiler as wc
fd,ac=wc.fd,wc.ac


def chain_validate(n,inverse,query):
    """Exact equality with a KNOWN bijective candidate, inverse provided locally."""
    source=ac.Source(query)
    N=1 << n
    previous=inverse(0)
    for rank in range(1,N):
        current=inverse(rank)
        if not source(previous,current):
            return dict(status='REJECT',comparison_calls=source.calls,violated_boundary=rank-1)
        previous=current
    return dict(status='EXACT_MATCH',comparison_calls=source.calls,certificate='all adjacent candidate items ordered')


def sampled_chain_validate(n,inverse,query,beta,rng,perfect_completeness=True):
    """Sharp worst-cap whole-order test; distinguishes equality vs ANY mismatch."""
    if not 0<=beta<.5:
        raise ValueError('beta in [0,1/2)')
    M=(1 << n)-1
    if not perfect_completeness and rng.random()<beta:
        return dict(status='REJECT',comparison_calls=0,branch='blind rejection')
    fraction=1-beta if perfect_completeness else (1-2*beta)/(1-beta)
    T=math.ceil(fraction*M)
    source=ac.Source(query)
    for j in rng.sample(range(M),T):
        if not source(inverse(j),inverse(j+1)):
            return dict(status='REJECT',comparison_calls=source.calls,sample_cap=T)
    return dict(status='ACCEPT',comparison_calls=source.calls,sample_cap=T,
                guarantee='bounded error whole equality; source exact static bijection')


def prepare_prefix(n,d,polynomials,toggles):
    if len(polynomials)!=len(toggles) or len(polynomials)>n:
        raise ValueError('candidate dimensions')
    meter=ac.Meter()
    prefix=fd.Prefix(n,meter)
    for q,v in zip(polynomials,toggles):
        if q.n!=n or any(mask.bit_count()>d for mask in q.terms):
            raise ValueError('candidate degree/body mismatch')
        prefix.add(q,v)
    return prefix,prefix.sampler(),meter


def exact_prefix_validate(n,d,polynomials,toggles,query):
    """Exact prefix equality via actual source minima/maxima in model blocks."""
    prefix,sampler,meter=prepare_prefix(n,d,polynomials,toggles)
    h=len(polynomials)
    if h==0:
        return dict(status='EXACT_PREFIX_MATCH',comparison_calls=0,local_operations=dict(meter.ops))
    source=ac.Source(query)
    previous_max=None
    for target in range(1 << h):
        points=iter(sampler.fiber(target))
        minimum=maximum=next(points)
        for x in points:
            if source(x,minimum):minimum=x
            if source(maximum,x):maximum=x
        if previous_max is not None and not source(previous_max,minimum):
            return dict(status='REJECT',comparison_calls=source.calls,violated_model_block=target)
        previous_max=maximum
    B=1 << h
    cap=2*(1 << n)-B-1
    assert source.calls<=cap
    return dict(status='EXACT_PREFIX_MATCH',comparison_calls=source.calls,comparison_cap=cap,
                local_operations=dict(meter.ops),certificate='actual extrema order all balanced model blocks')


def _prefix_test(n,d,prefix,sampler,source,rng,eta,meter):
    h=len(prefix.q)
    if h==0:return dict(status='ACCEPT',tests=0,test_cap=0)
    rejection=2.0**(-2*d)/h
    cap=math.ceil(math.log(1/eta)/-math.log1p(-rejection))
    for count in range(1,cap+1):
        stage=rng.randrange(h)
        earlier=rng.getrandbits(stage)
        remaining=h-stage-1
        left_target=(earlier << (remaining+1))|rng.getrandbits(remaining)
        right_target=(earlier << (remaining+1))|(1 << remaining)|rng.getrandbits(remaining)
        meter.add('validation_stage_draws')
        meter.add('validation_prefix_random_bits',stage+2*remaining)
        left=sampler.sample(left_target,rng,meter)
        right=sampler.sample(right_target,rng,meter)
        if not source(left,right):
            return dict(status='REJECT',tests=count,test_cap=cap,rejection_lower_bound=rejection,
                        witness=dict(stage=stage,left=left,right=right,earlier_prefix=earlier))
    return dict(status='ACCEPT',tests=cap,test_cap=cap,rejection_lower_bound=rejection)


def degree_promised_validate(n,d,polynomials,toggles,query,seed,eta=.01,prefix_only=False):
    """Sound exact-model validation UNDER the true coordinate-degree promise.

Prefix: true first h bits degree<=d; arbitrary suffix allowed.
Full: ALL true bits degree<=d. Candidate need not be globally bijective.
Candidate prefix identities are checked exactly locally. Every accepted
wrong candidate has probability <=eta conditional on any prior transcript
when this validation uses fresh independent randomness and the true promise.
"""
    started=time.perf_counter()
    h=len(toggles)
    if (prefix_only and len(polynomials)!=h) or (not prefix_only and len(polynomials)!=n):
        raise ValueError('model scope')
    if not 0<eta<1:
        raise ValueError('eta in (0,1)')
    if any(q.n!=n or any(mask.bit_count()>d for mask in q.terms) for q in polynomials):
        raise ValueError('candidate degree')
    prefix,sampler,meter=prepare_prefix(n,d,polynomials[:h],toggles)
    source=ac.Source(query)
    rng=random.Random(seed)
    prefix_eta=eta if prefix_only else eta/2
    first=_prefix_test(n,d,prefix,sampler,source,rng,prefix_eta,meter)
    if first['status']=='REJECT':
        return dict(status='REJECT',comparison_calls=source.calls,prefix_test=first,
                    tail_tests=0,local_operations=dict(meter.ops),seconds=time.perf_counter()-started)
    if prefix_only:
        return dict(status='ACCEPT_UNDER_TRUE_DEGREE_PROMISE',comparison_calls=source.calls,
                    prefix_test=first,tail_tests=0,error_budget=eta,
                    local_operations=dict(meter.ops),seconds=time.perf_counter()-started)
    r=n-h
    cap=math.ceil(math.log(2/eta)/-math.log1p(-2.0**(-d))) if r else 0
    for count in range(1,cap+1):
        x=rng.getrandbits(n)
        meter.add('tail_validation_raw_random_bits',n)
        source_rank=sum(source(y,x) for y in sampler.fiber(prefix.prefix(x)) if y!=x)
        candidate_rank=0
        for q in polynomials[h:]:candidate_rank=(candidate_rank << 1)|q(x,meter)
        if source_rank!=candidate_rank:
            return dict(status='REJECT',comparison_calls=source.calls,prefix_test=first,
                tail_tests=count,tail_test_cap=cap,
                tail_witness=dict(raw=x,source_fiber_rank=source_rank,candidate_tail=candidate_rank),
                local_operations=dict(meter.ops),seconds=time.perf_counter()-started)
    return dict(status='ACCEPT_UNDER_TRUE_DEGREE_PROMISE',comparison_calls=source.calls,
        prefix_test=first,tail_tests=cap,tail_test_cap=cap,
        comparison_cap=first['test_cap']+((1 << r)-1)*cap,error_budget=eta,
        candidate_bijectivity_supplied_or_globally_checked=False,
        local_operations=dict(meter.ops),seconds=time.perf_counter()-started)


def ancestor_validate(n,inverse,query,epsilon,beta,seed):
    """Established sortedness test: exact match vs deletion-distance>=epsilon.

inverse must enumerate a KNOWN candidate total order; its acquisition/lifting
cost is external and must be charged. PASS is an approximate validation only.
"""
    if not 0<epsilon<1 or not 0<beta<1:
        raise ValueError('epsilon,beta in (0,1)')
    rng=random.Random(seed)
    source=ac.Source(query)
    N=1 << n
    trials=math.ceil(math.log(1/beta)/-math.log1p(-epsilon))
    for count in range(1,trials+1):
        i=rng.randrange(N)
        item=inverse(i)
        low,high=0,N
        while True:
            middle=(low+high)//2
            if middle==i:break
            other=inverse(middle)
            if bool(source(item,other))!=(i<middle):
                return dict(status='REJECT',comparison_calls=source.calls,trials=count,
                            witness=[i,middle])
            if i<middle:high=middle
            else:low=middle+1
    return dict(status='APPROXIMATE_PASS',comparison_calls=source.calls,trials=trials,
                comparison_cap=n*trials,distance='(N-LIS)/N in candidate order',beta=beta)
