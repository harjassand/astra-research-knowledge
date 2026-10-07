"""Exact bounded checks for the hard two-replica/parity interface."""
from itertools import combinations, permutations
from math import prod
import json
from pathlib import Path


def determinant(a):
    m = len(a)
    if m == 0:
        return 1
    total = 0
    for p in permutations(range(m)):
        inversions = sum(p[i] > p[j] for i in range(m) for j in range(i + 1, m))
        total += (-1 if inversions % 2 else 1) * prod(a[i][p[i]] for i in range(m))
    return total


def directed_cycle_support(q):
    n = 2 * q
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        F[i][(i + 1) % n] = 1
    support = []
    for I in combinations(range(n), q):
        J = tuple(i for i in range(n) if i not in I)
        minor = determinant([[F[i][j] for j in J] for i in I])
        if minor:
            support.append((I, J, minor))
    return support


rows = []
for q in range(2, 6):
    support = directed_cycle_support(q)
    expected = [tuple(range(0, 2*q, 2)), tuple(range(1, 2*q, 2))]
    assert sorted(s[0] for s in support) == sorted(expected)
    assert all(abs(s[2]) == 1 for s in support)
    assert len(set(s[0][i] != s[1][i] for s in support for i in range(q))) == 1
    rows.append({"q": q, "n": 2*q, "positive_states": len(support),
                 "I_supports": [list(s[0]) for s in support],
                 "amplitudes": [s[2] for s in support],
                 "Hamming_distance": q})

out = {"scope": "exact checks for directed permutation cycles, q=2..5",
       "result": "PASS", "instances": rows,
       "claim_limit": "finite arithmetic corroborates the universal cycle argument in INITIAL.txt; it is not a mixing lower bound after positive auxiliary edges are added"}
Path("work/cycle6/c01_l09/initial_checks.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
