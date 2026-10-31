"""Meaningful small checks and worked examples for trace_confidence.py."""

from dataclasses import asdict
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from trace_confidence import (
    BlockObservation,
    TraceConfidenceSet,
    confidence_set_from_observations,
    gamma_deviance,
    gamma_shape_interval,
)


def summarize(confidence):
    return {
        "lower_sizes": confidence.lower_sizes,
        "upper_sizes": confidence.upper_sizes,
        "ambient_dimension": confidence.ambient_dimension,
    }


def observations(r, m, q, rng):
    return [BlockObservation(int(ra), int(min(ma, q * ra)), q,
                             float(rng.gamma(q * ra * ma)))
            for ra, ma in zip(r, m)]


def run_checks():
    rng = np.random.default_rng(831701)
    result = {}

    # The objective contains arbitrary signs.  Verify against an independent
    # general-purpose linear-program solver, rather than duplicating greed.
    worst_difference = 0.0
    optimizer_cases = 0
    for dimension in range(1, 9):
        for _ in range(8):
            truth = rng.integers(1, 30, dimension).astype(float)
            lower = np.maximum(0, truth - rng.random(dimension) * truth)
            upper = truth + rng.random(dimension) * 25
            total = int(sum(truth))
            box = TraceConfidenceSet(tuple(lower), tuple(upper), total)
            tight = box.tighten_total()
            assert tight.contains(truth)
            slopes = rng.normal(size=dimension)
            bounds = tight.trace_bounds(slopes)
            for sign, got in ((1, bounds.lower), (-1, bounds.upper)):
                lp = linprog(sign * slopes, A_eq=np.ones((1, dimension)),
                             b_eq=[total], bounds=list(zip(lower, upper)), method="highs")
                assert lp.success
                difference = abs(got - sign * lp.fun)
                worst_difference = max(worst_difference, difference)
                assert difference < 1e-8
            assert tight.contains(bounds.minimizing_sizes, 1e-7)
            assert tight.contains(bounds.maximizing_sizes, 1e-7)
            optimizer_cases += 1
    result["greedy_vs_independent_linear_program"] = {
        "cases": optimizer_cases,
        "maximum_absolute_difference": worst_difference,
    }

    # Inversion endpoints must satisfy the defining deviance equation, except
    # for the explicit lower endpoint at zero.
    maximum_endpoint_residual = 0.0
    for w in (1e-6, 0.1, 1, 5, 10, 100, 1e4, 1e8):
        for t in (0.1, 1, 5, 20):
            lo, hi = gamma_shape_interval(w, t)
            assert lo <= w <= hi
            for endpoint in ((lo, hi) if lo > 0 else (hi,)):
                error = abs(gamma_deviance(w, endpoint) - t)
                maximum_endpoint_residual = max(maximum_endpoint_residual, error)
                assert error < 1e-6
            if w <= t:
                assert lo == 0
    result["deviance_inversion"] = {
        "cases": 32,
        "maximum_endpoint_deviance_residual": maximum_endpoint_residual,
    }

    # Equality m=q*r must stay unresolved.  The known ambient size can then
    # determine that multiplicity even though the cyclic rank alone cannot.
    block_data = observations([2, 3], [1, 6], 2, rng)
    raw = confidence_set_from_observations(block_data, 20, delta=0.05, tighten_total=False)
    tight = confidence_set_from_observations(block_data, 20, delta=0.05)
    assert not block_data[1].resolved
    assert tight.lower_sizes == tight.upper_sizes == (2.0, 18.0)
    for extreme_energy in (1e-200, 1e200):
        altered = [block_data[0], BlockObservation(3, 6, 2, extreme_energy)]
        deterministic = confidence_set_from_observations(altered, 20, delta=0.05)
        assert deterministic.lower_sizes == deterministic.upper_sizes == (2.0, 18.0)
    result["single_unresolved_block_becomes_exact"] = {
        "observations": [asdict(x) for x in block_data],
        "true_sizes": [2, 18],
        "before_known_total": summarize(raw),
        "after_known_total": summarize(tight),
        "identity_trace": asdict(tight.trace_bounds([1, 1])),
        "extreme_tail_energy_does_not_change_exact_deduction": True,
    }

    # Several uncertain multiplicities remain; the known total tightens their
    # coordinate intervals and makes the identity trace exactly known.
    block_data = observations([1, 2, 3], [2, 8, 12], 3, rng)
    raw = confidence_set_from_observations(block_data, 54, delta=0.05, tighten_total=False)
    tight = raw.tighten_total()
    assert raw.contains([2, 16, 36]) and tight.contains([2, 16, 36])
    result["known_total_tightening"] = {
        "true_sizes": [2, 16, 36],
        "before_known_total": summarize(raw),
        "after_known_total": summarize(tight),
        "unconstrained_identity_interval": [sum(raw.lower_sizes), sum(raw.upper_sizes)],
        "identity_trace": asdict(tight.trace_bounds([1, 1, 1])),
    }

    # Positive-cone relative accuracy must not be misreported as relative
    # accuracy for a signed trace.  Here the true trace cancels to exactly zero.
    block_data = observations([1, 1], [50, 50], 4, rng)
    confidence = confidence_set_from_observations(block_data, 100, delta=0.05)
    signed = confidence.trace_bounds([1, -1])
    plugin_signed = (block_data[0].energy - block_data[1].energy) / 4
    assert signed.lower <= 0 <= signed.upper
    assert abs(plugin_signed) > 1e-3
    result["indefinite_cancellation"] = {
        "true_sizes": [50, 50],
        "future_slopes": [1, -1],
        "true_trace": 0,
        "unconstrained_plugin_trace": plugin_signed,
        "confidence_trace_interval": asdict(signed),
        "interpretation": "The absolute interval is valid; relative error at trace zero is undefined.",
    }

    # The future query is chosen from the observations: ask for the central
    # projection of the most uncertain component, not a fixed component.
    block_data = observations([1, 2, 3, 1], [8, 4, 7, 30], 2, rng)
    confidence = confidence_set_from_observations(block_data, 67, delta=0.05)
    widths = np.asarray(confidence.upper_sizes) - confidence.lower_sizes
    selected = int(np.argmax(widths))
    slopes = np.eye(4)[selected]
    adaptive = confidence.trace_bounds(slopes)
    truth = [8, 8, 21, 30][selected]
    assert adaptive.lower <= truth <= adaptive.upper
    result["adaptive_maximum_uncertainty_query"] = {
        "true_sizes": [8, 8, 21, 30],
        "confidence_set": summarize(confidence),
        "selected_block_after_observing_data": selected,
        "selected_block_true_trace": truth,
        "selected_block_interval": asdict(adaptive),
        "extra_query_failure_budget": 0,
    }

    # Modest simulation checks simultaneous rather than single-query coverage.
    # Empty sets count as failures, rather than being silently repaired.
    trials = 2000
    delta = 0.05
    simultaneous_misses = adaptive_query_misses = empty_sets = 0
    for _ in range(trials):
        block_data = observations([1, 2, 3, 1], [8, 4, 7, 30], 2, rng)
        try:
            confidence = confidence_set_from_observations(block_data, 67, delta=delta)
        except ValueError:
            empty_sets += 1
            simultaneous_misses += 1
            adaptive_query_misses += 1
            continue
        true_sizes = [8, 8, 21, 30]
        simultaneous_misses += not confidence.contains(true_sizes)
        widths = np.asarray(confidence.upper_sizes) - confidence.lower_sizes
        selected = int(np.argmax(widths))
        adaptive = confidence.trace_bounds(np.eye(4)[selected])
        adaptive_query_misses += not adaptive.lower <= true_sizes[selected] <= adaptive.upper
    result["simultaneous_coverage_simulation"] = {
        "trials": trials,
        "nominal_simultaneous_failure_bound": delta,
        "observed_simultaneous_misses": simultaneous_misses,
        "observed_adaptively_selected_query_misses": adaptive_query_misses,
        "observed_empty_sets": empty_sets,
        "interpretation": "Numerical check only; the Chernoff and union-bound proof supplies the guarantee.",
    }
    return result


if __name__ == "__main__":
    results = run_checks()
    destination = Path(__file__).with_name("trace_confidence_checks.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
