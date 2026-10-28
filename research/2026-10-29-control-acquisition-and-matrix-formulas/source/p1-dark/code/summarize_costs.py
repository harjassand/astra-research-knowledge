"""Summarize complete recorded costs without querying a source."""
from pathlib import Path
from fractions import Fraction as F
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    acquisitions = json.loads((ROOT / "results/LATTICE_RESULTS.json").read_text())
    rows = []
    for summary in acquisitions["cases"]:
        label = summary["label"]
        acquired = json.loads((ROOT / "results" / (label + "_results.json")).read_text())
        refined = json.loads((ROOT / "results" / (label + "_curvature.json")).read_text())
        row = {"label": label, "physical_ledger": acquired["physical_ledger"],
               "ideal_costs": acquired["ideal_costs"],
               "exact_transform_cost": acquired["transform_cost"],
               "curvature_matrix_count": refined["matrix_count"],
               "curvature_matrix_order": refined["matrix_order"],
               "shared_calibration_standards": 2, "later_tasks": []}
        for old, task in zip(acquired["tasks"], refined["tasks"]):
            assert old["utility"] == task["utility"] and old["task"] == task["task"]
            command = [F(x) for x in task["candidate"]["command"]]
            nonzero = sum(bool(x) for x in command)
            use = {"utility": task["utility"], "task": task["task"],
                   "certificate_source_readings": 0,
                   "selected_command": task["candidate"]["command"],
                   "selected_command_nonzero_writes": nonzero,
                   "reset_writes_if_cleared_individually": nonzero,
                   "dose": str(sum(command)), "dac_bits": 20,
                   "preparation_settling_and_reset_required_for_physical_use": True,
                   "elapsed_physical_time_and_energy": "unacquired",
                   "extra_measurement_if_requested": "pay separately; none used by this certificate",
                   "optimizer_coefficient_evaluations": task["proposal"]["evaluations"],
                   "hypograph_regret": old["certificate"]["continuous_simplex_regret"],
                   "combined_regret": task["continuous_simplex_regret"],
                   "equally_informed_conventional_same_method_regret": task["continuous_simplex_regret"]}
            if "direct_negative_Z_certificate_same_candidate" in old:
                use["direct_negative_Z_same_hypograph_candidate_regret"] = old[
                    "direct_negative_Z_certificate_same_candidate"]["continuous_simplex_regret"]
            row["later_tasks"].append(use)
        rows.append(row)
    result = {"scope": "Recorded synthetic acquisition and required physical-use operations; no hardware timing or energy benchmark.",
              "comparison": "An equally informed conventional route may adopt the same representations and exact checks, so it matches these records and certificates. Stronger conventional methods are not ruled out.",
              "standard_acquisition_obligation": "Each known standard requires preparation/routing, settling, readout and restoration; apparatus-specific cost is unacquired.",
              "source_class_obligation": "Fixed affine-SPD actuators, source offset, calibrated readout, G/kappa bounds, permitted doses and stable source remain warranted inputs.",
              "offline_general_cost": {"lattice_nodes": "M=binom(n+k,k)",
                  "coefficient_storage_each_representation": "M",
                  "face_transform_maximum_block_order": "binom(k-1,s-1) for support size s",
                  "hull_sort_per_price": "O(M log M) rational comparisons",
                  "curvature_matrices": "binom(n+k-2,k-2), each n by n",
                  "curvature_assembly": "O(n^2) coefficient operations per matrix",
                  "exact_LDL": "O(n^3) rational operations per matrix; bit growth also paid",
                  "polynomial_evaluation": "Depends on stored sparse basis and n,k; no free source evaluation is substituted"},
              "cases": rows}
    (ROOT / "results/COST_AND_COMPARISON.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"cases": len(rows), "tasks": sum(len(r["later_tasks"]) for r in rows),
                      "extra_source_readings": 0, "conventional_advantage_claimed": False}))


if __name__ == "__main__":
    main()
