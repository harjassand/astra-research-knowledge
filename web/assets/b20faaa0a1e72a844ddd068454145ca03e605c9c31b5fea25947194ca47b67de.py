"""Exact checks for the selective tensor note. No upstream code is executed."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import json
from pathlib import Path


def solve(a, b):
    a = [list(row) + [rhs] for row, rhs in zip(a, b)]
    n = len(a)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        z = a[j][j]
        a[j] = [v / z for v in a[j]]
        for i in range(n):
            if i != j:
                z = a[i][j]
                a[i] = [x - z * y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


def spectral_lp(alpha=None):
    # Coordinates are p_X, p_Y, p_Z, u, with u <= min(15/8, p_X+p_Y).
    constraints = []
    for j in range(4):
        a = [Q(0)] * 4
        a[j] = Q(-1)
        constraints.append((a, Q(0)))
    for j in range(3):
        a = [Q(0)] * 4
        a[j] = Q(1)
        constraints.append((a, Q(1)))
    constraints += [([Q(0), Q(0), Q(0), Q(1)], Q(15, 8)),
                    ([Q(-1), Q(-1), Q(0), Q(1)], Q(0)),
                    ([Q(1), Q(1), Q(1), Q(0)], Q(9, 4))]
    if alpha is not None:
        for j in range(3):
            a = [Q(1), Q(1), Q(1), Q(0)]
            a[j] = alpha
            constraints.append((a, Q(2)))
    vertices = []
    for subset in combinations(constraints, 4):
        point = solve([x[0] for x in subset], [x[1] for x in subset])
        if point is None:
            continue
        if all(sum(x*y for x, y in zip(a, point)) <= b
               for a, b in constraints):
            vertices.append(point)
    maximum = max(point[3] + point[2]/4 for point in vertices)
    witness = next(point for point in vertices if point[3]+point[2]/4 == maximum)
    return {"upper_bound": str(maximum), "feasible_vertex": list(map(str, witness)),
            "vertex_count_with_duplicates": len(vertices)}


def pruning_fixture(k):
    # Actual <16,2,16> scheme: 64 independent <2,2,2> Strassen schemes.
    # There are 320 base leaves with output support 2 and 128 with support 1.
    assert k % 2 == 0
    cutoff = k // 2  # N^(-1/8)=16^(-k/8)=2^(-k/2).
    total = 0
    for t in range(k + 1):
        count = comb(k, t) * 320**t * 128**(k-t)
        total += count * min(Q(2)**(t-cutoff), Q(1))
    return {"power": k, "incidence_proxy": str(total),
            "leaf_count": str(448**k), "proxy_fraction": str(Q(total, 448**k))}


omega = spectral_lp()
dual = spectral_lp(Q(93, 200))
assert omega["upper_bound"] == "63/32"
assert dual["upper_bound"] == "1445/744"
assert Q(2) - Q(1445, 744) == Q(43, 744)
assert Q(5, 7) * Q(1, 4) > Q(1, 8)

# Exact large finite illustration of the counting inequality, for K <= N^100.
# N=2^256, D=2^64, m=2^480, C=2^508, eta=1/64.
# (N+1)^(U+V) K <= 2^(257*2^445 + 25600).
# (N^2/C)^m = 2^(4*2^480).
counting_left = 257 * 2**445 + 25600
counting_right = 4 * 2**480
assert counting_left < counting_right

result = {
    "status": "exact finite checks; no target algorithm or rank kernel acquired",
    "omega_only_spectral_polytope": omega,
    "dual_spectral_polytope": dual,
    "counting_finite_illustration": {
        "N": "2^256", "eta": "1/64", "K_bound": "N^100",
        "base2_log_upper_family_factor": str(counting_left),
        "base2_log_lower_binomial_ratio": str(counting_right), "passes": True},
    "actual_blocked_strassen_pruning": [pruning_fixture(k) for k in [2, 4, 8, 16, 32]],
}
path = Path(__file__).with_name("selective_tensor_checks.json")
path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"omega": omega["upper_bound"], "dual": dual["upper_bound"],
                  "counting": True, "pruning_cases": 5, "output": str(path)}))
