#!/usr/bin/env python3
"""Finite spin check for a covariant rank-Q instrument (not a converse).

The channel on spin j is

  Lambda_{j,Q}(X) = (2j+1)/Q int K_u X K_u d u,
  K_u = U_u P_top,Q U_u^*,

where du is normalized area measure and P_top,Q projects onto the Q highest
J_z weights.  This is a valid instrument with a Q-dimensional quantum branch
and a continuous classical direction label.  The label is deliberately not
charged/ discretized here, so the check is only a spin-block diagnostic.

For a diagonal input, covariance reduces the output to its diagonal, and the
Haar integral reduces to x=cos^2(theta/2) uniform on [0,1].  NumPy is the only
non-standard dependency.  The exact dipole eigenvalue for this family is

  lambda_1 = [j^2+(Q-1)/2]/[j(j+1)].

The script checks this identity numerically and records thermal trace errors
for beta=gamma/(2j), i.e. a fixed critical spin parameter 2 beta j=gamma.
These checks do not establish the optimality of this family or any all-channel
bound.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss


def spin_rotation_data(j: int):
    m = np.arange(-j, j + 1, dtype=float)
    d = len(m)
    jp = np.zeros((d, d), dtype=np.complex128)
    for a, ma in enumerate(m[:-1]):
        jp[a + 1, a] = math.sqrt(j * (j + 1) - ma * (ma + 1))
    jy = (jp - jp.conj().T) / (2.0j)
    evals, evecs = np.linalg.eigh(jy)
    return m, evals, evecs


def apply_diagonal(j: int, q: int, weights: np.ndarray, values: np.ndarray,
                   quadrature_order: int = 128) -> np.ndarray:
    """Diagonal of Lambda(diag(values)); values need not be positive."""
    m, evals, evecs = spin_rotation_data(j)
    d = len(m)
    norm = float(np.dot(weights, weights))
    ids = np.arange(d - q, d)
    xs, ws = leggauss(quadrature_order)
    xs, ws = (xs + 1.0) / 2.0, ws / 2.0
    out = np.zeros(d, dtype=float)
    for x, w in zip(xs, ws):
        theta = 2.0 * math.acos(math.sqrt(float(x)))
        u = (evecs * np.exp(-1j * theta * evals)) @ evecs.conj().T
        r = u[:, ids]
        k = (r * weights) @ r.conj().T
        out += (d / norm) * float(w) * ((np.abs(k) ** 2) @ values)
    return out


def thermal_fixture(j: int, q: int, gamma: float) -> dict:
    m = np.arange(-j, j + 1, dtype=float)
    beta = gamma / (2.0 * j)
    p = np.exp(2.0 * beta * m)
    p /= p.sum()
    weights = np.ones(q, dtype=float)  # P_top,Q, normalized by ||P||_F^2=Q
    out = apply_diagonal(j, q, weights, p)
    dipole_out = apply_diagonal(j, q, weights, m)
    lam_numeric = float(np.dot(m, dipole_out) / np.dot(m, m))
    lam_exact = (j * j + (q - 1) / 2.0) / (j * (j + 1.0))
    tv = float(0.5 * np.abs(out - p).sum())
    return {
        "j": j,
        "Q": q,
        "gamma_2beta_j": gamma,
        "trace_out": float(out.sum()),
        "dipole_lambda_numeric": lam_numeric,
        "dipole_lambda_exact": lam_exact,
        "dipole_lambda_abs_residual": abs(lam_numeric - lam_exact),
        "thermal_half_trace_error": tv,
        "j_times_error": j * tv,
    }


def main() -> None:
    records = [
        thermal_fixture(j, q, gamma)
        for gamma in (0.5, 1.0, 2.0)
        for j in (8, 16, 32)
        for q in (1, 2, 3)
        if q <= 2 * j + 1
    ]
    residual = max(r["dipole_lambda_abs_residual"] for r in records)
    trace_residual = max(abs(r["trace_out"] - 1.0) for r in records)
    result = {
        "status": "FINITE-EVIDENCE; one covariant channel family only",
        "records": records,
        "max_dipole_formula_residual": residual,
        "max_trace_residual": trace_residual,
        "interpretation": (
            "For this top-weight rank-Q filter, Q=1,2,3 all retain a positive "
            "j*error scale in the fixtures. This does not rule out other "
            "rank-Q instruments, output-sector transport, or optimized decoders."
        ),
    }
    out_path = Path(__file__).with_name("fixed_q_critical_checks.json")
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "records": len(records),
        "max_dipole_formula_residual": residual,
        "max_trace_residual": trace_residual,
        "output": str(out_path),
    }, indent=2))


if __name__ == "__main__":
    main()
