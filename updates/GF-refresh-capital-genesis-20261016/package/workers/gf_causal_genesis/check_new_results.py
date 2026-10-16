#!/usr/bin/env python3
"""Reproduce finite witnesses and numerical diagnostics using only Python stdlib.

This is a check of specified finite constructions, not a proof/novelty validator.
It writes only check_results.json beside this script.
"""
from __future__ import annotations

import cmath
import json
import math
import random
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSTAR = (math.pi + 2.0) / 4.0


def bisect_zero(f, lo, hi, n=90):
    assert f(lo) * f(hi) <= 0
    for _ in range(n):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


ALPHA = bisect_zero(lambda x: math.tan(x) - 2*x, 0.8, 1.5)
KCUT = ALPHA / math.sin(ALPHA)**2


def phi(p):
    p = min(1.0, max(0.0, p))
    if p <= 0.5:
        return math.asin(math.sqrt(p)) / KSTAR
    return (math.pi/4 + p - 0.5) / KSTAR


def rotate(v, theta):
    c, s = math.cos(theta), math.sin(theta)
    return [c*v[0] - s*v[1], s*v[0] + c*v[1]]


def norm2(v):
    return sum(abs(x)**2 for x in v)


def weak_finite(eps, n):
    theta0 = math.pi / 4
    delta = theta0 - math.atan(math.sqrt(1-eps))
    v = rotate([1.0, 0.0], theta0)
    success = 0.0
    action = theta0
    probes = 0.0
    feedback = 0.0
    click_branches = []
    for k in range(n):
        probes += norm2(v)
        click = [0.0, math.sqrt(eps)*v[1]]
        cp = norm2(click)
        click_branches.append(cp)
        success += cp
        v = [v[0], math.sqrt(1-eps)*v[1]]
        feedback += norm2(v)
        action += delta*norm2(v)
        v = rotate(v, delta)
    final_odd = abs(v[1])**2
    final_even = abs(v[0])**2
    success += final_odd
    r = 1 - eps/2
    expected = {
        "success": 1 - 0.5*r**n,
        "action": theta0 + delta*r*(1-r**n)/(1-r),
        "weak_probes": (1-r**n)/(1-r),
        "feedback_rotations": r*(1-r**n)/(1-r),
    }
    observed = {
        "success": success,
        "action": action,
        "weak_probes": probes,
        "feedback_rotations": feedback,
    }
    assert abs(success + final_even - 1) < 2e-12
    for key in observed:
        assert abs(observed[key]-expected[key]) < 3e-11
    assert action + 1e-12 >= KSTAR*success
    return {
        "epsilon": eps,
        "maximum_weak_probes": n,
        **observed,
        "action_per_success": action/success,
        "final_odd_probability_after_all_no_clicks": final_odd,
        "final_even_probability": final_even,
        "initial_rotation_action": theta0,
        "feedback_angle": delta,
        "actual_final_complete_measurements_if_required": 1,
        "maximum_formula_error": max(abs(observed[k]-expected[k]) for k in observed),
        "click_branch_probabilities": click_branches if n <= 12 else "omitted",
        "finite_exact_success_fallback": {
            "success": 1.0,
            "fallback_branch_probability": final_even,
            "additional_expected_action": math.pi/2*final_even,
            "total_expected_action": action+math.pi/2*final_even,
            "maximum_odd_action": theta0+n*delta+math.pi/2,
            "maximum_measurement_calls_with_boundary_verification": n+2,
            "expected_measurement_calls_with_boundary_verification": probes+1+final_even,
        },
    }


def weak_infinite(eps):
    delta = math.pi/4 - math.atan(math.sqrt(1-eps))
    return math.pi/4 + delta*(2-eps)/eps


def cut_full_cost(c):
    a = bisect_zero(lambda x: math.tan(x) - 2*(x+c), 0.8, math.pi/2-1e-9)
    return {"angle": a, "mean_cost": (a+c)/math.sin(a)**2,
            "mean_detector_calls": 1/math.sin(a)**2}


def zero(n, m=None):
    return [[0j for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = 1
    return a


def mul(a, b):
    out = zero(len(a), len(b[0]))
    for i in range(len(a)):
        for k in range(len(b)):
            for j in range(len(b[0])):
                out[i][j] += a[i][k]*b[k][j]
    return out


def adj(a):
    return [[a[i][j].conjugate() for i in range(len(a))] for j in range(len(a[0]))]


def add(a, b):
    return [[a[i][j]+b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def rot_a(theta):
    c, s = cmath.cos(theta), cmath.sin(theta)
    out = zero(4)
    for bath in range(2):
        out[bath][bath] = c
        out[bath][bath+2] = -s
        out[bath+2][bath] = s
        out[bath+2][bath+2] = c
    return out


def su2(theta, phase):
    c, s = math.cos(theta), math.sin(theta)
    u = cmath.exp(1j*phase)
    return [[c, -s*u.conjugate()], [s*u, c]]


def controlled_bath(u0, u1):
    out = zero(4)
    for a, u in enumerate([u0, u1]):
        for b in range(2):
            for c in range(2):
                out[2*a+b][2*a+c] = u[b][c]
    return out


def bath_projection(bit):
    out = zero(4)
    out[bit][bit] = out[bit+2][bit+2] = 1
    return out


def eigmax2(a):
    aa, bb = a[0][0].real, a[1][1].real
    assert abs(a[0][0].imag) < 1e-11 and abs(a[1][1].imag) < 1e-11
    return (aa+bb+math.sqrt(max(0, (aa-bb)**2+4*abs(a[0][1])**2)))/2


def variable_gap_check():
    rng = random.Random(26101637)
    max_excess = -1.0
    worst_tp = 0.0
    diagnostics = 0
    for _ in range(240):
        cap = rng.uniform(0.05, 1.4)
        first = cap*rng.uniform(0.15, 0.55)
        later = [cap-first, (cap-first)*rng.uniform(0.05, 0.9)]
        d = controlled_bath(su2(rng.uniform(0, 3), rng.uniform(-3, 3)),
                            su2(rng.uniform(0, 3), rng.uniform(-3, 3)))
        for x in [0.25, 0.7, 1.0, 1.35]:
            effect = zero(2)
            tp = zero(4)
            for b in range(2):
                k = mul(rot_a(x*later[b]), mul(bath_projection(b), mul(d, rot_a(x*first))))
                tp = add(tp, mul(adj(k), k))
                f = [[k[2+i][j] for j in range(2)] for i in range(2)]
                effect = add(effect, mul(adj(f), f))
            maxp = eigmax2(effect)
            bound = math.sin(min(abs(x)*cap, math.pi/2))**2
            max_excess = max(max_excess, maxp-bound)
            worst_tp = max(worst_tp, max(abs(tp[i][j]-(1 if i == j else 0))
                                         for i in range(4) for j in range(4)))
            assert maxp <= bound+4e-12
            assert worst_tp < 4e-12
            diagnostics += 1
    # Exact meaning of the selected-record counterexample: copy A into B after
    # angle pi/6 and read B. B=1 heralds parity 1 with probability 1/4.
    return {"samples": diagnostics, "bath_dimension": 2,
            "maximum_numerical_excess_over_sine_cap": max_excess,
            "maximum_trace_preservation_error": worst_tp,
            "postselected_record_obstruction": {
                "angle": "pi/6", "full_gap_opposite_probability": "1/4",
                "probability_of_selected_bath_record": "1/4",
                "conditional_opposite_probability_on_selected_record": "1",
                "claimed_normalized_conditional_sine_bound": "1/4",
                "verdict": "false; full unnormalized instrument bound remains valid"}}


def potential_check():
    rng = random.Random(26101638)
    gain = -1.0
    mass_error = 0.0
    speed_excess = -1.0
    for _ in range(4000):
        p, g0, g1 = rng.random(), rng.random(), rng.random()
        w0 = (1-p)*g0+p*g1
        w1 = 1-w0
        q0 = p*g1/w0
        q1 = p*(1-g1)/w1
        gain = max(gain, w0*phi(q0)+w1*phi(q1)-phi(p))
        mass_error = max(mass_error, abs(w0*q0+w1*q1-p))
        t0, t1 = rng.random()*math.pi/2, rng.random()*math.pi/2
        speed_excess = max(speed_excess,
                           abs(phi(math.sin(t0)**2)-phi(math.sin(t1)**2))
                           - abs(t0-t1)/KSTAR)
    assert gain < 2e-12 and mass_error < 2e-12 and speed_excess < 2e-12
    return {"samples": 4000, "maximum_Jensen_gain": gain,
            "maximum_population_preservation_error": mass_error,
            "maximum_potential_speed_excess": speed_excess}


def main():
    start = time.perf_counter()
    finite = weak_finite(0.5, 12)
    exact_success = 1-Fraction(1, 2)*Fraction(3, 4)**12
    exact_weak_calls = (1-Fraction(3, 4)**12)/Fraction(1, 4)
    exact_feedback = Fraction(3, 4)*exact_weak_calls
    assert abs(finite["success"]-float(exact_success)) < 2e-12
    assert abs(finite["weak_probes"]-float(exact_weak_calls)) < 2e-12
    assert finite["action_per_success"] < KCUT
    finite["exact_success"] = str(exact_success)
    finite["exact_expected_weak_probes"] = str(exact_weak_calls)
    finite["exact_expected_feedback_rotations"] = str(exact_feedback)
    convergence = [{"epsilon": e, "mean_odd_action": weak_infinite(e),
                    "excess_above_universal_infimum": weak_infinite(e)-KSTAR,
                    "expected_weak_probes": 2/e,
                    "expected_feedback_rotations": (2-e)/e}
                   for e in [1.0, 0.5, 0.2, 0.1, 0.02, 0.005]]
    assert all(row["mean_odd_action"] >= KSTAR-1e-10 for row in convergence)
    break_even = bisect_zero(lambda c: weak_infinite(0.5)+4*c-cut_full_cost(c)["mean_cost"], 0, 0.1)
    costs = [{"probe_cost": c,
              "weak_epsilon_half_mean_cost": weak_infinite(0.5)+4*c,
              "finite_exact_witness_full_measurement_cost": finite["finite_exact_success_fallback"]["total_expected_action"]
                  +c*finite["finite_exact_success_fallback"]["expected_measurement_calls_with_boundary_verification"],
              "best_complete_cut_benchmark": cut_full_cost(c)}
             for c in [0, 0.01, 0.03, 0.1]]
    fallback = finite["finite_exact_success_fallback"]
    assert KSTAR <= fallback["total_expected_action"] < KCUT
    balanced_cost = fallback["total_expected_action"]-math.pi/4
    pure_values = []
    for theta in [0, math.pi/8, math.pi/4, math.pi/3, 1.5, math.pi/2]:
        p = math.sin(theta)**2
        lower = KSTAR-theta if theta <= math.pi/4 else 1-p
        construction = math.pi/4-theta+balanced_cost if theta <= math.pi/4 else 2*(1-p)*balanced_cost
        assert construction+1e-12 >= lower
        assert abs(lower-KSTAR*(1-phi(p))) < 1e-12
        pure_values.append({"initial_angle": theta, "initial_odd_population": p,
                            "exact_infimum": lower,
                            "finite_exact_success_design_action": construction})
    activation = {
        "activation_probability": "1/4",
        "conditional_active_angle_each": "pi/2",
        "joint_all_bad": "1/4", "each_marginal_bad": "1/4",
        "product_of_marginal_bad": "1/16",
        "expected_action_each": "pi/8",
        "full_endpoint_distribution": {"00": "3/4", "01": "0", "10": "0", "11": "1/4"},
        "product_of_universal_mean_action_certificates": (math.pi/(8*KSTAR))**2,
        "product_of_complete_cut_mean_action_certificates": (math.pi/(8*KCUT))**2,
    }
    assert activation["product_of_universal_mean_action_certificates"] < 0.25
    assert activation["product_of_complete_cut_mean_action_certificates"] < 0.25
    mean_hazard = {
        "common_activation_probability": "1/4",
        "conditional_active_angle": "pi/4",
        "joint_all_bad": "1/16",
        "each_mean_authorized_hazard": "(log 2)/4",
        "product_of_mean_hazard_factors": (1-2**(-0.25))**2,
        "stopped_singleton_obstruction": {
            "maximum_attempts": 2, "each_attempt_angle": "pi/4",
            "stopping_rule": "stop on first mismatch",
            "actual_success": "3/4",
            "expected_billed_hazard": "(3/2) log 2",
            "invalid_mean_hazard_certificate": 1-2**(-1.5),
            "source": "internal reconstruction by gf_causal_adversary"},
    }
    assert mean_hazard["product_of_mean_hazard_factors"] < 1/16
    assert mean_hazard["stopped_singleton_obstruction"]["invalid_mean_hazard_certificate"] < 3/4
    out = {
        "status": "specified finite checks passed",
        "scope": "analytic proofs remain in the Markdown files; these checks do not establish general validity, novelty or hardware performance",
        "dependencies": "Python standard library only; no install, downloaded code, model calls, GPU or external execution",
        "constants": {"universal_weak_instrument_infimum": KSTAR,
                      "complete_cut_restart_angle": ALPHA,
                      "complete_cut_restart_success_per_attempt": math.sin(ALPHA)**2,
                      "complete_cut_restart_infimum": KCUT},
        "finite_weak_herald_witness": finite,
        "known_pure_state_value_checks": pure_values,
        "weak_limit_costs": convergence,
        "positive_probe_cost_design_comparison": costs,
        "epsilon_half_break_even_probe_cost_against_complete_cut_benchmark": break_even,
        "joint_mean_cost_counterexample": activation,
        "mean_hazard_counterexamples": mean_hazard,
        "variable_classical_tree_gap_diagnostics": variable_gap_check(),
        "population_potential_diagnostics": potential_check(),
    }
    out["execution_wall_seconds"] = time.perf_counter()-start
    path = HERE/"check_results.json"
    path.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"status": out["status"], "output": str(path),
                      "finite_success": finite["success"],
                      "finite_action_per_success": finite["action_per_success"],
                      "universal_action_infimum": KSTAR,
                      "complete_cut_restart_infimum": KCUT,
                      "wall_seconds": out["execution_wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
