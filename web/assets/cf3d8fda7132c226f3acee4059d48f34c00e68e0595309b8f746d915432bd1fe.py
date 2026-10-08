"""Find a finite EB Weyl comparator as a mixture of twirled product Choi states."""
from __future__ import annotations

import argparse
import json
import numpy as np
from scipy.optimize import linprog

from weyl_sdp import phase_space, symplectic


def product_twirled_features(psi: np.ndarray, d: int):
    """Return Bell weights and Weyl multipliers of Twirl(|psi><psi|⊗|psi*><psi*|)."""
    points, _ = phase_space(d)
    omega = np.exp(2j * np.pi / d)
    bells = []
    for a, b in points:
        U = np.zeros((d, d), dtype=complex)
        for j in range(d):
            U[(j + a) % d, j] = omega ** (b * j)
        ket = np.zeros(d * d, dtype=complex)
        for i in range(d):
            ket[i * d:(i + 1) * d] = U[:, i] / np.sqrt(d)
        bells.append(ket)
    bell_matrix = np.asarray(bells)
    product = np.kron(psi, psi.conjugate())
    q = np.abs(bell_matrix.conj() @ product) ** 2
    C = np.array([[np.exp(2j * np.pi * symplectic(x, z, d) / d)
                   for z in points] for x in points])
    lam = C @ q
    return q, lam


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--d", type=int, default=5)
    ap.add_argument("--seed", type=int, default=20261009)
    ap.add_argument("--dictionary-size", type=int, default=5000)
    args = ap.parse_args()
    d = args.d
    source = json.load(open(args.candidate))
    target_channel = source["best"]["lambda"]
    t = np.maximum(2 * np.asarray(target_channel) - 1, 0)
    active = np.flatnonzero(t[1:] > 1e-10) + 1

    rng = np.random.default_rng(args.seed)
    states, feature_cols, bell_cols = [], [], []
    for _ in range(args.dictionary_size):
        psi = rng.normal(size=d) + 1j * rng.normal(size=d)
        psi /= np.linalg.norm(psi)
        q, lam = product_twirled_features(psi, d)
        if np.max(np.abs(lam.imag)) > 1e-8 or np.min(lam.real) < -1e-8:
            continue
        states.append(psi)
        feature_cols.append(lam.real)
        bell_cols.append(q)
    F = np.asarray(feature_cols).T
    Q = np.asarray(bell_cols).T
    lp = linprog(c=np.ones(F.shape[1]), A_ub=-F[active], b_ub=-t[active],
                 bounds=(0, None), method="highs")
    if not lp.success:
        raise RuntimeError(lp.message)
    support = np.flatnonzero(lp.x > 1e-8)
    weights = lp.x[support]
    weights = weights / np.sum(weights)
    mu = F[:, support] @ weights
    bell_q = Q[:, support] @ weights
    payload = {
        "dimension": d,
        "construction": "convex mixture of Weyl twirls of product Choi states |psi_j><psi_j| tensor |conj(psi_j)><conj(psi_j)|",
        "channel_target_lambda": target_channel,
        "clipped_lower_bounds_t": t.tolist(),
        "dictionary": {"seed": args.seed, "sampled_product_states": args.dictionary_size,
                       "solver": "SciPy HiGHS linear programming"},
        "weights_normalized_to_sum_one": weights.tolist(),
        "product_kets": [[[float(z.real), float(z.imag)] for z in states[i]]
                         for i in support],
        "comparator_lambda": mu.tolist(),
        "comparator_bell_probabilities": bell_q.tolist(),
        "active_modes": active.tolist(),
        "minimum_active_slack": float(np.min(mu[active] - t[active])),
        "minimum_all_mode_value": float(np.min(mu[1:])),
        "weight_sum": float(np.sum(weights)),
        "support_size": int(len(support)),
        "candidate_state_indices": support.tolist(),
        "scope": "finite floating-point construction; each summand is exactly separable by construction, inequalities have numerical margin",
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(json.dumps({k: payload[k] for k in (
        "weight_sum", "support_size", "active_modes", "minimum_active_slack",
        "minimum_all_mode_value", "weights_normalized_to_sum_one",
        "comparator_lambda", "comparator_bell_probabilities")}, indent=2))


if __name__ == "__main__":
    main()

