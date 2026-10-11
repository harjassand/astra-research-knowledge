"""Conditional engineering scales for a polarizability/mass powder certificate.

No device simulation or validation is claimed. All calculations use SI units.
Run from any directory; writes powder_results.json beside this file.
"""

import json
import math
from pathlib import Path

EPS0 = 8.8541878128e-12
QE = 1.602176634e-19
KB = 1.380649e-23
NA = 6.02214076e23
H = 6.62607015e-34
C = 299792458.0


def upper_normal_quantile(tail_probability):
    """Solve Q(z)=tail_probability without rounding 1-p to one."""
    lo, hi = 0.0, 15.0
    for _ in range(100):
        mid = (lo + hi) / 2
        tail = 0.5 * math.erfc(mid / math.sqrt(2))
        if tail > tail_probability:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def normal_cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))


def damped_displacement(acceleration, kick, drift, tau):
    hk = -math.expm1(-kick / tau)
    ht = -math.expm1(-drift / tau)
    return acceleration * tau * (kick - tau * hk) + acceleration * tau**2 * hk * ht


def main():
    radius = 15e-6
    rho = 2700.0  # Assumed homogeneous metallic aluminum matrix density.
    volume = 4 * math.pi * radius**3 / 3
    mass = rho * volume
    alpha = 3 * EPS0 * volume
    field_rms = 1e6
    gradient_rms = 1e9
    field_length = field_rms / gradient_rms
    force = alpha * field_rms * gradient_rms
    acceleration = force / mass
    kick, drift = 1e-3, 10e-3
    displacement = acceleration * kick * (drift + kick / 2)
    feed_kg_h = 1.0
    rate = feed_kg_h / 3600 / mass
    count_hour = rate * 3600
    position_sigma = displacement * 0.002 / math.sqrt(6)
    p = alpha * field_rms
    speed = 10.0

    result = {
        "status": "conditional analytic scale model; not a working-device or feasibility claim",
        "assumptions": {
            "radius_m": radius,
            "matrix_density_kg_m3": rho,
            "field_rms_V_m": field_rms,
            "field_gradient_rms_V_m2": gradient_rms,
            "field_length_m": field_length,
            "kick_s": kick,
            "drift_s": drift,
            "beam_speed_m_s": speed,
            "feed_kg_h": feed_kg_h,
        },
        "sphere": {
            "volume_m3": volume,
            "mass_kg": mass,
            "polarizability_per_axis_SI": alpha,
            "polarizability_trace_SI": 3 * alpha,
            "trace_over_mass_SI": 9 * EPS0 / rho,
            "dipole_C_m": p,
            "force_N": force,
            "acceleration_m_s2": acceleration,
            "displacement_m": displacement,
            "one_percent_void_signal_m": displacement * (1 / 0.99 - 1),
            "relative_0p2_percent_displacement_error_m": displacement * 0.002,
            "three_screen_per_position_sigma_m": position_sigma,
            "particle_rate_s": rate,
            "particle_count_hour": count_hour,
            "particles_simultaneously_in_kick_and_drift": rate * (kick + drift),
            "feed_kg_h_at_1000_particles_s": 1000 * mass * 3600,
        },
    }

    charge = []
    omega = 2 * math.pi * 100e3
    hwall = 0.5e-3
    for electrons in (1, 1e4, 1e5):
        q = electrons * QE
        charge.append({
            "charge_electrons": electrons,
            "force_q_times_field_scale_N": q * field_rms,
            "force_over_DEP_scale": q * field_rms / force,
            "DC_charge_displacement_after_drift_m": q * field_rms / mass * kick * (drift + kick / 2),
            "DC_charge_displacement_inside_kick_m": q * field_rms / mass * kick**2 / 2,
            "100kHz_micromotion_peak_m_for_RMS_field": math.sqrt(2) * q * field_rms / (mass * omega**2),
            "100kHz_charge_ponderomotive_over_DEP_scale": q**2 / (mass * omega**2 * alpha),
            "image_force_at_0p5mm_wall_over_DEP": q**2 / (16 * math.pi * EPS0 * hwall**2) / force,
            "Coulomb_pair_force_at_0p5mm_over_DEP": q**2 / (4 * math.pi * EPS0 * hwall**2) / force,
        })
    result["charge_stress_cases_not_measured_distribution"] = charge

    inertia = 0.4 * mass * radius**2
    anisotropy = []
    for fraction in (0.01, 0.1):
        torque = 0.5 * fraction * alpha * field_rms**2
        anisotropy.append({
            "relative_polarizability_anisotropy": fraction,
            "torque_scale_N_m": torque,
            "angular_acceleration_scale_rad_s2": torque / inertia,
            "one_ms_rotation_from_rest_rad_constant_torque_scale": torque / inertia * kick**2 / 2,
        })
    phi = 0.01
    com_offset = phi * radius / (1 - phi)
    result["rotation_and_centroid"] = {
        "sphere_inertia_kg_m2": inertia,
        "anisotropy_stress_cases": anisotropy,
        "one_percent_void_max_COM_offset_bound_m": com_offset,
        "COM_offset_acceleration_at_1000rad_s_m_s2": com_offset * 1000**2,
        "COM_offset_acceleration_over_DEP_at_1000rad_s": com_offset * 1000**2 / acceleration,
        "three_screen_worst_offset_coefficient_4a_over_D": 4 * radius / displacement,
        "central_spherical_one_percent_cavity_radius_m": radius * phi ** (1 / 3),
    }

    interaction_cases = []
    for exclusion_radius in (0.15e-3, 0.317e-3, 0.5e-3, 1e-3):
        pair_force = 3 * p**2 / (2 * math.pi * EPS0 * exclusion_radius**4)
        clean_probability = 0.95
        number_density = -math.log(clean_probability) / (4 * math.pi * exclusion_radius**3 / 3)
        area = rate / (number_density * speed)
        lane_rate = -math.log(clean_probability) * speed / (2 * exclusion_radius)
        interaction_cases.append({
            "exclusion_radius_m": exclusion_radius,
            "worst_aligned_single_axis_pair_force_over_DEP": pair_force / force,
            "single_dipole_field_perturbation_fraction": 2 * radius**3 / exclusion_radius**3,
            "clean_probability_assumed": clean_probability,
            "Poisson_3d_number_density_limit_m3": number_density,
            "Poisson_3d_beam_area_m2_at_10m_s": area,
            "Poisson_3d_square_beam_side_m_at_10m_s": math.sqrt(area),
            "Poisson_1d_lane_rate_limit_s_at_10m_s": lane_rate,
            "Poisson_1d_lanes_for_feed_rate": math.ceil(rate / lane_rate),
            "deterministic_hard_spacing_lane_rate_s": speed / exclusion_radius,
            "deterministic_hard_spacing_lanes": math.ceil(rate * exclusion_radius / speed),
        })
    result["interaction_and_occupancy"] = {
        "caveat": "Leading uniform-field induced dipole pair energy cancels under ideal equal orthogonal averaging of identical spheres. Single-axis values are conservative stress cases. 150um is only an optimistic conditional residual-interaction scenario, not a justified tolerance.",
        "cases": interaction_cases,
    }

    temperature, nitrogen_molar_mass = 300.0, 28.0134e-3
    molecule_mass = nitrogen_molar_mass / NA
    cbar = math.sqrt(8 * KB * temperature / (math.pi * molecule_mass))
    drag_cases = []
    for pressure in (0.1, 1.0, 10.0):
        gas_density = pressure * molecule_mass / (KB * temperature)
        for accommodation in (1.0, 1.4):
            tau = rho * radius / (accommodation * gas_density * cbar)
            drag_cases.append({
                "pressure_Pa": pressure,
                "accommodation_factor_assumed": accommodation,
                "relaxation_time_s": tau,
                "fractional_signal_reduction": 1 - damped_displacement(acceleration, kick, drift, tau) / displacement,
                "Brownian_10ms_position_sigma_m": math.sqrt(2 * KB * temperature * drift**3 / (3 * mass * tau)),
                "drag_acceleration_for_10m_s_relative_gas_speed_m_s2": 10 / tau,
            })
    std_pressure = 101325.0
    carrier_Q = std_pressure * 1e-3 / 60  # 1 L/min at standard pressure, isothermal rough scale.
    dry_solid_m3_s = feed_kg_h / rho / 3600
    dry_entrained_Q = std_pressure * dry_solid_m3_s  # 50% volume loading: void air ~solid volume.
    result["vacuum"] = {
        "gas": "nitrogen at 300 K; free-molecular linear drag; accommodation factors are assumptions",
        "gas_mean_speed_m_s": cbar,
        "drag_cases": drag_cases,
        "one_standard_L_min_gas_load_Pa_m3_s": carrier_Q,
        "one_standard_L_min_pump_speed_at_0p1Pa_L_s": carrier_Q / 0.1 * 1000,
        "dry_airlock_50_percent_fill_entrained_gas_load_Pa_m3_s": dry_entrained_Q,
        "dry_airlock_entrained_gas_pump_speed_at_0p1Pa_L_s": dry_entrained_Q / 0.1 * 1000,
    }

    observations = 10
    views = 2
    roi_pixels = 15**2
    photons = (radius / 2 / position_sigma)**2
    photon_energy = H * C / 532e-9
    conservative_area = next(x for x in interaction_cases if x["exclusion_radius_m"] == 0.5e-3)["Poisson_3d_beam_area_m2_at_10m_s"]
    result["optical_ideal_scales"] = {
        "photons_per_position_ideal_uniform_bright_disk": photons,
        "assumed_observations_per_view_per_particle": observations,
        "assumed_views": views,
        "detected_photons_s_all_views": photons * observations * views * rate,
        "detected_optical_power_W_at_532nm": photons * observations * views * rate * photon_energy,
        "ROI_pixels_per_observation_assumed": roi_pixels,
        "ROI_data_bytes_s_16bit_all_views": roi_pixels * 2 * observations * views * rate,
        "full_beam_object_pixels_at_2um_sampling_per_frame": conservative_area / (2e-6)**2,
        "full_beam_pixels_s_at_10kframes_s": conservative_area / (2e-6)**2 * 1e4,
        "exposure_s_for_0p1um_axial_blur_at_10m_s": 0.1e-6 / speed,
        "depth_of_field_scale_m_532nm_NA0p1": 532e-9 / 0.1**2,
        "caveat": "Shot-noise precision does not bound COM, speckle, optical shape/rotation, detector, track association, or calibration bias; axial blur may be modeled rather than strictly frozen.",
    }

    contamination_kg_h = 1e-6 * feed_kg_h
    deposition_area = 10e-4  # ten square centimetres
    deposition_thickness_hour = contamination_kg_h / rho / deposition_area
    result["field_tolerance_scales"] = {
        "nominal_voltage_V": field_rms * field_length,
        "gap_tolerance_m_for_0p1percent_force_gain_if_alone": field_length * 0.001 / 3,
        "voltage_fraction_tolerance_for_0p1percent_gain_if_alone": 0.001 / 2,
        "finite_size_sphere_quadratic_scale_a_over_L_squared": (radius / field_length)**2,
        "one_ppm_feed_deposition_over_10cm2_thickness_m_hour": deposition_thickness_hour,
        "corresponding_gap_gain_drift_fraction_hour_scale": 3 * deposition_thickness_hour / field_length,
    }

    hour_failure_probability = 0.01
    tail = hour_failure_probability / count_hour
    z = upper_normal_quantile(tail)
    z95 = upper_normal_quantile(0.05)
    stats = []
    for void_limit in (0.01, 0.02, 0.05):
        margin = 1 / (1 - void_limit) - 1
        sigma = 0.002
        for bias_budget in (0.0, 0.001):
            stats.append({
                "void_fraction_limit": void_limit,
                "bias_upper_bound_fraction_of_R0": bias_budget,
                "response_threshold_excess_fraction": margin,
                "Gaussian_dense_grain_acceptance_at_0p2percent_sigma": normal_cdf((margin - bias_budget - z * sigma) / sigma),
                "max_Gaussian_sigma_for_95percent_dense_acceptance": max(0.0, (margin - bias_budget) / (z + z95)),
            })
    result["certificate_confidence_conditional_Gaussian_model"] = {
        "all_grains_hour_failure_probability_limit": hour_failure_probability,
        "per_grain_upper_bound_failure_probability_by_union_bound": tail,
        "one_sided_sigma_guard": z,
        "guard_fraction_at_0p2percent_sigma": z * 0.002,
        "five_sigma_one_sided_tail": 0.5 * math.erfc(5 / math.sqrt(2)),
        "five_sigma_expected_upper_bound_coverage_failures_hour": count_hour * 0.5 * math.erfc(5 / math.sqrt(2)),
        "root_material_budget_normalized_threshold_assumed": 1.004056,
        "root_material_budget_max_sigma_for_95percent_dense_acceptance": 0.004056 / (z + z95),
        "root_material_budget_equivalent_three_screen_position_sigma_m": displacement * 0.004056 / (z + z95) / math.sqrt(6),
        "root_material_budget_dense_acceptance_at_0p2percent_sigma": normal_cdf((0.004056 - z * 0.002) / 0.002),
        "cases": stats,
        "caveat": "This is a conditional Gaussian noise calculation, not a validated tail bound. A true bounded 0.2% uncertainty is a different specification. Sparse finite experiments cannot establish 1e-13 tail probabilities.",
    }

    lane_rate_500um = -math.log(0.95) * speed / (2 * 0.5e-3)
    sorting = []
    for sort_kick in (1e-3, 0.1e-3, 10e-6):
        desired_shift = 100e-6
        sort_acceleration = desired_shift / (sort_kick * (drift + sort_kick / 2))
        sort_field_multiplier = math.sqrt(sort_acceleration / acceleration)
        clean_lane_rate = -math.log(0.95) / (2 * sort_kick)
        sorting.append({
            "sort_kick_s": sort_kick,
            "sort_active_length_m_at_10m_s": speed * sort_kick,
            "acceleration_for_100um_shift_m_s2": sort_acceleration,
            "field_RMS_V_m_if_G_scales_as_E_squared_same_length": field_rms * sort_field_multiplier,
            "probability_no_other_particle_within_plus_minus_one_kick_at_500um_measurement_lane_rate": math.exp(-2 * lane_rate_500um * sort_kick),
            "Poisson_lane_rate_s_for_95percent_actuator_isolation": clean_lane_rate,
            "Poisson_lanes_for_95percent_actuator_isolation": math.ceil(rate / clean_lane_rate),
        })
    lanes = math.ceil(rate / lane_rate_500um)
    voltage = field_rms * field_length
    ideal_capacitance_per_lane = EPS0 * 1e-3 * (speed * kick) / field_length
    wiring_capacitance = 10e-12
    result["sorting_and_driver"] = {
        "cases": sorting,
        "lane_count_reference_500um_measurement": lanes,
        "ideal_cell_parallel_plate_capacitance_F_per_lane_per_axis": ideal_capacitance_per_lane,
        "assumed_wiring_capacitance_F_per_lane_per_axis": wiring_capacitance,
        "ideal_cells_100kHz_1kVRMS_reactive_VA_per_axis": omega * ideal_capacitance_per_lane * lanes * voltage**2,
        "10pF_per_lane_100kHz_1kVRMS_reactive_VA_per_axis": omega * wiring_capacitance * lanes * voltage**2,
        "unrecovered_CV_squared_f_loss_scale_W_per_axis_10pF": wiring_capacitance * lanes * voltage**2 * 100e3,
        "single_binary_half_CV_squared_energy_J_10pF": 0.5 * wiring_capacitance * voltage**2,
        "single_binary_kick_every_particle_power_W_10pF": 0.5 * wiring_capacitance * voltage**2 * rate,
        "ideal_reflection_radiation_pressure_power_W_for_force": force * C / 2,
        "one_ms_radiation_kick_all_absorbed_temperature_rise_K_cp900": force * C / 2 * kick / (mass * 900),
        "caveat": "Reactive VA is not dissipation. Actual resonant drive, wiring, switching, field shielding and addressability must be designed. Poisson pulse-isolation is a sufficient conservative constraint; rare grouped rejection or metered injection changes it.",
    }
    path = Path(__file__).with_name("powder_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(path)
    print(json.dumps({
        "particle_rate_s": rate,
        "signal_um": displacement * 1e6,
        "position_sigma_nm": position_sigma * 1e9,
        "hour_guard_sigma": z,
        "one_percent_void_dense_acceptance_at_sigma_0p2percent": stats[0]["Gaussian_dense_grain_acceptance_at_0p2percent_sigma"],
        "one_percent_void_sigma_limit_for_95percent_dense_acceptance": stats[0]["max_Gaussian_sigma_for_95percent_dense_acceptance"],
    }, indent=2))


if __name__ == "__main__":
    main()
