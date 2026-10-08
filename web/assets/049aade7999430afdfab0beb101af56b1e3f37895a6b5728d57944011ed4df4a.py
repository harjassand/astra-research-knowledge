#!/usr/bin/env python3
"""Focused exact and numerical diagnostics for LOW_WINDOW_JACOBI_PROOF.txt.

The polynomial identity is checked as an identity by exact_potential.py.
The finite checks here exercise source reversal, rate orientation, endpoints,
the AM--GM constants, the soft-slot interlacing, and representative counts.
They are not a replacement for the uniform inequalities in the proof.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import isqrt, prod, sqrt
from pathlib import Path
import json
import numpy as np

from exact_potential import main as exact_identity_check


def invariants(a, b):
    N = a + b
    c2 = F(a * a + a * b + b * b + 3 * N, 3)
    c3 = F((a - b) * (2 * a + b + 3) * (a + 2 * b + 3), 18)
    alpha = c3 / c2
    cs = (c2 * (c2 / 3 + F(1, 4)) - c3 * c3 / c2) / (N * N)
    v = F(2 * a + b + 3, 3) - 2 * alpha
    return N, c2, c3, alpha, cs, v


def rates(a, b, R, delta, j):
    N, _, _, _, _, v = invariants(a, b)
    Q = R + delta
    A = F((a + 1 - Q + j) * (j + 1) * (j + 1 - delta), N * N)
    A *= N + Q + 2 - v - j
    C = F((Q - j) * (R - j) * (b - j), N * N) * (v + j + 1)
    return A, C


def potential(a, b, R, delta, j):
    N, _, _, _, _, v = invariants(a, b)
    z, w = (v - b) / 2, a + 1 - v
    L1 = (delta + 1) * ((N + 2) * w - delta * (delta + 2)
                        - R * (2 * z + delta + 1))
    L0 = (R * R * z * (z + delta) + R * delta * ((z + b) ** 2 + v)
          + R * delta * delta * z + R * (2 * z * z + b * (v + 1))
          + delta * (delta + 1) * (z + b) * (z + b + 1))
    return ((delta + 1) * (delta + 2) * j * j + L1 * j + L0) / (N * N)


def source_data(a, b, R, delta):
    N = a + b
    Q = R + delta
    ell, n = N + 1 - Q, N + 1 - R
    xi = [ell, b + 1, b + 1 + ell - n, ell - a - 1, n - a - 1, 0]
    xi_b = max(xi[3:])
    dim = min(xi[:3]) - xi_b
    Lambda = sum(xi[:3]) - sum(xi[3:]) + 2 * abs(ell - n)
    lm, lp = -F(Lambda, 2) + F(sum(xi), 6), F(Lambda, 2) + F(sum(xi), 6)
    return xi, xi_b, dim, Lambda, lm, lp


def source_diagonal(a, b, R, delta, j):
    N, c2, c3, alpha, _, _ = invariants(a, b)
    xi, xi_b, _, Lambda, _, _ = source_data(a, b, R, delta)
    source_index = b - j + 1 - xi_b
    x = [F(z - source_index - xi_b) + F(1, 2) for z in xi]
    E = {k: sum(z ** k for z in x) for k in range(1, 5)}
    X = -(F(7, 2) * E[1] ** 3 - 18 * E[1] * E[2] + 18 * E[3]) / 108
    X -= E[1] * (Lambda * Lambda + 2) / 24
    Y = (F(5, 2) * E[1] ** 4 + 32 * E[1] * E[3]
         + 6 * (E[2] ** 2 - 3 * E[1] ** 2 * E[2] - 4 * E[4])
         + 6 * E[2] * (Lambda * Lambda + 2)
         - 3 * E[1] ** 2 * (Lambda * Lambda - 2)
         - F(3, 2) * Lambda ** 4 + 6 * Lambda * Lambda - 36) / 288
    c = R * R + R * delta + delta * delta + 2 * R + delta
    scalar = -F(c * c, 12) + (c2 / 3 + F(1, 4) + alpha * alpha) * c
    scalar -= F(4, 3) * alpha * c3
    return (-Y - 2 * alpha * X + scalar) / (N * N)


def source_rates(a, b, R, delta, j):
    N, _, _, alpha, _, _ = invariants(a, b)
    xi, _, _, _, lm, lp = source_data(a, b, R, delta)
    t = b - j
    upper = prod(t - x for x in xi[:3])
    lower = prod(t - x for x in xi[3:])
    # Source order is reversed: its upper entry is K_(j+1,j).
    return (-F(upper, N * N) * (t - lm + 2 * alpha),
            -F(lower, N * N) * (t - lp + 2 * alpha))


def jacobi(a, b, R, delta):
    jmax = min(R, b)
    js = list(range(delta, jmax + 1))
    J = np.zeros((len(js), len(js)))
    for i, j in enumerate(js):
        Aprev, _ = rates(a, b, R, delta, j - 1)
        A, C = rates(a, b, R, delta, j)
        J[i, i] = float(Aprev + C + potential(a, b, R, delta, j))
        if i + 1 < len(js):
            J[i, i + 1] = J[i + 1, i] = -sqrt(float(A * C))
    return J, js


def cases():
    result = set()
    for b in [1, 2, 3, 5, 10, 20, 50, 100]:
        for N in {100 * b, 1000 * b, 100 * b * b, 1000 * b * b, 1_000_000}:
            if b * 100 > N:
                continue
            a = N - b
            rmax = isqrt(N // 100)
            choices = {0, 1, 2, 3, b - 1, b, b + 1, 2 * b, rmax // 2, rmax}
            for R in sorted(x for x in choices if 0 <= x <= rmax):
                dmax = min(R, b)
                for delta in {0, 1, 2, dmax // 2, dmax - 1, dmax}:
                    if not 0 <= delta <= dmax:
                        continue
                    c = R * R + R * delta + delta * delta + 2 * R + delta
                    if 100 * c <= N:
                        result.add((a, b, R, delta))
    return sorted(result)


def main():
    exact_identity_check()
    totals = dict(blocks=0, coordinates=0, offdiagonal_source_checks=0,
                  truncated_blocks=0, soft_blocks=0, singleton_blocks=0)
    worst_form = [float('inf'), None]
    worst_spectrum = [float('inf'), None]
    for a, b, R, delta in cases():
        N, c2, c3, alpha, cs, v = invariants(a, b)
        c = R * R + R * delta + delta * delta + 2 * R + delta
        Q, jmax, u = R + delta, min(R, b), F(b * R, N)
        assert v == F((2 * a + b + 3) * b * (b + 2), 3) / c2
        assert 0 < v <= F(9 * b * b, N)
        assert 0 < cs <= F(5, 2) * b * (b + 2) < 4 * (b + 1) ** 2
        assert source_data(a, b, R, delta)[2] == jmax - delta + 1
        assert rates(a, b, R, delta, delta - 1)[0] == 0
        assert rates(a, b, R, delta, jmax)[1] == 0
        for j in range(delta, jmax + 1):
            Aprev, _ = rates(a, b, R, delta, j - 1)
            A, C = rates(a, b, R, delta, j)
            P = potential(a, b, R, delta, j)
            assert source_diagonal(a, b, R, delta, j) == Aprev + C + P
            assert P >= F(7, 10) * (delta + 1) * j + F(1, 5) * u * u
            assert Aprev >= F(9, 10) * j * (j - delta)
            if j >= 1:
                assert C <= F(9, 50) * u * u + F(1, 2500) * j
                assert Aprev / 2 - C + P >= F(2, 5) * j * (j + 1)
            if j < jmax:
                assert A > 0 and C > 0
                assert source_rates(a, b, R, delta, j) == (A, C)
                totals['offdiagonal_source_checks'] += 1
            totals['coordinates'] += 1
        J, js = jacobi(a, b, R, delta)
        start = 1 if delta == 0 else 0
        if start < len(js):
            tail = J[start:, start:]
            diagonal = np.array([.4 * j * (j + 1) for j in js[start:]])
            margin = float(np.linalg.eigvalsh(tail - np.diag(diagonal))[0])
            assert margin >= -1e-9 * max(1, np.linalg.norm(tail, ord=np.inf))
            if margin < worst_form[0]:
                worst_form = [margin, [a, b, R, delta]]
        eigs = np.linalg.eigvalsh(J)
        for eig, j in zip(eigs, js):
            assert eig + 1e-9 * max(1, np.linalg.norm(J, ord=np.inf)) >= .4 * j * (j + 1)
            if j:
                ratio = float(eig / (j * (j + 1)))
                if ratio < worst_spectrum[0]:
                    worst_spectrum = [ratio, [a, b, R, delta, j]]
        totals['blocks'] += 1
        totals['truncated_blocks'] += int(jmax < R)
        totals['soft_blocks'] += int(delta == 0)
        totals['singleton_blocks'] += int(jmax == delta)

    count_checks = []
    for N, b in [(1000, 1), (1000, 10), (3000, 1), (3000, 20), (10000, 1), (10000, 100)]:
        a, B = N - b, b + 1
        cs = float(invariants(a, b)[4])
        T = F(N, 100)
        positive_count = 0
        for R in range(isqrt(N // 100) + 1):
            for delta in range(min(R, b) + 1):
                c = R * R + R * delta + delta * delta + 2 * R + delta
                if not 0 < c <= T:
                    continue
                p, q = R - delta, R + 2 * delta
                dim = (p + 1) * (q + 1) * (p + q + 2) // 2
                eigs = np.linalg.eigvalsh(jacobi(a, b, R, delta)[0])
                counted = int(sum(c + (N / sqrt(cs)) * x <= float(T) + 1e-8 for x in eigs))
                positive_count += dim * counted * (1 if p == q else 2)
        bound = 480 * T * T * (1 + F(B, N) * T)
        assert positive_count <= bound
        count_checks.append(dict(N=N, b=b, T=str(T), positive_count=positive_count,
                                 thin_count_bound=float(bound)))

    output = dict(status='PASS: finite diagnostics and exact polynomial identity; not a uniform proof',
                  totals=totals, worst_tail_form_margin=worst_form,
                  minimum_spectral_ratio_to_j_jplus1=worst_spectrum,
                  representative_count_checks=count_checks,
                  proof='LOW_WINDOW_JACOBI_PROOF.txt')
    path = Path(__file__).with_name('LOW_WINDOW_CHECKS.json')
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
