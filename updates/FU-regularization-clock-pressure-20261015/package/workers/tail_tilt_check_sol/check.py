#!/usr/bin/env python3
"""Deterministic high-precision checks for PROOF.md; no Monte Carlo claims.

Run: python3 check.py
Requires the existing host mpmath package. Writes RESULTS.json and NUMERICS.md
next to this script. The numerical assertions are independent diagnostics;
the analytic endpoint and uniform-family claims are proved in PROOF.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

mp.mp.dps = 90
OUT = Path(__file__).resolve().parent
COUNTS: dict[str, int] = {}


def counted(name: str) -> None:
    COUNTS[name] = COUNTS.get(name, 0) + 1


def close(x: mp.mpf, y: mp.mpf, name: str, tol: str = "1e-65") -> None:
    assert abs(x - y) <= mp.mpf(tol) * max(abs(x), abs(y), mp.mpf("1e-80")), (
        name,
        mp.nstr(x, 30),
        mp.nstr(y, 30),
    )
    counted(name)


def par(M: int | mp.mpf) -> dict[str, mp.mpf]:
    M = mp.mpf(M)
    p = M ** -3
    d = p * M / (M - 1)
    a = 1 - d
    u = a * mp.exp(-M)
    v = d / mp.e
    q = u + v
    eps = u / v
    alpha = mp.mpf(3) / 2 - 1 / (M - 1)
    beta = alpha**2 / 2 + mp.mpf(1) / 8 + 1 / (2 * (M - 1) ** 2)
    kappa = alpha - 1 + beta / alpha
    return locals()


def density(t: mp.mpf, z: dict[str, mp.mpf]) -> mp.mpf:
    """Original branch-convolution density, rather than compact coefficients."""
    M, p = z["M"], z["p"]
    return (1 - p) * mp.exp(-t) + p * (mp.exp(-t / M) - mp.exp(-t)) / (M - 1)


def K(s: mp.mpf, z: dict[str, mp.mpf]) -> mp.mpf:
    M, p = z["M"], z["p"]
    if s >= 1:
        return mp.inf
    return (1 - p + p / (1 - s)) / (1 - s / M)


def H(s: mp.mpf, z: dict[str, mp.mpf]) -> mp.mpf:
    if s <= -1:
        return mp.inf
    M = z["M"]
    return mp.exp(-s) * (z["u"] / (1 + s / M) + z["v"] / (1 + s))


def R(s: mp.mpf, z: dict[str, mp.mpf]) -> mp.mpf:
    if not -1 < s < 1:
        return mp.inf
    return K(s, z) * H(s, z) / z["q"] ** 2


def compact_R(s: mp.mpf, z: dict[str, mp.mpf]) -> mp.mpf:
    M, p, q = z["M"], z["p"], z["q"]
    eta = (M * z["u"] + z["v"]) / q
    return (
        mp.exp(-s)
        * M
        * (1 - (1 - p) * s)
        * (M + eta * s)
        / (q * (M**2 - s**2) * (1 - s**2))
    )


def delta_R(delta: mp.mpf, z: dict[str, mp.mpf]) -> mp.mpf:
    M, p, eps = z["M"], z["p"], z["eps"]
    r = M * (2 - delta) / (M + 1 - delta)
    return (
        mp.exp(delta)
        * (1 - p + p / delta)
        / ((2 - delta) * (1 + delta / (M - 1)))
        * (1 + eps * r)
        / (1 + eps) ** 2
        / p
    )


def log_delta_derivative(delta: mp.mpf, z: dict[str, mp.mpf]) -> mp.mpf:
    M, p, eps = z["M"], z["p"], z["eps"]
    r = M * (2 - delta) / (M + 1 - delta)
    return (
        1
        + 1 / (2 - delta)
        - 1 / (M - 1 + delta)
        - p / (delta * ((1 - p) * delta + p))
        - eps * M * (M - 1) / ((M + 1 - delta) ** 2 * (1 + eps * r))
    )


def optimum(z: dict[str, mp.mpf]) -> tuple[mp.mpf, mp.mpf]:
    lo, hi = mp.mpf(0), mp.mpf(1)
    assert log_delta_derivative(hi, z) > 0
    for _ in range(310):
        mid = (lo + hi) / 2
        if log_delta_derivative(mid, z) < 0:
            lo = mid
        else:
            hi = mid
    delta = (lo + hi) / 2
    return delta, delta_R(delta, z)


def scalar_lower(z: dict[str, mp.mpf]) -> mp.mpf:
    p, eps, alpha = z["p"], z["eps"], z["alpha"]
    return (mp.sqrt(1 - p) + mp.sqrt(alpha * p)) ** 2 / (2 * p * (1 + eps) ** 2)


def mixture_lower(z: dict[str, mp.mpf]) -> mp.mpf:
    return (1 - z["p"]) / (2 * z["p"] * (1 + z["eps"]) ** 2)


def n(x: mp.mpf, digits: int = 25) -> str:
    return mp.nstr(x, digits)


def check_integrals() -> None:
    for M0 in (2, 4, 12, 40):
        z = par(M0)
        M = z["M"]
        q_integral = mp.quad(lambda u: M * density(M * u, z), [1, 2, 4, 8, mp.inf])
        close(q_integral, z["q"], "tail_density_quadrature")
        for ss in ("-0.9", "-0.3", "0", "0.4", "0.93"):
            s = mp.mpf(ss)
            k_integral = mp.quad(
                lambda u: M * density(M * u, z) * mp.exp(s * u),
                [0, mp.mpf("0.05"), mp.mpf("0.2"), 1, 2, 4, 8, mp.inf],
            )
            h_integral = mp.quad(
                lambda u: M * density(M * u, z) * mp.exp(-s * u),
                [1, 2, 4, 8, mp.inf],
            )
            close(k_integral, K(s, z), "mgf_density_quadrature")
            close(h_integral, H(s, z), "weighted_tail_density_quadrature")
            close(R(s, z), compact_R(s, z), "compact_formula")
            close(R(s, z), delta_R(1 - s, z), "delta_formula")


def check_domain_and_grid() -> list[dict[str, str | int]]:
    rows = []
    for M in (2, 3, 4, 5, 8, 10, 20, 50, 100, 1000, 10000):
        z = par(M)
        p = z["p"]
        lb = scalar_lower(z)
        for j in range(-99, 100):
            s = mp.mpf(j) / 100
            value = R(s, z)
            assert value >= lb, (M, j, value, lb)
            counted("finite_scalar_lower_bound")
            if s < 0:
                assert value > 1 / z["q"]
                counted("negative_tilt_worse_than_zero")
        for delta in (mp.mpf("1e-12"), mp.sqrt(p), p, p**2):
            if delta < 1:
                assert delta_R(delta, z) >= lb
                counted("near_boundary_lower_bound")
        assert K(mp.mpf(1), z) == mp.inf
        assert H(mp.mpf(-1), z) == mp.inf
        assert H(mp.mpf("-1.01"), z) == mp.inf
        counted("analytic_endpoint_domain")
        delta, value = optimum(z)
        assert abs(log_delta_derivative(delta, z)) < mp.mpf("1e-55")
        counted("optimum_stationarity")
        for factor in (mp.mpf("0.99"), mp.mpf("1.01")):
            assert delta_R(delta * factor, z) > value
            counted("optimum_neighbor_comparison")
        # Independent differentiation of the unsimplified K(s)H(s) formula.
        direct_derivative = mp.diff(lambda s: mp.log(K(s, z) * H(s, z)), 1 - delta)
        assert abs(direct_derivative) < mp.mpf("1e-55")
        counted("direct_optimum_stationarity")
        rows.append(
            {
                "M": M,
                "p": n(p),
                "delta_star": n(delta),
                "theta_star": n((1 - delta) / z["M"]),
                "minimum_relative_second_moment": n(value),
                "two_p_times_minimum": n(2 * p * value),
                "epsilon": n(z["eps"]),
                "finite_scalar_lower_bound": n(lb),
                "finite_mixture_lower_bound": n(mixture_lower(z)),
                "tilted_branch_probability": n(p / (p + (1 - p) * delta)),
            }
        )
    assert mp.mpf(rows[2]["two_p_times_minimum"]) < 1  # M=4: finite-M correction matters.
    counted("uncorrected_finite_bound_counterexample")
    return rows


def check_asymptotics() -> list[dict[str, str | int]]:
    rows = []
    for M in (50, 100, 300, 1000, 10000, 100000):
        z = par(M)
        p, alpha, beta, kappa = z["p"], z["alpha"], z["beta"], z["kappa"]
        delta, value = optimum(z)
        delta_approx = mp.sqrt(p / alpha) - beta * p / alpha**2
        value_approx = 1 / (2 * p) + mp.sqrt(alpha / p) + kappa / 2
        delta_scaled_remainder = (delta - delta_approx) / p ** mp.mpf("1.5")
        value_scaled_remainder = (value - value_approx) / mp.sqrt(p)
        assert abs(delta_scaled_remainder) < 10
        assert abs(value_scaled_remainder) < 10
        counted("third_order_optimum_expansion")
        counted("third_order_minimum_expansion")
        rows.append(
            {
                "M": M,
                "delta_over_sqrt_p": n(delta / mp.sqrt(p)),
                "expected_delta_coefficient": n(1 / mp.sqrt(alpha)),
                "delta_remainder_over_p_3_over_2": n(delta_scaled_remainder),
                "minimum_remainder_over_sqrt_p": n(value_scaled_remainder),
                "minimum_minus_first_two_terms": n(value - 1 / (2 * p) - mp.sqrt(alpha / p)),
                "expected_constant_kappa_over_two": n(kappa / 2),
            }
        )
    return rows


def check_mixtures() -> list[dict[str, str | int]]:
    for M0 in (2, 4, 10, 50, 1000):
        z = par(M0)
        for ss in ("-100", "-3", "-1", "-0.5", "0", "0.7", "0.99", "0.999999"):
            s = mp.mpf(ss)
            for uu in ("1", "1.01", "2", "5", "20", "100"):
                u = mp.mpf(uu)
                envelope_ratio = (
                    mp.exp((s - 1) * u) * (1 - z["p"])
                    / ((1 - 1 / z["M"]) * K(s, z))
                )
                assert envelope_ratio <= 1
                counted("all_scalar_parameters_pointwise_envelope")
    rows = []
    components = [(mp.mpf("-3"), mp.mpf("0.2")), (mp.mpf("0.2"), mp.mpf("0.3")), (mp.mpf("0.98"), mp.mpf("0.5"))]
    for M0 in (2, 10, 50):
        z = par(M0)
        M = z["M"]

        def g(u: mp.mpf) -> mp.mpf:
            return sum(w * mp.exp(s * u) / K(s, z) for s, w in components)

        second = mp.quad(
            lambda u: M * density(M * u, z) / g(u), [1, 2, 4, 8, mp.inf]
        )
        value = second / z["q"] ** 2
        assert value >= mixture_lower(z)
        counted("marginal_mixture_second_moment_quadrature")
        rows.append(
            {
                "M": M0,
                "s_components": "-3, 0.2, 0.98",
                "weights": "0.2, 0.3, 0.5",
                "negative_component_alone_has_infinite_second_moment": True,
                "marginal_mixture_relative_second_moment": n(value),
                "mixture_lower_bound": n(mixture_lower(z)),
            }
        )
    return rows


def check_decomposition_and_branch_sampler() -> list[dict[str, str | int]]:
    rows = []
    for M0 in (2, 4, 10, 50, 1000):
        z = par(M0)
        M, p, q = z["M"], z["p"], z["q"]
        a0 = mp.exp(-M)
        a1 = (M / mp.e - mp.exp(-M)) / (M - 1)
        close((1 - p) * a0 + p * a1, q, "branch_tail_decomposition")
        for ss in ("-0.7", "0", "0.5", "0.95"):
            s = mp.mpf(ss)
            k0 = 1 / (1 - s / M)
            k1 = k0 / (1 - s)
            h0 = mp.exp(-M - s) / (1 + s / M)
            h1 = (
                M * mp.exp(-1 - s) / (1 + s)
                - mp.exp(-M - s) / (1 + s / M)
            ) / (M - 1)
            r0, r1 = (1 - p) * k0 / K(s, z), p * k1 / K(s, z)
            w0, w1 = (1 - p) * a0 / q, p * a1 / q
            rho0, rho1 = k0 * h0 / a0**2, k1 * h1 / a1**2
            assert rho0 >= 1 and rho1 >= 1
            close(w0**2 * rho0 / r0 + w1**2 * rho1 / r1, R(s, z), "general_mixture_decomposition")
        r = mp.mpf("0.5")
        branch_second = (1 - p) ** 2 * a0 / (1 - r) + p**2 * a1 / r
        allocation_denom = (1 - p) * mp.sqrt(a0) + p * mp.sqrt(a1)
        optimal_r = p * mp.sqrt(a1) / allocation_denom
        optimal_r0 = (1 - p) * mp.sqrt(a0) / allocation_denom
        optimal_second = (1 - p) ** 2 * a0 / optimal_r0 + p**2 * a1 / optimal_r
        close(
            optimal_second,
            ((1 - p) * mp.sqrt(a0) + p * mp.sqrt(a1)) ** 2,
            "optimal_branch_allocation",
            "1e-60",
        )
        corrected_var = p**2 * a1 * (1 - a1) / q**2
        rows.append(
            {
                "M": M0,
                "fixed_half_branch_relative_second_moment": n(branch_second / q**2),
                "target_two_e": n(2 * mp.e),
                "optimal_branch_relative_second_moment": n(optimal_second / q**2),
                "target_e": n(mp.e),
                "analytic_fast_plus_rare_branch_relative_variance": n(corrected_var),
                "target_e_minus_one": n(mp.e - 1),
                "omitted_fast_branch_bias": n(-(1 - p) * a0),
            }
        )
    return rows


def generic_value(M0: int, c: mp.mpf, k: int, base: str) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    M, p = mp.mpf(M0), mp.mpf(M0) ** -k
    delta, s = mp.sqrt(p), 1 - mp.sqrt(p)
    if base.startswith("constant"):
        x0 = mp.mpf(base.split(":")[1])
        assert x0 < c * M
        q = p * mp.exp(-c + x0 / M)
        km = mp.exp(s * x0 / M) * (1 - p + p / delta)
        hm = p * mp.exp(-c * (1 + s) + x0 / M) / (1 + s)
    elif base == "exponential_mean_2":
        b = mp.mpf(2)
        u = (1 - p * M / (M - b)) * mp.exp(-c * M / b)
        v = p * M / (M - b) * mp.exp(-c)
        q = u + v
        km = (1 - p + p / delta) / (1 - b * s / M)
        hm = mp.exp(-c * s) * (u / (1 + b * s / M) + v / (1 + s))
    else:
        raise ValueError(base)
    return q, km * hm / q**2, p


def check_generic_family() -> list[dict[str, str | int]]:
    rows = []
    for base in ("constant:0", "constant:7", "exponential_mean_2"):
        for cc in ("0.3", "1", "3"):
            c = mp.mpf(cc)
            for k in (1, 3):
                errors = []
                for M0 in (1000, 10000, 100000):
                    q, value, p = generic_value(M0, c, k, base)
                    ratio = 2 * p * value
                    errors.append(abs(ratio - 1))
                    assert ratio > 1
                    counted("generic_light_base_rare_scale_example")
                    rows.append(
                        {
                            "base": base,
                            "c": cc,
                            "k": k,
                            "M": M0,
                            "q_over_p_exp_minus_c": n(q / (p * mp.exp(-c))),
                            "two_p_times_upper_construction_R": n(ratio),
                        }
                    )
                assert errors[0] > errors[1] > errors[2]
                assert errors[2] < mp.mpf("0.05")
                counted("generic_asymptotic_convergence_sequence")
    return rows


def main() -> None:
    check_integrals()
    optimal_rows = check_domain_and_grid()
    asymptotic_rows = check_asymptotics()
    mixture_rows = check_mixtures()
    branch_rows = check_decomposition_and_branch_sampler()
    generic_rows = check_generic_family()
    result = {
        "status": "PASS",
        "scope": "Deterministic numerical diagnostics; mathematical proof is in PROOF.md.",
        "mpmath_version": mp.__version__,
        "decimal_precision": mp.mp.dps,
        "counts": COUNTS,
        "total_assertion_groups": sum(COUNTS.values()),
        "finite_optima": optimal_rows,
        "sharp_asymptotic_expansion": asymptotic_rows,
        "scalar_esscher_mixtures": mixture_rows,
        "branch_sampler": branch_rows,
        "generic_family": generic_rows,
    }
    (OUT / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = [
        "# Deterministic numerical diagnostics",
        "",
        f"Status: PASS. Precision: {mp.mp.dps} decimal digits; mpmath {mp.__version__}.",
        f"Counted checks: {sum(COUNTS.values())}. These are numerical diagnostics, not independent proof certificates.",
        "",
        "The optimizer includes both branches and the exact finite-M correction.",
        "",
        "| M | 1-M theta_star | minimum R | 2p minimum R | finite scalar lower bound |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in optimal_rows:
        lines.append(
            f"| {row['M']} | {row['delta_star']} | {row['minimum_relative_second_moment']} "
            f"| {row['two_p_times_minimum']} | {row['finite_scalar_lower_bound']} |"
        )
    lines += [
        "",
        "At M=4 the minimum is below 1/(2p), confirming why the finite correction cannot be omitted.",
        "",
        "| M | residual minimum after first two terms | predicted constant kappa/2 | residual error / sqrt(p) |",
        "|---:|---:|---:|---:|",
    ]
    for row in asymptotic_rows:
        lines.append(
            f"| {row['M']} | {row['minimum_minus_first_two_terms']} "
            f"| {row['expected_constant_kappa_over_two']} | {row['minimum_remainder_over_sqrt_p']} |"
        )
    lines += [
        "",
        "The marginal mixture check uses scaled tilts s=(-3,0.2,0.98) with weights (0.2,0.3,0.5).",
        "The s=-3 component alone has infinite second moment. The full mixture is integrated directly.",
        "",
        "| M | marginal mixture R | proven mixture lower bound |",
        "|---:|---:|---:|",
    ]
    for row in mixture_rows:
        lines.append(
            f"| {row['M']} | {row['marginal_mixture_relative_second_moment']} | {row['mixture_lower_bound']} |"
        )
    lines += [
        "",
        "Full branch allocation and generic-family tables are saved in RESULTS.json.",
        "The generic tests cover X=0, X=7, and exponential X of mean 2; thresholds cM with c=0.3,1,3;",
        "and branch probabilities p=M^{-1},M^{-3}.",
        "",
        "Replay: python3 check.py",
        "",
    ]
    (OUT / "NUMERICS.md").write_text("\n".join(lines))
    print(json.dumps({"status": "PASS", "total_checks": sum(COUNTS.values()), "counts": COUNTS}, indent=2))


if __name__ == "__main__":
    main()
