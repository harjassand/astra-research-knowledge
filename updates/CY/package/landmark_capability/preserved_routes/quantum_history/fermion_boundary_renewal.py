#!/usr/bin/env python3
"""Exact sparse-detector renewal on a number-conserving free-fermion circuit.

One-particle V is compiled from local rational two-mode rotations. Its
m-particle kernel is a Slater minor det((V^t)[A,B]). Sparse configuration
monitoring is not Gaussian, yet first-hit amplitudes close on k targets.
Small cases are compared with direct exterior-power state evolution.
"""

from fractions import Fraction
from itertools import combinations
import json
import sys
import time


def eye(n):
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def matmul(a, b):
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n)), Fraction())
             for j in range(n)] for i in range(n)]


def one_particle_circuit(n, sweeps=2):
    v = eye(n)
    a, b = Fraction(3, 5), Fraction(4, 5)
    gates = []
    for _ in range(sweeps):
        gates.extend(range(n - 1))
        gates.extend(range(n - 2, -1, -1))
    for i in gates:
        old_i, old_j = v[i], v[i + 1]
        v[i] = [a * x - b * y for x, y in zip(old_i, old_j)]
        v[i + 1] = [b * x + a * y for x, y in zip(old_i, old_j)]
    return v, len(gates)


def determinant(a):
    n = len(a)
    if n == 0:
        return Fraction(1)
    x = [list(row) for row in a]
    sign = 1
    product = Fraction(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if x[i][j]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != j:
            x[j], x[pivot] = x[pivot], x[j]
            sign = -sign
        p = x[j][j]
        product *= p
        for i in range(j + 1, n):
            scale = x[i][j] / p
            for col in range(j + 1, n):
                x[i][col] -= scale * x[j][col]
            x[i][j] = 0
    return sign * product


def slater_kernel(v, target, source):
    return determinant([[v[i][j] for j in source] for i in target])


def free_powers(v, horizon):
    result = [eye(len(v))]
    for _ in range(horizon):
        result.append(matmul(v, result[-1]))
    return result


def renewal(v, start, targets, horizon):
    powers = free_powers(v, horizon)
    k = len(targets)
    g = [None] + [[slater_kernel(powers[t], a, start) for a in targets]
                  for t in range(1, horizon + 1)]
    h = [None] + [[[slater_kernel(powers[t], a, b) for b in targets]
                   for a in targets] for t in range(1, horizon + 1)]
    f = [[Fraction(0)] * k for _ in range(horizon + 1)]
    p = []
    for t in range(1, horizon + 1):
        for a in range(k):
            f[t][a] = g[t][a] - sum(
                (h[t - s][a][b] * f[s][b]
                 for s in range(1, t) for b in range(k)), Fraction())
        p.append(sum((z * z for z in f[t]), Fraction()))
    return f[1:], p


def direct(v, start, targets, horizon):
    n, m = len(v), len(start)
    basis = list(combinations(range(n), m))
    index = {config: i for i, config in enumerate(basis)}
    dim = len(basis)
    fock = [[slater_kernel(v, a, b) for b in basis] for a in basis]
    state = [Fraction(0)] * dim
    state[index[start]] = Fraction(1)
    f, p = [], []
    for _ in range(horizon):
        state = [sum((fock[i][j] * state[j] for j in range(dim)), Fraction())
                 for i in range(dim)]
        hit = [state[index[a]] for a in targets]
        f.append(hit)
        p.append(sum((z * z for z in hit), Fraction()))
        for a in targets:
            state[index[a]] = Fraction(0)
    return f, p


def fixture(n, m, targets, horizon):
    v, gate_count = one_particle_circuit(n)
    start = tuple(range(m))
    boundary_f, boundary_p = renewal(v, start, targets, horizon)
    direct_f, direct_p = direct(v, start, targets, horizon)
    assert boundary_f == direct_f
    assert boundary_p == direct_p
    return {
        "n_modes": n,
        "particles": m,
        "local_two_mode_gates_per_step": gate_count,
        "fock_sector_dimension": len(list(combinations(range(n), m))),
        "detector_boundary_dimension": len(targets),
        "horizon": horizon,
        "exact_amplitude_and_probability_agreement": True,
        "first_detection_probabilities": [str(x) for x in boundary_p],
    }


if __name__ == "__main__":
    if sys.argv[1:] == ["--entanglement-check"]:
        n, m = 8, 4
        v, gates = one_particle_circuit(n, sweeps=4)
        occupied_columns = tuple(range(m))
        minors = [slater_kernel(v, cut, occupied_columns)
                  for cut in combinations(range(n), m)]
        assert all(minors)
        print(json.dumps({
            "n_modes": n,
            "particles": m,
            "local_two_mode_gates": gates,
            "balanced_bipartitions_checked": len(minors),
            "nonzero_balanced_minors": sum(bool(x) for x in minors),
            "exact_schmidt_rank_across_every_balanced_cut": 1 << m,
            "scope": "single free-evolved Slater state; not a tensor-network lower bound",
        }, indent=2))
    elif sys.argv[1:] == ["--benchmark"]:
        n, m, horizon = 16, 8, 6
        v, gates = one_particle_circuit(n)
        start = tuple(range(m))
        targets = [tuple(range(8, 16)), tuple(range(0, 16, 2))]
        tic = time.perf_counter()
        _, probabilities = renewal(v, start, targets, horizon)
        elapsed = time.perf_counter() - tic
        total = sum(probabilities, Fraction())
        print(json.dumps({
            "n_modes": n,
            "particles": m,
            "fock_sector_dimension": len(list(combinations(range(n), m))),
            "local_two_mode_gates_per_step": gates,
            "boundary_dimension": len(targets),
            "horizon": horizon,
            "elapsed_seconds_local_observation": round(elapsed, 6),
            "cumulative_probability_numerator_bits": total.numerator.bit_length(),
            "cumulative_probability_denominator_bits": total.denominator.bit_length(),
            "nonzero_first_detection_steps": sum(bool(x) for x in probabilities),
        }, indent=2))
    else:
        cases = [
            (4, 2, [(2, 3), (0, 2)], 3),
            (6, 3, [(3, 4, 5), (0, 2, 4)], 4),
        ]
        print(json.dumps([fixture(*case) for case in cases], indent=2))
