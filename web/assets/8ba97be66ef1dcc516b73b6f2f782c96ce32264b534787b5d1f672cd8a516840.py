#!/usr/bin/env python3
"""Finite audit of two endpoint-increment compound-Poisson laws.

Pure Python, no simulation and no external packages.  The recursion is exact
for the probability-generating-function coefficients; floating point is used
only for evaluating the Poisson exponential and the displayed divergences.
The support hole at increment 1 is handled explicitly.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


K0 = (1, 1, 4, 0)
K1 = (0, 4, 1, 1)


def pmf(mu: float, rates: tuple[int, ...]) -> list[float]:
    """Return p(0),...,p(N), where N leaves a tiny Chernoff tail."""
    mean = 15.0 * mu
    variance = 41.0 * mu
    nmax = math.ceil(mean + 22.0 * math.sqrt(variance) + 100.0)
    p = [0.0] * (nmax + 1)
    p[0] = math.exp(-6.0 * mu)
    # If G(z)=exp(mu sum_j k_j(z^j-1)), then n p_n is
    # mu sum_j j k_j p_{n-j}.
    for n in range(1, nmax + 1):
        p[n] = (mu / n) * sum(
            j * rates[j - 1] * p[n - j]
            for j in range(1, 5)
            if n >= j
        )
    return p


def chernoff_tail(mu: float, rates: tuple[int, ...], nmax: int) -> float:
    """Optimized exponential upper bound for P(X > nmax)."""
    target = nmax + 1

    def derivative(s: float) -> float:
        return mu * sum(j * rates[j - 1] * math.exp(j * s) for j in range(1, 5)) - target

    lo, hi = 0.0, 1.0
    while derivative(hi) < 0.0:
        hi *= 2.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if derivative(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    s = (lo + hi) / 2.0
    log_bound = mu * sum(rates[j - 1] * (math.exp(j * s) - 1.0) for j in range(1, 5)) - s * target
    return min(1.0, math.exp(log_bound))


def compare(mu: float) -> dict[str, float | int]:
    p0 = pmf(mu, K0)
    p1 = pmf(mu, K1)
    nmax = min(len(p0), len(p1)) - 1
    tv = 0.5 * sum(abs(p0[i] - p1[i]) for i in range(nmax + 1))
    affinity = sum(math.sqrt(p0[i] * p1[i]) for i in range(nmax + 1))
    h2 = 1.0 - affinity  # normalized squared Hellinger distance
    kl_1_0 = sum(
        p1[i] * math.log(p1[i] / p0[i])
        for i in range(nmax + 1)
        if p1[i] > 0.0
    )
    return {
        "mu": mu,
        "nmax": nmax,
        "sum_p0": sum(p0),
        "sum_p1": sum(p1),
        "chernoff_tail_p0": chernoff_tail(mu, K0, nmax),
        "chernoff_tail_p1": chernoff_tail(mu, K1, nmax),
        "tv": tv,
        "hellinger_squared": h2,
        "kl_p1_to_p0": kl_1_0,
        "mu_times_kl_p1_to_p0": mu * kl_1_0,
        "mu_times_h2": mu * h2,
        "sqrt_mu_times_tv": math.sqrt(mu) * tv,
        "p0_increment_1": mu * math.exp(-6.0 * mu),
        "p1_increment_1": 0.0,
    }


def main() -> None:
    mus = (1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 24.0, 32.0, 40.0, 48.0, 56.0)
    rows = [compare(mu) for mu in mus]
    # Fixed T=1 and critical sequence V=m^2, Delta=1/m, mu=m, n=m.
    critical = []
    for m in (4, 8, 16, 32, 48):
        row = compare(float(m))
        critical.append({
            "T": 1.0,
            "V": m * m,
            "Delta": 1.0 / m,
            "mu": float(m),
            "bins": m,
            "total_KL_P1_to_P0": m * float(row["kl_p1_to_p0"]),
            "limiting_total_KL_constant": 3.0 / (41.0**3),
        })
    result = {
        "method": "PGF coefficient recurrence plus optimized Chernoff truncation bound",
        "rates_h0": list(K0),
        "rates_h1": list(K1),
        "predicted_limits": {
            "mu_KL_P1_to_P0": 3.0 / (41.0**3),
            "mu_Hellinger_squared": 0.75 / (41.0**3),
            "sqrt_mu_TV": (1.0 / math.sqrt(2.0 * math.pi)) * (1.0 + 4.0 * math.exp(-1.5)) / (41.0**1.5),
        },
        "rows": rows,
        "critical_cadence_T1": critical,
        "directed_KL_P0_to_P1": "infinity, since P0(X=1)=mu*exp(-6*mu)>0 and P1(X=1)=0",
    }
    out = Path(__file__).with_name("exact_law_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
