"""Propagate the rational short-excursion counts and compare with exact means."""
from fractions import Fraction as F
from pathlib import Path
import json
import math

HERE=Path(__file__).resolve().parent


def displayed(x):
    return {"exact":str(x),"decimal":float(x)}


def main():
    exact=json.loads((HERE/"code_target_exact.json").read_text())
    counts=json.loads((HERE/"code_receiver_counts.json").read_text())
    N=counts["trials"]
    success=counts["killed_before_return"]
    n=exact["n"]
    p=F(exact["p_exact"])
    b=1-p
    s=F(exact["s_exact"])
    M0=F(exact["M0_exact"])
    Rs=F(exact["Rs_exact"])
    mu=F(exact["receiver_success_probability_exact"])
    muhat=F(success,N)
    halfwidth=F(1,120)
    mulo=max(F(0),muhat-halfwidth)
    muhi=min(F(1),muhat+halfwidth)
    rhat=s+n*muhat
    rlo=s+n*mulo
    rhi=s+n*muhi
    Rhat=1/(p*rhat)-1/s
    Rlo=1/(p*rhi)-1/s
    Rhi=1/(p*rlo)-1/s
    assert mulo<=mu<=muhi
    assert Rlo<=Rs<=Rhi
    intervals={}
    for name,g in (("full_reference_gap",F(2)),
                   ("exact_quotient_gap",F(2*exact["minimum_nonzero_dual_weight"]))):
        factor=1+s/g
        lo=Rlo/(b*factor)
        hi=Rhi*factor/b
        assert lo<=M0<=hi
        intervals[name]={"g_exact":str(g),"screen_factor_exact":str(factor),
                         "M_lower":displayed(lo),"M_upper":displayed(hi),
                         "lower_over_exact":float(lo/M0),"upper_over_exact":float(hi/M0)}
    out={
        "n":n,"m":exact["m"],"target_probability":displayed(p),
        "exact_reference_mean":displayed(M0),
        "trials":N,"successes":success,
        "true_success_probability":displayed(mu),"observed_success_fraction":displayed(muhat),
        "absolute_success_error":float(abs(muhat-mu)),
        "confidence_halfwidth":str(halfwidth),
        "hoeffding_failure_bound":2*math.exp(-2*N*float(halfwidth)**2),
        "confidence_event_contains_true_probability":True,
        "r_s_estimate":displayed(rhat),"exact_r_s":displayed(F(exact["r_s_exact"])),
        "R_s_estimate":displayed(Rhat),"exact_R_s":displayed(Rs),
        "mean_point_proxy_Rhat_over_b":displayed(Rhat/b),
        "point_proxy_over_exact_mean":float(Rhat/(b*M0)),
        "mean_intervals":intervals,
        "expected_following_events_exact":displayed(N*(10*n+1)*mu),
        "expected_following_event_upper_bound":N*(10*n+1),
        "high_probability_following_event_cap":2*N*(10*n+1),
        "event_cap_failure_bound_description":"at most exp(-trials/4) under independent ideal bits",
        "following_events_observed":counts["following_events_including_kills"],
        "all_initial_and_following_events_observed":counts["total_boundary_and_following_events"],
        "conditional_target_preparation_paid":{
            "uniform_codewords":counts["conditional_samples"],
            "free_bit_entropy":counts["conditional_sample_random_bits"],
            "Pz_xors":counts["conditional_codeword_parity_xors"],
            "initial_coordinate_inspections":counts["initial_membership_bit_inspections"],
            "initial_membership_xors":counts["initial_membership_xors"]},
        "rng64_words_observed":counts["rng64_words_drawn"],
        "total_prng_bits_observed":64*counts["rng64_words_drawn"],
        "rng_rejections":counts["rng_rejections"],
        "host_wall_seconds_one_diagnostic_run":counts["host_wall_seconds_this_run"],
        "native_80_bit_calibration_claimed":False,
        "ordinary_reference_method_already_exact":True,
        "limitations":["This is a known uniform reference, not acquired unknown native rates.",
                       "The weight-enumerator baseline is exact conventional machinery.",
                       "Seeded PRNG execution illustrates the receiver; confidence assumes independent ideal bits.",
                       "One measured host runtime is not a general hardware-performance claim."]}
    (HERE/"code_receiver_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"exact_mean":float(M0),"point_proxy":float(Rhat/b),
        "point_ratio":float(Rhat/(b*M0)),"failure_bound":out["hoeffding_failure_bound"],
        "full_gap_interval":[intervals["full_reference_gap"]["M_lower"]["decimal"],
                             intervals["full_reference_gap"]["M_upper"]["decimal"]],
        "quotient_gap_interval":[intervals["exact_quotient_gap"]["M_lower"]["decimal"],
                                 intervals["exact_quotient_gap"]["M_upper"]["decimal"]]},indent=2))


if __name__=="__main__":
    main()
