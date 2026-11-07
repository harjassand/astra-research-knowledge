"""Exact rational certification of a positive actuator-noise repair loop.

This is a mathematical coefficient certificate, not hardware calibration.
E[i][j] is the rate of noise type i produced by one unit of repair j.
The governing simultaneous native law is a separate supplied premise.
"""
from fractions import Fraction as Q


def solve(a, b):
    """Gauss-Jordan elimination over Python arbitrary precision rationals."""
    n = len(b)
    rows = [[Q(x) for x in row] + [Q(y)] for row, y in zip(a, b)]
    for j in range(n):
        k = next((k for k in range(j, n) if rows[k][j]), None)
        if k is None:
            raise ValueError("singular matrix")
        rows[j], rows[k] = rows[k], rows[j]
        z = rows[j][j]
        rows[j] = [x / z for x in rows[j]]
        for k in range(n):
            if k != j:
                z = rows[k][j]
                rows[k] = [x - z*y for x, y in zip(rows[k], rows[j])]
    return [row[-1] for row in rows]


def certify(e, b, caps=None, prices=None):
    n = len(b)
    if len(e) != n or any(len(row) != n for row in e):
        raise ValueError("E must be square and match b")
    e = [[Q(x) for x in row] for row in e]
    b = [Q(x) for x in b]
    if any(x < 0 for row in e for x in row) or any(x < 0 for x in b):
        raise ValueError("positive native-law coefficients required")
    reach = {i for i, x in enumerate(b) if x > 0}
    while True:
        more = {i for j in reach for i in range(n) if e[i][j] > 0}
        if more <= reach:
            break
        reach |= more
    ids = sorted(reach)
    mat = [[Q(i == j) - e[i][j] for j in ids] for i in ids]
    result = {"reachable": ids, "arithmetic": "exact Fraction"}
    try:
        w = solve(mat, [1]*len(ids))
    except ValueError:
        return dict(result, feasible_balance=False,
                    reason="reachable I-E is singular")
    if any(z <= 0 for z in w):
        return dict(result, feasible_balance=False,
                    reason="reachable I-E fails the positive inverse-vector criterion",
                    inverse_ones=[str(z) for z in w])
    xx = solve(mat, [b[i] for i in ids])
    x = [Q(0) for _ in range(n)]
    for i, z in zip(ids, xx):
        x[i] = z
    assert all(z >= 0 for z in x)
    residual = [x[i]-b[i]-sum(e[i][j]*x[j] for j in range(n))
                for i in range(n)]
    assert not any(residual)
    g = max(((z-1)/z for z in w), default=Q(0))
    assert 0 <= g < 1 or not ids
    result.update(feasible_balance=True, x=[str(z) for z in x],
                  positive_weight=[str(z) for z in w],
                  weighted_gain=str(g), residual=[str(z) for z in residual])
    if caps is not None:
        if len(caps) != n:
            raise ValueError("caps must match b")
        result["within_caps"] = all(z <= Q(c) for z, c in zip(x, caps))
    if prices is not None:
        if len(prices) != n or any(Q(c) < 0 for c in prices):
            raise ValueError("nonnegative prices must match b")
        result["minimal_balance_price"] = str(sum(z*Q(c) for z, c in zip(x, prices)))
    return result
