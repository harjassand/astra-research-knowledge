"""Executable checks of the theorem and the polynomial event-time compiler."""
from __future__ import annotations

import itertools
import json
import math
import time
from pathlib import Path

import numpy as np

from event_time_compiler import (
    LocalRate, compile_model, direct_held_probability, exact_ctmc_probability,
    sample_reactive, simulate_held_thresholds, simulate_thresholds,
)


def chain(n: int, base: float = 1.0, multiplier: float = 3.0):
    return [LocalRate((), np.array([base]))] + [
        LocalRate((i - 1,), np.array([base * (1 + 0.07 * i),
                                    multiplier * base * (1 + 0.07 * i)]))
        for i in range(1, n)
    ]


def ring(n: int):
    return [LocalRate(((i - 1) % n,), np.array([0.6 + 0.1 * i, 2.0 + 0.2 * i]))
            for i in range(n)]


def main():
    rng = np.random.default_rng(1209761)
    results = {}
    rates = ring(4)
    deadline, bins = 0.35, 24
    compiled = compile_model(rates, bins, deadline)
    direct = direct_held_probability(rates, bins, deadline)
    exact = exact_ctmc_probability(rates, deadline)
    approximate = math.exp(compiled.log_probability)
    assert abs(approximate / direct - 1) < 1e-11
    assert approximate <= exact * (1 + 1e-11)
    theoretical_retention = (1 - len(rates) / bins) ** len(rates)
    assert approximate / exact >= theoretical_retention - 1e-12
    normalized = compile_model(rates, bins, deadline, required=[])
    assert abs(math.expm1(normalized.log_probability)) < 1e-11
    partial = compile_model(rates, bins, deadline, required=[0, 2])
    partial_direct = direct_held_probability(rates, bins, deadline, required=[0, 2])
    assert abs(math.exp(partial.log_probability) / partial_direct - 1) < 1e-11
    results["factorization_and_variable_elimination"] = {
        "n": len(rates), "bins": bins, "deadline": deadline,
        "actual_elimination_width": compiled.width,
        "largest_bucket_entries": compiled.peak_entries,
        "delayed_probability_variable_elimination": approximate,
        "delayed_probability_full_state_check": direct,
        "undelayed_probability_full_state_check": exact,
        "actual_relative_bias": 1 - approximate / exact,
        "proved_relative_bias_bound": 1 - theoretical_retention,
        "normalization_error_without_event": abs(math.expm1(normalized.log_probability)),
        "partial_event_relative_difference": math.exp(partial.log_probability) / partial_direct - 1,
    }

    # Check common-threshold pathwise coupling on cyclic, nonlinear local
    # rates and a wide rate range.  These are separate from probability tests.
    max_lag, min_lag, path_count = 0.0, math.inf, 0
    largest_scale_ratio = 1.0
    for trial in range(50):
        n = 7
        bases = 10 ** rng.uniform(-2, 2, n)
        rates_random = []
        for i in range(n):
            parents = ((i - 1) % n, (i + 1) % n)
            increases = rng.uniform(0.1, 8.0, 3)
            table = bases[i] * np.array([1.0, 1 + increases[0], 1 + increases[1],
                                        1 + increases[0] + increases[1] + increases[2]])
            rates_random.append(LocalRate(parents, table))
        largest_scale_ratio = max(largest_scale_ratio,
                                  max(r.table.max() for r in rates_random) /
                                  min(r.table.min() for r in rates_random))
        step = 0.013
        for _ in range(20):
            thresholds = rng.exponential(size=n)
            truth = simulate_thresholds(rates_random, thresholds)
            delayed = simulate_held_thresholds(rates_random, thresholds, step)
            lag = delayed - truth
            assert lag.min() >= -1e-9
            assert lag.max() <= n * step + 1e-9
            max_lag = max(max_lag, float(lag.max()))
            min_lag = min(min_lag, float(lag.min()))
            path_count += 1
    results["pathwise_coupling"] = {
        "independent_paths": path_count, "nodes": 7, "bin_width": step,
        "largest_rate_ratio_tested": largest_scale_ratio,
        "min_delayed_minus_true": min_lag,
        "max_delayed_minus_true": max_lag,
        "proved_max_delay": 7 * step,
    }

    # This is a genuinely rare event.  The compiler itself uses only pair
    # factors and width-one elimination.  The 2**n comparator is separate.
    rates = chain(10)
    deadline, bins = 1e-4, 1000
    start = time.perf_counter()
    rare = compile_model(rates, bins, deadline)
    elapsed = time.perf_counter() - start
    exact_rare = exact_ctmc_probability(rates, deadline)
    approx_rare = math.exp(rare.log_probability)
    retention = (1 - len(rates) / bins) ** len(rates)
    assert retention - 1e-10 <= approx_rare / exact_rare <= 1 + 1e-10
    results["rare_probability"] = {
        "n": len(rates), "deadline": deadline, "bins": bins,
        "actual_elimination_width": rare.width,
        "largest_bucket_entries": rare.peak_entries,
        "log_probability_compiler": rare.log_probability,
        "probability_compiler": approx_rare,
        "probability_positive_uniformization_check": exact_rare,
        "relative_bias": 1 - approx_rare / exact_rare,
        "proved_relative_bias_bound": 1 - retention,
        "compiler_seconds_this_run": elapsed,
    }
    returned = 500
    max_conditional_lag = 0.0
    max_true_time = 0.0
    changed_order = 0
    for _ in range(returned):
        sample = sample_reactive(rates, rare, deadline, rng)
        times, held = sample["times"], sample["held_times"]
        lag = held - times
        assert lag.min() >= -1e-11
        assert lag.max() <= len(rates) * deadline / bins + 1e-11
        assert times.max() <= deadline * (1 + 1e-10)
        max_conditional_lag = max(max_conditional_lag, float(lag.max()))
        max_true_time = max(max_true_time, float(times.max()))
        changed_order += not np.array_equal(np.argsort(times), np.argsort(held))
    results["rare_conditioned_path_pullback"] = {
        "draws": returned, "all_returned_paths_satisfy_deadline": True,
        "largest_completion_time": max_true_time,
        "largest_delay_before_driver_pullback": max_conditional_lag,
        "paths_whose_event_order_changed_in_pullback": int(changed_order),
        "proved_conditional_law_TV_bound": 1 - retention,
        "status": "This bound is analytic. Sampling checks do not estimate or certify total variation.",
    }

    # Check one-sided monotone rate replacement and probability sandwich.
    zeta = 0.015
    lower_rates = [LocalRate(r.parents, (1 - zeta) * r.table) for r in rates]
    lower = compile_model(lower_rates, bins, deadline)
    true_lower = exact_ctmc_probability(lower_rates, deadline)
    assert (1 - zeta) ** len(rates) - 1e-10 <= true_lower / exact_rare <= 1 + 1e-10
    combined = (1 - zeta) ** len(rates) * retention
    probability = math.exp(lower.log_probability)
    assert probability <= exact_rare * (1 + 1e-10)
    assert exact_rare <= probability / combined * (1 + 1e-10)
    results["rate_and_time_composition"] = {
        "rate_fraction_error": zeta,
        "computed_probability_lower_bound": probability,
        "computed_probability_upper_bound": probability / combined,
        "reference_probability": exact_rare,
        "conditional_path_TV_bound": (1 - (1 - zeta) ** len(rates)) + (1 - retention),
    }
    output = Path(__file__).with_name("event_time_results.json")
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
