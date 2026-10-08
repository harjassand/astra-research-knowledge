#!/usr/bin/env python3
"""Eight-state, two-dimensional full-state version of the moment alias.

This companion check addresses the interpretation where “full observable
state” means a vector state x in R^2 rather than one scalar coordinate. For
d=2 there are 5 first/second-moment constraints per source. Seven generic
states give 6 outgoing rates/source and a nontrivial exact integer nullspace;
this is the minimum generic state count in two dimensions.

Run from the workspace root:
  python3 work/agents/cell_control/cell_observation_design/cycle3_full_vector_witness.py
"""
from __future__ import annotations

import itertools
import json
import math

import numpy as np

from cycle2_rate_separation import expm


X = np.array(
    [[0, 0], [1, 0], [0, 1], [1, 1], [2, 0], [0, 2], [2, 2]],
    dtype=float,
)
K = len(X)
DESTS = [[j for j in range(K) if j != i] for i in range(K)]
DELTA_0 = np.array(
    [
        [4, 4, -4, -1, -1, 1],
        [-3, 4, -4, -1, -1, 1],
        [-3, 4, -4, -1, -1, 1],
        [-3, 4, 4, -1, -1, 1],
        [-3, 4, 4, -4, -1, 1],
        [-3, 4, 4, -4, -1, 1],
        [3, -4, -4, 4, 1, 1],
    ],
    dtype=float,
)
DELTA_1 = DELTA_0.copy()


def generator(rates: np.ndarray) -> np.ndarray:
    q = np.zeros((K, K), dtype=float)
    for i, dests in enumerate(DESTS):
        for j, rate in zip(dests, rates[i]):
            q[j, i] = rate
        q[i, i] = -np.sum(rates[i])
    return q


def drift_cov(q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    b = np.zeros((K, 2))
    a = np.zeros((K, 2, 2))
    for i, dests in enumerate(DESTS):
        for j in dests:
            z = X[j] - X[i]
            rate = q[j, i]
            b[i] += rate * z
            a[i] += rate * np.outer(z, z)
    return b, a


def moment_design(source: int) -> np.ndarray:
    cols = []
    for dest in DESTS[source]:
        z = X[dest] - X[source]
        cols.append([z[0], z[1], z[0] ** 2, z[0] * z[1], z[1] ** 2])
    return np.asarray(cols, dtype=float).T


def word_law(q0: np.ndarray, q1: np.ndarray, e: np.ndarray, pi: np.ndarray, tau: float) -> np.ndarray:
    p0 = expm(q0 * tau)
    p1 = expm(q1 * tau)
    out = np.zeros((K, K, K))
    for i, j, k in itertools.product(range(K), repeat=3):
        out += pi[i] * p0[j, i] * p1[k, j] * np.einsum("a,b,c->abc", e[:, i], e[:, j], e[:, k])
    return out


def main() -> None:
    rates0_a = np.ones((K, K - 1))
    rates1_a = np.array(
        [
            [1.1, 0.8, 1.2, 0.9, 1.3, 0.7],
            [0.8, 1.3, 0.7, 1.1, 0.9, 1.4],
            [1.4, 0.8, 1.2, 0.9, 1.1, 0.7],
            [0.9, 1.2, 0.8, 1.4, 0.7, 1.1],
            [1.3, 0.7, 1.1, 0.8, 1.4, 1.0],
            [0.7, 1.4, 0.9, 1.2, 0.8, 1.3],
            [1.2, 0.9, 1.4, 0.7, 1.1, 0.8],
        ],
        dtype=float,
    )
    rates0_b = rates0_a + 0.05 * DELTA_0
    rates1_b = rates1_a + 0.025 * DELTA_1
    qa = [generator(rates0_a), generator(rates1_a)]
    qb = [generator(rates0_b), generator(rates1_b)]
    assert min(float(np.min(z)) for z in (rates0_a, rates1_a, rates0_b, rates1_b)) > 0.0
    ba = [drift_cov(q) for q in qa]
    bb = [drift_cov(q) for q in qb]
    moment_gaps = [
        {
            "drift_sup": float(np.max(np.abs(ba[a][0] - bb[a][0]))),
            "covariance_sup": float(np.max(np.abs(ba[a][1] - bb[a][1]))),
        }
        for a in range(2)
    ]
    assert max(max(v.values()) for v in moment_gaps) < 1e-11
    ranks = [int(np.linalg.matrix_rank(moment_design(i))) for i in range(K)]
    null_dims = [K - 1 - rank for rank in ranks]
    assert ranks == [5] * K and null_dims == [1] * K

    tau = 0.1
    e = 0.8 * np.eye(K) + (0.2 / K) * np.ones((K, K))
    pi = np.full(K, 1.0 / K)
    law_a = word_law(qa[0], qa[1], e, pi, tau)
    law_b = word_law(qb[0], qb[1], e, pi, tau)
    law_l1 = float(np.abs(law_a - law_b).sum())
    tv = law_l1 / 2.0
    n_simple_known_nuisance = math.ceil(2.0 / tv**2 * math.log(1.0 / 0.05))
    min_sv = float(np.linalg.svd(e, compute_uv=False)[-1])
    tau_norm = max(float(np.linalg.norm(q, 1)) for q in qa + qb) * tau
    assert law_l1 > 1e-8 and tau_norm < math.pi

    pa = [expm(q * tau) for q in qa]
    pb = [expm(q * tau) for q in qb]
    best_q_gap = math.inf
    best_p_gap = math.inf
    for perm in itertools.permutations(range(K)):
        s = np.eye(K)[:, perm]
        q_gap = sum(np.linalg.norm(qa[a] - s.T @ qb[a] @ s, ord="fro") for a in range(2))
        p_gap = sum(np.linalg.norm(pa[a] - s.T @ pb[a] @ s, ord="fro") for a in range(2))
        best_q_gap = min(best_q_gap, float(q_gap))
        best_p_gap = min(best_p_gap, float(p_gap))

    out = {
        "state_dimension": 2,
        "state_count": K,
        "state_values": X.tolist(),
        "moment_feature_count": 2 + 2 * 3 // 2,
        "outgoing_rates_per_state": K - 1,
        "generic_minimum_K_for_a_null_direction": 2 + 2 * 3 // 2 + 2,
        "moment_design_rank_by_source": ranks,
        "moment_nullity_by_source": null_dims,
        "rowwise_integer_null_vectors_by_action": {"action0": DELTA_0.astype(int).tolist(), "action1": DELTA_1.astype(int).tolist()},
        "moment_gaps_by_action": moment_gaps,
        "minimum_perturbed_rate": min(float(np.min(z)) for z in (rates0_b, rates1_b)),
        "unknown_full_rank_reporter_min_singular_value_in_numeric_example": min_sv,
        "initial_distribution_minimum_mass": float(np.min(pi)),
        "controlled_word": ["Y0", "action0(0.1)", "Y1", "action1(0.1)", "Y2"],
        "output_word_alphabet_size": K**3,
        "observed_word_l1_gap_for_numeric_nuisance_example": law_l1,
        "known_nuisance_tv_gap_for_numeric_example": tv,
        "known_nuisance_hoeffding_lineages_delta_0_05": n_simple_known_nuisance,
        "known_nuisance_reporter_reads": 3 * n_simple_known_nuisance,
        "known_nuisance_controlled_intervals": 2 * n_simple_known_nuisance,
        "unknown_emission_free_parameters": K * (K - 1),
        "unknown_initial_distribution_free_parameters": K - 1,
        "unknown_two_action_generator_parameters_per_model": 2 * K * (K - 1),
        "unknown_parameter_total_per_model_square_reporter": K * (K - 1) + (K - 1) + 2 * K * (K - 1),
        "min_common_permutation_generator_pair_frobenius_gap": best_q_gap,
        "min_common_permutation_transition_pair_frobenius_gap": best_p_gap,
        "max_tau_Q_1_norm": tau_norm,
        "short_lag_log_condition": "max tau*||Q||_1 < pi",
        "scope": "Full two-dimensional state b and the complete 2x2 covariance A match at every one of all 7 states and under both actions. The hidden-emission word law separates this concrete pair. The numerical E,pi illustrate a full-rank reporter; uniform unknown-nuisance sample size still requires a certified profiled margin.",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
