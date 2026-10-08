#!/usr/bin/env python3
"""Rational finite checks for the two-state horizon-gap construction."""
from fractions import Fraction as F
from itertools import product
from math import log
import json


ETA = F(1, 2)
SIGNS = (1, -1)


def trans(rho):
    return [[(1 + rho) / 2, (1 - rho) / 2],
            [(1 - rho) / 2, (1 + rho) / 2]]


def emit(y, state):
    return (1 + ETA * y * state) / 2


def word_prob(word, rho):
    """Exact stationary probability of an observed sign word."""
    p = trans(rho)
    weights = [F(1, 2), F(1, 2)]
    for t, y in enumerate(word):
        weights = [weights[i] * emit(y, SIGNS[i]) for i in range(2)]
        if t != len(word) - 1:
            weights = [sum((weights[i] * p[i][j] for i in range(2)), F(0))
                       for j in range(2)]
    return sum(weights, F(0))


def g(x):
    x = float(x)
    return 0.5 * ((1 + x) * log(1 + x) + (1 - x) * log(1 - x))


def conditional_future_kl(rho, context_len, horizon):
    total = 0.0
    for context in product(SIGNS, repeat=context_len):
        p_context = word_prob(context, rho)
        for future in product(SIGNS, repeat=horizon):
            p_joint = word_prob(context + future, rho)
            p_cond = float(p_joint / p_context)
            total += float(p_joint) * log(p_cond * (2 ** horizon))
    return total


def check(rho):
    k = 2
    p = trans(rho)
    e = [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]
    assert all(sum(row, F(0)) == 1 for row in p)
    assert all(sum(row, F(0)) == 1 for row in e)
    assert min(min(row) for row in p) >= F(3, 8)
    assert min(min(row) for row in e) >= F(1, 4)

    c = ETA * ETA * rho
    h1 = [[(1 + c) / 4, (1 - c) / 4],
          [(1 - c) / 4, (1 + c) / 4]]
    gamma = c / 2
    determinant = h1[0][0] * h1[1][1] - h1[0][1] * h1[1][0]
    assert determinant == c / 4
    assert sum(h1[0], F(0)) == F(1, 2)
    assert sum(h1[1], F(0)) == F(1, 2)
    assert h1[0][0] - h1[0][1] == gamma
    rank1 = [[F(1, 4), F(1, 4)], [F(1, 4), F(1, 4)]]
    checkerboard = ((1, -1), (-1, 1))
    assert all(h1[i][j] - rank1[i][j] == c * checkerboard[i][j] / 4
               for i in range(2) for j in range(2))

    # Enumerate positive raw laws and finite-context H-step risks.
    laws = {}
    for length in range(1, 8):
        probs = [word_prob(w, rho) for w in product(SIGNS, repeat=length)]
        assert sum(probs, F(0)) == 1
        assert min(probs) >= F(1, 2) * F(1, 4) ** (length - 1)
        laws[str(length)] = {
            "word_count": len(probs),
            "min_word_probability": str(min(probs)),
        }

    c_float = float(c)
    contexts = []
    for w in (1, 2, 3):
        for h in (1, 2, 3):
            risk = conditional_future_kl(rho, w, h)
            lo, hi = h * g(c), h * g(rho)
            assert lo - 1e-12 <= risk <= hi + 1e-12
            contexts.append({"history_length": w, "future_horizon": h,
                              "risk": risk, "lower": lo, "upper": hi})

    rho_float = float(rho)
    return {
        "rho": str(rho),
        "K": k,
        "transition_floor": str(min(min(row) for row in p)),
        "emission_floor": "1/4",
        "Hankel_sigma_2_gamma": str(gamma),
        "analytic_sigma_1": "1/2",
        "min_history_mass_bound": "(1/2)*(1/4)^(length-1)",
        "raw_law_checks": laws,
        "finite_context_risks_within_H_g_bounds": contexts,
        "asymptotic_modulus_constants": {
            "lower_ratio_R_over_Hgamma2": 2.0,
            "upper_ratio_R_over_Hgamma2": 512.0 / 15.0,
            "rho": rho_float,
            "c": c_float,
        },
    }


if __name__ == "__main__":
    fixtures = [check(F(1, 4)), check(F(1, 8)), check(F(1, 16)), check(F(0))]
    print(json.dumps({"status": "FINITE-RATIONAL-CHECKS-PASS",
                      "fixtures": fixtures}, indent=2))
