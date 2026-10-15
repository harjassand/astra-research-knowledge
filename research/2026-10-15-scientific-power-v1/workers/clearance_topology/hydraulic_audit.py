#!/usr/bin/env python3
"""Dimensionless duct, gate-schedule, diffusion, and leakage calculations.

Newtonian, rigid no-slip fully developed ducts. Not laboratory measurements.
All one-pore-volume clocks are transport quantities, not clearance endpoints.
"""
import json
import math
from pathlib import Path


def resistance(mu, length, width, height, terms=1000):
    """Exact rectangular Poiseuille series, with explicitly bounded tail.

    The omitted positive series tail has magnitude <=1/(4*(2N-1)^4),
    using the larger sum over every integer beyond the last retained odd.
    """
    w, h = max(width, height), min(width, height)
    assert mu > 0 and length > 0 and h > 0
    series = sum(math.tanh(n * math.pi * w / (2 * h)) / n**5
                 for n in range(1, 2 * terms, 2))
    correction = 1 - 192 * h * series / (math.pi**5 * w)
    return 12 * mu * length / (w * h**3 * correction)


def diffusion_mass(theta, terms=10000):
    """Mean mass fraction: c(0,t)=0; c_x(L,t)=0; uniform initial c=1.

    theta = D*t/L^2. The theta=0 initial mass is supplied exactly.
    """
    if theta == 0:
        return 1.0
    return sum(8 / (math.pi**2 * n**2) * math.exp(-n**2 * math.pi**2 * theta / 4)
               for n in range(1, 2 * terms, 2))


def diffusion_time(residual):
    lo, hi = 0.0, 1.0
    while diffusion_mass(hi) > residual:
        hi *= 2
    for _ in range(90):
        mid = (lo + hi) / 2
        if diffusion_mass(mid) > residual:
            lo = mid
        else:
            hi = mid
    return hi


def width_split(aspect, delta_fraction):
    w, h, delta = aspect, 1.0, delta_fraction * aspect
    original = resistance(1, 1, w, h)
    lane = resistance(1, 1, (w - delta) / 2, h)
    return {"width_over_height": aspect, "septum_width_fraction": delta_fraction,
            "R_full": original, "R_lane": lane,
            "two_serial_lanes_over_R_full": 2 * lane / original,
            "lane_area": (w - delta) * h / 2,
            "retained_liquid_area_fraction": 1 - delta_fraction}


def wheatstone(delta_fraction):
    shape = width_split(1.0, delta_fraction)
    lam = shape["R_lane"] / shape["R_full"]
    # Three unsplit edges; two split edges with two serial lanes each.
    re = 3 + 4 * lam
    ve = 5 - 2 * delta_fraction
    # Gates AB and CD closed: open path A-C-B-D, then open all edges.
    # Flush until the clean front exits BC: two edge volumes at q=1/3,
    # giving 6*tau. Open all: outer branches each have two edge volumes
    # at q=1/2; 4*tau clears even the recontaminated BD edge. BC is clean
    # and stagnant in the final balanced network. Total 10*tau, 6*V0 feed.
    return {"septum_width_fraction": delta_fraction,
            "R_E_over_R0": re, "V_E_over_V0": ve,
            "one_PV_E_in_tau": re * ve,
            "explicit_two_stage_gate_plug_clearance_in_tau": 10,
            "gate_stage_times_in_tau": [6, 4],
            "gate_feed_volume_over_V0": 6,
            "Euler_feed_volume_over_V0": ve,
            "E_transport_clock_over_gate": re * ve / 10,
            "normalization": "tau=R0*V0/DeltaP; ideal 1D plug displacement only",
            "excluded": "gate erase time, junction losses, dissolution, residual tails, leakage"}


def blind_branch(delta_fraction):
    shape = width_split(1.0, delta_fraction)
    lam = shape["R_lane"] / shape["R_full"]
    return {"septum_width_fraction": delta_fraction,
            "branch_loop_R_over_R0": 2 * lam,
            "backbone_plus_loop_R_over_R0": 2 + 2 * lam,
            "whole_temporary_V_over_V0": 3 - delta_fraction,
            "whole_path_one_PV_in_tau": (2 + 2 * lam) * (3 - delta_fraction),
            "loop_only_one_PV_in_tau": 2 * lam * (1 - delta_fraction)}


def illustrative_scales():
    # a, length, mu, and DeltaP are user-visible assumptions, not acquired data.
    a, length, mu, pressure = 1e-3, 1e-2, 1e-3, 10.0
    r0 = resistance(mu, length, a, a)
    v0 = a * a * length
    tau = r0 * v0 / pressure
    b = blind_branch(0.05)
    rtotal = b["backbone_plus_loop_R_over_R0"] * r0
    q = pressure / rtotal
    lane_area = 0.475 * a * a
    u = q / lane_area
    dh = 2 * (0.475 * a) * a / (1.475 * a)
    return {"assumptions_only": {"square_side_m": a, "edge_length_m": length,
                                 "mu_Pa_s": mu, "DeltaP_Pa": pressure,
                                 "septum_width_fraction": 0.05, "density_kg_m3": 1000},
            "R0_Pa_s_per_m3": r0, "V0_m3": v0, "tau_s": tau,
            "blind_whole_path_one_PV_s": b["whole_path_one_PV_in_tau"] * tau,
            "blind_Q_m3_s": q, "blind_lane_mean_velocity_m_s": u,
            "blind_lane_Re": 1000 * u * dh / mu,
            "D_examples_m2_s": {str(d): {"blind_diffusion_1_percent_time_s": diffusion_time(0.01) * length**2 / d,
                                          "Pe_L_using_whole_path_Q": u * length / d}
                                   for d in [1e-9, 1e-10, 1e-11]},
            "caution": "No F127 viscosity, diffusivity, seal strength, or actual clearance measured."}


def main():
    r_square = resistance(1, 1, 1, 1)
    r_circle_equal_area = 8 * math.pi
    tail_bound = 192 / math.pi**5 / (4 * (2 * 1000 - 1)**4)
    result = {
        "scope": "internal analytic-model calculations; transport clocks are not clearance measurements",
        "rectangular_series": {"terms": 1000,
                               "max_correction_factor_tail_bound_for_aspect_ge_1": tail_bound,
                               "square_R_times_a4_over_muL": r_square,
                               "equal_area_circle": r_circle_equal_area},
        "width_split_shapes": [width_split(aspect, delta) for aspect in [1, 2, 10, 1000]
                               for delta in [0, 0.05, 0.1]],
        "wheatstone": [wheatstone(d) for d in [0, 0.05, 0.1]],
        "blind_branch": [blind_branch(d) for d in [0, 0.05, 0.1]],
        "blind_diffusion_dimensionless_times": {str(e): diffusion_time(e) for e in [0.1, 0.01, 0.001]},
        "circular_Poiseuille_pure_advection_residual": {
            str(theta): (1 - theta if theta <= 0.5 else 1 / (4 * theta))
            for theta in [0, 0.25, 0.5, 1, 5, 25, 250]},
        "distributed_leakage_distal_flux_ratio": {
            str(x): (1.0 if x == 0 else x / math.sinh(x))
            for x in [0, 0.1, 1, 2, 5, 10]},
        "illustrative_physical_scales": illustrative_scales(),
        "current_attached_lobe_fixture_assumptions": {
            "loop_length_m": 0.08,
            "square_side_m": 0.001,
            "mu_Pa_s_assumed": 0.001,
            "loop_R_Pa_s_per_m3": resistance(0.001, 0.08, 0.001, 0.001),
            "loop_volume_m3": 0.08 * 0.001**2,
            "loop_only_one_PV_s_at_10Pa_allocated_drop": resistance(0.001, 0.08, 0.001, 0.001) * (0.08 * 0.001**2) / 10,
            "root_chamber_m": [0.003, 0.003, 0.001],
            "diagonal_wall_thickness_m": 0.0005,
            "diagonal_wall_volume_m3_idealized": math.sqrt(2) * 0.003 * 0.001 * 0.0005,
            "caution": "Assumed Newtonian viscosity; excludes mainline/root losses, dissolution and actual final residue."},
    }
    Path("hydraulic_certificate.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"square_coefficient": r_square,
                      "wheatstone": result["wheatstone"],
                      "blind_branch": result["blind_branch"],
                      "diffusion_t_D_over_L2": result["blind_diffusion_dimensionless_times"],
                      "output": "hydraulic_certificate.json"}, indent=2))


if __name__ == "__main__":
    main()
