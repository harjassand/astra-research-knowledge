#!/usr/bin/env python3
"""Reproduce retained-candidate and finite-RMS Stark-control obstructions.

Only standard-library arithmetic is used. No experiments or fitted molecular
parameters are represented. Output numbers are illustrative model values.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def acceptance(u: float, d: float, escape: float, n: int) -> float:
    discr = math.sqrt((u + d + escape) ** 2 - 4 * u * d)
    rp = (u + d + escape + discr) / (2 * u)
    rm = (u + d + escape - discr) / (2 * u)
    # Stable form of (rp-rm)/(rp**(n+1)-rm**(n+1)).
    return (1 - rm / rp) * math.exp(-n * math.log(rp)) / (
        1 - math.exp((n + 1) * math.log(rm / rp))
    )


def absorption_acceptance(u: float, d: float, escape: float, n: int) -> float:
    # Independent tridiagonal Dirichlet solve for h(i), i=0,...,n-1.
    diag = [u + d + escape] * n
    upper = [-u] * (n - 1)
    lower = [-d] * (n - 1)
    rhs = [0.0] * (n - 1) + [u]
    for i in range(1, n):
        factor = lower[i - 1] / diag[i - 1]
        diag[i] -= factor * upper[i - 1]
        rhs[i] -= factor * rhs[i - 1]
    sol = [0.0] * n
    sol[-1] = rhs[-1] / diag[-1]
    for i in range(n - 2, -1, -1):
        sol[i] = (rhs[i] - upper[i] * sol[i + 1]) / diag[i]
    return sol[0]


def bessel_j(n: int, z: float) -> float:
    # Convergent series for nonnegative integer n, adequate for tested z<=4.
    term = (z / 2) ** n / math.factorial(n)
    total = term
    for k in range(1, 160):
        term *= -(z * z / 4) / (k * (n + k))
        total += term
        if abs(term) < 2e-17:
            break
    return total


def sinusoid_rate(kappa: float, a_rms: float, omega: float) -> dict[str, float]:
    # q(t)=sqrt(2)*a_rms*cos(omega*t), u=exp[-iz*sin(omega*t)].
    # Floquet spectrum weight J_n(z)^2 at n*omega, z=sqrt(2)*a_rms/omega.
    z = math.sqrt(2) * a_rms / omega
    weights = [(0, bessel_j(0, z) ** 2)]
    for n in range(1, 80):
        w = bessel_j(n, z) ** 2
        weights.extend([(n, w), (-n, w)])
    mass = sum(w for _, w in weights)
    moment = sum(w * (n * omega) ** 2 for n, w in weights)
    normalized_rate = sum(
        w * kappa * kappa / (kappa * kappa + (n * omega) ** 2)
        for n, w in weights
    )
    lower = kappa * kappa / (kappa * kappa + a_rms * a_rms)
    assert abs(mass - 1) < 1e-12, (z, mass)
    assert abs(moment - a_rms * a_rms) < 1e-10, (z, moment)
    assert normalized_rate >= lower - 1e-12
    return {
        "omega": omega,
        "a_rms": a_rms,
        "spectrum_mass": mass,
        "spectrum_second_moment": moment,
        "sinusoidal_leakage_relative_to_no_control": normalized_rate,
        "static_optimum_and_proved_lower_bound": lower,
    }


def slope_field_for_suppression(suppression: float) -> float:
    lo, hi = 0.0, 2 * suppression
    for _ in range(100):
        mid = (lo + hi) / 2
        ratio = math.atan(mid) / mid
        if ratio > 1 / suppression:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main() -> None:
    retention = []
    for escape in (0.0, 0.01, 0.1, 1.0):
        for n in (4, 16, 64, 256):
            right = acceptance(2, 1, escape, n)
            wrong = acceptance(1, 2, escape, n)
            assert math.isclose(wrong / right, 2.0 ** -n, rel_tol=5e-13)
            if n <= 64:
                independent = absorption_acceptance(2, 1, escape, n)
                assert math.isclose(right, independent, rel_tol=1e-12)
            retention.append({
                "N": n,
                "escape_rate": escape,
                "right_acceptance_probability": right,
                "wrong_acceptance_probability": wrong,
                "equal_prior_product_error": wrong / (right + wrong),
            })
    moving_barrier = []
    for n in (16, 64, 256, 1024, 4096, 16384):
        moving_barrier.append({
            "N": n,
            "escape_rate": 1 / n,
            "right_yield": acceptance(2, 1, 1 / n, n),
            "limit": 0.5 * math.exp(-1),
        })
    stark = []
    for a in (0.2, 1, 2):
        for omega in (1, 2, 4, 16):
            stark.append(sinusoid_rate(1, a, omega))
    slopes = [
        {"suppression": s, "x_required_uniform_slopes": slope_field_for_suppression(s)}
        for s in (2, 10, 100, 1000)
    ]
    result = {
        "scope": "Exact model formulas plus independent linear solve/Floquet checks; no experiment or novelty certification.",
        "retention_obstruction": retention,
        "retention_mu_equal_one_over_N": moving_barrier,
        "finite_RMS_stark_control": stark,
        "near_immune_uniform_slope_continuum": slopes,
    }
    dest = Path(__file__).with_name("replay_results.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "output": str(dest),
        "retention_cases": len(retention),
        "stark_cases": len(stark),
        "all_checks": "passed",
        "slope_field_for_10x": slopes[1]["x_required_uniform_slopes"],
    }, indent=2))


if __name__ == "__main__":
    main()
