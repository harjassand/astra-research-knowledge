#!/usr/bin/env python3
"""Exact finite-bit exponential-lag clock, not physical or simulated driver data."""
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from hashlib import sha256
from pathlib import Path
import json

def exp_minus_enclosure(x, tolerance=F(1,10**50)):
    """Positive Taylor series for exp(x), then reciprocate exact rational bounds."""
    assert x>=0
    term=F(1); total=term; k=0
    while True:
        k+=1; term*=x/k; total+=term
        next_term=term*x/(k+1)
        ratio=x/(k+2)
        if ratio<1:
            upper=total+next_term/(1-ratio)
            lo,hi=1/upper,1/total
            if hi-lo<=tolerance:
                return lo,hi,k

def dec(x, up=False):
    with localcontext() as ctx:
        ctx.prec=30
        ctx.rounding=ROUND_CEILING if up else ROUND_FLOOR
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def main():
    gamma=F(1); delta=F(1,32); count=256; tc=count*delta
    bits=32; denominator=2**bits
    lo_step,hi_step,terms=exp_minus_enclosure(gamma*delta)
    lo,hi=F(1),F(1)
    ticks=[]; thresholds=[]; used=0
    tv_upper=F(0); mean_time=F(0)
    for k in range(count):
        next_lo,next_hi=lo*lo_step,hi*hi_step
        p_lo=max(F(0),lo-next_hi)
        p_hi=hi-next_lo
        ticks_k=(p_lo.numerator*denominator)//p_lo.denominator
        q_k=F(ticks_k,denominator)
        assert F(0)<=q_k<=p_lo<=p_hi
        ticks.append(ticks_k); used+=ticks_k; thresholds.append(used)
        tv_upper+=p_hi-q_k
        mean_time+=q_k*k*delta
        lo,hi=next_lo,next_hi
    q_censor=F(denominator-used,denominator)
    assert q_censor>=hi
    assert sum(F(t,denominator) for t in ticks)+q_censor==1
    assert mean_time<=(1-lo)/gamma+tv_upper*tc
    assert tv_upper<=F(count+1,denominator)
    # Illustrative feature bounds, not a margin obtained from physical observations.
    # d=tau=gamma=1, B=(1,1), L=(1,2); ||B||||L||=sqrt(10)<=16/5.
    timing_jitter=F(1,1000)
    eta_time_upper=F(16,5)*(delta+timing_jitter)
    eta_bits_upper=4*tv_upper
    eta_tail_upper=2*hi
    result={
      "status":"PASS",
      "scope":"exact rational clock construction only; no source paths, physical observations, or random trials",
      "script_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
      "gamma":"1","grid_step":"1/32","censor_time":"8",
      "noncensor_outcomes":count,"fair_bits_per_draw":bits,
      "exp_step_positive_taylor_terms":terms,
      "clock_probability_tv_upper":dec(tv_upper,True),
      "censor_probability_interval":[dec(lo),dec(hi,True)],
      "implemented_censor_probability_exact":str(q_censor),
      "actual_mean_evolution_time_censor_skipped":dec(mean_time),
      "actual_mean_evolution_time_exact":str(mean_time),
      "worst_case_grid_lag":str((count-1)*delta),
      "max_lag_with_timing_jitter":str((count-1)*delta+timing_jitter),
      "threshold_denominator":denominator,
      "integer_cumulative_noncensor_thresholds":thresholds,
      "illustrative_feature_contract":{"d":1,"tau":"1","B":["1","1"],"L":["1","2"],"timing_jitter":"1/1000"},
      "illustrative_extra_matrix_bias_upper":{
        "time":dec(eta_time_upper,True),"bits":dec(eta_bits_upper,True),"tail":dec(eta_tail_upper,True)
      },
      "unpaid_gates":["independent equilibrium driver preparations","noninvasive calibrated bounded Lipschitz feature readouts","actual timing jitter bound","calibrated bath and one-way force actuator"]
    }
    out=Path(__file__).with_name("FINITE_CLOCK_CONSTRUCTION.json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    report={k:v for k,v in result.items() if k!="integer_cumulative_noncensor_thresholds"}
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()

