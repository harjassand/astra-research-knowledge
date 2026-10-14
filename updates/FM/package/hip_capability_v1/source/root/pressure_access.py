"""Reproducible conditional HIP gates; no physical experiment or fitted alloy law.

Python standard library only. All dimensional examples are sensitivity tests.
Run from any directory; JSON is written beside this script.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math


def pressure_coefficient(radius, length, volume, viscosity):
    return math.pi * radius**4 / (16 * viscosity * length * volume)


def step_pressure(p0, external, coefficient, duration):
    """Exact fixed-geometry isothermal ideal-gas Poiseuille step, 0<=p0<P."""
    assert external > 0 and 0 <= p0 < external
    return external * math.tanh(coefficient * external * duration
                                + math.atanh(p0 / external))


def ramp_pressure(radius, length, volume, viscosity, rate, maximum, steps):
    """Implicit Euler at endpoints of a linear ramp, with analytic root.

    This convergent stepping is stable even for fast gas filling. Using the
    endpoint pressure avoids a spurious half-step lag in the stiff limit.
    Fixed throat and volume: it does NOT simulate sealing or material repair.
    """
    coefficient = pressure_coefficient(radius, length, volume, viscosity)
    dt = maximum / rate / steps
    p = 0.0
    lag_max = 0.0
    for j in range(steps):
        external = rate * (j + 1) * dt
        b = p + coefficient*dt*external**2
        p = 2*b/(1+math.sqrt(1+4*coefficient*dt*b))
        lag_max = max(lag_max, external-p)
    return {"end_internal_Pa": p, "end_lag_Pa": maximum-p,
            "max_sampled_lag_Pa": lag_max, "steps": steps}


def tracer_coefficient_interval(u, error, external, duration):
    """Normalized full-scale step response; error includes normalization error.

    Fixed V,T; initial p=0; independently acquired full-scale response.
    Does not infer a hot coefficient or certify sealing.
    """
    lo, hi = max(0, u-error), min(1, u+error)
    return (math.atanh(lo)/(external*duration),
            math.inf if hi == 1 else math.atanh(hi)/(external*duration))


def hot_fill_verdict(coefficient_interval, multiplier_interval, pressure,
                     duration, allowed_fraction):
    """Only a fixed-geometry filling decision given an acquired hot transfer."""
    if multiplier_interval is None:
        return "UNKNOWN: hot transfer not acquired"
    low = math.tanh(coefficient_interval[0]*multiplier_interval[0]*pressure*duration)
    high = math.tanh(coefficient_interval[1]*multiplier_interval[1]*pressure*duration)
    if high <= allowed_fraction:
        return "LOW_FILL_CONDITIONAL"
    if low > allowed_fraction:
        return "HIGH_FILL_CONDITIONAL"
    return "UNKNOWN: interval crosses decision"


def main():
    # Interior two-world witness. Same complete room pressure map, different
    # unacquired hot creep. Locally linear hot flow model only. Finite z is a
    # stipulated geometric/contact event, NOT a gas-tight seal from this ODE.
    ell = math.log(2)
    integral = Fraction(15, 64)  # (1-exp(-4 ell))/4
    p_a = integral / 10
    p_b_formal = integral / Fraction(1, 10)
    assert p_a == Fraction(3, 128)
    assert p_b_formal == Fraction(75, 32) > 1
    z_b_limit = -math.log(0.6)/4
    assert z_b_limit < ell
    room_curve = [step_pressure(0, 1, .25, t) for t in [0, .1, 1, 10]]

    # Full compressible model invariant: log(1+q)=(1-exp(-4z))/(4*m*tau).
    z_seal = .1
    numerator = 1-math.exp(-4*z_seal)
    compressible = []
    for mt in [.2, .01]:
        exponent = numerator/(4*mt)
        attainable = exponent < math.log(2)
        compressible.append({"m_times_tau": mt, "criterion_attainable": attainable,
            "q_at_criterion_if_formal": math.expm1(exponent),
            "z_at_q_0_9": -math.log(1-4*mt*math.log(1.9))/4})
    assert compressible[0]["criterion_attainable"]
    assert not compressible[1]["criterion_attainable"]

    # Sensitivity envelope, explicitly not source-measured HIP parameters.
    volume = 4*math.pi*(10e-6)**3/3
    length, viscosity, rate, maximum = 100e-6, 5e-5, 10e6, 100e6
    rows = []
    for radius_nm in [5, 10, 20, 50, 100, 500]:
        radius = radius_nm*1e-9
        coefficient = pressure_coefficient(radius, length, volume, viscosity)
        r1 = ramp_pressure(radius, length, volume, viscosity, rate, maximum, 20000)
        r2 = ramp_pressure(radius, length, volume, viscosity, rate, maximum, 40000)
        # Slew barrier for constant C: Delta <= sqrt(Rmax/C), initial p=P=0.
        barrier = math.sqrt(rate/coefficient)
        assert r2["max_sampled_lag_Pa"] <= barrier + maximum/40000
        rows.append({"radius_nm": radius_nm,
                     "near_equilibrium_time_s": 1/(2*coefficient*maximum),
                     "conservative_slew_barrier_Pa": barrier,
                     "ramp_20000": r1, "ramp_40000": r2,
                     "end_lag_discretization_difference_Pa": abs(r1["end_lag_Pa"]-r2["end_lag_Pa"]),
                     "quasistatic_lag_approximation_Pa": rate/(2*coefficient*maximum)})

    # Positive metrology in the supplied fixed-geometry model, followed by the
    # indispensable UNKNOWN when hot transport has not been acquired.
    true_c = .002
    u = step_pressure(0, 2, true_c, 10)/2
    interval = tracer_coefficient_interval(u, .001, 2, 10)
    assert interval[0] <= true_c <= interval[1]
    unknown = hot_fill_verdict(interval, None, 100, 1, .1)
    assert unknown.startswith("UNKNOWN")
    result = {
        "scope": "internal exact algebra, fixed-geometry synthetic numerics and conditional acquisition gate only",
        "physical_experiment": False, "novelty_established": False,
        "linear_two_worlds": {"same_room_curve_both_worlds": room_curve,
            "p_at_criterion_A_exact": str(p_a), "p_at_criterion_B_formal_exact": str(p_b_formal),
            "world_B_closure_limit": z_b_limit, "criterion_z": ell,
            "gas_tight_seal_law": "NOT ACQUIRED; finite radius is not a seal"},
        "compressible_two_worlds": compressible,
        "illustrative_parameters": {"pore_radius_m": 10e-6,
            "throat_length_m": length, "viscosity_Pa_s": viscosity,
            "ramp_Pa_per_s": rate, "maximum_Pa": maximum,
            "alloy_creep_parameters": "NOT ACQUIRED"},
        "sensitivity_rows": rows,
        "tracer": {"measured_synthetic_u": u, "C_interval": interval,
            "missing_hot_transfer_verdict": unknown,
            "conditional_fill_at_transfer_1": hot_fill_verdict(interval, (1,1), 100, 1, .1)},
        "trapped_gas": {"p_seal_Pa": 70e6, "P_final_Pa": 100e6,
            "V_final_over_V_seal_min_isothermal_no_capillarity": .7},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out = Path(__file__).with_name("pressure_access_results.json")
    out.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"passed": True, "output": str(out), "scope": result["scope"]}))


if __name__ == "__main__":
    main()
