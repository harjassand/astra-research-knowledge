#!/usr/bin/env python3
"""Exact synthetic checks only; no experimental inputs or capability claims."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def vec(*v):
    return tuple(F(x) for x in v)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def mul(a, x):
    return tuple(a * b for b in x)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def mix(w, x, y):
    return add(mul(w, x), mul(1 - w, y))


def nuisance(r):
    return (r[0] + r[1], r[2])


def exchange(r):
    return (r[0] - r[1]) / 2


def det(x, y):
    return x[0] * y[1] - x[1] * y[0]


def endpoint_capacity(delta):
    return max(sum(max(v, 0) for v in delta), sum(max(-v, 0) for v in delta))


def trace_capacity(trace):
    coordinate_maxima = [max(row[i] for row in trace) for i in range(len(trace[0]))]
    return sum(coordinate_maxima) - min(sum(row) for row in trace)


def strings(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, tuple):
        return [strings(x) for x in obj]
    if isinstance(obj, list):
        return [strings(x) for x in obj]
    if isinstance(obj, dict):
        return {k: strings(v) for k, v in obj.items()}
    return obj


def main():
    z = vec(1, 1, -1)
    e = vec(1, -1, 0)
    r1 = vec(4, 2, 6)
    r2 = vec(-1, -2, -3)
    w = F(1, 3)
    nominal = mix(w, r1, r2)
    assert nominal == mul(F(2, 3), e)
    assert dot(z, r1) == dot(z, r2) == dot(z, e) == 0

    nonneutral = vec(-1, -2, -4)
    chloride_weight = F(2, 5)
    chloride_cancel = mix(chloride_weight, r1, nonneutral)
    assert chloride_cancel == vec(1, F(-2, 5), 0)
    cation_cancel = mix(w, r1, nonneutral)
    assert cation_cancel == vec(F(2, 3), F(-2, 3), F(-2, 3))
    assert det(nuisance(r1), nuisance(nonneutral)) == -6

    q = F(25)  # Synthetic nanomole units.
    alpha = F(3)
    membrane = vec(q, -q, -alpha)
    xi_R = -alpha
    reservoir_R = vec(membrane[0], membrane[1], membrane[2] - xi_R)
    assert reservoir_R == mul(q, e)
    assert xi_R == -dot(z, membrane)

    # Smooth-state solution: exp(-ln(2)*1)=1/2,
    # exp(-ln(2)*2)=1/4. All integrated checks are rational.
    a, b = F(1, 2), F(1, 4)
    h0 = (1 - b) / (1 - a * b)
    h1 = a * h0
    h2 = 1 - b + b * h1
    d = h0 - h1
    assert (h0, h1, h2, d) == (F(6, 7), F(3, 7), F(6, 7), F(3, 7))
    v = mul(1 / d, e)
    corr_A = mul(h1 - h0, v)
    corr_B = mul(-(h2 - h1), v)
    baseline_integral = add(r1, mul(F(2), r2))
    actual_integral = add(baseline_integral, add(corr_A, corr_B))
    assert corr_A == corr_B == mul(F(-1), e)
    assert baseline_integral == mul(F(2), e)
    assert actual_integral == vec(0, 0, 0)

    # Current AND chloride match program by program, exchange does not.
    alt1 = vec(3, 3, 6)
    alt2 = vec(F(-3, 2), F(-3, 2), -3)
    assert dot(z, alt1) == dot(z, alt2) == 0
    assert (alt1[2], alt2[2]) == (r1[2], r2[2])
    assert mix(w, alt1, alt2) == vec(0, 0, 0)

    # Common total cation capacity B, hidden order LLi, LNa, RLi, RNa.
    B = 2 * q
    s0 = vec(0, q, q, 0)
    sT = vec(q, 0, 0, q)
    ds = add(sT, mul(F(-1), s0))
    dL = mul(F(-1), ds[:2])
    dR = mul(F(-1), ds[2:])
    Qobs = (dR[0] - dR[1] - dL[0] + dL[1]) / 4
    assert dL == vec(-q, q) and dR == vec(q, -q)
    assert sum(s0) == sum(sT) == B
    assert s0[0] + s0[2] == sT[0] + sT[2] == q
    assert s0[1] + s0[3] == sT[1] + sT[3] == q
    assert Qobs == q == B / 2

    vertices = [vec(0, 0, 0, 0)]
    vertices += [tuple(B if i == j else F(0) for i in range(4)) for j in range(4)]
    coeff = vec(F(1, 4), F(-1, 4), F(-1, 4), F(1, 4))
    values = [dot(coeff, s) for s in vertices]
    width = max(values) - min(values)
    assert width == B / 2
    # Exhaustive simplex-vertex pairs attain the width; the balanced
    # storage construction also attains it with global species totals fixed.
    errors = [dot(coeff, add(t, mul(F(-1), s))) for s, t in product(vertices, repeat=2)]
    assert min(errors) == -B / 2 and max(errors) == B / 2
    assert dot(coeff, ds) == B / 2

    # Independently enumerate all integer initial/final simplex states,
    # then compare their difference set with the closed-form capacity test.
    enum_B = 4
    simplex_states = [v for v in product(range(enum_B + 1), repeat=4) if sum(v) <= enum_B]
    attainable_changes = {
        tuple(ti - si for si, ti in zip(s, t))
        for s, t in product(simplex_states, repeat=2)
    }
    enum_checked = 0
    for delta_vec in product(range(-enum_B, enum_B + 1), repeat=4):
        assert (delta_vec in attainable_changes) == (endpoint_capacity(delta_vec) <= enum_B)
        enum_checked += 1
    for candidate in (F(i) for i in range(-10, 61)):
        J_candidate = vec(candidate, -candidate)
        hidden_change = add(mul(F(-1), J_candidate), mul(F(-1), dL)) + add(J_candidate, mul(F(-1), dR))
        assert endpoint_capacity(hidden_change) == 2 * abs(q - candidate)

    positive_trace = [vec(0, 0, 0, 0), vec(-q, q, q, -q)]
    bidirectional_trace = positive_trace + [vec(q, -q, -q, q)]
    assert trace_capacity(positive_trace) == 2 * q
    assert trace_capacity(bidirectional_trace) == 4 * q
    trace_m = vec(*(max(row[i] for row in bidirectional_trace) for i in range(4)))
    hidden_trace = [add(trace_m, mul(F(-1), row)) for row in bidirectional_trace]
    assert all(min(row) >= 0 for row in hidden_trace)
    assert max(map(sum, hidden_trace)) == trace_capacity(bidirectional_trace)

    # Robust two-program interval example.
    a1, b1, a2, b2 = F(5), F(7), F(-4), F(-2)
    m1, m2 = (a1 + b1) / 2, (a2 + b2) / 2
    w1, w2 = (b1 - a1) / 2, (b2 - a2) / 2
    robust_weight = -m2 / (m1 - m2)
    robust_radius = robust_weight * w1 + (1 - robust_weight) * w2
    assert robust_weight == F(1, 3) and robust_radius == 1
    low = robust_weight * a1 + (1 - robust_weight) * a2
    high = robust_weight * b1 + (1 - robust_weight) * b2
    assert (low, high) == (F(-1), F(1))
    # Check all rectangle corners and a fine rational weight grid.
    for t in (F(i, 300) for i in range(301)):
        worst = max(abs(t * S1 + (1 - t) * S2) for S1, S2 in product((a1, b1), (a2, b2)))
        assert worst >= robust_radius
    delta = F(1)
    lower = max(F(0), (-delta - a2) / (a1 - a2))
    upper = min(F(1), (delta - b2) / (b1 - b2))
    assert lower == upper == robust_weight
    tight_delta = F(1, 2)
    tight_lower = max(F(0), (-tight_delta - a2) / (a1 - a2))
    tight_upper = min(F(1), (tight_delta - b2) / (b1 - b2))
    assert tight_lower > tight_upper
    x1_min, x2_min = F(9, 10), F(2, 5)
    x_guaranteed = robust_weight * x1_min + (1 - robust_weight) * x2_min
    assert x_guaranteed == F(17, 30)

    # Proposed design arithmetic is conditional, not a physical B estimate.
    eta = F(5, 2)
    capacity_strict_upper = 2 * (q - eta)
    assert capacity_strict_upper == 45
    per_run_error = F(5, 2)
    gain = q - per_run_error
    N_min = (B / (2 * gain)).numerator // (B / (2 * gain)).denominator + 1
    assert N_min == 2
    assert N_min * gain > B / 2 and (N_min - 1) * gain <= B / 2

    # Complete scalar traces distinguish excursion from total variation.
    trace = [F(0), F(10), F(0), F(10), F(0)]
    scalar_B = F(10)
    assert max(trace) - min(trace) == scalar_B
    total_variation = sum(abs(y - x) for x, y in zip(trace, trace[1:]))
    assert total_variation == 4 * scalar_B
    s_initial = max(trace)
    scalar_stores = [s_initial - x for x in trace]
    assert all(0 <= s <= scalar_B for s in scalar_stores)

    results = {
        "status": "PASS_SYNTHETIC_IDENTITIES_ONLY",
        "physical_measurements": False,
        "novelty_established": False,
        "neutral_time_share": {"weight": w, "output": nominal},
        "nonneutral_counterexample": {
            "nuisance_determinant": det(nuisance(r1), nuisance(nonneutral)),
            "chloride_cancel_output": chloride_cancel,
            "cation_cancel_output": cation_cancel,
        },
        "electrode_counterexample": {"membrane": membrane, "xi_R": xi_R, "reservoir_R": reservoir_R},
        "hysteresis": {"h0": h0, "h1": h1, "h2": h2, "baseline_integral": baseline_integral, "actual_integral": actual_integral},
        "current_and_chloride_alias": {"alternative_output": mix(w, alt1, alt2)},
        "storage": {"B": B, "q": q, "s0": s0, "sT": sT, "dL": dL, "dR": dR, "support_width": width},
        "endpoint_capacity_formula": {"enumeration_capacity": enum_B, "simplex_state_count": len(simplex_states), "initial_final_pair_count": len(simplex_states) ** 2, "candidate_changes_checked": enum_checked, "attainable_changes": len(attainable_changes)},
        "common_initial_trace": {"single_excursion_capacity": trace_capacity(positive_trace), "bidirectional_excursion_capacity": trace_capacity(bidirectional_trace), "explicit_minimal_hidden_trace": hidden_trace},
        "robust_selector": {"weight": robust_weight, "unavoidable_salt_radius": robust_radius, "exchange_lower_rate": x_guaranteed, "half_unit_tolerance_feasible": False},
        "finite_design": {"Qhat": q, "eta": eta, "B_must_be_strictly_below_for_positive_exchange": capacity_strict_upper, "synthetic_B": B, "N_min_at_synthetic_per_run_values": N_min},
        "storage_trace": {"range": max(trace) - min(trace), "total_variation": total_variation, "stores": scalar_stores},
        "limitations": ["No physical rate, capacity or uncertainty data", "No historical priority established", "No experimental capability or comparative advantage established"],
    }
    output = Path(__file__).with_name("EXACT_RESULTS.json")
    output.write_text(json.dumps(strings(results), indent=2) + "\n")
    print(json.dumps({"status": results["status"], "output": str(output)}))


if __name__ == "__main__":
    main()
