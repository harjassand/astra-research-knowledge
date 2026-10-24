#!/usr/bin/env python3
"""Shot-only predictive-state benchmark for a hidden-memory qubit collision.

The learner receives only a callable that resets the process, runs requested
binary system preparations, and returns noisy Z outcomes. Hidden process
parameters and memory are held by the server object and are never arguments to
the fitting or prediction routines. This is a synthetic benchmark, not a
physical experiment.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from fractions import Fraction
from typing import Callable, Iterable

import numpy as np


class _HiddenCollisionServer:
    """Private episode state for one of two legal finite-memory collisions."""

    def __init__(self, rule: str, p_readout: float, delta_memory: float,
                 seed: int) -> None:
        assert rule in {"parity", "overwrite"}
        self.__rule = rule
        self.__p = p_readout
        self.__delta = delta_memory
        self.__rng = np.random.default_rng(seed)
        self.__m = 0
        self.episodes = 0
        self.collisions = 0

    def reset(self) -> None:
        self.__m = 0
        self.episodes += 1

    def step(self, action: int) -> int:
        """One system preparation, collision, noisy Z readout, and memory noise."""
        assert action in (0, 1)
        old_m = self.__m
        # U_parity = SWAP * CNOT(memory -> system): |a,m> -> |m,a xor m>.
        # U_overwrite = SWAP: |a,m> -> |m,a>.
        # Both output system state |m>; the memory rule remains hidden.
        y = old_m ^ int(self.__rng.random() < self.__p)
        if self.__rule == "parity":
            after_collision = old_m ^ action
        else:
            after_collision = action
        self.__m = after_collision ^ int(self.__rng.random() < self.__delta)
        self.collisions += 1
        return y


def _query_api(server: _HiddenCollisionServer) -> Callable[[Iterable[int]], list[int]]:
    """The fitting routine receives only this episode-query callback."""
    def query(actions: Iterable[int]) -> list[int]:
        server.reset()
        return [server.step(int(a)) for a in actions]
    return query


def _safe_clip(x: float, lo: float, hi: float) -> float:
    return min(hi, max(lo, x))


def _bernoulli_ll(successes: int, trials: int, prob: float) -> float:
    q = _safe_clip(prob, 1e-12, 1 - 1e-12)
    return successes * math.log(q) + (trials - successes) * math.log1p(-q)


def _sequence_probability(rule: str, actions: tuple[int, ...],
                          outcomes: tuple[int, ...], p: Fraction,
                          delta: Fraction) -> Fraction:
    """Exact hidden-state sum for the auditor's rational benchmark fixture."""
    state = [Fraction(1), Fraction(0)]  # P(M=0), P(M=1)
    for action, outcome in zip(actions, outcomes):
        after = [Fraction(0), Fraction(0)]
        for m, mass in enumerate(state):
            p_y = (p if m == 0 else 1 - p) if outcome else (1 - p if m == 0 else p)
            nominal = (m ^ action) if rule == "parity" else action
            after[nominal] += mass * p_y * (1 - delta)
            after[1 - nominal] += mass * p_y * delta
        state = after
    return sum(state)


def exact_structure_checks() -> dict:
    """Exhaustively verify the horizon-2 alias and first separating probe."""
    p, delta = Fraction(2, 25), Fraction(1, 25)
    max_h2_difference = Fraction(0)
    for actions in ((a0, a1) for a0 in (0, 1) for a1 in (0, 1)):
        for outcomes in ((y0, y1) for y0 in (0, 1) for y1 in (0, 1)):
            pp = _sequence_probability("parity", actions, outcomes, p, delta)
            po = _sequence_probability("overwrite", actions, outcomes, p, delta)
            max_h2_difference = max(max_h2_difference, abs(pp - po))

    actions = (1, 0, 0)
    q: dict[str, Fraction] = {}
    for rule in ("parity", "overwrite"):
        q[rule] = sum(
            _sequence_probability(rule, actions, ys, p, delta)
            for ys in ((y0, y1, 1)
                       for y0 in (0, 1) for y1 in (0, 1))
        )
    expected_gap = (1 - 2 * p) * (1 - 3 * delta + 2 * delta ** 2)
    matched_rate0 = p + (1 - 2 * p) * delta
    matched_rate1 = p + (1 - 2 * p) * (1 - delta)
    assert max_h2_difference == 0
    assert q["parity"] - q["overwrite"] == expected_gap
    assert matched_rate1 - matched_rate0 == (1 - 2 * p) * (1 - 2 * delta)
    return {
        "exact_horizon_2_max_joint_probability_difference": str(max_h2_difference),
        "p_first_report_zero": str(1 - p),
        "next_outcome_rate_after_action0_given_report0": str(matched_rate0),
        "next_outcome_rate_after_action1_given_report0": str(matched_rate1),
        "matched_state_rate_difference": str(matched_rate1 - matched_rate0),
        "first_separating_actions": list(actions),
        "true_p_y3_1_parity": str(q["parity"]),
        "true_p_y3_1_overwrite": str(q["overwrite"]),
        "exact_gap": str(q["parity"] - q["overwrite"]),
    }


def fit_from_shots(query: Callable[[Iterable[int]], list[int]],
                   n_pairs: int = 2000, n_rule: int = 2000) -> dict:
    """Estimate readout/memory noise and select a two-rule family from shots."""
    first_successes = 0
    pair0_y2_successes = 0
    pair1_y2_successes = 0
    matched0_n = matched0_successes = 0
    matched1_n = matched1_successes = 0
    for _ in range(n_pairs):
        y = query([0, 0])
        first_successes += y[0]
        pair0_y2_successes += y[1]
        if y[0] == 0:
            matched0_n += 1
            matched0_successes += y[1]
    for _ in range(n_pairs):
        y = query([1, 0])
        first_successes += y[0]
        pair1_y2_successes += y[1]
        if y[0] == 0:
            matched1_n += 1
            matched1_successes += y[1]
    rule_y3_successes = 0
    for _ in range(n_rule):
        y = query([1, 0, 0])
        first_successes += y[0]
        rule_y3_successes += y[2]

    total_first = 2 * n_pairs + n_rule
    p_hat = first_successes / total_first
    r0 = pair0_y2_successes / n_pairs
    r1 = pair1_y2_successes / n_pairs
    den = max(1e-6, 1 - 2 * p_hat)
    d0 = (r0 - p_hat) / den
    d1 = (1 - r1 - p_hat) / den
    delta_hat = _safe_clip((d0 + d1) / 2, 0.0, 0.49)

    q_overwrite = p_hat + (1 - 2 * p_hat) * delta_hat
    p_m2_one_parity = (1 + (1 - 2 * delta_hat) ** 2) / 2
    q_parity = p_hat + (1 - 2 * p_hat) * p_m2_one_parity
    r3 = rule_y3_successes / n_rule
    ll_parity = _bernoulli_ll(rule_y3_successes, n_rule, q_parity)
    ll_overwrite = _bernoulli_ll(rule_y3_successes, n_rule, q_overwrite)
    rule_hat = "parity" if ll_parity >= ll_overwrite else "overwrite"

    # Matched-current-state diagnostic uses all pair shots but conditions only
    # for this reported witness; fitting above uses every episode outcome.
    cond0 = matched0_successes / matched0_n
    cond1 = matched1_successes / matched1_n
    matched_se = math.sqrt(cond0 * (1 - cond0) / matched0_n
                            + cond1 * (1 - cond1) / matched1_n)
    return {
        "p_readout_hat": p_hat,
        "delta_memory_hat": delta_hat,
        "pair_y2_rate_action0": r0,
        "pair_y2_rate_action1": r1,
        "rule_y3_rate_for_100": r3,
        "candidate_y3_rate_parity": q_parity,
        "candidate_y3_rate_overwrite": q_overwrite,
        "rule_hat": rule_hat,
        "log_likelihood_parity": ll_parity,
        "log_likelihood_overwrite": ll_overwrite,
        "training_episodes": 2 * n_pairs + n_rule,
        "training_collisions": 4 * n_pairs + 3 * n_rule,
        "matched_state": {
            "current_reported_outcome": 0,
            "future_action": 0,
            "next_outcome_rate_after_action0": cond0,
            "next_outcome_rate_after_action1": cond1,
            "future_rate_difference": cond1 - cond0,
            "difference_standard_error": matched_se,
            "difference_normal_95pct_interval": [
                (cond1 - cond0) - 1.96 * matched_se,
                (cond1 - cond0) + 1.96 * matched_se,
            ],
            "conditioned_samples_after_action0": matched0_n,
            "conditioned_samples_after_action1": matched1_n,
            "conditioning_fraction_action0": matched0_n / n_pairs,
            "conditioning_fraction_action1": matched1_n / n_pairs,
        },
    }


class PredictiveState:
    """One-scalar posterior state for the learned two-state operation."""

    def __init__(self, p: float, delta: float, rule: str) -> None:
        self.p = p
        self.delta = delta
        self.rule = rule
        self.b = 0.0  # P(hidden memory bit is 1 before current readout)

    def predict_one(self) -> float:
        return self.p + (1 - 2 * self.p) * self.b

    def observe_and_act(self, outcome: int, action: int) -> None:
        p_y = self.predict_one()
        if outcome == 1:
            post = self.b * (1 - self.p) / max(p_y, 1e-15)
        else:
            post = self.b * self.p / max(1 - p_y, 1e-15)
        post = _safe_clip(post, 0.0, 1.0)
        if self.rule == "parity":
            preflip = post if action == 0 else 1 - post
            self.b = self.delta + (1 - 2 * self.delta) * preflip
        else:
            self.b = self.delta + (1 - 2 * self.delta) * action


class TwoStateHMM:
    """Generic rank-2 forward filter used as the conventional spectral/HMM comparator."""

    def __init__(self, p: float, delta: float, rule: str) -> None:
        self.p = p
        self.delta = delta
        self.rule = rule
        self.alpha = np.array([1.0, 0.0])

    def predict_one(self) -> float:
        return float(self.alpha @ np.array([self.p, 1 - self.p]))

    def observe_and_act(self, outcome: int, action: int) -> None:
        emission = np.array([1 - self.p, self.p]) if outcome == 0 else np.array([self.p, 1 - self.p])
        post = self.alpha * emission
        post /= max(float(post.sum()), 1e-15)
        transition = np.zeros((2, 2))
        for m in (0, 1):
            if self.rule == "parity":
                nominal = m ^ action
            else:
                nominal = action
            transition[m, nominal] += 1 - self.delta
            transition[m, 1 - nominal] += self.delta
        self.alpha = post @ transition


def adaptive_policy(t: int, previous_outcomes: list[int]) -> int:
    if t == 0:
        return 1
    return previous_outcomes[-1] ^ (t & 1)


def heldout_adaptive(server: _HiddenCollisionServer, p: float, delta: float,
                     rule: str, episodes: int = 2000, horizon: int = 20) -> dict:
    brier_pred: list[float] = []
    logloss_pred: list[float] = []
    brier_hmm: list[float] = []
    logloss_hmm: list[float] = []
    max_prediction_difference = 0.0
    query_steps = 0
    for _ in range(episodes):
        server.reset()
        pred = PredictiveState(p, delta, rule)
        hmm = TwoStateHMM(p, delta, rule)
        outcomes: list[int] = []
        for t in range(horizon):
            action = adaptive_policy(t, outcomes)
            y = server.step(action)
            pp, ph = pred.predict_one(), hmm.predict_one()
            max_prediction_difference = max(max_prediction_difference, abs(pp - ph))
            brier_pred.append((pp - y) ** 2)
            logloss_pred.append(-math.log(max(pp if y else 1 - pp, 1e-15)))
            brier_hmm.append((ph - y) ** 2)
            logloss_hmm.append(-math.log(max(ph if y else 1 - ph, 1e-15)))
            pred.observe_and_act(y, action)
            hmm.observe_and_act(y, action)
            outcomes.append(y)
            query_steps += 1
    return {
        "episodes": episodes,
        "horizon": horizon,
        "adaptive_actions": "a_0=1; for t>0, a_t=y_(t-1) XOR (t mod 2)",
        "collisions": query_steps,
        "predictive_state_brier": float(np.mean(brier_pred)),
        "rank2_hmm_brier": float(np.mean(brier_hmm)),
        "predictive_state_logloss_nats": float(np.mean(logloss_pred)),
        "rank2_hmm_logloss_nats": float(np.mean(logloss_hmm)),
        "max_stepwise_prediction_difference": max_prediction_difference,
    }


def benchmark(seed: int = 241024, n_pairs: int = 2000, n_rule: int = 2000,
              test_episodes: int = 2000, test_horizon: int = 20) -> dict:
    # Synthetic hidden instance. These values belong only to the server.
    server = _HiddenCollisionServer(rule="parity", p_readout=0.08,
                                    delta_memory=0.04, seed=seed)
    query = _query_api(server)
    fit = fit_from_shots(query, n_pairs=n_pairs, n_rule=n_rule)
    train_episodes = server.episodes
    train_collisions = server.collisions
    test = heldout_adaptive(server, fit["p_readout_hat"], fit["delta_memory_hat"],
                            fit["rule_hat"], episodes=test_episodes,
                            horizon=test_horizon)
    return {
        "synthetic_only": True,
        "hidden_process_definition_for_auditor_not_learner": {
            "system_and_memory": "two qubits; M reset to |0> each episode",
            "native_unitary_family": {
                "parity": "SWAP * CNOT(M->S): |a,m> -> |m,a XOR m>",
                "overwrite": "SWAP: |a,m> -> |m,a>",
            },
            "instrument": "measure S in Z; independently flip reported bit with hidden p",
            "memory_noise": "after collision, independently flip M with hidden delta",
            "hidden_instance": "parity rule, p=0.08, delta=0.04 (not passed to fit_from_shots)",
        },
        "fit": fit,
        "accounting": {
            "training_resets": train_episodes,
            "training_actions_and_collisions": train_collisions,
            "heldout_resets": test_episodes,
            "heldout_actions_and_collisions": test["collisions"],
            "total_resets": train_episodes + test_episodes,
            "total_actions_and_collisions": train_collisions + test["collisions"],
            "conditioning": "fitting uses all shot outcomes; only the matched-state diagnostic conditions on y1=0, and its retained counts are reported",
            "learner_state": "one scalar hidden-state posterior plus two fitted parameters; O(1) update and memory per action",
            "fit_runtime": "O(number of requested shots); O(1) training sufficient statistics and O(1) predictor state",
        },
        "heldout_adaptive": test,
        "finite_horizon_identifiability": {
            "exact_rational_checks": exact_structure_checks(),
            "training_max_horizon": 3,
            "two_rules_identical_through_horizon_2": True,
            "first_distinguishing_action_sequence": [1, 0, 0],
            "why": "Both rules produce the same first two output laws from reset; at step 3, parity retains the earlier action while overwrite discards it.",
            "scope": "A length-2 process tensor cannot determine this continuation. Training to horizon 3 separates these two candidates, but arbitrary unseen continuations still require a declared model/rank assumption.",
        },
        "strongest_conventional_comparator": {
            "model": "rank-2 controlled HMM / spectral state-space fit on the same shot data and same two-rule candidate family",
            "result": "The generic two-state forward filter is algebraically equivalent to the one-scalar predictive-state update; it ties here, as it should.",
            "finite_history": "An exact process tensor through horizon 3 fits those interventions but has no unique horizon-20 extension without an added state-space assumption.",
            "no_advantage_claim": True,
        },
    }


if __name__ == "__main__":
    out = Path(__file__).with_name("SUPPORT_BENCHMARK_RESULTS.json")
    result = benchmark()
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "results": str(out),
        "learned_rule": result["fit"]["rule_hat"],
        "p_hat": result["fit"]["p_readout_hat"],
        "delta_hat": result["fit"]["delta_memory_hat"],
        "matched_future_rate_difference": result["fit"]["matched_state"]["future_rate_difference"],
        "heldout_brier": result["heldout_adaptive"]["predictive_state_brier"],
        "rank2_brier": result["heldout_adaptive"]["rank2_hmm_brier"],
    }, indent=2))
