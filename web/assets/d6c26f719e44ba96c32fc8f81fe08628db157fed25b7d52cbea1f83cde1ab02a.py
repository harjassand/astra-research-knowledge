#!/usr/bin/env python3
"""Exact finite checks for the boundary-modulated endotactic Foster certificate.

The proof in INITIAL.txt supplies the all-state algebra. This script checks the
displayed generator formula and rational drift inequality on bounded fixtures;
it is a diagnostic, not a proof of the universal quantified inequality.
"""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def ceil_fraction(x: F) -> int:
    return (x.numerator + x.denominator - 1) // x.denominator


def params(alpha: F, beta: F, gamma: F):
    q = max(1, ceil_fraction(2 * beta / gamma))
    delta = min(alpha / (q * (q + 1)), gamma / (2 * (q + 1)))
    eta = min(delta * q, beta)
    return q, delta, eta


def potential(a: int, b: int, q: int) -> F:
    return F(a, b + q) + b


def generator(a: int, b: int, m: int, alpha: F, beta: F, gamma: F, q: int) -> F:
    value = F(0)
    value += alpha * (potential(a, b + 1, q) - potential(a, b, q))
    if b >= 1:
        value += beta * b * (potential(a + m, b - 1, q) - potential(a, b, q))
    if a >= 1 and b >= 1:
        value += gamma * a * b * (potential(a - 1, b, q) - potential(a, b, q))
    return value


def closed_form(a: int, b: int, m: int, alpha: F, beta: F, gamma: F, q: int) -> F:
    if b == 0:
        return -alpha * a / (q * (q + 1)) + alpha
    coefficient = (
        -alpha / ((b + q) * (b + q + 1))
        + beta * b / ((b + q - 1) * (b + q))
        - gamma * b / (b + q)
    )
    additive = alpha + m * beta * b / (b + q - 1) - beta * b
    return coefficient * a + additive


def check_case(m: int, alpha: F, beta: F, gamma: F, bound: int = 60):
    q, delta, eta = params(alpha, beta, gamma)
    constant = alpha + m * beta
    checks = 0
    for a, b in product(range(bound + 1), repeat=2):
        actual = generator(a, b, m, alpha, beta, gamma, q)
        formula = closed_form(a, b, m, alpha, beta, gamma, q)
        assert actual == formula, (m, alpha, beta, gamma, q, a, b, actual, formula)
        v = potential(a, b, q)
        assert actual <= constant - eta * v, (m, alpha, beta, gamma, q, a, b, actual, v)
        checks += 1
    return {
        "m": m,
        "rates": [str(alpha), str(beta), str(gamma)],
        "q": q,
        "delta": str(delta),
        "eta": str(eta),
        "constant": str(constant),
        "states_checked": checks,
        "max_coordinate": bound,
        "result": "PASS",
    }


def main():
    cases = [
        (1, F(1), F(1), F(1)),
        (2, F(1), F(1), F(1)),
        (3, F(1, 3), F(5, 2), F(2, 3)),
        (2, F(7, 5), F(3, 2), F(5, 4)),
        (4, F(2, 7), F(11, 3), F(1, 2)),
    ]
    results = [check_case(*case) for case in cases]
    out = {
        "scope": "exact rational fixtures for the derived Foster inequality; not an all-state proof",
        "total_states_checked": sum(x["states_checked"] for x in results),
        "cases": results,
    }
    target = Path(__file__).with_name("CHECK_RESULTS.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
