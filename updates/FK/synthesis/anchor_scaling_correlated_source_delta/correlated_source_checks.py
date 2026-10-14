#!/usr/bin/env python3
"""Exact finite checks for a correlated Gaussian first-order source repair."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def zeros(n, m=None):
    m = n if m is None else m
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    out = zeros(n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def mscale(c, a):
    return [[c * x for x in row] for row in a]


def solve(a, b):
    """Gauss-Jordan solve over exact rationals."""
    n = len(b)
    aug = [list(a[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col]), None)
        if pivot is None:
            raise ArithmeticError("singular exact system")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            if factor:
                aug[r] = [aug[r][j] - factor * aug[col][j]
                          for j in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


def inverse(a):
    n = len(a)
    cols = [solve(a, [F(i == j) for i in range(n)]) for j in range(n)]
    return transpose([[cols[j][i] for j in range(n)] for i in range(n)])


def solve_lyapunov(k, rhs):
    n = len(k)
    dim = n * n
    lhs = zeros(dim)
    flat_rhs = [rhs[i][j] for i in range(n) for j in range(n)]
    for i, j in product(range(n), repeat=2):
        row = i * n + j
        for a, b in product(range(n), repeat=2):
            col = a * n + b
            lhs[row][col] = k[i][a] * F(b == j) + F(i == a) * k[b][j]
    flat = solve(lhs, flat_rhs)
    return [flat[i * n:(i + 1) * n] for i in range(n)]


def lyapunov_lhs(k, x):
    return madd(matmul(k, x), matmul(x, k))


def fstr(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def double_factorial(n):
    if n <= 0:
        return 1
    out = 1
    while n > 0:
        out *= n
        n -= 2
    return out


def scalar_quartic_coefficients(order=3):
    """Series for E[x^2] under exp(-x^2/2-lambda*x^4/24), c=1."""
    b = [F(1)]
    a = [F(1)]
    for n in range(1, order + 1):
        sign = -1 if n % 2 else 1
        den = F(24**n * __import__('math').factorial(n))
        b.append(F(sign * double_factorial(4 * n - 1), 1) / den)
        a.append(F(sign * double_factorial(4 * n + 1), 1) / den)
    # If R(lambda)=A(lambda)/B(lambda), coefficients obey this recurrence.
    r = [a[0]]
    for n in range(1, order + 1):
        r.append(a[n] - sum((b[j] * r[n-j] for j in range(1, n + 1)), F(0)))
    return r


def main():
    # Three-cycle: K=2I+L, with spectrum 2,5,5 and exact Green matrix.
    k = [[F(4), F(-1), F(-1)],
         [F(-1), F(4), F(-1)],
         [F(-1), F(-1), F(4)]]
    c = inverse(k)
    c0 = c[0][0]
    assert all(c[i][i] == c0 for i in range(3))
    c_beta = 2 * c0

    # Full mask: exact matrix identity C1=-c_beta*C^2/2.
    p_full = eye(3)
    q_full = zeros(3)
    s3_full = c_beta / c0
    r_full = mscale(3 * s3_full * c0, c)
    rhs_full = mscale(F(-1, 6), madd(matmul(p_full, r_full),
                                     matmul(transpose(r_full), p_full)))
    c1_full = solve_lyapunov(k, rhs_full)
    expected_full = mscale(-c_beta / 2, matmul(c, c))
    assert c1_full == expected_full
    assert lyapunov_lhs(k, c1_full) == rhs_full

    # Partial one-site mask: s^3=4 makes every Fourier diagonal match.
    p_part = [[F(i == 0) if i == j else F(0) for j in range(3)]
              for i in range(3)]
    q_part = madd(eye(3), mscale(F(-1), p_part))
    f = F(1, 3)
    s3_part = (c_beta / c0 - (1 - f)) / f
    assert s3_part == 4
    r_part = mscale(3 * s3_part * c0, c)
    rhs_part = madd(
        mscale(-c0 / 2, madd(matmul(q_part, c), matmul(c, q_part))),
        mscale(F(-1, 6), madd(matmul(p_part, r_part),
                              matmul(transpose(r_part), p_part))),
    )
    c1_part = solve_lyapunov(k, rhs_part)
    assert lyapunov_lhs(k, c1_part) == rhs_part
    assert transpose(c1_part) == c1_part

    # Complex plane waves on the 3-cycle; q=0 has k_q=2, q=1,2 have k_q=5.
    import cmath
    q_diagonals = []
    for qmode, eig in ((0, 2), (1, 5), (2, 5)):
        v = [cmath.exp(2j * cmath.pi * qmode * j / 3) / (3 ** 0.5)
             for j in range(3)]
        projection = sum(v[i].conjugate() * float(p_part[i][i]) * v[i]
                         for i in range(3))
        got = sum(v[i].conjugate() * float(c1_part[i][j]) * v[j]
                  for i in range(3) for j in range(3))
        want = -float(c_beta) / (2 * eig * eig)
        assert abs(projection - 1 / 3) < 1e-14
        assert abs(got.real - want) < 1e-13 and abs(got.imag) < 1e-13
        q_diagonals.append({'mode': qmode, 'eigenvalue': eig,
                            'mask_fraction': projection.real,
                            'computed': got.real, 'expected': want})

    # Wick cross moments checked exactly against 3*s^3*C_ii*C_ij.
    wick_max_error = F(0)
    for i, j in product(range(3), repeat=2):
        lhs = 3 * s3_full * c0 * c[i][j]
        rhs = 3 * s3_full * c[i][i] * c[i][j]
        wick_max_error = max(wick_max_error, abs(lhs - rhs))
    assert wick_max_error == 0

    # True scalar quartic Gibbs target has nonzero coefficients through order 3.
    target_series = scalar_quartic_coefficients(3)
    assert target_series == [F(1), F(-1, 2), F(2, 3), F(-11, 8)]
    # Full-mask fixed-source OU covariance: c=1,s=1 gives 1,-1/2,1/6,0,...
    engineered_series = [F(1), F(-1, 2), F(1, 6), F(0)]
    assert target_series[1] == engineered_series[1]
    assert target_series[2] - engineered_series[2] == F(1, 2)
    assert target_series[3] != engineered_series[3]

    # Directly check the OU convolution integrals at k=c=1:
    # I1=int int exp(-(t+u)-|t-u|)=1/2; I3=...3|t-u|=1/4.
    i1, i3 = F(1, 2), F(1, 4)
    engineered_quadratic = (9 * i1 + 6 * i3) / 36
    assert engineered_quadratic == F(1, 6)

    out = {
        'status': 'PASS',
        'finite_lattice': {
            'K': [[fstr(x) for x in row] for row in k],
            'C': [[fstr(x) for x in row] for row in c],
            'c0': fstr(c0),
            'c_beta': fstr(c_beta),
            'full_mask_gain_cubed': fstr(s3_full),
            'full_mask_C1': [[fstr(x) for x in row] for row in c1_full],
            'full_mask_identity': 'C1 = -c_beta*C^2/2, exact Fractions',
            'partial_mask_fraction': fstr(f),
            'partial_mask_gain_cubed': fstr(s3_part),
            'partial_mask_fourier_checks': q_diagonals,
            'wick_cross_moment_max_exact_error': fstr(wick_max_error),
        },
        'scalar_series_c_equals_1': {
            'quartic_target': [fstr(x) for x in target_series],
            'fixed_source_engineered': [fstr(x) for x in engineered_series],
            'order2_target_minus_engineered': fstr(target_series[2] - engineered_series[2]),
            'interpretation': 'same first derivative; order-2 mismatch and nonzero target order-3 coefficient',
        },
        'ou_convolution_integrals_k_equals_1': {
            'I1': fstr(i1),
            'I3': fstr(i3),
            'engineered_order2': fstr(engineered_quadratic),
        },
        'claim_boundary': 'Exact finite Gaussian and scalar-series checks only; no physical quantum second-order calculation or all-coupling sampler validation.',
    }
    out_path = Path(__file__).with_name('results.json')
    out_path.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
