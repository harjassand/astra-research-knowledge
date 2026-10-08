#!/usr/bin/env python3
"""Finite checks for hidden-emission discrimination of the C2 cycle alias.

NumPy-only. The reporter is deliberately not identity: its emission matrix is
unknown to the proposed test, but a full-column-rank lower bound is assumed.
Each independent unit is one lineage/founder with repeated observations.
"""

from __future__ import annotations

import itertools
import json
import math

import numpy as np

from cycle2_rate_separation import cycle_generator, expm


def pair_law(Q: np.ndarray, E: np.ndarray, pi: np.ndarray, tau: float) -> np.ndarray:
    """J[a,b]=Pr(Y0=a,Y1=b)=E diag(pi) P(tau)^T E^T."""
    P = expm(Q * tau)
    return E @ np.diag(pi) @ P.T @ E.T


def triple_law(
    Q: np.ndarray,
    E: np.ndarray,
    pi0: np.ndarray,
    tau1: float,
    tau2: float,
    scale2: float = 1.0,
) -> np.ndarray:
    """Three emissions with transitions exp(Q*tau1), exp(scale2*Q*tau2)."""
    P1 = expm(Q * tau1)
    P2 = expm(Q * (scale2 * tau2))
    K = len(pi0)
    m = E.shape[0]
    T = np.zeros((m, m, m))
    for i in range(K):
        for j in range(K):
            for k in range(K):
                weight = pi0[i] * P1[j, i] * P2[k, j]
                T += weight * np.einsum("a,b,c->abc", E[:, i], E[:, j], E[:, k])
    return T


def cp_view_factors(Q: np.ndarray, E: np.ndarray, pi0: np.ndarray, tau1: float, tau2: float, u: float):
    """Return left/middle/right conditional emission factors around X_1."""
    P1 = expm(Q * tau1)
    P2 = expm(Q * (u * tau2))
    pi1 = P1 @ pi0
    left = E @ np.diag(pi0) @ P1.T @ np.diag(1.0 / pi1)
    middle = E
    right = E @ P2
    return left, middle, right, pi1


def l1_empirical_bound(sample_alphabet_size: int, gap: float, delta: float) -> int:
    """Weissman-style L1 bound, for nearest-set testing with separation gap.

    A nearest-set classifier is correct if empirical L1 error < gap/2. The
    bound Pr(||P_hat-P||_1 >= eps) <= (2^L-2) exp(-n eps^2/2) is applied at
    eps=gap/2. For the pair-asymmetry classifier below we use eps=gamma/4.
    """
    return math.ceil(8.0 / (gap * gap) * math.log((2**sample_alphabet_size - 2) / delta))


def cycle_for_d(s: float, d: float, tau: float) -> np.ndarray:
    return cycle_generator((s + d) / 2.0, (s - d) / 2.0)


def main() -> None:
    K = 3
    tau = 1.0
    s = 10.0
    d_alias = 4.0 * math.pi / (math.sqrt(3.0) * tau)
    Q_rev = cycle_for_d(s, 0.0, tau)
    Q_nonrev = cycle_for_d(s, d_alias, tau)
    pi = np.full(K, 1.0 / K)

    # This unknown-to-the-classifier but full-rank shared reporter is used only
    # for a transparent numerical run; the theorem is stated through kappa.
    E = 0.8 * np.eye(K) + 0.2 * np.ones((K, K)) / K
    kappa = float(np.linalg.svd(E, compute_uv=False)[-1])

    P_alias_rev = expm(Q_rev * tau)
    P_alias_nonrev = expm(Q_nonrev * tau)
    J_tau_rev = pair_law(Q_rev, E, pi, tau)
    J_tau_nonrev = pair_law(Q_nonrev, E, pi, tau)

    # Choose the shorter second lag/rate scale to reveal the orientation.
    a = 1.5 * s * tau
    u_opt = math.atan(2.0 * math.pi / a) / (2.0 * math.pi)
    P_u_rev = expm(Q_rev * (u_opt * tau))
    P_u_nonrev = expm(Q_nonrev * (u_opt * tau))
    J_u_rev = pair_law(Q_rev, E, pi, u_opt * tau)
    J_u_nonrev = pair_law(Q_nonrev, E, pi, u_opt * tau)

    skew_rev = float(np.linalg.norm(J_u_rev - J_u_rev.T, "fro"))
    skew_nonrev = float(np.linalg.norm(J_u_nonrev - J_u_nonrev.T, "fro"))
    p_min = float(np.min(P_alias_rev))
    skew_hidden_bound = (2.0 * math.sqrt(2.0) / 3.0) * math.exp(-a * u_opt) * abs(
        math.sin(2.0 * math.pi * u_opt)
    )
    gamma_lower = kappa * kappa * skew_hidden_bound
    delta = 0.05
    n_pairs = math.ceil(32.0 / (gamma_lower * gamma_lower) * math.log((2**(K * K) - 2) / delta))

    # A no-go: a rank-one reporter erases all state information under every word.
    E_rank_one = np.tile(np.array([[0.7], [0.3]]), (1, K))
    J_rank_one_rev = pair_law(Q_rev, E_rank_one, pi, u_opt * tau)
    J_rank_one_nonrev = pair_law(Q_nonrev, E_rank_one, pi, u_opt * tau)
    T_rank_one_rev = triple_law(Q_rev, E_rank_one, pi, tau, u_opt * tau)
    T_rank_one_nonrev = triple_law(Q_nonrev, E_rank_one, pi, tau, u_opt * tau)

    # Generic three-observation realization uses two short, incommensurate gaps.
    h1 = 0.05 * tau
    h2 = math.sqrt(2.0) * h1
    left, middle, right, pi1 = cp_view_factors(Q_nonrev, E, pi, h1, h2, 1.0)
    triple_rev = triple_law(Q_rev, E, pi, h1, h2)
    triple_nonrev = triple_law(Q_nonrev, E, pi, h1, h2)

    # Label-invariant check: no latent-state permutation conjugates the two Qs.
    permutation_gap = math.inf
    for perm in itertools.permutations(range(K)):
        S = np.eye(K)[:, perm]
        permutation_gap = min(permutation_gap, float(np.linalg.norm(Q_rev - S.T @ Q_nonrev @ S, "fro")))

    result = {
        "pair_alias_hidden_outputs_at_original_tau": {
            "tau": tau,
            "max_abs_hidden_transition_difference": float(np.max(np.abs(P_alias_rev - P_alias_nonrev))),
            "max_abs_observed_pair_law_difference": float(np.max(np.abs(J_tau_rev - J_tau_nonrev))),
            "one_read_marginal_depends_on": "E*pi only; it contains no transition/rate factor",
        },
        "minimal_two_read_time_reversal_word": {
            "reads_per_independent_lineage": 2,
            "one_transition_interval": u_opt * tau,
            "known_rate_scale_if_used": u_opt,
            "emission_matrix_is_unknown_to_test": True,
            "reporter_min_singular_value_in_finite_example": kappa,
            "common_stationary_initial_distribution": pi.tolist(),
            "observed_pair_law_rev_skew_frobenius": skew_rev,
            "observed_pair_law_nonrev_skew_frobenius": skew_nonrev,
            "hidden_skew_lower_bound": skew_hidden_bound,
            "observed_skew_lower_bound_gamma": gamma_lower,
            "endpoint_alias_pmin": p_min,
            "independent_paired_lineages_for_delta_0_05_bound": n_pairs,
            "sample_cost": {
                "lineages": n_pairs,
                "reporter_reads": 2 * n_pairs,
                "controlled_intervals": n_pairs,
                "lineage_tracking_cost": "charge one independent tracked lineage per pair; no descendants counted as replicates",
                "excluded": "culture, reporter calibration or singular-value certification, dose/timing calibration, and pre-equilibration costs are external supplied costs",
            },
        },
        "rank_deficient_emission_no_go": {
            "emission_rank": int(np.linalg.matrix_rank(E_rank_one)),
            "pair_law_difference_any_test": float(np.max(np.abs(J_rank_one_rev - J_rank_one_nonrev))),
            "triple_law_difference_any_test": float(np.max(np.abs(T_rank_one_rev - T_rank_one_nonrev))),
            "claim": "Identical emission columns make the entire observation process independent of hidden rates under every action/sampling word.",
        },
        "generic_three_view_realization": {
            "reads_per_independent_lineage": 3,
            "action_or_gap_word": [h1, h2],
            "gap_ratio": h2 / h1,
            "gap_ratio_is_irrational_by_design": True,
            "left_factor_min_singular_value": float(np.linalg.svd(left, compute_uv=False)[-1]),
            "middle_factor_min_singular_value": float(np.linalg.svd(middle, compute_uv=False)[-1]),
            "right_factor_min_singular_value": float(np.linalg.svd(right, compute_uv=False)[-1]),
            "triple_law_l1_difference_under_shared_reporter": float(np.abs(triple_rev - triple_nonrev).sum()),
            "min_rate_generator_frobenius_gap_over_state_permutations": permutation_gap,
            "free_parameters_K3_three_emissions": {
                "emission_matrix": K * (K - 1),
                "initial_distribution": K - 1,
                "generator_off_diagonal_rates": K * (K - 1),
                "total": K * (K - 1) + (K - 1) + K * (K - 1),
                "known_dose_multiplier": 0,
            },
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
