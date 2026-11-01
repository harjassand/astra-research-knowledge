"""Rational confidence propagation for the driven, nonreversible reference."""
from fractions import Fraction as F
from pathlib import Path
import json
import math

HERE=Path(__file__).resolve().parent


def show(x):
    return {"exact":str(x),"decimal":float(x)}


def main():
    code=json.loads((HERE/"code_target_exact.json").read_text())
    counts=json.loads((HERE/"driven_code_receiver_counts.json").read_text())
    n,N=counts["n"],counts["trials"]
    rate=2*n-1
    p=F(code["p_exact"])
    b=1-p
    s,g=F(1,10),F(2)
    muhat=F(counts["killed_before_return"],N)
    halfwidth=F(1,120)
    mulo=max(F(0),muhat-halfwidth)
    muhi=min(F(1),muhat+halfwidth)
    rhat=s+rate*muhat
    rlo=s+rate*mulo
    rhi=s+rate*muhi
    Rhat=1/(p*rhat)-1/s
    Rlo=1/(p*rhi)-1/s
    Rhi=1/(p*rlo)-1/s
    factor=1+s/g
    Mlo=Rlo/(b*factor)
    Mhi=Rhi*factor/b
    assert counts["killed_before_return"]+counts["returned_after_initial_exit"]+counts["initial_proposals_staying_in_target"]==N
    assert counts["initial_proposals_staying_in_target"]==counts["initial_null_proposals"]
    assert counts["following_primitive_proposals"]+counts["killed_before_return"]==counts["following_events_including_kills"]
    assert counts["following_null_proposals"]+counts["following_single_bit_moves"]+counts["following_two_bit_moves"]==counts["following_primitive_proposals"]
    assert counts["full_state_syndrome_checks"]==2*N
    # Structural, exact failure of syndrome lumping. Both0 and this codeword
    # have syndrome0, but a pair01 is fixed by its three-cycle. Every nonnull
    # one/two-bit move exits C because its minimum distance is22.
    witness=int(code["minimum_kernel_words_hex"][0],16)
    null_edges=[i for i in range(n-1) if ((witness>>i)&3)==2]
    assert null_edges and code["minimum_nonzero_kernel_weight"]>2
    witness_syndrome=0
    for i,col in enumerate(code["H_columns_uint64"]):
        if (witness>>i)&1:
            witness_syndrome ^= col
    assert witness_syndrome==0
    out={
        "reference":"80 unit coordinate flips plus79 alternating unit three-cycle permutations",
        "n":n,"m":code["m"],"uniform_stationary_law_earned_by_permutation_invariance":True,
        "source_gap_lower_bound":str(g),"target_mass":show(p),
        "dominant_primitive_rate":rate,"kill_rate":str(s),
        "trials":N,"killed_before_return":counts["killed_before_return"],
        "returned_after_initial_exit":counts["returned_after_initial_exit"],
        "initial_nulls_included_as_zero_trials":counts["initial_null_proposals"],
        "observed_success_fraction":show(muhat),"confidence_halfwidth":str(halfwidth),
        "hoeffding_failure_bound":2*math.exp(-2*N*float(halfwidth)**2),
        "r_s_estimate":show(rhat),"r_s_confidence_interval":[show(rlo),show(rhi)],
        "R_s_estimate":show(Rhat),"R_s_confidence_interval":[show(Rlo),show(Rhi)],
        "nonreversible_two_sided_screen_factor":str(factor),
        "reference_mean_interval":[show(Mlo),show(Mhi)],
        "mean_point_proxy_Rhat_over_b":show(Rhat/b),
        "exact_driven_mean_computed":False,
        "reference_mean_interval_uses_quotient_lumping":False,
        "native_80_site_acquisition_claimed":False,
        "exact_syndrome_lumping_failure":{
            "two_same_syndrome_states_hex":["0x0",hex(witness)],
            "common_syndrome":0,
            "zero_state_exit_rate_from_target":rate,
            "witness_exit_rate_from_target":rate-len(null_edges),
            "witness_null_pair_edges":null_edges},
        "exact_nonreversibility_witness":{
            "state_pair_hex":["0x0","0x1"],"forward_rate":2,"backward_rate":1,
            "stationary_weights_equal":True},
        "total_initial_and_following_events":counts["total_boundary_and_following_events"],
        "all_following_nulls_paid":counts["following_null_proposals"],
        "initial_membership_bit_inspections":counts["initial_membership_bit_inspections"],
        "final_membership_bit_inspections":counts["final_membership_bit_inspections"],
        "syndrome_transition_xors":counts["syndrome_transition_xors"],
        "rng64_words":counts["rng64_words_drawn"],
        "rng64_bits":64*counts["rng64_words_drawn"],
        "expected_following_event_upper_bound":N*(10*rate+1),
        "following_event_cap":2*N*(10*rate+1),
        "event_cap_failure_bound_description":"at most exp(-trials/4) under independent ideal bits",
        "host_wall_seconds_single_receiver_run":counts["host_wall_seconds_this_run"],
        "limitations":["Reference rates, target matrix and uniform stationary law are supplied mathematical data.",
                       "The full80-bit state is simulated; syndrome is only a maintained membership statistic.",
                       "No exact driven mean is supplied by the product MacWilliams calculation.",
                       "Confidence assumes independent ideal bits; the executed seeded PRNG is a reproducible diagnostic.",
                       "Applying a native perturbation certificate additionally requires the specified native admission event."]}
    (HERE/"driven_code_receiver_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"success":float(muhat),"rhat":float(rhat),"M_point_proxy":float(Rhat/b),
                      "M_interval":[float(Mlo),float(Mhi)],
                      "failure_bound":out["hoeffding_failure_bound"],
                      "all_initial_and_following_events":out["total_initial_and_following_events"]},indent=2))


if __name__=="__main__":
    main()
