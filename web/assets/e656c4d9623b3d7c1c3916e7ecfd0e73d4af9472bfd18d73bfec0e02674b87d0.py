#!/usr/bin/env python3
"""Finite checks for actionwise-moment-matched hidden CTMCs.

The example is a four-state scalar jump process x in {0,1,2,3}. Two controls
each select a time-homogeneous generator. In each state there are three
outgoing rates but only two chemical-Langevin moments (drift and variance),
so a one-dimensional null direction changes the jump law without changing
either moment. A three-read word with two controlled transitions is then
used for an unknown-emission HMM realization check.

Run from the workspace root:
  python3 work/agents/cell_control/cell_observation_design/cycle3_moment_matched_controls.py

NumPy only. Numerical checks support the displayed instance; the report gives
the exact algebraic and conditional statistical claims separately.
"""

from __future__ import annotations

import itertools
import json
import math
import argparse
from typing import Iterable

import numpy as np

from cycle2_rate_separation import expm


K = 4
X = np.arange(K, dtype=float)
DELTAS = {
    0: np.array([3.0, -3.0, 1.0]),
    1: np.array([-1.0, -3.0, 1.0]),
    2: np.array([1.0, -3.0, -1.0]),
    3: np.array([1.0, -3.0, 3.0]),
}


def generator_from_rates(rates: np.ndarray) -> np.ndarray:
    """Column generator from rows [source, destinations in index order]."""
    q = np.zeros((K, K), dtype=float)
    for source in range(K):
        destinations = [j for j in range(K) if j != source]
        for dest, rate in zip(destinations, rates[source]):
            q[dest, source] = rate
        q[source, source] = -float(np.sum(rates[source]))
    return q


def action_moment_fields(q: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return b_i, A_i, and third jump cumulant-rate Σ q Δx^3 by source."""
    b = np.zeros(K)
    a = np.zeros(K)
    c3 = np.zeros(K)
    for source in range(K):
        for dest in range(K):
            if source == dest:
                continue
            dx = X[dest] - X[source]
            rate = q[dest, source]
            b[source] += rate * dx
            a[source] += rate * dx**2
            c3[source] += rate * dx**3
    return b, a, c3


def triple_law(
    q1: np.ndarray,
    q2: np.ndarray,
    emission: np.ndarray,
    pi0: np.ndarray,
    tau1: float,
    tau2: float,
) -> np.ndarray:
    """P(Y0,Y1,Y2) for the controlled word q1 then q2."""
    p1 = expm(q1 * tau1)
    p2 = expm(q2 * tau2)
    out = np.zeros((emission.shape[0],) * 3)
    for i, j, k in itertools.product(range(K), repeat=3):
        out += (
            pi0[i]
            * p1[j, i]
            * p2[k, j]
            * np.einsum("a,b,c->abc", emission[:, i], emission[:, j], emission[:, k])
        )
    return out


def tensor_factors(
    q1: np.ndarray,
    q2: np.ndarray,
    emission: np.ndarray,
    pi0: np.ndarray,
    tau1: float,
    tau2: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Conditional emission factors around X1 for the rank-K CP tensor."""
    p1 = expm(q1 * tau1)
    p2 = expm(q2 * tau2)
    pi1 = p1 @ pi0
    left = emission @ np.diag(pi0) @ p1.T @ np.diag(1.0 / pi1)
    middle = emission.copy()
    right = emission @ p2
    return left, middle, right, pi1


def pairwise_transition_word_gap(qa: list[np.ndarray], qb: list[np.ndarray]) -> float:
    """Smallest Frobenius gap over one common hidden-state relabeling."""
    best = math.inf
    for perm in itertools.permutations(range(K)):
        s = np.eye(K)[:, perm]
        gap = sum(np.linalg.norm(qa[a] - s.T @ qb[a] @ s, ord="fro") for a in range(2))
        best = min(best, float(gap))
    return best


def multinomial_profile_n(alphabet_size: int, l1_margin: float, delta: float) -> int:
    """Weissman L1 plug-in bound for nearest disjoint composite-law sets.

    If the two complete observable-word model families have certified L1
    distance gamma, empirical L1 error < gamma/2 guarantees nearest-set
    classification. Weissman's finite-alphabet inequality gives the result.
    """
    if not (0.0 < l1_margin <= 2.0):
        raise ValueError("l1_margin must be in (0,2]")
    return math.ceil(
        8.0 / l1_margin**2 * math.log((2**alphabet_size - 2) / delta)
    )


def simple_hypothesis_n(tv: float, delta: float) -> int:
    """Two-sided error <= delta for a known TV-optimal binary word statistic."""
    if not (0.0 < tv <= 1.0):
        raise ValueError("tv must be in (0,1]")
    return math.ceil(2.0 / tv**2 * math.log(1.0 / delta))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile-gamma",
        type=float,
        default=None,
        help="externally certified lower bound on profiled L1 separation of the two compact word-law families",
    )
    parser.add_argument("--delta", type=float, default=0.05, help="target classification error")
    parser.add_argument("--c-lineage", type=float, default=0.0, help="cost per independent lineage")
    parser.add_argument("--c-read", type=float, default=0.0, help="cost per reporter read")
    parser.add_argument("--c-action", type=float, default=0.0, help="cost per controlled interval")
    parser.add_argument("--c-state-calibration", type=float, default=0.0)
    parser.add_argument("--c-dose-calibration", type=float, default=0.0)
    args = parser.parse_args()
    if not (0.0 < args.delta < 1.0):
        parser.error("--delta must lie in (0,1)")

    rates_a = [
        np.ones((K, K - 1)),
        np.array(
            [
                [1.1, 0.7, 1.4],
                [0.8, 1.3, 0.6],
                [1.5, 0.9, 0.7],
                [0.6, 1.2, 1.6],
            ],
            dtype=float,
        ),
    ]
    # Distinct coefficients are applied to the moment-null row direction for
    # each control, keeping every actionwise drift and variance fixed.
    eps = [0.10, 0.08]
    rates_b = []
    for action in range(2):
        rb = rates_a[action].copy()
        for source in range(K):
            rb[source] += eps[action] * DELTAS[source]
        rates_b.append(rb)
    qa = [generator_from_rates(r) for r in rates_a]
    qb = [generator_from_rates(r) for r in rates_b]

    assert min(float(np.min(r)) for r in rates_a + rates_b) > 0.0
    moments_a = [action_moment_fields(q) for q in qa]
    moments_b = [action_moment_fields(q) for q in qb]
    moment_gaps = []
    third_moment_gaps = []
    for action in range(2):
        bgap = float(np.max(np.abs(moments_a[action][0] - moments_b[action][0])))
        agap = float(np.max(np.abs(moments_a[action][1] - moments_b[action][1])))
        c3gap = float(np.max(np.abs(moments_a[action][2] - moments_b[action][2])))
        moment_gaps.append({"drift_sup_gap": bgap, "variance_sup_gap": agap})
        third_moment_gaps.append(c3gap)
        assert bgap < 1e-12 and agap < 1e-12

    tau1 = tau2 = 0.10
    # A shared but initially unknown full-rank four-symbol reporter. It is
    # used to make one transparent numeric instance of the observation law;
    # the identifiability claim does not reveal E or pi to the estimator.
    emission = 0.7 * np.eye(K) + 0.075 * np.ones((K, K))
    pi0 = np.full(K, 1.0 / K)
    kappa = float(np.linalg.svd(emission, compute_uv=False)[-1])
    assert np.allclose(emission.sum(axis=0), 1.0)
    law_a = triple_law(qa[0], qa[1], emission, pi0, tau1, tau2)
    law_b = triple_law(qb[0], qb[1], emission, pi0, tau1, tau2)
    l1_gap = float(np.abs(law_a - law_b).sum())
    tv_gap = l1_gap / 2.0
    assert l1_gap > 1e-8

    left, middle, right, pi1 = tensor_factors(
        qa[0], qa[1], emission, pi0, tau1, tau2
    )
    factor_sigmas = [
        float(np.linalg.svd(f, compute_uv=False)[-1]) for f in (left, middle, right)
    ]
    assert min(factor_sigmas) > 0.0 and float(np.min(pi1)) > 0.0

    # No common permutation makes the two controlled transition systems the
    # same. The positive gap is a finite check for this explicit instance.
    q_perm_gap = pairwise_transition_word_gap(qa, qb)
    assert q_perm_gap > 1e-6
    p_perm_gap = math.inf
    for perm in itertools.permutations(range(K)):
        s = np.eye(K)[:, perm]
        gap = sum(
            np.linalg.norm(expm(qa[a] * (tau1 if a == 0 else tau2)) -
                           s.T @ expm(qb[a] * (tau1 if a == 0 else tau2)) @ s,
                           ord="fro")
            for a in range(2)
        )
        p_perm_gap = min(p_perm_gap, float(gap))

    # Commutator check: these controls give a genuinely ordered action word.
    commutator_a = float(np.linalg.norm(qa[1] @ qa[0] - qa[0] @ qa[1], ord="fro"))
    commutator_b = float(np.linalg.norm(qb[1] @ qb[0] - qb[0] @ qb[1], ord="fro"))

    # A rank-one reporter has identical emission columns and erases every
    # controlled word, not only the selected three-read word.
    rank_one_emission = np.tile(np.array([[0.65], [0.35]]), (1, K))
    rank_one_a = triple_law(qa[0], qa[1], rank_one_emission, pi0, tau1, tau2)
    rank_one_b = triple_law(qb[0], qb[1], rank_one_emission, pi0, tau1, tau2)

    delta = args.delta
    n_known_nuisance = simple_hypothesis_n(tv_gap, delta)
    # With genuinely unknown nuisance parameters, the relevant margin is the
    # *profiled* L1 gap over the compact sets, not the fixed-E number above.
    # A user-supplied certified gamma plugs directly into this bound.
    example_certified_profile_gamma = args.profile_gamma
    if example_certified_profile_gamma is None:
        profile_n = None
        profile_cost = None
    else:
        profile_n = multinomial_profile_n(4**3, example_certified_profile_gamma, delta)
        profile_cost = (
            profile_n
            * (args.c_lineage + 3.0 * args.c_read + 2.0 * args.c_action)
            + args.c_state_calibration
            + args.c_dose_calibration
        )

    out = {
        "status": "finite witness for exact actionwise b/A equality; standard HMM realization machinery handles hidden labels",
        "state_and_rate_parameterization": {
            "state_count": K,
            "scalar_state_values": X.tolist(),
            "outgoing_rates_per_state_per_action": K - 1,
            "moment_constraints_per_state": 2,
            "action_count": 2,
            "independent_stochastic_units": "tracked founders/lineages, never descendant cells",
        },
        "moment_nullspace": {
            "row_null_vectors_destination_order": {str(i): DELTAS[i].tolist() for i in range(K)},
            "alternative_rates": "q_B[action,i->dest] = q_A[action,i->dest] + eps[action]*delta[i,dest]",
            "eps_by_action": eps,
            "minimum_rate_across_both_models": min(float(np.min(r)) for r in rates_a + rates_b),
            "actionwise_max_gaps": moment_gaps,
            "actionwise_third_jump_moment_sup_gaps": third_moment_gaps,
            "theorem": "For x={0,1,2,3}, each source has three rates and the two constraints ΣqΔx and Σq(Δx)^2. The displayed nonzero δ rows lie in their nullspace. Thus the two models have exactly identical chemical-Langevin drift and variance at every state for each intervention, but differ in third jump moment and in Q.",
        },
        "controlled_hidden_word": {
            "sampling_word": ["read Y0", "action 0 for tau1", "read Y1", "action 1 for tau2", "read Y2"],
            "reads_per_independent_lineage": 3,
            "controlled_transitions_per_lineage": 2,
            "finite_lags": [tau1, tau2],
            "largest_tau_generator_1_norm": max(float(np.linalg.norm(q, 1)) for q in qa + qb) * max(tau1, tau2),
            "principal_log_no_alias_sufficient_check": "max_a tau_a*||Q_a||_1 < pi; in this explicit example it holds, so P_a=e^(tau_a Q_a) recovers Q_a by the principal matrix logarithm within this bounded class",
            "unknown_shared_emission_matrix": True,
            "unknown_initial_state_distribution": True,
            "emission_min_singular_value_in_numeric_witness_only": kappa,
            "initial_distribution_min_mass_in_numeric_witness_only": float(np.min(pi0)),
            "three_view_factor_min_singular_values_in_numeric_witness": factor_sigmas,
            "initial_distribution_after_action_0_min_mass": float(np.min(pi1)),
            "observed_triple_law_l1_gap_for_numeric_nuisance_instance": l1_gap,
            "observed_triple_law_tv_gap_for_numeric_nuisance_instance": tv_gap,
            "min_common_permutation_generator_pair_frobenius_gap": q_perm_gap,
            "min_common_permutation_transition_pair_frobenius_gap": p_perm_gap,
            "action_generator_commutator_frobenius": {"model_A": commutator_a, "model_B": commutator_b},
            "exact_identifiability_argument": "The joint law is a rank-K CP tensor Σ_j π1[j] L[:,j]⊗E[:,j]⊗R[:,j], where L=E diag(π0)P0ᵀdiag(π1)^−1 and R=E P1. If E is square full rank, π0>0, and P0,P1 are nonsingular, all three factors have column rank K; Kruskal uniqueness identifies E,L,R up to one common state permutation. Marginals recover π0,π1, then P1=E^−1R and P0=(E^−1L diag(π1))ᵀ diag(π0)^−1. A short-lag generator norm bound then gives Q_a=Log(P_a)/tau_a.",
            "minimality_scope": "One read contains no transition information. For K=m=4, unknown E(12)+pi(3)+two action transitions(24)=39 parameters, whereas two separate action-conditioned pair laws contain at most 2*(m^2−1)=30 degrees of freedom. Thus two-read pair data cannot generically identify all unknown parameters; the 3-read/two-transition word is the shortest generic tensor realization in this two-action design. This is not a claim that 3 reads are necessary for every calibrated or specially structured model.",
        },
        "noise_and_sample_cost": {
            "independent_unit": "one lineage observed at three scheduled timepoints; no pseudoreplication across progeny",
            "known_nuisance_simple_test": {
                "interpretation": "For the displayed E,pi instance only, if both predicted categorical word laws are known, use the TV-optimal binary event and threshold its frequency.",
                "delta": delta,
                "lineages_sufficient_by_hoeffding": n_known_nuisance,
                "reporter_reads": 3 * n_known_nuisance,
                "controlled_intervals": 2 * n_known_nuisance,
                "cost_formula": "n*(c_lineage + 3*c_reporter_read + 2*c_control_interval) + c_state_coordinate_calibration + c_dose_calibration",
            },
            "unknown_nuisance_profile_test": {
                "unknown_per_model_parameters": {
                    "emission_matrix_4x4_column_stochastic": 12,
                    "initial_simplex": 3,
                    "two_action_generator_offdiagonal_rates": 24,
                    "total": 39,
                    "add_if_state_coordinates_not_calibrated": "3 free coordinates after fixing origin (or 4 if absolute origin is meaningful)",
                    "add_if_action_potency_not_calibrated": 2,
                },
                "required_assumptions_for_uniform_finite_n": "compact parameter boxes; emission singular value >= kappa0>0; pi_i>=eta>0; bounded rates and sampling times; alternative pair families separated after quotienting common state permutations",
                "required_certified_composite_margin": "gamma = inf_{P in H_A, R in H_B} ||P-R||_1 > 0 for the length-3 observable-word laws, optimizing over all unknown emissions, initial distributions, rate boxes, state coordinates, and dose nuisances",
                "alphabet_size": 4**3,
                "lineages_sufficient_if_gamma_certified": "ceil(8/gamma^2 * log((2^(4^3)-2)/delta)) using the finite-alphabet L1 concentration bound and nearest-set classification",
                "cost_if_gamma_certified": "n*(c_lineage + 3*c_reporter_read + 2*c_control_interval) + c_state_coordinate_calibration + c_dose_calibration",
                "externally_certified_profile_gamma_input": example_certified_profile_gamma,
                "margin_certificate_is_assumed_from_caller_not_verified_by_this_script": example_certified_profile_gamma is not None,
                "lineages_sufficient_if_gamma_input_certified": profile_n,
                "cost_under_supplied_unit_prices": profile_cost,
                "unit_prices": {
                    "lineage": args.c_lineage,
                    "reporter_read": args.c_read,
                    "controlled_interval": args.c_action,
                    "state_calibration": args.c_state_calibration,
                    "dose_calibration": args.c_dose_calibration,
                },
                "current_decision": (
                    "UNKNOWN for a uniform numeric sample count; no nuisance boxes or profiled margin certificate were supplied."
                    if example_certified_profile_gamma is None
                    else "Conditional count/cost computed from the caller-supplied certified profiled margin; this script does not verify that certificate."
                ),
            },
            "finite_lag_bias": "The hidden-word test uses exact exp(Q*tau) and has no infinitesimal-lag approximation bias. If rates are instead estimated by (P-I)/tau, ||P-I-tau Q||_1 <= exp(tau||Q||_1)-1-tau||Q||_1; this finite-lag remainder must be charged separately.",
        },
        "no_go": {
            "emission_rank": int(np.linalg.matrix_rank(rank_one_emission)),
            "rank_one_reporter_triple_law_max_gap": float(np.max(np.abs(rank_one_a - rank_one_b))),
            "claim": "If every hidden state has the same emission distribution, every controlled output word has the same law under both generators. No action sequence can identify hidden rates; a positive rank/conditioning assumption is necessary.",
        },
        "routine_prior_art_boundary": [
            "Unknown full-rank HMM realization from three observations is standard (Allman-Matias-Rhodes 2009; Gassiat-Cleynen-Robin 2016); controlled-HMM observability/reconstructibility is also established (Liu-Bitmead 2010).",
            "The present witness is not claimed novel: its load-bearing point is the explicit smallest scalar-state actionwise moment-matched CTMC pair satisfying the strengthened same-b(x), A(x) quantifier, followed by an ordinary full-rank controlled-HMM word that separates them.",
        ],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
