"""Numerical candidates for fixed-law finite-data trajectory certificates.

The exact mathematical justification is in FIXED_LAW_CERTIFICATION.md.
Floating-point feasibility, rank estimates, and dual eigenvalues are diagnostics,
not formal proof objects. NumPy, SciPy, and CVXPY are required.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Sequence
import math

import cvxpy as cp
import numpy as np
from scipy.linalg import null_space


@dataclass(frozen=True)
class Measurement:
    a: Sequence[float]
    b: Sequence[float]
    u: Sequence[float] = field(default_factory=tuple)
    radius: float = 0.0


def _vector(x, dimension=None):
    out = np.asarray(x, dtype=float).reshape(-1)
    if dimension is not None and len(out) != dimension:
        raise ValueError(f"Expected dimension {dimension}, received {len(out)}")
    if not np.all(np.isfinite(out)):
        raise ValueError("Inputs must be finite")
    return out


def _solve(problem, solver="CLARABEL", solver_options=None):
    options = dict(solver_options or {})
    if solver == "CLARABEL":
        for key, value in {
            "tol_gap_abs": 1e-9,
            "tol_gap_rel": 1e-9,
            "tol_feas": 1e-9,
            "max_iter": 300,
        }.items():
            options.setdefault(key, value)
    problem.solve(solver=solver, **options)
    if problem.status not in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE}:
        raise RuntimeError(f"Optimization status: {problem.status}")


def reconstruct_gram(gram, known_basis, tolerance=1e-6):
    """Reconstruct an approximate realization and report the required dimension.

    known_basis is a d-by-r orthonormal matrix. If the numerical Schur-complement
    rank fits d-r, returned unknown vectors use the original d coordinates.
    Otherwise they use r+q abstract coordinates, with known vectors represented
    by their coordinates in known_basis. Tiny eigenvalues are discarded, and
    the resulting reconstruction error is reported explicitly.
    """
    G = np.asarray(gram, dtype=float)
    E = np.asarray(known_basis, dtype=float)
    d, r = E.shape
    B = G[:r, r:]
    D = G[r:, r:] - B.T @ B
    D = (D + D.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(D)
    scale = max(1.0, float(np.linalg.norm(G, 2)))
    keep = eigenvalues > tolerance * scale
    residual_vectors = np.sqrt(eigenvalues[keep])[:, None] * eigenvectors[:, keep].T
    q = int(keep.sum())
    abstract = np.block([
        [np.eye(r), B],
        [np.zeros((q, r)), residual_vectors],
    ])
    error = float(np.max(np.abs(abstract.T @ abstract - G)))
    fits = r + q <= d
    if fits:
        complement = null_space(E.T) if r else np.eye(d)
        unknown = (E @ B + complement[:, :q] @ residual_vectors).T
        ambient_dimension = d
    else:
        unknown = np.vstack((B, residual_vectors)).T
        ambient_dimension = r + q
    return {
        "unknown_vectors": unknown,
        "rank_estimate": r + q,
        "rank_fits_numerically": fits,
        "realization_dimension": ambient_dimension,
        "reconstruction_max_error": error,
        "schur_min_eigenvalue": float(eigenvalues.min(initial=0.0)),
        "warning": "Numerical rank and reconstructed feasibility require verification.",
    }


def solve_fixed_law(
    observations: Sequence[Measurement],
    x0,
    horizon: int,
    L: float,
    *,
    direction=None,
    reference=None,
    controls=None,
    keep_future_pairs: bool = True,
    solver="CLARABEL",
    solver_options=None,
):
    """Maximize a terminal direction or squared reference error by Gram SDP.

    Exactly one of direction/reference must be supplied. All known vectors have
    their true physical dimension d. Fixed controls have shape (horizon, m).
    Omitting controls means an autonomous map, and requires empty record controls.
    keep_future_pairs=False constructs the explicitly studied stepwise relaxation.
    The physical rank constraint is diagnosed but not imposed by this convex SDP.
    """
    if not observations:
        raise ValueError("At least one measurement is required for the trace cap")
    if horizon < 1 or not isinstance(horizon, int):
        raise ValueError("horizon must be a positive integer")
    if not math.isfinite(L) or L < 0:
        raise ValueError("L must be finite and nonnegative")
    if (direction is None) == (reference is None):
        raise ValueError("Supply exactly one of direction or reference")
    initial = _vector(x0)
    d = len(initial)
    if d < 1:
        raise ValueError("The physical dimension must be positive")
    plan = np.zeros((horizon, 0)) if controls is None else np.asarray(controls, dtype=float)
    if plan.ndim != 2 or plan.shape[0] != horizon or not np.all(np.isfinite(plan)):
        raise ValueError("controls must be a finite horizon-by-m array")
    m = plan.shape[1]
    data = []
    for obs in observations:
        a, b, u = _vector(obs.a, d), _vector(obs.b, d), _vector(obs.u, m)
        eta = float(obs.radius)
        if not math.isfinite(eta) or eta < 0:
            raise ValueError("Output-error radii must be finite and nonnegative")
        data.append((a, b, u, eta))
    target = _vector(direction if direction is not None else reference, d)
    known = np.column_stack([initial, target] + [vec for a, b, _, _ in data for vec in (a, b)])
    U, singular_values, _ = np.linalg.svd(known, full_matrices=False)
    basis_tolerance = np.finfo(float).eps * max(known.shape) * singular_values.max(initial=0.0)
    r = int(np.count_nonzero(singular_values > basis_tolerance))
    E = U[:, :r]
    noisy = [i for i, (_, _, _, eta) in enumerate(data) if eta > 0]
    noisy_index = {record: horizon + j for j, record in enumerate(noisy)}
    K = horizon + len(noisy)
    size = r + K

    def known_coeff(vector):
        coeff = np.zeros(size)
        coeff[:r] = E.T @ vector
        return coeff

    def unknown_coeff(index):
        coeff = np.zeros(size)
        coeff[r + index] = 1
        return coeff

    xs = [known_coeff(initial)] + [unknown_coeff(t) for t in range(horizon)]
    outputs = [unknown_coeff(noisy_index[i]) if i in noisy_index else known_coeff(b)
               for i, (_, b, _, _) in enumerate(data)]
    graph = [(known_coeff(a), u, outputs[i], f"data:{i}")
             for i, (a, _, u, _) in enumerate(data)]
    graph += [(xs[t], plan[t], xs[t + 1], f"future:{t}") for t in range(horizon)]
    matrices, right_sides, labels = [], [], []
    for i, j in combinations(range(len(graph)), 2):
        if not keep_future_pairs and i >= len(data) and j >= len(data):
            continue
        p, u, y, ilabel = graph[i]
        q, v, z, jlabel = graph[j]
        dx, dy = p - q, y - z
        matrices.append(np.outer(dy, dy) - L * L * np.outer(dx, dx))
        right_sides.append(L * L * float(np.dot(u - v, u - v)))
        labels.append(f"{ilabel}/{jlabel}")
    for i in noisy:
        delta = outputs[i] - known_coeff(data[i][1])
        matrices.append(np.outer(delta, delta))
        right_sides.append(data[i][3] ** 2)
        labels.append(f"output_error:{i}")

    # Any record proves a valid cap. Choose the tightest of these simple caps.
    caps = []
    for a, b, u, eta in data:
        radius = float(np.linalg.norm(initial))
        cap = float(r)
        for t in range(horizon):
            radius = float(np.linalg.norm(b)) + eta + L * (
                radius + float(np.linalg.norm(a)) + float(np.linalg.norm(plan[t] - u)))
            cap += radius * radius
        cap += sum((float(np.linalg.norm(data[i][1])) + data[i][3]) ** 2 for i in noisy)
        caps.append(cap)
    trace_cap = min(caps)

    G = cp.Variable((size, size), symmetric=True)
    psd_constraint = G >> 0
    constraints = [psd_constraint]
    anchor_constraint = G[:r, :r] == np.eye(r) if r else None
    if anchor_constraint is not None:
        constraints.append(anchor_constraint)
    inequalities = [cp.sum(cp.multiply(A, G)) <= b for A, b in zip(matrices, right_sides)]
    constraints += inequalities
    trace_constraint = cp.trace(G) <= trace_cap
    constraints.append(trace_constraint)
    if direction is not None:
        c = known_coeff(target)
        C = (np.outer(c, xs[-1]) + np.outer(xs[-1], c)) / 2
    else:
        delta = xs[-1] - known_coeff(target)
        C = np.outer(delta, delta)
    objective = cp.Maximize(cp.sum(cp.multiply(C, G)))
    problem = cp.Problem(objective, constraints)
    _solve(problem, solver, solver_options)
    gram = np.asarray(G.value)
    gram = (gram + gram.T) / 2
    lam = np.asarray([float(c.dual_value) for c in inequalities])
    rho = float(trace_constraint.dual_value)
    Y = np.asarray(anchor_constraint.dual_value) if r else np.zeros((0, 0))
    S = rho * np.eye(size) - C
    S[:r, :r] += (Y + Y.T) / 2
    for multiplier, matrix in zip(lam, matrices):
        S += multiplier * matrix
    S = (S + S.T) / 2
    dual_objective = float(np.trace(Y) + lam @ np.asarray(right_sides) + rho * trace_cap)
    residuals = np.asarray([np.sum(A * gram) - b for A, b in zip(matrices, right_sides)])
    realization = reconstruct_gram(gram, E)
    return {
        "status": problem.status,
        "value": float(problem.value),
        "gram": gram,
        "known_basis": E,
        "known_span_dimension": r,
        "unknown_vector_count": K,
        "physical_dimension": d,
        "interpolation_and_noise_constraint_count": len(matrices),
        "trace_cap": trace_cap,
        "gram_min_eigenvalue": float(np.linalg.eigvalsh(gram).min()),
        "maximum_constraint_violation": float(max(0.0, residuals.max(initial=0.0))),
        "anchor_max_error": float(np.max(np.abs(gram[:r, :r] - np.eye(r)), initial=0.0)),
        "trace_violation": max(0.0, float(np.trace(gram) - trace_cap)),
        "dual_objective_candidate": dual_objective,
        "dual_min_eigenvalue": float(np.linalg.eigvalsh(S).min()),
        "dual_nonnegative_multiplier_min": float(min(rho, lam.min(initial=math.inf))),
        "duality_gap_candidate": dual_objective - float(problem.value),
        "dual_multipliers": lam,
        "dual_anchor": Y,
        "dual_trace_multiplier": rho,
        "dual_slack": S,
        "constraint_labels": labels,
        "constraint_matrices": matrices,
        "constraint_right_sides": right_sides,
        "realization": realization,
        "future_vectors": realization["unknown_vectors"][:horizon],
        "warning": "Floating-point primal and dual candidates, not formal certificates; physical rank is not imposed.",
    }


def equilibrium_balls(observations: Sequence[Measurement], L: float):
    """Exact algebraic ball formula; numerical evaluation, autonomous exact data."""
    if not observations or not 0 <= L < 1:
        raise ValueError("At least one observation and 0 <= L < 1 are required")
    d = len(observations[0].a)
    centers, radii = [], []
    for obs in observations:
        if obs.radius != 0 or len(obs.u) != 0:
            raise ValueError("This helper requires exact autonomous observations")
        a, b = _vector(obs.a, d), _vector(obs.b, d)
        centers.append((b - L * L * a) / (1 - L * L))
        radii.append(L * float(np.linalg.norm(b - a)) / (1 - L * L))
    for i, j in combinations(range(len(observations)), 2):
        a, b = _vector(observations[i].a), _vector(observations[i].b)
        c, e = _vector(observations[j].a), _vector(observations[j].b)
        if np.linalg.norm(b - e) > L * np.linalg.norm(a - c) + 1e-12:
            raise ValueError("Observed graph violates the supplied Lipschitz bound")
    return np.asarray(centers), np.asarray(radii)


def solve_equilibrium(observations, L, direction, solver="CLARABEL", solver_options=None):
    centers, radii = equilibrium_balls(observations, L)
    c = _vector(direction, centers.shape[1])
    x = cp.Variable(centers.shape[1])
    constraints = [cp.norm(x - center) <= radius for center, radius in zip(centers, radii)]
    problem = cp.Problem(cp.Maximize(c @ x), constraints)
    _solve(problem, solver, solver_options)
    return {
        "value": float(problem.value),
        "point": np.asarray(x.value),
        "centers": centers,
        "radii": radii,
        "status": problem.status,
        "maximum_constraint_violation": float(max(0.0, np.max(np.linalg.norm(x.value - centers, axis=1) - radii))),
        "warning": "Numerical SOCP candidate; a checked bound is needed for a formal conclusion.",
    }


def contraction_radius(observation: Measurement, x0, L):
    if observation.radius != 0 or len(observation.u) != 0 or not 0 <= L < 1:
        raise ValueError("Exact autonomous observation and 0 <= L < 1 required")
    a, b, initial = _vector(observation.a), _vector(observation.b), _vector(x0)
    return float(np.linalg.norm(initial - a) + np.linalg.norm(b - a) / (1 - L))


def tail_horizon(L, kappa, radius, epsilon):
    """Sufficient prefix H so kappa*radius*L**(H+1) <= epsilon."""
    if not 0 <= L < 1 or min(kappa, radius) < 0 or epsilon <= 0:
        raise ValueError("Require 0 <= L < 1, nonnegative bounds, positive epsilon")
    if L == 0 or kappa * radius <= epsilon:
        return 0
    return max(0, math.ceil(math.log(kappa * radius / epsilon) / -math.log(L)) - 1)


def vector_envelope(L):
    if L < 0:
        raise ValueError("L must be nonnegative")
    return -1 + L * (1 + L) / (1 + 2 * L) if L <= 0.5 else L * L - 7 / 8


def scalar_envelope(L):
    if L < 0:
        raise ValueError("L must be nonnegative")
    phi = (1 + math.sqrt(5)) / 2
    return -1 + L * (1 + L) / (1 + 2 * L) if L <= phi else L * L - L - 1


def scalar_t_attainer(x, L):
    """The globally Lipschitz piecewise map attaining t(L), for every L>=0."""
    if L < 0:
        raise ValueError("L must be nonnegative")
    if L == 0:
        return -1.0
    s = -(1 + L) / (1 + 2 * L)
    t = -1 + L * (1 + L) / (1 + 2 * L)
    if x <= -1:
        return s
    if x <= s:
        return s + L * (x + 1)
    if x <= 0:
        return t - L * (x - s)
    return -1.0


def vector_attainer(x, L):
    """Explicit two-dimensional sharp attaining map, e=(1,0)."""
    x = _vector(x, 2)
    if L <= 0.5:
        return np.array([scalar_t_attainer(x[0], L), 0.0])
    cosine = -1 / (4 * L)
    sine = -math.sqrt(1 - cosine * cosine)
    Q = np.array([[cosine, -sine], [sine, cosine]])
    return L * Q @ x - np.array([1.0, 0.0])
