#!/usr/bin/env python3
"""Finite grouped-wait assay audit with explicit censor and clock service.

This is synthetic execution of the statistical procedure, not apparatus data.
The learner receives requested-context first-exit waits; the hidden rate
arrays are read only by the final audit and synthetic physical mechanism.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import time
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parent


def schedule(lam_min=Fraction(1,2), lam_max=Fraction(6,5),
             eta=Fraction(1,8), delta=Fraction(1,20), K=6):
    j = 0
    while Fraction(1, 2**(3*j)) > eta:
        j += 1
    a = Fraction(1,2**j)/lam_max
    B = 3/a
    L = 0
    while Fraction(2**L) < 192/eta:
        L += 1
    D = L/lam_min
    Delta = eta*lam_min*a*a/1024
    omega = eta*lam_min/128
    beta = eta*lam_min/(128*B)
    kappa = lam_max/lam_min
    m = math.ceil(256*kappa/(eta*eta))
    q = 1
    while Fraction(1,2**q) > delta/K:
        q += 2
    L_confidence=0
    while Fraction(2**L_confidence) < 2*K/delta:
        L_confidence+=1
    # log_2 ceiling is an exact rational upper bound for the natural log.
    n_direct=math.ceil(40*kappa/(eta*eta)*L_confidence)
    vals = locals().copy()
    for k in ("vals",): vals.pop(k,None)
    return {k: {"numerator":v.numerator,"denominator":v.denominator,
                "decimal":float(v)} if isinstance(v,Fraction) else v
            for k,v in vals.items()}


def fnum(s,k):
    return s[k]["decimal"] if isinstance(s[k],dict) else s[k]


def analytic_checks(s):
    mp.mp.dps = 70
    a = mp.mpf(s["a"]["numerator"])/s["a"]["denominator"]
    D = mp.mpf(s["D"]["numerator"])/s["D"]["denominator"]
    eta = mp.mpf(s["eta"]["numerator"])/s["eta"]["denominator"]
    checks=[]
    for lam_text in ("0.5","0.6","0.9","1.2"):
        lam=mp.mpf(lam_text)
        density=lambda z: lam**4*z**3*mp.exp(-lam*z)/6
        clip_loss=mp.quad(lambda z:(3/z-3/a)*density(z),[0,a])
        clip_bound=lam**4*a**3/24
        e=mp.exp(-lam*D); q=1-e
        dwell=q/lam*sum(q**j for j in range(4))
        wasted=sum(q**(j-1)*e*(D+(j-1)*(1/lam-D*e/q)) for j in range(1,5))
        assert clip_loss>=0 and clip_loss<=clip_bound
        assert dwell<=4/lam
        assert wasted<=16*D*e
        checks.append({"lambda":lam_text,"exact_clipping_loss":str(clip_loss),
                       "clipping_bound":str(clip_bound),
                       "second_moment_unclipped":str(mp.mpf("1.5")*lam**2),
                       "ideal_expected_active_dwell":str(dwell),
                       "ideal_expected_discarded_dwell":str(wasted),
                       "discarded_dwell_bound":str(16*D*e)})
    return checks


def execute_menu(rates, s, seed, method="direct_mean"):
    rng=np.random.default_rng(seed)
    N=len(rates)
    if method=="direct_mean":
        m,q=fnum(s,"n_direct"),1
    else:
        m,q=fnum(s,"m"),fnum(s,"q")
    a,B,D,Delta,omega=[fnum(s,k) for k in ("a","B","D","Delta","omega")]
    actual_deadline=D+Delta/2
    detector_latency=Delta/4
    timer_bits=math.ceil(math.log2(8/Delta))
    timer_tick=2.0**(-timer_bits)
    # Reserve half the declared arithmetic tolerance. Timestamp counts and
    # the reciprocal rate quantization below are exact integer operations.
    omega_fraction=Fraction(s["omega"]["numerator"],s["omega"]["denominator"])
    output_grid=omega_fraction/2
    numerator=3*2**timer_bits*output_grid.denominator
    denominator_scale=output_grid.numerator
    a_fraction=Fraction(s["a"]["numerator"],s["a"]["denominator"])
    cap_units=math.floor((3/a_fraction)/output_grid)
    blockmeans=[]
    block_sums=[]
    tally={"trials":0,"pins":0,"first_exit_records":0,"censored_trials":0,
           "active_dwell":0.0,"discarded_active_dwell":0.0,
           "clipped_successful_trials":0,"coordinate_draws":0}
    second_sum=0.0
    start=time.monotonic()
    for _ in range(q):
        idx=rng.integers(0,N,size=m)
        # The mechanism knows the requested local rate; the estimator does not.
        waits=rng.exponential(size=(m,4))/rates[idx,None]
        detected_times=waits+detector_latency
        exits=detected_times<=actual_deadline
        active=np.c_[np.ones(m,dtype=bool),np.cumprod(exits[:,:3],axis=1).astype(bool)]
        dwell=np.sum(active*np.minimum(detected_times,actual_deadline),axis=1)
        success=np.all(exits,axis=1)
        timestamp_counts=np.rint(detected_times/timer_tick).astype(np.int64)
        sum_counts=timestamp_counts.sum(axis=1)
        safe_denominator=np.maximum(sum_counts,1)*denominator_scale
        if numerator < 2**63:
            units=np.minimum(cap_units,numerator//safe_denominator)
        else:
            units=np.array([min(cap_units,numerator//int(d)) for d in safe_denominator],dtype=np.int64)
        units=np.where(success,units,0)
        output=units*float(output_grid)
        sums=sum_counts*timer_tick
        exact_sum_units=int(units.sum())
        block_sums.append(exact_sum_units)
        blockmeans.append(float(output.mean()))
        second_sum+=float(output@output)
        tally["trials"]+=m
        tally["coordinate_draws"]+=m
        tally["pins"]+=int(active.sum())
        tally["first_exit_records"]+=int((active & exits).sum())
        tally["censored_trials"]+=int((~success).sum())
        tally["active_dwell"]+=float(dwell.sum())
        tally["discarded_active_dwell"]+=float(dwell[~success].sum())
        tally["clipped_successful_trials"]+=int((success & (sums<a)).sum())
    median_sum=sorted(block_sums)[len(block_sums)//2]
    exact_estimate=Fraction(median_sum,m)*output_grid
    estimate=float(exact_estimate)
    true_mean=float(rates.mean())
    eta=fnum(s,"eta")
    eta_fraction=Fraction(s["eta"]["numerator"],s["eta"]["denominator"])
    exact_lower=exact_estimate/(1+eta_fraction)
    exact_upper=exact_estimate/(1-eta_fraction)
    interval=[float(np.nextafter(float(exact_lower),-math.inf)),
              float(np.nextafter(float(exact_upper),math.inf))]
    assert interval[0]<=true_mean<=interval[1]
    assert tally["active_dwell"]<=4*tally["trials"]*(D+Delta)
    return {"N":N,"concentration_method":method,"hidden_mean_rate_for_audit":true_mean,
            "estimated_mean_rate":estimate,"certified_interval":interval,
            "exact_estimate":{"numerator":exact_estimate.numerator,"denominator":exact_estimate.denominator},
            "exact_interval":[{"numerator":x.numerator,"denominator":x.denominator} for x in (exact_lower,exact_upper)],
            "relative_audit_error":abs(estimate/true_mean-1),
            "block_means":blockmeans,
            "empirical_second_moment":second_sum/tally["trials"],
            "conditional_second_moment_bound":4*fnum(s,"lam_max")**2,
            "sharper_conditional_second_moment_bound_for_audit":4*fnum(s,"lam_max")*true_mean,
            "timing_service":{"actual_deadline":actual_deadline,
                              "detector_latency":detector_latency,"timestamp_tick":timer_tick,
                              "output_rounding_grid":float(output_grid),
                              "declared_numerical_error_allowance":omega,
                              "reciprocal_quantization_and_final_interval_arithmetic":"exact integer/rational",
                              "persistent_timing_offsets":True,
                              "stochastic_service_failures_in_simulation":0},
            "ledger":tally,
            "worst_case_active_dwell_bound":4*tally["trials"]*(D+Delta),
            "reference_expected_active_dwell_upper":tally["trials"]*(4/fnum(s,"lam_min")+4*Delta+4*fnum(s,"beta")*(D+Delta)),
            "elapsed_execution_seconds":time.monotonic()-start}


def lower_bound_checks():
    rows=[]
    q_star=.25
    for eta in (.25,.125,.0625,.03125):
        theta=2*eta
        rplus=(1+theta)/(1-q_star)
        rminus=(1-theta)/(1-q_star)
        klplus=rplus*math.log(rplus/rminus)-rplus+rminus
        klminus=rminus*math.log(rminus/rplus)-rminus+rplus
        upper=64*eta*eta
        assert max(klplus,klminus)<=upper*(1+1e-14)
        delta=.05
        binary=(1-2*delta)*math.log((1-delta)/delta)
        rows.append({"eta":eta,"lambda0":1,"delta":delta,"q_star":q_star,
                     "stationary_target_probability":"q_star**N, for arbitrary N",
                     "max_exact_divergence_rate_over_fields":max(klplus,klminus),
                     "proved_divergence_rate_bound":upper,
                     "expected_total_exposure_lower_bound":binary/upper,
                     "completion_mean_ratio":(1+theta)/(1-theta)})
    return rows


def main():
    s=schedule()
    results=[]
    for N in (64,4096,262144):
        hidden_rng=np.random.default_rng(7315500+N)
        base=.8+.4*hidden_rng.random(N)
        protective=.5+.2*hidden_rng.random(N)
        pair=[]
        for u,rates in enumerate((base,protective)):
            result=execute_menu(rates,s,5108100+N+u)
            result["menu"]=u
            pair.append(result)
            print(json.dumps({"N":N,"menu":u,"mean":result["hidden_mean_rate_for_audit"],
                              "estimate":result["estimated_mean_rate"],
                              "pins":result["ledger"]["pins"],
                              "active_dwell":result["ledger"]["active_dwell"]}),flush=True)
        assert pair[1]["certified_interval"][1]<pair[0]["certified_interval"][0]
        results.append({"N":N,"menus":pair,"certified_minimum_rate_menu":1,
                        "global_probability_not_used_by_assay":"not requested or estimated",
                        "global_first_event_bridge":"not claimed by this local audit"})
    result={"scope":"Synthetic requested-context first-exit observations with actual simulated censoring and persistent finite timer offsets; no physical apparatus was executed.",
            "schedule":s,"analytic_checks":analytic_checks(s),"growing_family_execution":results,
            "controlled_likelihood_checks":lower_bound_checks(),
            "unpriced_physical_services":["field metrology","source/copy fidelity","pins and clamps","settling","detector and timer calibration","inter-menu slew","safe mission preparation","deployment"],
            "environment":{"python":platform.python_version(),"numpy":np.__version__,"mpmath":mp.__version__,"platform":platform.platform()},
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/"rate_assay_execution.json").write_text(json.dumps(result,indent=2)+"\n")


if __name__=="__main__":main()
