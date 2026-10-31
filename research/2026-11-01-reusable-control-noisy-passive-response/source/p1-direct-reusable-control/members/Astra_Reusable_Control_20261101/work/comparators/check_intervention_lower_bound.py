#!/usr/bin/env python3
"""Exact rational checks of signed-cycle and inherited signed-path witnesses.

The general claims rest on the accompanying ordinary proofs. This program uses
no floating point arithmetic for a pass/fail decision and no hidden-source
access to pretend to acquire the model; it validates explicitly supplied
adversarial mathematical examples.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json


def determinant(a):
    a = [list(row) for row in a]
    n = len(a)
    if not n:
        return Q(1)
    ans = Q(1)
    for j in range(n):
        p = next((i for i in range(j, n) if a[i][j]), None)
        if p is None:
            return Q(0)
        if p != j:
            a[p], a[j] = a[j], a[p]
            ans = -ans
        pivot = a[j][j]
        ans *= pivot
        for i in range(j + 1, n):
            ratio = a[i][j] / pivot
            for k in range(j + 1, n):
                a[i][k] -= ratio * a[j][k]
    return ans


def solve(a, b):
    a = [list(row) + [rhs] for row, rhs in zip(a, b)]
    n = len(a)
    for j in range(n):
        p = next(i for i in range(j, n) if a[i][j])
        a[p], a[j] = a[j], a[p]
        pivot = a[j][j]
        for k in range(j, n + 1):
            a[j][k] /= pivot
        for i in range(n):
            if i == j:
                continue
            ratio = a[i][j]
            for k in range(j, n + 1):
                a[i][k] -= ratio * a[j][k]
    return [row[n] for row in a]


def response(b, g, u):
    keep = [i for i, x in enumerate(u) if x]
    if not keep:
        return Q(0)
    a = [[Q(i == j) + b[i][j] * u[j] for j in keep] for i in keep]
    x = solve(a, [g[i] for i in keep])
    return sum(g[i] * u[i] * xj for i, xj in zip(keep, x))


def matrix(n, cycle, sign, kappa=Q(1)):
    a = kappa / (2 if cycle else 4)
    b = [[kappa if i == j else Q(0) for j in range(n)] for i in range(n)]
    for i in range(n - 1):
        b[i][i + 1] = b[i + 1][i] = a
    if cycle:
        b[0][-1] = b[-1][0] = sign * a
    else:
        b[-1][-2] = b[-2][-1] = sign * a
    return b


def shifted(b, t):
    return [[Q(i == j) + t * x for j, x in enumerate(row)] for i, row in enumerate(b)]


def as_json(q):
    return {"exact": str(q), "decimal_display_only": float(q)}


def main():
    delta = Q(1, 5)
    counts = {"proper_support_comparisons": 0,
              "cycle_gap_checks": 0,
              "cycle_determinant_checks": 0,
              "rational_lower_bounds": 0,
              "path_gap_checks": 0,
              "path_recurrence_checks": 0}
    rows = []
    for n in range(3, 9):
        bp, bm = matrix(n, True, 1), matrix(n, True, -1)
        g = [Q(1)] + [Q(0)] * (n - 1)
        for size in range(n):
            for support in combinations(range(n), size):
                for pattern in [0, 1]:
                    u = [Q(0)] * n
                    for i in support:
                        u[i] = delta / n if not pattern else delta * (i + 1) / (n * (n + 1))
                    assert sum(u) <= delta
                    assert response(bp, g, u) == response(bm, g, u)
                    counts["proper_support_comparisons"] += 1
        for dose in [delta, Q(1), Q(5)]:
            t = dose / n
            ap, am = shifted(bp, t), shifted(bm, t)
            dp, dm = determinant(ap), determinant(am)
            cofactor = determinant([row[1:] for row in ap[1:]])
            assert cofactor >= 1 and dp >= 1 and dm >= 1
            assert dp - dm == 4 * (-1)**(n - 1) * (t / 2)**n
            counts["cycle_determinant_checks"] += 1
            fp, fm = response(bp, g, [t] * n), response(bm, g, [t] * n)
            gap = abs(fp - fm)
            assert gap == 4 * t * cofactor * (t / 2)**n / (dp * dm)
            counts["cycle_gap_checks"] += 1
            lower = 4 * t * (t / 2)**n / (1 + t)**(2 * n)
            assert gap >= lower > 0
            counts["rational_lower_bounds"] += 1
            rows.append({"kind": "cycle", "n": n, "dose": str(dose),
                         "gap": as_json(gap), "rational_lower": as_json(lower)})
    for n in range(2, 11):
        bp, bm = matrix(n, False, 1), matrix(n, False, -1)
        g = [Q(1)] + [Q(0)] * (n - 2) + [Q(1)]
        for dose in [delta, Q(1), Q(5)]:
            t = dose / n
            dp, dm = determinant(shifted(bp, t)), determinant(shifted(bm, t))
            d0, d1 = Q(1), 1 + t
            for j in range(2, n + 1):
                d0, d1 = d1, (1 + t) * d1 - (t / 4)**2 * d0
            assert dp == dm == d1
            counts["path_recurrence_checks"] += 1
            gap = abs(response(bp, g, [t] * n) - response(bm, g, [t] * n))
            assert gap == 4 * Q(1, 4)**(n - 1) * t**n / dp
            counts["path_gap_checks"] += 1
            lower = 4 * t * (t / 4)**(n - 1) / (1 + t)**n
            assert gap >= lower > 0
            counts["rational_lower_bounds"] += 1
            rows.append({"kind": "path", "n": n, "dose": str(dose),
                         "gap": as_json(gap), "rational_lower": as_json(lower)})
    # Closed-form triangle used in the correspondence with root.
    for t in [Q(1, 15), Q(1), Q(3), Q(10)]:
        bp, bm = matrix(3, True, 1), matrix(3, True, -1)
        g = [Q(1), Q(0), Q(0)]
        fp, fm = response(bp, g, [t] * 3), response(bm, g, [t] * 3)
        assert fp == t * (2 + 3*t) / (2 + 5*t + 2*t*t)
        assert fm == t * (2 + t) / (2 + 3*t)
        assert fm - fp == 2*t**4 / ((2+3*t)*(2+5*t+2*t*t))
    # Continuous-control five-actuator counterexample.
    b = [[Q(i == j) for j in range(5)] for i in range(5)]
    for j in range(1, 5):
        b[0][j] = b[j][0] = Q(3, 10)
    b[1][2] = b[2][1] = Q(-4, 5)
    b[3][4] = b[4][3] = Q(4, 5)
    perm = [0, 3, 4, 1, 2]
    bprime = [[b[perm[i]][perm[j]] for j in range(5)] for i in range(5)]
    v = [Q(1), Q(-3, 2), Q(-3, 2), Q(-1, 6), Q(-1, 6)]
    g = [Q(1), Q(0), Q(0), Q(0), Q(0)]
    assert all(sum(b[i][j]*v[j] for j in range(5)) == 0 for i in range(5))
    # PSD is independently checked by all principal minors, including singular ones.
    principal_checks = 0
    for size in range(1, 6):
        for support in combinations(range(5), size):
            assert determinant([[b[i][j] for j in support] for i in support]) >= 0
            principal_checks += 1
    pair_checks = 0
    for size in range(3):
        for support in combinations(range(5), size):
            for dose in [Q(1, 5), Q(1), Q(100), Q(10000)]:
                u = [Q(0)] * 5
                for i in support:
                    u[i] = dose * (i+1) / 15
                assert sum(u) <= dose
                assert response(b, g, u) == response(bprime, g, u)
                pair_checks += 1
    augmented = [row + [v[i]] for i, row in enumerate(b)] + [v + [Q(0)]]
    cs = []
    for j in range(5):
        w = [Q(i == j) / v[j] - g[i] for i in range(5)]
        z = solve(augmented, w + [Q(0)])[:5]
        cs.append(sum(w[i]*z[i] for i in range(5)))
    assert cs == [Q(0), Q(100,81), Q(100,81), Q(100), Q(100)]
    counts["five_control_psd_principal_minors"] = principal_checks
    counts["five_control_pair_equalities"] = pair_checks
    result = {"status": "PASS", "arithmetic": "exact fractions; float displays only",
              "counts": counts, "rows": rows,
              "continuous_regret": {"uniform_remainder_values": list(map(str,cs)),
                  "known_source_slope": "9/169",
                  "robust_source_slope": "9/(3+2*sqrt(41))^2",
                  "regret_bound": "delta*(9/169-9/(3+2*sqrt(41))^2)-100"}}
    dest = Path(__file__).with_name("intervention_lower_bound_checks.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "counts": counts, "output": str(dest)}, indent=2))


if __name__ == "__main__":
    main()
