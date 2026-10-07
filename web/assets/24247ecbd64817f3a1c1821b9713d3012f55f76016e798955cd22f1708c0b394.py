"""Exact conditional sampler for a canonical functional-digraph BCS sector.

The arithmetic oracle is functional_digraph_dp.count_poly. Each branch uses
an exact rational conditional probability; uniform integers are obtained from
unbiased bits with a polynomially capped rejection loop.
"""
from fractions import Fraction as Q
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from functional_digraph_dp import count_poly


class SamplingAbort(RuntimeError):
    pass


def bernoulli_rational(p, rng, max_rejections):
    p = Q(p)
    if p <= 0:
        return 0
    if p >= 1:
        return 1
    a, d = p.numerator, p.denominator
    bits = (d - 1).bit_length()
    for _ in range(max_rejections):
        value = rng.getrandbits(bits)
        if value < d:
            return int(value < a)
    raise SamplingAbort("capped exact-uniform-integer rejection loop")


def sample_canonical_rows(p, w, t, k, *, rng=None, failure_budget=Q(1, 1000000)):
    """Sample I with probability proportional to its exact BCS norm weight.

    Returns (selected_rows, corresponding_columns, abort_probability_bound).
    For the supplied failure_budget, the total probability of a capped random-
    bit abort over at most n conditional choices is at most that budget.
    """
    n = len(p)
    if not 0 <= k <= n:
        raise ValueError("k must be in [0,n]")
    rng = random.SystemRandom() if rng is None else rng
    failure_budget = Q(failure_budget)
    if not 0 < failure_budget < 1:
        raise ValueError("failure_budget must be strictly between 0 and 1")
    norm = count_poly(p, w, t)[k]
    if not norm:
        raise ValueError("requested sector has zero norm")
    # Per-choice rejection failure <=2^-R; union bound over n choices.
    max_rejections = 1
    while Q(n, 2 ** max_rejections) > failure_budget:
        max_rejections += 1

    fixed = {}
    for i in range(n):
        z0 = count_poly(p, w, t, {**fixed, i: 0})[k]
        z1 = count_poly(p, w, t, {**fixed, i: 1})[k]
        total = z0 + z1
        if not total:
            raise AssertionError("positive prefix lost all mass")
        fixed[i] = bernoulli_rational(z1 / total, rng, max_rejections)
    rows = tuple(i for i, bit in fixed.items() if bit)
    columns = tuple(sorted(p[i] for i in rows if p[i] is not None))
    if len(columns) != len(rows):
        raise AssertionError("positive sample violated injectivity")
    if len(rows) != k:
        raise AssertionError("canonical sampler returned the wrong pair number")
    return rows, columns, Q(n, 2 ** max_rejections)
