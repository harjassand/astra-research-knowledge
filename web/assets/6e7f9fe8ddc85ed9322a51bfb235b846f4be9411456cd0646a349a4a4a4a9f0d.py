#!/usr/bin/env python3
"""Reproduce the paper's local alpha_L probe, then juxtapose global ranking.

This is an internal Gillespie audit, not a reanalysis of experimental data.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_audit import EB_LOW, EPS_E, simulate_one


def local(policy: str, control: float, n: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    scores = {}
    for label, L, Eb in (("base", 100, EB_LOW), ("affinity", 100, EB_LOW+EPS_E), ("dose_plus24", 124, EB_LOW)):
        trajectories = [simulate_one(L, Eb, policy, control, 5.0, 800.0, rng) for _ in range(n)]
        scores[label] = {
            "mean_score_at_tmax": float(np.mean([x.score for x in trajectories])),
            "sd_score_at_tmax": float(np.std([x.score for x in trajectories], ddof=1)),
            "fraction_censored": float(np.mean([x.tmax_censored for x in trajectories])),
            "mean_duration_s": float(np.mean([x.duration_s for x in trajectories])),
            "mean_work_proxy_pN_nm": float(np.mean([x.force_work_proxy_pN_nm for x in trajectories])),
        }
    sigma = scores["base"]["sd_score_at_tmax"]
    scores["alpha_E"] = (scores["affinity"]["mean_score_at_tmax"] - scores["base"]["mean_score_at_tmax"]) / (EPS_E * sigma)
    scores["alpha_L_per_ligand"] = (scores["dose_plus24"]["mean_score_at_tmax"] - scores["base"]["mean_score_at_tmax"]) / (24.0 * sigma)
    scores["alpha_L_for_delta24"] = scores["alpha_L_per_ligand"] * 24.0
    return scores


def main() -> None:
    n = 5000
    res = {
        "n_per_local_condition": n,
        "dose_step": 24,
        "affinity_step_kBT": EPS_E,
        "conditions": {
            "mmax_mc60_beta5_F0800": local("mmax", 60.0, n, 910060),
            "time_tc60_beta5_F0800": local("time", 60.0, n, 910061),
        },
        "definition": "alpha_E=(mean(n|Eb+0.5)-mean(n|Eb))/(0.5*sd(n|L=100,Eb)); alpha_L=(mean(n|L=124,Eb)-mean(n|L=100,Eb))/(24*sd(n|L=100,Eb)). Means use the tmax-observed score; censor rates are reported alongside.",
    }
    p = Path(__file__).with_name("local_vs_global_results.json")
    p.write_text(json.dumps(res, indent=2)+"\n")
    print(p)
    for name, x in res["conditions"].items():
        print(name, "alpha_E", round(x["alpha_E"], 4), "alpha_L", round(x["alpha_L_per_ligand"], 6), "alpha_L*24", round(x["alpha_L_for_delta24"], 4),
              "base mean", round(x["base"]["mean_score_at_tmax"], 3), "base sigma", round(x["base"]["sd_score_at_tmax"], 3),
              "censor", [round(x[k]["fraction_censored"], 3) for k in ("base", "affinity", "dose_plus24")])

if __name__ == "__main__": main()
