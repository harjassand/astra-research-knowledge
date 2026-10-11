"""Finite diagnostics for R23 identities; not a global algorithm or proof.

Uses exact rational elimination for the anchor-fixed row-module identity and
the inherited hard-cut counterexample. Separately checks the trace-objective
gradient and clipping bound on deterministic numerical concentrated frames.
The numerical optimizer is diagnostic gradient descent, not the polynomial
second-order acquisition algorithm cited in the mathematical record.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


def partial_b(matrix: sp.Matrix, da: int, db: int) -> sp.Matrix:
    return sp.Matrix(da, da, lambda i, j: sum(matrix[i * db + b, j * db + b]
                                           for b in range(db)))


def rational_psd(matrix: sp.Matrix) -> bool:
    """Exact Schur-complement PSD test, including singular rational matrices."""
    a = matrix.copy()
    if a != a.conjugate().T:
        return False
    while a.rows:
        diagonal = [sp.simplify(a[i, i]) for i in range(a.rows)]
        if any(x < 0 for x in diagonal):
            return False
        positive = next((i for i, x in enumerate(diagonal) if x > 0), None)
        if positive is None:
            return a == sp.zeros(a.rows)
        order = [positive] + [i for i in range(a.rows) if i != positive]
        a = a.extract(order, order)
        a = a[1:, 1:] - a[1:, :1] * a[:1, 1:] / a[0, 0]
    return True


def verify_guard_certificate(rows: sp.Matrix, filtered: sp.Matrix,
                             anchor: sp.Matrix, db: int,
                             rank_budget: int, marginal_cap: sp.Rational) -> dict:
    """Polynomial-size exact certificate contract for one-sided output."""
    da = anchor.rows
    assert anchor == anchor.conjugate().T
    assert anchor * anchor == anchor
    assert anchor.rank() <= rank_budget
    assert filtered.rank() <= rows.rank()
    slab_columns = sp.kronecker_product(anchor, sp.eye(db)).columnspace()
    slab = (sp.Matrix.hstack(*slab_columns) if slab_columns
            else sp.zeros(da * db, 0))
    left = sp.Matrix.hstack(rows, slab)
    right = sp.Matrix.hstack(filtered, slab)
    assert left.rank() == right.rank() == sp.Matrix.hstack(left, right).rank()
    independent = filtered.columnspace()
    if independent:
        frame = sp.Matrix.hstack(*independent)
        projector = frame * (frame.conjugate().T * frame).inv() * frame.conjugate().T
    else:
        projector = sp.zeros(da * db)
    marginal = partial_b(projector, da, db)
    assert rational_psd(marginal_cap * sp.eye(da) - marginal)
    return {"anchor_rank": int(anchor.rank()),
            "retained_row_rank": len(independent),
            "row_module_rank": int(left.rank()),
            "marginal_cap": str(marginal_cap)}


def exact_checks() -> dict:
    da, db = 3, 2
    rows = sp.zeros(da * db, 2)
    rows[0, 0], rows[2, 0] = 4, 5
    rows[1, 1], rows[3, 1] = 4, -5
    filt = sp.diag(1, sp.Rational(4, 5), 1)
    filtered = sp.kronecker_product(filt, sp.eye(db)) * rows
    anchor = sp.diag(0, 1, 0)
    slab = sp.kronecker_product(anchor, sp.eye(db)).columnspace()
    slab_matrix = sp.Matrix.hstack(*slab)
    left = sp.Matrix.hstack(rows, slab_matrix)
    right = sp.Matrix.hstack(filtered, slab_matrix)
    both = sp.Matrix.hstack(left, right)
    assert left.rank() == right.rank() == both.rank()
    projector = filtered * (filtered.T * filtered).inv() * filtered.T
    marginal = partial_b(projector, da, db)
    assert marginal == sp.diag(1, 1, 0)
    certificate = verify_guard_certificate(rows, filtered, anchor, db, 1, sp.Integer(1))
    hard = sp.kronecker_product(sp.eye(da) - anchor, sp.eye(db)) * rows
    hard_projector = hard * (hard.T * hard).inv() * hard.T
    assert partial_b(hard_projector, da, db) == sp.diag(2, 0, 0)

    # A rational frame with an exact stationary point of Q_s.
    s = sp.Integer(1)
    frame = sp.Matrix([sp.Rational(3, 4), 0, 0, sp.Rational(4, 3)])
    sqrt_h = sp.diag(sp.Rational(4, 5), sp.Rational(3, 5))
    h = sqrt_h * sqrt_h
    out = sp.kronecker_product(sqrt_h, sp.eye(2)) * frame
    out_projector = out * (out.T * out).inv() * out.T
    rho = partial_b(out_projector, 2, 2)
    assert rho == s * (sp.eye(2) - h)
    return {
        "module_join_rank": int(left.rank()),
        "filtered_marginal": str(marginal),
        "hard_cut_marginal": str(partial_b(hard_projector, da, db)),
        "exact_trace_objective_stationarity": True,
        "exact_guard_certificate": certificate,
    }


def spectral_function(h: np.ndarray, fun) -> np.ndarray:
    values, vectors = np.linalg.eigh((h + h.conj().T) / 2)
    return (vectors * fun(values)) @ vectors.conj().T


def objective_data(h: np.ndarray, frame: np.ndarray, da: int, db: int, s: float):
    sqrt_h = spectral_function(h, np.sqrt)
    out = np.kron(sqrt_h, np.eye(db)) @ frame
    gram = out.conj().T @ out
    projector = out @ np.linalg.solve(gram, out.conj().T)
    rho = np.einsum("ibjb->ij", projector.reshape(da, db, da, db))
    sign_g, logdet_g = np.linalg.slogdet(gram)
    sign_h, logdet_h = np.linalg.slogdet(h)
    assert np.real(sign_g) > 0 and np.real(sign_h) > 0
    q = float(np.real(logdet_g - s * logdet_h + s * np.trace(h)))
    gradient = rho - s * np.eye(da) + s * h
    return q, gradient, projector, rho


def numerical_check(seed: int) -> dict:
    rng = np.random.default_rng(seed)
    da, db, rank, s = 10, 5, 6, 2.0
    frame = rng.integers(-4, 5, size=(da * db, rank)).astype(float)
    weights = np.array([1, 1, 1] + [0.03] * (da - 3))
    frame *= np.repeat(weights, db)[:, None]
    # Column QR changes no row range and improves the diagnostic conditioning.
    frame = np.linalg.qr(frame)[0]
    h = np.eye(da)
    q, gradient, _, _ = objective_data(h, frame, da, db, s)

    direction = rng.normal(size=(da, da))
    direction = (direction + direction.T) / 2
    direction /= np.linalg.norm(direction)
    delta = 1e-5
    q_plus = objective_data(spectral_function(delta * direction, np.exp),
                            frame, da, db, s)[0]
    q_minus = objective_data(spectral_function(-delta * direction, np.exp),
                             frame, da, db, s)[0]
    measured = (q_plus - q_minus) / (2 * delta)
    predicted = float(np.trace(gradient @ direction))
    assert abs(measured - predicted) < 2e-7

    for iteration in range(4000):
        q, gradient, _, _ = objective_data(h, frame, da, db, s)
        norm = np.linalg.norm(gradient)
        if norm < 1e-6:
            break
        sqrt_h = spectral_function(h, np.sqrt)
        step = min(0.5, 0.5 / max(1.0, norm))
        for _ in range(40):
            proposal = sqrt_h @ spectral_function(-step * gradient, np.exp) @ sqrt_h
            q_next = objective_data(proposal, frame, da, db, s)[0]
            if q_next <= q - 0.1 * step * norm * norm:
                h = (proposal + proposal.T) / 2
                break
            step /= 2
        else:
            raise AssertionError(f"Diagnostic line search failed at iteration {iteration}, gradient {norm}")
    q, gradient, _, rho = objective_data(h, frame, da, db, s)
    assert np.linalg.norm(gradient) < 1e-6
    values = np.linalg.eigvalsh(h)
    hhat = spectral_function(h, lambda x: np.minimum(2 * x, 1))
    _, _, _, rho_hat = objective_data(hhat, frame, da, db, s)
    ell = int(np.count_nonzero(values < 0.5))
    assert ell <= 2 * rank / s
    assert np.linalg.eigvalsh(rho_hat)[-1] <= 2 * s + 1e-7
    return {
        "seed": seed,
        "iterations": iteration + 1,
        "gradient_frobenius": float(np.linalg.norm(gradient)),
        "gradient_finite_difference_error": abs(measured - predicted),
        "minimum_h_eigenvalue": float(values[0]),
        "clipped_anchor_rank": ell,
        "rank_budget": 2 * rank / s,
        "original_scaled_marginal_max": float(np.linalg.eigvalsh(rho)[-1]),
        "clipped_marginal_max": float(np.linalg.eigvalsh(rho_hat)[-1]),
        "clipped_marginal_bound": 2 * s,
    }


if __name__ == "__main__":
    result = {
        "scope": "finite exact and numerical diagnostics; not universal proof or encoder",
        "exact": exact_checks(),
        "numerical": [numerical_check(seed) for seed in (23, 2301, 2302)],
    }
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
