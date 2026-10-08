#!/usr/bin/env python3
"""Independent exact reconstruction of the j=3/2 dipole-quadrupole star blocks."""

from __future__ import annotations

import sympy as sp
from sympy.physics.wigner import clebsch_gordan


J = sp.Rational(3, 2)
D = 4
M_VALUES = (J, J - 1, J - 2, -J)
IDENT = sp.eye(D)


def spin_matrices() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    jp = sp.zeros(D)
    jm = sp.zeros(D)
    for col, m in enumerate(M_VALUES):
        if m < J:
            jp[M_VALUES.index(m + 1), col] = sp.sqrt((J - m) * (J + m + 1))
        if m > -J:
            jm[M_VALUES.index(m - 1), col] = sp.sqrt((J + m) * (J - m + 1))
    return (jp + jm) / 2, (jp - jm) / (2 * sp.I), sp.diag(*M_VALUES)


def hs_norm2(op: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(op * op) / D)


def sector_bases() -> tuple[list[sp.Matrix], list[sp.Matrix]]:
    jx, jy, jz = spin_matrices()
    rank1 = [sp.sqrt(sp.Rational(4, 5)) * op for op in (jx, jy, jz)]
    casimir = jx**2 + jy**2 + jz**2
    raw2 = [
        3 * jz**2 - casimir,
        jx * jz + jz * jx,
        jy * jz + jz * jy,
        jx**2 - jy**2,
        jx * jy + jy * jx,
    ]
    rank2 = [sp.simplify(op / sp.sqrt(hs_norm2(op))) for op in raw2]
    assert all(hs_norm2(op) == 1 for op in rank1 + rank2)
    assert all(
        sp.simplify(sp.trace(rank2[i] * rank2[j]) / D) == 0
        for i in range(5)
        for j in range(i)
    )
    return rank1, rank2


def star(basis: list[sp.Matrix]) -> sp.Matrix:
    h = sp.zeros(D**3)
    for op in basis:
        h += (
            sp.kronecker_product(op.T, op, IDENT)
            + sp.kronecker_product(op.T, IDENT, op)
        )
    return h.applyfunc(sp.simplify)


def spin_flip() -> sp.Matrix:
    """Unitary identifying the conjugate reference spin with an ordinary spin."""
    y = sp.zeros(D)
    for col, m in enumerate(M_VALUES):
        y[M_VALUES.index(-m), col] = (-1) ** int(J - m)
    return y


def coupled_vector(s: int, total_f: sp.Rational, total_m: sp.Rational) -> sp.Matrix:
    vector = sp.zeros(D**3, 1)
    for i, mr in enumerate(M_VALUES):
        for j, mb1 in enumerate(M_VALUES):
            pair_m = mr + mb1
            c1 = clebsch_gordan(J, J, sp.Integer(s), mr, mb1, pair_m)
            if c1 == 0:
                continue
            for k, mb2 in enumerate(M_VALUES):
                if pair_m + mb2 != total_m:
                    continue
                c2 = clebsch_gordan(sp.Integer(s), J, total_f, pair_m, mb2, total_m)
                if c2 != 0:
                    vector[(i * D + j) * D + k] += c1 * c2
    return vector.applyfunc(sp.simplify)


def allowed_pair_spins(total_f: sp.Rational) -> list[int]:
    return [
        s
        for s in range(4)
        if abs(sp.Integer(s) - J) <= total_f <= sp.Integer(s) + J
    ]


def block(h: sp.Matrix, total_f: sp.Rational) -> sp.Matrix:
    spins = allowed_pair_spins(total_f)
    basis = [coupled_vector(s, total_f, total_f) for s in spins]
    for i in range(len(basis)):
        for j in range(len(basis)):
            assert sp.simplify((basis[i].conjugate().T * basis[j])[0]) == int(i == j)
    return sp.Matrix(
        [
            [
                sp.simplify((basis[i].conjugate().T * h * basis[j])[0])
                for j in range(len(basis))
            ]
            for i in range(len(basis))
        ]
    )


def main() -> None:
    rank1, rank2 = sector_bases()
    h1, h2 = star(rank1), star(rank2)
    flip = sp.kronecker_product(spin_flip(), IDENT, IDENT)
    # The reference is a conjugate spin. After this identification, rank ell
    # picks up the standard spin-flip phase (-1)^ell.
    h1 = flip * h1 * flip.conjugate().T
    h2 = flip * h2 * flip.conjugate().T
    expected_h1 = {
        sp.Rational(1, 2): [sp.Rational(18, 5), 2],
        sp.Rational(3, 2): [sp.Rational(24, 5), sp.Rational(12, 5), sp.Rational(4, 5), 0],
        sp.Rational(5, 2): [sp.Rational(14, 5), sp.Rational(2, 5), sp.Rational(-6, 5)],
        sp.Rational(7, 2): [0, sp.Rational(-12, 5)],
        sp.Rational(9, 2): [sp.Rational(-18, 5)],
    }
    expected_h2 = {
        sp.Rational(1, 2): [0, -4],
        sp.Rational(3, 2): [6, 2, 2 * sp.sqrt(5), -2 * sp.sqrt(5)],
        sp.Rational(5, 2): [2, 0, -4],
        sp.Rational(7, 2): [0, -4],
        sp.Rational(9, 2): [2],
    }
    total_fs = list(expected_h1)
    blocks1 = {}
    blocks2 = {}
    for f in total_fs:
        blocks1[f] = block(h1, f)
        blocks2[f] = block(h2, f)
        spec1 = sorted(blocks1[f].eigenvals().keys(), reverse=True)
        spec2 = sorted(blocks2[f].eigenvals().keys(), reverse=True)
        assert spec1 == sorted(expected_h1[f], reverse=True)
        assert spec2 == sorted(expected_h2[f], reverse=True)
        print(f"F={f}: exact rank-1 and rank-2 block spectra PASS")

    x, a, b = sp.symbols("x a b")
    mixed = a * blocks1[sp.Rational(3, 2)] + b * blocks2[sp.Rational(3, 2)]
    observed = sp.factor(mixed.charpoly(x).as_expr())
    expected = (
        (5 * x**2 - 12 * a * x - 100 * b**2)
        * (
            25 * x**2
            - (140 * a + 200 * b) * x
            + 96 * a**2
            + 480 * a * b
            + 300 * b**2
        )
        / 125
    )
    assert sp.expand(observed - expected) == 0
    print("F=3/2 mixed characteristic polynomial PASS")


if __name__ == "__main__":
    main()
