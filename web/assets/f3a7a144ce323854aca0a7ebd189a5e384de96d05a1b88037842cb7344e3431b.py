"""Finite-field Weyl-channel self-compatibility SDP from Haapasalo (2019)."""
from __future__ import annotations

import numpy as np
import cvxpy as cp


def phase_space(d: int):
    points = [(a, b) for a in range(d) for b in range(d)]
    index = {v: i for i, v in enumerate(points)}
    return points, index


def symplectic(x, y, d):
    return (x[0] * y[1] - x[1] * y[0]) % d


def data(d: int):
    points, index = phase_space(d)
    n = d * d
    # F[m,n,r] = exp(2 pi i S(m-n,r)/d), the kernel in Haapasalo,
    # Corollary 2, equation (22).
    F = np.empty((n, n, n), dtype=complex)
    for i, m in enumerate(points):
        for j, z in enumerate(points):
            delta = ((m[0] - z[0]) % d, (m[1] - z[1]) % d)
            for k, r in enumerate(points):
                F[i, j, k] = np.exp(2j * np.pi * symplectic(delta, r, d) / d)
    # Character table of the random-Weyl channel's action on Weyl modes.
    C = np.empty((n, n), dtype=complex)
    for ix, x in enumerate(points):
        for ir, r in enumerate(points):
            C[ix, ir] = np.exp(2j * np.pi * symplectic(x, r, d) / d)
    return points, index, F, C


def compatibility_sdp(d: int, solver="SCS", eps=2e-7, max_iters=200000,
                      hs_positive=False):
    """Build an SDP for self-adjoint self-compatible Weyl channels.

    Variables are q (the Weyl error law) and X=diag(sqrt(q))*beta*diag(sqrt(q)),
    where beta is the unit-diagonal positive kernel in Corollary 2. Thus X >= 0,
    diag(X)=q, and the compatibility equation is affine in X. Requiring q=q'
    gives self-compatibility. q[-r]=q[r] and all Fourier modes >=0 impose the
    self-adjoint subclass; set hs_positive=True to additionally require every
    Weyl eigenvalue nonnegative.
    """
    points, index, F, C = data(d)
    n = d * d
    X = cp.Variable((n, n), hermitian=True)
    q = cp.Variable(n)
    lam = cp.Variable(n)
    constraints = [X >> 0, q >= 0, cp.diag(X) == q, cp.sum(q) == 1]
    compat = []
    for r in range(n):
        compat.append(cp.real(cp.sum(cp.multiply(F[:, :, r], X))) / (d * d))
    constraints += [q == cp.hstack(compat)]
    for i, r in enumerate(points):
        minus = ((-r[0]) % d, (-r[1]) % d)
        constraints.append(q[i] == q[index[minus]])
    constraints += [lam == cp.real(C @ q), lam[index[(0, 0)]] == 1]
    if hs_positive:
        constraints += [lam >= 0]
    direction_parameter = cp.Parameter(n)
    problem = cp.Problem(cp.Maximize(direction_parameter @ lam), constraints)

    def solve(direction, extra=(), warm_start=True):
        """Maximize a real linear combination of lambda over compatible maps."""
        direction_parameter.value = np.asarray(direction, dtype=float)
        if extra:
            # Used only for fixed-channel feasibility fixtures; no objective sweep.
            fixed_problem = cp.Problem(problem.objective, constraints + list(extra))
            fixed_problem.solve(solver=solver, eps=eps, max_iters=max_iters,
                                warm_start=warm_start, verbose=False)
            result = fixed_problem
        else:
            problem.solve(solver=solver, eps=eps, max_iters=max_iters,
                          warm_start=warm_start, verbose=False)
            result = problem
        if result.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
            raise RuntimeError(f"solver status {result.status}")
        return {
            "status": result.status,
            "value": float(result.value),
            "q": np.array(q.value).reshape(-1),
            "lambda": np.array(lam.value).reshape(-1),
            "X": np.array(X.value),
            "solver_stats": {
                "name": solver,
                "num_iters": getattr(result.solver_stats, "num_iters", None),
                "solve_time": getattr(result.solver_stats, "solve_time", None),
            },
        }

    return points, index, q, lam, solve


def line_system(d: int):
    """Return the d+1 projective lines as indices of nonzero Weyl labels."""
    points, index = phase_space(d)
    lines = []
    for slope in range(d):
        lines.append([index[(a, slope * a % d)] for a in range(1, d)])
    lines.append([index[(0, b)] for b in range(1, d)])
    return lines


def line_cover(lambdas, lines):
    peaks = [max(float(lambdas[i]) for i in line) for line in lines]
    contributions = [max(0.0, 2 * peak - 1) for peak in peaks]
    return float(sum(contributions)), peaks, contributions
