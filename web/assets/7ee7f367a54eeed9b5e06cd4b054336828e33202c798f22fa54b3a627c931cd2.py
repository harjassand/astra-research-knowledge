"""Executable mandatory-core residual counter, with an explicit admission cap.

All arithmetic is exact. Randomness in diagnostics is seeded; the theorem
assumes independent uniform fair bits. The cap avoids exponential work on an
unadmitted input. Only imports the owned paired_exact module.
"""
from fractions import Fraction as F
from math import ceil, isqrt, comb
from statistics import median

from paired_exact import Q, canonical, estimator_sample, force_project, mandatory_core_pit


def log2_ceil(x):
    assert x >= 1
    if not isinstance(x, F):
        x = F(x)
    exponent = max(0, x.numerator.bit_length()-x.denominator.bit_length())
    while F(1 << exponent) < x:
        exponent += 1
    return exponent


def sqrt_up_to_activity(lam, gamma):
    """Find rational b with lam <= b*b <= (1+gamma)*lam.

    Exact exponent normalization and integer square root; polynomial in binary
    input length and log(1/gamma), including very small/large activities.
    """
    assert lam > 0 and 0 < gamma < 1
    numerator, denominator = lam.numerator, lam.denominator
    e = numerator.bit_length()-denominator.bit_length()
    if F(2)**e > lam:
        e -= 1
    a = e//2
    x = lam/(F(2)**(2*a))
    assert 1 <= x < 4
    p = log2_ceil(F(3)/gamma)
    scaled_numerator = x.numerator << (2*p)
    q = isqrt(scaled_numerator//x.denominator)
    if q*q*x.denominator != scaled_numerator:
        q += 1
    b = F(q, 1 << p)*(F(2)**a)
    assert lam <= b*b <= (1+gamma)*lam
    return b


def paired_fpras(V, k, epsilon, delta, rng, second_moment_bound=None):
    assert 0 < epsilon < 1 and 0 < delta < 1
    if k == 0:
        return {'value': F(1), 'sign_samples': 0, 'batches': 0, 'batch_size': 0}
    # Post-exposure improvement credited to c01_s01, FOUR_PHASE_VARIANCE_PROOF
    # Section 2: tensor monomials have orthogonal exponents 0,1,2, and each
    # collision class has size at most binom(2k,k).
    if second_moment_bound is None:
        second_moment_bound = comb(2*k, k)
    assert second_moment_bound >= 1
    batch = ceil(F(4*second_moment_bound)/(epsilon*epsilon))
    groups = 16*log2_ceil(F(1)/delta)+1
    N = len(V[0])//2
    means = []
    for _ in range(groups):
        total = F(0)
        for _ in range(batch):
            roots = [Q(1),Q(-1),Q(0,1),Q(0,-1)]
            phases = [roots[rng.getrandbits(2)] for _ in range(N)]
            total += estimator_sample(V, k, phases)
        means.append(total/batch)
    return {'value': median(means), 'sign_samples': batch*groups,
            'batches': groups, 'batch_size': batch,
            'relative_second_moment_bound': second_moment_bound,
            'phase_random_bits': 2*N*batch*groups,
            'four_phase_bound_origin': 'c01_s01 phase2 Section 2'}


def mandatory_core_count(Fmat, k, epsilon, delta, residual_cap, rng, activities=None):
    """Count on the acquired subclass; UNKNOWN when residual exceeds cap.

    Count accuracy >=1-delta for inputs whose true mandatory residual is within
    cap. With probability >=1-delta/2, support/core classification is correct
    on every input. False admission is possible only within that PIT budget.
    """
    assert 0 < epsilon < 1 and 0 < delta < 1 and residual_cap >= 0
    V = canonical(Fmat)
    N = len(Fmat)
    if activities is not None:
        assert len(activities) == N and all(lam > 0 for lam in activities)
    acquired = mandatory_core_pit(V, k, delta/2, rng)
    if acquired['status'].startswith('ZERO'):
        return {'status': 'ZERO_WITH_CONFIDENCE', 'value': F(0), 'acquisition': acquired}
    r = acquired['residual']
    if r is None or r > residual_cap:
        return {'status': 'UNKNOWN', 'value': None, 'acquisition': acquired}
    d, W, remaining = force_project(V, acquired['core'])
    eta = epsilon
    if activities is not None:
        for i in acquired['core']:
            d *= activities[i]
        if r:
            eta = epsilon/4
            gamma = epsilon/(8*r)
            for j, label in enumerate(remaining):
                b = sqrt_up_to_activity(activities[label], gamma)
                for row in W:
                    row[2*j+1] = b*row[2*j+1]
    estimate = paired_fpras(W, r, eta, delta/2, rng)
    return {'status': 'APPROXIMATE_WITH_CONFIDENCE', 'value': d*estimate['value'],
            'acquisition': acquired, 'factor': d, 'residual_estimate': estimate,
            'residual_cap': residual_cap,
            'claim': 'relative epsilon, confidence 1-delta on admitted inputs'}
