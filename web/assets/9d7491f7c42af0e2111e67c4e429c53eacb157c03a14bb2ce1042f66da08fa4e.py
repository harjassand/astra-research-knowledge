#!/usr/bin/env python3
"""Finite-state controlled-jump witness: same CLE (b,A), different pulse words.

This is a model check, not a biological model.  State is (x,m), x in {0,...,4}
and a hidden two-level memory coordinate m in {0,1}.  Actions are passive 0,
prime P, neutral-load L, and challenge B.  The two hypotheses are sigma=+1/-1.
"""

from __future__ import annotations

import json
from math import exp, log, sqrt
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
X_STATES = range(5)
M_STATES = range(2)
STATES = [(x, m) for x in X_STATES for m in M_STATES]
IDX = {s: i for i, s in enumerate(STATES)}
JUMPS = (-2, -1, 1, 2)
H = np.array([1.0, -2.0, 2.0, -1.0])
H_X = np.array([1.0, -2.0, 0.0, 2.0, -1.0])


def expm_generator(Q: np.ndarray, duration: float, tol: float = 1e-14) -> np.ndarray:
    """Uniformization matrix exponential for a finite-state CTMC generator."""
    rate = float(np.max(-np.diag(Q)))
    if rate == 0.0 or duration == 0.0:
        return np.eye(Q.shape[0])
    mean = rate * duration
    if mean > 500:
        raise ValueError("uniformization helper is intended for bounded pulse durations")
    P = np.eye(Q.shape[0]) + Q / rate
    term = np.eye(Q.shape[0])
    weight = exp(-mean)
    total = weight * term
    cdf = weight
    k = 0
    while 1.0 - cdf > tol:
        k += 1
        term = term @ P
        weight *= mean / k
        total += weight * term
        cdf += weight
        if k > 10000:
            raise ArithmeticError("uniformization did not converge")
    return total


def add_rate(Q: np.ndarray, source: tuple[int, int], target: tuple[int, int], rate: float) -> None:
    i, j = IDX[source], IDX[target]
    Q[i, j] += rate
    Q[i, i] -= rate


def generators(
    sigma: int,
    *,
    lam: float,
    mu: float,
    delta: float,
    a: float,
    ell: float,
    c: tuple[float, float, float, float],
    epsilon: float,
) -> dict[str, np.ndarray]:
    """Return row-generator matrices for 0/P/L/B under one sign hypothesis."""
    if not np.isclose(a, ell, rtol=0.0, atol=1e-12):
        raise ValueError("the closed-form difference-in-differences assumes matched P/L loading rates")
    q0 = np.zeros((len(STATES), len(STATES)))
    qp = np.zeros_like(q0)
    ql = np.zeros_like(q0)
    qb = np.zeros_like(q0)

    # Common passive birth/death and common memory washout. Bound X to [0,4].
    for x, m in STATES:
        if x < 4:
            add_rate(q0, (x, m), (x + 1, m), lam)
        if x > 0:
            add_rate(q0, (x, m), (x - 1, m), mu * x)
        if m == 1:
            add_rate(q0, (x, m), (x, 0), delta)

    # Matched pulses: same unknown rate, same X displacement, different memory bit.
    add_rate(qp, (0, 0), (2, 1), a)
    add_rate(ql, (0, 0), (2, 0), ell)

    # At m=0 B is the common reference channel; at m=1 it has a null-moment
    # perturbation.  Rate order matches JUMPS and H.
    for m in (0, 1):
        for jump, base, hval in zip(JUMPS, c, H):
            rate = base + (sigma * epsilon * hval if m == 1 else 0.0)
            if rate <= 0:
                raise ValueError("all controlled reaction rates must be positive")
            add_rate(qb, (2, m), (2 + jump, m), rate)

    return {"0": q0, "P": qp, "L": ql, "B": qb}


def moments(Q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Kramers-Moyal first and second jump-moment fields for the full (x,m)."""
    b = np.zeros((len(STATES), 2))
    A = np.zeros((len(STATES), 2, 2))
    for i, (x, m) in enumerate(STATES):
        for j, (xp, mp) in enumerate(STATES):
            if i == j or Q[i, j] <= 0:
                continue
            dv = np.array([xp - x, mp - m], dtype=float)
            b[i] += Q[i, j] * dv
            A[i] += Q[i, j] * np.outer(dv, dv)
    return b, A


def confusion(eta: float) -> np.ndarray:
    """Symmetric five-category X-readout channel; eta is total error mass."""
    C = np.full((5, 5), eta / 4.0)
    np.fill_diagonal(C, 1.0 - eta)
    return C


def run_example() -> dict:
    # Rates are dimensionless example values. c is intentionally asymmetric;
    # the neutral-load arm cancels its unknown score projection h.c.
    pars = {
        "lam": 0.7,
        "mu": 0.15,
        "delta": 0.08,
        "a": 3.0,
        "ell": 3.0,
        "c": (1.2, 0.8, 1.1, 0.9),
        "epsilon": 0.1,
        "tau_pulse": 0.2,
        "tau_b": 0.25,
        "eta": 0.2,
    }
    initial_q0 = 1.0
    q_plus = generators(+1, **{k: v for k, v in pars.items() if k not in ("tau_pulse", "tau_b", "eta")})
    q_minus = generators(-1, **{k: v for k, v in pars.items() if k not in ("tau_pulse", "tau_b", "eta")})

    # Check exact actionwise equality numerically over every full state.
    max_b_diff = 0.0
    max_A_diff = 0.0
    action_moment_differences: dict[str, dict[str, float]] = {}
    for u in ("0", "P", "L", "B"):
        bp, ap = moments(q_plus[u])
        bm, am = moments(q_minus[u])
        db, da = float(np.max(np.abs(bp - bm))), float(np.max(np.abs(ap - am)))
        action_moment_differences[u] = {"max_abs_b_difference": db, "max_abs_A_difference": da}
        max_b_diff, max_A_diff = max(max_b_diff, db), max(max_A_diff, da)

    # The moment-null direction and the first differing local jump moment.
    v = np.array(JUMPS, dtype=float)
    null_checks = {
        "sum_h": float(np.sum(H)),
        "h_dot_v": float(H @ v),
        "h_dot_v2": float(H @ (v**2)),
        "h_dot_v3": float(H @ (v**3)),
    }
    third_moment_gap = 2 * pars["epsilon"] * null_checks["h_dot_v3"]

    # P/L then B, alongside their no-B controls. Start at the calibrated state (0,0).
    e0 = np.zeros(len(STATES))
    e0[IDX[(0, 0)]] = initial_q0
    e0[IDX[(0, 1)]] = 1.0 - initial_q0
    T = pars["tau_pulse"]
    TB = pars["tau_b"]
    Cx = confusion(pars["eta"])
    out: dict[str, dict] = {}
    for sig, q in ((+1, q_plus), (-1, q_minus)):
        eP = e0 @ expm_generator(q["P"], T)
        eL = e0 @ expm_generator(q["L"], T)
        ePB = eP @ expm_generator(q["B"], TB)
        eLB = eL @ expm_generator(q["B"], TB)
        # Passive no-pulse paths are shared, and single P/L/B from (0,0) agree.
        eB = e0 @ expm_generator(q["B"], TB)
        # Reversing the two-pulse word makes B act at X=0, where it is inactive.
        eBP_order = e0 @ expm_generator(q["B"], TB) @ expm_generator(q["P"], T)

        def x_marg(p: np.ndarray) -> np.ndarray:
            ans = np.zeros(5)
            for i, (x, m) in enumerate(STATES):
                ans[x] += p[i]
            return ans

        pP, pL, pPB, pLB, pB, pBP_order = map(
            x_marg, (eP, eL, ePB, eLB, eB, eBP_order)
        )
        # Raw score h(Yx); symmetric confusion contracts the zero-sum contrast by kappa.
        def score(p_x: np.ndarray) -> float:
            return float((p_x @ Cx) @ H_X)

        gap = (score(pPB) - score(pP)) - (score(pLB) - score(pL))
        lam_total = sum(pars["c"])
        r = 1.0 - exp(-pars["a"] * T)
        s = 1.0 - exp(-lam_total * TB)
        kappa = 1.0 - 5.0 * pars["eta"] / 4.0
        predicted_gap = initial_q0 * sig * 10.0 * kappa * r * s * pars["epsilon"] / lam_total
        out[str(sig)] = {
            "p_B_from_00_x": pB.tolist(),
            "p_P_x": pP.tolist(),
            "p_L_x": pL.tolist(),
            "p_PB_x": pPB.tolist(),
            "p_LB_x": pLB.tolist(),
            "p_BP_order_x": pBP_order.tolist(),
            "difference_in_differences_observed_score": gap,
            "predicted_score_gap": predicted_gap,
            "formula_abs_error": abs(gap - predicted_gap),
        }

    pb_difference = np.array(out["1"]["p_PB_x"]) - np.array(out["-1"]["p_PB_x"])
    bp_difference = np.array(out["1"]["p_BP_order_x"]) - np.array(out["-1"]["p_BP_order_x"])
    pb_tv_raw = 0.5 * float(np.sum(np.abs(pb_difference)))
    pb_tv_reported = 0.5 * float(np.sum(np.abs(pb_difference @ Cx)))
    bp_tv_raw = 0.5 * float(np.sum(np.abs(bp_difference)))
    lam_total_order = sum(pars["c"])
    r_order = 1.0 - exp(-pars["a"] * T)
    s_order = 1.0 - exp(-lam_total_order * TB)
    k_order = 1.0 - 5.0 * pars["eta"] / 4.0
    order_tv_check = {
        "PB_raw_tv": pb_tv_raw,
        "PB_raw_tv_predicted": 6.0 * initial_q0 * r_order * s_order * pars["epsilon"] / lam_total_order,
        "PB_reported_tv": pb_tv_reported,
        "PB_reported_tv_predicted": 6.0 * initial_q0 * r_order * s_order * pars["epsilon"] * k_order / lam_total_order,
        "BP_raw_tv": bp_tv_raw,
        "scope": "endpoint X-law comparison between H+ and H-; B then P is inactive on X0=0",
    }

    # Sample-cost illustration from Hoeffding for four independent arms, each n founders.
    r = 1.0 - exp(-pars["a"] * T)
    lam_total = sum(pars["c"])
    s = 1.0 - exp(-lam_total * TB)
    kappa = 1.0 - 5.0 * pars["eta"] / 4.0
    d_obs = 10.0 * kappa * r * s * pars["epsilon"] / lam_total
    alpha = 0.05
    n_per_arm = int(np.ceil(32.0 * log(1 / alpha) / d_obs**2))

    # Unknown initial memory occupancy scales the exact DID.  Verify the factor
    # for a nontrivial mixture supported on X=0, without revealing M to the X reporter.
    q0_check = 0.4
    e0_mix = np.zeros(len(STATES))
    e0_mix[IDX[(0, 0)]] = q0_check
    e0_mix[IDX[(0, 1)]] = 1.0 - q0_check
    mixture_gaps: dict[str, dict[str, float]] = {}
    for sig, q in ((+1, q_plus), (-1, q_minus)):
        eP = e0_mix @ expm_generator(q["P"], T)
        eL = e0_mix @ expm_generator(q["L"], T)
        ePB = eP @ expm_generator(q["B"], TB)
        eLB = eL @ expm_generator(q["B"], TB)

        def mixture_x_marg(p: np.ndarray) -> np.ndarray:
            ans = np.zeros(5)
            for i, (x, m) in enumerate(STATES):
                ans[x] += p[i]
            return ans

        gap = (
            score(mixture_x_marg(ePB)) - score(mixture_x_marg(eP))
            - score(mixture_x_marg(eLB)) + score(mixture_x_marg(eL))
        )
        pred = q0_check * sig * 10.0 * kappa * r * s * pars["epsilon"] / lam_total
        mixture_gaps[str(sig)] = {
            "q0": q0_check,
            "observed_score_gap": gap,
            "predicted_score_gap": pred,
            "formula_abs_error": abs(gap - pred),
        }

    return {
        "status": "finite_model_check_only",
        "state_space": STATES,
        "actions": ["passive", "prime_P", "neutral_load_L", "challenge_B"],
        "parameters": {k: list(v) if isinstance(v, tuple) else v for k, v in pars.items()},
        "initial_distribution": {
            "support": [[0, 0], [0, 1]],
            "q0": initial_q0,
            "interpretation": "P(M0=0 | X0=0); X reporter does not observe M",
        },
        "null_moment_checks": null_checks,
        "third_jump_moment_gap_plus_minus": third_moment_gap,
        "actionwise_moment_differences": action_moment_differences,
        "max_abs_full_state_b_difference": max_b_diff,
        "max_abs_full_state_A_difference": max_A_diff,
        "hypothesis_outputs": out,
        "pulse_order_tv_check": order_tv_check,
        "finite_sample_example": {
            "raw_score_range": [-2, 2],
            "order_contrast_gap_abs": d_obs,
            "family_error_target_for_four_arm_test": alpha,
            "hoeffding_founders_per_arm_sufficient": n_per_arm,
            "total_four_arm_founders": 4 * n_per_arm,
            "calibration_and_passive_controls_additional": True,
        },
        "emission_channel": {
            "eta_total_error": pars["eta"],
            "contrast_eigenvalue_kappa": kappa,
            "rank": int(np.linalg.matrix_rank(Cx)),
            "condition_number": float(np.linalg.cond(Cx)),
        },
        "unknown_initial_memory_mixture_check": {
            "baseline_support": [[0, 0], [0, 1]],
            "q0": q0_check,
            "hypothesis_outputs": mixture_gaps,
            "scope": "finite diagnostic for q0 scaling; memory bit is hidden from the X reporter",
        },
    }


if __name__ == "__main__":
    result = run_example()
    outfile = ROOT / "CYCLE3_RUN.json"
    outfile.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
