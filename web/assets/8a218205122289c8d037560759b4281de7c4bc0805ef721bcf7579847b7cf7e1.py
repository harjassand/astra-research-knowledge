#!/usr/bin/env python3
"""Two explicit boundaries for the ideal integer-count cadence result."""

from __future__ import annotations

import json
import math
from pathlib import Path

K0 = (1, 1, 4, 0)
K1 = (0, 4, 1, 1)


def gamma_mixed_pmf(mu: float, rates: tuple[int, ...], shape: int = 10) -> list[float]:
    """PMF when a fresh hidden Gamma(shape, rate=shape) activity multiplies
    every channel rate in each observation interval.

    Its PGF is [1-(mu/shape) sum_j k_j(z^j-1)]^(-shape).
    """
    a0 = 1.0 + 6.0 * mu / shape
    nmax = math.ceil(200.0 * mu + 100.0)
    p = [0.0] * (nmax + 1)
    p[0] = a0 ** (-shape)
    for n in range(1, nmax + 1):
        p[n] = (mu / (a0 * n)) * sum(
            rates[j - 1] * (n / shape + j * (1.0 - 1.0 / shape)) * p[n - j]
            for j in range(1, 5)
            if n >= j
        )
    return p


def parity_row(mu: float, bins: int) -> dict[str, float | int]:
    # An odd-mark event flips parity. Independent even marks are invisible.
    p0_odd = -math.expm1(-10.0 * mu) / 2.0
    p1_odd = -math.expm1(-2.0 * mu) / 2.0
    one_bin_tv = abs(p0_odd - p1_odd)
    return {
        "mu": mu,
        "bins": bins,
        "P0_odd": p0_odd,
        "P1_odd": p1_odd,
        "one_bin_TV": one_bin_tv,
        "product_TV_coupling_upper": min(1.0, bins * one_bin_tv),
        "asymptotic_product_TV_upper": bins * 0.5 * math.exp(-2.0 * mu),
    }


def main() -> None:
    gamma_rows = []
    for mu in (8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0):
        p0 = gamma_mixed_pmf(mu, K0)
        p1 = gamma_mixed_pmf(mu, K1)
        tv = 0.5 * math.fsum(abs(a - b) for a, b in zip(p0, p1))
        gamma_rows.append({
            "mu": mu,
            "truncated_mass_model0": math.fsum(p0),
            "truncated_mass_model1": math.fsum(p1),
            "TV": tv,
            "mu_squared_times_TV": mu * mu * tv,
            "model0_increment_1": p0[1],
            "model1_increment_1": p1[1],
        })

    parity_rows = [parity_row(float(m), m) for m in (2, 4, 8, 16, 32, 64)]
    result = {
        "gamma_interval_activity": {
            "activity_law": "fresh independent Gamma(shape=10, rate=10), mean 1, once per measurement bin",
            "rates_model0": list(K0),
            "rates_model1": list(K1),
            "moment_effect": "unconditional first and second cumulants agree; third-cumulant difference remains 6*mu, but count variance is order mu^2",
            "candidate_local_limit": {
                "limiting_density": "Y=15*A, A~Gamma(10,10)",
                "g_definition": "g(y)=(y/15)f_Y(y)",
                "J_integral": "integral (g'''(y))^2/f_Y(y) dy = 8/3645",
                "normalized_hellinger_affinity_loss": "1-affinity ~ J/(8*mu^4) = 1/(3645*mu^4)",
                "reverse_KL": "D(P1||P0) ~ J/(2*mu^4) = 4/(3645*mu^4)",
                "fixed_T_cadence_boundary": "Delta order V^(-4/5), under this reset-per-bin latent environment",
            },
            "finite_TV_recurrence_rows": gamma_rows,
            "scope": "The random activity is refreshed independently each bin; this is a Cox/state-nuisance countermodel, outside the homogeneous compound-Poisson premise.",
        },
        "parity_only_readout": {
            "exact_model": "same homogeneous compound-Poisson process; sensor reports only cumulative count modulo 2",
            "odd_increment_probabilities": {
                "model0": "(1-exp(-10*mu))/2",
                "model1": "(1-exp(-2*mu))/2",
            },
            "finite_rows": parity_rows,
            "scope": "Data processing cannot improve information; the parity channel loses the polynomial third-cumulant signal and its product TV tends to zero at polynomial critical cadence.",
        },
    }
    out = Path(__file__).with_name("scope_counterexample_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
