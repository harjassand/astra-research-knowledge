#!/usr/bin/env python3
"""Exact N=3 test of the Dicke phase-twirl identity over Q(i).

This diagnostic uses Fraction arithmetic only.  It checks the full 8x8
computational-basis density matrix for a two-atom rational product ensemble,
then compares it entrywise with the Dicke-sector formula.  It is an exact
small-instance check, not a proof of the all-N identity or of Cycle 3's
uniform scalar approximation theorem.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from math import comb
from pathlib import Path


@dataclass(frozen=True)
class GQ:
    re: Fraction = Fraction(0)
    im: Fraction = Fraction(0)

    def __add__(self, other: "GQ") -> "GQ":
        return GQ(self.re + other.re, self.im + other.im)

    def __sub__(self, other: "GQ") -> "GQ":
        return GQ(self.re - other.re, self.im - other.im)

    def __mul__(self, other: "GQ") -> "GQ":
        return GQ(self.re * other.re - self.im * other.im,
                  self.re * other.im + self.im * other.re)

    def conjugate(self) -> "GQ":
        return GQ(self.re, -self.im)

    def scale(self, scalar: Fraction) -> "GQ":
        return GQ(self.re * scalar, self.im * scalar)


ZERO = GQ()
ONE = GQ(Fraction(1))
I = GQ(Fraction(0), Fraction(1))


def product_vector(a: Fraction, b: Fraction, phase: GQ, n: int) -> list[GQ]:
    """Computational vector for (a|0> + b phase |1>)^tensor n."""
    phased_b = GQ(b) * phase
    out = []
    for x in range(1 << n):
        k = x.bit_count()
        amp = GQ(a ** (n - k))
        for _ in range(k):
            amp = amp * phased_b
        out.append(amp)
    return out


def fraction_text(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main() -> None:
    n = 3
    # Rational Pythagorean pairs: a^2+b^2=1 exactly.
    atoms = [
        (Fraction(2, 7), Fraction(3, 5), Fraction(4, 5)),
        (Fraction(5, 7), Fraction(5, 13), Fraction(12, 13)),
    ]
    phases = [ONE, I, GQ(Fraction(-1)), GQ(Fraction(0), Fraction(-1))]
    dim = 1 << n
    observed = [[ZERO for _ in range(dim)] for _ in range(dim)]

    for atom_weight, a, b in atoms:
        assert a * a + b * b == 1
        for phase in phases:
            v = product_vector(a, b, phase, n)
            label_weight = atom_weight / len(phases)
            for x in range(dim):
                for y in range(dim):
                    observed[x][y] = observed[x][y] + (v[x] * v[y].conjugate()).scale(label_weight)

    sector_mass: list[Fraction] = []
    for k in range(n + 1):
        mass = sum((w * comb(n, k) * (b * b) ** k * (a * a) ** (n - k)
                    for w, a, b in atoms), Fraction(0))
        sector_mass.append(mass)

    expected = [[ZERO for _ in range(dim)] for _ in range(dim)]
    for x in range(dim):
        kx = x.bit_count()
        for y in range(dim):
            if y.bit_count() == kx:
                entry = sector_mass[kx] / comb(n, kx)
                expected[x][y] = GQ(entry)

    assert observed == expected, "exact phase-twirl matrix does not match Dicke formula"
    assert sum(sector_mass, Fraction(0)) == 1, "sector probabilities do not normalize"
    assert all(mass > 0 for mass in sector_mass), "a Dicke sector has zero weight"

    # The per-string diagonal is the Dicke eigenvalue divided by the sector
    # multiplicity.  This explicitly catches the common binomial-factor error.
    per_string = [sector_mass[k] / comb(n, k) for k in range(n + 1)]
    assert per_string[1] != sector_mass[1]
    assert per_string[2] != sector_mass[2]
    for x in range(dim):
        k = x.bit_count()
        assert observed[x][x].re == per_string[k]
        assert observed[x][x].im == 0

    result = {
        "status": "EXACT_FINITE_DIAGNOSTIC_ONLY",
        "arithmetic": "fractions.Fraction over Q(i), no floating point",
        "N": n,
        "phase_order": n + 1,
        "atom_weights": [fraction_text(w) for w, _, _ in atoms],
        "atom_amplitudes": [
            {"a": fraction_text(a), "b": fraction_text(b), "p=b^2": fraction_text(b * b)}
            for _, a, b in atoms
        ],
        "sector_probabilities": [fraction_text(x) for x in sector_mass],
        "per_string_diagonal_by_weight": [fraction_text(x) for x in per_string],
        "full_8_by_8_matrix_matches_exact_Dicke_formula": True,
        "normalization_exact": True,
        "all_sector_weights_strictly_positive": True,
        "binomial_multiplicity_mismatch_witnessed": True,
        "limitations": [
            "tests only N=3 and a hand-chosen two-atom rational mixture",
            "does not establish the Cycle 3 scalar approximation theorem",
            "does not test the approximate rational phase construction for general N",
            "does not expand or time a 2^N-dimensional output"
        ]
    }
    out = Path(__file__).with_name("check_exact_twirl.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
