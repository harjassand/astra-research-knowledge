#!/usr/bin/env python3
"""Exact Clifford/Fierz check for the Spin(9) pure-spinor grade moments.

Uses S_R=O^2 and the real symmetric Clifford matrices
  Gamma_a = [[0,L_{e_a}],[L_{e_a}^T,0]], a=0,...,7,
  Gamma_8 = diag(I_8,-I_8),
with octonion multiplication fixed by the listed Fano triples.  The canonical
spinor is psi=a e_0 + i b(u e_1+v e_8), where e_1 is vertical and e_8
horizontal at x=e_0. Exact polynomial reduction imposes a^2+b^2=u^2+v^2=1.

This validates the formula from an explicit representation; completeness of
the (p,t) orbit parameters is proved in REPORT.md.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


FANO_TRIPLES = (
    (1, 2, 3),
    (1, 4, 5),
    (1, 7, 6),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 6, 5),
)


def octonion_left_multipliers() -> list[sp.Matrix]:
    # e_0=1 and e_i^2=-1 for imaginary units. Each oriented Fano triple
    # (i,j,k) means e_i e_j=e_k, e_j e_k=e_i, e_k e_i=e_j.
    products: dict[tuple[int, int], tuple[int, int]] = {}
    for i in range(8):
        products[i, i] = (1, 0) if i == 0 else (-1, 0)
    for i in range(1, 8):
        products[0, i] = (1, i)
        products[i, 0] = (1, i)
    for a, b, c in FANO_TRIPLES:
        for i, j, k in ((a, b, c), (b, c, a), (c, a, b)):
            products[i, j] = (1, k)
            products[j, i] = (-1, k)

    if len(products) != 64:
        raise AssertionError("octonion multiplication table is incomplete")

    left = []
    for i in range(8):
        matrix = sp.zeros(8)
        for j in range(8):
            sign, k = products[i, j]
            matrix[k, j] = sign
        left.append(matrix)
    return left


def spin9_real_clifford() -> list[sp.Matrix]:
    left = octonion_left_multipliers()
    gamma: list[sp.Matrix] = []
    for multiplier in left:
        matrix = sp.zeros(16)
        matrix[:8, 8:] = multiplier
        matrix[8:, :8] = multiplier.T
        gamma.append(matrix)
    last = sp.zeros(16)
    last[:8, :8] = sp.eye(8)
    last[8:, 8:] = -sp.eye(8)
    gamma.append(last)

    identity = sp.eye(16)
    for i, Gi in enumerate(gamma):
        assert Gi == Gi.T
        assert Gi * Gi == identity
        for j, Gj in enumerate(gamma):
            assert Gi * Gj + Gj * Gi == 2 * int(i == j) * identity
    return gamma


def exact_moments(gamma: list[sp.Matrix]) -> tuple[sp.Expr, ...]:
    a, b, u, v = sp.symbols("a b u v", real=True)
    psi = sp.zeros(16, 1)
    psi[0] = a
    psi[1] = sp.I * b * u
    psi[8] = sp.I * b * v

    moments = []
    for grade in range(1, 5):
        total = sp.Integer(0)
        phase = sp.I ** (grade * (grade - 1) // 2)
        for indices in combinations(range(9), grade):
            form = sp.eye(16)
            for index in indices:
                form = form * gamma[index]
            expectation = sp.expand_complex(
                (psi.conjugate().T * (phase * form) * psi)[0]
            )
            if sp.im(expectation) != 0:
                raise AssertionError((grade, indices, expectation))
            expectation = sp.re(expectation)
            total += expectation**2
        moments.append(sp.factor(sp.expand(total)))
    return tuple(moments)


def main() -> None:
    gamma = spin9_real_clifford()
    moments = exact_moments(gamma)
    a, b, u, v = sp.symbols("a b u v", real=True)
    p = (a**2 - b**2) ** 2
    expected = (
        p + 4 * a**2 * b**2 * u**2,
        4 * a**2 * b**2 * (1 + 3 * u**2),
        4 * a**2 * b**2 * (7 - 3 * u**2),
        7 * (1 + p) - 4 * a**2 * b**2 * u**2,
    )

    # Reduce exactly modulo the unit-norm constraints a^2+b^2=1 and
    # u^2+v^2=1.  In this representative p=(a^2-b^2)^2 and t=u^2.
    for grade, (observed, target) in enumerate(zip(moments, expected), 1):
        remainder = sp.reduced(
            sp.expand(observed - target),
            [b**2 - (1 - a**2), v**2 - (1 - u**2)],
            b,
            v,
            a,
            u,
        )[1]
        assert sp.expand(remainder) == 0, (grade, remainder)
        print(f"grade {grade}: {sp.factor(target)}")

    # A phase-invariant quartic resolves the p=0 phase ambiguity.  Under
    # psi -> exp(i phi) psi, each q_i=psi^T Gamma_i psi gets the same phase
    # exp(2 i phi), so sum |q_i|^2 is unchanged.
    psi = sp.zeros(16, 1)
    psi[0] = a
    psi[1] = sp.I * b * u
    psi[8] = sp.I * b * v
    q = tuple((psi.T * Gi * psi)[0] for Gi in gamma)
    q_norm = sp.factor(sum(entry * sp.conjugate(entry) for entry in q))
    q_target = 1 + (1 - p) * (1 - 2 * u**2)
    q_remainder = sp.reduced(
        sp.expand(q_norm - q_target),
        [b**2 - (1 - a**2), v**2 - (1 - u**2)],
        b,
        v,
        a,
        u,
    )[1]
    assert sp.expand(q_remainder) == 0
    print("phase-invariant quartic: sum_i |psi^T Gamma_i psi|^2 = 1+(1-p)(1-2t)")

    # Endpoint seeds: real, balanced horizontal, balanced vertical.
    endpoint_data = (
        (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(1), (1, 0, 0, 14)),
        (sp.sqrt(2) / 2, sp.sqrt(2) / 2, sp.Integer(0), sp.Integer(1), (0, 1, 7, 7)),
        (sp.sqrt(2) / 2, sp.sqrt(2) / 2, sp.Integer(1), sp.Integer(0), (1, 4, 4, 6)),
    )
    for aa, bb, uu, vv, target in endpoint_data:
        values = tuple(
            sp.simplify(moment.subs({a: aa, b: bb, u: uu, v: vv}))
            for moment in moments
        )
        assert values == target, (values, target)
    print("real / balanced-horizontal / balanced-vertical endpoints: PASS")
    print("explicit Spin(9) real Clifford/Fierz checks: PASS")


if __name__ == "__main__":
    main()
