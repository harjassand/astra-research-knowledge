#!/usr/bin/env python3
"""Reproduce finite checks for REPORT.md; Python standard library only.

These are exact rational identities and high-precision numerical checks, not
machine-checked proofs, novelty evidence, or physical measurements.
"""
from __future__ import annotations

from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from math import factorial, isqrt
from pathlib import Path
import json
import platform

getcontext().prec = 80
ONE = D(1)
TWO = D(2)
TOL = D("1e-65")


def tail(m: D, p: D) -> D:
    return (-m).exp() + p * m / (m - 1) * ((-ONE).exp() - (-m).exp())


def normalizer(m: D, p: D, a: D) -> D:
    """E exp(theta T), where a=M theta<1."""
    assert a < 1
    return (1 - p + p / (1 - a)) / (1 - a / m)


def backward_tail(m: D, p: D, a: D) -> D:
    """E[exp(-theta T) 1{T>M}], finite iff a>-1."""
    assert a > -1
    c = m / (m - 1)
    return (p * c * (-(1 + a)).exp() / (1 + a)
            + (1 - p * c) * (-m - a).exp() / (1 + a / m))


def relative_second_moment(m: D, p: D, a: D) -> D:
    return normalizer(m, p, a) * backward_tail(m, p, a) / tail(m, p) ** 2


def log_r_derivative(m: D, p: D, a: D) -> D:
    c = m / (m - 1)
    b = 1 - a
    u = p * c * (-(1 + a)).exp() / (1 + a)
    v = (1 - p * c) * (-m - a).exp() / (1 + a / m)
    log_z_prime = 1 / (m - a) + p / (b * ((1 - p) * b + p))
    log_b_prime = (u * (-1 - 1 / (1 + a))
                   + v * (-1 - 1 / (m + a))) / (u + v)
    return log_z_prime + log_b_prime


def optimal_scalar_tilt(m: D, p: D) -> D:
    # log R is strictly convex: both factors are log moment-generating
    # functions of nondegenerate measures. Its derivative changes sign here.
    lo, hi = -1 + D("1e-30"), 1 - D("1e-30")
    assert log_r_derivative(m, p, lo) < 0
    assert log_r_derivative(m, p, hi) > 0
    for _ in range(230):
        mid = (lo + hi) / 2
        if log_r_derivative(m, p, mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def bernoulli_kl(p: D, q: D) -> D:
    return p * (p / q).ln() + (1 - p) * ((1 - p) / (1 - q)).ln()


def poisson_kl(x: D, y: D) -> D:
    return x * (x / y).ln() - x + y


def adaptive_tree_check(p: D, q: D, rule) -> dict:
    leaves = []

    def visit(bits, pp, qq):
        if len(bits) == 8 or (bits and rule(bits)):
            leaves.append((bits, pp, qq))
            return
        visit(bits + (0,), pp * (1 - p), qq * (1 - q))
        visit(bits + (1,), pp * p, qq * q)

    visit((), ONE, ONE)
    assert abs(sum(x[1] for x in leaves) - 1) < TOL
    assert abs(sum(x[2] for x in leaves) - 1) < TOL
    kl_transcript = sum(pp * (pp / qq).ln() for _, pp, qq in leaves)
    expected_n = sum(D(len(bits)) * pp for bits, pp, _ in leaves)
    residual = abs(kl_transcript - expected_n * bernoulli_kl(p, q))
    assert residual < TOL
    return {"leaves": len(leaves), "expected_departures": str(expected_n),
            "kl_identity_residual": str(residual)}


def positive_uniformization(m: int, p: D) -> tuple[D, D, int]:
    """Positive Poisson-series action of exp(M Q) on the survival vector.

    Q=[[-1,p],[0,-1/M]], uniformization rate 1. The returned tail bound
    bounds analytic truncation; Decimal rounding is not interval-certified.
    """
    md = D(m)
    kmax = m + 25 * (isqrt(m) + 1) + 200
    poisson = (-md).exp()
    state_s, state_r = ONE, D(0)
    result = poisson
    for k in range(1, kmax + 1):
        poisson *= md / k
        state_s, state_r = D(0), state_s * p + state_r * (1 - 1 / md)
        result += poisson * (state_s + state_r)
    first_omitted = poisson * md / (kmax + 1)
    remainder_bound = first_omitted / (1 - md / (kmax + 2))
    return result, remainder_bound, kmax


def main() -> None:
    rational_checks = 0
    for m in (2, 3, 5, 10, 50):
        for p in (F(0), F(1, 8), F(1, 3), F(1, m ** 3)):
            ms, mr = F(1), F(1)
            for k in range(1, 7):
                ms, mr = k * (ms + p * m * mr), k * m * mr
                formula = factorial(k) * (1 + p * sum(m ** j for j in range(1, k + 1)))
                assert ms == formula
                rational_checks += 1
            # E[(JY-pMX)^2] for the specified common-X coupling.
            coupling = 2 * p * m ** 2 - 2 * p ** 2 * m ** 2 + 2 * p ** 2 * m ** 2
            assert coupling == 2 * p * m ** 2
            rational_checks += 1
    assert sum(F(7 ** k, factorial(k)) for k in range(11)) > 897
    rational_checks += 1

    numerical_rows = []
    pointwise_checks = 0
    for mi in (5, 8, 10, 30, 100, 300, 1000, 3000, 10000):
        m = D(mi)
        p = m ** -3
        q = tail(m, p)
        a = optimal_scalar_tilt(m, p)
        lower = (1 - p) * backward_tail(m, p, ONE) / q ** 2
        optimum = relative_second_moment(m, p, a)
        candidate = relative_second_moment(m, p, 1 - p.sqrt())
        assert lower <= optimum <= candidate * (1 + D("1e-60"))
        assert abs(log_r_derivative(m, p, a)) < D("1e-50")
        for aa in map(D, ("-10", "-2", "-1", "-.5", "0", ".5", ".9", ".99", ".999999")):
            for z in map(D, ("1", "1.1", "2", "5", "20")):
                ratio = (aa * z).exp() / normalizer(m, p, aa)
                envelope = z.exp() / (1 - p)
                assert ratio <= envelope
                pointwise_checks += 1
        for z in map(D, ("1", "2", "5", "20")):
            aa = (D(0), D(".5"), 1 - p.sqrt())
            weights = (D(".2"), D(".3"), D(".5"))
            ratio = sum(w * (aai * z).exp() / normalizer(m, p, aai)
                        for w, aai in zip(weights, aa))
            assert ratio <= z.exp() / (1 - p)
            pointwise_checks += 1
        kl = bernoulli_kl(p, 2 * p)
        delta = D(".05")
        binary_decision_kl = bernoulli_kl(1 - delta, delta)
        convolution_tail = (m * (-ONE).exp() - (-m).exp()) / (m - 1)
        branch_r = (2 * (1 - p) ** 2 * (-m).exp()
                    + 2 * p ** 2 * convolution_tail) / q ** 2
        numerical_rows.append({
            "M": mi, "p": str(p), "true_tail": str(q),
            "pgt_tail_divided_by_true_tail": str((-m / (1 + p * m)).exp() / q),
            "squared_clock_certificate": str(2 * p * m ** 2),
            "optimal_a_Mtheta": str(a),
            "p_times_optimal_scalar_relative_second_moment": str(p * optimum),
            "p_times_all_mixtures_lower_bound": str(p * lower),
            "p_times_constructive_scalar_relative_second_moment": str(p * candidate),
            "p_times_crude_relative_second_moment": str(p / q),
            "branch_stratified_relative_second_moment": str(branch_r),
            "native_decision_expected_N_lower_bound_delta_005": str(binary_decision_kl / kl),
            "p_times_native_decision_expected_N_lower_bound_delta_005": str(p * binary_decision_kl / kl),
        })

    uniformization_checks = []
    for mi in (2, 5, 10, 30, 100):
        m, p = D(mi), D(mi) ** -3
        actual, remainder, kmax = positive_uniformization(mi, p)
        residual = abs(actual - tail(m, p))
        assert residual <= remainder + D("1e-70")
        uniformization_checks.append({"M": mi, "terms": kmax + 1,
                                      "residual": str(residual),
                                      "analytic_truncation_bound": str(remainder)})

    adaptive_checks = []
    rules = (lambda b: sum(b) >= 1,
             lambda b: sum(b) >= 2,
             lambda b: len(b) >= 3 and b[-2:] == (0, 1),
             lambda b: len(b) >= 3 and (sum(b) == 0 or sum(b) >= 2))
    for p in (D(1) / 8, D(1) / 100, D(1) / 1000):
        for rule in rules:
            adaptive_checks.append(adaptive_tree_check(p, 2 * p, rule))

    dose_checks = 0
    for p in (D(1) / 4, D(1) / 100, D(1) / 1000000):
        for eta in (D(1) / 16, D(1) / 4, ONE):
            q = (1 + eta) * p
            d_rare = poisson_kl(p, q)
            d_safe = poisson_kl(1 - p, 1 - q)
            assert abs(d_rare + d_safe - bernoulli_kl(p, q)) < TOL
            assert d_rare <= p * eta ** 2 / 2
            assert d_safe <= p ** 2 * eta ** 2
            dose_checks += 3

    results = {
        "scope": "Exact rational identities and 80-digit numerical checks; not formal proof, physical validation, or novelty clearance.",
        "python": platform.python_version(), "decimal_precision": getcontext().prec,
        "rational_identity_checks": rational_checks,
        "pointwise_esscher_envelope_checks": pointwise_checks,
        "adaptive_stopping_KL_checks": len(adaptive_checks),
        "controlled_dose_checks": dose_checks,
        "positive_uniformization_checks": uniformization_checks,
        "scalar_tilt_and_acquisition_table": numerical_rows,
        "adaptive_stopping_details": adaptive_checks,
        "status": "PASS",
    }
    destination = Path(__file__).with_name("RESULTS.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(f"PASS: {rational_checks} exact rational identities; {pointwise_checks} tilt-envelope checks; "
          f"{len(adaptive_checks)} adaptive KL identities; {dose_checks} dose checks; "
          f"{len(uniformization_checks)} positive-semigroup comparisons.")
    print("M       p R_opt          p R_mix_lower    p N_lower (delta=.05)")
    for row in numerical_rows:
        print(f"{row['M']:5d}   {D(row['p_times_optimal_scalar_relative_second_moment']):.10f}    "
              f"{D(row['p_times_all_mixtures_lower_bound']):.10f}    "
              f"{D(row['p_times_native_decision_expected_N_lower_bound_delta_005']):.10f}")


if __name__ == "__main__":
    main()
