#!/usr/bin/env python3
"""Exact checks for supplied feedback closure and its unrestricted obstruction.

This is not a general LP solver. Exhaustive circuit/vertex searches below are
small finite verification only, and their enumeration counts are reported.
"""

from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
from random import Random


def mv(a, x):
    return [sum((z * t for z, t in zip(row, x)), F(0)) for row in a]


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def feedback_closure(m, rhs):
    """Exact positive-pivot Z-matrix alternative; count rational operations."""
    n = len(m)
    z = [[F(int(i == j)) - F(m[i][j]) for j in range(n)] for i in range(n)]
    a = [row[:] for row in z]
    b = list(map(F, rhs))
    ops = n * n
    for p in range(n):
        ops += 1  # sign comparison
        if a[p][p] <= 0:
            v = [F(0)] * n
            v[p] = F(1)
            for i in range(p - 1, -1, -1):
                t = F(0)
                for j in range(i + 1, p + 1):
                    t += a[i][j] * v[j]
                    ops += 2
                v[i] = -t / a[i][i]
                ops += 2
            assert all(t >= 0 for t in v) and any(v)
            assert all(t <= 0 for t in mv(z, v))
            return "recession", v, ops
        for i in range(p + 1, n):
            ratio = a[i][p] / a[p][p]
            ops += 1
            for j in range(p + 1, n):
                a[i][j] -= ratio * a[p][j]
                ops += 2
            b[i] -= ratio * b[p]
            ops += 2
            a[i][p] = F(0)
    alpha = [F(0)] * n
    for i in range(n - 1, -1, -1):
        t = b[i]
        for j in range(i + 1, n):
            t -= a[i][j] * alpha[j]
            ops += 2
        alpha[i] = t / a[i][i]
        ops += 1
    assert all(t >= 0 for t in alpha)
    assert mv(z, alpha) == list(map(F, rhs))
    return "closure", alpha, ops


def solve_square(a, b):
    n = len(a)
    aug = [list(map(F, row)) + [F(z)] for row, z in zip(a, b)]
    for p in range(n):
        choices = [i for i in range(p, n) if aug[i][p]]
        if not choices:
            return None
        q = choices[0]
        aug[p], aug[q] = aug[q], aug[p]
        pivot = aug[p][p]
        aug[p] = [t / pivot for t in aug[p]]
        for i in range(n):
            if i != p:
                factor = aug[i][p]
                aug[i] = [u - factor * v for u, v in zip(aug[i], aug[p])]
    return [row[-1] for row in aug]


def one_dim_kernel(a):
    """Return a generator only when the exact nullity is one."""
    rows, cols = len(a), len(a[0])
    q = [list(map(F, row)) for row in a]
    pivots = []
    r = 0
    for j in range(cols):
        candidates = [i for i in range(r, rows) if q[i][j]]
        if not candidates:
            continue
        p = candidates[0]
        q[r], q[p] = q[p], q[r]
        t = q[r][j]
        q[r] = [v / t for v in q[r]]
        for i in range(rows):
            if i != r:
                t = q[i][j]
                q[i] = [u - t * v for u, v in zip(q[i], q[r])]
        pivots.append(j)
        r += 1
        if r == rows:
            break
    free = [j for j in range(cols) if j not in pivots]
    if len(free) != 1:
        return None
    g = [F(0)] * cols
    g[free[0]] = F(1)
    for i, j in enumerate(pivots):
        g[j] = -q[i][free[0]]
    return g


def vertices(h, d, dim):
    points, searched = [], 0
    for active in combinations(range(len(h)), dim):
        searched += 1
        point = solve_square([h[i] for i in active], [d[i] for i in active])
        if point is not None and all(a <= b for a, b in zip(mv(h, point), d)):
            points.append(point)
    return points, searched


def bit_length(q):
    return abs(q.numerator).bit_length() + q.denominator.bit_length()


def main():
    report = {"status": "PASS", "general_lp_status": "NOT_ACHIEVED"}
    coefficient_tests = []
    for length in [1, 2, 8, 64, 512]:
        a = F((1 << length) - 1, 1 << length)
        matrix = [[F(1), 0, F(1), -a], [0, F(1), -a, F(1)]]
        c = [0, 0, -(1 - a), -(1 - a)]
        g1, g2 = [F(-1), a, F(1), F(0)], [a, F(-1), F(0), F(1)]
        assert mv(matrix, g1) == [0, 0] == mv(matrix, g2)
        assert dot(c, g1) == dot(c, g2) == -(1 - a)
        x = [F(1), F(1), F(0), F(0)]
        for t in range(1, 9):
            q = x[0]
            assert q == x[1] > 0
            x = [v + q * (u + w) for v, u, w in zip(x, g1, g2)]
            assert x == [a**t, a**t, (1 - a**t) / (1 - a), (1 - a**t) / (1 - a)]
            assert mv(matrix, x) == [1, 1]
            assert dot(c, x) == -2 * (1 - a**t) > -2
        kind, alpha, ops = feedback_closure([[0, a], [a, 0]], [1, 1])
        assert kind == "closure" and alpha == [1 / (1 - a)] * 2
        final = [F(1) + alpha[0] * g1[0] + alpha[1] * g2[0],
                 F(1) + alpha[0] * g1[1] + alpha[1] * g2[1], alpha[0], alpha[1]]
        assert final[:2] == [0, 0] and mv(matrix, final) == [1, 1]
        assert dot(c, final) == -2
        coefficient_tests.append({"L": length, "closure_arithmetic_operations": ops,
                                  "max_output_rational_bits": max(map(bit_length, alpha))})
    assert len({r["closure_arithmetic_operations"] for r in coefficient_tests}) == 1
    report["coefficient_tests"] = coefficient_tests

    counts = {"closure": 0, "recession": 0}
    count_exhaustive = 0
    values = [F(0), F(1, 2), F(1), F(2)]
    for n in [1, 2, 3]:
        positions = [(i, j) for i in range(n) for j in range(n) if i != j]
        for entries in product(values, repeat=len(positions)):
            m = [[F(0)] * n for _ in range(n)]
            for (i, j), value in zip(positions, entries):
                m[i][j] = value
            rhs = [F(i + 1) for i in range(n)]
            kind, cert, _ = feedback_closure(m, rhs)
            counts[kind] += 1
            count_exhaustive += 1
    rng = Random(20261013)
    for n in range(4, 9):
        for _ in range(40):
            m = [[F(0) if i == j else F(rng.randrange(5), rng.randrange(1, 10))
                  for j in range(n)] for i in range(n)]
            kind, _, _ = feedback_closure(m, [F(rng.randrange(1, 8)) for _ in range(n)])
            counts[kind] += 1
    report["feedback_tests"] = {"exhaustive": count_exhaustive, "random": 200, "outcomes": counts}

    h = [[F(1, 3), F(2, 3)], [F(2, 3), F(1, 3)]]
    a = [[F(1), F(0)] + h[0], [F(0), F(1)] + h[1]]
    c = [F(0), F(0), F(-1), F(-1)]
    circuit_count, support_searches = 0, 0
    for size in range(1, 4):
        for support in combinations(range(4), size):
            support_searches += 1
            g_sub = one_dim_kernel([[row[j] for j in support] for row in a])
            if g_sub is None or not all(g_sub):
                continue
            g = [F(0)] * 4
            for j, v in zip(support, g_sub):
                g[j] = v
            circuit_count += 1
            for sign in [1, -1]:
                oriented = [sign * v for v in g]
                if sum(v < 0 for v in oriented) <= 1:
                    assert dot(c, oriented) >= 0
    assert circuit_count == 4
    report["absolute_sign_obstruction"] = {"supports_searched": support_searches,
                                            "circuits": circuit_count, "orientations": 2 * circuit_count}

    box_cases, packing_enumerations, box_enumerations, negative_rhs_cases = 0, 0, 0, 0
    for _ in range(50):
        n, m = 2, 2
        a = [[F(rng.randrange(-3, 4)) for _ in range(n)] for _ in range(m)]
        b = [F(rng.randrange(-3, 4)) for _ in range(m)]
        identities = [[F(int(i == j)) for j in range(n)] for i in range(n)]
        original_h = a + identities + [[-v for v in row] for row in identities]
        original_d = b + [F(1)] * n + [F(0)] * n
        original_points, searched = vertices(original_h, original_d, n)
        box_enumerations += searched
        pos = [[max(v, F(0)) for v in row] for row in a]
        neg = [[max(-v, F(0)) for v in row] for row in a]
        packed_rhs = [v + sum(row, F(0)) for v, row in zip(b, neg)]
        if any(v < 0 for v in packed_rhs):
            negative_rhs_cases += 1
            assert not original_points
            continue
        packed_h = [p + q for p, q in zip(pos, neg)]
        for i in range(n):
            packed_h.append([F(int(i == j)) for j in range(n)] * 2)
        packed_rhs += [F(1)] * n
        packed_h += [[F(-int(i == j)) for j in range(2 * n)] for i in range(2 * n)]
        packed_rhs += [F(0)] * (2 * n)
        packed_points, searched = vertices(packed_h, packed_rhs, 2 * n)
        packing_enumerations += searched
        assert packed_points
        optimum = max(sum(point, F(0)) for point in packed_points)
        assert (optimum == n) == bool(original_points)
        assert optimum <= n
        box_cases += 1
    report["packing_reduction_tests"] = {"random_box_cases": 50,
                                          "packing_cases": box_cases,
                                          "immediate_negative_rhs_cases": negative_rhs_cases,
                                          "box_active_sets_searched": box_enumerations,
                                          "packing_active_sets_searched": packing_enumerations}
    output = Path(__file__).with_name("verified.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
