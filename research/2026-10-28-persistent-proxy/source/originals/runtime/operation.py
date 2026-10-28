"""Exact classical proxy operations. No physical service is acquired here.

All matrix columns are input distributions. Runtime proxy callbacks must return
fresh iid records conditional on one already-classical persistent input X.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import factorial, lcm
import random


def matrix(values):
    return [[F(value) for value in row] for row in values]


def product(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def inverse(a):
    n = len(a)
    t = [list(row) + [F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if t[i][j]), None)
        if pivot is None:
            raise ValueError("singular confusion matrix")
        t[j], t[pivot] = t[pivot], t[j]
        scale = t[j][j]
        t[j] = [v / scale for v in t[j]]
        for i in range(n):
            if i != j:
                scale = t[i][j]
                t[i] = [v - scale * w for v, w in zip(t[i], t[j])]
    return [row[n:] for row in t]


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, parts - 1):
                yield (first,) + rest


def type_probability(counts, column):
    numerator = factorial(sum(counts))
    denominator = 1
    probability = F(1)
    for count, p in zip(counts, column):
        denominator *= factorial(count)
        probability *= p ** count
    return (numerator // denominator) * probability


def compile_by_classifier(k, ell, repeats):
    """Ordinary exact confusion-matrix inversion, with explicit type enumeration.

    Returns a certificate, even if its candidate postprocessor has negatives.
    There are binomial(repeats + k_proxy - 1, k_proxy - 1) enumerated types.
    This is not a polynomial-in-input-bit-length performance claim.
    """
    k, ell = matrix(k), matrix(ell)
    proxy_alphabet, inputs = len(ell), len(ell[0])
    confusion = [[F(0) for _ in range(inputs)] for _ in range(inputs)]
    rules = {}
    for counts in compositions(repeats, proxy_alphabet):
        empirical = [F(c, repeats) for c in counts]
        distances = [max(abs(empirical[z] - ell[z][x])
                         for z in range(proxy_alphabet)) for x in range(inputs)]
        predicted = min(range(inputs), key=lambda x: (distances[x], x))
        rules[counts] = predicted
        for x in range(inputs):
            confusion[predicted][x] += type_probability(
                counts, [ell[z][x] for z in range(proxy_alphabet)])
    post = product(k, inverse(confusion))
    stochastic = (all(v >= 0 for row in post for v in row)
                  and all(sum(row[x] for row in post) == 1 for x in range(inputs)))
    return {"repeats": repeats, "confusion": confusion, "post": post,
            "rules": rules, "stochastic": stochastic,
            "identity_checked": product(post, confusion) == k}


def exact_choice(weights, rng=None):
    """Sample a rational table from unbiased getrandbits, using rejection."""
    rng = rng or random.SystemRandom()
    weights = [F(w) for w in weights]
    if any(w < 0 for w in weights) or sum(weights) != 1:
        raise ValueError("weights must be a probability vector")
    denominator = lcm(*(w.denominator for w in weights))
    if denominator == 1:
        return next(i for i, w in enumerate(weights) if w)
    while True:
        draw = rng.getrandbits((denominator - 1).bit_length())
        if draw < denominator:
            break
    for i, weight in enumerate(weights):
        mass = weight.numerator * (denominator // weight.denominator)
        if draw < mass:
            return i
        draw -= mass
    raise AssertionError("unreachable probability-table tail")


def source_two_proxy_output(proxy_callback, rng=None):
    """One exact K output for N1073's stored pair; exactly two L calls, no raw.

    Private records are discarded. Both calls must see the SAME classical X.
    Runtime is exact given unbiased random bits, with finite expected bit cost.
    """
    z1, z2 = proxy_callback(), proxy_callback()
    if z1 not in (0, 1, 2) or z2 not in (0, 1, 2):
        raise ValueError("proxy record outside source alphabet")
    count = int(z1 == 0) + int(z2 == 0)
    probability_zero = (F(13, 25), F(17, 100), F(0))[count]
    return exact_choice([probability_zero, (1 - probability_zero) / 2,
                         (1 - probability_zero) / 2], rng)


def classifier_output(compiled, proxy_callback, rng=None):
    if not compiled["stochastic"]:
        raise ValueError("candidate postprocessor contains a negative entry")
    proxy_alphabet = len(next(iter(compiled["rules"])))
    counts = [0] * proxy_alphabet
    for _ in range(compiled["repeats"]):
        z = proxy_callback()
        if not 0 <= z < proxy_alphabet:
            raise ValueError("proxy record outside compiled alphabet")
        counts[z] += 1
    prediction = compiled["rules"][tuple(counts)]
    return exact_choice([row[prediction] for row in compiled["post"]], rng)


def common_part_output(k, raw_callback, rng=None):
    """Exact distribution-free baseline: no proxy calls; at most one raw call."""
    k = matrix(k)
    common = [min(row) for row in k]
    q = 1 - sum(common)
    branch = exact_choice(common + [q], rng)
    if branch < len(k):
        return branch
    x = raw_callback()
    return exact_choice([(row[x] - baseline) / q
                         for row, baseline in zip(k, common)], rng)


def source_approximate_output(proxy_callback, rng=None, cheap_calls=102):
    """Ordinary threshold inference + exact randomization; approximate K only.

    At TV radius1/600, 102 calls certify output TV<=1e-6, even for predictable
    per-draw biases in the separated intervals. No stationary factory required.
    """
    count = 0
    for _ in range(cheap_calls):
        z = proxy_callback()
        if z not in (0, 1, 2):
            raise ValueError("proxy record outside source alphabet")
        count += z == 0
    high = 12 * count > 5 * cheap_calls
    probability_zero = F(2, 15) if high else F(49, 120)
    return exact_choice([probability_zero, (1-probability_zero)/2,
                         (1-probability_zero)/2], rng)
