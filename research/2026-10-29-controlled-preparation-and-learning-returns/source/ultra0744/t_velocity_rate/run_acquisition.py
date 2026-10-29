"""Fixed acquisition declared before execution, with all comparator costs.

12,000 independent outputs at t=0,1/4,1 for each exact-ideal recursive model;
16 independent finite-N populations, N=5,000 at t=1. No seed/parameter retries.
All executed arithmetic is binary64; Monte Carlo diagnostics are not proofs.
"""
from dataclasses import asdict
import json
import math
from pathlib import Path
import statistics
import time

from hard_sphere import HardSphere, Counts, axis_source, kac_population, norm2


def observables(v):
    r2 = norm2(v)
    return {"mass": 1.0, "energy": r2, "vx": v[0],
            "vx_squared": v[0]*v[0], "fourth_radial": r2*r2,
            "bounded_radial": 1.0/(1.0+r2),
            "bounded_angular": sum(x**4 for x in v)/(1.0+r2)**2,
            "cos_vx": math.cos(v[0])}


def summarize(values):
    n = len(values)
    mean = statistics.fmean(values)
    variance = statistics.variance(values) if n > 1 else 0.0
    return {"mean": mean, "empirical_standard_error": math.sqrt(variance/n),
            "min": min(values), "max": max(values)}


def exact_model_batch(mode, t, size, seed):
    started = time.perf_counter()
    engine = HardSphere(axis_source(), a=1.0, seed=seed)
    counts = Counts()
    observations = {}
    weights = []
    per_output_events = []
    for _ in range(size):
        previous = counts.events
        if mode == "normalized_currency":
            v, weight = engine.physical(t, counts), 1.0
        else:
            v, weight = engine.weighted(t, counts)
        weights.append(weight)
        per_output_events.append(counts.events-previous)
        for name, value in observables(v).items():
            observations.setdefault(name, []).append(weight*value)
    attempts = counts.final_attempts if mode == "normalized_currency" else size
    assert counts.exponentials == 2*counts.events+attempts
    assert counts.source_draws == counts.events+attempts
    result = {"mode": mode, "time": t, "size": size, "seed": seed,
              "elapsed_seconds": time.perf_counter()-started,
              "counts": asdict(counts), "events_per_output": summarize(per_output_events),
              "output_weight": summarize(weights),
              "observables": {name: summarize(values) for name,values in observations.items()},
              "weighted_CLT_assumed": False,
              "floating_implementation": True}
    if mode == "normalized_currency":
        result["final_success_fraction"] = size/counts.final_attempts
        result["iid_bounded_observable_sampling"] = True
        # Distribution-free simultaneous error radius for 3 bounded tests.
        # Each test is in [-1,1], union bound 6 exp(-n r^2/2).
        result["three_bounded_tests_Hoeffding_radius_99pct"] = math.sqrt(2*math.log(600)/size)
        result["hoeffding_scope"] = "ideal law/independent source; not binary64 solver certification"
    return result


def population_batch(size=5000, replicates=16, horizon=1.0):
    started = time.perf_counter()
    means, receipts = {}, []
    for replicate in range(replicates):
        values, costs = kac_population(axis_source(), size, horizon, seed=834800+replicate)
        columns = {}
        for v in values:
            for name, value in observables(v).items():
                columns.setdefault(name, []).append(value)
        for name, column in columns.items():
            means.setdefault(name, []).append(statistics.fmean(column))
        receipts.append(costs)
    return {"method": "continuous_time_finite_N_Kac",
            "size_each": size, "independent_replicates": replicates,
            "time": horizon, "elapsed_seconds": time.perf_counter()-started,
            "costs": receipts,
            "independent_population_mean_statistics": {k:summarize(v) for k,v in means.items()},
            "population_bias_bound_acquired": False,
            "pooled_particles_treated_iid": False}


def main():
    started = time.perf_counter()
    output_dir = Path(__file__).parent/"outputs"
    data = {"source": "uniform 6-axis unit velocities", "energy": 1,
            "a": 1, "angular_measure_mass": 1,
            "fixed_sample_plan": "12000 each mode at 0,.25,1; 16 Kac populations N5000 t1",
            "recursive": [], "binary64_is_not_exact_continuous_output": True}
    for mode_index, mode in enumerate(("normalized_currency", "Fournier_weighted")):
        for index, t in enumerate((0.0, 0.25, 1.0)):
            batch=exact_model_batch(mode,t,12000,834000+100*mode_index+index)
            data["recursive"].append(batch)
            print(mode,t,"seconds",round(batch["elapsed_seconds"],4),
                  "events",batch["counts"]["events"],flush=True)
            (output_dir/"ACQUISITION_PARTIAL.json").write_text(json.dumps(data,indent=2)+"\n")
    data["ordinary_finite_population"] = population_batch()
    data["elapsed_seconds_total"] = time.perf_counter()-started
    # Descriptive differences; weighted/population empirical SEs are not rigorous error bars.
    at1={b["mode"]:b for b in data["recursive"] if b["time"]==1.0}
    differences={}
    for name in ("bounded_radial","bounded_angular","cos_vx"):
        normalized=at1["normalized_currency"]["observables"][name]
        weighted=at1["Fournier_weighted"]["observables"][name]
        pop=data["ordinary_finite_population"]["independent_population_mean_statistics"][name]
        differences[name]={"currency_minus_weighted":normalized["mean"]-weighted["mean"],
                           "currency_minus_finiteN":normalized["mean"]-pop["mean"],
                           "combined_empirical_SE_weighted": math.hypot(normalized["empirical_standard_error"],weighted["empirical_standard_error"]),
                           "combined_empirical_SE_finiteN": math.hypot(normalized["empirical_standard_error"],pop["empirical_standard_error"])}
    data["descriptive_comparisons"] = differences
    (output_dir/"ACQUISITION.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({"elapsed_seconds_total":data["elapsed_seconds_total"],
                      "descriptive_comparisons":differences},indent=2))


if __name__ == "__main__":
    main()
