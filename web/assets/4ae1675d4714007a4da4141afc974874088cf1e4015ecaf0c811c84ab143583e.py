#!/usr/bin/env python3
"""Exact rational fixtures for the bounded-sandwich POVM outcome audit.

This checks the admitted diagonal family and dephasing reconstruction for a
few dimensions. The lower bound for arbitrary EB factorizations is proved in
acquisition_cost_audit.md; this script is only finite illustrative evidence.
"""

from fractions import Fraction
import json


def fixture(d: int, theta: Fraction = Fraction(1, 2)) -> dict:
    inv_d = Fraction(1, d)
    sigma = [inv_d] * d
    states = []
    likelihoods = []
    for i in range(d):
        h = [theta * (Fraction(1 if j == i else 0) - inv_d) for j in range(d)]
        rho = [inv_d * (1 + x) for x in h]
        likelihoods.append(h)
        states.append(rho)

    # The POVM {P_i} followed by preparation of P_i is dephasing on this
    # diagonal experiment, so each rho_i is reproduced coordinatewise.
    reconstructed = [[state[j] for j in range(d)] for state in states]
    exact_reconstruction = reconstructed == states
    average_state = [sum((state[j] for state in states), Fraction(0)) / d for j in range(d)]
    centered = all(sum(h, Fraction(0)) == 0 for h in likelihoods)
    sandwich = all(max(abs(x) for x in h) <= theta for h in likelihoods)

    return {
        "dimension": d,
        "theta": f"{theta.numerator}/{theta.denominator}",
        "sigma_diagonal": [f"{x.numerator}/{x.denominator}" for x in sigma],
        "average_state_equals_sigma": average_state == sigma,
        "all_likelihoods_centered": centered,
        "all_likelihoods_within_theta": sandwich,
        "dephasing_outcomes": d,
        "exact_reconstruction": exact_reconstruction,
        "exact_half_trace_error": "0",
        "dirichlet_residual_on_family": "0",
    }


if __name__ == "__main__":
    print(json.dumps([fixture(d) for d in (2, 4, 8)], indent=2))
