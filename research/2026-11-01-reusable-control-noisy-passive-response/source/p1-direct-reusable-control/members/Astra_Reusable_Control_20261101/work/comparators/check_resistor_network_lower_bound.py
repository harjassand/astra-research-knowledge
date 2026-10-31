#!/usr/bin/env python3
"""Literal exact Kirchhoff checks for the root's passive-circuit lower bound.

All assertion decisions use fractions. The full source solve uses n+1 internal
node voltages and the rail-current equation, not the reduced response formula.
The latter is computed separately for comparison.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json

from check_intervention_lower_bound import determinant, solve, response


def circuit(n, kappa, final_rail):
    assert n >= 2
    s = 2 / kappa
    a = [Q(0)] + [Q(1, 2)] * (n - 1) + [Q(final_rail)]
    to_one = [s * x for x in a]
    to_zero = [s * (1 - x) for x in a]
    assert all(x >= 0 for x in to_one + to_zero)
    assert all(x + y == s for x, y in zip(to_one, to_zero))
    return s, a, to_one, to_zero


def literal_current(n, kappa, final_rail, u):
    s, a, to_one, to_zero = circuit(n, kappa, final_rail)
    h = [[s if i == j else Q(0) for j in range(n + 1)] for i in range(n + 1)]
    for i, ui in enumerate(u):
        h[i][i] += ui
        h[i + 1][i + 1] += ui
        h[i][i + 1] -= ui
        h[i + 1][i] -= ui
    x = solve(h, to_one)
    current = sum(c * (1 - xx) for c, xx in zip(to_one, x))
    dissipation = sum(c1 * (xx - 1)**2 + c0 * xx**2
                      for c1, c0, xx in zip(to_one, to_zero, x))
    dissipation += sum(ui * (x[i+1] - x[i])**2 for i, ui in enumerate(u))
    assert current == dissipation
    assert all(0 <= xx <= 1 for xx in x)
    return current


def reduced(n, kappa, final_rail, u):
    s, a, _, _ = circuit(n, kappa, final_rail)
    e = [[Q(j == i+1)-Q(j == i) for j in range(n + 1)] for i in range(n)]
    b = [[sum(e[i][j] * e[k][j] for j in range(n+1)) / s
          for k in range(n)] for i in range(n)]
    assert all(b[i][j] == (kappa if i == j else -kappa/2 if abs(i-j) == 1 else 0)
               for i in range(n) for j in range(n))
    g = [sum(e[i][j] * a[j] for j in range(n+1)) for i in range(n)]
    assert g == [Q(1,2)] + [Q(0)]*(n-2) + [Q(final_rail)-Q(1,2)]
    c0 = sum(s*aj*(1-aj) for aj in a)
    assert c0 == Q(n-1, 2) / kappa
    return c0 + response(b, g, u)


def main():
    counts = {"proper_support_equalities": 0, "literal_reduced_equalities": 0,
              "baseline_equalities": 0, "dense_gap_equalities": 0,
              "rational_gap_lower_bounds": 0, "strict_psd_leading_minors": 0}
    rows = []
    for n in range(2, 9):
        dose, kappa = Q(1, 5), Q(1)
        for size in range(n):
            for support in combinations(range(n), size):
                for pattern in [0, 1]:
                    u = [Q(0)] * n
                    for i in support:
                        u[i] = dose/n if pattern == 0 else dose*(i+1)/(n*(n+1))
                    assert sum(u) <= dose
                    ca = literal_current(n, kappa, 0, u)
                    cb = literal_current(n, kappa, 1, u)
                    assert ca == cb
                    counts["proper_support_equalities"] += 1
                    assert ca == reduced(n, kappa, 0, u)
                    assert cb == reduced(n, kappa, 1, u)
                    counts["literal_reduced_equalities"] += 2
    for n in range(2, 11):
        for kappa in [Q(1), Q(2), Q(3,5)]:
            b = [[kappa if i == j else -kappa/2 if abs(i-j)==1 else Q(0)
                  for j in range(n)] for i in range(n)]
            for j in range(1, n+1):
                assert determinant([row[:j] for row in b[:j]]) > 0
                counts["strict_psd_leading_minors"] += 1
            for final_rail in [0, 1]:
                baseline = literal_current(n, kappa, final_rail, [Q(0)] * n)
                assert baseline == Q(n-1, 2)/kappa
                counts["baseline_equalities"] += 1
            for dose in [Q(1, 5), Q(1), Q(5)]:
                t = dose / n
                ca = literal_current(n, kappa, 0, [t]*n)
                cb = literal_current(n, kappa, 1, [t]*n)
                assert ca == reduced(n, kappa, 0, [t]*n)
                assert cb == reduced(n, kappa, 1, [t]*n)
                counts["literal_reduced_equalities"] += 2
                d0, d1 = Q(1), 1+kappa*t
                for j in range(2, n+1):
                    d0, d1 = d1, (1+kappa*t)*d1 - (kappa*t/2)**2*d0
                gap = cb-ca
                expected = (kappa/2)**(n-1)*t**n/d1
                assert gap == expected > 0
                counts["dense_gap_equalities"] += 1
                lower = (kappa/2)**(n-1)*t**n/(1+kappa*t)**n
                assert gap >= lower > 0
                counts["rational_gap_lower_bounds"] += 1
                rows.append({"n": n, "kappa": str(kappa), "dose": str(dose),
                             "baseline": str(Q(n-1,2)/kappa),
                             "current_A": str(ca), "current_B": str(cb),
                             "gap": str(gap), "gap_decimal_display": float(gap),
                             "rational_lower": str(lower)})
    assert literal_current(2, Q(1), 0, [Q(1,2)]*2) == Q(9,14)
    assert literal_current(2, Q(1), 1, [Q(1,2)]*2) == Q(7,10)
    result = {"status": "PASS", "arithmetic": "exact rational assertions",
              "counts": counts, "rows": rows,
              "scope": "Root-origin circuit, finite exact source checks; all-n claims proved in note; n>=2."}
    dest = Path(__file__).with_name("resistor_network_lower_bound_checks.json")
    dest.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "counts": counts, "output": str(dest)}, indent=2))


if __name__ == "__main__":
    main()
