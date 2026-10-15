#!/usr/bin/env python3
"""Read-only independent synthetic audit; writes only its own receipt."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def reachable(vertices, edges, start):
    reached = {start}
    pending = [start]
    while pending:
        v = pending.pop()
        for tail, head in edges:
            if tail == v and head not in reached:
                reached.add(head)
                pending.append(head)
    return reached


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def vm(p, P):
    return [sum(p[i] * P[i][j] for i in range(len(p))) for j in range(len(p))]


def phase(sp, h):
    P = [[F(i == j) for j in range(3)] for i in range(3)]
    P[0][sp] = h / 2
    P[0][0] = 1 - h / 2
    P[sp][0] = (1 - h) / 2
    P[sp][sp] = 1 - (1 - h) / 2
    return P


def strings(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {k: strings(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [strings(x) for x in v]
    return v


def main():
    # Root graph edge order: 0->1, 1->0, loop1, idle0.
    edges = [(0, 1), (1, 0), (1, 1), (0, 0)]
    salt = [F(1), F(0), F(0), F(0)]
    output = [F(0), F(0), F(1), F(0)]
    times = [F(1)] * 4
    assert all(reachable({0, 1}, edges, v) == {0, 1} for v in (0, 1))
    f = [F(0), F(0), F(1), F(0)]
    assert sum(a * b for a, b in zip(salt, f)) == 0
    assert sum(a * b for a, b in zip(times, f)) == 1
    assert sum(a * b for a, b in zip(output, f)) == 1
    assert all(x <= t for x, t in zip(output, times))  # tau=1,u=kappa=0.
    finite_count_cases = 0
    for a, b, c, d in product(range(7), repeat=4):
        if a != b:
            continue
        if c > 0 and a == 0:
            continue  # Disconnected support is not a legal reset-0 walk.
        if a == 0:
            assert c == 0
        if c > 0:
            assert a >= 1
        finite_count_cases += 1
    closure_samples = []
    for N in (1, 10, 100, 1000):
        freq = [F(1, N + 2), F(1, N + 2), F(N, N + 2), F(0)]
        assert freq[0] == freq[1]
        assert sum(freq) == 1
        closure_samples.append({"N": N, "salt_rate": freq[0], "exchange_rate": freq[2]})

    # Hidden chloride correction counterexample.
    true_x, true_s, h_x, h_s = F(1), F(1), F(0), F(-1)
    kappa, tau, potential_span = F(1), F(0), F(0)
    observed_s, observed_x = true_s + h_s, true_x + h_x
    old_bound = abs(kappa) * abs(observed_s) + potential_span + abs(h_x) + tau
    corrected_bound = old_bound + abs(kappa) * abs(h_s)
    assert true_x <= kappa * true_s
    assert observed_x > old_bound and observed_x <= corrected_bound

    # Exact support of each robust x/s rectangle.
    box_cases = 0
    for k in (F(-3), F(-1, 2), F(0), F(2)):
        xhat, shat, ex, es = F(7, 3), F(-5, 4), F(2, 7), F(3, 8)
        corner_max = max(x - k * s for x, s in product((xhat - ex, xhat + ex), (shat - es, shat + es)))
        formula = xhat - k * shat + ex + abs(k) * es
        assert corner_max == formula
        box_cases += 1

    # Independent reconstruction of the stochastic four-phase worker fixture.
    phases = [phase(1, F(3, 4)), phase(1, F(1, 4)), phase(2, F(3, 4)), phase(2, F(1, 4))]
    P = [[F(i == j) for j in range(3)] for i in range(3)]
    for phase_P in phases:
        P = mm(P, phase_P)
    expected_P = [
        [F(121, 256), F(5, 16), F(55, 256)],
        [F(77, 256), F(9, 16), F(35, 256)],
        [F(7, 16), F(0), F(9, 16)],
    ]
    assert P == expected_P
    pi = [F(7, 17), F(5, 17), F(5, 17)]
    assert vm(pi, P) == pi
    p = pi
    q_Li, q_Na = F(0), F(0)
    trace = [p]
    for j, phase_P in enumerate(phases):
        p_next = vm(p, phase_P)
        if j == 1:
            q_Li -= p_next[1] - p[1]
        if j == 2:
            q_Na -= p_next[2] - p[2]
        p = p_next
        trace.append(p)
    assert p == pi
    assert q_Li == F(2, 17) and q_Na == F(-2, 17)
    dobrushin = max(sum(abs(x - y) for x, y in zip(a, b)) / 2 for a, b in product(P, repeat=2))
    assert dobrushin == F(9, 16)
    vertices = {(j, state) for j in range(4) for state in range(3)}
    phase_edges = [((j, state), ((j + 1) % 4, target)) for j, phase_P in enumerate(phases) for state in range(3) for target in range(3) if phase_P[state][target] > 0]
    assert all(reachable(vertices, phase_edges, v) == vertices for v in vertices)

    # Stationary occupation does not imply reachability from a fixed reset.
    absorbing_edges = [(0, 0), (1, 1)]
    assert reachable({0, 1}, absorbing_edges, 0) == {0}
    invariant_mu = [F(0), F(1)]
    identity = [[F(1), F(0)], [F(0), F(1)]]
    assert vm(invariant_mu, identity) == invariant_mu

    result = {
        "status": "PASS_SYNTHETIC_AUDIT_ONLY",
        "root_exact_zero_graph": {"reset_component_strongly_connected": True, "primal_rate": F(1), "dual_tau": F(1), "enumerated_legal_count_cases": finite_count_cases, "closure_samples": closure_samples},
        "hidden_salt_correction": {"observed_exchange": observed_x, "observed_salt": observed_s, "bound_without_hidden_salt": old_bound, "bound_with_hidden_salt": corrected_bound},
        "robust_box_corner_cases": box_cases,
        "worker_four_phase_fixture": {"P": P, "pi": pi, "trace": trace, "Li_right": q_Li, "Na_right": q_Na, "dobrushin": dobrushin, "phase_augmented_vertices": len(vertices), "phase_augmented_edges": len(phase_edges), "phase_augmented_graph_strongly_connected": True},
        "occupation_measure_reachability_counterexample": {"reset_0_reachable": [0], "invariant_mass_at_1": True},
        "physical_validation": False,
        "limitations": ["Graph and kernels supplied/synthetic", "No acquired species response or storage capacity", "No broad literature priority audit"],
    }
    path = Path(__file__).with_name("AUDIT_RESULTS.json")
    path.write_text(json.dumps(strings(result), indent=2) + "\n")
    print(json.dumps({"status": result["status"], "output": str(path)}))


if __name__ == "__main__":
    main()
