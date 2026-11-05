#!/usr/bin/env python3
"""Deterministic execution of the direct compliance-decision formulas.

This is a calculation of the declared two-state model, not a material experiment.
It verifies the transfer-function contrasts, exact Gaussian risk, polynomial
initial-state annihilation, and the slow-rate scaling of two complete tests.
"""
from pathlib import Path
import json
import math
import warnings

import numpy as np
from numpy.polynomial import Polynomial
from scipy.integrate import quad, IntegrationWarning
from scipy.optimize import brentq
from scipy.stats import norm

MU = 1.0
B = 1.0
F = 1.0
NU = 1.0
K = MU + B
ALPHA = 0.05
Z = norm.ppf(1 - ALPHA)
TARGET_INFO = 4 * Z * Z
PHI = Polynomial([0, 0, 0, 0, 256, -1024, 1536, -1024, 256])
DERIV = {j: PHI.deriv(j) for j in range(1, 5)}


def roots(lam):
    disc = math.sqrt((K + lam) ** 2 - 4 * MU * lam)
    rp = (K + lam + disc) / 2
    rm = MU * lam / rp
    return rm, rp


def step(lam, t):
    if lam == 0:
        return -math.expm1(-K * t) / K
    rm, rp = roots(lam)
    cm = (1 - rp / MU) / (rp - rm)
    cp = (rm / MU - 1) / (rp - rm)
    # These equivalent expm1 expressions avoid cancelling the t=0 constants.
    return cm * math.expm1(-rm * t) + cp * math.expm1(-rp * t)


def contrast(lam, t):
    return step(lam, t) - step(0, t)


def info_step(lam, horizon):
    # Integrate on the unit interval and retain the short initial boundary.
    pts = sorted(set([0.0, min(1.0, 1 / (K * horizon)),
                      min(1.0, 10 / (K * horizon)), 1.0]))
    val = sum(quad(lambda u: contrast(lam, horizon * u) ** 2,
                   a, b, epsabs=1e-15, epsrel=2e-10)[0]
              for a, b in zip(pts[:-1], pts[1:]))
    return F * F * horizon * val / NU


def q_poly(lam, horizon):
    eta = 1 / (K * horizon)
    rho_h = MU * lam * horizon / K
    return (eta ** 2 * DERIV[4]
            - (2 + lam / K) * eta * DERIV[3]
            + (1 + (K + MU) * lam / (K * K)) * DERIV[2]
            - rho_h * DERIV[1])


def q_norm2(lam, horizon):
    q = q_poly(lam, horizon)
    # A low-degree Gauss-Legendre quadrature is exact in exact arithmetic and
    # avoids the large cancellation in antiderivatives of squared polynomials.
    x, wt = np.polynomial.legendre.leggauss(16)
    return float(np.sum(wt * q((x + 1) / 2) ** 2) / 2)


def info_poly(lam, horizon):
    signal = 2 * lam * B * F * horizon ** 2 / K ** 2
    variance = NU * horizon * q_norm2(lam, horizon)
    return signal * signal / variance


def solve_horizon(fun, lam):
    low, high = 1e-4, 1.0
    while fun(lam, high) < TARGET_INFO:
        high *= 2
    return brentq(lambda h: fun(lam, h) - TARGET_INFO,
                  low, high, xtol=1e-8, rtol=2e-12)


def weighted_integral(lam, horizon, fun):
    q = q_poly(lam, horizon)
    pts = sorted(set([0.0, min(horizon, 1 / K), min(horizon, 10 / K),
                      horizon / 2, horizon]))
    return sum(quad(lambda t: q(t / horizon) * fun(t), a, b,
                    epsabs=2e-9, epsrel=1e-10)[0]
               for a, b in zip(pts[:-1], pts[1:]))


def main():
    records = []
    j2 = 1572864 / 5005
    for lam in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]:
        h0 = solve_horizon(info_step, lam)
        hn = solve_horizon(info_poly, lam)
        ha0 = (12 * NU * K ** 4 * Z ** 2 / (F ** 2 * B ** 2 * lam ** 2)) ** (1 / 3)
        han = (NU * K ** 4 * j2 * Z ** 2 / (F ** 2 * B ** 2 * lam ** 2)) ** (1 / 3)
        rm, rp = roots(lam)
        records.append({
            "lambda": lam,
            "slow_relaxation_time": 1 / rm,
            "known_state_optimal_horizon": h0,
            "known_state_risk": norm.cdf(-math.sqrt(info_step(lam, h0)) / 2),
            "known_state_asymptotic_horizon": ha0,
            "known_state_asymptotic_ratio": h0 / ha0,
            "unknown_state_polynomial_horizon": hn,
            "unknown_state_risk": norm.cdf(-math.sqrt(info_poly(lam, hn)) / 2),
            "unknown_state_asymptotic_horizon": han,
            "unknown_state_asymptotic_ratio": hn / han,
            "decision_to_relaxation_ratio": h0 * rm,
        })

    # Finite check of the exact nuisance annihilation and the forcing identity.
    lam, horizon = 0.001, 200.0
    rm, rp = roots(lam)
    nuisance = {
        "constant": weighted_integral(lam, horizon, lambda t: 1.0),
        "frozen_fast_mode": weighted_integral(lam, horizon, lambda t: math.exp(-K*t)),
        "relaxing_slow_mode": weighted_integral(lam, horizon, lambda t: math.exp(-rm*t)),
        "relaxing_fast_mode": weighted_integral(lam, horizon, lambda t: math.exp(-rp*t)),
    }

    def forced_contrast(t):
        out = F * contrast(lam, t)
        if t >= horizon / 2:
            out -= 2 * F * contrast(lam, t - horizon / 2)
        return out

    measured_signal = weighted_integral(lam, horizon, forced_contrast)
    expected_signal = -2 * lam * B * F * horizon ** 2 / K ** 2
    relative_signal_error = abs(measured_signal - expected_signal) / abs(expected_signal)
    assert max(abs(v) for v in nuisance.values()) < 1e-6
    assert relative_signal_error < 1e-8
    assert all(abs(r["known_state_risk"] - ALPHA) < 1e-9 for r in records)
    assert all(abs(r["unknown_state_risk"] - ALPHA) < 1e-9 for r in records)
    # A direct numerical check of the nonnegative contrast on a logarithmic grid.
    contrast_min = min(contrast(l, t) for l in [0.001, 0.1, 1.0]
                       for t in np.geomspace(0.01, 1e4, 250))
    assert contrast_min > -1e-12

    result = {
        "scope": "Deterministic evaluation of known two-state equations; no material experiment or Monte Carlo evidence.",
        "parameters": {"mu": MU, "B": B, "F": F, "nu": NU, "alpha": ALPHA},
        "required_information": float(TARGET_INFO),
        "polynomial_second_derivative_norm_squared": j2,
        "unknown_to_known_asymptotic_time_factor": (j2 / 12) ** (1 / 3),
        "scaling_records": records,
        "finite_identity_check": {
            "lambda": lam, "horizon": horizon,
            "nuisance_weighted_integrals": nuisance,
            "forcing_signal_computed": measured_signal,
            "forcing_signal_exact": expected_signal,
            "relative_signal_error": relative_signal_error,
        },
        "minimum_sampled_contrast": contrast_min,
        "limitations": [
            "Exact known-model formulas and declared Gaussian readout are premises.",
            "No physical preparation, ADC, actuator or calibration apparatus was executed.",
            "The polynomial receiver has a matching asymptotic rate, not a proved optimal unknown-state constant.",
            "White-noise idealization excludes intrinsic colored thermal process noise.",
        ],
    }
    dest = Path(__file__).with_name("execution.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"written": str(dest), "records": len(records),
                      "max_nuisance_residual": max(abs(v) for v in nuisance.values()),
                      "signal_relative_error": relative_signal_error,
                      "last_record": records[-1]}, indent=2))


if __name__ == "__main__":
    main()
