"""Executable conditional-sampling reduction, with every oracle explicit.

This file does not implement the missing efficient conditional Gaussian sampler.
sample_batch(B, eta, count) must perform count fresh independent executions of a
sampler whose output law is eta-TV-close to the two-leaf conditional photon law;
it returns the number of outcomes (1,1). Outputs outside {(0,0),(1,1)} count as 0.
has_pm(A) is an ordinary deterministic polynomial-time blossom/existence routine.
No exact-count oracle is used by the reduction itself.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import ceil
from verify_reduction import kernel, remove_pair


class BudgetExceeded(RuntimeError):
    pass


def count_via_conditional_sampler(A, sample_batch, has_pm, epsilon, delta,
                                  max_samples=None):
    epsilon, delta = F(str(epsilon)), F(str(delta))
    if not (0 < epsilon <= 1 and 0 < delta < 1):
        raise ValueError('Need 0 < epsilon <= 1 and 0 < delta < 1')
    n = len(A)
    if n == 0:
        return Decimal(1), {'sample_calls':0,'batches':0}
    if n % 2 or not has_pm(A):
        return Decimal(0), {'sample_calls':0,'batches':0}
    J = n.bit_length()+2
    # Upper bound all selection/calibration batches and refinement batches.
    K = 2*n*n*(J+1)
    # Integer upper bound on ln(4K/delta), avoiding a floating-log schedule.
    L = ceil(4*K/delta).bit_length()
    M0 = 32768*L
    M1 = ceil(131072*n*n/epsilon**2*L)
    eta0 = F(1,256)
    eta1 = epsilon/(512*n)
    used = batches = 0

    def estimate(current, v, shift, eta, size):
        nonlocal used, batches
        if max_samples is not None and used+size > max_samples:
            raise BudgetExceeded(f'Requires {used+size} conditional samples; '
                                 f'budget is {max_samples}. No estimate returned.')
        B, _, _ = kernel(current,0,v,shift)
        hits = sample_batch(B,eta,size)
        if not isinstance(hits,int) or not 0 <= hits <= size:
            raise ValueError('sample_batch must return integer hits in [0,size]')
        used += size
        batches += 1
        return F(hits,size)

    product = F(1)
    current = A
    while current:
        # Bad sampling runs must not query an undefined zero-probability herald.
        if not has_pm(current):
            return Decimal(0), {'sample_calls':used,'batches':batches,
                                'failed':True,'reason':'zero residual'}
        N = len(current)
        candidates = [(estimate(current,v,0,eta0,M0),v)
                      for v in range(1,N) if current[0][v]]
        _, v = max(candidates)
        shift = 0
        q = estimate(current,v,shift,eta0,M0)
        while q > F(1,2) and shift < J:
            shift += 1
            q = estimate(current,v,shift,eta0,M0)
        if shift == J and q > F(1,2):
            return Decimal(0), {'sample_calls':used,'batches':batches,
                                'failed':True,'reason':'calibration'}
        q = estimate(current,v,shift,eta1,M1)
        if not 0 < q < 1:
            return Decimal(0), {'sample_calls':used,'batches':batches,
                                'failed':True,'reason':'refinement'}
        R = F(N,4*4**shift)
        product *= R*R*(1-q)/q
        current = remove_pair(current,0,v)
    # Relative decimal rounding is much below epsilon/8, including large Z.
    digits = max(40,epsilon.denominator.bit_length()-epsilon.numerator.bit_length()+20)
    with localcontext() as ctx:
        ctx.prec = digits
        estimate = (Decimal(product.numerator)/Decimal(product.denominator)).sqrt()
    return estimate, {'sample_calls':used,'batches':batches,
                      'eta_min':str(eta1),'precision_digits':digits}
