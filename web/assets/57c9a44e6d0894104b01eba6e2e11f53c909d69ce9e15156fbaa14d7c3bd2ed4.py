"""Exact rational checks for the c06_l03 second-order XXZ gate proposal.

This is a finite diagnostic, not a proof of the universal inequalities or an
implementation of Chen--Liu's approximate counter.
"""

from fractions import Fraction as F
from itertools import product


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def mscale(c, a):
    return [[c * x for x in row] for row in a]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def taylor2(a, s):
    return madd(madd(eye(len(a)), mscale(s, a)),
                mscale(s * s / 2, matmul(a, a)))


def check_pair_gates():
    alphas = [F(0), F(1, 5), F(1), F(2)]
    scales = [F(0), F(1, 100), F(1, 3), F(1)]
    checked = 0
    for alpha in alphas:
        gammas = sorted({-alpha, -alpha / 2, F(0), alpha / 2, alpha})
        for gamma, s in product(gammas, scales):
            h = 3 * alpha
            aop = [
                [h + gamma, 0, 0, 0],
                [0, h - gamma, 2 * alpha, 0],
                [0, 2 * alpha, h - gamma, 0],
                [0, 0, 0, h + gamma],
            ]
            aop = [[F(x) for x in row] for row in aop]
            got = taylor2(aop, s)
            a = 1 + s * (h + gamma) + s * s * (h + gamma) ** 2 / 2
            b = 1 + s * (h - gamma) + s * s * ((h - gamma) ** 2 + 4 * alpha ** 2) / 2
            c = 2 * s * alpha + 2 * s * s * alpha * (h - gamma)
            expected = [
                [a, 0, 0, 0],
                [0, b, c, 0],
                [0, c, b, 0],
                [0, 0, 0, a],
            ]
            assert got == expected
            assert c - (a - b) == 2 * s * (alpha - gamma) * (1 + s * (h + alpha))
            assert c + (a - b) == 2 * s * (alpha + gamma) * (1 + s * (h - alpha))
            assert a + b - c == (
                2 + 2 * s * (h - alpha)
                + s * s * ((h - alpha) ** 2 + (alpha + gamma) ** 2)
            )
            assert c >= abs(a - b) and a + b >= c
            checked += 1
    return checked


def check_field_gates():
    bs = [F(0), F(1, 3), F(2)]
    cs = [F(-2), F(-1, 2), F(0), F(1, 3), F(3)]
    scales = [F(0), F(1, 100), F(1, 3), F(1)]
    checked = 0
    for b, c, s in product(bs, cs, scales):
        r = b + abs(c)
        aop = [[r + c, b], [b, r - c]]
        got = taylor2(aop, s)
        u0 = 1 + s * r + s * s * (r * r + b * b + c * c) / 2
        w = s + s * s * r
        expected = [[u0 + w * c, w * b], [w * b, u0 - w * c]]
        assert got == expected
        top, bottom = expected[0][0], expected[1][1]
        off = expected[0][1]
        assert top >= 0 and bottom >= 0 and off >= 0
        assert top * bottom - off * off >= 0
        checked += 1
    return checked


def check_palindrome_second_order():
    # Three noncommuting real symmetric 2x2 matrices, in palindromic order.
    a = [[F(1), F(0)], [F(0), F(-1)]]
    b = [[F(0), F(1)], [F(1), F(0)]]
    c = [[F(1), F(1)], [F(1), F(2)]]
    factors = [a, b, c, c, b, a]
    linear = [[sum((x[i][j] for x in factors), F(0)) for j in range(2)]
              for i in range(2)]
    quadratic = [[F(0), F(0)], [F(0), F(0)]]
    for j, x in enumerate(factors):
        quadratic = madd(quadratic, mscale(F(1, 2), matmul(x, x)))
        for y in factors[j + 1:]:
            quadratic = madd(quadratic, matmul(x, y))
    assert quadratic == mscale(F(1, 2), matmul(linear, linear))
    return len(factors)


if __name__ == "__main__":
    pair = check_pair_gates()
    field = check_field_gates()
    palindrome = check_palindrome_second_order()
    print({"pair_gate_cases": pair, "field_gate_cases": field,
           "palindrome_factors": palindrome, "arithmetic": "exact fractions"})
