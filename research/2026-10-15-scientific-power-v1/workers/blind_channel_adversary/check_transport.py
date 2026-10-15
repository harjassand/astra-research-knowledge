"""Internal analytic checks for blind-channel adversarial models.

No laboratory observations. Input transport constants are explicitly illustrative.
Only Python's standard library is required.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def remaining_mass(tau: float, modes: int = 2000) -> float:
    """Uniform initial solute, clean mouth, reflecting distal end; tau = D t / L^2."""
    return 8 / math.pi**2 * sum(
        math.exp(-(2 * n + 1) ** 2 * math.pi**2 * tau / 4) / (2 * n + 1) ** 2
        for n in range(modes)
    )


def quantile_tau(epsilon: float) -> float:
    lo, hi = 0.0, 100.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if remaining_mass(mid) > epsilon:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def rectangular_resistance(length: float, narrow: float, wide: float, mu: float) -> float:
    """Fully developed Newtonian flow, no slip, straight rectangular lane."""
    assert 0 < narrow <= wide
    correction = 1 - 192 * narrow / (math.pi**5 * wide) * sum(
        math.tanh(n * math.pi * wide / (2 * narrow)) / n**5
        for n in range(1, 10001, 2)
    )
    return 12 * mu * length / (wide * narrow**3 * correction)


tau = quantile_tau(0.01)
diffusion = []
hydraulics = []
for label, length, side in [('topology_fixture', 0.01, 0.001), ('manufacturing_fixture', 0.08, 0.0005)]:
    for d in (1e-9, 1e-10, 1e-11):
        seconds = tau * length**2 / d
        diffusion.append(dict(fixture=label, L_m=length, D_assumed_m2_s=d,
                              t_99pct_s=seconds, t_99pct_days=seconds / 86400))
    delta = side * 0.05
    width = (side - delta) / 2
    mu = 1e-3
    q = 1e-10  # 0.1 microlitre/s, arbitrary comparison rate
    r_loop = 2 * rectangular_resistance(length, width, side, mu)
    u = q / (width * side)
    hydraulics.append(dict(fixture=label, L_m=length, side_m=side, delta_m=delta,
                           mu_assumed_Pa_s=mu, Q_assumed_m3_s=q,
                           ideal_loop_R_Pa_s_m3=r_loop, ideal_pressure_Pa=r_loop*q,
                           mean_speed_m_s=u, residence_loop_s=2*length/u,
                           Pe_L_at_D_1e_9=u*length/1e-9,
                           lane_transverse_diffusion_s_at_D_1e_9=width**2/1e-9))

leak = [dict(kappa_L=k, tip_flow_ratio=k/math.sinh(k)) for k in (0.1, 1, 2, 5, 10)]
length, side, delta, pitch, crack_width, mu = .08, .0005, .000025, .001, .000010, .001
lane_r = rectangular_resistance(length, (side-delta)/2, side, mu)/length
crack_g = 1/rectangular_resistance(delta, crack_width, side, mu)
n_segments = round(length/pitch)
alpha = math.acosh(1 + lane_r*pitch*crack_g)
discrete_tip_ratio = n_segments*math.sinh(alpha)/math.sinh(n_segments*alpha)
continuum_k = length*math.sqrt(2*lane_r*crack_g/pitch)
gas_fraction = 0.5
pressure_ratio = 0.5  # P_low/P_high
mass_ratio = (1-gas_fraction)/(1-gas_fraction*pressure_ratio)
result = dict(
    status='INTERNAL_ANALYTIC_CHECK_ONLY',
    mass_diffusion_tau_1pct=tau,
    first_mode_tau_1pct=4/math.pi**2 * math.log(8/(math.pi**2*0.01)),
    mass_fraction_at_computed_tau=remaining_mass(tau),
    diffusion_examples=diffusion,
    ideal_hydraulics=hydraulics,
    leaky_septum_examples=leak,
    explicit_partially_erased_septum_countermodel=dict(
        status='HYPOTHETICAL_GEOMETRY_NO_MATERIAL_EROSION_DATA',
        L_m=length, side_m=side, septum_thickness_m=delta,
        perforation_axial_width_m=crack_width,
        perforation_height_m=side,
        perforation_pitch_m=pitch,
        number_of_perforated_internal_nodes=n_segments-1,
        lane_resistance_per_m_Pa_s_m4=lane_r,
        each_cross_crack_conductance_m3_Pa_s=crack_g,
        discrete_ladder_tip_flow_ratio=discrete_tip_ratio,
        continuum_kappa_L=continuum_k,
        continuum_tip_flow_ratio=continuum_k/math.sinh(continuum_k),
        assumptions=['straight fully developed rectangular Newtonian resistors',
                     'fixed root pressure difference', 'negligible entrance and Uturn resistances',
                     '79 equal distributed leaks; completely sealed elsewhere']),
    gas_compartment_countermodel=dict(
        gas_fraction_at_low_pressure=gas_fraction,
        P_low_over_P_high=pressure_ratio,
        complete_mixing_assumed=True,
        mass_retained_each_complete_cycle=mass_ratio,
        mass_retained_after_12_cycles=mass_ratio**12,
        net_volume_flow_per_complete_cycle=0,
    ),
    liquid_only_pulse_example=dict(beta_assumed_Pa_inverse=4.5e-10,
                                  delta_P_assumed_Pa=1e5,
                                  fractional_stroke=4.5e-5,
                                  required_ideal_well_mixed_cycles_99pct=math.ceil(math.log(0.01)/math.log(1-4.5e-5))),
    removable_tube_comparator=dict(
        status='IDEAL_HYDRAULICS_ONLY_INSERTION_AND_EXTRACTION_UNKNOWN',
        L_m=.08, tube_inner_diameter_m=.0001, tube_outer_diameter_m=.0002,
        Q_m3_s=1e-10, mu_assumed_Pa_s=.001,
        ideal_tube_pressure_drop_Pa=8*.001*.08*1e-10/(math.pi*(.0001/2)**4),
        tube_cross_section_fraction_of_500um_square=math.pi*(.0002/2)**2/(.0005**2),
        final_channel_volume_m3=.08*.0005**2,
        five_final_channel_volumes_s=5*.08*.0005**2/1e-10,
        warning='Five pumped volumes do not certify 99% residue removal.'),
    lollipop_mutation=dict(
        status='TWO_DISTINCT_MOUTHS_AT_TWO_PRESSURE_NODES_ASSUMED',
        loop_length_m=.08, loop_cross_section_m=[.001,.001],
        chamber_segment_length_m=.003, chamber_cross_section_m=[.001,.003],
        loop_R_Pa_s_m3=rectangular_resistance(.08,.001,.001,.001),
        chamber_R_Pa_s_m3=rectangular_resistance(.003,.001,.003,.001),
        unpartitioned_loop_fraction_of_total_flow=
            rectangular_resistance(.003,.001,.003,.001)/(
            rectangular_resistance(.08,.001,.001,.001)+rectangular_resistance(.003,.001,.003,.001)),
        required_total_flow_multiplier_to_match_partitioned_loop_flow=
            1+rectangular_resistance(.08,.001,.001,.001)/rectangular_resistance(.003,.001,.003,.001),
        warning='Local entrance flow and exact mouth locations are not supplied; this is an explicit possible countermodel, not target CFD.'),
)
assert abs(result['first_mode_tau_1pct'] - tau) < 1e-12
assert abs(remaining_mass(tau)-0.01) < 1e-14
assert 0 < mass_ratio**12 < 0.01
Path(__file__).with_name('TRANSPORT_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
