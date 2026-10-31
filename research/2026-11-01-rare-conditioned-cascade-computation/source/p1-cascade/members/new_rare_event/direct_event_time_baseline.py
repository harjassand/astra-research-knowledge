"""An equally informed ordinary importance/rejection comparator.

For the all-components-by-T event, independent uniform failure times on
[0,T]^n give a simple positive importance sampler.  This is deliberately
included because the tiny-deadline compiler vignette does not demonstrate
practical superiority over ordinary methods.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np

from event_time_compiler import LocalRate, exact_ctmc_probability
from check_event_time_compiler import chain


def completed_log_density_batch(rates: list[LocalRate], times: np.ndarray) -> np.ndarray:
    count, n = times.shape
    result = np.zeros(count)
    for i, rate in enumerate(rates):
        own = times[:, i]
        current_code = np.zeros(count, dtype=np.int64)
        for k, parent in enumerate(rate.parents):
            current_code += (times[:, parent] < own).astype(np.int64) << k
        exposure = np.zeros(count)
        for code, value in enumerate(rate.table):
            lower = np.zeros(count)
            upper = own.copy()
            for k, parent in enumerate(rate.parents):
                if code & (1 << k):
                    lower = np.maximum(lower, times[:, parent])
                else:
                    upper = np.minimum(upper, times[:, parent])
            exposure += value * np.maximum(upper - lower, 0)
        selected = rate.table[current_code]
        with np.errstate(divide="ignore"):
            result += np.log(selected) - exposure
    return result


def main():
    rng = np.random.default_rng(71961)
    rates = chain(10)
    n, deadline, proposals = len(rates), 1e-4, 100_000
    start = time.perf_counter()
    times = rng.uniform(0, deadline, size=(proposals, n))
    log_weights = completed_log_density_batch(rates, times) + n * math.log(deadline)
    weights = np.exp(log_weights)
    elapsed = time.perf_counter() - start
    exact = exact_ctmc_probability(rates, deadline)
    envelope = deadline ** n * math.prod(float(rate.table.max()) for rate in rates)
    assert np.max(weights) <= envelope * (1 + 1e-12)
    accepted = rng.random(proposals) <= weights / envelope
    result = {
        "task": "Same acquired local rates and same all-fail-by-T query as the compiler vignette",
        "n": n, "deadline": deadline, "proposals": proposals,
        "proposal": "Independent uniform event times on [0,T]^n",
        "importance_probability_estimate": float(weights.mean()),
        "positive_uniformization_reference": exact,
        "realized_relative_error": float(weights.mean() / exact - 1),
        "estimated_relative_standard_error": float(weights.std(ddof=1) / np.sqrt(proposals) / weights.mean()),
        "second_moment_ratio_estimate": float(np.mean(weights ** 2) / weights.mean() ** 2),
        "source_free_density_evaluation_seconds_this_run": elapsed,
        "rejection_envelope": envelope,
        "reference_expected_proposals_per_exact_reactive_sample": envelope / exact,
        "reactive_samples_accepted": int(accepted.sum()),
        "observed_proposals_per_accepted_path": proposals / int(accepted.sum()),
        "conclusion": "Ordinary event-time importance/rejection sampling is already effective on this vignette. The compiler example demonstrates the construction, not a practical speed advantage. The comparator does not supply a polynomial relative-variance guarantee over the whole bounded-width model class.",
    }
    Path(__file__).with_name("direct_baseline_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
