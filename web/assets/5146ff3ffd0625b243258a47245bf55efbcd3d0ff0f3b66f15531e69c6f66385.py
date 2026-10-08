#!/usr/bin/env python3
"""Finite-dimensional diagnostic for Sections 3-4 of PROOF.txt.

This is numerical evidence only; the report gives the separate general proof.
Uses real symmetric matrices so the construction is reproducible with NumPy.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def entropy(a: np.ndarray) -> float:
    vals = np.linalg.eigvalsh((a + a.T) / 2)
    vals = np.clip(vals, 0.0, None)
    vals = vals[vals > 1e-14]
    return float(-np.sum(vals * np.log(vals)))


def log_partition(h: np.ndarray, beta: float) -> float:
    vals = np.linalg.eigvalsh((h + h.T) / 2)
    x = -beta * vals
    m = float(np.max(x))
    return m + float(np.log(np.exp(x - m).sum()))


def gibbs(h: np.ndarray, beta: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh((h + h.T) / 2)
    x = -beta * vals
    x -= np.max(x)
    weights = np.exp(x)
    return (vecs * (weights / weights.sum())) @ vecs.T


def trace_norm(a: np.ndarray) -> float:
    return float(np.sum(np.abs(np.linalg.eigvalsh((a + a.T) / 2))))


def trial(rng: np.random.Generator, d: int, r: int, beta: float) -> dict[str, float]:
    raw = rng.normal(size=(d, d))
    h0 = (raw + raw.T) / 2
    rho0 = gibbs(h0, beta)
    pmat = np.diag([1.0] * r + [0.0] * (d - r))
    qmat = np.eye(d) - pmat
    p = float(np.trace(rho0 @ pmat))
    delta = 1.0 - p
    if not (1e-8 < p < 1.0 - 1e-8):
        raise RuntimeError("degenerate conditioning probability in finite diagnostic")
    sigma = pmat @ rho0 @ pmat / p
    omega = qmat @ rho0 @ qmat / delta
    pinched = pmat @ rho0 @ pmat + qmat @ rho0 @ qmat
    hdelta = -delta * np.log(delta) - p * np.log(p)

    # A positive penalty supported entirely on the rejected subspace.
    x = rng.normal(size=(d, d))
    b = x.T @ x
    w = qmat @ b @ qmat
    rho_w = gibbs(h0 + w, beta)
    logz0 = log_partition(h0, beta)
    logzw = log_partition(h0 + w, beta)
    d_rel = -entropy(sigma) + beta * float(np.trace(sigma @ h0)) + logzw
    variational_rhs = entropy(rho0) - entropy(sigma) + beta * (
        float(np.trace(sigma @ h0)) - float(np.trace(rho0 @ h0))
    )

    t_cond = trace_norm(sigma - rho0)
    t_pinsker = trace_norm(sigma - rho_w)
    t_target = trace_norm(rho0 - rho_w)
    return {
        "pinching_entropy_gain": entropy(pinched) - entropy(rho0),
        "entropy_block_identity_residual": entropy(pinched)
        - (hdelta + p * entropy(sigma) + delta * entropy(omega)),
        "claimed_entropy_bound_slack": (hdelta + delta * np.log(d)) / p
        - (entropy(rho0) - entropy(sigma)),
        "conditioning_gentle_slack": 2 * np.sqrt(delta) - t_cond,
        "penalty_annihilation_norm": float(np.linalg.norm(w @ sigma, ord="fro")),
        "partition_order_slack": logz0 - logzw,
        "gibbs_variational_slack": variational_rhs - d_rel,
        "relative_entropy": d_rel,
        "quantum_pinsker_slack": np.sqrt(max(0.0, 2 * d_rel)) - t_pinsker,
        "final_trace_norm_slack": 2 * np.sqrt(delta) + np.sqrt(max(0.0, 2 * d_rel)) - t_target,
    }


def main() -> None:
    rng = np.random.default_rng(20261008)
    rows = [trial(rng, d, r, beta=0.7) for d in range(2, 9) for r in range(1, d) for _ in range(8)]
    keys = list(rows[0])
    summary = {
        "status": "FINITE_NUMERICAL_DIAGNOSTIC_ONLY",
        "seed": 20261008,
        "trials": len(rows),
        "dimensions": [2, 8],
        "matrix_family": "random real symmetric H0; W=Q X^T X Q; beta=0.7",
        "maxima": {key: max(row[key] for row in rows) for key in keys},
        "minima": {key: min(row[key] for row in rows) for key in keys},
        "tolerances": {
            "entropy_and_variational_violations": 2e-10,
            "trace_bound_violations": 2e-9,
            "penalty_annihilation_frobenius": 2e-12,
        },
    }
    summary["checks_pass"] = bool(
        summary["minima"]["pinching_entropy_gain"] >= -2e-10
        and summary["maxima"]["entropy_block_identity_residual"] <= 2e-10
        and summary["minima"]["claimed_entropy_bound_slack"] >= -2e-10
        and summary["minima"]["conditioning_gentle_slack"] >= -2e-9
        and summary["maxima"]["penalty_annihilation_norm"] <= 2e-12
        and summary["minima"]["partition_order_slack"] >= -2e-10
        and summary["minima"]["gibbs_variational_slack"] >= -2e-10
        and summary["minima"]["quantum_pinsker_slack"] >= -2e-9
        and summary["minima"]["final_trace_norm_slack"] >= -2e-9
    )
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
