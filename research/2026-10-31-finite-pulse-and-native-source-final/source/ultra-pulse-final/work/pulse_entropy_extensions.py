#!/usr/bin/env python3
"""Post-freeze analytical attacks and bounded-potential robustness.

No new draws and no edits to the frozen receiver, protocol or records.
These are additional mathematical controls, not acquired gate calibration.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/pulse_entropy'
sys.path.insert(0, str(ROOT/'work'))
from pulse_entropy import logs, enclose, down, linear_range, binary_kl_lower, dual_witness
from pulse_entropy_source import population, B, T
from ctmc_reflection_control import exp_negative_bounds
sys.path.insert(0, str(ROOT/'outputs/entropy_witnesses'))
from entropy_cone import exponential_bounds


def robust_bound(r, s, B, epsilon):
    """Static microscopic potential range <= epsilon, symmetric component <= M.

    sigma0 >= 4/(B exp(epsilon)) [min kl(u||s)-epsilon^2/8]_+,
    where u ranges over all Gibbs reweightings of the initial bit mean.
    """
    epsilon, B = F(epsilon), F(B)
    if epsilon < 0 or B <= 0:
        raise ValueError('nonnegative potential range and positive exposure required')
    eupper = enclose(*exponential_bounds(epsilon, 100))[1]
    rlo, rhi = map(F, r)
    slo, shi = map(F, s)
    ulo = rlo/(rlo+(1-rlo)*eupper)
    uhi = rhi*eupper/(1-rhi+rhi*eupper)
    if ulo > shi:
        KL = binary_kl_lower(ulo, shi)
    elif slo > uhi:
        KL = binary_kl_lower(uhi, slo)
    else:
        KL = F(0)
    initial_cost_upper = epsilon*epsilon/8
    lower = max(F(0), down(4*(KL-initial_cost_upper)/(B*eupper)))
    return {'potential_range_bound': str(epsilon), 'exp_epsilon_upper': str(eupper),
        'reference_label_mean_interval': [str(ulo), str(uhi)],
        'initial_reference_KL_upper': str(initial_cost_upper),
        'endpoint_reference_KL_lower': str(KL),
        'stationary_sigma_lower': str(lower), 'stationary_sigma_lower_preview': float(lower)}


def main():
    start = time.perf_counter()
    frozen = json.loads((OUT/'PROTOCOL.json').read_text())
    for path, sha in frozen['code_SHA256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == sha
    driven = json.loads((OUT/'driven_inference.json').read_text())
    box = [tuple(map(F, row)) for row in driven['probability_box']]
    r = linear_range([0, 0, 1, 1], box)
    s = linear_range([0, 1, 0, 1], box)
    curve = [robust_bound(r, s, B, eps) for eps in
        (F(0), F(1, 50), F(1, 20), F(1, 10), F(1, 5), F(1, 2))]
    assert curve[0]['stationary_sigma_lower'] == driven['ordinary_shared_method_comparators']['ordinary_marginal_KL_rate_lower']
    assert F(curve[4]['stationary_sigma_lower']) > 0
    # The amplitude envelope cannot be replaced by an unmeasured setting.
    # Scale the baseline down, scale only the actual cut multiplier up.
    scale = F(1, 1000)
    amplified, tail = population(p=10*scale, q=scale, gate=16/scale)
    wrong = down(4*dual_witness(amplified)[0]/B)
    right = down(4*dual_witness(amplified)[0]/(B/scale))
    true_sigma_upper = 9*scale*logs(F(10))[1]
    assert wrong > true_sigma_upper and right < true_sigma_upper
    # Small conservative contamination in a reversible source. The visible
    # pulsed chain is exactly lumpable, with rates 176*a and 88/a. Its
    # baseline stationary entropy is zero, but the pure-kinetic formula
    # would report a positive population floor if the potential were hidden.
    a = F(21, 20)
    h = [2*x for x in logs(a)]
    assert 0 < h[0] <= h[1] < F(1, 10)
    k = 176*a+88/a
    u = (88/a)/k
    elo, ehi = exp_negative_bounds(k*T, 180)
    terminal = enclose(u+(F(1, 3)-u)*elo, u+(F(1, 3)-u)*ehi)
    naive = 4*binary_kl_lower(F(1, 3), terminal[1])/B
    robust = robust_bound((F(1, 3), F(1, 3)), terminal, B, F(1, 10))
    assert naive > 0 and F(robust['stationary_sigma_lower']) == 0
    # Exact detailed-balance check for the tilted geometric reference on a
    # nonuniform pi, with irrational potentials represented by their rational
    # exp(V/2). This independently checks the cancellation after the tilt.
    pi = [F(1, 2), F(1, 3), F(1, 6)]
    half_exp = [F(1), F(21, 20), F(10, 9)]
    Z = sum((pi[i]/half_exp[i]**2 for i in range(3)), F(0))
    rho = [pi[i]/half_exp[i]**2/Z for i in range(3)]
    tilted_pair_checks = 0
    for i in range(3):
        j = (i+1) % 3
        Qij, Qji = 9/pi[i], 4/pi[j]
        Rij, Rji = 6/pi[i], 6/pi[j]
        RVij, RVji = Rij*half_exp[i]/half_exp[j], Rji*half_exp[j]/half_exp[i]
        QVij, QVji = Qij*half_exp[i]/half_exp[j], Qji*half_exp[j]/half_exp[i]
        c = rho[i]*RVij
        assert c == rho[j]*RVji
        assert (RVij/QVij)*(RVji/QVji) == 1
        expected = (9+4-12)/(Z*half_exp[i]*half_exp[j])
        assert rho[i]*QVij+rho[j]*QVji-2*c == expected
        tilted_pair_checks += 1
    result = {'status': 'PULSE_CALIBRATION_BOUNDARIES_AND_CONSERVATIVE_ROBUSTNESS_PASSED',
        'post_freeze_extension': True, 'new_draws': 0, 'frozen_code_and_records_changed': False,
        'same_confidence_set_robustness_curve': curve,
        'robustness_requires': ['static state potential V with supplied range bound epsilon',
            'actual q_pulse_ij=m_ij*q_ij*exp((V_i-V_j)/2)', 'symmetric m with supplied envelope',
            'same independent stationary preparation and calibrated time/sensor contract'],
        'arbitrary_asymmetric_actuator_errors': 'NOT_COVERED by bounded conservative-potential theorem',
        'unbounded_amplitude_counterexample': {'baseline_rate_scale': str(scale),
            'true_cut_multiplier': str(16/scale), 'incorrectly_assumed_cut_envelope': '16',
            'true_sigma_upper': str(true_sigma_upper), 'true_sigma_upper_preview': float(true_sigma_upper),
            'wrong_pure_pulse_floor_preview': float(wrong), 'correct_amplitude_floor_preview': float(right),
            'population_enclosure': [[str(a), str(b)] for a, b in amplified],
            'uniformization_tail_upper': str(tail),
            'finite_n_limit_obstruction': 'TV(p_s^n,p_star^n)<=10*n*s*T, while baseline sigma_s=9*s*log(10) tends to zero'},
        'small_energy_contamination_equilibrium_counterexample': {'baseline_sigma': '0',
            'exp_potential_half': str(a), 'potential_range_enclosure': list(map(str, h)),
            'potential_range_bound': '1/10', 'initial_mean': '1/3',
            'terminal_mean_enclosure': list(map(str, terminal)),
            'naive_pure_kinetic_floor_preview': float(naive),
            'correct_robust_floor': robust['stationary_sigma_lower'],
            'tilted_reference_detailed_balance_and_log_cancellation_pair_checks': tilted_pair_checks},
        'physical_calibration_acquired': False, 'independent_audit': 'NOT_PERFORMED',
        'CPU_wall_seconds': time.perf_counter()-start,
        'code_SHA256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'extensions.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'seconds': result['CPU_wall_seconds'],
        'robust_curve': [{'epsilon': x['potential_range_bound'], 'floor': x['stationary_sigma_lower_preview']} for x in curve],
        'amplitude_counterexample': {'true_sigma_upper': float(true_sigma_upper), 'wrong_floor': float(wrong), 'correct_floor': float(right)},
        'energy_contamination_naive_floor': float(naive), 'correct_floor': robust['stationary_sigma_lower'],
        'new_draws': 0}, indent=2))


if __name__ == '__main__':
    main()
