#!/usr/bin/env python3
"""Finite diagnostic for the rational Newton/Gauss-support identities.

This is not a proof of the uniform tail bound or the exact Sturm precision
ledger. It checks small N using high-precision mpmath roots and exponentials,
then rationalizes coefficients, nodes, and quadrature weights and compares
the resulting finite positive mixture with the same Newton polynomial.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import mpmath as mp


BITS = 220
mp.mp.dps = 180


def dyadic_floor(value: mp.mpf, bits: int = BITS) -> Fraction:
    scale = 1 << bits
    return Fraction(int(mp.floor(value * scale)), scale)


def legendre_and_derivative_at(q: int, x: Fraction) -> tuple[Fraction, Fraction]:
    if q == 0:
        return Fraction(1), Fraction(0)
    p0, p1 = Fraction(1), x
    d0, d1 = Fraction(0), Fraction(1)
    if q == 1:
        return p1, d1
    for n in range(2, q + 1):
        pn = (Fraction(2 * n - 1) * x * p1 - Fraction(n - 1) * p0) / n
        dn = (Fraction(2 * n - 1) * (p1 + x * d1) - Fraction(n - 1) * d0) / n
        p0, p1 = p1, pn
        d0, d1 = d1, dn
    return p1, d1


def newton_coefficients_mp(N: int, m: int) -> tuple[list[mp.mpf], list[mp.mpf]]:
    nodes = [(mp.mpf(N) / 2 + i) ** 2 for i in range(1, m + 1)]
    exponentials = [mp.exp(-u / N) for u in nodes]
    coeffs: list[mp.mpf] = []
    for ell in range(m):
        val = mp.mpf(0)
        for i in range(ell + 1):
            denom = mp.mpf(1)
            for j in range(ell + 1):
                if i != j:
                    denom *= nodes[i] - nodes[j]
            val += (-1) ** ell * exponentials[i] / denom
        coeffs.append(val)
    return coeffs, nodes


def beta_normalizers(N: int, m: int) -> list[int]:
    out = []
    for ell in range(m):
        c = N + 1
        for j in range(2 * ell):
            c *= N + 2 + j
        out.append(c)
    return out


def run_case(N: int) -> dict[str, object]:
    m = 2 * N
    degree = N + 2 * m - 2
    q = (degree + 2) // 2
    coeffs_mp, nodes = newton_coefficients_mp(N, m)
    nodes_q = [Fraction((N + 2 * i) ** 2, 4) for i in range(1, m + 1)]

    # Rational positive coefficient extraction from the Lagrange sum.
    coeffs_q = []
    for ell in range(m):
        value = Fraction(0)
        for i in range(ell + 1):
            denom = Fraction(1)
            for j in range(ell + 1):
                if i != j:
                    denom *= nodes_q[i] - nodes_q[j]
            value += Fraction((-1) ** ell, 1) * dyadic_floor(mp.exp(-nodes[i] / N)) / denom
        coeffs_q.append(value)

    xs, ws = mp.gauss_quadrature(q, "legendre")
    xq = [dyadic_floor(x) for x in xs]
    p_atoms = [(x + 1) / 2 for x in xq]
    # Evaluate the shifted Gauss weight formula at the rational root approximation.
    omega_atoms = []
    for x in xq:
        _, derivative = legendre_and_derivative_at(q, x)
        omega_atoms.append(1 / ((1 - x * x) * derivative * derivative))

    norms = beta_normalizers(N, m)

    def density(p: Fraction) -> Fraction:
        z = p * (1 - p)
        result = Fraction(0)
        power = Fraction(1)
        for ell in range(m):
            result += coeffs_q[ell] * norms[ell] * power
            power *= z
        return result

    def polynomial_population(k: int) -> Fraction:
        result = Fraction(0)
        basis = 1
        for ell in range(m):
            result += coeffs_q[ell] * basis
            if ell < m - 1:
                basis *= (ell + 1 + k) * (ell + 1 + N - k)
        return result

    def finite_support_population(k: int) -> Fraction:
        result = Fraction(0)
        choose = math.comb(N, k)
        for p, omega in zip(p_atoms, omega_atoms):
            if not (0 < p < 1 and omega > 0 and density(p) > 0):
                raise AssertionError("rational atom or weight is not positive")
            bernoulli = Fraction(choose) * p**k * (1 - p) ** (N - k)
            result += omega * density(p) * bernoulli
        return result

    max_quad_rel = mp.mpf(0)
    max_target_defect = mp.mpf(0)
    for k in range(N + 1):
        poly = polynomial_population(k)
        mixture = finite_support_population(k)
        target = mp.exp(-(mp.mpf(2 * k - N) / 2) ** 2 / N)
        poly_mp = mp.mpf(poly.numerator) / poly.denominator
        mix_mp = mp.mpf(mixture.numerator) / mixture.denominator
        max_quad_rel = max(max_quad_rel, abs(mix_mp - poly_mp) / target)

        exact_poly = mp.mpf(0)
        basis = 1
        for ell, coeff in enumerate(coeffs_mp):
            exact_poly += coeff * basis
            if ell < m - 1:
                basis *= (ell + 1 + k) * (ell + 1 + N - k)
        max_target_defect = max(max_target_defect, abs(target - exact_poly) / target)

    if not all(c > 0 for c in coeffs_q):
        raise AssertionError("a rationalized Newton coefficient is nonpositive")

    return {
        "N": N,
        "newton_terms": m,
        "gauss_atoms": q,
        "all_rational_newton_coefficients_positive": True,
        "all_rationalized_support_weights_positive": True,
        "max_relative_gauss_vs_rational_newton_population": mp.nstr(max_quad_rel, 12),
        "max_observed_relative_truncation_defect": mp.nstr(max_target_defect, 12),
        "target_uniform_theorem_bound": "not tested at these small N; analytic proof is in RESULT.txt"
    }


def main() -> None:
    result = {
        "status": "FINITE_NUMERICAL_DIAGNOSTIC_ONLY",
        "mpmath_version": mp.__version__,
        "decimal_precision": mp.mp.dps,
        "dyadic_bits": BITS,
        "cases": [run_case(n) for n in (1, 2, 3, 4, 6, 8, 10)],
        "limitations": [
            "does not certify the uniform Chernoff or coefficient-conditioning bounds",
            "uses high-precision numerical Gauss roots instead of the Sturm isolation implementation",
            "does not validate N117, an operator-level separability theorem, or external priority"
        ]
    }
    out = Path(__file__).with_name("check_finite_support.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
