#!/usr/bin/env python3
"""Exact algebra/sample check for the conditional Grassmann scalar lemma."""
from fractions import Fraction as F

import sympy as sp


def symbolic_identity_check() -> None:
    d, m, x = sp.symbols("d m x")
    u = (2 * m + x) / (2 * m + d - x)
    v = (m + x) * (2 * m + d - x) / ((m + d - x) * (2 * m + x))
    alpha = d / (2 * (m + d))
    kappa = (2 * m + d) / (2 * (m + d))
    nonpositive = (
        (-x) * (d - 2 * x) * (d**2 + 3 * d * m - (d + 2 * m) * x)
        / (2 * (d + m) * (2 * m + x) * (d + 2 * m - x) * (d + m - x))
    )
    positive = (
        m * (d - x) * (d - 2 * x) ** 2
        / ((d + 2 * m) * (2 * m + x) * (d + 2 * m - x) * (d + m - x))
    )
    difference = v - u
    difference_form = (
        (d - 2 * x) * (d * m + d * x - x**2)
        / ((2 * m + x) * (d + 2 * m - x) * (d + m - x))
    )
    assert sp.cancel(alpha + kappa * u - v - nonpositive) == 0
    assert sp.cancel((d + 2 * m * u) / (d + 2 * m) - v - positive) == 0
    assert sp.cancel(difference - difference_form) == 0


def column_scan() -> dict:
    checked = 0
    worst = F(0)
    worst_case = None
    for d in range(2, 41):
        for m in range(1, 13):
            alpha = F(d, 2 * (m + d))
            kappa = F(2 * m + d, 2 * (m + d))
            for t in range(m):
                for h in range(1, d // 2 + 1):
                    U = V = F(1)
                    for j in range(h):
                        x = j - t
                        u = F(2 * m + x, 2 * m + d - x)
                        v = F((m + x) * (2 * m + d - x), (m + d - x) * (2 * m + x))
                        U *= u
                        V *= v
                    assert V <= alpha + kappa * U, (d, m, t, h, U, V)
                    ratio = (F(1) - U) / (F(1) - V)
                    assert ratio <= 1 / kappa, (d, m, t, h, ratio, 1 / kappa)
                    checked += 1
                    if ratio > worst:
                        worst = ratio
                        worst_case = (d, m, t, h)
    return {
        "status": "PASS_EXACT_RATIONAL",
        "symbolic_identities": 3,
        "column_cases": checked,
        "max_column_ratio": str(worst),
        "max_case_d_m_t_h": worst_case,
        "scope": "Finite exact checks; theorem is the conditional proof in GRASSMANN_SCALAR_LEMMA.txt.",
    }


if __name__ == "__main__":
    symbolic_identity_check()
    import json

    print(json.dumps(column_scan(), indent=2))
