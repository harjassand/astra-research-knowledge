#!/usr/bin/env python3
"""Finite-bit response acquisition on a synthetic implicit 256 x 256 grid.

All certificate arithmetic (including log and square-root upper bounds) is
rational/integer. Target axial ratios are acquired lazily and cached. No target
transverse coefficients are queried: the enclosure is valid for ANY positive
values of those coefficients. The reference field is known analytically.

The confidence theorem assumes independent uniform random bits, as usual for
randomised algorithms. The default seeded PRNG is a reproducibility diagnostic,
not a verification of a random-number generator. Use --system-random for an
OS-backed bit source. The full sampled edge-index stream is recorded.
"""
from __future__ import annotations
import argparse
from bisect import bisect_right
from fractions import Fraction as F
import json
import math
from pathlib import Path
import random
import time

SCALE = 1 << 48


def ceil_div(num: int, den: int) -> int:
    return -(-num // den)


def log_upper(q: int, terms: int = 16) -> F:
    """Rational upper bound on log(q), q positive integer.

    log(z) = 2 sum_{j>=0} t^(2j+1)/(2j+1), t=(z-1)/(z+1).
    Scaling z into [1,2] bounds t by 1/3. A geometric tail majorant
    supplies a rigorous outward error bound without floating-point logs.
    """
    if q < 1:
        raise ValueError('q must be at least one')
    def unit_log(z: F) -> F:
        t = (z-1)/(z+1)
        total = sum((2*t**(2*j+1)/F(2*j+1) for j in range(terms)), F(0))
        return total + 2*t**(2*terms+1)/(F(2*terms+1)*(1-t*t))
    k = q.bit_length()-1
    return k * unit_log(F(2)) + unit_log(F(q, 1 << k))


def sqrt_upper(value: F) -> F:
    """Ceil(sqrt(value) * 2^48) / 2^48, computed by integer arithmetic."""
    if value < 0:
        raise ValueError('square-root input must be nonnegative')
    num, den = value.numerator * SCALE*SCALE, value.denominator
    root = math.isqrt(num//den)
    if root*root*den < num:
        root += 1
    return F(root, SCALE)


class Moments:
    def __init__(self) -> None:
        self.n = self.lo_sum = self.hi_sum = self.square_hi_sum = 0

    def add(self, value: F) -> None:
        if value <= 0:
            raise ValueError('positive values required')
        p, q = value.numerator*SCALE, value.denominator
        lo, hi = p//q, ceil_div(p, q)
        self.n += 1
        self.lo_sum += lo
        self.hi_sum += hi
        self.square_hi_sum += ceil_div(hi*hi, SCALE)

    def mean_upper(self, log_two_over_delta: F) -> F:
        n = self.n
        if n < 2:
            return F(2)
        sample_mean_upper = F(self.hi_sum, n*SCALE)
        # An upper enclosure of the unbiased sample variance.
        var_upper = F(n*SCALE*self.square_hi_sum-self.lo_sum**2,
                      n*(n-1)*SCALE*SCALE)
        radius = sqrt_upper(2*var_upper*log_two_over_delta/n)
        radius += 7*F(3,2)*log_two_over_delta/(3*(n-1))
        return min(F(2), sample_mean_upper + radius)


class LazyOracle:
    def __init__(self, ny: int) -> None:
        self.ny, self.cache = ny, {}

    def ratio(self, edge: int) -> F:
        if edge not in self.cache:
            x, y = divmod(edge, self.ny)
            # Exact synthetic target ratio in [0.95,1.05]. This arithmetic
            # stands in for an expensive microscopic calculation, not a
            # physical validation of a real transition rate.
            self.cache[edge] = F(1000 + ((17*x+13*y) % 101)-50, 1000)
        return self.cache[edge]


def run(seed: int | None = 19031) -> dict:
    started = time.perf_counter()
    nx = ny = 256
    # An exact integer-weight reference with heterogeneous channels.
    channel_weights = [256 + ((983*y+137*y*y) % 3841) for y in range(ny)]
    cumulative, acc = [], 0
    for w in channel_weights:
        acc += w
        cumulative.append(acc)
    C0 = F(acc, 1024*(nx-1))
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    oracle = LazyOracle(ny)
    forward, inverse = Moments(), Moments()
    lo, hi = C0/2, 2*C0
    stream, stages = [], []
    k, target_n = 0, 128
    while target_n <= 131072:
        k += 1
        while len(stream) < target_n:
            y = bisect_right(cumulative, rng.randrange(acc))
            x = rng.randrange(nx-1)
            edge = x*ny + y
            stream.append(edge)
            r = oracle.ratio(edge)
            assert F(1,2) <= r <= 2
            forward.add(r)
            inverse.add(1/r)
        # delta_k=alpha/[2 k(k+1)], alpha=1/100, for each of two moments.
        # Hence 2/delta_k = 400 k(k+1).
        logU = log_upper(400*k*(k+1))
        aU, bU = forward.mean_upper(logU), inverse.mean_upper(logU)
        lo, hi = max(lo, C0/bU), min(hi, C0*aU)
        if lo > hi:
            raise RuntimeError('confidence intersection is empty')
        stages.append({'stage':k, 'samples':len(stream), 'distinct_queries':len(oracle.cache),
                       'lower_exact':str(lo), 'upper_exact':str(hi),
                       'relative_width_display':float(hi/lo-1)})
        if hi/lo <= F(21,20):
            break
        target_n *= 2
    return {'status':'synthetic finite-bit confidence procedure; no physical validation',
            'randomness_model':'i.i.d. uniform bits required by theorem; PRNG not certified',
            'seed':seed, 'grid':[nx,ny], 'vertices':nx*ny,
            'edges':(nx-1)*ny+nx*(ny-1), 'axial_support':(nx-1)*ny,
            'C0_exact':str(C0), 'epsilon_exact':'1/20', 'alpha_exact':'1/100',
            'passed':hi/lo <= F(21,20), 'samples':len(stream),
            'distinct_target_coefficients_acquired':len(oracle.cache),
            'transverse_coefficients_acquired':0, 'lower_exact':str(lo), 'upper_exact':str(hi),
            'lower_display':float(lo), 'upper_display':float(hi),
            'relative_width_display':float(hi/lo-1), 'compute_seconds':time.perf_counter()-started,
            'stages':stages, 'sampled_edge_stream':stream,
            'distinct_oracle_records':{str(e):str(r) for e,r in sorted(oracle.cache.items())}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--system-random', action='store_true')
    args = parser.parse_args()
    result = run(None if args.system_random else 19031)
    Path(__file__).with_name('finite_bit_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in
                     ('stages','sampled_edge_stream','distinct_oracle_records')},indent=2))
