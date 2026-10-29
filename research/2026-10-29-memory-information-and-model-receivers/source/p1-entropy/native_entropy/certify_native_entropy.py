#!/usr/bin/env python3
"""Consumer: PUBLIC_CONTRACT + actual native record only; never source truth."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import hashlib,json,time,sys
import numpy as np
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"run"
BITS=80
DEN=1<<BITS

def log_one_two(x,terms=60):
    assert 1<=x<=2
    z=(x-1)/(x+1); zz=z*z
    term=z; lo=F(0)
    for k in range(terms):
        lo+=2*term/(2*k+1);term*=zz
    return lo,lo+2*term/((2*terms+1)*(1-zz))

def log_upper(x):
    assert x>=1
    k=0
    while x>=2:x/=2;k+=1
    lo,hi=log_one_two(x)
    _,hi2=log_one_two(F(2))
    exact=hi+k*hi2
    return F((exact.numerator*DEN+exact.denominator-1)//exact.denominator,DEN)

def sqrt_upper(x):
    assert x>=0
    z=isqrt((x.numerator*DEN*DEN)//x.denominator)
    if z*z*x.denominator<x.numerator*DEN*DEN:z+=1
    return F(z,DEN)

def exp_negative_upper(x,terms=128):
    assert x>=0
    s=F(1);t=F(1)
    for k in range(1,terms+1):
        t*=x/k;s+=t
    # s is a positive Taylor LOWER bound for exp(x).
    q=1/s
    return F((q.numerator*DEN+q.denominator-1)//q.denominator,DEN)

def rep(x):
    if isinstance(x,F):return {"rational":str(x),"decimal":float(x)}
    if isinstance(x,dict):return {k:rep(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [rep(v) for v in x]
    return x

def main():
    start_time=time.perf_counter()
    contract_path=OUT/"PUBLIC_CONTRACT.json"
    record_path=OUT/"native_record.npz"
    contract=json.loads(contract_path.read_text())
    assert contract["ports"]==5 and contract["selection"].startswith("Each port chosen uniformly")
    assert contract["native_port_rates"]==["32/15"]*5
    scale=int(contract["timestamp_scale"])
    raw=np.load(record_path,allow_pickle=False)
    i=raw["start_port"];j=raw["end_port"]
    upper=raw["interior_duration_upper_ticks"].astype(np.uint64)
    N=len(i)
    assert N==int(contract["acquired_trials"]) and all(len(raw[x])==N for x in raw.files)
    assert np.all(i<5) and np.all(j<5)
    delta=(j.astype(np.int16)-i.astype(np.int16))%5
    sign=np.where((delta==1)|(delta==4),-1,1).astype(np.int8)
    lower=np.where(upper>0,upper-1,0)
    # Upper score over the instrument's true-time interval. Direct atoms,
    # if present, have a separately resolved zero-tick marker.
    definitely_inside=(upper>0)&(upper<=scale)
    definitely_outside=(upper==0)|(lower>scale)
    score_upper=np.where(definitely_inside,sign,
        np.where(definitely_outside,0,np.maximum(sign,0))).astype(np.int8)
    empirical=F(int(score_upper.astype(np.int64).sum()),N)
    ds=F(contract["confidence_score_failure"])
    dm=F(contract["confidence_mean_failure"])
    score_radius=sqrt_upper(2*log_upper(1/ds)/N)
    score_expectation_upper=empirical+score_radius
    gamma=max(F(0),-score_expectation_upper)
    entropy_per_departure_lower=4*gamma
    trunc=F(contract["mean_truncation"]);trunc_ticks=int(trunc*scale)
    truncated_ticks=np.minimum(upper,trunc_ticks)
    empirical_truncated_mean_upper=F(int(truncated_ticks.sum()),N*scale)
    mean_radius=trunc*sqrt_upper(log_upper(1/dm)/(2*N))
    tail_bias_upper=2*exp_negative_upper(trunc/2)
    interior_mean_upper=empirical_truncated_mean_upper+mean_radius+tail_bias_upper
    native_hold_mean=F(15,32)
    cycle_mean_upper=native_hold_mean+interior_mean_upper
    entropy_rate_lower=entropy_per_departure_lower/cycle_mean_upper
    counts=np.zeros((5,5),dtype=np.int64)
    window_counts=np.zeros((5,5),dtype=np.int64)
    np.add.at(counts,(i,j),1)
    np.add.at(window_counts,(i[definitely_inside],j[definitely_inside]),1)
    # Copositivity has an ordinary exact proof: triangle-free simplex edge
    # maximum <=1/4. No numerical eigenvalue check is substituted for it.
    output={
      "status":"PASS" if gamma>0 else "NO_CERTIFICATE",
      "permitted_inputs":[str(contract_path),str(record_path)],
      "private_source_reads":0,
      "new_source_observations":0,"new_source_preparations":0,
      "reused_individual_native_records":N,
      "record_sha256":hashlib.sha256(record_path.read_bytes()).hexdigest(),
      "contract_sha256":hashlib.sha256(contract_path.read_bytes()).hexdigest(),
      "consumer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "confidence_failure_total":ds+dm,
      "score_failure":ds,"mean_failure":dm,
      "score_sum":int(score_upper.astype(np.int64).sum()),
      "score_empirical_upper":empirical,
      "score_radius_outward":score_radius,
      "score_expectation_upper":score_expectation_upper,
      "copositive_gap_lower":gamma,
      "entropy_per_native_departure_lower_nats":entropy_per_departure_lower,
      "native_hold_mean_from_calibration":native_hold_mean,
      "empirical_censored_duration_upper":empirical_truncated_mean_upper,
      "mean_radius_outward":mean_radius,"tail_bias_outward":tail_bias_upper,
      "interior_mean_upper":interior_mean_upper,
      "cycle_mean_upper":cycle_mean_upper,
      "entropy_rate_lower_nats_per_native_time":entropy_rate_lower,
      "bin_counts":window_counts.tolist(),"all_endpoint_counts":counts.tolist(),
      "timestamp_ambiguous_trials":int(np.sum(~definitely_inside & ~definitely_outside)),
      "source_tail_used_for_bounded_witness":False,
      "source_tail_used_for_time_rate":True,
      "witness":"Classical Horn copositive matrix on the predeclared 5-cycle; h_minus=1.",
      "theorem_scope":"Every compatible finite stationary even-state CTMC with the stated native resolved-port/flux-weighted reset interface; no hidden rate ceiling or chosen hidden dimension.",
      "not_established":["Physical calibration","Physical experiment","Floating RNG law guarantee","Complete source identification","Observed exact time-reversal symmetry from finite data"],
      "arithmetic":"Exact rational empirical quantities; rational atanh-series logarithm bounds, integer-square-root upper bounds, inverse positive Taylor bound for exp(-12).",
      "python_version":sys.version.split()[0],"numpy_version":np.__version__,
      "software_wall_seconds":time.perf_counter()-start_time
    }
    (OUT/"ACQUIRED_ENTROPY_CERTIFICATE.json").write_text(json.dumps(rep(output),indent=2)+"\n")
    print(json.dumps(rep({k:v for k,v in output.items() if k not in ["bin_counts","all_endpoint_counts","not_established"]}),indent=2))
if __name__=="__main__":main()

