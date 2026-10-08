#!/usr/bin/env python3
"""Finite recurrence check of the proposed first-differing-cumulant law.

This independent k=3 pair is formed from the fourth finite-difference
contrast (1,-4,6,-4,1) on marks 1,...,5, split into positive and negative
parts and with a common mark-1 baseline added to make both supports span one.
All reported probabilities are floating-point Panjer-recursion values; this
is a falsification diagnostic, not interval-certified evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# Scale the positive/negative parts by 2/3 so the total rate is 6, matching
# the original pair's event scale and keeping this finite audit well-scaled.
RATES = (
    (4 / 3, 0, 4, 0, 2 / 3),
    (2 / 3, 8 / 3, 0, 8 / 3, 0),
)
MU_VALUES = (10, 20, 30)
K = 3


def cumulants(rates: tuple[float, ...], order: int) -> list[float]:
    return [math.fsum(rate * mark**r for mark, rate in enumerate(rates, 1))
            for r in range(1, order + 1)]


def pmf(mu: float, rates: tuple[float, ...], cutoff: int) -> list[float]:
    q = [0.0] * (cutoff + 1)
    q[0] = 1.0
    for m in range(1, cutoff + 1):
        q[m] = (mu / m) * math.fsum(
            mark * rates[mark - 1] * q[m - mark]
            for mark in range(1, min(len(rates), m) + 1)
            if rates[mark - 1]
        )
    return [math.exp(-mu * math.fsum(rates)) * value for value in q]


def main() -> None:
    moms = [cumulants(rates, K + 1) for rates in RATES]
    m2 = moms[0][1]
    delta = moms[1][K] - moms[0][K]
    # For first differing cumulant k+1, H^2 ~ C_H / mu^(k-1).
    c_h = delta**2 / (4 * math.factorial(K + 1) * m2 ** (K + 1))
    rows = []
    for mu in MU_VALUES:
        mean = mu * moms[0][0]
        cutoff = math.ceil(mean + 20 * math.sqrt(mu * m2) + 200)
        p0, p1 = (pmf(mu, rates, cutoff) for rates in RATES)
        h2 = math.fsum((math.sqrt(a) - math.sqrt(b)) ** 2
                       for a, b in zip(p0, p1))
        rows.append({
            "mu": mu,
            "cutoff": cutoff,
            "mass0": math.fsum(p0),
            "mass1": math.fsum(p1),
            "H2_truncated": h2,
            "mu_power_k_minus_1_times_H2": mu ** (K - 1) * h2,
            "predicted_constant": c_h,
            "ratio_to_predicted": mu ** (K - 1) * h2 / c_h,
        })
    result = {
        "k": K,
        "rates": {"model0": RATES[0], "model1": RATES[1]},
        "cumulant_sums": {"model0": moms[0], "model1": moms[1]},
        "common_second_cumulant": m2,
        "first_difference_delta": delta,
        "predicted_H2_constant": c_h,
        "rows": rows,
        "scope": "finite floating-point Panjer recurrence with truncation; a k=3 falsifier diagnostic, not a proof or interval certificate",
    }
    out = Path(__file__).with_name("generic_k_falsifier.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
