"""Finite scalar constants for the output-only classical calibration construction.

This is deterministic quadrature and evaluation of sufficient bounds.
It is not a hardware simulation, a sampled-data experiment, or a practical resource claim.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from scipy.integrate import quad
from scipy.optimize import brentq


def slope(b: int, q: float) -> float:
    """C_b(q), the positive first derivative after q-normalization."""
    if q == 0:
        return 2.0

    def integrand(u: float) -> float:
        if u <= 1:
            a = (-math.expm1(-q*u) - math.expm1(-q*(1-u))) / q
        else:
            a = math.exp(-q*(u-1)) * (-math.expm1(-q)) / q
        x = math.expm1(q*min(1.0, u)) / q
        z0 = max(1.0, u)
        z = math.exp(-q*z0) * (-math.expm1(-q*(2-z0))) / q
        return 2*a**(b-1)*x*z

    return sum(quad(integrand, left, right, epsabs=2e-13, epsrel=2e-13)[0]
               for left, right in [(0.0, 1.0), (1.0, 2.0)])


def even_power_minus_one(x: float, exponent: float) -> float:
    return (math.expm1(-exponent*math.log1p(-x))
            + math.expm1(-exponent*math.log1p(x))) / 2


def damping_rho(alpha: float, k: int, d: int) -> float:
    return max(2*d*b/slope(b, 1.0) *
               even_power_minus_one(alpha, b+1)
               for b in range(1, k+1))


def finite_time_rho(w: float, r: float, strength: float, k: int, d: int) -> float:
    a = max(1, k-1)
    x = 4*a*strength*w
    if x >= 1:
        return math.inf
    return max(4*d*b/slope(b, r*w) *
               even_power_minus_one(x, 1+b/a)
               for b in range(1, k+1))


def overlap(delta: float, r: float, time: float) -> float:
    """Stable global-pure overlap for the one-qubit lower-bound family."""
    s = math.sqrt(r*r-4*delta*delta)
    if s == 0:
        return math.exp(-r*time/2)*(1+r*time/2)
    gamma = (r-s)/2
    return math.exp(-gamma*time) * (
        (1+r/s)/2 - (r/s-1)*math.exp(-s*time)/2)


def run() -> dict:
    table = [{
        "weight": b,
        "C_at_q_1": slope(b, 1.0),
        "C_at_q_0_1": slope(b, 0.1),
        "finite_LO_variance_mu_kappa_q_1": 3.25**(b+1),
        "variance_over_slope_squared": 3.25**(b+1)/slope(b, 1.0)**2,
        "preferred_matched_LO_variance_kappa_q_1": 3.0**(b+1),
        "preferred_matched_variance_over_slope_squared": 3.0**(b+1)/slope(b, 1.0)**2,
    } for b in range(1, 7)]

    thresholds = []
    for k, degree in [(1, 3), (2, 1), (2, 12), (2, 15), (2, 21), (3, 30)]:
        alpha = brentq(lambda z: damping_rho(z, k, degree)-0.25,
                       1e-7, 0.49, xtol=1e-14)
        thresholds.append({
            "k": k, "candidate_degree": degree,
            "sufficient_r_over_J_for_w_1_over_r": 2/alpha,
            "alpha": alpha,
            "evaluated_sufficient_rho_not_interval_certified": damping_rho(alpha, k, degree),
        })

    all_rate = []
    k, degree, strength = 2, 12, 1.0
    c_star = max(b/slope(b, 1.0) for b in range(1, k+1))
    a_k = 64*max(1, k-1)*math.sqrt(c_star)
    for r in [0.01, 0.1, 1.0, 4.0, 100.0, 1000.0]:
        w = 1/(r+a_k*math.sqrt(degree)*strength)
        all_rate.append({
            "r_over_J": r/strength, "window_times_J": w*strength,
            "q_r_w": r*w, "rho_time": finite_time_rho(w, r, strength, k, degree),
            "min_diagonal_slope": min(w*slope(b, r*w) for b in range(1, k+1)),
            "variance_kappa_mu_1": (2/(r*w)+1.25)**(k+1),
        })

    lower = []
    for delta, r, time in [(0.1, 1.0, 10.0), (0.01, 1.0, 1000.0), (0.25, 1.0, 4.0)]:
        a = overlap(delta, r, time)
        lower.append({
            "delta": delta, "r": r, "time": time,
            "exact_overlap": a,
            "proven_overlap_lower": math.exp(-2*delta*delta*time/r),
            "binary_error_exact": (1-math.sqrt(max(0.0, 1-a*a)))/2,
            "binary_error_lower": math.exp(-4*delta*delta*time/r)/4,
        })
    return {
        "status": "Deterministic scalar evaluation only; not a source or hardware simulation.",
        "slopes_and_variances": table,
        "strong_noise_sufficient_thresholds": thresholds,
        "conservative_all_rate_windows_k2_d12": all_rate,
        "exact_passive_lower_bound_diagnostic": lower,
    }


if __name__ == "__main__":
    result = run()
    output = Path(__file__).with_name("response_constants.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(output)
    for row in result["strong_noise_sufficient_thresholds"]:
        print(row)
