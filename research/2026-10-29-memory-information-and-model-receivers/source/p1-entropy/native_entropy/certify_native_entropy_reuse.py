#!/usr/bin/env python3
"""Reuse one record for two fixed witnesses with simultaneous confidence."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,time,sys
import numpy as np
from certify_native_entropy import log_upper,sqrt_upper,exp_negative_upper,rep
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"run"
def main():
    started=time.perf_counter()
    cp=OUT/"PUBLIC_CONTRACT.json";rp=OUT/"native_record.npz"
    contract=json.loads(cp.read_text());raw=np.load(rp,allow_pickle=False)
    i=raw["start_port"];j=raw["end_port"];u=raw["interior_duration_upper_ticks"]
    N=len(i);scale=int(contract["timestamp_scale"])
    assert contract["native_port_rates"]==["32/15"]*5
    d=(j.astype(np.int16)-i.astype(np.int16))%5
    h=np.where((d==1)|(d==4),-1,1).astype(np.int64)
    lo=np.where(u>0,u-1,0)
    inside=(u>0)&(u<=scale)
    outside=(u==0)|(lo>scale)
    y_window=np.where(inside,h,np.where(outside,0,np.maximum(h,0)))
    y_all=np.where(u>0,h,0)
    failure=F(1,3000)
    radius=sqrt_upper(2*log_upper(1/failure)/N)
    scores={}
    for name,y in [("duration_at_most_1",y_window),("all_positive_duration_returns",y_all)]:
        empirical=F(int(y.sum()),N);gap=max(F(0),-empirical-radius)
        scores[name]={"score_sum":int(y.sum()),"empirical_score_upper":empirical,
            "confidence_radius":radius,"gap_lower":gap,
            "entropy_per_departure_lower":4*gap}
    trunc=F(24)
    mean_emp=F(int(np.minimum(u,int(trunc*scale)).sum()),N*scale)
    mean_radius=trunc*sqrt_upper(log_upper(1/failure)/(2*N))
    tail=2*exp_negative_upper(F(12))
    mean_upper=F(15,32)+mean_emp+mean_radius+tail
    for value in scores.values():value["entropy_rate_lower"]=value["entropy_per_departure_lower"]/mean_upper
    best=max(scores,key=lambda x:scores[x]["entropy_per_departure_lower"])
    out={
      "status":"PASS" if scores[best]["gap_lower"]>0 else "NO_CERTIFICATE",
      "inputs":[str(cp),str(rp)],"source_private_reads":0,
      "new_source_trials":0,"new_source_preparations":0,
      "individual_records_reused":N,"confidence_failure_total":3*failure,
      "simultaneous_family":"Two fixed Horn scores: the original (0,1] time bin and all positive-duration excursions; same mean bound. No score matrix was fit to the data.",
      "analysis_scope":"Post-acquisition reuse with simultaneous finite-family confidence; the earlier one-window certificate is preserved separately.",
      "scores":scores,"stronger_certificate":best,
      "mean_cycle_upper":mean_upper,"truncated_mean_upper":mean_emp,
      "mean_radius":mean_radius,"tail_allowance":tail,
      "record_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),
      "consumer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "helper_sha256":hashlib.sha256((ROOT/"certify_native_entropy.py").read_bytes()).hexdigest(),
      "numpy_version":np.__version__,"python_version":sys.version.split()[0],
      "wall_seconds":time.perf_counter()-started,
      "sampling_and_physics_scope":"Same numerical RNG qualification and supplied reset/flux/clock/timestamp/tail contracts as the producer. Entropy is for an even-state stationary CTMC. No physical validation."
    }
    (OUT/"REUSED_ENTROPY_CERTIFICATE.json").write_text(json.dumps(rep(out),indent=2)+"\n")
    print(json.dumps(rep(out),indent=2))
if __name__=="__main__":main()

