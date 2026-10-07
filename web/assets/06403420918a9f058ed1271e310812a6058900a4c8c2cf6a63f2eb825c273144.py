#!/usr/bin/env python3
"""Capped exact-bit implementation of the audited low-sector approximation.

Origin: random-sign Pfaffian estimator c03_l10 (Luna); coefficient engine,
central-binomial variance bound, and physical-prefix program c03_s02 (Sol).
Input G is a square Gaussian-integer matrix and F=G/common_denominator.
The asymptotic guarantees are in AUDIT_REPORT.txt, not inferred from tests.
"""
import math
import random
from fractions import Fraction

from pfaffian_prefix_checks import prefix_sample


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def ceil_log2_reciprocal(x):
    bits = 0
    while (1 << bits) * x.numerator < x.denominator:
        bits += 1
    return bits


def canonical_configuration(n, k):
    return {"I": list(range(k)), "J": list(range(k, 2 * k))}


def relative_prefix_count(g, k, eta, delta, up=(), down=(), empty=(),
                          common_denominator=1, rng=None, stats=None):
    """Median of capped means; exact zero when the true prefix mass is zero.

    An output of zero on a positive instance has probability at most delta;
    consequently an output zero is not a deterministic zero certificate.
    """
    eta, delta = Fraction(eta), Fraction(delta)
    if not 0 < eta <= Fraction(1, 2) or not 0 < delta < 1:
        raise ValueError("require 0<eta<=1/2 and 0<delta<1")
    n = len(g)
    if any(len(row) != n for row in g) or not 0 <= k <= n // 2:
        raise ValueError("require square matrix and a legal pair sector")
    if not isinstance(common_denominator, int) or common_denominator <= 0:
        raise ValueError("common_denominator must be a positive integer")
    up, down, empty = set(up), set(down), set(empty)
    if up & down or up & empty or down & empty:
        raise ValueError("occupation restrictions must be disjoint")
    if not up | down | empty <= set(range(n)):
        raise ValueError("occupation restrictions contain an invalid index")
    a, b = len(up), len(down)
    if a > k or b > k or 2 * k > n - len(empty):
        return Fraction(0)
    if k == 0:
        return Fraction(1)
    c = math.comb(2 * k - a - b, k - a)
    assert (1 << b) * c <= math.comb(2 * k, k)
    if c == 1:
        # The pointwise Y<=c_prefix and E Y=c_prefix imply Y=c_prefix
        # identically, since the sign space is finite with positive measure.
        signs = [1] * n
        value = prefix_sample(g, k, signs, up, down, empty)
        if stats is not None:
            stats["deterministic_C1_calls"] = stats.get("deterministic_C1_calls", 0) + 1
        return Fraction(value, common_denominator ** (2 * k))
    per_batch = ceil_fraction(4 * c / (eta * eta))
    batches = 16 * ceil_log2_reciprocal(delta) + 1
    rng = random.SystemRandom() if rng is None else rng
    free = sorted(set(range(n)) - up - down - empty)
    means = []
    for _ in range(batches):
        total = 0
        for _ in range(per_batch):
            signs = [0] * n
            for i in free:
                signs[i] = 1 if rng.getrandbits(1) else -1
            total += prefix_sample(g, k, signs, up, down, empty)
        means.append(total)
    means.sort()
    if stats is not None:
        stats["count_calls"] = stats.get("count_calls", 0) + 1
        stats["sign_samples"] = stats.get("sign_samples", 0) + per_batch * batches
        stats["max_sample_denominator_bits"] = max(
            stats.get("max_sample_denominator_bits", 0),
            (common_denominator ** (2 * k)).bit_length())
    return Fraction(means[batches // 2], per_batch * common_denominator ** (2 * k))


def born_sample(g, k, epsilon, rng=None, stats=None):
    """Capped TV-epsilon sampler for the promise c_k(G)>0.

    Normalization cancels a common matrix denominator. On an all-zero estimate
    event, return one fixed legal configuration. The probability of such bad
    estimation events is included in the total-variation proof. Thus a rare
    fallback can have zero target weight; no support guarantee is claimed for
    every execution. A zero-total-norm input has no normalized target law.
    """
    n, epsilon = len(g), Fraction(epsilon)
    if not 0 < epsilon < 1 or not 0 <= k <= n // 2:
        raise ValueError("require 0<epsilon<1 and a legal pair sector")
    if any(len(row) != n for row in g):
        raise ValueError("require a square matrix")
    if k == 0:
        return {"I": [], "J": [], "fallback": False}
    rng = random.SystemRandom() if rng is None else rng
    root_n = math.isqrt(n)
    if root_n * root_n < n:
        root_n += 1
    # c03_s03's Hellinger-chain refinement, independently reconstructed in
    # HELLINGER_SAMPLER_ADDENDUM.txt, saves a factor n in sign evaluations.
    eta, delta = epsilon / (16 * root_n), epsilon / (12 * n)
    bits = 0
    while (1 << bits) * epsilon < 8 * n:
        bits += 1
    denominator = 1 << bits
    up, down, empty = set(), set(), set()
    for i in range(n):
        weights = [relative_prefix_count(g, k, eta, delta, up | {i}, down, empty,
                                         rng=rng, stats=stats),
                   relative_prefix_count(g, k, eta, delta, up, down | {i}, empty,
                                         rng=rng, stats=stats),
                   relative_prefix_count(g, k, eta, delta, up, down, empty | {i},
                                         rng=rng, stats=stats)]
        total = sum(weights)
        if total == 0:
            return {**canonical_configuration(n, k), "fallback": True}
        first = weights[0] * denominator / total
        second = (weights[0] + weights[1]) * denominator / total
        t1, t2 = first.numerator // first.denominator, second.numerator // second.denominator
        word = rng.getrandbits(bits)
        if word < t1:
            up.add(i)
        elif word < t2:
            down.add(i)
        else:
            empty.add(i)
    assert len(up) == len(down) == k and not up & down
    return {"I": sorted(up), "J": sorted(down), "fallback": False}


def smoke_checks():
    """Small count calls and exact-prefix sampler smoke tests, not a benchmark."""
    from pfaffian_prefix_checks import direct_norm, ZERO
    stats, rng, records = {}, random.Random(55102), []
    matrices = [([[(0, 0), (1, 1)], [(2, -1), (0, 0)]], 1, 3),
                ([[(1, 1), (2, -1), (-1, 2)],
                  [(0, 1), (3, 2), (1, -1)],
                  [(2, 0), (-2, 1), (0, 1)]], 1, 6),
                ([[(1, 0) if i != j else ZERO for j in range(4)] for i in range(4)], 2, 1)]
    for g, k, denominator in matrices:
        target = Fraction(direct_norm(g, k), denominator ** (2 * k))
        value = relative_prefix_count(g, k, Fraction(1, 2), Fraction(1, 4),
                                      common_denominator=denominator, rng=rng, stats=stats)
        if target == 0:
            assert value == 0
        else:
            assert abs(value - target) <= target / 2
        records.append({"n": len(g), "k": k, "target": str(target), "estimate": str(value)})
    assert born_sample(matrices[0][0], 0, Fraction(1, 2), rng=rng) == {"I": [], "J": [], "fallback": False}
    support_samples = []
    for _ in range(32):
        sample = born_sample(matrices[0][0], 1, Fraction(1, 4), rng=rng, stats=stats)
        assert not sample["fallback"]
        assert len(sample["I"]) == len(sample["J"]) == 1
        assert sample["I"][0] != sample["J"][0]
        support_samples.append(sample)
    for kwargs in ({"up": (0, 1)}, {"down": (0, 1)}, {"empty": (0,)}):
        assert relative_prefix_count(matrices[0][0], 1, Fraction(1, 2), Fraction(1, 4),
                                     rng=rng, **kwargs) == 0
    return {"status": "PASS", "scope": "3 complete randomized count calls; 32 two-site Born sampler calls using exact C=1 prefixes; no generic nontrivial Born FPRAS benchmark",
            "records": records, "two_site_sample_count": len(support_samples), "telemetry": stats}


if __name__ == "__main__":
    import json
    from pathlib import Path
    result = smoke_checks()
    Path(__file__).with_name("low_sector_smoke_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
