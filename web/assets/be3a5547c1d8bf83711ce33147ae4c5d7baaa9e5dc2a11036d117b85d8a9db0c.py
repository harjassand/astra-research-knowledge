"""Exact finite checks for positive Taylor gates P_N(sA).

These fixtures support the algebraic formulas only.  They are not an FPRAS
and do not certify the imported Chen--Liu counting theorem.
"""
from fractions import Fraction as F
from itertools import product


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def scale(c, a):
    return [[c * v for v in row] for row in a]


def p_n(A, s, degree):
    out, power = eye(len(A)), eye(len(A))
    for k in range(1, degree + 1):
        power = mm(power, A)
        out = madd(out, scale(s**k / __import__('math').factorial(k), power))
    return out


def edge_checks():
    count = 0
    for alpha in (F(0), F(1, 3), F(1), F(2)):
        for ratio in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
            gamma = alpha * ratio
            for s, degree in product((F(0), F(1, 20), F(1, 3)), (1, 2, 4, 6)):
                A = [[3*alpha+gamma, 0, 0, 0],
                     [0, 3*alpha-gamma, 2*alpha, 0],
                     [0, 2*alpha, 3*alpha-gamma, 0],
                     [0, 0, 0, 3*alpha+gamma]]
                G = p_n(A, s, degree)
                lo, mid, hi = alpha-gamma, 3*alpha+gamma, 5*alpha-gamma
                qlo = sum((s**k * lo**k / __import__('math').factorial(k)
                           for k in range(degree+1)), F(0))
                qmid = sum((s**k * mid**k / __import__('math').factorial(k)
                            for k in range(degree+1)), F(0))
                qhi = sum((s**k * hi**k / __import__('math').factorial(k)
                           for k in range(degree+1)), F(0))
                a, b, c = qmid, (qhi+qlo)/2, (qhi-qlo)/2
                assert G == [[a, 0, 0, 0], [0, b, c, 0],
                             [0, c, b, 0], [0, 0, 0, a]]
                assert qlo <= qmid <= qhi
                assert c >= abs(a-b) and c <= a+b
                count += 1
    return count


def field_checks():
    count = 0
    for b, c, s, degree in product(
            (F(0), F(1, 3), F(2)),
            (F(-2), F(-1, 2), F(0), F(1, 3)),
            (F(0), F(1, 20), F(1, 3)), (1, 2, 4, 6)):
        r = b + abs(c)
        A = [[r+c, b], [b, r-c]]
        G = p_n(A, s, degree)
        v, d, u = G[0][0], G[0][1], G[1][1]
        assert v >= 1 and u >= 1 and d >= 0
        assert u*v-d*d > 0
        # Exact positive two-dummy homogeneous lift criterion.
        assert d*d <= u*v
        count += 1
    return count


if __name__ == '__main__':
    print({"edge_fixtures": edge_checks(),
           "field_fixtures": field_checks(),
           "degrees": [1, 2, 4, 6],
           "arithmetic": "exact Fraction"})
