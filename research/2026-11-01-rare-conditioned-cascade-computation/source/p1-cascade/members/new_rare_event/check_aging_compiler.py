"""Check the root's non-Markovian Weibull-threshold generalization."""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss

from event_time_compiler import LocalRate, simulate_thresholds
from aging_event_time_compiler import (
    WeibullThreshold, compile_aging_model, sample_aging_reactive,
    completed_path_log_density,
)


def independent_quadrature(rates, clocks, deadline, order_nodes):
    """Small-n independent reference: integrate each failure-order cone.

    This does not enter the event-time compiler.  Gauss quadrature is a
    numerical reference, not a certified enclosure of the continuous law.
    """
    n = len(rates)
    points, weights = leggauss(order_nodes)
    points, weights = (points + 1) / 2, weights / 2
    mesh = np.meshgrid(*([points] * n), indexing="ij")
    weight_mesh = np.meshgrid(*([weights] * n), indexing="ij")
    joint_weight = np.prod(np.array(weight_mesh), axis=0)
    ordered_times = [deadline * np.prod(np.array(mesh[k:]), axis=0) for k in range(n)]
    durations = [ordered_times[0]] + [ordered_times[k] - ordered_times[k - 1]
                                      for k in range(1, n)]
    jacobian = np.full_like(joint_weight, deadline ** n)
    for k in range(1, n):
        jacobian *= mesh[k] ** k
    total = 0.0
    for ordering in itertools.permutations(range(n)):
        state = np.zeros(n, dtype=bool)
        hazards = np.zeros((n,) + joint_weight.shape)
        log_density = np.zeros_like(joint_weight)
        for rank, i in enumerate(ordering):
            for j in range(n):
                if not state[j]:
                    hazards[j] += rates[j].at_state(state) * durations[rank]
            log_density += np.log(rates[i].at_state(state)) + clocks[i].log_density(hazards[i])
            state[i] = True
        total += float(np.sum(joint_weight * jacobian * np.exp(log_density)))
    return total


def main():
    rng = np.random.default_rng(160328)
    rates = [LocalRate(((i - 1) % 3,), np.array([0.7 + 0.2 * i, 2.2 + 0.3 * i]))
             for i in range(3)]
    clocks = [WeibullThreshold(1.5, 1.1), WeibullThreshold(2.0, 0.8),
              WeibullThreshold(2.5, 1.3)]
    deadline, bins = 0.01, 160
    compiled = compile_aging_model(rates, clocks, bins, deadline)
    normalized = compile_aging_model(rates, clocks, 15, deadline, required=[])
    assert abs(math.expm1(normalized.log_probability)) < 1e-10
    dimension = sum(c.scaling_dimension for c in clocks)
    reference_64 = independent_quadrature(rates, clocks, deadline, 64)
    reference_96 = independent_quadrature(rates, clocks, deadline, 96)
    assert abs(reference_64 / reference_96 - 1) < 2e-6
    probability = math.exp(compiled.log_probability)
    retention = (1 - len(rates) / bins) ** dimension
    assert retention - 1e-6 <= probability / reference_96 <= 1 + 1e-6

    # The second held computation supplies a usable enclosure independent
    # of the quadrature reference and the original process state space.
    upper = compile_aging_model(rates, clocks, bins + len(rates),
                                deadline * (1 + len(rates) / bins))
    upper_probability = math.exp(upper.log_probability)
    assert probability <= reference_96 * (1 + 1e-6)
    assert reference_96 <= upper_probability * (1 + 1e-6)

    max_lag = 0.0
    for _ in range(300):
        sample = sample_aging_reactive(rates, clocks, compiled, deadline, rng)
        lag = sample["held_times"] - sample["times"]
        assert lag.min() >= -1e-12
        assert lag.max() <= len(rates) * deadline / bins + 1e-12
        assert sample["times"].max() <= deadline * (1 + 1e-12)
        max_lag = max(max_lag, float(lag.max()))

    rho = 0.04
    lower_rates = [LocalRate(rate.parents, rate.table * np.exp(np.array([-rho, -rho / 2])))
                   for rate in rates]
    smallest_log_ratio = math.inf
    for _ in range(1000):
        thresholds = np.array([clock.sample(rng) for clock in clocks])
        times = simulate_thresholds(rates, thresholds)
        true_log_density = completed_path_log_density(rates, clocks, times)
        lower_log_density = completed_path_log_density(lower_rates, clocks, times)
        log_ratio = lower_log_density - true_log_density
        assert log_ratio >= -rho * dimension - 1e-10
        smallest_log_ratio = min(smallest_log_ratio, log_ratio)

    output = {
        "clock_family": "Independent Weibull exposure thresholds; state process generally non-Markov",
        "nodes": len(rates), "shapes": [c.shape for c in clocks],
        "scaling_dimension_D": dimension, "bins": bins, "deadline": deadline,
        "actual_elimination_width": compiled.width,
        "largest_bucket_entries": compiled.peak_entries,
        "probability_compiler": probability,
        "positive_quadrature_reference_64": reference_64,
        "positive_quadrature_reference_96": reference_96,
        "quadrature_relative_agreement": reference_64 / reference_96 - 1,
        "actual_relative_bias_against_quadrature": 1 - probability / reference_96,
        "proved_relative_bias_bound": 1 - retention,
        "computable_probability_upper_bound": upper_probability,
        "computable_conditional_TV_bound": 1 - probability / upper_probability,
        "unconditioned_normalization_error": abs(math.expm1(normalized.log_probability)),
        "reactive_draws": 300, "all_paths_satisfy_deadline": True,
        "maximum_held_minus_replayed_time": max_lag,
        "path_density_checks": 1000, "rho": rho,
        "smallest_log_density_ratio": smallest_log_ratio,
        "proved_log_density_ratio_lower_bound": -rho * dimension,
        "limitations": "Floating arithmetic and finite random-bit outputs. The continuous-law TV theorem is analytic; finite stored paths require a rounded-output comparison, not TV to an ideal continuous density.",
    }
    Path(__file__).with_name("aging_results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
