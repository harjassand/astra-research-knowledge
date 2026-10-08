#!/usr/bin/env python3
"""Exact Fraction verifier for strict small-gain/Farkas certificates.

This is a checker, not an LP optimizer. Input fixtures are embedded so the
script is dependency-free and reproduces the two 3-species witnesses in the
adjacent certificate_decidability.txt report.
"""

from fractions import Fraction as F


def build_A(delta, p, q, k, u):
    """Build A for rows (catalyst margins, edge margins, positivity).

    x = (lambda_1,...,lambda_r,w_1,...,w_s), and the target is Ax > 0.
    Rates are exact Fractions; p,q,k,u are rectangular r-by-s arrays.
    """
    r = len(delta)
    s = len(p[0])
    assert r > 0 and s > 0
    assert len(p) == len(q) == len(k) == len(u) == r
    assert all(len(row) == s for arr in (p, q, k, u) for row in arr)
    n = r + s
    rows = []
    for j in range(r):
        row = [F(0)] * n
        row[j] = F(delta[j])
        for i in range(s):
            row[r + i] = -F(p[j][i])
        rows.append(row)
    for j in range(r):
        for i in range(s):
            row = [F(0)] * n
            row[j] = -F(k[j][i]) * F(u[j][i])
            row[r + i] = F(q[j][i])
            rows.append(row)
    rows.extend([[F(int(a == b)) for b in range(n)] for a in range(n)])
    return rows


def mat_vec(A, x):
    return [sum((a * b for a, b in zip(row, x)), F(0)) for row in A]


def transpose_vec(A, y):
    return [sum((A[i][j] * y[i] for i in range(len(A))), F(0))
            for j in range(len(A[0]))]


def verify_primal(A, x):
    return (len(x) == len(A[0]) and sum(x, F(0)) == 1
            and all(v > 0 for v in x)
            and all(v > 0 for v in mat_vec(A, x)))


def verify_farkas(A, y):
    return (len(y) == len(A) and all(v >= 0 for v in y)
            and sum(y, F(0)) == 1
            and all(v <= 0 for v in transpose_vec(A, y)))


def rational_power_equal(base, target, exponent):
    """Compare positive rational base**exponent to target without huge powers."""
    base = F(base)
    target = F(target)
    exponent = int(exponent)
    if base <= 0 or target <= 0 or exponent < 1:
        return False

    def integer_power_equal(a, b):
        if a == 1:
            return b == 1
        if exponent > b.bit_length():
            return False
        # Once this guard passes, at most polynomially many output bits are
        # constructed: exponent is bounded by the target's bit length.
        return pow(a, exponent) == b

    return (integer_power_equal(base.numerator, target.numerator)
            and integer_power_equal(base.denominator, target.denominator))


def complex_balance(alpha, delta, p, q, k, u, v):
    """Exact edge-balance test for this tree-shaped complete family."""
    r = len(delta)
    s = len(p[0])
    c_a = [F(alpha[j]) / F(delta[j]) for j in range(r)]
    c_b = []
    for i in range(s):
        ratios = [F(p[j][i]) / F(q[j][i]) for j in range(r)]
        if any(ratios[j] != ratios[0] for j in range(1, r)):
            return False
        c_b.append(ratios[0])
    for j in range(r):
        for i in range(s):
            if not rational_power_equal(c_a[j], F(u[j][i]) / F(v[j][i]),
                                        k[j][i]):
                return False
    return all(c > 0 for c in c_a + c_b)


def main():
    # Strict-LP-infeasible, yet complex balanced: r=1, s=2.
    alpha_bad = [F(1)]
    delta_bad = [F(1)]
    p_bad = [[F(1), F(1)]]
    q_bad = [[F(2), F(2)]]
    k = [[1, 1]]
    u = [[F(1), F(1)]]
    v = [[F(1), F(1)]]
    A_bad = build_A(delta_bad, p_bad, q_bad, k, u)
    y = [F(1, 2), F(1, 4), F(1, 4), F(0), F(0), F(0)]
    assert verify_farkas(A_bad, y)
    assert transpose_vec(A_bad, y) == [F(0), F(0), F(0)]
    assert complex_balance(alpha_bad, delta_bad, p_bad, q_bad, k, u, v)

    # Strict-LP-feasible, yet not complex balanced: r=1, s=2.
    alpha_good = [F(1)]
    delta_good = [F(3)]
    p_good = [[F(1), F(1)]]
    q_good = [[F(2), F(2)]]
    A_good = build_A(delta_good, p_good, q_good, k, u)
    x = [F(1, 3), F(1, 3), F(1, 3)]
    assert verify_primal(A_good, x)
    assert mat_vec(A_good, x) == [F(1, 3)] * 6
    assert not complex_balance(alpha_good, delta_good, p_good, q_good, k, u, v)

    print("strict feasible fixture: exact primal accepted; margins = 1/3 each")
    print("strict infeasible fixture: exact Farkas witness accepted; A^T y = 0")
    print("complex balance: infeasible fixture YES; feasible fixture NO")


if __name__ == "__main__":
    main()
