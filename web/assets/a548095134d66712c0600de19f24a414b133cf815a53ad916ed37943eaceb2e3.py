"""Bounded Choi-HS versus normalized infinity-to-one channel-norm check.

This is a finite diagnostic of an exact all-even-dimension construction in
INITIAL.txt. It constructs the normalized Choi matrix of
    Phi_t(X) = tau(X) I + t tau(U X) V,
where U,V are traceless Hermitian unitaries and tau=Tr/d.
"""
import json
import numpy as np


def matrices(d):
    if d % 2:
        raise ValueError("d must be even")
    u = np.diag([1.0] * (d // 2) + [-1.0] * (d // 2))
    v = np.zeros((d, d), dtype=float)
    for i in range(0, d, 2):
        v[i, i + 1] = 1.0
        v[i + 1, i] = 1.0
    return u, v


def normalized_choi(d, u, v, t):
    return (np.eye(d * d) + t * np.kron(u.T, v)) / (d * d)


def run():
    t = 0.5
    rows = []
    for d in (2, 4, 8):
        u, v = matrices(d)
        j_phi = normalized_choi(d, u, v, t)
        j_dep = np.eye(d * d) / (d * d)
        min_eig = float(np.linalg.eigvalsh(j_phi).min())
        hs_gap = float(np.linalg.norm(j_phi - j_dep, ord="fro"))
        tau_u2 = float(np.trace(u @ u).real / d)
        tau_abs_v = float(np.linalg.svd(v, compute_uv=False).sum() / d)
        output = t * v
        normalized_output_trace_norm = float(np.linalg.svd(output, compute_uv=False).sum() / d)
        rows.append({
            "d": d,
            "t": t,
            "min_normalized_choi_eigenvalue": min_eig,
            "normalized_choi_trace": float(np.trace(j_phi).real),
            "normalized_choi_hilbert_schmidt_gap_to_depolarizing": hs_gap,
            "dimension_times_hs_gap": d * hs_gap,
            "tau_U_squared": tau_u2,
            "tau_abs_V": tau_abs_v,
            "normalized_trace_norm_of_(Phi_minus_depolarizing)(U)": normalized_output_trace_norm,
            "analytic_normalized_infinity_to_one_gap": t,
        })
        assert min_eig >= -1e-12
        assert abs(np.trace(j_phi).real - 1.0) < 1e-12
        assert abs(hs_gap - t / d) < 1e-12
        assert abs(normalized_output_trace_norm - t) < 1e-12
        assert abs(tau_u2 - 1.0) < 1e-12
        assert abs(tau_abs_v - 1.0) < 1e-12
    return {
        "status": "finite matrix diagnostics passed; exact all-even-dimension proof is in INITIAL.txt",
        "dimensions": [r["d"] for r in rows],
        "rows": rows,
        "scope_limit": "does not construct a selfcompatible counterexample or refute the broadcasting-to-EB target"
    }


if __name__ == "__main__":
    result = run()
    with open("work/cycle6/c04_l01/norm_interface_check.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(json.dumps(result, indent=2))
