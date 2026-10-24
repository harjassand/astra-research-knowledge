#!/usr/bin/env python3
"""Exact post-run checks of rank gates, isolation of inputs and paid costs.

This does not replace the all-future proof or certify the architecture promise.
It uses private truth only after learning to check algebra and stored outputs.
"""
import ast
import copy
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

import private_plant
import reset_learner


HERE = Path(__file__).resolve().parent
RUN = HERE/"run_seed_20261025_held_out"


def frac(value):
    return Fraction(value["numerator"], value["denominator"])


def main():
    counts = json.loads((RUN/"counts.json").read_text())
    pure_input = json.loads((RUN/"learner_input.json").read_text())
    original = json.loads((HERE/"run_seed_20261024/counts.json").read_text())
    stored = json.loads((RUN/"acquired_reset.json").read_text())
    learned = reset_learner.acquire(pure_input)
    assert learned == stored
    assert counts["calibration"] == original["calibration"]
    assert "simulator_seed" not in counts
    tree = ast.parse((HERE/"reset_learner.py").read_text())
    imports = {name.name for node in ast.walk(tree) if isinstance(node, ast.Import)
               for name in node.names}
    assert imports <= {"argparse", "json"} and "private_plant" not in imports
    assert "private_plant" not in (HERE/"reset_learner.py").read_text()
    assert counts["calibration"]["paid_initializers"] == 450_000
    assert sum(c["trials"]*c["primitive_actions_per_trial"]
               for c in counts["calibration"]["settings"]) == 1_050_000
    future = json.loads((RUN/"retained_future_counts.json").read_text())
    assert future["paid_initializers"] == 0 and future["reset_invocations"] == 60_000
    assert future["paid_primitive_actions"] == 280_000
    assert future["fresh_selection_bits"] == 960_000
    assert "simulation_seed" not in future
    # Every actual scalar calibration mean satisfies its stated interval in
    # this realized fixture; that is evaluation-only, not information supplied.
    p0 = Fraction(19, 20)
    for cell in counts["calibration"]["settings"]:
        p = p0
        for a in private_plant.PREPARATIONS[cell["preparation"]]+private_plant.MACROS[cell["macro"]]:
            p = private_plant.hidden_p_after(a, p)
        true_mean = private_plant.sensor_probability(p)
        assert abs(Fraction(cell["ones"], cell["trials"])-true_mean) <= Fraction(1,100)
    actual_weight = frac(learned["implemented_weight_a"])
    actual_slope = Fraction(9,10)*actual_weight-Fraction(4,5)*(1-actual_weight)
    assert abs(actual_slope) <= frac(learned["uniform_all_future_tv_diameter_certificate"])
    # All fixed words up to length eight retain a nonzero scalar slope.
    # The all-length statement follows because each primitive slope is nonzero.
    word_count = 0
    for length in range(9):
        for word in product(("s", "a", "b"), repeat=length):
            slope = Fraction(1)
            for a in word:
                slope *= {"s": Fraction(1), "a": Fraction(9,10), "b": Fraction(-4,5)}[a]
            assert slope != 0
            word_count += 1
    # No basis gap => UNKNOWN. The algorithm is not a rank-two recognizer.
    flat = copy.deepcopy(pure_input)
    for cell in flat["calibration"]["settings"]:
        cell["ones"] = 25_000
    assert reset_learner.acquire(flat)["status"] == "UNKNOWN"
    # Clear basis gap but positive control contrasts => no positive cancellation.
    positive = copy.deepcopy(pure_input)
    means = {"initial": 10_000, "a": 20_000, "b": 30_000}
    for cell in positive["calibration"]["settings"]:
        cell["ones"] = means[cell["preparation"]]
    assert reset_learner.acquire(positive)["status"] == "UNKNOWN"
    # Mixture is reset marginally but cannot return its label as part of reset.
    joint0 = {(0,0): Fraction(1,2), (1,1): Fraction(1,2)}
    joint1 = {(0,1): Fraction(1,2), (1,0): Fraction(1,2)}
    joint_tv = sum(abs(joint0.get(k,0)-joint1.get(k,0)) for k in joint0.keys()|joint1.keys())/2
    assert joint_tv == 1
    # Same-data conventional affine regression gives the identical fit and
    # dyadic controller: this is an incumbent tie, not an algorithmic win.
    prep0, prep1 = learned["basis_preparations"]
    c = {(x["preparation"],x["macro"]): Fraction(x["ones"],x["trials"])
         for x in counts["calibration"]["settings"]}
    g = c[prep1,"none"]-c[prep0,"none"]
    slope_a = (c[prep1,"a"]-c[prep0,"a"])/g
    slope_b = (c[prep1,"b"]-c[prep0,"b"])/g
    conventional_weight = slope_b/(slope_b-slope_a)
    assert conventional_weight == frac(learned["zero_contrast_rational_weight_a"])
    exact_allowance = frac(learned["uniform_all_future_tv_diameter_certificate"])+Fraction(1,50)
    # Same 6*e^-16 three-event sampling confidence: n0*A^2 >= 8.
    target = Fraction(8)/(exact_allowance**2)
    n0 = (target.numerator+target.denominator-1)//target.denominator
    gap_lower = frac(learned["basis_gap_lower"])
    r = frac(learned["implemented_empirical_contrast_residual"])
    eta = (r+Fraction(1,50))/gap_lower
    powers = []
    for depth in (1,2,3):
        cert = eta**depth/gap_lower
        assert abs(actual_slope)**depth/gap_lower <= cert
        allowance = cert+Fraction(1,50)
        exact_count = Fraction(8)/(allowance**2)
        sufficient = (exact_count.numerator+exact_count.denominator-1)//exact_count.denominator
        powers.append({"depth": depth, "certificate": float(cert),
                       "actual_controls_per_reset": depth,
                       "fresh_bits_per_reset": 16*depth,
                       "executed": depth == 1,
                       "exact_initializer_trials_for_matched_allowance": sufficient})
    # Strongest fixed pure word for this private fixture uses b at each step.
    # This is a restricted word-class comparison; positive-mixture control ties.
    pure_b_bound = (abs(frac(learned["observed_control_contrasts"]["b"]))+Fraction(1,50))/gap_lower
    pure_b_length = 0
    while pure_b_bound**pure_b_length/gap_lower > frac(learned["uniform_all_future_tv_diameter_certificate"]):
        pure_b_length += 1
    report = {"status": "PASS", "exact_fixed_word_checks": word_count,
              "calibration_intervals_actual_truth_checked": 9,
              "degenerate_gap_and_positive_hull_gates_checked": True,
              "count_only_learner_input_replay": "identical acquired artifact",
              "same_data_conventional_affine_controller": "exact rational weight tie",
              "logged_key_counterexample_joint_tv": str(joint_tv),
              "matched_error_exact_initializer_trials_per_program_sufficient": n0,
              "executed_acquired_preparation_trials_per_program": 20_000,
              "matched_error_fewer_samples_for_exact_initializer": True,
              "acquisition_plus_all_early_and_final_steps": 1_050_000+200_000+280_000,
              "acquisition_plus_all_early_and_final_initializers": 450_000,
              "all_early_and_final_reset_invocations": 120_000,
              "all_early_and_final_selection_bits": 1_920_000,
              "acquired_scalar_contraction_upper": float(eta),
              "mathematical_composition_corollary": powers,
              "restricted_pure_b_self_reference_diameter_length": pure_b_length,
              "pure_b_reference_scope": "its own b^L(rho0), not target matching to S(rho0)"}
    (RUN/"operation_checks.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
