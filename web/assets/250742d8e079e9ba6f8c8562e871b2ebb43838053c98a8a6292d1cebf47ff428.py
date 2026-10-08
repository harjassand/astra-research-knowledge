#!/usr/bin/env python3
"""Exact finite audit for a two-source CLE-equivalent catalytic CTMC pair.

Uses only the Python standard library.  All likelihood and moment calculations
are rational/integer; no stochastic simulation is used.
"""

from fractions import Fraction
from math import factorial


RA = (2, 1, 4, 1)          # source C, network A
RB = (1, 4, 1, 2)          # source C, network B
QA = (4, 1, 10, 1)         # source 2C, network A
QB = (1, 10, 1, 4)         # source 2C, network B
YIELDS = (1, 2, 3, 4)


def raw_moment(rates, order):
    return sum(rate * k**order for rate, k in zip(rates, YIELDS))


def outer(a, b):
    return tuple(tuple(x * y for y in b) for x in a)


def add_matrix(a, b):
    return tuple(tuple(x + y for x, y in zip(ra, rb)) for ra, rb in zip(a, b))


def scale_matrix(a, c):
    return tuple(tuple(c * x for x in row) for row in a)


def signature_sum(b, u, rates):
    m0, m1, m2 = (raw_moment(rates, p) for p in range(3))
    drift = tuple(m0 * x + m1 * z for x, z in zip(b, u))
    cross = add_matrix(outer(b, u), outer(u, b))
    covariance = add_matrix(
        add_matrix(scale_matrix(outer(b, b), m0), scale_matrix(cross, m1)),
        scale_matrix(outer(u, u), m2),
    )
    return (m0, m1, m2), drift, covariance


def overlap_for_marked_paths(n):
    """Optimal equal-prior LRT overlap = sum of the two error probabilities.

    A replicate has 20 ordered path categories: one mark k, or two marks
    (i,j).  Their probabilities have common denominator 128.  The dynamic
    program merges sequences with the same pair of likelihood numerators.
    """
    path_a = [4 * q for q in QA] + [x * y for x in RA for y in RA]
    path_b = [4 * q for q in QB] + [x * y for x in RB for y in RB]
    assert sum(path_a) == sum(path_b) == 128
    states = {(1, 1): 1}
    for _ in range(n):
        nxt = {}
        for (pa, pb), multiplicity in states.items():
            for a, b in zip(path_a, path_b):
                if a == b == 0:
                    continue  # impossible under both; contributes no risk
                key = (pa * a, pb * b)
                nxt[key] = nxt.get(key, 0) + multiplicity
        states = nxt

    err_a = Fraction(0)  # A true, decide B
    err_b = Fraction(0)  # B true, decide A
    for (pa, pb), multiplicity in states.items():
        if pa < pb:
            err_a += multiplicity * pa
        elif pa > pb:
            err_b += multiplicity * pb
        else:
            err_a += Fraction(multiplicity * pa, 2)
            err_b += Fraction(multiplicity * pb, 2)
    denom = 128**n
    return err_a / denom + err_b / denom, err_a / denom, err_b / denom, len(states)


def overlap_for_endpoint(n):
    """Exact optimal LRT overlap using only terminal total product P."""
    def conv(a, b):
        out = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] += x * y
        return out

    conv_a, conv_b = conv(RA, RA), conv(RB, RB)
    end_a = [
        4 * (QA[z - 1] if z <= 4 else 0)
        + (conv_a[z - 2] if 2 <= z <= 8 else 0)
        for z in range(1, 9)
    ]
    end_b = [
        4 * (QB[z - 1] if z <= 4 else 0)
        + (conv_b[z - 2] if 2 <= z <= 8 else 0)
        for z in range(1, 9)
    ]
    assert sum(end_a) == sum(end_b) == 128

    numerator = 0

    def visit(i, left, la, lb, multinomial_factor):
        nonlocal numerator
        if i == 7:
            c = left
            numerator += (multinomial_factor // factorial(c)) * min(
                la * end_a[i] ** c, lb * end_b[i] ** c
            )
            return
        for c in range(left + 1):
            visit(
                i + 1,
                left - c,
                la * end_a[i] ** c,
                lb * end_b[i] ** c,
                multinomial_factor // factorial(c),
            )

    visit(0, n, 1, 1, factorial(n))
    return Fraction(numerator, 128**n), end_a, end_b


def main():
    b1, b2, u = (-1, 1, 4, 0), (-2, 2, 8, 0), (0, 0, -1, 1)
    moments_a1, drift_a1, cov_a1 = signature_sum(b1, u, RA)
    moments_b1, drift_b1, cov_b1 = signature_sum(b1, u, RB)
    moments_a2, drift_a2, cov_a2 = signature_sum(b2, u, QA)
    moments_b2, drift_b2, cov_b2 = signature_sum(b2, u, QB)
    assert moments_a1 == moments_b1 == (8, 20, 58)
    assert moments_a2 == moments_b2 == (16, 40, 114)
    assert (drift_a1, cov_a1) == (drift_b1, cov_b1)
    assert (drift_a2, cov_a2) == (drift_b2, cov_b2)
    assert (raw_moment(RA, 3), raw_moment(RB, 3)) == (182, 188)
    assert (raw_moment(QA, 3), raw_moment(QB, 3)) == (346, 364)

    # Standard factorial-normalized count propensities: C for source C and
    # choose(C,2) for source 2C. At C=2, hazards are 2*8=16 and 1*16=16.
    assert 2 * sum(RA) == sum(QA) == 16
    assert 2 * sum(RB) == sum(QB) == 16
    assert sum(RA) == sum(RB) == 8

    print("Source C moments A/B:", moments_a1, moments_b1)
    print("Source 2C moments A/B:", moments_a2, moments_b2)
    print("Source C common drift:", drift_a1)
    print("Source C common covariance:", cov_a1)
    print("Source 2C common drift:", drift_a2)
    print("Source 2C common covariance:", cov_a2)
    print("Initial total hazard at C=2: 32; branch probabilities: 1/2, 1/2")
    print("Third product-generator gap Q_A(P^3)-Q_B(P^3) at C=2:", -30)

    path_a = [4 * q for q in QA] + [x * y for x in RA for y in RA]
    path_b = [4 * q for q in QB] + [x * y for x in RB for y in RB]
    print("Marked-path weights A/128:", path_a)
    print("Marked-path weights B/128:", path_b)
    for n in range(1, 6):
        risk, err_a, err_b, states = overlap_for_marked_paths(n)
        print(
            f"Marked-path N={n}: sum-error={risk} ({float(risk):.12f}); "
            f"type-errors=({err_a}, {err_b}); DP-states={states}"
        )

    for n in (5, 8, 12, 13, 14, 15, 16):
        risk, _, _ = overlap_for_endpoint(n)
        print(f"Endpoint-only N={n}: sum-error={risk} ({float(risk):.12f})")

    risk5, end_a, end_b = overlap_for_endpoint(5)
    del risk5
    moments_end_a = tuple(
        Fraction(sum(w * z**p for z, w in enumerate(end_a, start=1)), 128)
        for p in (1, 2, 3)
    )
    moments_end_b = tuple(
        Fraction(sum(w * z**p for z, w in enumerate(end_b, start=1)), 128)
        for p in (1, 2, 3)
    )
    assert moments_end_a[:2] == moments_end_b[:2]
    assert moments_end_b[2] - moments_end_a[2] == Fraction(21, 16)
    print("Endpoint weights A/128:", end_a)
    print("Endpoint weights B/128:", end_b)
    print("Endpoint raw moments A:", moments_end_a)
    print("Endpoint raw moments B:", moments_end_b)
    print("All exact assertions passed.")


if __name__ == "__main__":
    main()
