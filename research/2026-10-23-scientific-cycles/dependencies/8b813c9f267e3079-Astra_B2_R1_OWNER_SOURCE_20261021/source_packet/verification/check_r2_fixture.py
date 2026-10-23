#!/usr/bin/env python3
"""Exact rational checks of a NEW six-state equilibrium fixture.

Only finite algebra is checked. This is not a proof verifier for the universal
operator inequality, a novelty check, or an experimental inference procedure.
Uses only the Python standard library. Run from any directory.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math


def matmul(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def add(*terms):
    return [[sum((c*m[i][j] for c, m in terms), F(0))
             for j in range(len(terms[0][1][0]))]
            for i in range(len(terms[0][1]))]


def visible(t, pi, labels):
    p = [sum((pi[x] for x in range(len(pi)) if labels[x] == i), F(0))
         for i in range(4)]
    return [[sum((pi[x]*t[x][y]
                  for x in range(len(pi)) for y in range(len(pi))
                  if labels[x] == i and labels[y] == j), F(0))/p[i]
             for j in range(4)] for i in range(4)]


def main():
    # State order: (+,1),(+,3),(+,4),(-,2),(-,3),(-,4).
    labels = [0, 2, 3, 1, 2, 3]
    r = [F(1, 2), F(1, 4), F(1, 4)]
    pi = [x/2 for x in r]*2
    i6 = eye(6)
    block_reset = [[r[j % 3] if i//3 == j//3 else F(0)
                    for j in range(6)] for i in range(6)]
    global_reset = [pi[:] for _ in range(6)]
    assert matmul(block_reset, block_reset) == block_reset
    assert matmul(global_reset, global_reset) == global_reset
    assert matmul(block_reset, global_reset) == global_reset
    assert matmul(global_reset, block_reset) == global_reset
    # G = beta*(block_reset-I) + gamma*(global_reset-I), where
    # beta=log(9/2)/tau, gamma=log(10/9)/tau. Both terms obey balance.
    for reset in (block_reset, global_reset):
        for i in range(6):
            assert sum(reset[i], F(0)) == 1
            for j in range(6):
                assert pi[i]*reset[i][j] == pi[j]*reset[j][i]
    assert all(pi)  # global reset has strictly positive off-diagonal rates.
    a, delta = F(9, 10), F(2, 9)
    t1 = add((a*delta, i6), (a*(1-delta), block_reset),
             (1-a, global_reset))
    t2 = add((a*a*delta*delta, i6),
             (a*a*(1-delta*delta), block_reset),
             (1-a*a, global_reset))
    assert matmul(t1, t1) == t2
    p = visible(t1, pi, labels)
    target = [[F(23,40), F(1,40), F(1,5), F(1,5)],
              [F(1,40), F(23,40), F(1,5), F(1,5)],
              [F(1,5), F(1,5), F(2,5), F(1,5)],
              [F(1,5), F(1,5), F(1,5), F(2,5)]]
    assert p == target
    k = visible(t2, pi, labels)
    d = add((F(1), k), (F(-1), matmul(p, p)))
    v = [1, -1, 0, 0]
    expected_d = [[F(49,800)*x*y for y in v] for x in v]
    assert d == expected_d
    trace = sum((d[i][i] for i in range(4)), F(0))
    assert trace == F(49,400)
    for vector, eigenvalue in [([1,1,1,1], F(1)),
                              ([1,-1,0,0], F(11,20)),
                              ([0,0,1,-1], F(1,5)),
                              ([1,1,-1,-1], F(1,5))]:
        assert [sum((p[i][j]*vector[j] for j in range(4)), F(0))
                for i in range(4)] == [eigenvalue*x for x in vector]
    lower = (math.sqrt(11)-math.sqrt(5)-1)/25
    result = {
        "scope": "exact finite rational identities; universal inequality is analytic",
        "status": "PASS",
        "hidden_states": 6,
        "irreducible": True,
        "reversible": True,
        "pi": [str(x) for x in pi],
        "labels_one_based": [x+1 for x in labels],
        "beta_times_tau": "log(9/2)",
        "gamma_times_tau": "log(10/9)",
        "P": [[str(x) for x in row] for row in p],
        "K": [[str(x) for x in row] for row in k],
        "D": [[str(x) for x in row] for row in d],
        "trace_D_exact": str(trace),
        "universal_trace_lower_expression": "(sqrt(11)-sqrt(5)-1)/25",
        "universal_trace_lower_decimal_diagnostic": lower,
        "explicit_trace_upper_exact": "49/400",
        "stationary_entropy_production": "exactly zero by detailed balance",
        "novelty": "UNKNOWN; compare with existing Astra two-lag owner"
    }
    dest = Path(__file__).with_name("r2_fixture_result.json")
    dest.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
