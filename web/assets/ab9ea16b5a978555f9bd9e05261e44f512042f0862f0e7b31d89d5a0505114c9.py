#!/usr/bin/env python3
"""Compound-Poisson PMF and information audit using a log-domain recurrence.

The recurrence is Panjer's recursion for a compound Poisson law with
integer marks.  This implementation stores log coefficients q_n in
exp(mu * sum_j k_j z^j), avoiding exp(6 mu) overflow in an unscaled table.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

RATES = ((1, 1, 4, 0), (0, 4, 1, 1))
M2 = 41
M3 = (117, 123)
M4 = (341, 401)
M6 = (2981, 5081)


def max_count(mu: float) -> int:
    # More than 20 standard deviations beyond the shared mean, with a
    # 100-count cushion for the small-mu rows.
    return math.ceil(15 * mu + 20 * math.sqrt(41 * mu) + 100)


def logsumexp(values: list[float]) -> float:
    top = max(values)
    if top == -math.inf:
        return top
    return top + math.log(math.fsum(math.exp(value - top) for value in values))


def panjer_log_coefficients(mu: float, rates: tuple[int, ...], cutoff: int) -> list[float]:
    logq = [-math.inf] * (cutoff + 1)
    logq[0] = 0.0
    for n in range(1, cutoff + 1):
        terms = [
            math.log(j * rates[j - 1]) + logq[n - j]
            for j in range(1, min(len(rates), n) + 1)
            if rates[j - 1] and logq[n - j] > -math.inf
        ]
        if terms:
            logq[n] = math.log(mu / n) + logsumexp(terms)
    return logq


def kl_remainder(log_ratio: float) -> float:
    """Return exp(d)*d-exp(d)+1 stably; this is nonnegative for real d."""
    if not math.isfinite(log_ratio):
        return 1.0  # The only nonfinite ratio here is P1=0<P0.
    if abs(log_ratio) < 0.1:
        return math.fsum(
            (order - 1) * log_ratio**order / math.factorial(order)
            for order in range(2, 14)
        )
    return 1.0 + (log_ratio - 1.0) * math.exp(log_ratio)


def kl_weighted(p0: float, p1: float, log_ratio: float) -> float:
    if not math.isfinite(log_ratio):
        return p0
    if abs(log_ratio) < 0.1:
        return p0 * kl_remainder(log_ratio)
    return p0 + p1 * (log_ratio - 1.0)


def log_tail_chernoff(mu: float, rates: tuple[int, ...], threshold: int) -> float:
    """Log Chernoff upper bound P(S >= threshold), optimized over t>=0."""
    target = threshold / mu

    def derivative(t: float) -> float:
        return math.fsum(j * rates[j - 1] * math.exp(j * t)
                         for j in range(1, len(rates) + 1))

    lo, hi = 0.0, 1.0
    while derivative(hi) < target:
        hi *= 2
    for _ in range(80):
        mid = (lo + hi) / 2
        if derivative(mid) < target:
            lo = mid
        else:
            hi = mid
    t = (lo + hi) / 2
    cumulant = math.fsum(rates[j - 1] * (math.exp(j * t) - 1)
                         for j in range(1, len(rates) + 1))
    return mu * cumulant - t * threshold


def audit(mu: float) -> dict[str, float | int]:
    cutoff = max_count(mu)
    logqs = [panjer_log_coefficients(mu, rates, cutoff) for rates in RATES]
    logps = [[value - 6 * mu for value in row] for row in logqs]
    probs = [[math.exp(value) if value > -745 else 0.0 for value in row]
             for row in logps]
    p0, p1 = probs

    affinity = math.fsum(math.sqrt(a) * math.sqrt(b) for a, b in zip(p0, p1))
    h2 = math.fsum((math.sqrt(a) - math.sqrt(b)) ** 2 for a, b in zip(p0, p1))
    d10 = math.fsum(
        kl_weighted(p0[n], p1[n], logqs[1][n] - logqs[0][n])
        for n in range(cutoff + 1)
        if p0[n] > 0 or p1[n] > 0
    )
    tails = [math.exp(log_tail_chernoff(mu, rates, cutoff + 1)) for rates in RATES]
    affinity_upper = affinity + math.sqrt(tails[0] * tails[1])
    variance_u = [
        6
        + 9 * M4[b] / (M2**2 * mu)
        + 9 * M3[b] ** 2 / (M2**3 * mu)
        + M6[b] / (M2**3 * mu**2)
        for b in range(2)
    ]
    delta_mean = 6 / (M2**1.5 * math.sqrt(mu))
    finite_tests = []
    for lam in (1, 10, 100, 124_288):
        n = round(lam * mu)
        a_lower_n = affinity**n
        a_upper_n = affinity_upper**n
        tv_upper = math.sqrt(max(0.0, 1 - a_lower_n**2))
        finite_tests.append({
            "n_over_mu_approx": n / mu,
            "increments_n": n,
            "equal_prior_error_lower_from_affinity": (1 - tv_upper) / 2,
            "equal_prior_error_upper_from_affinity": min(0.5, a_upper_n / 2),
            "score_test_typeI_plus_typeII_Chebyshev_upper": min(
                2.0,
                4 * (variance_u[0] + variance_u[1]) / (n * delta_mean**2),
            ),
        })
    return {
        "mu": mu,
        "cutoff": cutoff,
        "mass0_truncated": math.fsum(p0),
        "mass1_truncated": math.fsum(p1),
        "chernoff_tail0": tails[0],
        "chernoff_tail1": tails[1],
        "affinity_truncated": affinity,
        "H2_truncated": h2,
        "mu_H2_truncated": mu * h2,
        "KL_1_to_0_truncated": d10,
        "mu_KL_1_to_0_truncated": mu * d10,
        "target_mu_H2": 3 / (2 * 41**3),
        "target_mu_KL": 3 / 41**3,
        "finite_test_bounds": finite_tests,
    }


def main() -> None:
    rows = [audit(mu) for mu in (1, 2, 5, 10, 20, 40, 80, 100, 250, 1000)]
    output = {
        "rates": {"model0": RATES[0], "model1": RATES[1]},
        "recurrence": "logq[0]=0; logq[n]=log(mu/n)+logsumexp_j(log(j*k_j)+logq[n-j]); logp[n]=logq[n]-6*mu",
        "support_check": {
            "p0_at_one": "mu*exp(-6*mu)",
            "p1_at_one": 0,
            "KL_0_to_1": "infinity for every mu>0",
        },
        "rows": rows,
        "scope": "finite floating-point recurrence with explicit Chernoff truncation bounds; this is diagnostic evidence, not the asymptotic proof",
    }
    out = Path(__file__).with_name("exact_cp_audit.json")
    out.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
