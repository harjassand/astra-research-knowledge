#!/usr/bin/env python3
"""Reproducible feasibility checks, NOT a simulation or validation of FeNi axis writing.

Python 3.10+, standard library only. Source values are transcribed from publications;
the 1.5 T magnetic scenarios are explicit assumptions, not a combined specimen.
Run: python analyse.py --output results.json
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Any

MU0 = 4.0 * math.pi * 1e-7  # H/m; engineering approximation
OE_TO_A_PER_M = 1000.0 / (4.0 * math.pi)
MGOE_TO_J_PER_M3 = 1e6 * 1e-4 * OE_TO_A_PER_M


def energy_product_envelope(br_t: float, hcj_a_per_m: float) -> dict[str, float]:
    """Upper envelope for a monotone descending J(H) <= Br in quadrant II.

    With h=-H >= 0, B=J-mu0*h <= Br-mu0*h. Restrict h<=HcJ.
    This is NOT a predicted BHmax. Equality would require an idealized loop.
    """
    if not (math.isfinite(br_t) and math.isfinite(hcj_a_per_m)):
        raise ValueError('Inputs must be finite.')
    if br_t < 0 or hcj_a_per_m < 0:
        raise ValueError('Inputs must be non-negative.')
    h_star = min(hcj_a_per_m, br_t / (2 * MU0))
    return {'br_t': br_t, 'hcj_a_per_m': hcj_a_per_m,
            'envelope_max_j_per_m3': h_star * (br_t - MU0 * h_star),
            'envelope_argmax_a_per_m': h_star,
            'unrestricted_br_ceiling_j_per_m3': br_t**2 / (4 * MU0)}


def run() -> dict[str, Any]:
    # No unmeasured elastic modulus, activation volume, rate, or texture is supplied.
    n42_j_m3 = 334_000.0  # Manufacturer nominal N42; not highest commercial grade.
    n55_j_m3 = 422_000.0  # Actual N55 datasheet value, NOT grade-name arithmetic.
    reported_hlova_mgoe = 6.0
    reported_hlova_hcj = 2.3 * 1000 * OE_TO_A_PER_M
    a_nitride_nm, c_nitride_nm = 0.400, 0.371  # Wang et al. 2022
    a_reference_nm = 0.358  # Goto 2017 SI diffraction calculation assumption
    volume_ratio = a_nitride_nm**2 * c_nitride_nm / a_reference_nm**3
    # Comparing these cells gives a geometric reference estimate, NOT a measured
    # macroscopic shrinkage or a correspondence/activation strain tensor.
    i001_over_i111_s1 = 1.63 / 100.0  # calculated RIETAN powder intensities
    s_example = 0.71  # separately reported powder order parameter
    feni_molar_g = 55.845 + 58.6934
    scenarios = {}
    for name, fraction, remanence_ratio in (
        ('random_axes_dense', 1.0, 0.5),
        ('aligned_dense', 1.0, 1.0),
        ('aligned_80pct_active_volume', 0.8, 1.0),
    ):
        br = 1.5 * fraction * remanence_ratio  # hypothetical Js=1.5 T
        scenarios[name] = energy_product_envelope(br, reported_hlova_hcj)
        scenarios[name].update({'assumed_js_t': 1.5,
                                'assumed_active_volume_fraction': fraction,
                                'assumed_remanence_ratio': remanence_ratio})
    n42_ideal_br = math.sqrt(4 * MU0 * n42_j_m3)
    # To reach N42 with this small HcJ the envelope optimum is truncated at HcJ.
    n42_required_br_at_hc = n42_j_m3 / reported_hlova_hcj + MU0 * reported_hlova_hcj
    out = {
        'status': 'UNVALIDATED_PHYSICAL_HYPOTHESIS',
        'date': '2026-10-15',
        'measured_stress_to_retained_axis_response': None,
        'raw_instrument_data_acquired': False,
        'constants': {'mu0_h_per_m': MU0, 'oe_to_a_per_m': OE_TO_A_PER_M,
                      'mgoe_to_j_per_m3': MGOE_TO_J_PER_M3},
        'reported_benchmark_conversions': {
            'hlova2024_bhmax_kj_per_m3': reported_hlova_mgoe * MGOE_TO_J_PER_M3 / 1000,
            'hlova2024_hcj_ka_per_m': reported_hlova_hcj / 1000,
            'n42_nominal_bhmax_kj_per_m3': n42_j_m3 / 1000,
            'n55_nominal_bhmax_kj_per_m3': n55_j_m3 / 1000,
            'ratio_n55_to_reported_feni': n55_j_m3 / (reported_hlova_mgoe * MGOE_TO_J_PER_M3),
            'ratio_n42_to_reported_feni': n42_j_m3 / (reported_hlova_mgoe * MGOE_TO_J_PER_M3),
            'warning': 'Different sample types; this is not a matched experimental comparison.'},
        'cell_geometry_reference_estimate': {
            'nitride_a_nm': a_nitride_nm, 'nitride_c_nm': c_nitride_nm,
            'metal_reference_a_nm': a_reference_nm,
            'nitride_c_over_a': c_nitride_nm/a_nitride_nm,
            'volume_nitride_over_reference_metal': volume_ratio,
            'contraction_fraction_relative_to_nitride': 1-1/volume_ratio,
            'warning': 'Cross-publication geometric reference; not a measured specimen or transformation-strain tensor.'},
        'diffraction_diagnostic': {
            'calculated_powder_i001_over_i111_at_s1': i001_over_i111_s1,
            'example_s': s_example,
            'expected_powder_i001_over_i111_at_example_s': i001_over_i111_s1*s_example**2,
            'percent_of_fundamental_at_example_s': 100*i001_over_i111_s1*s_example**2,
            'assumed_relative_texture_factor': 2.0,
            'naive_inferred_s_after_factor2_texture': s_example*math.sqrt(2),
            'warning': 'Illustrative intensity calculation; no new diffraction data or actual texture factor measured.'},
        'source_2017_gas_throughflow': {
            'sample_g': 1.0, 'ammonia_l_per_min': 5.0, 'nitridation_h': 50.0,
            'ammonia_throughflow_l_per_g': 5.0 * 60 * 50,
            'warning': 'Delivered laboratory throughflow, NOT net reagent consumption or a production-scale requirement.'},
        'stoichiometric_material_fractions': {
            'nickel_mass_fraction_in_equiatomic_feni': 58.6934 / feni_molar_g,
            'nitrogen_kg_per_kg_feni_at_fenin_stoichiometry': 14.007 / feni_molar_g,
            'warning': 'Inventory cycling, NOT net consumption, embodied energy, or cost.'},
        'hypothetical_magnetic_envelopes': scenarios,
        'n55_envelope_requirements': {
            'ideal_unrestricted_minimum_br_t': math.sqrt(4*MU0*n55_j_m3),
            'minimum_br_at_reported_hlova_hcj_t': n55_j_m3/reported_hlova_hcj+MU0*reported_hlova_hcj,
            'warning': 'Necessary envelope conditions, not sufficient material performance or prediction.'},
        'n42_envelope_requirements': {
            'ideal_unrestricted_minimum_br_t': n42_ideal_br,
            'ideal_operating_h_at_that_br_ka_per_m': n42_ideal_br/(2*MU0)/1000,
            'minimum_br_at_reported_hlova_hcj_t': n42_required_br_at_hc,
            'warning': 'Necessary envelope conditions, not sufficient material performance or prediction.'},
        'excluded_inferences': [
            'Tetragonal c/a does not establish mobile twins or stress-switchable variants.',
            'No three-axis coherent transformation correspondence is assumed.',
            'High order S, high saturation magnetization, and high coercivity are not interchangeable.',
            'No chemical-free-energy, furnace-energy, throughput, cost, or bulk yield claim.',
            'No novel-operation or historical-priority certification.']
    }
    # Algebra and unit checks, not physical validation.
    assert math.isclose(MGOE_TO_J_PER_M3, 7957.7471545947665, rel_tol=1e-12)
    assert 0 < 1-1/volume_ratio < 1
    assert s_example*math.sqrt(2) > 1  # diagnostic: texture can mimic impossible S
    assert energy_product_envelope(0.0, 100.0)['envelope_max_j_per_m3'] == 0
    for v in scenarios.values():
        assert v['envelope_max_j_per_m3'] <= v['unrestricted_br_ceiling_j_per_m3']*(1+1e-12)
    # Directly evaluate the proven envelope on a grid for a family of monotone
    # example curves J(h)=max(0, Br*(1-h/HcJ)^p). These are NOT measured FeNi loops.
    checks = 0
    for br in (0.2, 0.75, 1.2, 1.5):
        for hc in (1e4, 1e5, 5e5):
            e = energy_product_envelope(br, hc)['envelope_max_j_per_m3']
            for p in (0.25, 1.0, 2.0, 4.0):
                for k in range(1001):
                    h = hc*k/1000
                    j = br * max(0.0, 1-h/hc)**p
                    observed_product = max(0.0, (j-MU0*h)*h)
                    assert observed_product <= e + 1e-8
                    checks += 1
    out['numerical_envelope_inequality_checks'] = checks
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results.json'))
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
