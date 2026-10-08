#!/usr/bin/env python3
"""Exact small-R fixture for the complement-LCU seed transition lemma.

Uses only fractions and the audited seed supports. This checks the local
one-copy row and the tensor-product support count for R<=5; the all-R result
in 05_connection_enforcers.md is proved by the displayed factorization.
"""

from fractions import Fraction
from itertools import product
from math import prod

PHI = {0b00010: +1, 0b10010: -1}
PSI = {
    0b00010: +1,
    0b01110: -1,
    0b10110: -1,
    0b11010: -1,
}


def local_projector_entry(support, x, y):
    if x not in support or y not in support:
        return Fraction()
    return Fraction(support[x] * support[y], len(support))


def complement_row(support, x):
    return {
        y: Fraction(int(x == y)) - local_projector_entry(support, x, y)
        for y in range(32)
        if Fraction(int(x == y)) - local_projector_entry(support, x, y)
    }


def mat_row_product(left, right, x):
    left_row = complement_row(left, x)
    answer = {}
    for y in range(32):
        value = sum(
            (coeff * complement_row(right, z).get(y, Fraction())
             for z, coeff in left_row.items()),
            Fraction(),
        )
        if value:
            answer[y] = value
    return answer


def main():
    phi, psi = PHI, PSI
    u = next(iter(phi))
    union = set(phi) | set(psi)
    arow = mat_row_product(phi, psi, u)
    expected_support = set(phi) | set(psi)
    assert set(arow) == expected_support
    assert arow[u] == Fraction(3, 8)
    assert arow[next(x for x in phi if x != u)] == Fraction(1, 2)
    for y in set(psi) - {u}:
        assert arow[y] == Fraction(1, 8)

    s_phi_r = set(product(phi, repeat=1))
    s_psi_r = set(product(psi, repeat=1))
    for r in range(1, 6):
        row_support = set(product(union, repeat=r))
        phi_support = set(product(phi, repeat=r))
        psi_support = set(product(psi, repeat=r))
        unique = row_support - (phi_support | psi_support)
        expected = len(union) ** r - len(phi) ** r - len(psi) ** r + 1
        assert len(unique) == expected

        # On y outside both pure tensor supports, only
        # 4(A_phi A_psi)^{tensor r} remains in R_phi,R R_psi,R.
        for y in unique:
            value = 4 * prod(arow[yr] for yr in y)
            assert value

        # Also count the complete transition row for a diagnostic. The
        # theorem only needs the `unique` subset lower bound.
        support_count = 0
        for y in row_support:
            value = 4 * prod(arow[yr] for yr in y)
            if y in phi_support:
                value -= 2 * prod(complement_row(phi, u)[yr] for yr in y)
            if y in psi_support:
                value -= 2 * prod(complement_row(psi, u)[yr] for yr in y)
            if y == (u,) * r:
                value += 1
            support_count += bool(value)
        print(f"R={r}: transition row support={support_count}, proved lower bound={expected}")

    assert len(s_phi_r) == 2 and len(s_psi_r) == 4
    print("exact seed-reflection transition fixture: PASS")


if __name__ == "__main__":
    main()
