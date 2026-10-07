#!/usr/bin/env python3
"""Exploratory 1D quadrature for the displayed stopped-diffusion bounds.

Requires mpmath. Results are decimal estimates, not interval certificates.
No diffusion or quantum state is simulated.
"""
import json
from pathlib import Path

import mpmath as mp


def one_case(M="0.1", B="0.2", N=50_000, theta="0.99", epsilon="0.1"):
    mp.mp.dps = 30
    M, B, theta, epsilon = map(mp.mpf, (M, B, theta, epsilon))
    Nmp = mp.mpf(N)
    L, T, lam = 2 * M + 1, 3 * (2 * M + 1), M + 1
    delta = mp.mpf("0.5") - mp.log(mp.cosh(1))
    c = delta / 16
    xstar = 2 / (L + 2 + mp.sqrt(L * L + 4 * L))
    r0 = mp.sqrt(theta * xstar)
    a0 = 2 * mp.atanh(r0 / 2)
    lbase = mp.mpf(7) / 3 * mp.exp(-lam / 2 - mp.mpf(1) / 12)
    c0 = 2 * mp.exp(a0 / 2) / lbase
    ca = T * r0 / 2 + 3 * T * r0 / 4 + B / 2
    beta = T * r0 / (2 * mp.sqrt(Nmp)) + 3 * T * r0 / (4 * Nmp ** mp.mpf("1.5")) + B / (2 * Nmp ** mp.mpf("0.75"))
    c_n = T / (2 * mp.sqrt(Nmp)) + 3 * L * ca**2 / mp.sqrt(Nmp) + B * ca / Nmp ** mp.mpf("0.25")
    alpha = (3 * L - lam) / 16

    seed_integrand = lambda x: x * x * mp.exp(-c * x**4 + alpha * x**2 + B * x / 2)
    seed_integral = mp.quad(seed_integrand, [0, 2, 4, 6, 10, 20, 40])
    alpha_z = 1 / (6 * T)
    z_integrand = lambda z: (2 * alpha_z * z + B) * mp.exp(alpha_z * z**2 + B * z - z**2 / (3 * T))
    c_z = 1 + 6 * mp.quad(z_integrand, [0, 1, 2, 4, 8, 16, 32])
    c2 = mp.exp(c_n) * c_z * (1 + c0 * seed_integral)

    # Cauchy-Schwarz cutoffs: each discarded weighted mass is <= epsilon/16.
    zstar = mp.sqrt(3 * T * mp.log(1536 * c2 / epsilon**2))
    target_seed_probability = epsilon**2 / (256 * c2)
    seed_tail = lambda x: c0 * mp.quad(
        lambda u: u * u * mp.exp(-c * u**4 - lam * u**2 / 16), [x, mp.inf]
    )
    lower, upper = mp.mpf(0), mp.mpf(1)
    while seed_tail(upper) > target_seed_probability:
        lower, upper = upper, 2 * upper
    for _ in range(90):
        middle = (lower + upper) / 2
        if seed_tail(middle) > target_seed_probability:
            lower = middle
        else:
            upper = middle
    xstar_tail = upper

    dstar = Nmp ** mp.mpf("0.25") * beta + zstar / mp.sqrt(Nmp)
    alpha_g = (L - lam) / 16
    beta_g = L * dstar / 4 + B / 4
    g_integral = mp.quad(
        lambda x: x * x * mp.exp(-c * x**4 + alpha_g * x**2 + beta_g * x),
        [0, 2, 4, 6, 10, 20, 40],
    )
    # Add 1 for the replacement atom and include the d-dependent constant.
    g0 = mp.exp(L * dstar**2 / 4 + B * dstar / 2 + T / (4 * mp.sqrt(Nmp)))
    g_bound = g0 * (1 + c0 * g_integral)

    return {
        "M": str(M), "B": str(B), "N": N, "theta": str(theta), "epsilon": str(epsilon),
        "mpmath_dps": mp.mp.dps,
        "C0": float(c0), "C_N": float(c_n), "C_Z_bound": float(c_z),
        "seed_integral_bound_estimate": float(seed_integral),
        "E_w2_bound_estimate": float(c2),
        "Z_cutoff_for_weighted_tail": float(zstar),
        "R_cutoff_for_weighted_tail": float(xstar_tail),
        "d_star": float(dstar), "g_normalizer_bound_estimate": float(g_bound),
        "proposal_cap_4G": float(4 * g_bound),
        "scope": "mpmath quadrature estimates of analytic upper-bound integrals only; not interval certified and no sampler executed.",
    }


def main():
    result = {
        "scope": "Exploratory numerical quadrature; not a certified bound or runtime.",
        "cases": [one_case()],
    }
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
