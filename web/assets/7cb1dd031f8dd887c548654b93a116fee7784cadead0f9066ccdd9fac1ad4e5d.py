#!/usr/bin/env python3
"""Exact checks for the T15 projective near-degeneracy family.

For eps = 2**(-L), form four projective columns in R^2, normalize each
column to l1 norm one, and verify that the maximum-volume basis is the first
two columns while another circuit has coefficient imbalance 2*(1+eps)/eps.
All calculations use Fraction; no floating-point tolerance is involved.
"""

from fractions import Fraction
from itertools import combinations


def det2(u, v):
    return u[0] * v[1] - u[1] * v[0]


def scale(u, q):
    return (u[0] * q, u[1] * q)


def add(*vectors):
    return (sum(v[0] for v in vectors), sum(v[1] for v in vectors))


def linear_map(M, u):
    return (M[0][0] * u[0] + M[0][1] * u[1],
            M[1][0] * u[0] + M[1][1] * u[1])


def check(L):
    eps = Fraction(1, 2**L)
    # Raw columns: (1,0), (0,1), (1,1), (1,1+eps).
    # Positive column scaling is a variable substitution in Ax=b, x>=0.
    cols = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1, 1) / (2 + eps), (1 + eps) / (2 + eps)),
    ]
    assert all(abs(u[0]) + abs(u[1]) == 1 for u in cols)

    minors = {I: det2(cols[I[0]], cols[I[1]]) for I in combinations(range(4), 2)}
    assert abs(minors[(0, 1)]) == 1
    assert all(abs(v) <= 1 for v in minors.values())

    # Circuit on columns 1, 3, 4 (zero-based indices 0,2,3):
    # a*c1 + b*c3 + d*c4 = 0.
    a = eps / (2 * (2 + eps))
    b = -(1 + eps) / (2 + eps)
    d = Fraction(1, 2)
    residual = add(scale(cols[0], a), scale(cols[2], b), scale(cols[3], d))
    assert residual == (0, 0)
    imbalance = max(abs(a), abs(b), abs(d)) / min(abs(a), abs(b), abs(d))
    assert imbalance == 2 * (1 + eps) / eps

    # Embed the same geometry into an LP with b=c3, xbar=e3, and
    # c=(1, 2**(2L), 0, 1). Since c>=0, xbar is an exact optimum of value 0.
    # Two feasible tangent circuits can increase x1: h below and q=(1/2,1/2,-1,0).
    # For L>=2, h gives the strictly larger initial x1-per-cost slope.
    M = 2 ** (2 * L)
    c = (1, M, 0, 1)
    xbar = (0, 0, 1, 0)
    b = cols[2]
    assert add(*(scale(cols[j], xbar[j]) for j in range(4))) == b
    assert all(value >= 0 for value in c)
    assert sum(c[j] * xbar[j] for j in range(4)) == 0
    h = (eps / (2 * (1 + eps)), Fraction(0), Fraction(-1),
         (2 + eps) / (2 * (1 + eps)))
    q = (Fraction(1, 2), Fraction(1, 2), Fraction(-1), Fraction(0))
    assert add(*(scale(cols[j], h[j]) for j in range(4))) == (0, 0)
    assert add(*(scale(cols[j], q[j]) for j in range(4))) == (0, 0)
    h_cost = sum(c[j] * h[j] for j in range(4))
    q_cost = sum(c[j] * q[j] for j in range(4))
    assert h_cost == 1
    assert q_cost == Fraction(M + 1, 2)
    h_x1_slope = h[0] / h_cost
    q_x1_slope = q[0] / q_cost
    if L >= 2:
        assert h_x1_slope > q_x1_slope

    # Adjacent basis exchange has a positive but arbitrarily small relative
    # volume gain: det(c1,c4)/det(c1,c3) = 1 + eps/(2+eps).
    adjacent_gain = det2(cols[0], cols[3]) / det2(cols[0], cols[2]) - 1
    assert adjacent_gain == eps / (2 + eps)
    assert 0 < adjacent_gain < eps / 2

    # Projective cross-ratio, using raw columns to keep the integer formulas.
    raw = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(1) + eps),
    ]
    D = {I: det2(raw[I[0]], raw[I[1]]) for I in combinations(range(4), 2)}
    cross_ratio = D[(0, 2)] * D[(1, 3)] / (D[(0, 3)] * D[(1, 2)])
    assert cross_ratio == 1 / (1 + eps)
    assert 1 - cross_ratio == eps / (1 + eps)

    # The cross-ratio survives an invertible row map and independent positive
    # column rescalings. These operations are projective changes of frame.
    M = ((2, 1), (1, 3))
    column_scales = (Fraction(2), Fraction(3, 2), Fraction(5, 3), Fraction(7, 4))
    transformed = [scale(linear_map(M, raw[j]), column_scales[j]) for j in range(4)]
    DT = {I: det2(transformed[I[0]], transformed[I[1]]) for I in combinations(range(4), 2)}
    transformed_cross_ratio = (
        DT[(0, 2)] * DT[(1, 3)] / (DT[(0, 3)] * DT[(1, 2)])
    )
    assert transformed_cross_ratio == cross_ratio
    return eps, imbalance, 1 - cross_ratio


def main():
    print("L, eps, circuit_imbalance, projective_gap, adjacent_volume_gain, h_vs_q_x1_slope")
    for L in (1, 2, 8, 32, 128, 512):
        eps, imbalance, gap = check(L)
        gain = eps / (2 + eps)
        if L >= 2:
            slope_ratio = (eps / (2 * (1 + eps))) / Fraction(1, 2 ** (2 * L) + 1)
        else:
            slope_ratio = "not claimed"
        print(f"{L}, {eps}, {imbalance}, {gap}, {gain}, {slope_ratio}")
    print("PASS: exact Fraction identities hold for all cases.")


if __name__ == "__main__":
    main()
