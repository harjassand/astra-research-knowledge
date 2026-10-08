"""Finite diagnostic for a boundary-penalized mechanical SSH chain."""
import json
import numpy as np

N = 40
KAPPAS = [1e-5, 1e-4, 1e-3, 1e-2]
GAP = (1.0 - 0.4) ** 2


def run(q1, q2):
    C = np.zeros((N - 1, N), dtype=float)
    for i in range(N - 1):
        C[i, i] = q1
        C[i, i + 1] = q2
    H0 = C.T @ C

    ratio = q1 / q2
    if abs(ratio) <= 1:
        u = (-ratio) ** np.arange(N, dtype=float)
    else:
        u = (-1.0 / ratio) ** np.arange(N - 1, -1, -1, dtype=float)
    u /= np.linalg.norm(u)
    p0 = u[0] ** 2 + u[-1] ** 2
    e_left = np.zeros(N)
    e_right = np.zeros(N)
    e_left[0] = 1.0
    e_right[-1] = 1.0
    P = np.outer(e_left, e_left) + np.outer(e_right, e_right)

    results = []
    for kappa in KAPPAS:
        vals, vecs = np.linalg.eigh(H0 + kappa * P)
        low_vec = vecs[:, 0]
        c_left = float(e_left @ np.linalg.solve(H0 + kappa * P, e_left))
        c_right = float(e_right @ np.linalg.solve(H0 + kappa * P, e_right))
        results.append({
            "kappa": kappa,
            "lambda1": float(vals[0]),
            "lambda1_over_kappa": float(vals[0] / kappa),
            "predicted_slope": float(p0),
            "slope_relative_error": float(abs(vals[0] / kappa - p0) / p0),
            "lambda2": float(vals[1]),
            "lambda2_minus_gap": float(vals[1] - GAP),
            "abs_mode_overlap": float(abs(low_vec @ u)),
            "davis_kahan_bound_2k_over_gap": float(2 * kappa / GAP),
            "left_stiffness": float(1.0 / c_left),
            "right_stiffness": float(1.0 / c_right),
            "right_over_left_stiffness": float(c_left / c_right),
        })
    return {
        "q1": q1,
        "q2": q2,
        "winding_regime": "q2>q1; left soft mode" if q2 > q1 else "q1>q2; right soft mode",
        "null_mode_endpoint_weights": {"left": float(u[0] ** 2), "right": float(u[-1] ** 2)},
        "penalty_overlap": float(p0),
        "ideal_nonzero_gap_lower_bound": GAP,
        "results": results,
    }


out = {
    "N": N,
    "penalty": "kappa at both endpoints",
    "cases": [run(0.4, 1.0), run(1.0, 0.4)],
}
print(json.dumps(out, indent=2))
