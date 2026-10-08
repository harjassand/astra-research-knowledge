#!/usr/bin/env python3
"""Exact algebra and focused rational diagnostics for the narrow-wall proof.

The symbolic CPV-potential identity is exact in SymPy's rational function
field after alpha=C3/C2.  The carrier/output sweep uses Fraction arithmetic;
it is finite corroboration of the displayed inequalities, not their proof.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import sys

import sympy as sp

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "outputs/research/sol_semiclassical_memory/wall_su3/analytic_spectral_gate"))
import exact_potential as cpv  # noqa: E402


def symbolic_identity() -> None:
    a, b, r, delta, alpha_symbol, j = sp.symbols(
        "a b r delta alpha j"
    )
    poly = cpv.potential_polynomial()
    vars_ = (a, b, r, delta, alpha_symbol, j)
    raw_n2_p = sum(
        sp.Rational(value.numerator, value.denominator)
        * sp.prod(x**degree for x, degree in zip(vars_, monomial))
        for monomial, value in poly.c.items()
    )
    N = a + b
    C2 = (a**2 + a * b + b**2 + 3 * N) / 3
    C3 = (a - b) * (2 * a + b + 3) * (a + 2 * b + 3) / 18
    alpha = C3 / C2
    nu = (2 * a + b + 3) * b * (b + 2) / (3 * C2)
    assert sp.simplify(nu - ((2 * a + b + 3) / 3 - 2 * alpha)) == 0
    t0 = (nu - b) / 2
    w = a + 1 - nu
    compact = (
        (delta + 1) * (delta + 2) * j**2
        + (delta + 1)
        * ((N + 2) * w - delta * (delta + 2) - r * (2 * t0 + delta + 1))
        * j
        + r**2 * t0 * (t0 + delta)
        + r * delta * ((t0 + b) ** 2 + nu)
        + r * delta**2 * t0
        + r * (2 * t0**2 + b * (nu + 1))
        + delta * (delta + 1) * (t0 + b) * (t0 + b + 1)
    )
    assert sp.factor((raw_n2_p - compact).subs(alpha_symbol, alpha)) == 0

    Q = r + delta
    A_prev = (a - Q + j) * j * (j - delta) * (
        (a + 2 * b) / 3 + 2 * alpha + Q + 2 - j
    )
    C_j = (Q - j) * (r - j) * (b - j) * (
        (2 * a + b) / 3 - 2 * alpha + j + 2
    )
    # These are exactly the two directed CPV edge polynomials used in the
    # raw-potential construction, in the physical integer-index orientation.
    raw_a = (a - Q + j) * j * (j - delta) * (
        (a + 2 * b) / 3 + 2 * alpha_symbol + Q + 2 - j
    )
    raw_c = (Q - j) * (r - j) * (b - j) * (
        (2 * a + b) / 3 - 2 * alpha_symbol + j + 2
    )
    assert sp.factor(A_prev.subs(alpha, alpha) - raw_a.subs(alpha_symbol, alpha)) == 0
    assert sp.factor(C_j.subs(alpha, alpha) - raw_c.subs(alpha_symbol, alpha)) == 0
    print("PASS exact symbolic compact-potential and directed-rate identities")


def rational_diagnostics() -> None:
    carriers = [
        (99, 1),
        (199, 2),
        (999, 10),
        (9_900, 100),
        (99_000, 1_000),
        (999_900, 10_000),
    ]
    checked = 0
    for a, b in carriers:
        N = a + b
        eps = F(b, N)
        assert eps <= F(1, 100)
        C2 = F(a * a + a * b + b * b + 3 * N, 3)
        alpha = F((a - b) * (2 * a + b + 3) * (a + 2 * b + 3), 18) / C2
        nu = F((2 * a + b + 3) * b * (b + 2), 3) / C2
        t0 = (nu - b) / 2
        w = a + 1 - nu
        assert nu <= 9 * eps * b
        assert w >= F(98, 100) * N
        assert t0 * t0 >= F(b * b, 5)
        q_bound = isqrt(3 * N // 100) + 2
        for p in range(q_bound + 1):
            for q in range(p, q_bound + 1):
                if (q - p) % 3:
                    continue
                delta = F(q - p, 3)
                r = F(2 * p + q, 3)
                Q = r + delta
                chi = r * r + r * delta + delta * delta + 2 * r + delta
                if chi > F(N, 100) or delta > min(r, b):
                    continue
                for j_int in range(int(delta), int(min(r, b)) + 1):
                    j = F(j_int)
                    z = F(b) * r / N
                    P0 = (
                        r**2 * t0 * (t0 + delta)
                        + r * delta * ((t0 + b) ** 2 + nu)
                        + r * delta**2 * t0
                        + r * (2 * t0**2 + b * (nu + 1))
                        + delta * (delta + 1) * (t0 + b) * (t0 + b + 1)
                    )
                    Pj = (
                        (delta + 1) * (delta + 2) * j**2
                        + (delta + 1)
                        * ((N + 2) * w - delta * (delta + 2) - r * (2 * t0 + delta + 1))
                        * j
                        + P0
                    ) / N**2
                    if j >= 1:
                        Aprev = (a - Q + j) * j * (j - delta) * (
                            F(a + 2 * b, 3) + 2 * alpha + Q + 2 - j
                        ) / N**2
                        Cj = (Q - j) * (r - j) * (b - j) * (
                            F(2 * a + b, 3) - 2 * alpha + j + 2
                        ) / N**2
                        assert Pj >= F(7, 10) * (delta + 1) * j + F(1, 5) * z**2
                        assert Aprev >= F(9, 10) * j * (j - delta)
                        assert Cj <= F(18, 100) * z**2 + F(4, 10_000) * j
                    checked += 1
    print(f"PASS exact Fraction diagnostics on {len(carriers)} carriers/{checked} fiber rows")


if __name__ == "__main__":
    symbolic_identity()
    rational_diagnostics()
