#!/usr/bin/env python3
"""Exact identities and dimensionless countermodels, not material simulations."""
from fractions import Fraction as Q
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def A(mc, mn):
    return (mn - mc) / (2 * (mc + mn))


def d(a, mc_d, mn_d, mc_l, mn_l):
    return a * (A(mc_d, mn_d) - A(mc_l, mn_l))


def main():
    # Every rational identity is exact; only the stress-law example and
    # unit conversions use floating-point arithmetic.
    example = d(Q(1), Q(10), Q(1), Q(1, 10), Q(1))
    assert example == Q(-9, 11)
    assert d(Q(1), Q(10), Q(1), Q(10), Q(1)) == 0
    assert d(Q(1), Q(10), Q(1), Q(100), Q(10)) == 0
    assert d(Q(1), Q(10), Q(0), Q(1), Q(0)) == 0
    assert d(Q(1), Q(1, 10), Q(1), Q(10), Q(1)) == -example

    # Arbitrary four branch values: phase swapping is not generally reversal.
    ad_out, ad_in, al_out, al_in = map(Q, ['0.3', '0.1', '-0.1', '-0.2'])
    d_dl = ad_out - al_in
    d_ld = al_out - ad_in
    d_dd = ad_out - ad_in
    d_ll = al_out - al_in
    assert d_dl + d_ld == d_dd + d_ll
    assert d_ld != -d_dl

    # Equal-and-opposite mechanical forces plus a direct generalized drive.
    mc, mn, gc, gn = map(Q, [2, 3, 5, 0])
    force = (mc * gc - mn * gn) / (mc + mn)
    vc, vn = mc * (-force + gc), mn * (force + gn)
    assert vc == vn == Q(6)
    dissipation = vc * vc / mc + vn * vn / mn
    assert dissipation == (gc + gn) * vc == Q(30)

    # Thermodynamic metric identity away from zero mobilities.
    for mc, mn, dc, dl in [(Q(2), Q(3), Q(4), Q(5)),
                           (Q(1, 10), Q(7), Q(-2), Q(3))]:
        endpoint_metric = (dc - dl / 2) ** 2 / mc + (dc + dl / 2) ** 2 / mn
        reduced_metric = (mc + mn) / (mc * mn) * (dc - A(mc, mn) * dl) ** 2 + dl ** 2 / (mc + mn)
        assert endpoint_metric == reduced_metric

    s_d, s_l, a, duration = 11., 1.1, 1., 1.
    t_d = duration * (1 / math.sqrt(s_d)) / (1 / math.sqrt(s_d) + 1 / math.sqrt(s_l))
    t_l = duration - t_d
    e_min = a * a * (1 / math.sqrt(s_d) + 1 / math.sqrt(s_l)) ** 2 / duration
    e_direct = a * a / (s_d * t_d) + a * a / (s_l * t_l)
    assert math.isclose(e_min, e_direct, rel_tol=1e-14)

    # Symmetric activated odd glide laws, at one fixed optical state.
    # Different activation-force scales cause force-dependent ratios.
    # v_C(F)=sinh(F), v_N(F)=sinh(2F)/2. Parameters are dimensionless.
    def stress_a(force):
        return A(math.sinh(force) / force, math.sinh(2 * force) / (2 * force))
    a_out, a_in = stress_a(.2), stress_a(2.)

    # Under equal force caps, maximizing drift per excursion need not maximize
    # drift per second. This is an algebraic cost correction, not optimization
    # of unmeasured ZnS parameters.
    rate_cases = []
    for p, q in [(10., .1), (10., 1e-8)]:
        m = math.sqrt(p * q)
        span_drift = m * (p - q) / ((m + p) * (m + q))
        motion_time = 1 / (m + p) + 1 / (m + q)  # a=Fmax=1
        rate = m * (p - q) / (p + q + 2 * m)
        assert math.isclose(rate, span_drift / motion_time, rel_tol=1e-14)
        rate_cases.append({'p': p, 'q': q, 'm': m, 'drift_per_span': span_drift,
                           'motion_time': motion_time, 'useful_rate': rate})

    # Vurgaftman et al. (2001), Eq 2.13 and Table IV: the X gap.
    # This literature parameter calculation is not measured ZnS/GaP injection.
    def gap_gapp(temp_k):
        return 2.35 - .0005771 * temp_k ** 2 / (temp_k + 372.)

    h, c, electron_charge = 6.62607015e-34, 299792458., 1.602176634e-19
    photon_j = h * c / (365e-9)
    results = {
        'scope': 'exact algebra, dimensionless countermodels, and literature-parameter conversions; no calibrated dislocation simulation',
        'exact_drift_per_span': str(example),
        'exact_nulls': ['fixed constant mode', 'common scaling', 'permanently pinned endpoint'],
        'exact_phase_swap_with_four_branches': {
            'D_out_L_in': str(d_dl), 'L_out_D_in': str(d_ld),
            'D_out_D_in': str(d_dd), 'L_out_L_in': str(d_ll),
            'phase_swap_is_negative': False,
            'sum_identity_verified': True,
        },
        'exact_direct_drive_span_servo_example': {
            'mc': '2', 'mn': '3', 'gc': '5', 'gn': '0',
            'shape_force': str(force), 'C_velocity': str(vc), 'N_velocity': str(vn),
            'glide_dissipation': str(dissipation),
        },
        'dissipation_metric_identity_verified': True,
        'constant_stroke_minimum_glide_energy': {
            'dimensionless_parameters': {'S_D': s_d, 'S_L': s_l, 'span_excursion': a, 'motion_duration': duration},
            't_D': t_d, 't_L': t_l, 'E_min': e_min, 'E_recomputed': e_direct,
            'E_equal_stroke_times': a * a / (s_d * duration / 2) + a * a / (s_l * duration / 2),
        },
        'fixed_light_stress_only_countermodel': {
            'law': 'v_C(F)=sinh(F); v_N(F)=sinh(2F)/2; positive expansion F=0.2 and negative contraction F=-2',
            'A_out': a_out, 'A_in': a_in, 'drift_per_span': a_out - a_in,
            'physical_parameters_assigned': False,
        },
        'force_capped_sharp_displacement_matching_rate_countermodel': {
            'scope': 'dimensionless a=Fmax=1 and zero switching dead time; no material parameters',
            'cases': rate_cases,
            'implication': 'infinite contrast can approach unit displacement per excursion while its displacement-optimal neutral mobility drives throughput to zero',
        },
        'symmetric_off_diagonal_mobility_countermodel': {
            'M': [[1, 2], [2, 5]], 'determinant': 1,
            'force_vector': [-1, 1], 'velocity_vector': [1, 3], 'A': 1,
            'implication': 'the |A|<=1/2 bound is specific to the diagonal endpoint law',
        },
        'literature_GaP_X_gap_calculation_eV': {str(t): gap_gapp(t) for t in [5., 300., 623.15]},
        'published_photoplastic_illumination_conversion': {
            'wavelength_nm': 365, 'photon_energy_joule': photon_j,
            'photon_energy_eV': photon_j / electron_charge,
            'irradiance_W_m2': [.7, 6.7],
            'incident_photon_flux_m2_s': [.7 / photon_j, 6.7 / photon_j],
            'optical_dwell_seconds': None, 'wall_plug_efficiency': None,
            'note': 'no cycle joule estimate is possible from irradiance without dwell and area, and wall-plug costs remain separate',
        },
        'spectral_lead_wavelength_nm': {'2.24_eV': h * c / (2.24 * electron_charge) * 1e9},
        'physical_status': 'UNACQUIRED_SAME_LOOP_RESPONSE',
    }
    (ROOT / 'calculation_results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
