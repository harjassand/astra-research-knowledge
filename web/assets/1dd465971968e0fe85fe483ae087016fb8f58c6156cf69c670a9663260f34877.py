#!/usr/bin/env python3
"""Exact small-instance checks for the scalar bimolecular recovery certificate.

This script checks rational identities and finite-state Poisson equations. The
uniform predictable-control proof is in INITIAL.txt; these checks do not replace
that proof or validate the general network certificate search.
"""
from fractions import Fraction as F
from math import comb
import json
from pathlib import Path


def falling(n, m):
    if n < m:
        return 0
    out = 1
    for r in range(m):
        out *= n - r
    return out


def ceil_fraction(x):
    return (x.numerator + x.denominator - 1) // x.denominator


def weights(V, m, kappa, K):
    rho = kappa / K
    out = {}
    for j in range(m - 1, V - m + 2):
        w = rho**j
        for r in range(m):
            w *= comb(V - 2 * r, j - r)
        out[j] = w
    return out


def exact_lower_mean(V, m, kappa, K, L):
    """Exact lower-extremal birth-death mean from m-1 to L."""
    w = weights(V, m, kappa, K)
    diffs = {}
    cumulative = F(0)
    for j in range(m - 1, L):
        cumulative += w[j]
        birth = kappa * F(falling(V - j, m), V ** (m - 1))
        diffs[j] = cumulative / (w[j] * birth)
    h = {L: F(0)}
    for j in range(L - 1, m - 2, -1):
        h[j] = h[j + 1] + diffs[j]

    # Verify the backward Poisson equation exactly at each transient state.
    for j in range(m - 1, L):
        birth = kappa * F(falling(V - j, m), V ** (m - 1))
        death = K * F(falling(j, m), V ** (m - 1))
        rhs = birth * (h[j + 1] - h[j])
        if j > m - 1:
            rhs += death * (h[j - 1] - h[j])
        assert rhs == -1, (V, m, j, rhs)
    return h[m - 1], max(max(x.numerator.bit_length(), x.denominator.bit_length())
                          for x in h.values())


def one_fixture(V, m, kappa, K, q):
    assert V >= 2 * m
    L = (q.numerator * V) // q.denominator
    assert m <= L and 2 * L < V
    fq = kappa * (1 - q) ** m - K * q**m
    assert fq > 0
    eta = fq / (2 * m * (kappa + K))
    u = q + eta
    fu = kappa * (1 - u) ** m - K * u**m
    assert fu >= fq / 2 > 0
    mu = F(1, V ** (m - 1)) * (
        kappa * falling(V - L, m) - K * falling(L, m)
    )
    assert mu > 0
    delta = fu
    assert mu / V >= delta

    # Exact drift floor for every left-outside state under the worst controls.
    for j in range(m - 1, L):
        drift_floor = F(1, V ** (m - 1)) * (
            kappa * falling(V - j, m) - K * falling(j, m)
        )
        assert drift_floor >= mu

    S = kappa + K * F(L, V) ** m
    theta = mu / (2 * V * S)
    alpha = mu**2 / (4 * V * S)
    assert 0 < theta <= F(1, 2)
    gap = L - (m - 1)
    expected_upper = F(gap, 1) / mu
    return_time = F(4 * gap, 1) / mu
    tail_exponent = theta * gap - alpha * return_time
    assert tail_exponent == -mu * gap / (2 * V * S)
    exact_mean, mean_bits = exact_lower_mean(V, m, kappa, K, L)
    assert exact_mean <= expected_upper

    firing_rate_upper = K * V * (1 + F(L, V) ** m)
    firing_count_upper = firing_rate_upper * expected_upper
    return {
        "V": V,
        "m": m,
        "L": L,
        "kappa": str(kappa),
        "K": str(K),
        "q": str(q),
        "f_q": str(fq),
        "eta": str(eta),
        "u": str(u),
        "delta": str(delta),
        "mu_V": str(mu),
        "mu_V_over_V": str(mu / V),
        "S_L": str(S),
        "theta": str(theta),
        "alpha": str(alpha),
        "worst_start_expected_return_upper": str(expected_upper),
        "uniform_return_tail_time": str(return_time),
        "uniform_tail_exponent_at_that_time": str(tail_exponent),
        "exact_lower_chain_mean": str(exact_mean),
        "exact_mean_max_numerator_or_denominator_bits": mean_bits,
        "expected_firing_count_upper": str(firing_count_upper),
        "mu_numerator_or_denominator_bits": max(mu.numerator.bit_length(), mu.denominator.bit_length()),
        "exact_check": "PASS"
    }


def main():
    fixtures = [
        one_fixture(V, 2, F(1), F(4), F(1, 4))
        for V in (64, 128, 256)
    ]

    # A true second-order family with O(b)-bit rate/core data and a vanishing
    # large-deviation exponent. The asymptotic for Delta is proved in INITIAL.
    b = 8
    M = 1 << b
    N = M + 1
    q = F(M, N * N)
    kappa, K = F(1), F(M * M)
    p = F(1, N)
    fq = kappa * (1 - q) ** 2 - K * q**2
    eta = fq / (4 * (kappa + K))
    u = q + eta
    volume_floor = max(2 * 2, ceil_fraction(F(2, 1) / q),
                       ceil_fraction(F(1, 1) / eta))
    if volume_floor % 2:
        volume_floor += 1
    bit_family = {
        "m": 2,
        "rate_parameter_b": b,
        "M": M,
        "N": N,
        "kappa": str(kappa),
        "K": str(K),
        "p": str(p),
        "q": str(q),
        "p_minus_q": str(p - q),
        "f_q": str(fq),
        "eta": str(eta),
        "u": str(u),
        "our_conservative_return_certificate_even_volume_floor": volume_floor,
        "rate_encoding_bits": K.numerator.bit_length(),
        "q_encoding_numerator_bits": q.numerator.bit_length(),
        "q_encoding_denominator_bits": q.denominator.bit_length(),
        "scope": "cost illustration; the conservative volume threshold is not a lower bound"
    }
    report = {
        "status": "exact rational fixture checks; proof remains in INITIAL.txt",
        "fixtures": fixtures,
        "narrow_margin_family": bit_family,
        "verified": "finite-volume drift floors and lower-chain backward Poisson equations"
    }
    out = Path(__file__).with_name("recovery_return_cost_checks.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
