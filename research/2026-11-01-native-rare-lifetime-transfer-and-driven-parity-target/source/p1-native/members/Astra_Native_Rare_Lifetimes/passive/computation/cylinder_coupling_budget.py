"""Exact ordinary monotone-sandwich budget for a cylinder hitting mean.

No trajectories are generated. Fraction arithmetic solves the two biased
birth-death references exactly; decimal output is only presentation.
"""

from fractions import Fraction
from math import comb
import json
from pathlib import Path


def stationary_hitting(m, up, down):
    """Unconditional stationary mean of tau_0 for the m-bit count chain."""
    increments = [Fraction(0) for _ in range(m + 1)]
    increments[m] = 1 / (down * m)
    for j in range(m - 1, 0, -1):
        increments[j] = (1 + up * (m - j) * increments[j + 1]) / (down * j)
    hitting = []
    t = Fraction(0)
    for increment in increments:
        t += increment
        hitting.append(t)
    rho = up / (up + down)
    masses = [comb(m, j) * rho**j * (1 - rho) ** (m - j) for j in range(m + 1)]
    assert sum(masses) == 1
    mu = sum(masses[j] * hitting[j] for j in range(1, m + 1))
    # Independently check every positive-state Poisson equation exactly.
    for j in range(1, m + 1):
        residual = down * j * (hitting[j] - hitting[j - 1])
        if j < m:
            residual += up * (m - j) * (hitting[j] - hitting[j + 1])
        assert residual == 1
    return mu, 1 - masses[0], masses[0]


def main():
    n, m = 80, 64
    c, eta = Fraction(1, 2), Fraction("0.000391378")
    mu0, b0, p0 = stationary_hitting(m, c, c)
    mu_low, b_low, p_low = stationary_hitting(m, c * (1 - eta), c * (1 + eta))
    mu_high, b_high, p_high = stationary_hitting(m, c * (1 + eta), c * (1 - eta))
    mean0 = mu0 / b0
    mean_lower, mean_upper = mu_low / b_high, mu_high / b_low
    lower_ratio, upper_ratio = mean_lower / mean0, mean_upper / mean0
    assert b_low <= b0 <= b_high
    assert mu_low <= mu0 <= mu_high
    assert lower_ratio < 1 < upper_ratio
    result = {
        "calculation": "exact rational biased birth-death recurrence; no trajectories",
        "n": n,
        "m": m,
        "c": str(c),
        "eta": str(eta),
        "eta_decimal": float(eta),
        "reference_target_probability": float(p0),
        "lower_chain_target_probability": float(p_low),
        "upper_chain_target_probability": float(p_high),
        "reference_conditional_mean": float(mean0),
        "actual_conditional_mean_lower_bound": float(mean_lower),
        "actual_conditional_mean_upper_bound": float(mean_upper),
        "actual_to_reference_mean_lower_ratio": float(lower_ratio),
        "actual_to_reference_mean_upper_ratio": float(upper_ratio),
        "lower_chain_conditional_mean_ratio": float((mu_low / b_low) / mean0),
        "upper_chain_conditional_mean_ratio": float((mu_high / b_high) / mean0),
        "exact_rational_assertions": {
            "lower_ratio_exceeds_0.975": lower_ratio > Fraction(975, 1000),
            "upper_ratio_below_1.025": upper_ratio < Fraction(1025, 1000),
            "every_birth_death_Poisson_equation_exact": True,
        },
        "scope": "all actual single-bit sources inside the uniform rate box, regardless of monotonicity or free-coordinate dependence; target first m bits zero; initial actual stationary conditional complement",
    }
    output = Path(__file__).with_name("cylinder_coupling_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
