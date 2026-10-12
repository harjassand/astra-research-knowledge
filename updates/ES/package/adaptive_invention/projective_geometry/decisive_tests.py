#!/usr/bin/env python3
"""Exact rational tests for WORKING_MATHEMATICS.md. Python standard library."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def matvec(a, x):
    return [dot(row, x) for row in a]


def solve(a, b):
    n = len(a)
    q = [[F(x) for x in row] + [F(rhs)] for row, rhs in zip(a, b)]
    assert all(len(row) == n + 1 for row in q)
    for k in range(n):
        p = next((i for i in range(k, n) if q[i][k]), None)
        if p is None:
            return None
        q[k], q[p] = q[p], q[k]
        pivot = q[k][k]
        q[k] = [x / pivot for x in q[k]]
        for i in range(n):
            if i != k:
                scale = q[i][k]
                q[i] = [x - scale * y for x, y in zip(q[i], q[k])]
    return [row[-1] for row in q]


def feasible(h, b, x):
    return all(dot(row, x) <= rhs for row, rhs in zip(h, b))


def fan2(h, b, c, x, selected):
    """Exact global coordinate-pair slice, including degeneracy/recession."""
    j, k = selected
    rows = [(row[j], row[k]) for row in h]
    rhs = [r - dot(row, x) for row, r in zip(h, b)]
    cost = (c[j], c[k])
    rays = [(F(1), F(0)), (F(-1), F(0)),
            (F(0), F(1)), (F(0), F(-1))]
    for a1, a2 in rows:
        if a1 or a2:
            rays.extend([(a2, -a1), (-a2, a1)])
    for ray in rays:
        if dot(cost, ray) > 0 and all(dot(row, ray) <= 0 for row in rows):
            return {"unbounded": ray}
    candidates = [(F(0), F(0))]
    for row, r in zip(rows, rhs):
        n2 = dot(row, row)
        if n2:
            candidates.append(tuple(r * t / n2 for t in row))
    for i, ell in combinations(range(len(rows)), 2):
        sol = solve([rows[i], rows[ell]], [rhs[i], rhs[ell]])
        if sol is not None:
            candidates.append(tuple(sol))
    candidates = [u for u in candidates
                  if all(dot(row, u) <= r for row, r in zip(rows, rhs))]
    assert candidates  # 0 was supplied feasible
    u = max(candidates, key=lambda p: (dot(cost, p), p))
    out = list(x)
    out[j] += u[0]
    out[k] += u[1]
    assert feasible(h, b, out)
    return {"point": out, "value": dot(c, out)}


def cluster(d, alpha):
    m = [[F(1) if i == j else -alpha for j in range(d)]
         for i in range(d)]
    h = m + [[F(-1) if i == j else F(0) for j in range(d)]
             for i in range(d)] + [[F(1)] * d]
    b = [F(0)] * (2 * d) + [F(1)]
    return m, h, b


def ratio_jump(h, b, c, x, v):
    assert dot(c, v) > 0
    for row, rhs in zip(h, b):
        if dot(row, x) == rhs:
            assert dot(row, v) <= 0
    bounds = [(rhs - dot(row, x)) / dot(row, v)
              for row, rhs in zip(h, b) if dot(row, v) > 0]
    if not bounds:
        return None
    tau = min(bounds)
    assert tau > 0
    out = [xi + tau * vi for xi, vi in zip(x, v)]
    assert feasible(h, b, out)
    return out


def test_projective():
    records = []
    for ell in (1, 2, 4, 8, 16, 32):
        e, root = F(1, 2 ** (2 * ell)), F(1, 2 ** ell)
        a = [[F(1), F(0), F(1), F(1)],
             [F(0), F(1), F(1), e]]
        g = [[-1, -1, 1, 0], [-1, -e, 0, 1],
             [e-1, 0, -e, 1], [0, e-1, 1, -1]]
        g = [[F(x) for x in row] for row in g]
        assert all(matvec(a, row) == [0, 0] for row in g)
        det = lambda i, j: a[0][i]*a[1][j]-a[1][i]*a[0][j]
        assert all(det(i, j) for i, j in combinations(range(4), 2))
        cross = det(0, 2)*det(1, 3)/(det(0, 3)*det(1, 2))
        assert cross == 1/e
        scale = [F(1), root, root, F(1)]
        u = [[F(3), F(2)], [F(5), F(7)]]
        transformed = [[sum(u[i][k]*a[k][j] for k in range(2))*scale[j]
                        for j in range(4)] for i in range(2)]
        scaled_g = [[gi/di for gi, di in zip(row, scale)] for row in g]
        assert all(matvec(transformed, row) == [0, 0] for row in scaled_g)
        imbalance = max(max(abs(t) for t in row if t) /
                        min(abs(t) for t in row if t) for row in scaled_g)
        assert imbalance == 1/root
        r1 = abs(scaled_g[0][1]/scaled_g[0][0])
        r2 = abs(scaled_g[1][1]/scaled_g[1][0])
        assert r1/r2 == 1/e and imbalance**2 == 1/e
        records.append({"L": ell, "kappa_opt": str(imbalance),
                        "cross_ratio": str(cross)})
    return records


def test_fan_and_lower_bound():
    records = []
    eta, c = F(1, 12), [F(1)] * 3
    for ell in range(4, 10):
        delta = F(1, 2**ell)
        alpha = F(1, 2) + delta
        r = alpha/(1-alpha)
        m, h, b = cluster(3, alpha)
        x = [eta] * 3
        assert feasible(h, b, x)
        count, max_bits = 0, 0
        while sum(x) < 1:
            old_max = max(x)
            fixed = max(range(3), key=lambda j: x[j])
            selected = tuple(j for j in range(3) if j != fixed)
            raw_total = (1+2*r)*x[fixed]
            if raw_total < 1:
                expected = list(x)
                for j in selected:
                    expected[j] = r*x[fixed]
                if count < 4:
                    out = fan2(h, b, c, x, selected)
                    assert out["point"] == expected
                x = expected
            else:
                x = fan2(h, b, c, x, selected)["point"]
                assert sum(x) == 1
            count += 1
            assert feasible(h, b, x) and max(x) <= r*old_max
            max_bits = max(max_bits, *(max(t.numerator.bit_length(),
                                          t.denominator.bit_length()) for t in x))
        lower_bound = F(1, 8*delta)
        assert count > lower_bound
        records.append({"L": ell, "delta": str(delta), "greedy_jumps": count,
                        "universal_strict_lower_bound": str(lower_bound),
                        "max_rational_component_bits": max_bits})
    # At exact degeneracy every proper coordinate slice is a singleton.
    _, h, b = cluster(3, F(1, 2))
    for x in ([F(0)]*3, [eta]*3):
        for selected in combinations(range(3), 2):
            assert fan2(h, b, c, x, selected)["point"] == x
    # A parallel-normal strip and halfplane test the no-vertex/recession cases.
    strip = fan2([[F(1), F(0)], [F(-1), F(0)]], [F(2), F(2)],
                 [F(1), F(0)], [F(0), F(0)], (0, 1))
    assert strip["value"] == 2
    ray = fan2([[F(0), F(-1)]], [F(0)], [F(0), F(1)],
               [F(0), F(0)], (0, 1))
    assert "unbounded" in ray
    return records


def test_general_block_bound():
    cases = 0
    for d in range(3, 9):
        delta = F(1, 16*(d-1)**2)
        alpha = F(1, d-1) + delta
        eta = F(1, 4*d)
        _, h, b = cluster(d, alpha)
        x = [eta]*d
        for k in range(1, d):
            denom = 1-alpha*(k-1)
            r = alpha*(d-k)/denom
            assert r == 1+delta*(d-1)**2/(d-k-delta*(d-1)*(k-1))
            for selected in combinations(range(d), k):
                out = list(x)
                t = (d-k)*eta
                for j in selected:
                    out[j] = alpha*t/denom
                assert feasible(h, b, out)
                assert max(out) == r*max(x)
                cases += 1
    return cases


def test_collective_resolvent():
    records = []
    for ell in (4, 16, 64, 256, 1024):
        delta = F(1, 2**ell)
        alpha = F(1, 2) + delta
        m, h, b = cluster(3, alpha)
        v = solve(m, [F(-1)]*3)
        assert v == [1/(2*delta)]*3
        v = [t/v[0] for t in v]  # projective normalization
        x = [F(1, 12)]*3
        out = ratio_jump(h, b, [F(1)]*3, x, v)
        assert out == [F(1, 3)]*3
        records.append({"L": ell, "block_solves": 1, "ratio_jumps": 1,
                        "optimum": "1"})
    m, h, b = cluster(3, F(1, 2))
    assert solve(m, [F(-1)]*3) is None
    assert matvec(m, [F(1)]*3) == [0]*3
    out = ratio_jump(h, b, [F(1)]*3, [F(0)]*3, [F(1)]*3)
    assert out == [F(1, 3)]*3
    return records


def test_uniform_slack_failure():
    e = F(1, 16)
    h = [[F(-1), -e], [-e, F(1)]]
    uniform = solve(h, [F(-1)]*2)
    assert uniform == [(1+e)/(1+e**2), (e-1)/(1+e**2)]
    assert uniform[1] < 0
    v = [F(1), e/2]
    assert min(v) > 0 and max(matvec(h, v)) < 0
    return {"uniform_direction": [str(t) for t in uniform],
            "strict_feasible_direction": [str(t) for t in v]}


def test_face_freezing():
    h = [[F(-1), F(0), F(0)], [F(0), F(-1), F(0)],
         [F(0), F(0), F(-1)], [F(1), F(0), F(0)],
         [F(0), F(1), F(0)], [F(0), F(0), F(1)],
         [F(1), F(0), F(2)], [F(0), F(1), F(2)]]
    b = [F(0)]*3+[F(1)]*3+[F(2)]*2
    c = [F(1), F(1), F(5)]
    start = [F(1, 10)]*3
    sliced = fan2(h, b, c, start, (0, 1))["point"]
    assert sliced == [F(1), F(1), F(1, 10)]
    tight = [i for i, (row, rhs) in enumerate(zip(h, b)) if dot(row, sliced) == rhs]
    assert tight == [3, 4]
    vertices = set()
    for selected in combinations(range(len(h)), 3):
        v = solve([h[i] for i in selected], [b[i] for i in selected])
        if v is not None and feasible(h, b, v):
            vertices.add(tuple(v))
    best_value = max(dot(c, v) for v in vertices)
    optima = [v for v in vertices if dot(c, v) == best_value]
    assert optima == [(F(0), F(0), F(1))] and best_value == 5
    assert all(dot(h[i], optima[0]) < b[i] for i in tight)
    return {"slice_point": [str(t) for t in sliced],
            "unique_optimum": [str(t) for t in optima[0]],
            "new_tight_rows_all_slack_at_optimum": True}


def main():
    data = {
        "status": "RESTRICTED_OPERATIONS_VERIFIED_GENERAL_LP_UNRESOLVED",
        "arithmetic": "fractions.Fraction; no tolerance",
        "projective": test_projective(),
        "coordinate_pair_lower_bound": test_fan_and_lower_bound(),
        "general_coordinate_block_cases": test_general_block_bound(),
        "collective_resolvent": test_collective_resolvent(),
        "uniform_slack_failure": test_uniform_slack_failure(),
        "permanent_face_failure": test_face_freezing(),
    }
    output = Path(__file__).with_name("TEST_RESULTS.json")
    output.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
