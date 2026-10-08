#!/usr/bin/env python3
"""Exact algebraic check and illustrative sign/conditioning calculations.

No biological data are loaded. All numbers are synthetic model inputs.
"""
from __future__ import annotations
import json
from math import isclose
from itertools import product


def response_ratio(loop_gain: float, target_gain: float, feedback_gain: float) -> float:
    if loop_gain < 0 or target_gain <= 0 or feedback_gain < 0:
        raise ValueError("Require L>=0, r_g>0 and r_f>=0")
    return target_gain * (1.0 + loop_gain) / (1.0 + loop_gain * feedback_gain)


def estimate_loop_gain(q: float, feedback_gain: float) -> float:
    denom = q * feedback_gain - 1.0
    if abs(denom) < 1e-12:
        raise ValueError("ill-conditioned/singular q*r_f=1 interface")
    value = (1.0 - q) / denom
    if value < 0:
        raise ValueError("incompatible with positive loop gain")
    return value


def derivative_abs(q: float, feedback_gain: float) -> float:
    return abs(1.0 - feedback_gain) / abs(q * feedback_gain - 1.0) ** 2


def robust_classify(
    loop_gain: tuple[float, float],
    target_gain: tuple[float, float],
    feedback_gain: tuple[float, float],
    input_area_ratio: tuple[float, float] = (1.0, 1.0),
    margin: float = 0.0,
) -> dict[str, float | str]:
    """Return a certified sign only when every uncertainty corner clears it."""
    for name, interval in (("L", loop_gain), ("r_g", target_gain), ("r_f", feedback_gain), ("r_u", input_area_ratio)):
        if len(interval) != 2 or interval[0] > interval[1]:
            raise ValueError(f"invalid {name} interval")
    if loop_gain[0] < 0 or feedback_gain[0] < 0 or target_gain[0] <= 0 or input_area_ratio[0] <= 0:
        raise ValueError("invalid physical interval")
    values = [ru * response_ratio(L, rg, rf)
              for L, rg, rf, ru in product(loop_gain, target_gain, feedback_gain, input_area_ratio)]
    lower, upper = min(values), max(values)
    if lower > 1.0 + margin:
        status = "CERTIFIED_PRIMING"
    elif upper < 1.0 - margin:
        status = "CERTIFIED_TOLERANCE"
    else:
        status = "UNKNOWN"
    return {"status": status, "lower_ratio": lower, "upper_ratio": upper}


def simulate_auc(a_f: float, a_g: float, schedule: str, dt: float = 0.01) -> dict[str, float]:
    """RK4 integration of the stated linearized model, in synthetic min units."""
    lam, dm, dp = 1.0, 0.5, 0.2
    gamma, km, kp = 0.4, 1.0, 1.0
    b, kg, dg = 1.0, 1.0, 0.3
    horizon = 200.0
    n = round(horizon / dt)
    state = [0.0, 0.0, 0.0, 0.0]  # x, m, z, y
    integrals = [0.0, 0.0, 0.0, 0.0]

    def u(t: float) -> float:
        if schedule == "one_pulse":
            return 1.0 if 0.0 <= t < 6.0 else 0.0
        if schedule == "four_spaced_pulses":
            return 1.0 if any(s <= t < s + 1.5 for s in (0.0, 20.0, 40.0, 60.0)) else 0.0
        raise ValueError(schedule)

    def rhs(t: float, q: list[float]) -> list[float]:
        x, m, z, y = q
        return [b * u(t) - lam * x - gamma * z,
                km * a_f * x - dm * m,
                kp * m - dp * z,
                kg * a_g * x - dg * y]

    for j in range(n):
        t = j * dt
        k1 = rhs(t, state)
        k2 = rhs(t + dt / 2, [v + dt * w / 2 for v, w in zip(state, k1)])
        k3 = rhs(t + dt / 2, [v + dt * w / 2 for v, w in zip(state, k2)])
        k4 = rhs(t + dt, [v + dt * w for v, w in zip(state, k3)])
        nxt = [v + dt * (w1 + 2*w2 + 2*w3 + w4) / 6
               for v, w1, w2, w3, w4 in zip(state, k1, k2, k3, k4)]
        for j_state in range(4):
            integrals[j_state] += dt * (state[j_state] + nxt[j_state]) / 2
        state = nxt
    return {"auc_x": integrals[0], "auc_y": integrals[3], "terminal_state_norm": max(abs(v) for v in state)}


def main() -> None:
    L, rg, rf = 4.0, 1.5, 2.0
    R = response_ratio(L, rg, rf)
    q = (1.0 + L) / (1.0 + L * rf)
    recovered = estimate_loop_gain(q, rf)
    sens = derivative_abs(q, rf)
    assert isclose(R, 5.0 / 6.0, rel_tol=1e-14)
    assert isclose(q, 5.0 / 9.0, rel_tol=1e-14)
    assert isclose(recovered, L, rel_tol=1e-14)
    assert isclose(sens, 81.0, rel_tol=1e-14)
    no_feedback_enhancer_change = response_ratio(L, rg, 1.0)
    assert isclose(no_feedback_enhancer_change, 1.5)
    schedules = {}
    for pulse_schedule in ("one_pulse", "four_spaced_pulses"):
        naive = simulate_auc(a_f=1.0, a_g=1.0, schedule=pulse_schedule)
        primed = simulate_auc(a_f=2.0, a_g=rg, schedule=pulse_schedule)
        numerical_ratio = primed["auc_y"] / naive["auc_y"]
        assert abs(numerical_ratio - R) < 2e-5
        schedules[pulse_schedule] = {
            "naive_auc_x": naive["auc_x"],
            "naive_auc_y": naive["auc_y"],
            "primed_auc_x": primed["auc_x"],
            "primed_auc_y": primed["auc_y"],
            "observed_model_ratio": numerical_ratio,
            "tail_residual_max": max(naive["terminal_state_norm"], primed["terminal_state_norm"])
        }
    pulse_shape_naive_ratio = schedules["four_spaced_pulses"]["naive_auc_y"] / schedules["one_pulse"]["naive_auc_y"]
    robust_tolerance = robust_classify((4.0, 5.0), (1.4, 1.6), (2.0, 2.2), (0.98, 1.02), margin=0.05)
    robust_unknown = robust_classify((1.0, 6.0), (0.8, 1.6), (0.8, 2.2), (0.98, 1.02), margin=0.05)
    assert robust_tolerance["status"] == "CERTIFIED_TOLERANCE"
    assert robust_unknown["status"] == "UNKNOWN"
    result = {
        "status": "synthetic_algebraic_check_only",
        "inputs": {"L": L, "r_g": rg, "r_f": rf},
        "target_AUC_ratio": R,
        "classification": "tolerance" if R < 1 else "priming" if R > 1 else "neutral",
        "RelA_AUC_ratio_q": q,
        "recovered_L": recovered,
        "abs_dL_dq": sens,
        "target_only_gain_when_feedback_held_fixed": no_feedback_enhancer_change,
        "rk4_model_audit": {
            "status": "finite_synthetic_ode_replay",
            "step_minutes": 0.01,
            "horizon_minutes": 200.0,
            "equal_input_area": 6.0,
            "schedules": schedules,
            "LTI_AUC_ratio_four_spaced_over_one_pulse": pulse_shape_naive_ratio,
            "interpretation": "The model law is schedule-independent for fully captured AUC; it cannot explain the published equal-area pulse-train enhancement without nonlinear/state-dependent or finite-window terms."
        },
        "robust_decision_examples": {
            "synthetic_interval_certified_tolerance": robust_tolerance,
            "synthetic_overlap_returns_unknown": robust_unknown,
            "meaning": "Worst-case uncertainty is taken over all gain and matched-input interval corners; these synthetic intervals are not acquired biology."
        },
        "costs_not_included": ["cells", "perturbation calibration", "reporters", "RNA half-life", "culture replication", "chromatin assay"]
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
