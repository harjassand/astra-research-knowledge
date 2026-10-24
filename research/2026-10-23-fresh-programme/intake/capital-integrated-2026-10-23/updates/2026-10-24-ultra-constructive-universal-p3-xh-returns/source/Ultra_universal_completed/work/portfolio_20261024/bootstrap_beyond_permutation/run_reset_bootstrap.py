#!/usr/bin/env python3
"""Execute fixed-budget count acquisition, a separate pure learner, then new experiments.

Usage: python3 run_reset_bootstrap.py --out-dir run_seed_20261024
No old predictive-depth data or code is modified or resampled.
"""
import argparse
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import private_plant


def jsonable(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator,
                "decimal": float(value)}
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def save(path, value):
    path.write_text(json.dumps(jsonable(value), indent=2)+"\n")


def learner_input(counts):
    """Whitelist the actual process boundary; retain costs/audit outside it."""
    return {"interface": {k: counts["interface"][k] for k in (
                "full_controlled_hankel_rank_upper_bound", "reset_control_durations")},
            "calibration": {
                "samples_per_setting": counts["calibration"]["samples_per_setting"],
                "error_width": counts["calibration"]["error_width"],
                "settings": [{k: c[k] for k in ("preparation", "macro", "trials", "ones")}
                             for c in counts["calibration"]["settings"]]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20261024)
    parser.add_argument("--reuse-calibration", type=Path,
                        help="Read existing counts; pay no new acquisition episodes")
    parser.add_argument("--program-set", choices=("unmeasured", "legacy_controls"),
                        default="unmeasured")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    counts = (json.loads(args.reuse_calibration.read_text()) if args.reuse_calibration
              else private_plant.calibration_counts(args.seed))
    # Legacy replay seed is audit metadata, not a count-learner input.
    counts.pop("simulator_seed", None)
    save(args.out_dir/"counts.json", counts)
    save(args.out_dir/"learner_input.json", learner_input(counts))
    save(args.out_dir/"source_provenance.json", {
        "source_orchestrator_seed": args.seed,
        "reuse_calibration_path": str(args.reuse_calibration) if args.reuse_calibration else None,
        "future_simulator_seed": args.seed+1000,
        "not_released_to_learner_or_hypothetical_future_interface": True,
        "statistical_prng_fixture_not_physical_entropy_or_erasure_validation": True})
    calibration_seconds = time.perf_counter()-start
    # A separate count-only process imports no plant module. It receives only
    # the serialized integer counts, architecture bound and action contract.
    learner_start = time.perf_counter()
    subprocess.run([sys.executable, str(Path(__file__).with_name("reset_learner.py")),
                    str(args.out_dir/"learner_input.json"), "--out", str(args.out_dir/"acquired_reset.json")],
                   check=True, capture_output=True, text=True)
    learner_seconds = time.perf_counter()-learner_start
    acquired = json.loads((args.out_dir/"acquired_reset.json").read_text())
    if acquired["status"] != "CERTIFIED":
        print(json.dumps({"status": acquired["status"], "reason": acquired["reason"]}))
        return
    future_start = time.perf_counter()
    programs = (private_plant.PROGRAMS if args.program_set == "unmeasured"
                else private_plant.LEGACY_CONTROL_PROGRAMS)
    future = private_plant.retained_evaluation(acquired, args.seed+1000, programs=programs)
    save(args.out_dir/"retained_future_counts.json", future)
    future_seconds = time.perf_counter()-future_start
    # Private truth is opened only after both acquisition and new evaluation.
    truth = private_plant.post_execution_truth(acquired, future)
    save(args.out_dir/"post_execution_truth.json", truth)
    epsilon = Fraction(acquired["uniform_all_future_tv_diameter_certificate"]["numerator"],
                       acquired["uniform_all_future_tv_diameter_certificate"]["denominator"])
    tau = Fraction(1, 50)
    # K=3, N=20000, tau=.02 => union tail 6 exp(-16).
    future_failure = 6*Fraction(10, 27)**16
    cal_failure = Fraction(acquired["simultaneous_calibration_failure_upper"]["numerator"],
                           acquired["simultaneous_calibration_failure_upper"]["denominator"])
    passes = all(row["absolute_error"] <= epsilon+tau for row in truth["evaluated_programs"])
    summary = {"status": "CONDITIONAL_OPERATION_EXECUTED",
               "conditional_on": ["correct supplied full controlled rank bound two",
                                  "stationary complete-process initialization during calibration",
                                  "private fresh fixed-bit controller with hidden reset records and equal-duration actions"],
               "calibration_initializers": counts["calibration"]["paid_initializers"],
               "new_calibration_initializers_this_invocation": 0 if args.reuse_calibration else counts["calibration"]["paid_initializers"],
               "reused_calibration_path": str(args.reuse_calibration) if args.reuse_calibration else None,
               "calibration_primitive_actions": counts["calibration"]["paid_primitive_actions"],
               "future_initializers": future["paid_initializers"],
               "future_primitive_actions": future["paid_primitive_actions"],
               "future_trials": sum(b["trials"] for b in future["blocks"]),
               "future_fresh_selection_bits": future["fresh_selection_bits"],
               "uniform_reset_tv_certificate": epsilon,
               "future_sampling_tolerance": tau,
               "future_total_error_allowance": epsilon+tau,
               "joint_confidence_failure_upper": cal_failure+future_failure,
               "all_evaluation_program_errors_inside_allowance": passes,
               "evaluation_program_set": args.program_set,
               "calibration_simulator_seconds": calibration_seconds,
               "separate_learner_process_seconds": learner_seconds,
               "future_simulator_seconds": future_seconds,
               "same_data_conventional_contrast_controller": "ties identical operation and certificate",
               "finite_run_total_cost_advantage": "NOT_ESTABLISHED; 60000 uses do not amortize 450000 paid acquisition starts",
               "symbolic_break_even": "T*C_init > 450000*C_init + 1050000*C_step + acquisition_compute_and_noncommon_costs; plus any extra precision/sample costs",
               "physical_erasure_entropy_or_runtime_validation": "NOT_ESTABLISHED",
               "novelty_and_general_learning_advantage": "NOT_ESTABLISHED"}
    save(args.out_dir/"summary.json", summary)
    print(json.dumps(jsonable(summary), indent=2))


if __name__ == "__main__":
    main()
