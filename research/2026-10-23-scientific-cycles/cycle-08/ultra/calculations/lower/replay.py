#!/usr/bin/env python3
"""Bounded exact distribution admissions for the analytic joint-target lemma."""
from fractions import Fraction as F
from math import log
from pathlib import Path
import json
import time

START_CPU = time.process_time()
START_WALL = time.perf_counter()


def entropy(values):
    return -sum(float(x) * log(float(x)) for x in values if x)


def g(u):
    u = float(u)
    return (u + 1) * log(u + 1) - (u * log(u) if u else 0.0)


def h2(x):
    return entropy([x, 1-x])


def conditional_entropy(p):
    pj = {}
    for (k, j), prob in p.items():
        pj[j] = pj.get(j, F(0)) + prob
    return entropy(p.values()) - entropy(pj.values())


def target(D, L, w):
    result = {}
    for k in range(1, L + 1):
        # The randomized retained length is deliberately K-dependent.
        choices = [(k, F(k, L + 1)), (max(0, k-w), F(L + 1-k, L + 1))]
        for n, weight in choices:
            for j in range(n + 1):
                prob = F(1, D**n) if j == 0 else F(D - 1, D**(n-j+1))
                result[k, j] = result.get((k, j), F(0)) + weight * prob / L
    return result


CASES = [(2, 1, 0), (2, 2, 0), (2, 16, 0), (2, 16, 3),
         (2, 128, 8), (3, 16, 0), (3, 64, 5), (4, 64, 4)]
observations = []
for D, L, w in CASES:
    p = target(D, L, w)
    assert sum(p.values()) == 1
    for k in range(1, L + 1):
        assert sum(value for (kk, j), value in p.items() if kk == k) == F(1, L)
    mean_gap = sum(F(k-j) * value for (k, j), value in p.items())
    bound = F(w) + F(1, D-1)
    assert mean_gap <= bound
    hcond = conditional_entropy(p)
    assert hcond <= g(bound) + 1e-11

    a = 0
    while D**(a+1) <= L:
        a += 1
    event_prob = sum(value for (k, j), value in p.items() if 0 <= k-j <= w+a)
    event_floor = F(1)-F(1, D**(a+1))
    assert event_prob >= event_floor
    # An arbitrary K-independent last-digit distribution is a valid
    # no-feedback marginal. Check the exact event ceiling for uniform J.
    independent_event = sum(F(1, L*(L+1))
                            for k in range(1, L+1) for j in range(L+1)
                            if 0 <= k-j <= w+a)
    independent_ceiling = F(w+a+1, L)
    assert independent_event <= independent_ceiling

    # Replace J by 0 with probability e. K stays uniform, and the complete
    # classical distance is computed exactly rather than assumed to equal e.
    e = F(1, 7)
    q = {key: (1-e) * value for key, value in p.items()}
    for k in range(1, L+1):
        q[k, 0] = q.get((k, 0), F(0)) + e / L
    distance = sum(abs(q.get(key, F(0))-p.get(key, F(0)))
                   for key in set(q) | set(p)) / 2
    continuity_rhs = float(distance) * log(L) + h2(distance)
    continuity_lhs = abs(conditional_entropy(q)-hcond)
    assert continuity_lhs <= continuity_rhs + 1e-11
    observations.append({
        "D": D, "L": L, "w": w,
        "mean_K_minus_J_exact": str(mean_gap),
        "mean_upper_bound_exact": str(bound),
        "H_K_given_J_nats": hcond,
        "geometric_entropy_bound_nats": g(bound),
        "one_way_event_a": a,
        "target_event_probability_exact": str(event_prob),
        "target_event_probability_floor_exact": str(event_floor),
        "independent_event_probability_exact": str(independent_event),
        "independent_event_ceiling_exact": str(independent_ceiling),
        "continuity_test_distance_exact": str(distance),
        "continuity_test_lhs_nats": continuity_lhs,
        "continuity_test_rhs_nats": continuity_rhs,
        "status": "PASS",
    })

result = {
    "status": "PASS", "cases": len(CASES), "observations": observations,
    "proof_scope": "Exact rational target laws and mean checks; floating entropy admissions only",
    "cpu_seconds": time.process_time() - START_CPU,
    "wall_seconds": time.perf_counter() - START_WALL,
    "quantum_optimization_jobs": 0,
}
Path(__file__).with_name("RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: result[key] for key in ["status", "cases", "cpu_seconds", "wall_seconds"]}))
