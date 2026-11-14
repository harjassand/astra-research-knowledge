#!/usr/bin/env python3
"""Introduced two-frequency capture/activation diagnostics, one isolated solid sphere.

The source potential/scattering framework is established theory, not our invention.
All numerical points, fields, observations and activation clocks are INTRODUCED.
No acoustic propagation, cavitation, fusion, growing aggregate, housing or material
qualification is simulated. Standard library, serial work, no external data.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

P = {
    "sphere_radius_m": 1e-5,
    "fluid_density_kg_m3": 1000.0,
    "sphere_density_kg_m3": 1200.0,
    "fluid_sound_speed_m_s": 1500.0,
    "fluid_dynamic_viscosity_Pa_s": 0.001,
    "compressibility_ratio_particle_to_fluid": 0.7,
    "temperature_K": 298.15,
    "g_m_s2": 9.80665,
    "trap_frequency_Hz": 2e6,
    "activation_frequency_Hz": 0.5e6,
    "trap_peak_pressure_Pa": 0.3e6,
    "activation_peak_pressures_Pa": [1e6, 1.5e6],
    "introduced_initial_offset_m": 120e-6,
    "introduced_address_tolerance_m": 20e-6,
    "introduced_pre_capture_s": 0.4,
    "introduced_activation_on_time_s": 1.0,
    "introduced_pulse_period_s": 0.02,
    "introduced_pulse_duty": 0.2,
    "introduced_stream_speeds_m_s": [20e-6, 500e-6],
}


def mode(frequency: float, pressure: float) -> dict:
    a = P["sphere_radius_m"]
    rho = P["fluid_density_kg_m3"]
    c = P["fluid_sound_speed_m_s"]
    nu = P["fluid_dynamic_viscosity_Pa_s"] / rho
    omega = 2 * math.pi * frequency
    k = omega / c
    delta = math.sqrt(2 * nu / omega)
    d = delta / a
    gamma = -1.5 * (1 + 1j * (1 + d)) * d
    rr = P["sphere_density_kg_m3"] / rho
    f1 = 1 - P["compressibility_ratio_particle_to_fluid"]
    f2 = 2 * (1 - gamma) * (rr - 1) / (2 * rr + 1 - 3 * gamma)
    phi = f1 / 3 + f2.real / 2  # derived from read potential, not unread Eq50
    energy_density = pressure**2 / (4 * rho * c**2)
    amplitude = 4 * math.pi * a**3 * phi * k * energy_density
    return {
        "frequency_Hz": frequency, "peak_pressure_Pa": pressure,
        "k_per_m": k, "wavelength_m": 2 * math.pi / k, "ka": k * a,
        "viscous_layer_m": delta, "delta_over_a": d,
        "f1": f1, "f2_real": f2.real, "f2_imag": f2.imag,
        "derived_contrast_phi": phi, "energy_density_J_m3": energy_density,
        "force_amplitude_N": amplitude,
        "local_stiffness_magnitude_N_m": 2 * k * amplitude,
    }


TRAP = mode(P["trap_frequency_Hz"], P["trap_peak_pressure_Pa"])
ZETA = 6 * math.pi * P["fluid_dynamic_viscosity_Pa_s"] * P["sphere_radius_m"]
VOLUME = 4 * math.pi * P["sphere_radius_m"]**3 / 3
BUOYANT_WEIGHT = (
    P["sphere_density_kg_m3"] - P["fluid_density_kg_m3"]
) * VOLUME * P["g_m_s2"]


def force(x: float, activation: dict, on: bool, stream: float) -> float:
    ft = -TRAP["force_amplitude_N"] * math.sin(2 * TRAP["k_per_m"] * x)
    fc = activation["force_amplitude_N"] * math.sin(
        2 * activation["k_per_m"] * x) if on else 0.0
    return ft + fc + BUOYANT_WEIGHT + ZETA * stream


def potential(x: float, activation: dict, on: bool, stream: float) -> float:
    # A tilted 1D potential for the specified CONSTANT stream, not a general
    # fluid work functional or a wall-plug energy calculation.
    ut = TRAP["force_amplitude_N"] / (2 * TRAP["k_per_m"]) * (
        1 - math.cos(2 * TRAP["k_per_m"] * x))
    uc = -activation["force_amplitude_N"] / (2 * activation["k_per_m"]) * (
        1 - math.cos(2 * activation["k_per_m"] * x)) if on else 0.0
    return ut + uc - (BUOYANT_WEIGHT + ZETA * stream) * x


def dforce(x: float, activation: dict, on: bool) -> float:
    return -2 * TRAP["k_per_m"] * TRAP["force_amplitude_N"] * math.cos(
        2 * TRAP["k_per_m"] * x) + (
            2 * activation["k_per_m"] * activation["force_amplitude_N"] *
            math.cos(2 * activation["k_per_m"] * x) if on else 0.0)


def roots_in_one_trap_cell(activation: dict, on: bool, stream: float) -> list:
    bound = TRAP["wavelength_m"] / 4
    intervals = 4000
    candidates = []
    left = -bound
    fl = force(left, activation, on, stream)
    for index in range(1, intervals + 1):
        right = -bound + 2 * bound * index / intervals
        fr = force(right, activation, on, stream)
        if fl * fr < 0:
            lo, hi, flo = left, right, fl
            for _ in range(65):
                mid = (lo + hi) / 2
                fm = force(mid, activation, on, stream)
                if flo * fm <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            x = (lo + hi) / 2
            if not candidates or abs(x - candidates[-1]["x_m"]) > 1e-12:
                slope = dforce(x, activation, on)
                candidates.append({
                    "x_m": x, "force_residual_N": force(x, activation, on, stream),
                    "slope_N_m": slope, "stable_in_1d": slope < 0,
                    "tilted_potential_J": potential(x, activation, on, stream),
                })
        left, fl = right, fr
    return candidates  # finite bracketing, not a global root completeness theorem


def rk4(x: float, dt: float, activation: dict, on: bool, stream: float) -> float:
    def v(xx):
        return force(xx, activation, on, stream) / ZETA
    k1 = v(x)
    k2 = v(x + dt * k1 / 2)
    k3 = v(x + dt * k2 / 2)
    k4 = v(x + dt * k3)
    return x + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def schedule(kind: str, pressure: float, pre: float, stream: float,
             max_step: float) -> dict:
    activation = mode(P["activation_frequency_Hz"], pressure)
    segments = []
    if pre:
        segments.append((pre, False))
    if kind == "continuous":
        segments.append((P["introduced_activation_on_time_s"], True))
    else:
        period = P["introduced_pulse_period_s"]
        duty = P["introduced_pulse_duty"]
        count = round(P["introduced_activation_on_time_s"] / (period * duty))
        for _ in range(count):
            segments.extend([(period * duty, True), (period * (1 - duty), False)])
    x = P["introduced_initial_offset_m"]
    t = 0.0
    x_at_activation_start = None
    peak_during_activation_m = 0.0
    active_clock = 0.0
    escaped_first_cell = None
    max_abs_m = abs(x)
    sample = []
    for duration, on in segments:
        in_activation_stage = t >= pre - 1e-12
        if in_activation_stage and x_at_activation_start is None:
            x_at_activation_start = x
        count = max(1, math.ceil(duration / max_step))
        dt = duration / count
        for _ in range(count):
            x = rk4(x, dt, activation, on, stream)
            t += dt
            if on:
                active_clock += dt
            if in_activation_stage:
                peak_during_activation_m = max(peak_during_activation_m, abs(x))
            max_abs_m = max(max_abs_m, abs(x))
            if escaped_first_cell is None and abs(x) > TRAP["wavelength_m"] / 4:
                escaped_first_cell = t
        if len(sample) < 5 or abs(t - round(t)) < 1e-8:
            sample.append({"t_s": t, "x_m": x, "activation_on": on})
    return {
        "kind": kind, "activation_pressure_Pa": pressure,
        "pre_capture_s": pre, "stream_m_s": stream, "max_step_s": max_step,
        "elapsed_s": t, "on_time_surrogate_s": active_clock,
        "x_at_activation_start_m": x_at_activation_start,
        "final_x_m": x, "maximum_abs_offset_m": max_abs_m,
        "maximum_abs_offset_during_activation_stage_m": peak_during_activation_m,
        "inside_introduced_address_tolerance_throughout_activation":
            peak_during_activation_m <= P["introduced_address_tolerance_m"],
        "first_exit_from_initial_trap_cell_s": escaped_first_cell,
        "field_exposure_density_time_J_s_m3":
            TRAP["energy_density_J_m3"] * t +
            activation["energy_density_J_m3"] * active_clock,
        "field_exposure_unit_warning":
            "J*s/m^3 is NOT joules, electrical energy or heat dissipated.",
        "sample": sample,
        "limits": "An on-time clock is NOT a cured bond or accepted component.",
    }


def main():
    activations = [mode(P["activation_frequency_Hz"], x)
                   for x in P["activation_peak_pressures_Pa"]]
    local = []
    for a in activations:
        kt = TRAP["local_stiffness_magnitude_N_m"]
        kc = a["local_stiffness_magnitude_N_m"]
        duty = P["introduced_pulse_duty"]
        period = P["introduced_pulse_period_s"]
        avg_k = kt - duty * kc
        multiplier = math.exp(-avg_k * period / ZETA)
        local.append({
            "activation_pressure_Pa": a["peak_pressure_Pa"],
            "trap_k_N_m": kt, "activation_destabilizing_k_N_m": kc,
            "continuous_combined_k_N_m": kt - kc,
            "continuous_local_decay_rate_per_s": (kt - kc) / ZETA,
            "duty_0p2_linear_average_k_N_m": avg_k,
            "linear_homogeneous_period_multiplier": multiplier,
            "critical_duty_for_local_linear_stability": kt / kc,
            "scope": "Exact multiplier for homogeneous linear switched equation only; not nonlinear capture or cavitating chemistry.",
        })
    runs = []
    for kind, pressure, pre, stream in [
        ("continuous", 1e6, 0.0, 20e-6),
        ("continuous", 1e6, 0.4, 20e-6),
        ("continuous", 1.5e6, 0.4, 20e-6),
        ("pulsed", 1.5e6, 0.4, 20e-6),
        ("pulsed", 1.5e6, 0.4, 500e-6),
    ]:
        versions = [schedule(kind, pressure, pre, stream, dt)
                    for dt in [2e-4, 1e-4, 5e-5]]
        runs.append({
            "finest": versions[-1],
            "final_offset_changes_m": [
                abs(versions[0]["final_x_m"] - versions[1]["final_x_m"]),
                abs(versions[1]["final_x_m"] - versions[2]["final_x_m"]),
            ],
            "peak_offset_changes_m": [
                abs(versions[0]["maximum_abs_offset_during_activation_stage_m"] -
                    versions[1]["maximum_abs_offset_during_activation_stage_m"]),
                abs(versions[1]["maximum_abs_offset_during_activation_stage_m"] -
                    versions[2]["maximum_abs_offset_during_activation_stage_m"]),
            ],
            "scope": "Step refinement diagnostics, not a rigorous continuous-path error bound.",
        })

    root_cases = []
    for a in activations:
        rr = roots_in_one_trap_cell(a, True, 20e-6)
        root_cases.append({"activation_pressure_Pa": a["peak_pressure_Pa"],
                           "roots_in_initial_cell": rr})
    # Meaningful independent sign/gradient check of the implemented potential.
    residuals = []
    for a in activations:
        for x in [-130e-6, -20e-6, 0.0, 20e-6, 130e-6]:
            dx = 1e-9
            minus_grad = -(potential(x + dx, a, True, 20e-6) -
                           potential(x - dx, a, True, 20e-6)) / (2 * dx)
            residuals.append(abs(force(x, a, True, 20e-6) - minus_grad))
    assert max(residuals) < 2e-17
    equilibrium_residual = max(
        [abs(q["force_residual_N"]) for rc in root_cases
         for q in rc["roots_in_initial_cell"]] or [0.0])
    assert equilibrium_residual < 1e-20
    particle_relaxation_s = (
        2 * P["sphere_density_kg_m3"] * P["sphere_radius_m"]**2 /
        (9 * P["fluid_dynamic_viscosity_Pa_s"]))
    # Even granting perfect eventual binding, serial delivery has finite volume.
    cycles_s = [0.1, 1.0, 5.4]
    output = {
        "status": "INTRODUCED_ONE_DIMENSIONAL_CAPTURE_NOT_A_MANUFACTURING_INVENTION",
        "inputs": P, "trap": TRAP, "activation_modes": activations,
        "drag_N_s_per_m": ZETA, "introduced_buoyant_weight_N": BUOYANT_WEIGHT,
        "particle_inertial_relaxation_scale_s_without_added_mass": particle_relaxation_s,
        "local_stability": local, "finite_root_diagnostics": root_cases,
        "switching_paths": runs,
        "perfect_binding_serial_volume_upper_cases": [
            {"complete_seconds_per_particle": t,
             "sphere_volume_mm3": VOLUME * 1e9,
             "particles_per_mm3": 1.0 / (VOLUME * 1e9),
             "maximum_mm3_per_hour_at_one_site": VOLUME * 1e9 * 3600 / t}
            for t in cycles_s],
        "verification": {
            "potential_force_max_absolute_error_N": max(residuals),
            "finite_equilibrium_force_max_absolute_residual_N": equilibrium_residual,
            "step_refinements_per_case": 3, "cases": len(runs),
        },
        "unconstructed_operations": [
            "Three-dimensional restoring fields and transmission through a real opaque housing.",
            "Actual material density/compressibility/viscosity/temperature and installed pressure maps.",
            "Cavitation, streaming, heating and nonlinear sound during a real locking reaction.",
            "Incoming sphere access, selective identity/position sensing and final physical contact.",
            "A retained permanent or reversible bond, chemistry, shape function and residual feed removal.",
            "Aggregate scattering, hydrodynamic wall corrections, neighbour forces and finite stock renewal.",
            "Independent parallel sites, source/electrical power, life, manufacture and whole-service advantage.",
        ],
        "source_scope": {
            "exact_primary": "https://bruus-lab.dk/TMF/publications/pub2011/Settnes_rad_force_visc_PRE_85_016327_2012.pdf",
            "actual_read": "selected main370--868/pp3--6: standing potential Eq20, monopole Eq26, viscous dipole Eq39",
            "new_hold": "first governing followup868 returned400Timeout; no retry or alternate",
            "not_imported": "unread final standing-wave Eq50, later examples, appendices, cited originals",
            "derivation":
                "Own 1D specialization of actually read Eq20 using specified sinusoidal p and v; two different frequencies remove time-averaged cross terms in the assumed linear field.",
        },
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "output": str(out), "bytes": out.stat().st_size,
        "sha": hashlib.sha256(out.read_bytes()).hexdigest(),
        "local": local,
        "paths": [{k: r["finest"][k] for k in [
            "kind", "activation_pressure_Pa", "pre_capture_s", "stream_m_s",
            "final_x_m", "maximum_abs_offset_during_activation_stage_m",
            "inside_introduced_address_tolerance_throughout_activation",
            "first_exit_from_initial_trap_cell_s"]} for r in runs],
        "serial": output["perfect_binding_serial_volume_upper_cases"],
        "verification": output["verification"],
    }, indent=2))


if __name__ == "__main__":
    main()

