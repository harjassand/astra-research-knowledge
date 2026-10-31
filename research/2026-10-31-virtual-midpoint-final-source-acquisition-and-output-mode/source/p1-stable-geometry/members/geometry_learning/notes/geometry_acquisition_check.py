#!/usr/bin/env python3
"""Paid adaptive return-depth acquisition for the reflection counterfixture.

This is an ordinary retaining robust-phase learner, adopted as the constructive
comparator.  The family promise is explicit: two circle reflections, a known
unit-norm cosine seed, and fresh stationary endpoint-product returns.  It is not
a finite-data certificate of global rank two for an arbitrary contraction source.

The simulator aggregates samples of the EXACT physical endpoint-product law
  2*cos(X)*cos(X-n*theta) == cos(n*theta)+cos(2*X-n*theta), X uniform.
It executes that sample distribution numerically; every represented preparation,
readout, and primitive reflection is charged.  Its wall time is not physical time.
The proofs and finite-precision specification are in geometry_acquisition.md.
Numerical checks here use float64 and are diagnostics, not interval proofs.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ETA = 1.0 / 64.0
ANCHOR_THRESHOLD = 3.0 / 4.0
ALPHA = math.acos(ANCHOR_THRESHOLD - ETA)
PHASE_BUDGET = math.pi / 12.0
REPORT_BOUND = 2.0
REPORT_FRACTION_BITS = 10


def pow2_above(x: float) -> int:
    return 1 if x <= 1 else 1 << math.ceil(math.log2(x))


def circular_distance(a: float, b: float) -> float:
    return abs(math.remainder(a - b, 2.0 * math.pi))


class PaidSource:
    def __init__(self, theta: float, seed: int, mode: str = "physical_endpoint"):
        self.theta = theta
        self.rng = np.random.default_rng(seed)
        self.mode = mode
        self.episodes = 0
        self.primitive_steps = 0
        self.readouts = 0
        self.max_depth = 0

    def mean(self, n: int, shots: int) -> float:
        n = abs(n)
        c = math.cos(n * self.theta)
        self.episodes += shots
        self.primitive_steps += 2 * n * shots  # R is a two-reflection word.
        self.readouts += 2 * shots
        self.max_depth = max(self.max_depth, 2 * n)
        if self.mode == "randomized_bit":
            # Physical endpoint report z in [-2,2], randomized to +/-2 with
            # P(+2|z)=(z+2)/4.  The marginal count law below is exact.
            plus = int(self.rng.binomial(shots, (1.0 + c / 2.0) / 2.0))
            return 2.0 * (2.0 * plus / shots - 1.0)
        if self.mode != "physical_endpoint":
            raise ValueError(self.mode)
        total_grid_units = 0
        left = shots
        while left:
            batch = min(left, 65536)
            u = self.rng.uniform(0.0, 2.0 * math.pi, batch)
            # Finite report precision is charged and included in the proof.
            # Each value has rounding bias at most 2^(-11), below ETA/4.
            reports = c + np.cos(u)
            grid_units = np.rint(reports * (1 << REPORT_FRACTION_BITS)).astype(np.int64)
            total_grid_units += int(grid_units.sum())
            left -= batch
        return total_grid_units / ((1 << REPORT_FRACTION_BITS) * shots)

    def bill(self) -> dict:
        return {
            "episodes_and_stationary_preparations": self.episodes,
            "primitive_reflections": self.primitive_steps,
            "endpoint_readouts": self.readouts,
            "max_return_depth": self.max_depth,
            "unit_cost_total_if_prep_and_readout_each_cost_one": (
                self.primitive_steps + self.episodes + self.readouts
            ),
        }


class RetainedMoments:
    def __init__(self, source: PaidSource, delta: float):
        self.source = source
        self.delta = delta
        self.values = {0: 1.0}  # Known normalization in this explicit family.
        self.log = []

    def get(self, n: int) -> float:
        n = abs(n)
        if n in self.values:
            return self.values[n]
        index = len(self.log) + 1
        failure = self.delta / (index * (index + 1))
        shots = math.ceil(
            # Statistical tolerance ETA/2; report and arithmetic rounding use
            # the remaining ETA/2.  This is four times the ideal-real shot bill.
            8.0 * REPORT_BOUND**2 / ETA**2 * math.log(2.0 / failure)
        )
        estimate_raw = self.source.mean(n, shots)
        estimate = min(1.0, max(-1.0, estimate_raw))
        self.values[n] = estimate
        self.log.append({
            "moment_index": n,
            "query_number": index,
            "shots": shots,
            "return_depth": 2 * n,
            "confidence_allocation": failure,
            "estimate": estimate,
        })
        return estimate


def acquire(moments: RetainedMoments, horizon: int, epsilon: float) -> dict:
    """All normalized scalar word responses of length <= horizon to epsilon.

    Matrix representations are exact symbolic reflections at the learned phase.
    Evaluation uses a phase index, avoiding a floating matrix stability assumption.
    """
    cap = pow2_above(ALPHA * horizon / math.sqrt(epsilon))
    anchor = None
    k = 1
    failed_anchor_trials = 0
    while k <= cap:
        ck = moments.get(k)
        if abs(ck) <= ANCHOR_THRESHOLD:
            anchor = k
            break
        failed_anchor_trials += 1
        k *= 2

    if anchor is None:
        sign = 1 if moments.get(1) >= 0.0 else -1
        return {
            "dimension": 1,
            "mode": "family_promised_task_resolution_collapse",
            "sign": sign,
            "theta_hat": 0.0 if sign == 1 else math.pi,
            "anchor_cap": cap,
            "unsuccessful_anchor_trials": failed_anchor_trials,
            "family_promise_required": True,
            "generic_rank_certificate": False,
            "analytic_scalar_error_bound": ALPHA**2 * horizon**2 / (2 * cap**2),
        }

    cq = moments.get(anchor)
    sq = math.sqrt(1.0 - cq * cq)
    largest = pow2_above(2.0 * PHASE_BUDGET * horizon / epsilon)
    phase = 0.0
    levels = []
    n = 1
    while n <= largest:
        cn = moments.get(n)
        cnq = moments.get(n - anchor)
        quadrature = (cnq - cn * cq) / sq
        folded = math.atan2(quadrature, cn)
        if n == 1:
            phase = folded
        else:
            branch = round((n * phase - folded) / (2.0 * math.pi))
            phase = (folded + 2.0 * math.pi * branch) / n
        levels.append({"power": n, "phase_estimate": phase})
        n *= 2

    return {
        "dimension": 2,
        "mode": "adopted_retaining_robust_phase_estimation",
        "theta_hat": phase,
        "anchor": anchor,
        "anchor_cap": cap,
        "unsuccessful_anchor_trials": failed_anchor_trials,
        "largest_phase_power": largest,
        "anchor_measured_gram_condition": (1.0 + abs(cq)) / (1.0 - abs(cq)),
        "analytic_scalar_error_bound": PHASE_BUDGET * horizon / largest,
        "family_promise_required": True,
        "generic_rank_certificate": False,
        "levels": levels,
    }


def add_truth_diagnostics(model: dict, moments: RetainedMoments, theta: float) -> None:
    """Audit only, called after acquisition; truth never enters its decisions."""
    for query in moments.log:
        error = abs(query["estimate"] - math.cos(query["moment_index"] * theta))
        query["absolute_error_diagnostic"] = error
        query["within_promised_tolerance_diagnostic"] = error <= ETA
    if model["dimension"] == 2:
        anchor = model["anchor"]
        ctrue = math.cos(anchor * theta)
        orientation = 1 if math.sin(anchor * theta) >= 0.0 else -1
        model["anchor_true_gram_condition"] = (1 + abs(ctrue)) / (1 - abs(ctrue))
        model["phase_error_diagnostic"] = circular_distance(
            model["theta_hat"], orientation * theta
        )


def verify_model(model: dict, theta: float, horizon: int) -> dict:
    # Every A/B word of length <= H produces an integer index |n|<=H.
    # Checking all n therefore covers the scalar output of every such word.
    errors = [
        abs(math.cos(n * theta) - math.cos(n * model["theta_hat"]))
        for n in range(horizon + 1)
    ]
    worst = max(range(horizon + 1), key=errors.__getitem__)
    return {"max_scalar_error": errors[worst], "worst_phase_index": worst}


def bernoulli_kl(p: float, q: float) -> float:
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))


def lower_bound_checks() -> dict:
    rows = []
    for horizon in [4, 8, 32, 128, 1024]:
        for epsilon in [1/64, 1/32, 1/16]:
            theta0 = 1 / horizon
            theta1 = (1 + 16 * epsilon) / horizon
            step_kl = bernoulli_kl(theta0 / 2, theta1 / 2)
            task_gap = (1 - theta0)**horizon - (1 - theta1)**horizon
            ratios = []
            for depth in [1, 2, horizon, 2*horizon, 8*horizon]:
                p = (1 + (1-theta0)**depth) / 2
                q = (1 + (1-theta1)**depth) / 2
                ratios.append(bernoulli_kl(p, q) / (depth * step_kl))
            rows.append({
                "horizon": horizon, "epsilon": epsilon,
                "task_gap_over_epsilon": task_gap / epsilon,
                "step_kl_over_epsilon_squared_per_horizon": (
                    step_kl * horizon / epsilon**2
                ),
                "max_endpoint_kl_over_full_path_kl": max(ratios),
            })
    assert min(r["task_gap_over_epsilon"] for r in rows) > 2
    assert max(r["step_kl_over_epsilon_squared_per_horizon"] for r in rows) < 256
    assert max(r["max_endpoint_kl_over_full_path_kl"] for r in rows) <= 1 + 1e-8
    phase_rows = []
    for horizon in [1, 2, 3, 4, 7, 32, 128, 1024]:
        n = (horizon + 1) // 2
        word = "B" + "AB" * (n - 1)
        reached_index = 0
        for letter in word:
            reached_index = -reached_index if letter == "A" else 1-reached_index
        assert reached_index == n
        assert len(word) == 2*n-1 <= horizon
        for epsilon in [1/64, 1/8]:
            theta0 = math.pi/(2*n)
            theta1 = theta0 + 4*epsilon/n
            task_gap = abs(math.cos(n*theta0)-math.cos(n*theta1))
            assert task_gap > 2*epsilon
            assert 3*n/(8*epsilon) >= 3*horizon/(16*epsilon)
            phase_rows.append({
                "primitive_horizon": horizon,
                "reachable_phase_index": n,
                "target_word_length": len(word),
                "epsilon": epsilon,
                "task_gap_over_epsilon": task_gap/epsilon,
                "lower_bound_prefactor_before_binary_kl": 3*n/(8*epsilon),
            })
    return {
        "rank_one_reversible_chain_checks": rows,
        "phase_lower_bound_horizon_checks": phase_rows,
    }


def run() -> dict:
    horizon, epsilon, delta = 256, 0.02, 0.01
    angles = [
        ("zero", 0.0),
        ("below_task_resolution", 1e-5),
        ("old_rho_1_over_64", 2.0 * math.atan(1/64)),
        ("old_rho_1_over_16", 2.0 * math.atan(1/16)),
        ("interior", 1.3),
        ("rational_phase", math.pi/3),
        ("near_pi", math.pi-1e-5),
        ("pi", math.pi),
    ]
    cases = []
    for i, (label, theta) in enumerate(angles):
        source = PaidSource(theta, seed=47001+i)
        moments = RetainedMoments(source, delta)
        model = acquire(moments, horizon, epsilon)
        add_truth_diagnostics(model, moments, theta)
        verify = verify_model(model, theta, horizon)
        good = all(q["within_promised_tolerance_diagnostic"] for q in moments.log)
        assert good
        assert verify["max_scalar_error"] <= epsilon
        c = abs(math.cos(theta))
        short_condition = None if c == 1.0 else (1+c)/(1-c)
        cases.append({
            "label": label, "theta": theta,
            "short_basis_gram_condition": short_condition,
            "model": model,
            "verification": verify,
            "all_moments_within_tolerance_diagnostic": good,
            "distinct_sampled_moments": len(moments.log),
            "max_moment_error_diagnostic": max(q["absolute_error_diagnostic"] for q in moments.log),
            "bill": source.bill(),
            "moment_log": moments.log,
        })

    retained = []
    source = PaidSource(2.0 * math.atan(1/64), 47099)
    moments = RetainedMoments(source, delta)
    previous_bill = source.bill()
    previous_queries = 0
    for h in [64, 256, 1024]:
        model = acquire(moments, h, epsilon)
        add_truth_diagnostics(model, moments, source.theta)
        verify = verify_model(model, source.theta, h)
        assert verify["max_scalar_error"] <= epsilon
        bill = source.bill()
        retained.append({
            "horizon": h,
            "dimension": model["dimension"],
            "anchor": model.get("anchor"),
            "new_distinct_moments": len(moments.log)-previous_queries,
            "new_episodes": bill["episodes_and_stationary_preparations"]-previous_bill["episodes_and_stationary_preparations"],
            "new_primitive_reflections": bill["primitive_reflections"]-previous_bill["primitive_reflections"],
            "cumulative_bill": bill,
            "verification": verify,
        })
        previous_bill, previous_queries = bill, len(moments.log)

    return {
        "status": "all_numerical_diagnostics_passed",
        "date": "2026-10-31",
        "scope": "explicit rank-two reflection family; no generic rank certificate",
        "comparator": "ordinary retaining robust phase learner, adopted without an advantage claim",
        "source": "fresh uniform circle preparation; actual endpoint-product report law in [-2,2]",
        "report_precision": {"fraction_bits": REPORT_FRACTION_BITS, "max_rounding_bias": 2**(-REPORT_FRACTION_BITS-1)},
        "precision": "float64 diagnostics; theorem states independent finite-precision budget",
        "parameters": {"horizon": horizon, "epsilon": epsilon, "delta": delta, "moment_eta": ETA},
        "constants": {"first_crossing_angle": ALPHA, "unwrap_angle_budget": PHASE_BUDGET, "max_true_anchor_gram_condition": 113/15},
        "cases": cases,
        "retained_horizon_extensions": retained,
        "lower_bound_diagnostics": lower_bound_checks(),
    }


if __name__ == "__main__":
    result = run()
    path = Path(__file__).with_name("geometry_acquisition_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "cases": [{
            "label": c["label"],
            "dimension": c["model"]["dimension"],
            "anchor": c["model"].get("anchor"),
            "moments": c["distinct_sampled_moments"],
            "episodes": c["bill"]["episodes_and_stationary_preparations"],
            "primitive_reflections": c["bill"]["primitive_reflections"],
            "max_error": c["verification"]["max_scalar_error"],
        } for c in result["cases"]],
        "retained_horizon_extensions": result["retained_horizon_extensions"],
        "output": str(path),
    }, indent=2))
