"""Acquire a supported k-pair set and its maximum support Johnson radius.

N+1 projected support PIT queries plus 2k+1 exact univariate evaluations.
No optimization, partition, conditional-sampling or support-diameter oracle.
The one-sided finite-field-free PIT confidence is proved in the report.
"""
from fractions import Fraction as F
from math import comb, ceil

from paired_exact import estimator_sample, force_project, gram_weight
from residual_counter import paired_fpras


def acquire_support_radius(V, k, delta, rng):
    m, N = len(V), len(V[0])//2
    assert 0 < delta < 1
    if k == 0:
        return {'status':'POSITIVE','witness':[],'radius':0,'diameter_bound':0,
                'moment_bound':1,'grid':1,'support_calls':0}
    if 2*k > m or k > N:
        return {'status':'ZERO','witness':None,'radius':None}
    bits = (ceil(F(k*(N+2))/delta)-1).bit_length()
    grid = 1 << bits
    calls = 0
    query_random_bits = 0

    def supported(forced, excluded):
        nonlocal calls, query_random_bits
        calls += 1
        if len(forced) > k:
            return False
        d, W, labels = force_project(V,forced,excluded)
        if not d:
            return False
        r = k-len(forced)
        if len(labels) < r:
            return False
        if r == 0:
            return True
        xs = [rng.getrandbits(bits)+1 for _ in labels]
        query_random_bits += bits*len(labels)
        return estimator_sample(W,r,xs) != 0

    if not supported([],[]):
        return {'status':'ZERO_WITH_CONFIDENCE','witness':None,'radius':None,
                'grid':grid,'support_calls':calls,'random_bits':query_random_bits}
    forced, excluded = [],[]
    for i in range(N):
        if len(forced) == k:
            excluded.append(i)
        elif supported(forced+[i],excluded):
            forced.append(i)
        else:
            excluded.append(i)
    if len(forced) != k or not gram_weight(V,forced):
        return {'status':'UNKNOWN','witness':forced,'radius':None,
                'grid':grid,'support_calls':calls,'random_bits':query_random_bits}
    # Conditional on the previous history, this is fresh independent integer
    # randomness. A top-degree coefficient vanishes with probability <=k/grid.
    xs = [rng.getrandbits(bits)+1 for _ in range(N)]
    query_random_bits += bits*N
    inside = set(forced)
    values = [estimator_sample(V,k,[x if i in inside else z*x
                         for i,x in enumerate(xs)]) for z in range(2*k+1)]
    diffs = values[:]
    degree = 0
    first_differences = []
    for order in range(2*k+1):
        first_differences.append(diffs[0])
        if diffs[0]:
            degree = order
        diffs = [b-a for a,b in zip(diffs,diffs[1:])]
    assert degree % 2 == 0
    radius = degree//2
    diameter = min(k,2*radius)
    return {'status':'POSITIVE','witness':forced,'radius':radius,
            'diameter_bound':diameter,'moment_bound':comb(2*diameter,diameter),
            'grid':grid,'support_calls':calls,'radius_evaluations':2*k+1,
            'random_bits':query_random_bits,'finite_difference_degree':degree,
            'first_differences':first_differences,
            'confidence_contract':'support and radius correct together with probability >=1-delta'}


def acquired_radius_count(V,k,epsilon,delta,radius_cap,rng):
    assert radius_cap >= 0
    acquisition = acquire_support_radius(V,k,delta/2,rng)
    if acquisition['status'].startswith('ZERO'):
        return {'status':'ZERO_WITH_CONFIDENCE','value':F(0),'acquisition':acquisition}
    if acquisition['status'] != 'POSITIVE' or acquisition['radius'] > radius_cap:
        return {'status':'UNKNOWN','value':None,'acquisition':acquisition}
    if acquisition['radius'] == 0:
        return {'status':'EXACT_CONDITIONAL_ON_ACQUISITION',
                'value':gram_weight(V,acquisition['witness']),
                'acquisition':acquisition,'samples':0}
    estimate = paired_fpras(V,k,epsilon,delta/2,rng,
                           second_moment_bound=acquisition['moment_bound'])
    return {'status':'APPROXIMATE_WITH_CONFIDENCE','value':estimate['value'],
            'acquisition':acquisition,'estimate':estimate,
            'contract':'relative epsilon and confidence 1-delta on admitted inputs'}
