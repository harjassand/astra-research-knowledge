"""Acquisition of an optimizer whose complexity is measured after the query.

Unknown arbitrary resource baseline, sparse cyclic context interactions,
unknown placement forest, dense quadratic perturbation, noisy scalar source.
The learner sees only prepared input reports; true coefficients are used by
the independent scorer. Source simulation and noise are a float prototype;
the compiled consumer and certificate statistics use exact rational arithmetic.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "consequence_mechanism"))
from conditional_forest import (ModuleConditionalForestModel,
                                project_conditional_coefficients,
                                make_cyclic_cross_fixture)
from orbit_certificate import (module_features, module_orbit_pairs,
                               statistical_validate_group_action)
from module_quotient import PreparedEnergySource, query_checks, project_forest


def acquire(source, k, rows, cross_budget, iterations, seed, repetitions=1):
    """No coefficients, useful graph or optimizer are passed into acquisition."""
    rng = np.random.default_rng(seed)
    x, random_cost = module_orbit_pairs(rng, rows, 2*k)
    phi = module_features(x)
    design = (phi[0::2]-phi[1::2])/math.sqrt(2)
    del phi
    before = source.costs()
    observed = source.measure_many(x, repetitions)
    y = (observed[0::2]-observed[1::2])/math.sqrt(2)
    after = source.costs()
    D = design.shape[1]
    theta = np.zeros(D)
    records = []
    start = time.perf_counter()
    stable = 0
    previous_support = None
    for t in range(iterations):
        proposal = theta+design.T@(y-design@theta)/rows
        new = project_conditional_coefficients(k, proposal, cross_budget)
        difference = float(np.linalg.norm(new-theta))
        theta = new
        support = tuple(np.flatnonzero(theta))
        stable = stable+1 if support == previous_support else 0
        previous_support = support
        if not np.all(np.isfinite(theta)) or np.linalg.norm(theta) > 1.e10:
            raise RuntimeError("Candidate acquisition diverged; it is not an accepted service")
        if t % 10 == 0 or t == iterations-1:
            records.append({"iteration": t+1, "coefficient_change": difference,
                            "training_RMS": float(np.linalg.norm(design@theta-y)/math.sqrt(rows))})
        if difference < 1.e-10 and stable >= 5:
            break
    support = np.flatnonzero(theta)
    fitted, _, rank, singular = np.linalg.lstsq(design[:, support], y, rcond=None)
    theta[:] = 0.
    theta[support] = fitted
    candidate = ModuleConditionalForestModel.from_coefficients(k, theta, cross_budget, grid_bits=40)
    return candidate, {
        "method": "paired_contrasts_conditional_forest_IHT_then_support_LS",
        "pair_rows": rows, "feature_dimension": D, "cross_budget": cross_budget,
        "actual_iterations": t+1, "step": 1., "iteration_record": records,
        "source_repetitions_per_report": repetitions,
        "source_cost": {key: after[key]-before[key] for key in before},
        **random_cost,
        "distinct_training_contexts": len({row.tobytes() for row in
            ((x[0::2].reshape(rows, k, 2).sum(axis=2)+2)//2)}),
        "support_refit_rank": int(rank),
        "support_refit_normalized_min_singular_value": float(singular[-1]/math.sqrt(rows)),
        "paired_training_RMS": float(np.linalg.norm(design@theta-y)/math.sqrt(rows)),
        "training_design_entries": int(rows*D),
        "retained_scalar_coefficients": k+len(candidate.qq_units)+len(candidate.cross_units),
        "retained_placement_edges": len(candidate.qq_units),
        "retained_context_cross_terms": len(candidate.cross_units),
        "compiled_orientation_grid_bits": candidate.grid_bits,
        "training_wall_seconds": time.perf_counter()-start,
        "universal_RIP_sufficient_constants_executed": False,
        "soundness_basis": "fresh independent certificate for actual rounded candidate"
    }


def run(k=64, rows=4096, iterations=150, seed=8431, training_only=False):
    theta, placement_tree, cross_support = make_cyclic_cross_fixture(k, seed, tail=.002)
    source = PreparedEnergySource(k, theta, amplitude=1.e4, sigma=.002, seed=seed+1)
    started = time.perf_counter()
    # Budget is a proposed representation size. It does not disclose identities,
    # coefficients or a useful graph. Failed sizes may be independently rejected.
    budget = min(4*k, k*(k-1))
    candidate, acquisition = acquire(source, k, rows, budget, iterations, seed+2)
    error = float(np.linalg.norm(theta-candidate.coefficient_vector()))
    grouped, _ = project_forest(theta, k)
    result = {"modules": k, "physical_controls": 2*k,
              "resource_contexts": str(3**k), "binary_configurations": str(4**k),
              "acquisition": acquisition,
              "source_noise_sigma": source.sigma, "nuisance_amplitude": 1.e4,
              "fixture_only_residual_norm": error,
              "fixture_only_best_grouped_forest_residual_norm": float(np.linalg.norm(theta-grouped)),
              "fixture_only_placement_tree_recovered": {(a,b) for a,b,_ in candidate.qq_units} == placement_tree,
              "fixture_only_context_cross_support_recovered": {(a,b) for a,b,_ in candidate.cross_units} == cross_support,
              "full_linear_reconstruction_underdetermined": rows < len(theta)}
    if not training_only:
        certificate = statistical_validate_group_action(
            source, candidate, .02, module_orbit_pairs, math.sqrt(2)*k,
            global_failure=.05, candidate_number=1, seed=seed+3,
            contrast_rounding_radius=1.e-8, exact_statistics=True,
            feature_radius_squared=2*k*k)
        result["certificate"] = certificate
        if not certificate["accepted"]:
            result["status"] = "candidate rejected; no design service issued"
        else:
            assert error <= certificate["quotient_residual_norm_upper"]+1.e-9
            result["status"] = "accepted under the stated source and rounding contract"
            result["adaptive_queries"] = query_checks(candidate, theta, certificate, 16, seed+4)
    result["total_source_cost"] = source.costs()
    result["largest_absolute_report"] = source.max_absolute_report
    result["total_wall_seconds"] = time.perf_counter()-started
    result["limitations"] = [
        "Synthetic controlled-input simulator; no physical preparation-time claim",
        "The simulator and statistical noise use floating PRNG arithmetic",
        "The 1e-8 report/contrast numeric guard is an explicit prototype assumption",
        "Exact certificate-statistic arithmetic and integer DP do not calibrate the instrument",
        "No advantage claimed over conventional sparse recovery using the same operation quotient",
        "Unbounded noninvariant higher-order errors and unnoticed resource changes are excluded"]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules", type=int, default=64)
    parser.add_argument("--rows", type=int, default=4096)
    parser.add_argument("--iterations", type=int, default=150)
    parser.add_argument("--seed", type=int, default=8431)
    parser.add_argument("--training-only", action="store_true")
    parser.add_argument("--output", default="conditional_design_results.json")
    args = parser.parse_args()
    result = run(args.modules, args.rows, args.iterations, args.seed, args.training_only)
    path = HERE/args.output
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"output": str(path), "training_shots": result["acquisition"]["source_cost"]["energy_samples"],
                      "true_residual_for_check_only": result["fixture_only_residual_norm"],
                      "certificate": result.get("certificate", {}).get("all_context_regret_upper"),
                      "accepted": result.get("certificate", {}).get("accepted"),
                      "total_source_cost": result["total_source_cost"],
                      "seconds": result["total_wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
