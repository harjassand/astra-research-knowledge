#!/usr/bin/env python3
"""Exact finite checks for filter_construction.txt.

Only Python integers and fractions are used. This checks identities on sample
GT branching data; the uniform theorem is proved in the accompanying text.
"""

from fractions import Fraction


def dimension(a, b):
    return (a + 1) * (b + 1) * (a + b + 2) // 2


def layer_size(a, b, t):
    """GT multiplicity of E_11 eigenvalue t, for the whole valid range."""
    lo = max(0, t - b)
    hi = min(a, t)
    return sum(a + t - 2 * x + 1 for x in range(lo, hi + 1))


def branch_casimir_weight(a, b, t):
    """Exact upward crossing weight from the U(3)/U(2) Casimir split."""
    c3 = (a + b) * (a + b + 2) + b * b
    total = a + 2 * b
    lo = max(0, t - b)
    hi = min(a, t)
    result = Fraction(0)
    for x in range(lo, hi + 1):
        y = t - x
        u = a + b - x
        v = b - y
        branch_dim = u - v + 1
        c2 = u * (u + 1) + v * (v - 1)
        gamma = Fraction(c3 - t * t - c2 - 3 * t + total, 2)
        result += branch_dim * gamma
    return result


def closed_weight(a, b, t):
    return Fraction((a + 1) * (t + 1) * (t + 2) * (a + 2 * b - 2 * t), 2)


def cumulative_low_layers(a, r):
    return (a + 1) * (r + 1) * (r + 2) // 2


def check_case(N, a, b, Q):
    assert N >= 16 and N <= a <= 2 * N and N <= b <= 2 * N
    D = dimension(a, b)
    assert 1 <= Q <= D // 512

    # The GT branching dimensions sum to the Weyl dimension formula.
    assert sum(layer_size(a, b, t) for t in range(a + b + 1)) == D

    # Compare exact Casimir traces with the closed crossing conductance.
    for t in range(min(a, b) + 1):
        assert branch_casimir_weight(a, b, t) == closed_weight(a, b, t)
        assert layer_size(a, b, t) == (a + 1) * (t + 1)

    M = N // 2
    R = next(r for r in range(M + 1) if cumulative_low_layers(a, r) >= Q)
    assert R < M
    nullity = cumulative_low_layers(a, R)
    assert nullity >= Q

    rho = sum(
        (1 / closed_weight(a, b, t) for t in range(R, M)),
        Fraction(0),
    )
    alpha = []
    for t in range(a + b + 1):
        if t <= R:
            value = Fraction(1)
        elif t < M:
            value = sum(
                (1 / closed_weight(a, b, j) for j in range(t, M)),
                Fraction(0),
            ) / rho
        else:
            value = Fraction(0)
        alpha.append(value)

    # X=I-A is nonnegative; its zeros are precisely the layers <=R.
    x_values = [1 - value for value in alpha]
    assert all(value >= 0 for value in x_values)
    counted_nullity = sum(
        layer_size(a, b, t)
        for t, value in enumerate(x_values)
        if value == 0
    )
    rank = sum(
        layer_size(a, b, t)
        for t, value in enumerate(x_values)
        if value > 0
    )
    assert counted_nullity == nullity
    assert rank == D - nullity <= D - Q

    energy = sum(
        closed_weight(a, b, t) * (alpha[t] - alpha[t + 1]) ** 2
        for t in range(M)
    )
    assert energy == 1 / rho

    norm2 = sum(
        layer_size(a, b, t) * x_values[t] ** 2
        for t in range(a + b + 1)
    )
    assert norm2 >= Fraction(3 * D, 4)

    return D, R, nullity, rank, rho, energy, norm2


def main():
    cases = [
        (16, 16, 16, 1),
        (24, 24, 24, dimension(24, 24) // 512),
        (40, 80, 40, dimension(80, 40) // 512),
    ]
    for case in cases:
        D, R, nullity, rank, rho, energy, norm2 = check_case(*case)
        print(
            f"OK N,a,b,Q={case}; D={D}; R={R}; nullity={nullity}; "
            f"rank={rank}; exact energy={energy}; exact norm^2={norm2}"
        )


if __name__ == "__main__":
    main()
