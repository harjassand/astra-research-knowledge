#!/usr/bin/env python3
"""Tune the adaptive mmax threshold over the same known dose prior."""
import json
from pathlib import Path

from model_audit import run_pairs


def main():
    pairs = 1500
    seed = 190827
    cases = [("normal", 30.0), ("uniform_wide", 0.0), ("uniform_low", 0.0)]
    mcs = [20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0]
    rows = []
    for di, (distribution, sigma) in enumerate(cases):
        for ci, mc in enumerate(mcs):
            rows.append(run_pairs("mmax", distribution, sigma, pairs,
                                  seed + di * 10000 + ci * 31, mc, beta=5.0, f0=800.0))
    payload = {"pairs_per_candidate": pairs, "dose_prior_known_to_controller": True,
               "fixed_F0_pN": 800, "beta": 5,
               "mc_grid": mcs, "results": rows}
    out = Path(__file__).with_name("adaptive_threshold_scan_results.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    for distribution, sigma in cases:
        rr = [r for r in rows if r["distribution"] == distribution and r["sigma"] == sigma]
        best = max(rr, key=lambda r: r["auc_random_tie"])
        print({"case": (distribution, sigma), "best_auc": best["auc_random_tie"],
               "mc": best["control"], "time_s": best["mean_time_low_Eb_s"],
               "work_proxy": best["mean_force_barrier_work_low_Eb_pN_nm"],
               "censor": best["tmax_censor_low_Eb"],
               "all": [(r["control"], round(r["auc_random_tie"], 3),
                        round(r["mean_time_low_Eb_s"]),
                        round(r["tmax_censor_low_Eb"], 3)) for r in rr]})


if __name__ == "__main__":
    main()
