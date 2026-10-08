"""Exact arithmetic ledger for the smaller D(5,q) simplex candidate.

This checks only primality certificates, parameter counts, and the finite
spectral/rank budget. It does not construct D(5,q), enumerate E, certify the
CAT(-1) links, or formalize the approximate-permutation proof.
"""

from __future__ import annotations

import json
from decimal import Decimal, localcontext
from fractions import Fraction
from math import comb, gcd, isqrt, prod
from pathlib import Path


def prime_by_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def pocklington_certificate(n: int, witness: int, factors: dict[int, int]) -> dict:
    """Check a full n-1 factorization and the full-factor Pocklington tests."""
    assert prod(p**e for p, e in factors.items()) == n - 1
    assert pow(witness, n - 1, n) == 1
    checks = {}
    for p in factors:
        residue = pow(witness, (n - 1) // p, n)
        g = gcd(residue - 1, n)
        assert g == 1
        checks[str(p)] = {"residue": str(residue), "gcd_residue_minus_one_n": g}
    return {
        "n": str(n),
        "n_minus_one_factorization": {str(p): e for p, e in factors.items()},
        "witness": witness,
        "fermat_residue": pow(witness, n - 1, n),
        "factor_checks": checks,
    }


def decimal_approx(x: Fraction, places: int = 24) -> str:
    with localcontext() as ctx:
        ctx.prec = places
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def count_record(x: int) -> dict:
    return {"exact": str(x), "decimal_digits": len(str(x)), "bits": x.bit_length()}


def main() -> None:
    q = 6_300_000_000_013
    r = 19_000
    theta0 = Fraction(83, 100)
    s = (q - 3) // 2
    m = q**5
    n_marks = comb(s + 5, 5)
    rho = Fraction(n_marks, m)
    mu = Fraction((q - 1) * n_marks, m)

    # Nested full-factor Pocklington certificates for q-1 and its large prime.
    p = 16_935_483_871
    p_cert = pocklington_certificate(
        p,
        3,
        {2: 1, 3: 2, 5: 1, 617: 1, 304_979: 1},
    )
    assert prime_by_trial(617)
    assert prime_by_trial(304_979)
    q_cert = pocklington_certificate(q, 2, {2: 2, 3: 1, 31: 1, p: 1})

    # The exact integer inequality implies theta=1-log(r)/(2log(q)) >= 83/100.
    assert q**17 >= r**50

    # Use an outward integer square-root bound in the spectral exception estimate.
    sqrt_q_upper = isqrt(q) + 1
    e_fraction = (
        Fraction((2 * sqrt_q_upper + 1) ** 2)
        * rho
        * (1 - rho)
        / (mu - 4 * r * r) ** 2
    )
    delta_lower = rho * theta0 * r / 2 - 2 - r * e_fraction

    # S_inc <= N(q-1), delta=lambda=1/(100rq), and theta<=1.
    error_upper = (
        rho
        * r
        * Fraction(q - 1, 100 * q)
        + rho * r * Fraction(1, 400 * q)
    )
    margin = delta_lower - error_upper

    assert mu > 4 * r * r
    assert e_fraction < Fraction(1, 2 * r)
    assert margin > 0

    incidences = n_marks * (q - 1)
    edge_upper = n_marks * r * r + 2 * incidences
    triangle_upper = incidences * r * r
    rectangles = n_marks * r * r * (r - 1) ** 2
    height = (rectangles - 1).bit_length()
    assert height == 258
    leaf_word_length = 2 * height + 6
    balanced_word_bound = (1 << height) * leaf_word_length * rectangles
    lost_incidence_fraction = Fraction(q, q - 1) * e_fraction / rho
    triangle_lower_ratio = 1 - lost_incidence_fraction

    result = {
        "scope": "exact arithmetic only; graph, E ledger, CAT links, and rank theorem not certified here",
        "parameters": {"q": q, "r": r, "s": s, "theta_lower": "83/100"},
        "primality": {
            "large_factor_of_q_minus_one": p_cert,
            "small_factors_trial_divided": {
                "617_through_24": True,
                "304979_through_552": True,
            },
            "q": q_cert,
        },
        "spectral_rank_budget": {
            "q_pow_17_ge_r_pow_50": True,
            "sqrt_q_integer_upper_bound": sqrt_q_upper,
            "rho_exact": f"{rho.numerator}/{rho.denominator}",
            "rho_decimal": decimal_approx(rho),
            "mu_exact": f"{mu.numerator}/{mu.denominator}",
            "mu_decimal": decimal_approx(mu),
            "degree_threshold_4r2": 4 * r * r,
            "exceptional_fraction_upper_exact": f"{e_fraction.numerator}/{e_fraction.denominator}",
            "exceptional_fraction_upper_decimal": decimal_approx(e_fraction),
            "exceptional_fraction_threshold": f"1/{2*r}",
            "gap_over_m_lower_exact": f"{delta_lower.numerator}/{delta_lower.denominator}",
            "gap_over_m_lower_decimal": decimal_approx(delta_lower),
            "error_over_m_upper_exact_theta_le_1": f"{error_upper.numerator}/{error_upper.denominator}",
            "error_over_m_upper_decimal": decimal_approx(error_upper),
            "gap_minus_error_exact": f"{margin.numerator}/{margin.denominator}",
            "gap_minus_error_decimal": decimal_approx(margin),
        },
        "sizes": {
            "m_points": count_record(m),
            "N_marks_and_lines": count_record(n_marks),
            "incidences": count_record(incidences),
            "edge_symbols_upper": count_record(edge_upper),
            "triangle_cells_upper": count_record(triangle_upper),
            "rectangle_leaves": count_record(rectangles),
            "balanced_common_word_length_upper": count_record(balanced_word_bound),
            "binary_conjugator_height": height,
            "leaf_word_length_upper": leaf_word_length,
            "regular_incidence_fraction_lower": decimal_approx(triangle_lower_ratio),
        },
        "materialization": {
            "prime_and_budget_arithmetic_checked": True,
            "D5q_graph_materialized": False,
            "exception_set_E_enumerated": False,
            "presentation_materialized": False,
            "common_kernel_word_materialized": False,
        },
    }

    out = Path(__file__).with_name("parameter_certificate.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
