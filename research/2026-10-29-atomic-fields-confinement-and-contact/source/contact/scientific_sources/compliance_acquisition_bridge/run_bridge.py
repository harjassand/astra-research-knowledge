"""Run scoped conditional mechanics and published-contact-law screens.

The moment box is a declared calculation input from the peer's certificate,
not acquired component data. Published contact fits are not transferred into
an operator coercivity premise. Output labels preserve these distinctions.
"""
import hashlib
import json
import time
from dataclasses import asdict
from fractions import Fraction as F
from pathlib import Path

from contact_certificate import (
    Parameters, acquisition_envelope, certify, corrected_upper,
    reference_mass_bounds, sqrt_bounds, PI_LO, PI_HI,
)


def main():
    started = time.monotonic()
    p = Parameters()
    ml, mu = reference_mass_bounds()
    measured = (mu, F(0), mu / 100)
    errors = (mu / 50,) * 3
    U = corrected_upper(measured, errors)
    results = {
        "scope": "CONDITIONAL_MODEL_CONSTRUCTION_WITH_UNACQUIRED_INPUTS",
        "physical_data": "NONE; peer moment box is a declared interface example",
        "parameters": {k: str(v) for k, v in asdict(p).items()},
        "declared_moment_box": {
            "Mhat_over_Mref": [1, 0, 0.01],
            "absolute_entry_error_over_Mref": 0.02,
            "contact_contrast_not_open_compliance": True,
        },
        "contact_sweep": [],
        "nuisance_sweep": [],
        "matched_service_residual_screen": [],
    }
    for k in (None, 10**16, 2*10**15, 10**15, 5*10**14, 10**14, 10**13):
        result = certify(U, p, k, tolerance=F(1_000))
        result["declared_limit_MPa_sqrt_m"] = 5
        result["conditional_bound_below_limit"] = result["upper_MPa_sqrt_m"] < 5
        results["contact_sweep"].append(result)
    for b in (F(1, 100), F(2, 100), F(5, 100), F(1, 10), F(1), F(10), F(100)):
        result = certify(corrected_upper(measured, errors, b*mu), p, 10**15)
        result["nuisance_norm_over_Mref"] = float(b)
        results["nuisance_sweep"].append(result)
    # The acquisition residual also enters service risk for the same specimen
    # unless the declared service stress already includes it.
    residual_params = Parameters(service_residual0=F(10_000_000))
    for k,b in ((10**15,F(0)),(2*10**15,F(2,100))):
        result = certify(corrected_upper(measured,errors,b*mu),residual_params,k)
        result["service_residual_center_bound_Pa"] = 10_000_000
        result["nuisance_norm_over_Mref"] = float(b)
        results["matched_service_residual_screen"].append(result)

    # Same-information ordinary comparator: an explicitly supplied measured
    # absolute upper, with an unknown PSD background. No contact k is needed.
    # The large values match the baseline compliance scale; they are inputs,
    # not measured values. The geometric cap dominates their service bound.
    area, length = F(20, 10**6), F(20, 1000)
    I = area*p.H**2/12
    base00 = area*length/p.E
    base11 = base00/3
    scale = p.beta*p.a_scale**3
    absolute_upper = (base00/scale+10*mu, 0, base11/scale+10*mu)
    results["ordinary_absolute_total_compliance"] = certify(
        absolute_upper, p, None, tolerance=F(1000))
    results["ordinary_absolute_total_compliance"]["input_status"] = (
        "DECLARED_ABSOLUTE_UPPER_FOR_SCALE_COMPARISON_NOT_COMPONENT_DATA")

    # No bending information: scalar C00 bounds h(a); worst depth is an endpoint.
    # A large second diagonal makes this converge to the uniform-only result.
    results["ordinary_uniform_contrast_only"] = certify(
        (U[0], 0, 10**12), p, 10**15, tolerance=F(1000))

    Mref_lo = ml*p.a_scale**3
    Mref_hi = mu*p.a_scale**3
    Cref_lo = p.beta*Mref_lo
    Cref_hi = p.beta*Mref_hi
    a_ref_lo, a_ref_hi = sqrt_bounds(PI_HI), sqrt_bounds(PI_LO)
    a_ref_lo = F(1, 10_000)/a_ref_lo[1]
    a_ref_hi = F(1, 10_000)/a_ref_hi[0]
    source_scale = {
        "Mref_m3_interval": [float(Mref_lo), float(Mref_hi)],
        "a_ref_m_interval": [float(a_ref_lo), float(a_ref_hi)],
        "beta_per_Pa": float(p.beta),
        "Cref_m3_per_Pa": float(Cref_hi),
        "Cref_over_base00_ppm": float(Cref_hi/base00*10**6),
        "Cref_uniform_displacement_at_50MPa_m": float(Cref_hi*50_000_000/area),
        "individual_sensor_error_for_entry_error_002Mref": [],
    }
    for h in (5_000_000, 50_000_000):
        # 2*A*s_u/h <= .02*Cref, and 2*(2I/H)*s_theta/h <= .02*Cref.
        source_scale["individual_sensor_error_for_entry_error_002Mref"].append({
            "probe_stress_Pa": h,
            "displacement_error_upper_m": float(F(1, 50)*Cref_lo*h/(2*area)),
            "rotation_error_upper_rad": float(F(1, 50)*Cref_lo*h*p.H/(4*I)),
            "assumes_no_other_error_budget_consumed": True,
        })
    results["mechanical_signal_and_noise_scale"] = source_scale
    results["switching_screen"] = acquisition_envelope(
        p, preload=20_000_000, h0=5_000_000, h1=5_000_000,
        depth_radius=F(4, 5), residual0=10_000_000)
    results["switching_screen"]["all_inputs_hypothetical"] = True

    # A unit dimensionless load coefficient is an illustrative sensitivity,
    # not a literature estimate for titanium: C_bg(P)=C_bg(0)*(1+gamma*P/E).
    results["intrinsic_nonlinear_background_sensitivity"] = []
    for P in (20_000_000, 50_000_000):
        contrast_per_gamma = 2*F(P)/p.E*base00/Cref_hi
        results["intrinsic_nonlinear_background_sensitivity"].append({
            "preload_Pa": P,
            "nuisance_Mref_per_unit_gamma": float(contrast_per_gamma),
            "gamma_upper_for_nuisance_002Mref": float(F(1,50)/contrast_per_gamma),
            "gamma_status": "ILLUSTRATIVE_COEFFICIENT_NOT_MEASURED_OR_ASSUMED",
        })

    # Kim2021 Table2, copied from pinned primary XML. Mean fitted k(P) is
    # not a coercivity bound and its fitting windows exclude some pressures.
    published = [
        ("1", 0.179, 0.930, 2.41e-2),
        ("2", 1.458, 2.601, 4.09e-5),
        ("3", 2.567, 4.987, 3.47e-10),
        ("4", 4.524, 7.486, 5.85e-15),
    ]
    t = 1e-4
    rows = []
    for specimen, roughness, m, c in published:
        factor = 2**m
        extrapolated = 2*t/(1+t)-factor*t/(1+factor*t)
        rows.append({
            "specimen": specimen, "Ra_micrometre": roughness,
            "m": m, "C_MPa_power_1_minus_m_per_nm": c,
            "published_function_at_40MPa_Pa_per_m": c*40**m*1e15,
            "function_evaluation_is_not_new_measurement_or_lower_bound": True,
            "two_amplitude_contrast_over_open_Q_at_t_0001": extrapolated,
            "extrapolation_can_be_negative": extrapolated < 0,
        })
    results["primary_contact_table_and_failed_extrapolation"] = rows
    results["ordinary_method_prior"] = {
        "differential_compliance": "ESTABLISHED; Kovarik2025 DOI10.1007/s10704-025-00881-z, antecedent Golub1995 cited there",
        "baseline_free_VAM": "ESTABLISHED; Donskoy2020 DOI10.1016/j.jsv.2020.115808",
        "operator_parallel_sum": "ESTABLISHED; Anderson-Duffin1969 DOI10.1016/0022-247X(69)90200-5",
        "new_combination_novelty": "UNKNOWN",
        "same_information_method_advantage": "NOT_ESTABLISHED",
    }
    results["resource_receipt"] = {
        "wall_seconds": time.monotonic()-started,
        "external_solver": "NONE",
        "numeric_certificate_arithmetic": "STDLIB_EXACT_RATIONAL_WITH_INTEGER_SQRT_ENCLOSURES",
        "physical_load_settings_per_two_mode_contrast": 8,
        "sensor_coordinates_per_setting": 2,
        "physical_experiments": 0,
        "paid_compute": 0,
    }
    results["code_sha256"] = hashlib.sha256(Path('contact_certificate.py').read_bytes()).hexdigest()
    Path('bridge_results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps({
        "contact_sweep": [(x['contact_lower_Pa_per_m'], x['upper_MPa_sqrt_m'])
                          for x in results['contact_sweep']],
        "nuisance_sweep": [(x['nuisance_norm_over_Mref'],x['upper_MPa_sqrt_m'])
                           for x in results['nuisance_sweep']],
        "absolute_total_K": results['ordinary_absolute_total_compliance']['upper_MPa_sqrt_m'],
        "uniform_only_K": results['ordinary_uniform_contrast_only']['upper_MPa_sqrt_m'],
        "wall_seconds": results['resource_receipt']['wall_seconds'],
    },indent=2))

if __name__ == '__main__':
    main()
