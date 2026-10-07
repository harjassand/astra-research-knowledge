#!/usr/bin/env python3
"""Corrected small check for the m=2, K=3 finite-jet example.

Moments are evaluated exactly as Fractions.  The derivative formula uses
(-1)^k k! tau^(k+2), with no multi-index factorial denominator.
"""

from fractions import Fraction
from itertools import product
from math import factorial, prod, sqrt
import json
from pathlib import Path


M, K = 2, 3
TAU = 1.0 / (4.0 * sqrt(M))


def continuous_1d(power):
    if power % 2:
        return Fraction(0)
    return Fraction(1, power + 1)


def discrete_1d(power):
    if power % 2:
        return Fraction(0)
    if power == 0:
        return Fraction(1)
    # Three-node normalized Gauss-Legendre rule: nodes +/-sqrt(3/5), 0,
    # with normalized weights 5/18, 4/9, 5/18.  The zero node contributes
    # nothing for every positive power.
    return 2 * Fraction(5, 18) * Fraction(3, 5) ** (power // 2)


def moment(alpha, one_d):
    return prod(one_d(power) for power in alpha)


def multiindices(m, max_total):
    return [a for a in product(range(max_total + 1), repeat=m)
            if sum(a) <= max_total]


max_degree = K + 2
moment_count = 0
for alpha in multiindices(M, max_degree):
    assert moment(alpha, continuous_1d) == moment(alpha, discrete_1d)
    moment_count += 1


fisher_count = 0
fisher_max_abs = 0.0
for i in range(M):
    for j in range(M):
        for alpha in multiindices(M, K):
            k = sum(alpha)
            exponents = list(alpha)
            exponents[i] += 1
            exponents[j] += 1
            # Exact moment equality is the equality certificate; this factor
            # is the actual multi-index derivative, not the Taylor coefficient.
            assert moment(exponents, continuous_1d) == moment(exponents, discrete_1d)
            factor = ((-1) ** k) * factorial(k) * TAU ** (k + 2)
            c_value = float(moment(exponents, continuous_1d)) * factor
            d_value = float(moment(exponents, discrete_1d)) * factor
            fisher_max_abs = max(fisher_max_abs, abs(c_value - d_value))
            fisher_count += 1


score_count = 0
for order in range(1, K + 3):
    for indices in product(range(M), repeat=order):
        exponents = tuple(indices.count(i) for i in range(M))
        assert moment(exponents, continuous_1d) == moment(exponents, discrete_1d)
        score_count += 1


result = {
    "m": M,
    "K": K,
    "moment_degree": max_degree,
    "exact_moment_entries_checked": moment_count,
    "actual_fisher_derivative_entries_checked": fisher_count,
    "max_fisher_derivative_residual": fisher_max_abs,
    "score_product_entries_checked_through_order": K + 2,
    "score_product_entries_checked": score_count,
    "derivative_factor": "(-1)^|alpha| |alpha|! tau^(|alpha|+2)",
    "status": "exact rational moment match; floating derivative-factor evaluation is only a display check",
}

out = Path(__file__).with_name("finite_jet_derivative_check.json")
out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
