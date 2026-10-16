#!/usr/bin/env python3
"""Exact rational checks; constructed examples, not acquired chemistry data.

Run: python3 check_transfer_calibration.py
Writes TRANSFER_CALIBRATION_CHECK.json beside this source.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import time


def matmul(a, b):
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def transpose(a):
    return [list(x) for x in zip(*a)]


def rank(a):
    a = [[F(v) for v in row] for row in a]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        scale = a[r][c]
        a[r] = [v / scale for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                scale = a[i][c]
                a[i] = [v - scale * u for v, u in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def scalar(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {k: scalar(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [scalar(x) for x in v]
    return v


start = time.perf_counter()

# Three assigned, resolved species. All concentrations are strictly positive.
# The conserved quantity is q1 + 2*q2 + q3 = 10.
w = [F(1), F(2), F(1)]
response = [F(2), F(3), F(5)]
q = [[F(4), F(2), F(2)], [F(3), F(5, 2), F(2)],
     [F(3), F(2), F(3)]]
u = [[r * x for r, x in zip(response, row)] for row in q]
theta = [a / r for a, r in zip(w, response)]
delta = [[x - y for x, y in zip(row, u[0])] for row in u[1:]]
assert rank(u) == 3 and rank(delta) == 2
assert all(sum(a*x for a, x in zip(w, row)) == 10 for row in q)
assert all(sum(a*x for a, x in zip(theta, row)) == 10 for row in u)
assert all(sum(a*x for a, x in zip(theta, row)) == 0 for row in delta)

# Exact coelution / unknown spectrum ambiguity even with a perfect total.
# T preserves the sum of concentrations; both spectra and mixtures remain >0.
s = [[F(2), F(1)], [F(1), F(2)]]
t = [[F(4, 5), F(1, 5)], [F(1, 5), F(4, 5)]]
t_inv = [[F(4, 3), F(-1, 3)], [F(-1, 3), F(4, 3)]]
x = [[F(9, 10), F(1, 5), F(3, 5)],
     [F(1, 10), F(4, 5), F(2, 5)]]
xp = matmul(t, x)
sp = matmul(s, t_inv)
observations = matmul(s, x)
assert matmul(sp, xp) == observations
assert all(v > 0 for row in sp + xp for v in row)
assert [sum(col) for col in zip(*x)] == [sum(col) for col in zip(*xp)]
assert x[0] != xp[0]

# A full continuum of reaction times, not just an overfit finite example:
# A -> B with fraction 4/5 and A -> unseen H with fraction 1/5.
# All three carry one conserved moiety and the observed responses are 1.
# The closed two-species model changes B's response to 4/5 and exactly fits
# all data and a separately measured total of 100, yet overcounts B by 25%.
hidden_examples = []
for k in range(101):
    tau = F(k, 100)
    a, b, h = 100 * (1 - tau), 80 * tau, 20 * tau
    fitted_a, fitted_b = a, F(5, 4) * b
    assert a + b + h == 100
    assert fitted_a + fitted_b == 100
    assert F(4, 5) * fitted_b == b
    if b:
        assert (fitted_b - b) / b == F(1, 4)
    hidden_examples.append({"t": tau, "true_A": a, "true_B": b,
                            "unseen_H": h, "fitted_A": fitted_a,
                            "fitted_B": fitted_b})
assert rank([[e["true_A"], e["true_B"]] for e in hidden_examples]) == 2

# Symbolic endpoint coefficient identity establishes all real t in [0,1].
# Coefficients of 1,t: true total = [100,0] = fitted total.
assert [100, -100 + 80 + 20] == [100, -100 + F(5, 4)*80]
absolute_minimax_estimate = F(90)
relative_minimax_estimate = F(800, 9)
assert max(abs(absolute_minimax_estimate-80), abs(absolute_minimax_estimate-100)) == 10
assert abs(relative_minimax_estimate/80-1) == F(1, 9)
assert abs(relative_minimax_estimate/100-1) == F(1, 9)

# Even a completely observed connected branching network need not identify
# its response factors. A fixed product ratio makes its two product columns
# proportional at arbitrarily many reaction times.
fixed_branch_rows = [[100*(1-F(k, 100)), 2*80*F(k, 100),
                      3*20*F(k, 100)] for k in range(101)]
assert rank(fixed_branch_rows) == 2
# Independent control of branching can supply the missing direction.
varied_branch_rows = [[100, 0, 0], [50, 80, 30], [50, 20, 120]]
assert rank(varied_branch_rows) == 3
assert all(sum(a*b for a, b in zip(row, [F(1), F(1, 2), F(1, 3)])) == 100
           for row in varied_branch_rows)

# Bounded hidden branch fraction implies a sharp concentration-bias bound.
leakage = []
for eta in [F(0), F(1, 100), F(1, 20), F(1, 5)]:
    relative_error = eta / (1 - eta)
    leakage.append({"unobserved_branch_fraction": eta,
                    "relative_target_overestimate": relative_error})

# Binary channels with unknown cross-response remain nonidentified even when
# both transition shapes and all total measurements are perfectly smooth.
two_totals = [sum(col) for col in zip(*xp)]

result = {
    "scope": "Exact constructed algebra. No raw chemistry acquisition or physical validation.",
    "status": "PASS_EXACT_ALGEBRA_ONLY",
    "closed_assigned_channels": {
        "q_rows": q, "u_rows": u, "conserved_weights": w,
        "true_responses": response, "inverse_weighted_responses": theta,
        "observation_rank": rank(u), "difference_rank": rank(delta),
        "conserved_amount": 10,
    },
    "unknown_cross_response_counterexample": {
        "S": s, "T": t, "S_prime": sp, "X": x, "X_prime": xp,
        "identical_observation": observations, "identical_total": two_totals,
        "first_sample_target_fraction_original": x[0][0],
        "first_sample_target_fraction_alternative": xp[0][0],
    },
    "unseen_branch_counterexample": {
        "validity": "All real t in [0,1] by coefficient identity; 101 rational samples checked.",
        "true_A_formula": "100*(1-t)", "true_B_formula": "80*t",
        "true_unseen_H_formula": "20*t", "fitted_B_formula": "100*t",
        "total_true_and_fitted": 100,
        "true_B_response": 1, "fitted_B_response": F(4, 5),
        "relative_B_concentration_error": F(1, 4),
        "two_world_minimax_absolute_error_at_t1": 10,
        "two_world_minimax_relative_error_at_t1": F(1, 9),
        "absolute_error_optimal_estimate_at_t1": absolute_minimax_estimate,
        "relative_error_optimal_estimate_at_t1": relative_minimax_estimate,
        "perfect_initial_pure_A": True,
        "independent_total_conserved": True,
        "fitted_mass_balance_residual": 0,
        "observation_rank": 2,
        "examples": [hidden_examples[k] for k in (0, 25, 50, 75, 100)],
    },
    "leakage_bound": leakage,
    "connected_network_does_not_imply_excitation": {
        "reaction": "A -> B and A -> C; known complete three-species pool",
        "constant_branch_fraction_B": "4/5",
        "true_response_factors_A_B_C": [1, 2, 3],
        "number_of_times_checked": 101,
        "fixed_branch_observation_rank": rank(fixed_branch_rows),
        "required_rank": 3,
        "independently_varied_branch_rows": varied_branch_rows,
        "varied_branch_observation_rank": rank(varied_branch_rows),
    },
    "runtime_seconds": time.perf_counter() - start,
    "runtime_scope": "Only this exact-arithmetic script; not inference or experiment time.",
    "inference_tokens": "UNKNOWN", "inference_cost": "UNKNOWN",
    "inference_energy": "UNKNOWN", "physical_cost": "UNKNOWN",
}
out = Path(__file__).with_name("TRANSFER_CALIBRATION_CHECK.json")
out.write_text(json.dumps(scalar(result), indent=2) + "\n")
print(json.dumps({"status": result["status"], "output": str(out.resolve()),
                  "hidden_branch_relative_error": "1/4", "runtime_seconds": result["runtime_seconds"]}))
