"""Join the acquired data-only model to the implemented conditional compiler.

The expensive exact/positive reference is accessed only after the learned
model and conditional samples have been computed.  It is a small-system
check, not an input or subroutine of the learner/compiler.
"""
from __future__ import annotations
import gc
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "new_rare_event"))
from source_fixture import scrambled_chain, or_cycle
from event_time_compiler import (LocalRate, LogFactor, make_event_time_factor,
    eliminate, sample_reactive, exact_ctmc_probability)
from aging_event_time_compiler import (WeibullThreshold, make_threshold_factor,
    sample_aging_reactive)
from check_aging_compiler import independent_quadrature
from direct_event_time_baseline import completed_log_density_batch


def build(rates, clocks, N, T, order):
    q = N + 1
    if clocks is None:
        factors = [make_event_time_factor(i, rate, N, T) for i, rate in enumerate(rates)]
    else:
        factors = [make_threshold_factor(i, rate, clocks[i], N, T)
                   for i, rate in enumerate(rates)]
    for i in range(len(rates)):
        mask = np.zeros(q)
        mask[-1] = -np.inf
        factors.append(LogFactor((i,), mask))
    return eliminate(factors, len(rates), q, order=order)


def truth_tables(source):
    out = []
    for v, parents in enumerate(source.parents):
        table = []
        for code in range(1 << len(parents)):
            mask = sum(1 << p for j, p in enumerate(parents) if code & (1 << j))
            table.append(source.truth_rate(v, mask))
        out.append(LocalRate(tuple(parents), np.asarray(table)))
    return out


def main():
    acquisitions = json.loads((HERE / "acquisition_results.json").read_text())
    result = []
    rng = np.random.default_rng(8931)
    for name, N, T in [("scrambled_chain", 1024, .002),
                       ("aging_or_cycle", 96, .01)]:
        row = next(r for r in acquisitions if r["name"] == name)
        n, rho = row["n"], row["rho"]
        rates = [LocalRate(tuple(r["parents"]), np.asarray(r["table"])) for r in row["learned"]]
        clocks = (None if name == "scrambled_chain" else
                  [WeibullThreshold(k) for k in row["shapes"]])
        D = n if clocks is None else sum(c.shape for c in clocks)
        start = time.perf_counter()
        compiled = build(rates, clocks, N, T, row["acquired_order"])
        elapsed = time.perf_counter() - start
        lower = math.exp(compiled.log_probability)
        samples, changes, maximum_time = [], 0, 0.0
        for _ in range(250):
            draw = (sample_reactive(rates, compiled, T, rng) if clocks is None else
                    sample_aging_reactive(rates, clocks, compiled, T, rng))
            assert np.all(draw["times"] <= T * (1 + 1e-10))
            changes += int(not np.array_equal(np.argsort(draw["held_times"]), np.argsort(draw["times"])))
            maximum_time = max(maximum_time, float(max(draw["times"])))
            if len(samples) < 8:
                samples.append(draw["times"].tolist())
        peak, width = compiled.peak_entries, compiled.width
        del compiled
        gc.collect()
        upper_rates = [LocalRate(r.parents, math.exp(rho) * r.table) for r in rates]
        upper_compiled = build(upper_rates, clocks, N + n, T * (1 + n / N), row["acquired_order"])
        upper = math.exp(upper_compiled.log_probability)
        del upper_compiled
        gc.collect()

        # The ordinary comparator receives exactly the acquired rates.  It
        # pays the SAME calibration.  It is not given the true dense model.
        comparator = None
        if clocks is None:
            proposal_count = 100_000
            t0 = time.perf_counter()
            proposals = rng.uniform(0, T, size=(proposal_count, n))
            weights = np.exp(completed_log_density_batch(rates, proposals) + n * math.log(T))
            proposal_time = time.perf_counter() - t0
            envelope = T**n * math.prod(float(r.table.max()) for r in rates)
            acquired_reference = exact_ctmc_probability(rates, T)
            comparator = {"proposal_count": proposal_count,
                          "same_acquired_model_probability_estimate": float(weights.mean()),
                          "same_acquired_model_reference": acquired_reference,
                          "estimated_relative_SE": float(weights.std(ddof=1) / math.sqrt(proposal_count) / weights.mean()),
                          "density_evaluation_seconds": proposal_time,
                          "expected_rejection_proposals_per_path": envelope / acquired_reference,
                          "conclusion": "Ordinary importance sampling is strong on this vignette; no practical superiority claim."}
            source, _ = scrambled_chain(rho=rho)
            reference = exact_ctmc_probability(truth_tables(source), T)
            refinement = None
        else:
            source = or_cycle(seed=900, shapes=row["shapes"])
            truth = truth_tables(source)
            ref40 = independent_quadrature(truth, clocks, T, 40)
            reference = independent_quadrature(truth, clocks, T, 64)
            refinement = abs(ref40 / reference - 1)
        retention = math.exp(-D * rho) * (1 - n / N) ** D
        assert lower <= reference * (1 + 2e-6)
        assert reference <= upper * (1 + 2e-6)
        assert lower / reference >= retention - 2e-6
        result.append({
            "name": name, "n": n, "rho": rho, "D": D, "deadline": T,
            "bins": N, "acquired_width": width, "peak_factor_entries": peak,
            "source_exact_parent_count": [len(p) for p in source.parents],
            "learned_parent_count": [len(r.parents) for r in rates],
            "source_shots_including_failed_degrees": row["total_resets_including_failed_degrees"],
            "source_exposure_including_failed_degrees": row["total_exposure_including_failed_degrees"],
            "compiled_lower_probability": lower, "compiled_upper_probability": upper,
            "validation_only_true_probability": reference,
            "quadrature_refinement_relative_agreement": refinement,
            "actual_relative_deficit": 1 - lower / reference,
            "theorem_probability_relative_deficit_bound": 1 - retention,
            "theorem_per_path_TV_bound_ideal_continuous": 2 - math.exp(-D * rho) - (1 - n / N) ** D,
            "conditional_path_draws": 250, "all_draws_satisfy_deadline": True,
            "changed_trigger_orders_during_replay": changes,
            "largest_sample_time": maximum_time, "first_eight_paths": samples,
            "compiler_preprocess_seconds": elapsed, "ordinary_comparator": comparator,
            "numerical_scope": "Synthetic counts and floating calculations, no interval certificate or empirical TV certification"
        })
    (HERE / "end_to_end_results.json").write_text(json.dumps(result, indent=2))
    print(json.dumps([{k: v for k, v in r.items() if k != "first_eight_paths"} for r in result], indent=2))


if __name__ == "__main__":
    main()
