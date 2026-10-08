#!/usr/bin/env python3
"""Prior-informed grid search plus fresh validation of time-only force schedules."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_audit import EB_LOW, EPS_E, sample_l0, simulate_one


CASES = [("normal_sigma30", "normal", 30.0, 60.0),
         ("uniform_5_195", "uniform_wide", 0.0, 50.0),
         ("uniform_5_60", "uniform_low", 0.0, 30.0)]
F0_GRID = [200.0, 400.0, 600.0, 800.0, 1000.0]
TC_GRID = [5.0, 15.0, 30.0, 60.0, 120.0, 240.0, 480.0]


def evaluate(policy, control, f0, dist, sigma, pairs, seed):
    rng = np.random.default_rng(seed)
    outcomes=[]; times=[]; proxy=[]; censored=0
    for _ in range(pairs):
        l1=sample_l0(rng,dist,sigma); l2=sample_l0(rng,dist,sigma)
        a=simulate_one(l1,EB_LOW,policy,control,5.0,f0,rng)
        b=simulate_one(l2,EB_LOW+EPS_E,policy,control,5.0,f0,rng)
        outcomes.append(1.0 if b.score>a.score else 0.5 if b.score==a.score else 0.0)
        times.extend([a.duration_s,b.duration_s]); proxy.extend([a.force_work_proxy_pN_nm,b.force_work_proxy_pN_nm])
        censored += int(a.tmax_censored)+int(b.tmax_censored)
    auc=float(np.mean(outcomes)); sd=float(np.std(outcomes,ddof=1))
    return {"policy":policy,"control":control,"f0_pN":f0,"pairs":pairs,"seed":seed,
            "auc":auc,"auc_95pct_normal":[max(0,auc-1.96*sd/math.sqrt(pairs)),min(1,auc+1.96*sd/math.sqrt(pairs))],
            "mean_duration_s":float(np.mean(times)),"mean_barrier_proxy_pN_nm":float(np.mean(proxy)),
            "trajectory_censor_fraction":censored/(2*pairs)}


def main():
    scan_pairs=600; validation_pairs=4000
    out={"dose_prior_known_to_time_controller":True,
         "scan_grid":{"tc_s":TC_GRID,"F0_pN":F0_GRID},
         "screen_pairs_per_setting":scan_pairs,
         "validation_pairs_per_candidate":validation_pairs,
         "results":[]}
    for ci,(name,dist,sigma,mc) in enumerate(CASES):
        screened=[]
        for fi,f0 in enumerate(F0_GRID):
            for ti,tc in enumerate(TC_GRID):
                seed=100000+ci*10000+fi*100+ti
                screened.append(evaluate("time",tc,f0,dist,sigma,scan_pairs,seed))
        screened.sort(key=lambda x:x["auc"],reverse=True)
        # Validate the two leading schedules on disjoint random streams.
        validated=[]
        for j,candidate in enumerate(screened[:2]):
            validated.append(evaluate("time",candidate["control"],candidate["f0_pN"],dist,sigma,
                                      validation_pairs,200000+ci*100+j))
        # Fresh reference run for the prior-scan adaptive threshold.
        adaptive=evaluate("mmax",mc,800.0,dist,sigma,validation_pairs,300000+ci)
        out["results"].append({"case":name,"distribution":dist,"sigma":sigma,"adaptive_mc_from_separate_scan":mc,
                               "top_screened":screened[:5],"validated_time_top2":validated,"adaptive_fresh":adaptive})
        print(name,"screen tops",[(x["control"],x["f0_pN"],round(x["auc"],3)) for x in screened[:3]])
        print("validated",[(x["control"],x["f0_pN"],round(x["auc"],4),round(x["mean_duration_s"],1),round(x["trajectory_censor_fraction"],3)) for x in validated])
        print("adaptive",round(adaptive["auc"],4),"duration",round(adaptive["mean_duration_s"],1),"censor",round(adaptive["trajectory_censor_fraction"],3))
    p=Path(__file__).with_name("time_policy_sweep_results.json")
    p.write_text(json.dumps(out,indent=2)+"\n")
    print(p)

if __name__=="__main__":main()
