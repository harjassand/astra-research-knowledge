"""Final driven-reference certificate, with exact rational error propagation.

The 80-bit reference receiver was actually executed. The large native-source
acquisition remains a proved protocol/budget, not an observed data record.
The product-reference certificate is retained as a stronger ordinary baseline.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from coded_target_certificate import exp_lower, exp_upper, outward


def main():
    here = Path(__file__).resolve().parent
    counts = json.loads((here.parent/'code_target/driven_code_receiver_counts.json').read_text())
    assert counts['n'] == 80 and counts['m'] == 64 and counts['trials'] == 40000
    assert counts['boundary_dominating_rate'] == 159
    assert counts['following_total_integer_weight'] == 1591
    assert counts['full_state_syndrome_checks'] == 80000
    p, b = F(1, 2**64), 1-F(1, 2**64)
    theta = F(counts['killed_before_return'], counts['trials'])
    halfwidth, s, screen = F(1, 100), F(1, 10), F(21, 20)
    assert 0 < theta-halfwidth < theta+halfwidth < 1
    r_lo, r_hi = s+159*(theta-halfwidth), s+159*(theta+halfwidth)
    reference_lo = (1/(p*r_hi)-1/s)/(b*screen)
    reference_hi = screen*(1/(p*r_lo)-1/s)/b
    query_failure = F(2)/exp_lower(2*counts['trials']*halfwidth**2)
    assert query_failure < F(7, 10000)

    # General driven reference: pi0 uniform, c=1, g=2, Lambda=159.
    eta, lam = F(1, 50000), F(159)
    assert exp_lower(6) > 316
    tinf_upper = F(2)  # [log(316)+2]/4 < 2
    aa = 2*eta*lam*tinf_upper
    assert aa < F(1, 2)
    zz = aa/(1-aa)
    u = F(131, 10000)
    assert zz/(1-zz) < u
    v = F(657, 50000)
    assert u+eta/(1-eta) < v
    kbar = F(127, 10)
    assert kbar**2 > 159
    # log F <= K*v for K>=1; this avoids irrational numerical evaluation.
    upper_exp = exp_upper(2*u+kbar*v)
    eu = exp_upper(u)
    assert b/upper_exp > F(4, 5)
    assert upper_exp*b/(1-eu*p) < F(5, 4)
    model_lo, model_hi = F(4, 5), F(5, 4)
    native_lo, native_hi = model_lo*reference_lo, model_hi*reference_hi
    gap_lo = F(19, 10)
    assert 2*(1-eta)/exp_upper(2*u) > gap_lo
    assert eu < 2
    p_plus, b_minus = 2*p, 1-2*p
    delta_hi = 1/(gap_lo*b_minus*native_lo)
    assert delta_hi < F(1, 10**17)
    assert exp_lower(80) > 1+F(10**34, 4)
    shape_bound = F(368, 3*10**17)
    error = F(1, 10**14)
    assert (shape_bound+p_plus)/b_minus+p_plus < error
    deadline = F(10**17)
    cdf_lo = 1-1/exp_lower(deadline/native_hi)-error
    cdf_hi = 1-1/exp_upper(deadline/native_lo)+error

    # Complete native aggregate-rate observations: five-bit single-flip and
    # four-bit pair contexts; exact support is an independent architecture input.
    cells, qmin = 36*80-88, F(9, 10)
    gamma, quota, horizon = eta/5, 4*10**12, 54*10**13
    assert (1+eta/2)*(1+gamma)/(1-gamma) <= 1+eta
    assert (1-eta/2)*(1-gamma)/(1+gamma) >= 1-eta
    assert qmin*quota*gamma**2/3 > 18
    rate_failure = F(2*cells)/exp_lower(18)
    assert rate_failure < F(1, 10000)
    context_floor = F(3, 100)
    assert 1/(32*eu) > context_floor
    assert horizon > 4*quota/context_floor
    assert gap_lo*context_floor*horizon/8 > 100
    assert cells < 2**12
    occupation_failure = F(2**53)/exp_lower(100)
    assert occupation_failure < F(1, 10000)
    total_failure = query_failure+rate_failure+occupation_failure
    assert total_failure < F(9, 10000)

    out = dict(
        status='Executed driven-reference receiver + conditional native theorem; no high-precision 80-bit native acquisition performed.',
        all_rational_checks_passed=True,
        source_cutoff='51ce47ce39f976517d60e2f87bbe280b651f6056',
        target='saved 80-bit code with 64 parity constraints and 65536 target states',
        target_probability_reference=str(p),
        reference='80 unit flips + 79 alternating directed unit pair cycles; uniform pi0; symmetric gap at least 2',
        exact_driven_mean_claimed=False, reference_syndrome_lumping_assumed=False,
        receiver=dict(trials=counts['trials'], successes=counts['killed_before_return'],
                      theta_exact=str(theta), halfwidth=str(halfwidth),
                      mean_lower_exact=str(reference_lo), mean_upper_exact=str(reference_hi),
                      mean_lower=outward(reference_lo, 6), mean_upper=outward(reference_hi, 6, True),
                      statistical_failure_upper_decimal=float(query_failure),
                      total_proposal_calls=counts['total_boundary_and_following_events'],
                      full_state_syndrome_checks=counts['full_state_syndrome_checks']),
        model_transfer=dict(edge_relative_box=str(eta), stationary_log_bound=str(u),
                            flow_log_bound=str(v), actual_gap_lower=str(gap_lo),
                            mean_ratio_lower=str(model_lo), mean_ratio_upper=str(model_hi),
                            actual_Gibbs_law_assumed=False, actual_short_cycle_stationary_decomposition_assumed=False),
        actual_native_mean_lower=outward(native_lo, 6),
        actual_native_mean_upper=outward(native_hi, 6, True),
        actual_native_mean_lower_exact=str(native_lo), actual_native_mean_upper_exact=str(native_hi),
        deadline=int(deadline), deadline_probability_lower=outward(cdf_lo),
        deadline_probability_upper=outward(cdf_hi, upper=True),
        additive_shape_error_allowance=str(error),
        initial_law='actual stationary distribution conditioned outside the target',
        acquisition=dict(status='proved budget only', cells=cells, max_context_bits=5,
                         occupation_quota_per_cell=quota, relative_rate_precision=str(gamma),
                         true_distance_margin_for_guaranteed_admission=str(eta/2),
                         deterministic_native_horizon=horizon,
                         expected_observed_native_jump_count_upper=str((1+eta)*lam*horizon),
                         unknown_null_clock_or_hardware_work_bounded=False),
        joint_confidence_lower='9991/10000 = 0.9991',
        joint_failure_upper_decimal=float(total_failure),
        qualifications=['Complete ordered native observations, calibrated time, known kinetic range/support, and no source drift are premises.',
                        'The 80-bit source acquisition budget was not executed; only smaller native fixtures were run.',
                        'Seeded reference simulation is a diagnostic; statistical coverage assumes independent ideal random bits.',
                        'Ordinary product/cylinder/code baselines are preserved and are not claimed as new discoveries.',
                        'This construction does not establish historical priority or fastest-algorithm superiority.'])
    (here/'driven_code_certificate.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if not k.endswith('_exact')}, indent=2))


if __name__ == '__main__':
    main()
