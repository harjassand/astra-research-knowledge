"""Exact rational diagnostics for the tensorized relative-second-moment bound.

These are finite diagnostic checks, not a substitute for PROOF.md.
Run: python check_tensorization.py
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import time


def k_of_ratio(r):
    return (r + 1) ** 2 / (4 * r)


def independent_moments(values, probs):
    n = len(probs)
    first = F(0)
    second = F(0)
    for bits in product((0, 1), repeat=n):
        mass = F(1)
        for b, p in zip(bits, probs):
            mass *= p if b else 1 - p
        w = values[bits]
        first += mass * w
        second += mass * w * w
    return first, second


def coordinate_ratios(values, n):
    ratios = [F(1) for _ in range(n)]
    for bits, v in values.items():
        for i in range(n):
            other = list(bits)
            other[i] = 1 - other[i]
            ratio = v / values[tuple(other)]
            ratios[i] = max(ratios[i], ratio)
    return ratios


def main():
    start = time.perf_counter()
    rng = random.Random(20261023)
    cases = 0
    worst_fraction_of_bound = F(0)
    for n in range(1, 9):
        for rep in range(20):
            values = {bits: F(rng.randrange(1, 80), rng.randrange(1, 20))
                      for bits in product((0, 1), repeat=n)}
            probs = [F(rng.randrange(1, 20), 20) for _ in range(n)]
            m1, m2 = independent_moments(values, probs)
            actual = m2 / (m1 * m1)
            bound = F(1)
            for ratio in coordinate_ratios(values, n):
                bound *= k_of_ratio(ratio)
            assert actual <= bound, (n, rep, actual, bound)
            worst_fraction_of_bound = max(worst_fraction_of_bound, actual / bound)
            cases += 1

    rs = [F(2), F(3), F(5), F(7), F(11)]
    values = {}
    for bits in product((0, 1), repeat=len(rs)):
        val = F(1)
        for b, r in zip(bits, rs):
            if b:
                val *= r
        values[bits] = val
    m1, m2 = independent_moments(values, [1 / (1 + r) for r in rs])
    actual_sharp = m2 / (m1 * m1)
    bound_sharp = F(1)
    for r in rs:
        bound_sharp *= k_of_ratio(r)
    assert actual_sharp == bound_sharp

    n = 8
    r = F(2)
    correlated_actual = k_of_ratio(r ** n)
    falsely_independent_bound = k_of_ratio(r) ** n
    assert correlated_actual > falsely_independent_bound

    result = {
        "seed": 20261023,
        "exact_random_tensorization_cases": cases,
        "all_passed": True,
        "maximum_actual_over_bound_in_random_cases": str(worst_fraction_of_bound),
        "sharp_product_relative_second_moment": str(actual_sharp),
        "sharp_product_equality": True,
        "dependence_counterexample": {
            "n": n,
            "r": str(r),
            "actual_relative_second_moment": str(correlated_actual),
            "incorrect_independence_bound": str(falsely_independent_bound),
            "actual_over_false_bound": float(correlated_actual / falsely_independent_bound)
        },
        "seconds": time.perf_counter() - start,
        "arithmetic": "Python Fraction exact rational",
        "interpretation": "finite diagnostics only; no stochastic performance or novelty certification"
    }
    Path(__file__).with_name("tensorization_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
