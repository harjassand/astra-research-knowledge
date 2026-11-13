#!/usr/bin/env python3
"""Separate introduced rail-geometry and segmented-stiffness models; no hardware."""
import itertools
import json
import math
from pathlib import Path

R = 0.025                 # rail-centroid radius, m
L = 1.0                   # developed centreline length, m
N = 50
PITCH = L / N
Y = (R, -R / 2, -R / 2)
SUM_Y2 = sum(y*y for y in Y)
E = 70e9                  # introduced elastic modulus, not a source material fit
WIDTH = 0.020
THICKNESS = 0.0006
AREA = WIDTH * THICKNESS
EA = E * AREA
TIP_FORCE = 20.0
DEFLECTION_LIMIT = 0.010
EPS = 20e-6

def pose(curvatures):
    x = z = theta = 0.0
    for k in curvatures:
        end = theta + k * PITCH
        if abs(k) < 1e-14:
            x += PITCH * math.cos(theta)
            z += PITCH * math.sin(theta)
        else:
            x += (math.sin(end)-math.sin(theta)) / k
            z += (math.cos(theta)-math.cos(end)) / k
        theta = end
    return (x, z, theta)

def feed_for_curvature(ks):
    return [[PITCH*(1-y*k) for k in ks] for y in Y]

def curvature_for_feed(feed):
    # Least-squares constant-section, no-axial-centreline-strain inverse.
    return [-sum(y*(feed[i][j]-PITCH) for i,y in enumerate(Y))
            / (PITCH*SUM_Y2) for j in range(N)]

def endpoint_difference(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

profiles = {
    "straight": [0.0]*N,
    "quarter_turn": [math.pi/2]*N,
    "opposite_curvature_halves": [2.0]*(N//2)+[-2.0]*(N-N//2),
}
programs = {}
for name, ks in profiles.items():
    feed = feed_for_curvature(ks)
    reconstructed = curvature_for_feed(feed)
    programs[name] = {
        "centreline_endpoint_m_m_rad": pose(ks),
        "rail_feed_lengths_m": [sum(row) for row in feed],
        "max_per_step_offset_from_same_pitch_m":
            max(abs(v-PITCH) for row in feed for v in row),
        "max_same_pitch_relative_length_change":
            max(abs(v/PITCH-1) for row in feed for v in row),
        "max_reconstruction_curvature_error_per_m":
            max(abs(a-b) for a,b in zip(ks,reconstructed)),
        "reconstructed_endpoint_error_m":
            endpoint_difference(pose(ks),pose(reconstructed)),
        "positive_offset_curve_condition": max(abs(y*k) for y in Y for k in ks)<1,
    }

straight = profiles["straight"]
basefeed = feed_for_curvature(straight)
basepose = pose(straight)
# Opposite-sign interior errors conserve each total rail-feed length.
# They are introduced register-rest-length errors, not actual zipper faults.
feed_end_only = [[v + (EPS if j<N//2 else -EPS)*(1 if y>0 else -1)
                  for j,v in enumerate(basefeed[i])]
                 for i,y in enumerate(Y)]
end_only_ks = curvature_for_feed(feed_end_only)
# Absolute material phase is bounded at EVERY writing checkpoint, initial zero.
# Step errors are differences of adjacent phase errors, hence telescope.
phase = [[0.0]+[EPS*(1 if y>0 else -1)]*N for y in Y]
feed_phase = [[v+phase[i][j+1]-phase[i][j] for j,v in enumerate(basefeed[i])]
              for i in range(3)]
phase_ks = curvature_for_feed(feed_phase)
phase_angle_bound = EPS * sum(abs(y) for y in Y) / SUM_Y2
errors = {
    "endpoint_feed_only_zero_sum_register_error": {
        "introduced_each_step_error_bound_m": EPS,
        "total_rail_feed_error_m":
            [sum(row)-L for row in feed_end_only],
        "max_interior_cumulative_phase_error_m":
            max(abs(sum(feed_end_only[i][:j])-PITCH*j)
                for i in range(3) for j in range(N+1)),
        "actual_endpoint_m_m_rad": pose(end_only_ks),
        "endpoint_position_error_m":
            endpoint_difference(basepose,pose(end_only_ks)),
        "max_angle_error_rad":
            max(abs(sum(end_only_ks[:j])*PITCH) for j in range(N+1)),
        "assumption": "Serial register rest-length errors can redistribute length; no claim this is a physically realised tape/clip history.",
    },
    "bounded_absolute_phase_at_every_checkpoint": {
        "introduced_each_checkpoint_phase_bound_m": EPS,
        "initial_phase_is_exact": True,
        "actual_endpoint_m_m_rad": pose(phase_ks),
        "endpoint_position_error_m":
            endpoint_difference(basepose,pose(phase_ks)),
        "all_prefix_angle_error_bound_rad": phase_angle_bound,
        "endpoint_error_integral_bound_m": L*phase_angle_bound,
        "requires": "Actual material phase at every frozen checkpoint, after relevant slip/strain/thermal changes; final spool counts alone do not supply it.",
    },
}
# Independent analytical check over all eight phase-sign corners.
corners = [sum(y*e for y,e in zip(Y,es))/SUM_Y2
           for es in itertools.product((-EPS,EPS),repeat=3)]
errors["phase_bound_corner_check_rad"] = max(abs(v) for v in corners)
errors["phase_bound_absolute_difference_rad"] = abs(
    errors["phase_bound_corner_check_rad"]-phase_angle_bound)

# SEPARATE surrogate: segmented axial rails with serial register springs.
# This is not a constitutive derivation for uninterrupted tapes in external clips.
stiffness = []
for k in (1e6,1e7,1e8,5e8,1e9,math.inf):
    ea_eff = EA if math.isinf(k) else 1/(1/EA+1/(k*PITCH))
    ei = ea_eff*SUM_Y2
    stiffness.append({
        "per_rail_per_station_register_stiffness_N_per_m":
            "rigid ideal" if math.isinf(k) else k,
        "effective_rail_EA_N": ea_eff,
        "effective_bending_EI_N_m2": ei,
        "linear_tip_load_deflection_m": TIP_FORCE*L**3/(3*ei),
        "linear_bending_strain_energy_J": TIP_FORCE**2*L**3/(6*ei),
        "pinned_linear_Euler_load_N": math.pi**2*ei/L**2,
    })
required_ei = TIP_FORCE*L**3/(3*DEFLECTION_LIMIT)
required_ea = required_ei/SUM_Y2
needed_k = 1/(PITCH*(1/required_ea-1/EA)) if required_ea<EA else None
root_rail_forces = [TIP_FORCE*L*y/SUM_Y2 for y in Y]
elastic_tape_storage = {
    "introduced_density_kg_per_m3": 2700,
    "bare_three_rail_mass_kg": 3*L*AREA*2700,
    "coil_radius_m": 0.050,
    "outer_fibre_coil_strain": THICKNESS/(2*0.050),
    "linear_elastic_coil_stress_Pa": E*THICKNESS/(2*0.050),
    "minimum_coil_radius_m_for_introduced_stress_limits":
        {str(s):E*THICKNESS/(2*s) for s in (100e6,200e6,400e6)},
    "qualification": "Homogeneous intact-tape storage surrogate only. It does not qualify the segmented spring model or any common material/interface architecture.",
}
result = {
    "status": "INTRODUCED CONDITIONAL MODEL; NOT A WORKING DEVICE OR NOVELTY CLAIM",
    "geometry": {"R_m":R,"L_m":L,"stations":N,"pitch_m":PITCH,
                 "rail_y_m":Y,"sum_rail_y2_m2":SUM_Y2},
    "operation": "Same generic rails could encode different planar curvatures if a real head writes and retains the required differential registration. That head and adjustable locks are unconstructed.",
    "profiles": programs,
    "errors": errors,
    "load_and_stiffness": {
        "introduced_E_Pa":E,"rail_width_m":WIDTH,"rail_thickness_m":THICKNESS,
        "rail_EA_N":EA,"introduced_tip_load_N":TIP_FORCE,
        "deflection_limit_m":DEFLECTION_LIMIT,
        "required_EI_N_m2":required_ei,
        "required_per_rail_register_stiffness_N_per_m":needed_k,
        "root_rail_axial_force_N":root_rail_forces,
        "one_pitch_rail_force_change_due_to_tip_shear_N":
            [TIP_FORCE*PITCH*y/SUM_Y2 for y in Y],
        "cases":stiffness,
        "scope": "SEPARATE small-deflection segmented axial-rail surrogate with serial register springs, not a constitutive law for uninterrupted tapes held by external clips. Cross-links, shear transfer, torsion, joint opening/buckling, support, path, formation under load and common hardware remain unconstructed.",
    },
    "elastic_tape_storage":elastic_tape_storage,
    "verification": {
        "curvature_reconstruction_error_bound_per_m":
            max(v["max_reconstruction_curvature_error_per_m"] for v in programs.values()),
        "total_feed_zero_sum_error_m":
            max(abs(v) for v in errors["endpoint_feed_only_zero_sum_register_error"]["total_rail_feed_error_m"]),
        "phase_corner_identity_error_rad":errors["phase_bound_absolute_difference_rad"],
    },
    "limits": [
        "Geometry, segmented serial-joint stiffness and homogeneous intact-tape coiling are separate surrogates. Their favourable properties are not combined into an established physical stock/interface.",
        "Fixed equal-pitch one-to-one registration and undeformed rails cannot inherit unequal offset-curve lengths merely by changing motor commands; alternate geometry, sliding, strain or pairing must be constructed.",
        "This is not an impossibility result for all zippers, growing robots, material programmers or autonomous construction.",
        "An exact final rail length does not authenticate its interior registration in this declared model.",
        "Absolute checkpoint material-phase bounds can avoid the independent-step accumulation, but measuring commanded motor position does not by itself certify those bounds.",
        "No load-bearing physical clamp, controlled release, autonomous reacquisition, installation, sensor, stock renewal or full-cost advantage has been built.",
        "Bare rail mass excludes the write head, all locks/cross-links, reels, base, drives, sensing, power, waste, preparation and service.",
    ],
}
out=Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
print(json.dumps({"output":str(out),"verification":result["verification"],
                  "profiles":programs,"errors":errors,"load_and_stiffness":result["load_and_stiffness"],
                  "elastic_tape_storage":elastic_tape_storage},sort_keys=True))
