"""ROOT-owned conditional release model; no acquired hardware or vendor curve.

A captured initially loaded spring drives one relative coordinate x.  All
parameters are introduced except the separately recorded maker-page scope.
A one-time take-up distance is followed by an ideal viscous element, optionally
force limited.  Neither law is a measured ACE HB-28 law.  No 6D/frame/guide,
installed sensing, real seal/cavitation/temperature or life certificate follows.
"""
import json
import math
from pathlib import Path

FORCE_N = 2500.0
STIFFNESS_N_M = 5_000_000.0
MASS_KG = 100.0
OMEGA = math.sqrt(STIFFNESS_N_M / MASS_KG)
EQUILIBRIUM_M = FORCE_N / STIFFNESS_N_M
CRITICAL_C_NS_M = 2.0 * math.sqrt(STIFFNESS_N_M * MASS_KG)
INITIAL_ENERGY_J = FORCE_N ** 2 / (2.0 * STIFFNESS_N_M)
FORCE_CAP_N = 3000.0


def engagement(distance):
    """Exact undamped first arrival; None if free peak never reaches take-up."""
    a = EQUILIBRIUM_M
    if distance > 2.0 * a:
        return None
    phase = math.acos(max(-1.0, min(1.0, 1.0 - distance / a)))
    velocity = a * OMEGA * math.sin(phase)
    return phase / OMEGA, velocity


def critical_exact(distance):
    arrival = engagement(distance)
    a, w, c = EQUILIBRIUM_M, OMEGA, CRITICAL_C_NS_M
    if arrival is None:
        return {
            "engages": False,
            "peak_displacement_m": 2.0 * a,
            "peak_time_s": math.pi / w,
            "peak_damper_force_N": 0.0,
            "asymptotic_heat_J": 0.0,
        }
    td, vd = arrival
    A = distance - a
    B = vd + w * A
    tol = 1e-13
    if B > tol:
        tau = vd / (w * B)
        peak = a + (A + B * tau) * math.exp(-w * tau)
        peak_time = td + tau
    else:
        peak = a
        peak_time = None  # supremum reached only asymptotically
    candidates = [(0.0, vd)]
    if abs(B) > tol:
        tv = (vd + B) / (w * B)
        if tv > 0.0:
            candidates.append((tv, (vd - w * B * tv) * math.exp(-w * tv)))
    peak_velocity = max(abs(v) for _, v in candidates)
    at_engagement = 0.5 * MASS_KG * vd ** 2 + 0.5 * STIFFNESS_N_M * (distance - a) ** 2
    return {
        "engages": True,
        "engagement_time_s": td,
        "engagement_velocity_m_s": vd,
        "engagement_energy_J": at_engagement,
        "peak_displacement_m": peak,
        "peak_time_s": peak_time,
        "peak_damper_force_N": c * peak_velocity,
        "first_damper_force_N": c * vd,
        "asymptotic_heat_J": INITIAL_ENERGY_J,
        "monotone_to_equilibrium": B <= tol,
    }


def after_engagement_numerical(distance, dt, capped):
    """RK4 finite diagnostic, with the one-time take-up event solved exactly."""
    event = engagement(distance)
    if event is None:
        return {"engages": False, "peak_displacement_m": 2.0 * EQUILIBRIUM_M}
    td, velocity = event
    state = [distance, velocity, 0.0]
    peak_x = distance
    peak_force = 0.0
    max_energy_defect = 0.0

    def damper(v):
        f = CRITICAL_C_NS_M * v
        return max(-FORCE_CAP_N, min(FORCE_CAP_N, f)) if capped else f

    def rhs(s):
        x, v, _ = s
        f = damper(v)
        return [v, (FORCE_N - STIFFNESS_N_M * x - f) / MASS_KG, f * v]

    steps = math.ceil(0.2 / dt)
    actual_dt = 0.2 / steps
    for _ in range(steps):
        k1 = rhs(state)
        k2 = rhs([s + actual_dt * z / 2.0 for s, z in zip(state, k1)])
        k3 = rhs([s + actual_dt * z / 2.0 for s, z in zip(state, k2)])
        k4 = rhs([s + actual_dt * z for s, z in zip(state, k3)])
        state = [s + actual_dt * (a + 2*b + 2*c + d) / 6.0
                 for s, a, b, c, d in zip(state, k1, k2, k3, k4)]
        x, v, heat = state
        peak_x = max(peak_x, x)
        peak_force = max(peak_force, abs(damper(v)))
        energy = 0.5 * MASS_KG * v*v + 0.5 * STIFFNESS_N_M * (x - EQUILIBRIUM_M)**2
        max_energy_defect = max(max_energy_defect, abs(energy + heat - INITIAL_ENERGY_J))
    return {
        "engages": True,
        "dt_s": actual_dt,
        "steps": steps,
        "end_time_after_engagement_s": 0.2,
        "peak_displacement_m_sampled": peak_x,
        "peak_damper_force_N_sampled": max(peak_force, abs(damper(velocity))),
        "end_displacement_m": state[0],
        "end_velocity_m_s": state[1],
        "heat_J": state[2],
        "max_energy_defect_J": max_energy_defect,
        "scope": "finite sampled ODE diagnostic, not an interval or physical certificate",
    }


def run():
    distances = [0.0, 25e-6, 50e-6, 100e-6,
                 EQUILIBRIUM_M * (1.0 - 1.0 / math.sqrt(2.0)),
                 200e-6, 500e-6, 1e-3, 10e-3]
    rows = []
    for d in distances:
        exact = critical_exact(d)
        numerical = after_engagement_numerical(d, 2e-5, False)
        capped = after_engagement_numerical(d, 2e-5, True)
        capped_refined = after_engagement_numerical(d, 1e-5, True)
        if exact["engages"]:
            assert abs(exact["engagement_energy_J"] - INITIAL_ENERGY_J) < 1e-10
            assert abs(numerical["peak_displacement_m_sampled"] - exact["peak_displacement_m"]) < 2e-8
            assert numerical["max_energy_defect_J"] < 2e-8
        rows.append({"takeup_m": d, "ideal_linear_critical": exact,
                     "numerical_linear": numerical, "numerical_force_limited": capped,
                     "numerical_force_limited_refined": capped_refined})
    return {
        "status": "INTRODUCED_ONE_COORDINATE_MODEL_NOT_HARDWARE",
        "parameters": {"force_N": FORCE_N, "stiffness_N_m": STIFFNESS_N_M,
                       "mass_kg": MASS_KG, "omega_rad_s": OMEGA,
                       "critical_damping_Ns_m": CRITICAL_C_NS_M,
                       "equilibrium_m": EQUILIBRIUM_M,
                       "stored_spring_energy_J": INITIAL_ENERGY_J,
                       "introduced_force_limit_N": FORCE_CAP_N},
        "monotone_critical_takeup_threshold_m": EQUILIBRIUM_M * (1.0 - 1.0 / math.sqrt(2.0)),
        "force_limited_first_engagement_takeup_small_root_m":
            EQUILIBRIUM_M - math.sqrt(EQUILIBRIUM_M**2 - (FORCE_CAP_N / (CRITICAL_C_NS_M * OMEGA))**2),
        "maker_read_scope": {
            "url": "https://www.acecontrols.com/us/products/motion-control/hydraulic-dampers/hb-12-to-hb-70/hb-28.html",
            "scope": "main family description/table/Technical Data/Technical Notes, not linked catalogue or measured small-stroke curve",
            "nominal_min_stroke_inch": 1.97,
            "reported_free_fraction_approx": 0.20,
            "min_stroke_rounded_m": 0.050,
            "conditional_free_travel_m_if_full_reported_fraction_is_unengaged": 0.010,
            "separator_bias_N_reported": 80.0,
            "note": "The 3000 N numerical cap and all dynamic laws above are introduced, not a vendor force-speed map or safety/life qualification."
        },
        "lever_screen": [
            {"displacement_ratio": r, "conditional_joint_free_travel_m": 0.010/r,
             "effective_linear_damping_multiplier": r*r,
             "joint_force_for_reported_80N_separator_bias_N": r*80.0,
             "joint_force_if_3000N_at_damper_N": r*3000.0}
            for r in [1.0, 10.0, 20.0, 100.0, 200.0]
        ],
        "fixed_ratio_lever_feasibility_screen": {
            "introduced_joint_takeup_allowance_m": 50e-6,
            "introduced_required_joint_payout_m": EQUILIBRIUM_M,
            "rounded_damper_total_stroke_m": 0.050,
            "conditional_damper_free_travel_m": 0.010,
            "ratio_required_for_takeup_allowance": 0.010 / 50e-6,
            "ratio_max_for_total_stroke": 0.050 / EQUILIBRIUM_M,
            "minimum_joint_takeup_if_whole_stroke_needed_m": 0.20 * EQUILIBRIUM_M,
            "scope": "fixed positive motion ratio, no separate pre-stroke or extra motion source; all usable stroke granted, no end-stop margins"
        },
        "separator_affine_bias_screens": [
            {"introduced_constant_signed_bias_N": b,
             "equilibrium_m": (FORCE_N + b) / STIFFNESS_N_M,
             "relative_equilibrium_energy_J": (FORCE_N + b)**2 / (2.0 * STIFFNESS_N_M),
             "scope": "constant-force approximation only; actual gas preload direction/stiffness/inventory not supplied"}
            for b in [-80.0, 0.0, 80.0]
        ],
        "rows": rows,
        "limitations": ["one captured relative coordinate, fixed positive stiffness and mass",
                        "one-time take-up, not measured backlash on every reversal",
                        "ideal critical viscous law or introduced force clip",
                        "no geometric instability, full wrench, fluid compliance, seal or temperature model",
                        "viscous dissipation alone provides no static power-loss lock",
                        "no manufactured preload carriage, guides, receiver, sensing or finite-life qualification"]
    }


if __name__ == "__main__":
    output = run()
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({"output": str(path), "parameters": output["parameters"],
                      "threshold_m": output["monotone_critical_takeup_threshold_m"],
                      "rows": [{"d_m": r["takeup_m"],
                                "xmax_m": r["ideal_linear_critical"]["peak_displacement_m"],
                                "Fmax_N": r["ideal_linear_critical"]["peak_damper_force_N"],
                                "capped_xmax_m": r["numerical_force_limited"].get("peak_displacement_m_sampled")}
                               for r in output["rows"]]}))
