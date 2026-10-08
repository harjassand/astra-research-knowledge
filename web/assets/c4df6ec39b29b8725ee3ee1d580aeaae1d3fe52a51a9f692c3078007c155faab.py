#!/usr/bin/env python3
"""Optimize informed, time-only controls against the adaptive-mmax model.

This is a finite Monte Carlo scan, not a proof of global controller optimality.
The selection objective is tie-adjusted pairwise ranking AUC.  Candidate time
controls are tuned with the same dose prior supplied to the adaptive policy.
"""
import json
from pathlib import Path

from model_audit import run_pairs


def main():
    pairs = 1000
    seed = 221109
    cases = [
        ("normal", 30.0),
        ("uniform_wide", 0.0),
        ("uniform_low", 0.0),
    ]
    controls = [(f0, tc) for f0 in (400.0, 600.0, 800.0) for tc in (15.0, 60.0, 240.0)]
    rows = []
    for di, (distribution, sigma) in enumerate(cases):
        rows.append(run_pairs("mmax", distribution, sigma, pairs, seed + di * 1000, 60.0, beta=5.0, f0=800.0))
        for ci, (f0, tc) in enumerate(controls):
            rows.append(run_pairs("time", distribution, sigma, pairs,
                                  seed + di * 1000 + ci + 10, tc, beta=5.0, f0=f0))
    payload = {"pairs_per_candidate": pairs, "dose_prior_known_to_time_control": True,
               "parameter_grid": {"F0_pN": [400, 600, 800], "tc_s": [15, 60, 240]},
               "results": rows}
    out = Path(__file__).with_name("control_scan_results.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    for distribution, sigma in cases:
        rr = [r for r in rows if r["distribution"] == distribution and r["sigma"] == sigma]
        adapt = next(r for r in rr if r["policy"] == "mmax")
        time = [r for r in rr if r["policy"] == "time"]
        best = max(time, key=lambda r: r["auc_random_tie"])
        feasible = [r for r in time
                    if r["mean_time_low_Eb_s"] <= adapt["mean_time_low_Eb_s"] * 1.05
                    and r["mean_force_barrier_work_low_Eb_pN_nm"] <= adapt["mean_force_barrier_work_low_Eb_pN_nm"] * 1.05]
        best_matched = max(feasible, key=lambda r: r["auc_random_tie"]) if feasible else None
        print({"case": (distribution, sigma), "adaptive_auc": adapt["auc_random_tie"],
               "adaptive_time_s": adapt["mean_time_low_Eb_s"],
               "adaptive_work_proxy": adapt["mean_force_barrier_work_low_Eb_pN_nm"],
               "best_time_auc": best["auc_random_tie"], "best_time_F0": best["f0_pN"],
               "best_time_tc": best["control"], "best_time_s": best["mean_time_low_Eb_s"],
               "best_time_work_proxy": best["mean_force_barrier_work_low_Eb_pN_nm"],
               "matched_best": None if best_matched is None else {
                   "auc": best_matched["auc_random_tie"], "F0": best_matched["f0_pN"],
                   "tc": best_matched["control"], "time_s": best_matched["mean_time_low_Eb_s"],
                   "work_proxy": best_matched["mean_force_barrier_work_low_Eb_pN_nm"]}})


if __name__ == "__main__":
    main()
