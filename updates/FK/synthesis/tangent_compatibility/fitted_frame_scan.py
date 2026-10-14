#!/usr/bin/env python3
"""Numerically fit the covariance line and moving acoustic direction.

The field and its averaged Hessian/cubic moments are generated independently
from the exact two-phase profiles in exact_tangent_triad.py.  Periodic-grid
integration is exact for these finite bandwidths; only the nonlinear
rank-one maximization and eigenvectors use floating arithmetic.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import minimize

from exact_tangent_triad import G, a, b, c, d, gradG, hessG

variables = (a, b, c, d)
G_num = sp.lambdify(variables, G, "numpy")
grad_num = sp.lambdify(variables, gradG, "numpy")
hess_num = sp.lambdify(variables, hessG, "numpy")


def make_field(N: int, p1: int, p2: int, amp: tuple[float, float, float], grid_n: int = 64):
    p3 = p1 + p2
    modes = [((p1, 1), amp[0]), ((p2, 1), amp[1]), ((p3, 2), amp[2])]
    xx = np.arange(grid_n)[:, None] / grid_n
    yy = np.arange(grid_n)[None, :] / grid_n
    fields = [np.zeros((grid_n, grid_n), dtype=float) for _ in range(4)]
    eps = 1.0 / N
    for (p, q), coeff in modes:
        phase = 2*np.pi*(p*xx + q*yy)
        smode = coeff*np.cos(phase)
        amode = eps*(p/q)*smode
        dmode = 1.5*amode
        cmode = eps*(p/q)*dmode
        for j, value in enumerate((amode, smode, cmode, dmode)):
            fields[j] += value
    return fields


def rank_one(alpha: float, beta: float) -> np.ndarray:
    u = np.array([np.cos(alpha), np.sin(alpha)])
    v = np.array([np.cos(beta), np.sin(beta)])
    return np.outer(u, v).reshape(4)


def fit_line(cov: np.ndarray) -> tuple[np.ndarray, float, float, float]:
    def objective(z):
        r = rank_one(*z)
        return -float(r @ cov @ r)
    starts = [(aa, bb) for aa in np.linspace(-0.25, 0.25, 9)
              for bb in np.linspace(np.pi/2-0.25, np.pi/2+0.25, 9)]
    best = None
    for x0 in starts:
        result = minimize(objective, np.asarray(x0), method="BFGS",
                          options={"gtol": 1e-12, "maxiter": 1000})
        if best is None or result.fun < best.fun:
            best = result
    alpha, beta = best.x
    R = rank_one(alpha, beta)
    return R, float(alpha), float(beta), float(-best.fun)


def orthogonal_basis(A: np.ndarray) -> np.ndarray:
    A = A / np.linalg.norm(A)
    seed = np.eye(4)
    Q, _ = np.linalg.qr(np.column_stack([A, *seed]))
    # QR returns A followed by an orthonormal complement; rank-deficient
    # columns can alter the first direction, so re-orthogonalize explicitly.
    Q0 = A.reshape(4, 1)
    rest = []
    for v in seed:
        w = v - Q0 @ (Q0.T @ v)
        for u in rest:
            w -= u * (u @ w)
        n = np.linalg.norm(w)
        if n > 1e-10:
            rest.append(w/n)
        if len(rest) == 3:
            break
    return np.column_stack([A, *rest])


def analyze(N: int, p1: int, p2: int, amp: tuple[float, float, float]) -> dict:
    xs = make_field(N, p1, p2, amp)
    stack = np.stack(xs)
    cov = np.einsum("ixy,jxy->ij", stack, stack) / stack.shape[1] / stack.shape[2]
    R, alpha, beta, fitval = fit_line(cov)
    s = np.einsum("i,ixy->xy", R, stack)
    Y = stack - R[:, None, None]*s[None, :, :]
    m2 = float(np.mean(s**2)); m3 = float(np.mean(s**3)); m4 = float(np.mean(s**4))
    y2 = float(np.mean(np.sum(Y**2, axis=0)))
    y4 = float(np.mean(np.sum(Y**2, axis=0)**2))
    delta2 = float(np.sqrt(y2/m2)); delta4 = float((y4/m4)**0.25)
    # Exact finite-grid averaging is valid: all frequencies have |p|<=3, |q|<=2,
    # and the grid integrates every Fourier monomial arising in a quartic.
    vals = [z.ravel() for z in stack]
    grad = np.asarray(grad_num(*vals), dtype=float)
    hess = np.asarray(hess_num(*vals), dtype=float)
    bvec = grad.mean(axis=1)
    H = hess.mean(axis=2)
    # Moving acoustic direction: least eigenvector of D^2G(R).
    MR = np.asarray(hess_num(*[np.asarray([r]) for r in R]), dtype=float)[:, :, 0]
    evals, evecs = np.linalg.eigh(MR)
    A = evecs[:, 0]
    # Change sign for stable reporting; the Schur quotient is sign-invariant.
    if A @ np.array([1., 0., 0., 1.]) < 0:
        A = -A
    Q = orthogonal_basis(A)
    Hb = Q.T @ H @ Q
    ell = bvec - (m3/(3*m2))*H@R
    eb = Q.T @ ell
    h = float(Hb[0, 0]); D = Hb[1:, 1:]; k = Hb[1:, 0]
    hstar = float(h-k @ np.linalg.solve(D, k))
    rstar = float(eb[0]-k @ np.linalg.solve(D, eb[1:]))
    eigH = np.linalg.eigvalsh(H)
    cval = float(np.mean(G_num(*vals)))
    # H is positive definite for these three-mode profiles at finite N.
    fullgap = float(cval - 0.5*bvec @ np.linalg.solve(H, bvec))
    delta = max(delta2, delta4)
    ratio = float(rstar*rstar/(hstar*m4*delta*delta)) if hstar > 1e-15 else None
    return {
        "N": N, "fitted_output_angle_rad": alpha, "fitted_input_angle_from_e2_rad": beta-np.pi/2,
        "rank_one_covariance_max": fitval, "m2": m2, "m3": m3, "m4": m4,
        "delta2": delta2, "delta4": delta4, "hstar": hstar, "rstar": rstar,
        "hstar_over_h": hstar/h, "metric_ratio": ratio,
        "min_eigen_D2G_R": float(evals[0]), "min_eigen_H": float(eigH[0]),
        "optimized_gap": fullgap, "R": R.tolist(), "A_moving": A.tolist(),
    }


def main() -> None:
    profiles = {
        "source_positive_slopes": (1, 2, (1., 1., 1.5)),
        "balanced_moving_frame": (1, -3, (2., 1., 1.)),
        "balanced_high_slope": (2, -3, (1.5, 1., 1.)),
    }
    out = {}
    for name, (p1, p2, amp) in profiles.items():
        out[name] = {str(N): analyze(N, p1, p2, amp) for N in (4, 8, 16, 32)}
    path = Path(__file__).with_name("fitted_frame_scan.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(path)


if __name__ == "__main__":
    main()
