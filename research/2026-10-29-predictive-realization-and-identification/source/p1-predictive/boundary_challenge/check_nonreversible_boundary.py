#!/usr/bin/env python3
"""Exact nonreversible realization obstruction and phase-time controls.

All inputs are supplied rational sources. No trajectory/source observations.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import time

from check_passive_equivalence import F, sp, matrix_block, killed_mean, passive_mean, encode


def directed_laplacian(n, edges):
    L = sp.zeros(n)
    for i, j, f in edges:
        assert i != j and f > 0
        L[i, i] += f
        L[i, j] -= f
    assert L * sp.ones(n, 1) == sp.zeros(n, 1)
    assert L.T * sp.ones(n, 1) == sp.zeros(n, 1)
    return L


def nr_record(L, w):
    B, I = [0, 1], list(range(2, len(w)))
    G = matrix_block(L, I, I)
    X = matrix_block(L, B, I)
    Y = matrix_block(L, I, B)
    wi, wb = matrix_block(w, I, [0]), matrix_block(w, B, [0])
    Gi = G.inv()
    S = matrix_block(L, B, B) - X * Gi * Y
    bR = wb - X * Gi * wi
    bL = wb - Y.T * Gi.T * wi
    c = (wi.T * Gi * wi)[0]
    assert sum(bR) == sum(bL) == sum(w)
    assert all(x >= 0 for x in bR - wb) and all(x >= 0 for x in bL - wb)
    return S, bR, bL, c, G


def erlang_cycle(n, flow=F(1)):
    states = [0] + list(range(2, n + 2)) + [1, 0]
    L = directed_laplacian(n + 2, [(i, j, flow) for i, j in zip(states, states[1:])])
    w = sp.Matrix([F(1), F(1)] + [F(1, n)] * n)
    return L, w


def simple_path(flow, start, absorber):
    def dfs(v, seen):
        if v == absorber:
            return []
        for j in range(absorber + 1):
            if j not in seen and flow[v][j] > 0:
                tail = dfs(j, seen | {j})
                if tail is not None:
                    return [(v, j)] + tail
        return None
    return dfs(start, {start})


def verify_phase_flow_inequality(T, alpha):
    """Verify algebra and path decomposition, including arbitrary cycles."""
    k = T.rows
    N = (-T).inv()
    h = N * sp.ones(k, 1)
    d = [-sum(T[i, j] for j in range(k)) for i in range(k)]
    assert all(x > 0 for x in d)
    total_paths = 0
    for start in range(k):
        nu = matrix_block(N, [start], range(k))
        flow = [[F(0) for _ in range(k + 1)] for _ in range(k + 1)]
        for i in range(k):
            for j in range(k):
                if i != j:
                    flow[i][j] = nu[i] * T[i, j]
            flow[i][k] = nu[i] * d[i]
        potential = list(h) + [F(0)]
        energy = sum(flow[i][j] * (potential[i] - potential[j]) ** 2 for i in range(k) for j in range(k + 1))
        second = 2 * (N * h)[start]
        variance = second - h[start] ** 2
        assert energy == variance
        path_mass, path_energy = F(0), F(0)
        while path_mass < 1:
            path = simple_path(flow, start, k)
            assert path is not None and 1 <= len(path) <= k
            mass = min(flow[i][j] for i, j in path)
            cost = sum((potential[i] - potential[j]) ** 2 for i, j in path)
            assert cost >= h[start] ** 2 / k
            for i, j in path:
                flow[i][j] -= mass
                assert flow[i][j] >= 0
            path_mass += mass
            path_energy += mass * cost
            total_paths += 1
        assert path_mass == 1 and energy >= path_energy >= h[start] ** 2 / k
    mean = (alpha * h)[0]
    second = 2 * (alpha * N * h)[0]
    assert second >= (1 + F(1, k)) * mean * mean
    return mean, second, total_paths


def phase_channel(k, fraction):
    """Cyclic mixed-entry hidden channel with trace throughflux f<=1."""
    T = sp.zeros(k)
    for i in range(k):
        for j in range(k):
            if i != j:
                T[i, j] = F((i + 2 * j) % 5 + 1, k + 3)
        exit_rate = F(i + 1, k + 2)
        T[i, i] = -exit_rate - sum(T[i, j] for j in range(k) if j != i)
    alpha = sp.Matrix([[F(i + 1, k * (k + 1) // 2) for i in range(k)]])
    N0 = (-T).inv()
    mean0 = (alpha * N0 * sp.ones(k, 1))[0]
    T = T * (fraction * mean0)
    N = (-T).inv()
    wi_row = fraction * alpha * N
    wi = sp.Matrix(list(wi_row))
    assert sum(wi) == 1 and all(x > 0 for x in wi)
    w = sp.Matrix([1, 1] + list(wi))
    L = sp.zeros(k + 2)
    L[0, 0], L[1, 1], L[1, 0] = 1, 1, -1
    L[0, 1] = -(1 - fraction)
    G = sp.diag(*list(wi)) * (-T)
    L[2:, 2:] = G
    for i in range(k):
        L[0, i + 2] = -fraction * alpha[i]
        L[i + 2, 1] = -wi[i] * (-sum(T[i, j] for j in range(k)))
    assert L * sp.ones(k + 2, 1) == sp.zeros(k + 2, 1)
    assert L.T * sp.ones(k + 2, 1) == sp.zeros(k + 2, 1)
    return L, w, T, alpha


def main():
    started = time.perf_counter()
    S0 = sp.Matrix([[1, -1], [-1, 1]])
    cycle_results = []
    for n in [1, 2, 3, 5, 8, 16, 32]:
        for flow in [F(1), F(1, n)]:
            L, w = erlang_cycle(n, flow)
            S, bR, bL, c, G = nr_record(L, w)
            assert S == flow * S0
            assert bR == sp.Matrix([2, 1]) and bL == sp.Matrix([1, 2])
            assert c == F(n + 1, 2 * n) / flow
            assert sum(w) == 3
            N = G.inv() * sp.diag(*list(w)[2:])
            mean = (N * sp.ones(n, 1))[0]
            second = 2 * (N * N * sp.ones(n, 1))[0]
            assert mean == 1 / flow and second == (1 + F(1, n)) / flow ** 2
            assert c == flow * second / 2
            assert math.ceil(1 / (2 * flow * c - 1)) == n
            Ttarget = killed_mean(L, w, {1})
            assert Ttarget == (F(5, 4) + F(1, 4 * n)) / flow
            native_max = max(L[i, i] / w[i] for i in range(len(w)))
            if flow == F(1, n):
                assert native_max == 1
            cycle_results.append({"hidden_phases": n, "total_states": n + 2, "cycle_flow": flow, "S": S, "bR": bR, "bL": bL, "c": c, "hidden_duration_mean": mean, "hidden_duration_second_moment": second, "minimum_hidden_states_from_bound": n, "equilibrium_mean_to_port_1": Ttarget, "max_native_exit_rate": native_max})

    phase_results = []
    flow_paths = 0
    for k in range(1, 7):
        for fraction in [F(1), F(1, 2), F(1, 4)]:
            L, w, T, alpha = phase_channel(k, fraction)
            S, bR, bL, c, G = nr_record(L, w)
            assert S == S0 and bR == sp.Matrix([2, 1]) and bL == sp.Matrix([1, 2])
            mean, second, paths = verify_phase_flow_inequality(T, alpha)
            flow_paths += paths
            assert mean == 1 / fraction and c == fraction * second / 2
            lower = (1 + F(1, k)) / (2 * fraction)
            assert c >= lower
            a = [-L[0, i + 2] for i in range(k)]
            assert sum(a) == fraction <= 1
            assert sp.Matrix([a]) == sp.ones(k, 1).T * G
            phase_results.append({"phases": k, "throughflux": fraction, "c": c, "phase_lower_bound": lower, "phase_cv_squared": (second - mean * mean) / (mean * mean), "flow_decomposition_paths": paths})

    # Seven actual full-matrix scalar passive means identify the record up
    # to time reversal. These are supplied solves, not acquired samples.
    passive_results = []
    passive_solves = 0
    for n in [1, 3, 8, 16]:
        L, w = erlang_cycle(n)
        t1, t2, g = F(1), F(2), [F(1), F(1)]
        cache = {}
        def Fprobe(t, z):
            nonlocal passive_solves
            key = (t, tuple(z))
            if key not in cache:
                Tmean = passive_mean(L, w, [0, 1], t, z, g)
                Treverse = passive_mean(L.T, w, [0, 1], t, z, g)
                assert Tmean == Treverse
                passive_solves += 2
                cache[key] = (3 + sum(z)) * Tmean - sum(zi * zi for zi in z)
            return cache[key]
        f0 = Fprobe(t1, [0, 0])
        M, lin, singles = sp.zeros(2), sp.zeros(2, 1), []
        for i in range(2):
            z = [F(0), F(0)]
            z[i] = 1
            f1 = Fprobe(t1, z)
            singles.append(f1)
            z[i] = 2
            f2 = Fprobe(t1, z)
            M[i, i] = (f2 - 2 * f1 + f0) / 2
            lin[i] = f1 - f0 - M[i, i]
        M[0, 1] = M[1, 0] = (Fprobe(t1, [1, 1]) - singles[0] - singles[1] + f0) / 2
        assert M.inv() - t1 * sp.eye(2) == S0
        assert M.inv() * lin == sp.Matrix([3, 3])
        A1 = f0 - F(9, 2) / t1
        A2 = Fprobe(t2, [0, 0]) - F(9, 2) / t2
        delta_squared = (A2 - A1) / (2 * (1 / (t1 + 2) - 1 / (t2 + 2)))
        recovered_c = A1 + 2 * delta_squared / (t1 + 2)
        assert delta_squared == F(1, 4)
        assert recovered_c == F(n + 1, 2 * n)
        assert len(cache) == 7
        passive_results.append({"hidden_phases": n, "distinct_passive_probes": len(cache), "recovered_c": recovered_c, "recovered_delta_squared": delta_squared, "time_reverse_means_identical": True})

    approximate_controls = []
    for n in [8, 16, 32]:
        for k in [1, 2, 4, 8]:
            if k > n:
                continue
            cn, ck = F(n + 1, 2 * n), F(k + 1, 2 * k)
            eps = ck - cn
            assert eps >= 0 and eps <= F(1, 2 * k)
            assert 1 / (F(1, n) + 2 * eps) == k
            approximate_controls.append({"original_phases": n, "replacement_phases": k, "exact_c_error": eps, "hidden_state_lower_bound_with_that_error": k})

    result = {
        "status": "PASS",
        "arithmetic": "fractions.Fraction; no floating assertions",
        "scope": "finite supplied-generator controls of general ordinary proofs",
        "source_observations": 0,
        "physical_preparations": 0,
        "cycle_records": cycle_results,
        "cyclic_mixed_entry_phase_checks": phase_results,
        "total_deterministic_start_flow_paths_decomposed": flow_paths,
        "scalar_passive_probe_controls": passive_results,
        "full_forward_reverse_passive_solves": passive_solves,
        "fixed_error_controls": approximate_controls,
        "wall_seconds": time.perf_counter() - started,
        "not_claimed": ["cheap acquisition of small variance/residual differences", "fixed-error impossibility", "lower bound on memory bits", "lower bound against direct record evaluation or semi-Markov delays", "new phase-type variance inequality"],
    }
    destination = Path(__file__).with_name("NONREVERSIBLE_BOUNDARY_CHECKS.json")
    destination.write_text(json.dumps(encode(result), indent=2) + "\n")
    print(json.dumps({"status": result["status"], "cycle_records": len(cycle_results), "mixed_phase_cases": len(phase_results), "flow_paths": flow_paths, "passive_solves": passive_solves, "fixed_error_controls": len(approximate_controls), "wall_seconds": result["wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
