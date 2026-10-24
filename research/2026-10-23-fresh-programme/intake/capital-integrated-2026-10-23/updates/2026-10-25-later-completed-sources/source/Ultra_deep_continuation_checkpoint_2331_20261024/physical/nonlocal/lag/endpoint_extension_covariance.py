#!/usr/bin/env python3
"""Quantum equilibrium endpoint-extension variances for two counted cells.

Uses only NumPy and the standard library. Units set hbar=k_B=1 and theta=1.
The finite Matsubara sum is a lower estimate; a mass-matrix inequality gives
an explicit upper bound on its omitted positive-frequency tail. q integration
uses Gauss-Legendre quadrature, with a separate grid-convergence replay.
"""
import json
import math
from pathlib import Path

import numpy as np

THETA = 1.0
TAU = 1.0 / math.sqrt(101.0)
K = 1.0
M_TOTAL = 1.0
FEJER_M = 100.0 / 101.0
FEJER_K = np.array([0.15, 0.10, 0.05], dtype=float)
PENDANT_MB = 0.001
PENDANT_ELL_OVER_A = 0.4
PENDANT_K = 0.4
PENDANT_MROD = PENDANT_K * (PENDANT_ELL_OVER_A * TAU) ** 2
PENDANT_MS = M_TOTAL - PENDANT_MB - TAU**2 - PENDANT_MROD


def q_rule(nq):
    z, w = np.polynomial.legendre.leggauss(nq)
    q = (z + 1.0) * (math.pi / 2.0)
    # Average over the full reciprocal interval is (1/pi) integral_0^pi.
    wavg = w * 0.5
    return q, wavg


def sigma_factors(sig):
    """Return sig*coth(sig), sig*csch(sig), with no large-sigma overflow."""
    sig = np.asarray(sig, dtype=float)
    coth = sig / np.tanh(sig)
    csch = sig * (2.0 * np.exp(-sig) / (-np.expm1(-2.0 * sig)))
    return coth, csch


def positive_l_range(L, chunk_size=256):
    lo = 1
    while lo <= L:
        hi = min(L + 1, lo + chunk_size)
        yield np.arange(lo, hi, dtype=float)
        lo = hi


def integrate_fejer(nq, L):
    q, wavg = q_rule(nq)
    rods = np.arange(1, 4, dtype=float)
    cosnq = np.cos(np.outer(q, rods))
    numerator = 2.0 * (1.0 - cosnq)
    S = np.sum(FEJER_K[None, :] * (1.0 - cosnq), axis=1)
    # l=0 term, evaluated after quotienting the common translation.
    total = THETA * np.sum(wavg[:, None] * numerator / (2.0 * S[:, None]), axis=0)
    for ell in positive_l_range(L):
        nu = 2.0 * math.pi * THETA * ell
        sig = nu[:, None] * TAU * rods[None, :]
        f_coth, f_csch = sigma_factors(sig)
        D = FEJER_M * nu[:, None] ** 2 + 2.0 * np.sum(
            FEJER_K[None, :, None]
            * (f_coth[:, :, None] - f_csch[:, :, None] * cosnq.T[None, :, :]),
            axis=1,
        )
        # Both positive and negative Matsubara frequencies contribute equally.
        total += 2.0 * THETA * np.einsum(
            "q,lqr,q->r", wavg, numerator[None, :, :] / D[:, :, None],
            np.ones_like(wavg), optimize=True
        )
    # Mass-matrix bound for the omitted +/- l tail; average |e^{inq}-1|^2=2.
    tail = np.full(3, 1.0 / (FEJER_M * math.pi**2 * THETA * L))
    return {f"delta_{i+1}": {"partial_sum": float(total[i]), "tail_upper": float(tail[i])}
            for i in range(3)}


def pendant_matsubara_terms(ell):
    """Exact q-averaged relative and backbone terms for positive ell."""
    ell = np.asarray(ell, dtype=float)
    nu = 2.0 * math.pi * THETA * ell
    sigb = nu * TAU
    sigi = nu * PENDANT_ELL_OVER_A * TAU
    fb_coth, fb_csch = sigma_factors(sigb)
    fi_coth, fi_csch = sigma_factors(sigi)
    P = PENDANT_K * fi_coth
    C = PENDANT_K * fi_csch
    D = PENDANT_MS * nu**2 + P
    A = PENDANT_MB * nu**2 + 2.0 * K * fb_coth + P - C**2 / D
    B = 2.0 * K * fb_csch
    S = np.sqrt(A * A - B * B)
    relative = 1.0 / D + (1.0 - C / D) ** 2 / S
    backbone_neighbor = 2.0 / S * (1.0 - B / (A + S))
    return relative, backbone_neighbor


def integrate_pendant(L, chunk_size=16384):
    """Exact reciprocal-q average; truncates only the Matsubara series."""
    rel_sum = THETA / PENDANT_K  # exact ell=0 relative compliance
    bb_sum = THETA / K           # exact ell=0 neighboring-backbone compliance
    for ell in positive_l_range(L, chunk_size):
        rel, bb = pendant_matsubara_terms(ell)
        rel_sum += 2.0 * THETA * float(np.sum(rel))
        bb_sum += 2.0 * THETA * float(np.sum(bb))
    rel_tail = (1.0 / PENDANT_MB + 1.0 / PENDANT_MS) / (
        2.0 * math.pi**2 * THETA * L
    )
    bb_tail = 1.0 / (math.pi**2 * THETA * PENDANT_MB * L)
    return {
        "pendant_relative": {"partial_sum": float(rel_sum), "tail_upper": float(rel_tail)},
        "backbone_neighbor": {"partial_sum": float(bb_sum), "tail_upper": float(bb_tail)},
    }


def pendant_q_average_check(nq=256, selected_ell=(1, 2, 10, 100)):
    """Compare closed q averages to independent direct Gauss-Legendre sums."""
    q, wavg = q_rule(nq)
    cosq = np.cos(q)
    rows = []
    for ell in selected_ell:
        nu = 2.0 * math.pi * THETA * ell
        fb_coth, fb_csch = sigma_factors(nu * TAU)
        fi_coth, fi_csch = sigma_factors(nu * PENDANT_ELL_OVER_A * TAU)
        A0 = (PENDANT_MB * nu**2 + PENDANT_K * fi_coth
              + 2.0 * K * fb_coth)
        C0 = PENDANT_MS * nu**2 + PENDANT_K * fi_coth
        B0 = PENDANT_K * fi_csch
        A = A0 - B0**2 / C0
        B = 2.0 * K * fb_csch
        S = math.sqrt(A * A - B * B)
        rel_exact = 1.0 / C0 + (1.0 - B0 / C0) ** 2 / S
        bb_exact = 2.0 / S * (1.0 - B / (A + S))
        det = (A0 - B * cosq) * C0 - B0**2
        rel_q = np.sum(wavg * (A0 - B * cosq + C0 - 2.0 * B0) / det)
        bb_q = np.sum(wavg * 2.0 * (1.0 - cosq) * C0 / det)
        rows.append({
            "ell": int(ell),
            "relative_exact_q_average": float(rel_exact),
            "relative_direct_q_average": float(rel_q),
            "relative_abs_difference": float(abs(rel_exact - rel_q)),
            "backbone_neighbor_exact_q_average": float(bb_exact),
            "backbone_neighbor_direct_q_average": float(bb_q),
            "backbone_neighbor_abs_difference": float(abs(bb_exact - bb_q)),
        })
    return {"q_points": nq, "selected_terms": rows,
            "max_abs_difference": max(max(r["relative_abs_difference"],
                                           r["backbone_neighbor_abs_difference"])
                                       for r in rows)}

def main():
    # Matsubara convergence at fixed high q resolution, then independent q
    # convergence at a lower cutoff. No q-quadrature error is included in the
    # mass-tail interval.
    q_ref = 512
    L_ref = 500000
    q_grid = (64, 128, 256, 512)
    L_grid = (5000, 20000, 100000, 500000)
    q_convergence = {str(nq): integrate_fejer(nq, 20000) for nq in q_grid}
    matsubara_convergence = {}
    for L in L_grid:
        matsubara_convergence[str(L)] = {
            "Fejer": integrate_fejer(q_ref, L),
            "pendant_exact_q_average": integrate_pendant(L),
        }
    results = {
        "units": "hbar=k_B=theta=1",
        "parameters": {
            "theta": THETA,
            "tau_a_over_c": TAU,
            "K": K,
            "M_total": M_TOTAL,
            "Fejer_N": 4,
            "Fejer_kappa": FEJER_K.tolist(),
            "Fejer_point_mass": FEJER_M,
            "Fejer_rod_mass": TAU**2 * float(np.dot(np.arange(1, 4)**2, FEJER_K)),
            "pendant_m_backbone": PENDANT_MB,
            "pendant_length_over_a": PENDANT_ELL_OVER_A,
            "pendant_k": PENDANT_K,
            "pendant_rod_mass": PENDANT_MROD,
            "pendant_m_side": PENDANT_MS,
            "pendant_total_mass_check": PENDANT_MB + PENDANT_MS + TAU**2 + PENDANT_MROD,
        },
        "formulas": {
            "Fejer_D_E": "m*nu^2+2*sum_n k_n*sigma_n*(coth(sigma_n)-cos(nq)*csch(sigma_n))",
            "Fejer_endpoint_variance": "theta*sum_l average_q 2*(1-cos(nq))/D_E",
            "pendant_matrix": "[[mb*nu^2+2K*sigma_b*(coth(sigma_b)-cos(q)csch(sigma_b))+k*sigma_i*coth(sigma_i), -k*sigma_i*csch(sigma_i)],[-k*sigma_i*csch(sigma_i), ms*nu^2+k*sigma_i*coth(sigma_i)]]",
            "pendant_relative_variance": "theta*sum_l average_q (-1,1) D_E^-1 (-1,1)^T",
            "backbone_neighbor_variance": "theta*sum_l average_q 2*(1-cos(q))*(D_E^-1)_bb",
            "Matsubara_tail": "partial sum is a lower bound; upper interval adds the positive mass-matrix tail bound",
        },
        "Fejer_q_convergence_at_L_20000": q_convergence,
        "matsubara_convergence_Fejer_q512_and_pendant_exact_q": matsubara_convergence,
        "pendant_analytic_q_average_check": pendant_q_average_check(),
        "best_available_numerical_estimates": {
            "q_points": q_ref,
            "positive_matsubara_cutoff_L": L_ref,
            "Fejer": integrate_fejer(q_ref, L_ref),
            "pendant_exact_q_average": integrate_pendant(L_ref),
        },
        "scope": "ideal harmonic distributed-rod metric graphs; q-grid convergence is empirical, tail bounds only cover omitted Matsubara terms; no material or hardware inference",
    }
    out = Path(__file__).with_name("endpoint_extension_covariance_results.json")
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
