#!/usr/bin/env python3
"""Exact finite diagnostics for an aggregate-cofactor Foster certificate.

All rates and checks use fractions. The script has no external dependencies.
It checks the complete generator against the derived inequality on bounded
boxes only; the all-state statement is proved separately in the paired note.
"""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


FIXTURES = [
    {"name": "one_cofactor_unit", "alpha": [F(1)], "beta": [F(1)],
     "gamma": [F(1)], "births": [2], "extent": 60},
    {"name": "two_heterogeneous", "alpha": [F(1), F(2, 3)],
     "beta": [F(1), F(5, 4)], "gamma": [F(1), F(3, 2)],
     "births": [1, 2], "extent": 18},
    {"name": "three_heterogeneous", "alpha": [F(2, 5), F(3, 2), F(4, 3)],
     "beta": [F(3, 4), F(7, 5), F(5, 3)],
     "gamma": [F(2, 3), F(4, 5), F(7, 4)],
     "births": [1, 2, 1], "extent": 9},
]


def ceil_fraction(x):
    return (x.numerator + x.denominator - 1) // x.denominator


def certify(alpha, beta, gamma):
    assert len(alpha) == len(beta) == len(gamma) and len(alpha) >= 1
    assert all(x > 0 for x in alpha + beta + gamma)
    q = max(2, ceil_fraction(2 * max(beta) / min(gamma)))
    dlt = min(sum(alpha, F(0)) / (q * (q + 1)),
              min(gamma) / (2 * (q + 1)))
    eta = min(q * dlt, min(beta) / 2)
    return q, dlt, eta, 2 * sum(alpha, F(0))


def potential(a, bs, q):
    n = sum(bs)
    return F(a, n + q) + 2 * n


def direct_lv(a, bs, alpha, beta, gamma, births, q):
    v0 = potential(a, bs, q)
    total = F(0)
    for i, bi in enumerate(bs):
        # 0 -> B_i
        after = list(bs)
        after[i] += 1
        total += alpha[i] * (potential(a, after, q) - v0)
        # B_i -> 2A
        if bi:
            after = list(bs)
            after[i] -= 1
            total += beta[i] * bi * (potential(a + births[i], after, q) - v0)
        # A + B_i -> B_i
        if a and bi:
            total += gamma[i] * a * bi * (potential(a - 1, bs, q) - v0)
    return total


def formula_lv(a, bs, alpha, beta, gamma, births, q):
    n = sum(bs)
    asum = sum(alpha, F(0))
    beta_n = sum((beta[i] * bs[i] for i in range(len(bs))), F(0))
    gamma_n = sum((gamma[i] * bs[i] for i in range(len(bs))), F(0))
    c = -asum / ((n + q) * (n + q + 1))
    if n:
        c += beta_n / ((n + q - 1) * (n + q))
        c -= gamma_n / (n + q)
        d = 2 * asum + sum((beta[i] * bs[i] *
                            (F(births[i], n + q - 1) - 2)
                            for i in range(len(bs))), F(0))
    else:
        d = 2 * asum
    return a * c + d


def run_fixture(fixture):
    alpha, beta, gamma = fixture["alpha"], fixture["beta"], fixture["gamma"]
    births = fixture["births"]
    assert len(alpha) == len(births) and all(m in (1, 2) for m in births)
    q, dlt, eta, const = certify(alpha, beta, gamma)
    E = fixture["extent"]
    checked = 0
    min_slack = None
    for a in range(E + 1):
        for bs in product(range(E + 1), repeat=len(alpha)):
            lv = direct_lv(a, bs, alpha, beta, gamma, births, q)
            lv_formula = formula_lv(a, bs, alpha, beta, gamma, births, q)
            assert lv == lv_formula, (a, bs, lv, lv_formula)
            v = potential(a, bs, q)
            slack = -eta * v + const - lv
            assert slack >= 0, (a, bs, lv, v, slack)
            min_slack = slack if min_slack is None else min(min_slack, slack)
            checked += 1
    return {
        "name": fixture["name"],
        "cofactors": len(alpha),
        "A_birth_multiplicities": births,
        "extent": E,
        "states_checked": checked,
        "q": q,
        "delta": str(dlt),
        "eta": str(eta),
        "constant": str(const),
        "min_exact_slack": str(min_slack),
        "result": "PASS",
    }


if __name__ == "__main__":
    out = {
        "scope": "finite exact checks only; symbolic inequalities are in multico_factor_aggregate.txt",
        "method": "Python fractions, complete transition generator, no simulation",
        "fixtures": [run_fixture(f) for f in FIXTURES],
    }
    print(json.dumps(out, indent=2))
