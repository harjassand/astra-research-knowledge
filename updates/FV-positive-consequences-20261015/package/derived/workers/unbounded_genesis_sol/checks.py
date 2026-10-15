#!/usr/bin/env python3
"""Finite algebra/bound diagnostics; not a substitute for the infinite proof."""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import sympy as sp


def odd_df(k: int) -> int:
    ans = 1
    for j in range(k, 0, -2):
        ans *= j
    return ans


def mu_moment(p: int, q: int) -> Fraction:
    if p < 0 or q < 0 or p % 2 or q % 2:
        return Fraction(0)
    return Fraction(odd_df(p - 1) * odd_df(q - 1), odd_df(p + q + 1))


def kernel_moment(p: int, q: int):
    a, b = Fraction(2), Fraction(3, 5)
    scalar = (1 + p + q) * a**p * b**q * mu_moment(p, q)
    zz = p * a**p * b**q * mu_moment(p - 1, q) if p else Fraction(0)
    xx = q * a**p * b**q * mu_moment(p, q - 1) if q else Fraction(0)
    return scalar, zz, xx


def exponential_moment(p: int, q: int):
    """Coefficient in exp(s a sigma_z+t b sigma_x), times p!q!."""
    a, b = Fraction(2), Fraction(3, 5)
    degree = p + q
    fac = Fraction(math.factorial(p) * math.factorial(q), math.factorial(degree))
    if degree % 2 == 0:
        if p % 2 or q % 2:
            return Fraction(0), Fraction(0), Fraction(0)
        k = degree // 2
        scalar = fac * math.comb(k, p // 2) * a**p * b**q
        return scalar, Fraction(0), Fraction(0)
    k = degree // 2
    zz = fac * math.comb(k, (p - 1) // 2) * a**p * b**q if p % 2 and not q % 2 else Fraction(0)
    xx = fac * math.comb(k, p // 2) * a**p * b**q if q % 2 and not p % 2 else Fraction(0)
    return Fraction(0), zz, xx


def log_G(k: int, A: list[int], slopes: list[float], Q1: float, B: float) -> float:
    K = A[k + 1] + B  # A list index j-1; proof uses A_{k+2}.
    t = slopes[k]
    return (
        math.log1p(2 * K)
        + math.log(K + (1 + t) * K * K / 2)
        + 2 * K * t
        + math.log1p(K)
        + math.log(2 * t + Q1 * (2 * K + 1))
    )


def construct_bounds(kind: str, count: int = 24):
    if kind == "superexponential":
        slopes = [float(j) for j in range(1, count + 4)]
        lam1, M = 1.0, 1.0
    else:
        slopes = [1.0 - 2.0**(-j) for j in range(1, count + 4)]
        lam1, M = 0.5, 1.0
    B = 1.0
    Q1 = 8 * M
    H2, H3 = 2 * lam1 + 10 * M, 6 * lam1 + 190 * M
    D = 2 * (2 + 4 * H2 + H3)
    eta0 = 1 / (4 * (1 + D))
    A = []
    for j, lam in enumerate(slopes, 1):
        if kind == "superexponential":
            threshold = math.ceil(4 * (j + 1) + 2 * math.sqrt(3 * math.log1p(j) + j + math.log(1 / eta0))) + 3
        else:
            # Proof: delta=2^-j; sqrt(a), 2log(1+a) each <=delta*a/4,
            # remaining logarithmic constant <12, for this choice.
            threshold = max(100, 16 * 4**j, 48 * 2**j)
        A.append(max(threshold, A[-1] if A else 1))
    log_cutoff_values = []
    for j, (threshold, lam) in enumerate(zip(A, slopes), 1):
        for a in [threshold, threshold + 1, 2 * threshold, 10 * threshold]:
            log_b = -(a * a) if kind == "superexponential" else -a + math.sqrt(a)
            log_eta = log_b + 2 * math.log1p(a) + 3 * math.log1p(lam) + lam * (a + B)
            assert log_eta <= math.log(eta0)
            deriv = -2 * a + lam + 2 / (1 + a) if kind == "superexponential" else -(1 - lam) + 1 / (2 * math.sqrt(a)) + 2 / (1 + a)
            assert deriv < 0
            log_cutoff_values.append(log_eta)
    loggs = [log_G(k, A, slopes, Q1, B) for k in range(count + 1)]
    logL = math.log(2) + loggs[0]
    c0 = math.log(B + 3)
    thresholds = []
    for k in range(1, count + 1):
        value = max(k + 2, math.log1p(A[k + 1]), loggs[k])
        if thresholds:
            value = max(value, thresholds[-1] + c0 + 3)
        thresholds.append(value)
        assert loggs[k] - logL - value <= -math.log(2) + 1e-12
        assert value >= math.log1p(A[k + 1])
    # Check that the derivative constants genuinely make the high-gap
    # normalized perturbation strictly smaller than 1/2.
    assert D * eta0 * eta0 + eta0 < 0.5
    return {
        "target": "R=infinity" if kind == "superexponential" else "critical R=1",
        "first_cutoffs": A[:8],
        "eta0": eta0,
        "H2": H2,
        "H3": H3,
        "log_sufficient_L": logL,
        "first_thresholds": thresholds[:8],
        "tested_cutoff_log_eta_max": max(log_cutoff_values),
        "all_sampled_cutoff_and_monotone_tail_bounds_pass": True,
        "low_gap_log_bound_pass": True,
        "high_gap_normalized_bound": D * eta0 * eta0 + eta0,
        "scope": "finite evaluations plus explicit analytic tail inequalities in PROOF.md; not an infinite empirical test",
    }


def log_variance_lower(a: float, logb: float, s: float) -> float:
    u = a * s
    # log(sinh(2u)-2u), without overflowing the large-u expression.
    if u > 20:
        log_difference = 2 * u - math.log(2) + math.log1p(-math.exp(-4 * u) - 4 * u * math.exp(-2 * u))
    else:
        log_difference = math.log(math.sinh(2 * u) - 2 * u)
    return 2 * logb + log_difference - math.log(2 * u * u)


def main():
    u, b = sp.symbols("u b", positive=True, real=True)
    H0 = sp.diag(sp.exp(u), sp.exp(-u))
    H1 = b * sp.sinh(u) / u * sp.Matrix([[0, 1], [1, 0]])
    H2 = b**2 * (sp.sinh(u) / u * sp.eye(2) + (u * sp.cosh(u) - sp.sinh(u)) / u**2 * sp.diag(1, -1))
    Q = sp.diag(sp.exp(-u / 2), sp.exp(u / 2))
    actual = Q * (H1 * H0.inv() * H1 - H2) * Q
    target = b**2 * (sp.sinh(2 * u) - 2 * u) / (2 * u**2) * sp.diag(1, -1)
    differences = [sp.simplify(sp.expand_trig(x.rewrite(sp.exp))) for x in actual - target]
    assert all(x == 0 for x in differences)
    alpha, beta = sp.symbols("alpha beta", real=True)
    f = sp.sinh(u) / u
    fp = sp.diff(f, u)
    Z, X = sp.diag(1, -1), sp.Matrix([[0, 1], [1, 0]])
    general_H1 = b * (beta * H0 * Z + alpha * f * X)
    general_H2 = b**2 * (
        beta**2 * H0 + alpha**2 * (f * sp.eye(2) + fp * Z)
        + 2 * alpha * beta * fp * X
    )
    general_actual = Q * (general_H1 * H0.inv() * general_H1 - general_H2) * Q
    general_target = b**2 * (
        alpha**2 * (sp.sinh(2 * u) - 2 * u) / (2 * u**2) * Z
        - 2 * alpha * beta * fp * X
    )
    assert all(sp.simplify(sp.expand_trig(x.rewrite(sp.exp))) == 0 for x in general_actual - general_target)
    count = 0
    for p in range(15):
        for q in range(15 - p):
            assert kernel_moment(p, q) == exponential_moment(p, q)
            count += 1
    sqrt_countermodel = [
        {"n": n, "s": 0.05, "log_variance_lower": log_variance_lower(n, -math.sqrt(n), 0.05)}
        for n in [100, 400, 1600, 6400, 25600]
    ]
    assert sqrt_countermodel[-1]["log_variance_lower"] > 2000
    critical = []
    for delta in [0.2, 0.1, 0.05, 0.025, 0.0125]:
        n = math.ceil(1 / (4 * delta * delta))
        critical.append({"delta": delta, "n": n, "log_variance_lower": log_variance_lower(n, -n + math.sqrt(n), 1 - delta)})
    assert critical[-1]["log_variance_lower"] > critical[0]["log_variance_lower"] + 20
    report = {
        "status": "PASS",
        "symbolic_tilted_Schur_identity": True,
        "symbolic_arbitrary_tilt_Schur_identity": True,
        "sphere_kernel_exact_rational_moments": {"cases": count, "maximum_total_degree": 14, "pass": True},
        "all_exponential_example_bounds": construct_bounds("superexponential"),
        "critical_radius_example_bounds": construct_bounds("critical"),
        "incoming_sqrt_countermodel_log_lower_bounds": sqrt_countermodel,
        "critical_endpoint_variance_divergence_diagnostic": critical,
        "proof_scope": "Finite exact algebra and logarithmic arithmetic diagnostics. The infinite quantifiers and existence are established by the written analytic argument, not by these tests.",
    }
    Path(__file__).with_name("CHECKS.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
