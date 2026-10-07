"""Finite diagnostics for the exact EB/selfcompatible norm-separation family.

The all-even-dimension proof is in REVISION-02.txt. This checks the normalized
Choi formulas, product-preparation broadcaster, its marginals, and the witness
norms at d=2 and d=4. The PSD proof is structural: the Choi matrix is a sum of
positive product operators.
"""
import json
import numpy as np


def matrices(d):
    if d % 2:
        raise ValueError("d must be even")
    u = np.diag([1.0] * (d // 2) + [-1.0] * (d // 2))
    v = np.zeros((d, d), dtype=float)
    for i in range(0, d, 2):
        v[i, i + 1] = v[i + 1, i] = 1.0
    return u, v


def partial_trace_channel_choi(joint, d, keep):
    # Choi register order: input, first output, second output.
    t = joint.reshape(d, d, d, d, d, d)
    if keep == "first":
        return np.einsum("ibcjBc->ibjB", t)
    if keep == "second":
        return np.einsum("ibcjbC->icjC", t)
    raise ValueError(keep)


def run():
    t = 0.5
    rows = []
    for d in (2, 4):
        u, v = matrices(d)
        ident = np.eye(d)
        effects = [(ident + u) / 2, (ident - u) / 2]
        states = [(ident + t * v) / d, (ident - t * v) / d]

        # Normalized Choi matrix for Phi_t, with |Omega> normalized.
        j_phi = (np.kron(ident, ident) + t * np.kron(u.T, v)) / d**2

        # A(X)=sum_s Tr(P_s X) sigma_s tensor sigma_s.
        # Its normalized Choi is (1/d) sum_s P_s^T tensor sigma_s tensor sigma_s.
        j_joint = sum(
            np.kron(e.T, np.kron(s, s)) / d
            for e, s in zip(effects, states)
        )
        j_first = partial_trace_channel_choi(j_joint, d, "first").reshape(d * d, d * d)
        j_second = partial_trace_channel_choi(j_joint, d, "second").reshape(d * d, d * d)
        input_marginal = np.einsum(
            "ibcjbc->ij", j_joint.reshape(d, d, d, d, d, d)
        )

        min_eig_phi = float(np.linalg.eigvalsh(j_phi).min())
        min_eig_joint = float(np.linalg.eigvalsh(j_joint).min())
        hs_gap = float(np.linalg.norm(j_phi - np.eye(d * d) / d**2, ord="fro"))
        # Exact norm witness X=U: (Phi-D)(U)=tV, tau(|V|)=1.
        witness_gap = float(np.linalg.svd(t * v, compute_uv=False).sum() / d)
        rows.append({
            "d": d,
            "t": t,
            "phi_choi_min_eigenvalue": min_eig_phi,
            "joint_choi_min_eigenvalue": min_eig_joint,
            "joint_choi_trace": float(np.trace(j_joint).real),
            "joint_input_marginal_max_error": float(np.max(np.abs(input_marginal - ident / d))),
            "first_marginal_choi_max_error": float(np.max(np.abs(j_first - j_phi))),
            "second_marginal_choi_max_error": float(np.max(np.abs(j_second - j_phi))),
            "choi_hilbert_schmidt_gap_to_depolarizing": hs_gap,
            "expected_choi_gap_t_over_d": t / d,
            "full_ball_norm_witness_gap": witness_gap,
            "expected_full_ball_gap_t": t,
        })
        assert min_eig_phi >= -1e-12 and min_eig_joint >= -1e-12
        assert abs(np.trace(j_joint).real - 1) < 1e-12
        assert np.max(np.abs(input_marginal - ident / d)) < 1e-12
        assert np.max(np.abs(j_first - j_phi)) < 1e-12
        assert np.max(np.abs(j_second - j_phi)) < 1e-12
        assert abs(hs_gap - t / d) < 1e-12
        assert abs(witness_gap - t) < 1e-12
    return {
        "status": "bounded diagnostics passed; exact formulas/proofs are in REVISION-02.txt",
        "dimensions": [r["d"] for r in rows],
        "rows": rows,
        "scope_limit": "the channel is itself EB; this is a norm-transfer obstruction, not a failure of EB rounding"
    }


if __name__ == "__main__":
    result = run()
    path = "work/cycle6/c04_l01/revisions/norm_interface_selfcompatible_check.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(json.dumps(result, indent=2))
