#!/usr/bin/env python3
"""Reproduce the sign check for the Xiang et al. six-species photocycle.

All constants are the published MFE_kinetic_model.m defaults except beta.
Concentrations are micromolar, rates use seconds, and Q denotes FMNH radical.
This is a source-model calculation, not an inference about unknown in-vivo
radical identity or about fluorescence calibration in the Nature experiment.
"""
from __future__ import annotations

import json
from math import sqrt


LIS = 1652.0
KSR = 2.5e8
KTR = 224.0
KISC = 185497.528691897
KRED = 50.5406
KOX = 0.003675
KDIS = 5000.0
M_TOTAL = 50.0
F_TOTAL = 350.0
INVARIANT = 90.0
BETA0 = 0.68
BETA_RF = BETA0 + 0.117 * 0.3  # Nature S8 fitted law evaluated at B1=0.3 mT.
A = KISC * LIS / (KSR + KISC)
C_RATIO = KDIS / KOX


def state_at_q(q: float) -> dict[str, float]:
    """Stationary concentrations parameterized by Q, and local derivatives."""
    disc = sqrt((q - 40.0) ** 2 + 8.0 * C_RATIO * q**2)
    f = (40.0 - q + disc) / 4.0
    r = 2.0 * f + q - 40.0
    h = F_TOTAL - f - q
    c = KTR + KRED * h
    m_remaining = M_TOTAL - r  # G + T
    g = m_remaining * c / (A + c)
    t = A * m_remaining / (A + c)
    beta = KDIS * q**2 * (A + c) / (A * KRED * h * m_remaining)

    f_q = (-1.0 + (q - 40.0 + 8.0 * C_RATIO * q) / disc) / 4.0
    r_q = 2.0 * f_q + 1.0
    h_q = -f_q - 1.0
    g_q = -r_q * c / (A + c) + m_remaining * A * KRED * h_q / (A + c) ** 2
    beta_q = beta * (
        2.0 / q
        + KRED * h_q / (A + c)
        - h_q / h
        + r_q / m_remaining
    )
    return {
        "Q": q,
        "G": g,
        "T": t,
        "R": r,
        "F": f,
        "H": h,
        "beta": beta,
        "dF_dQ": f_q,
        "dR_dQ": r_q,
        "dH_dQ": h_q,
        "dG_dQ": g_q,
        "dbeta_dQ": beta_q,
        "dG_dbeta": g_q / beta_q,
    }


def find_q_for_beta(target: float, lo: float = 0.035, hi: float = 0.036) -> float:
    """Bisection on the physical local branch containing beta=0.68."""
    f_lo = state_at_q(lo)["beta"] - target
    f_hi = state_at_q(hi)["beta"] - target
    if f_lo * f_hi >= 0.0:
        raise ValueError("target beta not bracketed on selected physical branch")
    for _ in range(180):
        mid = (lo + hi) / 2.0
        f_mid = state_at_q(mid)["beta"] - target
        if f_lo * f_mid > 0.0:
            lo, f_lo = mid, f_mid
        else:
            hi, f_hi = mid, f_mid
    return (lo + hi) / 2.0


def stationary_rhs(s: dict[str, float], beta: float) -> dict[str, float]:
    g, t, r, f, h, q = (s[name] for name in ("G", "T", "R", "F", "H", "Q"))
    a = A * g
    u = beta * KRED * h * t
    v = KOX * f * r
    w = KDIS * q**2
    return {
        "dG": -a + (KTR + (1.0 - beta) * KRED * h) * t + v,
        "dT": a - (KTR + KRED * h) * t,
        "dR": u - v,
        "dF": -v + w,
        "dH": -u + w,
        "dQ": u - 2.0 * w + v,
    }


def main() -> None:
    q0 = find_q_for_beta(BETA0)
    q1 = find_q_for_beta(BETA_RF)
    s0 = state_at_q(q0)
    s1 = state_at_q(q1)
    delta_beta = BETA_RF - BETA0
    out = {
        "status": "source_model_stationary_calculation_only",
        "constants": {
            "lis_s-1": LIS,
            "ksr_s-1": KSR,
            "ktr_s-1": KTR,
            "kisc_s-1": KISC,
            "kred_uM-1_s-1": KRED,
            "kox_uM-1_s-1": KOX,
            "kdis_uM-1_s-1": KDIS,
            "initial_mScarlet_total_uM": M_TOTAL,
            "initial_flavin_total_uM": F_TOTAL,
            "initial_stoichiometric_invariant_uM": INVARIANT,
            "a_effective_s-1": A,
        },
        "beta_baseline": BETA0,
        "beta_after_Nature_fit_at_B1_0.3mT": BETA_RF,
        "baseline_stationary_state": s0,
        "rf_fit_stationary_state": s1,
        "delta_G_uM": s1["G"] - s0["G"],
        "relative_delta_G_percent": 100.0 * (s1["G"] / s0["G"] - 1.0),
        "beta_step": delta_beta,
        "instantaneous_delta_dG_dt_uM_per_s_after_beta_step": -delta_beta * KRED * s0["H"] * s0["T"],
        "baseline_full_rhs_residual_s-1_or_uM_s-1": stationary_rhs(s0, BETA0),
        "rf_fit_full_rhs_residual_s-1_or_uM_s-1": stationary_rhs(s1, BETA_RF),
        "conservation_residuals": {
            "baseline_mScarlet_uM": s0["G"] + s0["T"] + s0["R"] - M_TOTAL,
            "baseline_flavin_uM": s0["F"] + s0["H"] + s0["Q"] - F_TOTAL,
            "baseline_hidden_invariant_uM": s0["G"] + s0["T"] + 2*s0["F"] + s0["Q"] - INVARIANT,
            "rf_mScarlet_uM": s1["G"] + s1["T"] + s1["R"] - M_TOTAL,
            "rf_flavin_uM": s1["F"] + s1["H"] + s1["Q"] - F_TOTAL,
            "rf_hidden_invariant_uM": s1["G"] + s1["T"] + 2*s1["F"] + s1["Q"] - INVARIANT,
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
