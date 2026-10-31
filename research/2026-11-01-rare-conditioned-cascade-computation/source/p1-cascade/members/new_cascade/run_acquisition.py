"""Run actual learner logic against synthetic binary-outcome experiments."""
from __future__ import annotations
from dataclasses import asdict
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "new_rare_event"))
from acquire_local_rates import RateAssay, learn_local_scopes, json_model, acquire_unknown_degree
from acquire_width import acquire_order
from source_fixture import scrambled_chain, or_cycle
from event_time_compiler import (LocalRate, make_event_time_factor, LogFactor,
                                 eliminate, thresholds_from_bins, simulate_thresholds)


def evaluate(source, assay, learned):
    maximum_log_underestimate = 0.0
    minimum_log_underestimate = math.inf
    spurious = []
    for v, item in enumerate(learned):
        spurious.extend((v, p) for p in item["parents"] if p not in source.latent_parents[v])
        for mask in range(1 << source.n):
            code = sum(int(bool(mask & (1 << p))) << j for j, p in enumerate(item["parents"]))
            truth = source.truth_rate(v, mask)
            ratio = math.log(truth / float(item["table"][code]))
            maximum_log_underestimate = max(maximum_log_underestimate, ratio)
            minimum_log_underestimate = min(minimum_log_underestimate, ratio)
    observed_assay_errors = [abs(value - math.log(source.truth_rate(v, mask)))
                             for (v, mask), value in assay.cache.items()]
    assert not spurious
    assert minimum_log_underestimate >= -1e-12
    assert maximum_log_underestimate <= assay.rho + 1e-12
    assert max(observed_assay_errors) <= assay.a
    return {"maximum_log_underestimate_over_all_source_states": maximum_log_underestimate,
            "minimum_log_underestimate_over_all_source_states": minimum_log_underestimate,
            "maximum_actual_assay_log_error": max(observed_assay_errors),
            "spurious_parents": spurious}


def main():
    rho, delta = 0.01, 0.01
    rows = []
    fixtures = [("scrambled_chain", *scrambled_chain(rho=rho)),
                ("or_cycle", or_cycle(), None),
                ("aging_or_cycle", or_cycle(seed=900, shapes=[1.5, 2, 2.5]), None)]
    for name, source, permutation in fixtures:
        start = time.perf_counter()
        learned, witnesses, assay, attempts = acquire_unknown_degree(
            source.experiment, source.n, 0.05, 5.0, rho, delta, shapes=source.shapes)
        scopes = [tuple(sorted((v,) + x["parents"])) for v, x in enumerate(learned)]
        order, width, width_cost = acquire_order(scopes, source.n, max_width=3)
        row = {"name": name, "n": source.n, "rho": rho,
               "shapes": source.shapes.tolist(), "source_parents_for_validation_only": source.parents,
               "latent_parents_for_validation_only": source.latent_parents,
               "dense_log_perturbation_bound": source.dense_beta,
               "learned": json_model(learned), "witnesses": witnesses,
               "acquired_order": order, "acquired_width": width,
               "width_search_states": width_cost,
               "calibration": assay.summary(), "degree_discovery_attempts": attempts,
               "total_resets_including_failed_degrees": sum(a["calibration"]["represented_independent_resets"] for a in attempts),
               "total_exposure_including_failed_degrees": sum(a["calibration"]["represented_total_exposure_time"] for a in attempts),
               "verification": evaluate(source, assay, learned),
               "wall_seconds_for_aggregate_simulation": time.perf_counter() - start}
        if permutation is not None:
            row["hidden_permutation_for_validation_only"] = permutation
        rows.append(row)
        (HERE / (name + "_observations.json")).write_text(
            json.dumps([asdict(o) for o in assay.observations], indent=2))
    (HERE / "acquisition_results.json").write_text(json.dumps(rows, indent=2))
    print(json.dumps([{ "name": r["name"], "width": r["acquired_width"],
                       "calibration": r["calibration"], "total_resets": r["total_resets_including_failed_degrees"],
                       "verification": r["verification"]}
                      for r in rows], indent=2))


if __name__ == "__main__":
    main()
