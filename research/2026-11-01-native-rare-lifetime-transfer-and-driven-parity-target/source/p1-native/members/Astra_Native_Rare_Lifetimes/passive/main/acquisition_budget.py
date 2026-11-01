"""Analytical budgets, not executed large native acquisitions.

All reported real-number constants are floating diagnostics of formulas proved
in REFERENCE_TRANSFER.txt. A one-percent slack is added to the planned exposure
and horizon. This script does not purport to be an interval-arithmetic package.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import math


def transfer(n, m, eta, c=1.0, lam=None, product_reference=False):
    lam = (n*c if product_reference else 2*n-1) if lam is None else lam
    a = eta*lam/(c*(1-eta))
    beta = a/(1+a)
    r = math.log(4*(n-1)/beta)/(2*c)
    u_met = 2*eta*lam*r/(1-eta)-math.log1p(-beta)
    tinf = (math.log(4*(n-1))+2)/(4*c)
    aa = 2*eta*lam*tinf
    candidates = [(u_met, 'Metzler')]
    if aa < 0.5:
        candidates.append((math.log((1-aa)/(1-2*aa)), 'resolvent'))
    if product_reference and aa < 1:
        zprod = n*eta/(1-aa)
        if zprod < 1:
            candidates.append((-math.log1p(-zprod), 'product forcing'))
    u, method = min(candidates)
    v = u-math.log1p(-eta)
    kval = math.sqrt(lam/c)
    logf = 2*math.asinh(kval*math.sinh(v/2))
    p0 = 2.0**(-m)
    # log1p retains the tiny target normalization corrections.
    loglo = -2*u-logf+math.log1p(-p0)-math.log1p(-math.exp(-u)*p0)
    loghi = 2*u+logf+math.log1p(-p0)-math.log1p(-math.exp(u)*p0)
    kappa = kval*math.expm1(v)
    if product_reference:
        rlo = -2*u-v-math.log1p(kappa**2)+math.log1p(-p0)-math.log1p(-math.exp(-u)*p0)
        rhi = 2*u+v+math.log1p(-p0)-math.log1p(-math.exp(u)*p0)
        loglo, loghi = max(loglo, rlo), min(loghi, rhi)
    return dict(eta=eta, beta=beta, r_beta=r, u=u, v=v, K=kval, logF=logf,
                stationary_bound_method=method, stationary_Metzler_bound=u_met,
                resolvent_T_infinity=tinf, resolvent_contraction_a=aa,
                product_reference=product_reference, circulation_kappa=kappa,
                rare_mean_ratio_lower=math.exp(loglo), rare_mean_ratio_upper=math.exp(loghi),
                generic_mean_factor=math.exp(3*u+logf),
                actual_gap_lower=(1-eta)*math.exp(-2*u)*(2*c),
                target_mass_reference=p0)


def budget(n, m, product_reference=False):
    # Seek a 1.24 transfer factor, leaving display/numerical room below 1.25.
    low, high = 1e-12, 0.05
    for _ in range(90):
        mid = (low+high)/2
        test = transfer(n, m, mid, product_reference=product_reference)
        if max(test['rare_mean_ratio_upper'], 1/test['rare_mean_ratio_lower']) <= 1.24:
            low = mid
        else:
            high = mid
    eta = low
    out = transfer(n, m, eta, product_reference=product_reference)
    h = (32*n-80 if product_reference else 36*n-88)
    gamma = eta/5
    q_min = 0.9
    alpha_rate, alpha_occ = 0.001, 0.001
    # True source within eta/2 of the reference leaves an admission margin.
    assert (1+eta/2)*(1+gamma)/(1-gamma)-1 <= eta
    assert 1-(1-eta/2)*(1-gamma)/(1+gamma) <= eta
    rquota = math.ceil(1.01*3*math.log(2*h/alpha_rate)/(q_min*gamma**2))
    pstar = math.exp(-out['u'])/32
    g = out['actual_gap_lower']
    log_c = (n*math.log(2)+out['u'])/2
    t_occ = (8/(g*pstar))*(math.log(h/alpha_occ)+log_c)
    horizon = math.ceil(1.01*max(4*rquota/pstar, t_occ))
    lam = n if product_reference else 2*n-1
    s = 0.1  # reference gap/20; no committor is used for this lower bound
    p0 = out['target_mass_reference']
    mean_ref_lo = (1/(p0*(lam+s))-1/s)/((1-p0)*(1+s/2))
    if product_reference:
        exact_ref = sum((F(math.comb(m,j), j) for j in range(1,m+1)), F(0))/(2*(1-F(1,2**m)))
        mean_ref_lo = float(exact_ref)
        out['exact_reference_mean_fraction'] = str(exact_ref)
    mean_actual_lo = mean_ref_lo*out['rare_mean_ratio_lower']
    out.update(n=n, target_fixed_bits=m, target_free_bits=n-m,
               reference=('unit independent flips' if product_reference else
                          'unit independent flips + unit alternating preserving pair cycles'),
               all_aggregate_context_count=h, max_context_bits=5,
               assumed_true_relative_distance_for_planning=eta/2,
               acquisition_relative_precision_gamma=gamma,
               occupation_quota_per_cell=rquota, local_context_mass_lower=pstar,
               deterministic_native_horizon=horizon,
               expected_observed_native_jumps_upper=(1+eta)*lam*horizon,
               source_coverage_lower=1-alpha_rate-alpha_occ,
               reference_mean_used=mean_ref_lo,
               reference_mean_status=('exact ordinary Hamming-weight solve' if product_reference else
                                      'proved coarse lower bound, without rare simulation'),
               transferred_actual_mean_lower=mean_actual_lo,
               mean_lower_divided_by_acquisition_horizon=mean_actual_lo/horizon,
               walltime_bound_beats_mean_lower=mean_actual_lo>horizon,
               work_note='Observed jumps only. Unknown null clocks/physical implementation costs are not inferred.')
    return out


def entropy_failure():
    n, m, c, eta = 80, 64, 0.5, 1e-6
    lam = n*c
    killed_radius_upper = m*c/(2**m-1)
    entropy_integrand_lower = n*c*eta**2/(2*(1+eta))
    out = transfer(n, m, eta, c, lam, product_reference=True)
    out.update(n=n, m=m, c=c, reference='independent flips',
               actual_class='every flip perturbed by a local state-dependent sign times eta',
               killed_mgf_radius_upper=killed_radius_upper,
               stopped_entropy_rate_lower=entropy_integrand_lower,
               entropy_rate_to_radius_ratio=entropy_integrand_lower/killed_radius_upper,
               reduced_m_coordinate_entropy_ratio=(m*c*eta**2/(2*(1+eta)))/killed_radius_upper,
               rate_only_stopped_path_upper_bound_infinite=entropy_integrand_lower>=killed_radius_upper,
               comparison_scope='This failure concerns the rate-based stopped-path entropy instantiation, not all goal-oriented divergences.')
    return out


def main():
    rows = [budget(n, n-16, product_reference=prod)
            for prod in (False, True) for n in (32, 48, 64, 80, 96, 128)]
    out = dict(status='Analytical resource forecasts only; no large native records generated.',
               receiver_cost_excluded_from_acquisition_table=True,
               receiver_cost_source='Existing MAIN_PROOF and original large executions; must be added to native acquisition.',
               budgets=rows, exact_entropy_comparator_formula=entropy_failure())
    path = Path(__file__).with_name('acquisition_budget.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    for x in rows:
        print(json.dumps({k:x[k] for k in ('n','target_fixed_bits','product_reference','eta','occupation_quota_per_cell',
              'deterministic_native_horizon','expected_observed_native_jumps_upper',
              'mean_lower_divided_by_acquisition_horizon','rare_mean_ratio_upper')}))
    print(json.dumps(out['exact_entropy_comparator_formula']))


if __name__ == '__main__':
    main()
