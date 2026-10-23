#!/usr/bin/env python3
"""Supplementary checks of the fan obstruction; the analytic proof is RESULT.txt.

Run with one BLAS thread and a 45-second process limit. No external inputs,
network, installations, or writes outside this file's directory are used.
"""
import json
import math
import pathlib
import resource
import time
from fractions import Fraction as F

resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
resource.setrlimit(resource.RLIMIT_CPU, (40, 40))
START_WALL = time.perf_counter()
START_CPU = time.process_time()
import numpy as np


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def exact_rational_check():
    """Exactly check flow, two constraints, support, and lift over Q."""
    z = [[F(1, 4), F(1, 8)], [F(1, 8), F(3, 8)],
         [F(-1, 4), F(1, 8)], [F(-1, 8), F(-1, 4)],
         [F(1, 4), F(-1, 8)]]
    t = [F(1, 8), F(-1, 4), F(3, 16), F(1, 4), F(-1, 8)]
    r0 = F(1, 2)
    m = len(z)
    r2 = [sum(q*q for q in row) for row in z]
    perp = [[-row[1]/r, row[0]/r] for row, r in zip(z, r2)]
    h = [[t[i]*perp[i][a]-t[i+1]*perp[i+1][a]
          for i in range(m-1)] for a in range(2)]
    # A rational null vector of the first three columns of the constraint map.
    p, q = h[0][:3], h[1][:3]
    alpha = [p[1]*q[2]-p[2]*q[1], p[2]*q[0]-p[0]*q[2],
             p[0]*q[1]-p[1]*q[0]]
    assert any(alpha)
    c = alpha + [F(0)]
    assert all(sum(h[a][j]*c[j] for j in range(m-1)) == 0
               for a in range(2))
    determinants = [z[i][0]*z[i+1][1]-z[i][1]*z[i+1][0]
                    for i in range(m-1)]
    assert all(determinants)
    b = [ci/di for ci, di in zip(c, determinants)]
    B = [[F(0) for _ in range(m)] for _ in range(m)]
    for i, bi in enumerate(b):
        B[i][i+1] = B[i+1][i] = bi
    for i in range(m):
        B[i][i] = -sum(B[i][j]*sum(z[i][a]*z[j][a] for a in range(2))
                       for j in range(m) if j != i)/r2[i]
    padded = [F(0)] + c + [F(0)]
    expected = [[(padded[i+1]-padded[i])*perp[i][a] for a in range(2)]
                for i in range(m)]
    assert matmul(B, z) == expected
    assert all(sum(t[i]*expected[i][a] for i in range(m)) == 0
               for a in range(2))
    L = [[-ti/r0 for ti in t]] + [[F(int(i == j)) for j in range(m)]
                                       for i in range(m)]
    D = matmul(matmul(L, B), transpose(L))
    X = [[F(0), F(0), r0]] + [zi+[ti] for zi, ti in zip(z, t)]
    DX = matmul(D, X)
    assert DX[0] == [0, 0, 0]
    assert DX[1:] == [row+[F(0)] for row in expected]
    assert D == transpose(D)
    assert all(D[i][j] == 0 for i in range(1, m+1)
               for j in range(1, m+1) if abs(i-j) > 1)
    assert all(sum(q*q for q in row) <= 1 for row in X)
    assert any(v for row in D for v in row)
    assert any(v for row in DX for v in row)
    return {"passed": True, "arithmetic": "fractions.Fraction (exact rational)",
            "m": m, "claims_checked": ["row caps", "nonzero adjacent determinants",
              "nonzero two-constraint kernel", "path flow identity", "zero apex action",
              "lifted support", "symmetry", "nonzero witness", "nonzero action"],
            "note": "This exact check does not check a sine-mode energy inequality; that identity is proved analytically."}


def numerical_witness(X):
    m = len(X)-1
    r0 = np.linalg.norm(X[0])
    u = X[0]/r0
    axis = np.eye(3)[np.argmin(np.abs(u))]
    e1 = np.cross(u, axis)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(u, e1)
    U = np.column_stack((e1, e2))
    Z = X[1:] @ U
    t = X[1:] @ u
    r2 = np.sum(Z*Z, axis=1)
    delta = math.sqrt(float(np.min(r2)))
    determinants = Z[:-1, 0]*Z[1:, 1]-Z[:-1, 1]*Z[1:, 0]
    assert np.min(np.abs(determinants)) > 1e-12
    modes = np.sin(np.pi*np.arange(1, m)[:, None]*np.arange(1, 4)[None, :]/m)
    differences = np.diff(np.vstack((np.zeros((1, 3)), modes, np.zeros((1, 3)))), axis=0)
    perp = np.column_stack((-Z[:, 1], Z[:, 0])) / r2[:, None]
    H = np.array([t @ (differences[:, k, None]*perp) for k in range(3)]).T
    alpha = np.linalg.svd(H, full_matrices=True)[2][-1]
    c = modes @ alpha
    dc = np.diff(np.r_[0., c, 0.])
    b = c / determinants
    B = np.diag(b, 1)+np.diag(b, -1)
    dots = np.sum(Z[:-1]*Z[1:], axis=1)
    diagonal_numerator = np.r_[b*dots, 0.]+np.r_[0., b*dots]
    np.fill_diagonal(B, -diagonal_numerator/r2)
    D = np.zeros((m+1, m+1))
    D[1:, 1:] = B
    D[0, 1:] = D[1:, 0] = -(B @ t)/r0
    D[0, 0] = t @ B @ t/r0**2
    DX = D @ X
    predicted = np.zeros_like(DX)
    predicted[1:] = (dc[:, None]*perp) @ U.T
    scale = max(1., np.linalg.norm(D)*np.linalg.norm(X))
    identity_error = np.linalg.norm(DX-predicted)/scale
    assert identity_error < 2e-13
    action_norm = np.linalg.norm(DX)
    op_norm = np.max(np.abs(np.linalg.eigvalsh(D)))
    ratio = op_norm/action_norm
    Q = 1/(2*np.sqrt(m-1)*np.sin(3*np.pi/(2*m)))
    assert ratio >= delta*Q*(1-1e-8)
    low_mode_energy = np.sum(dc*dc)/np.sum(c*c)
    spectral_upper = 4*np.sin(3*np.pi/(2*m))**2
    assert low_mode_energy <= spectral_upper*(1+1e-12)
    local_i = int(np.argmin(r2))
    w = np.zeros(m+1)
    w[local_i+1] = 1
    w[0] = -t[local_i]/r0
    local_ratio = np.linalg.norm(w)/delta
    combined_ratio = max(local_ratio, ratio)
    theorem_bound = max(1., np.sqrt(Q))
    assert combined_ratio >= theorem_bound*(1-1e-8)
    return {"m": m, "delta": delta, "minimum_abs_projected_determinant": float(np.min(np.abs(determinants))),
            "scaled_identity_error": float(identity_error),
            "apex_action_norm": float(np.linalg.norm(DX[0])),
            "flow_operator_ratio": float(ratio), "local_operator_ratio": float(local_ratio),
            "theorem_lower_bound": float(theorem_bound),
            "flow_energy": float(low_mode_energy), "flow_energy_upper": float(spectral_upper)}


def numerical_checks():
    rng = np.random.default_rng(20261021)
    results = []
    for m in (4, 5, 8, 16, 32, 64, 128):
        # A completely dense design with unequal row norms.
        X = rng.normal(size=(m+1, 3))
        X /= np.linalg.norm(X, axis=1)[:, None]
        X *= rng.uniform(0.25, 1, size=(m+1, 1))
        result = numerical_witness(X)
        result["design"] = "dense_random_unequal_norms"
        results.append(result)
        # The projected directions may nearly approach the apex direction.
        theta = np.arange(m)*np.pi*0.419 + 0.13
        Z = np.column_stack((np.cos(theta), np.sin(theta)))
        radii = rng.uniform(0.15, 0.6, m)
        radii[m//2] = 0.01
        t = rng.uniform(-0.5, 0.5, m)
        X = np.vstack(([0., 0., 0.7], np.column_stack((Z*radii[:, None], t))))
        result = numerical_witness(X)
        result["design"] = "small_projection_with_nonzero_apex_parallel_components"
        results.append(result)
        # Zero parallel components make the apex constraint map have rank zero.
        X[1:, 2] = 0
        result = numerical_witness(X)
        result["design"] = "rank_zero_apex_constraint"
        results.append(result)
    return results


def degeneracy_checks():
    X = np.array([[0., 0., 1.], [.5, 0., 0.], [.3, 0., .4], [0., .5, 0.]])
    # x_2 = .6 x_1 + .4 x_0: the first triangle is dependent.
    w = np.array([-.4, -.6, 1., 0.])
    D = np.outer(w, w)
    assert np.linalg.norm(D @ X) < 1e-15
    assert np.linalg.norm(D) > 0
    X0 = X.copy()
    X0[0] = 0
    diagonal = np.diag([1., 0., 0., 0.])
    assert np.all(diagonal @ X0 == 0)
    return {"passed": True, "cases": ["dependent triangle rank-one kernel", "zero apex diagonal kernel"]}


def main():
    out = {"role": "Supplementary algebra checks; no finite experiment substitutes for the all-design proof.",
           "exact_rational": exact_rational_check(),
           "degenerate_cases": degeneracy_checks(),
           "numerical_cases": numerical_checks(),
           "failed_checks": [],
           "resource_limits": {"address_space_bytes": 1 << 30, "cpu_seconds": 40}}
    out["wall_seconds"] = time.perf_counter()-START_WALL
    out["cpu_seconds"] = time.process_time()-START_CPU
    path = pathlib.Path(__file__).with_name("CHECKS.json")
    path.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"passed": True, "exact_rational": True,
                      "numerical_case_count": len(out["numerical_cases"]),
                      "wall_seconds": out["wall_seconds"], "cpu_seconds": out["cpu_seconds"]}))


if __name__ == "__main__":
    main()
