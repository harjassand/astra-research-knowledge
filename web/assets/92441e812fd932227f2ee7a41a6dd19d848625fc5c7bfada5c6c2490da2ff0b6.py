#!/usr/bin/env python3
"""Independent-dose and matched-dose ranking audit with censor intervals.

At tmax a trajectory's terminal antigen score is right-censored by the model.
Rather than treating that score as its eventual readout, this script reports
the AUC interval obtained by allowing each censored score to range from its
observed n to its physical state-space maximum L. It also reruns affinity
pairs with either independently drawn or shared dose to separate hidden-dose
confounding from within-dose ranking.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_audit import (  # noqa: E402
    EB_LOW,
    EPS_E,
    TMAX,
    sample_l0,
    simulate_one,
)


def _auc_contribution(low_min: int, low_max: int, high_min: int, high_max: int) -> tuple[float, float]:
    """Best/worst tie-adjusted AUC contribution over integer score intervals."""
    worst = 1.0 if high_min > low_max else (0.5 if high_min == low_max else 0.0)
    best = 1.0 if high_max > low_min else (0.5 if high_max == low_min else 0.0)
    return worst, best


def run_case(name: str, distribution: str, sigma: float, adaptive_mc: float,
             time_tc: float, pairs: int, seed: int, matched_dose: bool) -> dict:
    rng = np.random.default_rng(seed)
    controls = (("mmax", adaptive_mc), ("time", time_tc))
    out = {"case": name, "distribution": distribution, "sigma": sigma,
           "pairs": pairs, "seed": seed, "matched_dose": matched_dose,
           "dose_prior_known_to_both_controllers": True,
           "tmax_s": TMAX, "policies": {}}
    for policy, control in controls:
        auc_values = []
        lower, upper = [], []
        low_cens = high_cens = 0
        times, works = [], []
        for _ in range(pairs):
            l_low = sample_l0(rng, distribution, sigma)
            l_high = l_low if matched_dose else sample_l0(rng, distribution, sigma)
            low = simulate_one(l_low, EB_LOW, policy, control, 5.0, 800.0, rng)
            high = simulate_one(l_high, EB_LOW + EPS_E, policy, control, 5.0, 800.0, rng)
            low_cens += int(low.tmax_censored)
            high_cens += int(high.tmax_censored)
            # Scores at a noncensored termination are exact; a censored one
            # can rise by at most the remaining finite antigen supply.
            lo_interval = (low.score, l_low if low.tmax_censored else low.score)
            hi_interval = (high.score, l_high if high.tmax_censored else high.score)
            w, b = _auc_contribution(*lo_interval, *hi_interval)
            lower.append(w)
            upper.append(b)
            auc_values.append(1.0 if high.score > low.score else 0.5 if high.score == low.score else 0.0)
            times.extend([low.duration_s, high.duration_s])
            works.extend([low.force_work_proxy_pN_nm, high.force_work_proxy_pN_nm])
        auc = float(np.mean(auc_values))
        sd = float(np.std(auc_values, ddof=1))
        out["policies"][policy] = {
            "control": control,
            "auc_observed_at_tmax": auc,
            "auc_mc_95pct_normal": [max(0.0, auc - 1.96 * sd / math.sqrt(pairs)),
                                    min(1.0, auc + 1.96 * sd / math.sqrt(pairs))],
            "auc_if_censored_final_scores_are_unknown": [float(np.mean(lower)), float(np.mean(upper))],
            "fraction_low_Eb_censored": low_cens / pairs,
            "fraction_high_Eb_censored": high_cens / pairs,
            "mean_contact_duration_s_both_affinities": float(np.mean(times)),
            "mean_model_force_barrier_proxy_pN_nm_both_affinities": float(np.mean(works)),
        }
    return out


def main() -> None:
    pairs = 5000
    specs = [
        ("normal_sigma30", "normal", 30.0, 60.0, 60.0),
        ("uniform_5_195", "uniform_wide", 0.0, 50.0, 60.0),
        ("uniform_5_60", "uniform_low", 0.0, 30.0, 240.0),
    ]
    results = []
    for i, (name, dist, sigma, mc, tc) in enumerate(specs):
        for matched in (False, True):
            results.append(run_case(name, dist, sigma, mc, tc, pairs,
                                    830001 + i * 100 + int(matched), matched))
    payload = {
        "description": "Fresh independent Gillespie reruns. mc is selected from the finite adaptive threshold scan; time tc is the best AUC on the 9-point finite time-only scan for that prior. Both controls know the dose prior.",
        "important_limit": "tmax-censored scores are bounded only by [observed n, L]; AUC interval is a worst/best completion bound, not a confidence interval. Work value is a barrier-lowering proxy, not physical work or ATP.",
        "pairs_per_case_policy": pairs,
        "results": results,
    }
    path = Path(__file__).with_name("score_interval_audit_results.json")
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(path)
    for r in results:
        print(r["case"], "matched" if r["matched_dose"] else "independent")
        for policy, x in r["policies"].items():
            print(policy, "control", x["control"], "AUC", round(x["auc_observed_at_tmax"], 4),
                  "CI", [round(v, 4) for v in x["auc_mc_95pct_normal"]],
                  "censor bounds", [round(v, 4) for v in x["auc_if_censored_final_scores_are_unknown"]],
                  "censored", round(x["fraction_low_Eb_censored"], 3), round(x["fraction_high_Eb_censored"], 3),
                  "duration", round(x["mean_contact_duration_s_both_affinities"], 1))


if __name__ == "__main__":
    main()
