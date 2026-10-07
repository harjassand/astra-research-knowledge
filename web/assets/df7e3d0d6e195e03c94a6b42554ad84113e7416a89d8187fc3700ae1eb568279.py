#!/usr/bin/env python3
"""Exact rational spectral check for the invariant-EB-projection lemma."""

from fractions import Fraction as F
import json

center_spectrum = [F(1), F(9, 16)]
fiber_spectrum = [F(1, 4), F(1, 16)]
rows = []
for m in range(1, 13):
    kappa_m = F(1, 4) ** m
    c = 1 / (1 - kappa_m)
    max_difference = F(0)
    minimum_slack = None
    for lam in center_spectrum:
        # On the EB range, E Phi^m equals Phi^m exactly.
        psi_lam = lam**m
        diff = abs(lam**m - psi_lam)
        slack = c * (1 - lam**m) - (1 - psi_lam)
        max_difference = max(max_difference, diff)
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
    for lam in fiber_spectrum:
        # E vanishes on the fiber complement.
        psi_lam = F(0)
        diff = abs(lam**m - psi_lam)
        slack = c * (1 - lam**m) - (1 - psi_lam)
        max_difference = max(max_difference, diff)
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
    assert max_difference == kappa_m
    assert minimum_slack >= 0
    rows.append({
        "m": m,
        "kappa_power": str(kappa_m),
        "comparison_constant": str(c),
        "max_L2_and_infinity_to_one_difference": str(max_difference),
        "minimum_dirichlet_slack": str(minimum_slack),
    })

result = {
    "status": "PASS",
    "center_spectrum_of_Phi": [str(x) for x in center_spectrum],
    "fiber_spectrum_of_Phi": [str(x) for x in fiber_spectrum],
    "checks": rows,
    "scope": "exact scalar spectral checks; not a proof of the operator decomposition or the peer's broadcaster construction",
}
print(json.dumps(result, indent=2))
