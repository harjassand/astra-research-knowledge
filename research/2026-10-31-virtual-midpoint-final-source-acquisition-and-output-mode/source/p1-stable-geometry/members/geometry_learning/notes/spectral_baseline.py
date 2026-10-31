"""Reference spectral-ball fit and a rigorous *final matrix* certificate.

This module is a comparator/audit aid, not an end-to-end physical experiment.
The optimizer uses NumPy floating point.  The final contraction and residual
certificates use exact rational arithmetic on the supplied binary floats.
They do not certify that supplied X, Y, or source observations were accurate.

Run: python geometry_learning/notes/spectral_baseline.py
"""

from __future__ import annotations

from fractions import Fraction
from math import ceil, isqrt, log2, sqrt
import json

import numpy as np


def project_contraction(a: np.ndarray, margin: float = 0.0) -> np.ndarray:
    """Frobenius projection onto ||A||_2 <= 1-margin (floating diagnostic)."""
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    return (u * np.minimum(s, 1.0 - margin)) @ vt


def fit_minimax_contraction(
    x: np.ndarray,
    target: np.ndarray,
    *,
    excess: float,
    max_steps: int | None = None,
    stop_at: float | None = None,
) -> tuple[np.ndarray, dict]:
    """Fit max-column residual on the spectral-norm unit ball.

    With exact arithmetic, start A=0, B=max_i||x_i||, dimension k, and
    T=ceil(k B^2/excess^2), the smallest objective among iterates is at most
    optimum+excess. A smaller max_steps explicitly forfeits that bound.
    Returning early by stop_at relies on the attained certificate, not on an
    optimality claim. No inverse or supplied condition number is used.
    """
    k, n = x.shape
    if target.shape != (k, n):
        raise ValueError("target and x must have identical shapes")
    if k == 0:
        return np.empty((0, 0)), {"iterations": 0, "residual": 0.0}
    b = float(np.linalg.norm(x, axis=0).max(initial=0.0))
    if b == 0:
        return np.zeros((k, k)), {
            "iterations": 0,
            "residual": float(np.linalg.norm(target, axis=0).max(initial=0.0)),
        }
    prescribed = max(1, ceil(k * b * b / (excess * excess)))
    steps = prescribed if max_steps is None else min(prescribed, max_steps)
    # This step size gives the standard exact-arithmetic bound at actual T.
    step_size = sqrt(k) / (b * sqrt(steps))
    a = np.zeros((k, k))
    best = a.copy()
    best_loss = float("inf")
    completed = 0
    for t in range(steps):
        residual = a @ x - target
        sizes = np.linalg.norm(residual, axis=0)
        j = int(np.argmax(sizes))
        loss = float(sizes[j])
        if loss < best_loss:
            best_loss, best = loss, a.copy()
        completed = t + 1
        if loss == 0.0 or (stop_at is not None and loss <= stop_at):
            break
        gradient = np.outer(residual[:, j] / loss, x[:, j])
        a = project_contraction(a - step_size * gradient)
    return best, {
        "iterations": completed,
        "prescribed_iterations": prescribed,
        "steps_cap": steps,
        "exact_arithmetic_excess_bound_at_cap": sqrt(k) * b / sqrt(steps),
        "residual_float": best_loss,
        "spectral_norm_float": float(np.linalg.norm(best, 2)),
        "status": "floating optimizer; use final certificates",
    }


def rational_matrix(a: np.ndarray) -> list[list[Fraction]]:
    return [[Fraction.from_float(float(v)) for v in row] for row in a]


def sqrt_upper(q: Fraction, bits: int = 80) -> Fraction:
    """Dyadic rational upper bound on sqrt(q), computed with integer arithmetic."""
    if q < 0:
        raise ValueError("negative radicand")
    scale = 1 << bits
    numerator = q.numerator * scale * scale
    denominator = q.denominator
    root = isqrt(numerator // denominator)
    if root * root * denominator < numerator:
        root += 1
    return Fraction(root, scale)


def frob_sq(a: list[list[Fraction]]) -> Fraction:
    return sum((v * v for row in a for v in row), Fraction(0))


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a)]


def multiply(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    bt = transpose(b)
    return [[sum((u * v for u, v in zip(row, col)), Fraction(0))
             for col in bt] for row in a]


def subtract(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[u - v for u, v in zip(ar, br)] for ar, br in zip(a, b)]


def identity(k: int) -> list[list[Fraction]]:
    return [[Fraction(int(i == j)) for j in range(k)] for i in range(k)]


def spectral_norm_upper(
    a: np.ndarray,
    bits: int = 80,
    *,
    exact_matrix: list[list[Fraction]] | None = None,
) -> Fraction:
    """Rigorous norm bound from a floating SVD, checked in exact rationals.

    For the returned numerical U,S,Vt, evaluate their orthogonality defects
    and reconstruction residual exactly. Then
      ||A|| <= sqrt(1+||U'U-I||F)*max(S)*
               sqrt(1+||Vt Vt'-I||F) + ||A-U S Vt||F.
    Even an inaccurate SVD cannot make this upper bound falsely small.
    """
    if a.size == 0:
        return Fraction(0)
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    ar = rational_matrix(a) if exact_matrix is None else exact_matrix
    ur, vr = map(rational_matrix, (u, vt))
    sr = [Fraction.from_float(float(t)) for t in s]
    us = [[v * sr[j] for j, v in enumerate(row)] for row in ur]
    error = sqrt_upper(frob_sq(subtract(ar, multiply(us, vr))), bits)
    eu = sqrt_upper(frob_sq(subtract(multiply(transpose(ur), ur), identity(len(s)))), bits)
    ev = sqrt_upper(frob_sq(subtract(multiply(vr, transpose(vr)), identity(len(s)))), bits)
    return sqrt_upper(1 + eu, bits) * max(sr) * sqrt_upper(1 + ev, bits) + error


def certified_gram_factor_error(ghat: np.ndarray, x: np.ndarray) -> Fraction:
    """Bound ||Ghat-X'X||, including all matrix-product rounding error.

    The residual used by the certificate is formed in exact rationals.
    A floating residual is only an SVD proposal; it is not trusted as exact.
    """
    xr = rational_matrix(x)
    residual = subtract(rational_matrix(ghat), multiply(transpose(xr), xr))
    proposal = ghat - x.T @ x
    return spectral_norm_upper(proposal, exact_matrix=residual)


def certify_rank_from_probes(ghat: np.ndarray, w: np.ndarray, eta: float) -> bool:
    """Prove rank(G)>=number of columns of W, conditional on ||G-Ghat||<=eta.

    Exactly test W'(Ghat-eta I)W positive definite by unpivoted LDL'.
    No eigensolver orthogonality or eigenvalue ordering is trusted.
    False means this particular numerical certificate failed, not low rank.
    """
    gr = rational_matrix(ghat)
    er = Fraction.from_float(float(eta))
    for i in range(len(gr)):
        gr[i][i] -= er
    wr = rational_matrix(w)
    c = multiply(multiply(transpose(wr), gr), wr)
    k = len(c)
    for j in range(k):
        pivot = c[j][j]
        if pivot <= 0:
            return False
        for i in range(j + 1, k):
            for l in range(i, k):
                value = c[l][i] - c[l][j] * c[i][j] / pivot
                c[l][i] = value
                c[i][l] = value
    return True


def certified_contraction(a: np.ndarray, perturbation_budget: float = 1e-6) -> tuple[np.ndarray, dict]:
    """Shrink and dyadically round, then prove the returned matrix contracts.

    All final inequalities use rationals. The perturbation budget is checked,
    not assumed. This helper only supports a dyadic output representable in
    binary64; a smaller budget requires a rational/MP output implementation.
    """
    if a.size == 0:
        return a.copy(), {"certified_contraction": True, "norm_upper": 0.0}
    k = a.shape[0]
    nu = Fraction.from_float(float(perturbation_budget))
    if not (0 < nu <= 1):
        raise ValueError("perturbation_budget must lie in (0,1]")
    upper = spectral_norm_upper(a)
    if upper > 1 + nu / 8:
        raise ValueError("input is too far outside the contraction ball; project first")
    scale = max(Fraction(1), upper) * (1 + nu / 4)
    bits = max(1, ceil(log2(10 * k / float(nu))))
    if bits > 50:
        raise ValueError("requested precision needs rational or multiprecision output")
    dyadic = 1 << bits
    ar = rational_matrix(a)
    out_r = []
    for row in ar:
        rounded_row = []
        for value in row:
            z = value * dyadic / scale
            # Nearest integer, with a deterministic choice at ties.
            integer = (2 * z.numerator + z.denominator) // (2 * z.denominator)
            rounded_row.append(Fraction(integer, dyadic))
        out_r.append(rounded_row)
    rounding_error = sqrt_upper(frob_sq(subtract(out_r,
        [[value / scale for value in row] for row in ar])))
    norm_bound = upper / scale + rounding_error
    change_bound = sqrt_upper(frob_sq(subtract(out_r, ar)))
    if norm_bound > 1 or change_bound > nu:
        raise AssertionError("final exact-rational contraction/perturbation check failed")
    out = np.array([[float(v) for v in row] for row in out_r])
    # The dyadic entries with bits<=50 and |entry|<=1 are exactly binary64.
    if rational_matrix(out) != out_r:
        raise AssertionError("output conversion was not exact")
    return out, {
        "certified_contraction": True,
        "norm_upper": float(norm_bound),
        "norm_upper_exact": str(norm_bound),
        "perturbation_frobenius_upper": float(change_bound),
        "dyadic_bits": bits,
    }


def certified_max_column_residual(a: np.ndarray, x: np.ndarray, target: np.ndarray) -> Fraction:
    """Exact-input certificate for max_i||A x_i-target_i||2."""
    residual = subtract(multiply(rational_matrix(a), rational_matrix(x)), rational_matrix(target))
    return max((sqrt_upper(sum((v * v for v in col), Fraction(0)))
                for col in zip(*residual)), default=Fraction(0))


def self_check() -> dict:
    rng = np.random.default_rng(20261031)
    # A two-dimensional contraction task with redundant raw training points.
    angles = np.linspace(0, 2 * np.pi, 29, endpoint=False)
    x = np.vstack((np.cos(angles), np.sin(angles)))
    theta = 0.37
    true_a = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    target = true_a @ x
    fitted, fit = fit_minimax_contraction(x, target, excess=0.02, stop_at=0.005)
    safe, certificate = certified_contraction(fitted, perturbation_budget=1e-6)
    residual = certified_max_column_residual(safe, x, target)
    if residual > Fraction(1, 100):
        raise AssertionError("simple contraction fit failed")
    # A random floating SVD is merely a proposal: exact checks certify it.
    audited = 0
    for k in (1, 2, 4, 7):
        for _ in range(3):
            candidate = project_contraction(rng.normal(size=(k, k)))
            _, info = certified_contraction(candidate, perturbation_budget=1e-6)
            assert info["certified_contraction"]
            audited += 1
    gram = x.T @ x
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    retained = eigenvalues > 1e-6
    w = eigenvectors[:, retained]
    factor = np.sqrt(eigenvalues[retained])[:, None] * w.T
    gram_error = certified_gram_factor_error(gram, factor)
    rank_certificate = certify_rank_from_probes(gram, w, 1e-6)
    if not rank_certificate:
        raise AssertionError("rank-two factor rank certificate failed")
    return {"fit": fit, "final_certificate": certificate,
            "certified_max_column_residual": float(residual),
            "random_matrix_certificates_checked": audited,
            "gram_factor_error_upper": float(gram_error),
            "rank_lower_certificate_conditional_on_eta": rank_certificate,
            "scope": "Numerical optimizer plus exact-input final certificates; no source-acquisition claim"}


if __name__ == "__main__":
    print(json.dumps(self_check(), indent=2))
