#!/usr/bin/env python3
"""Finite exact checks of the diagonal covariance rejection identities.

This validates formulas on small rational fixtures only; it is not a proof of
Theorem PC-15 or of the general finite-bit sampler.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import json
from pathlib import Path

getcontext().prec = 60

CASES = [
    {"A": [Fraction(4, 5), Fraction(1, 1)], "eps": Fraction(1, 5),
     "t": Fraction(1, 10), "counts": [2, None]},
    {"A": [Fraction(9, 10), Fraction(11, 10)], "eps": Fraction(1, 10),
     "t": Fraction(3, 1), "counts": [7, None]},
    {"A": [Fraction(6, 5), Fraction(4, 5)], "eps": Fraction(1, 5),
     "t": Fraction(1, 50), "counts": [4, None]},
]


def dec(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def frac_text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


rows = []
for idx, case in enumerate(CASES, start=1):
    vals = case["A"]
    eps = case["eps"]
    t = case["t"]
    c = 1 + eps
    counts = case["counts"]
    assert all(1 - eps <= a <= c for a in vals)
    assert t > 0 and all(a > 0 for a in vals)

    dvals = [1 / a - 1 / c for a in vals]
    assert all(d >= 0 for d in dvals)
    d_modes = len(vals)
    M = c**d_modes
    for a in vals:
        M /= a

    heralded = [(a, k) for a, k in zip(vals, counts) if k is not None]
    p_h = Fraction(1)
    q_h = Fraction(1)
    for a, k in heralded:
        p_h *= (a * t) ** k / (1 + a * t) ** (k + 1)
        q_h *= (c * t) ** k / (1 + c * t) ** (k + 1)

    alpha_ratio = p_h / (M * q_h)
    alpha_integral = Fraction(1)
    exponent = Fraction(0)
    for a, k, d in zip(vals, counts, dvals):
        if k is None:
            alpha_integral /= 1 + d * c
            exponent += d * c
        else:
            alpha_integral /= (1 + d * c / (1 + c * t)) ** (k + 1)
            exponent += d * c * (k + 1) / (1 + c * t)
    assert alpha_integral == alpha_ratio, (idx, alpha_integral, alpha_ratio)

    lower = (-dec(exponent)).exp()
    alpha_decimal = dec(alpha_integral)
    assert alpha_decimal + Decimal("1e-55") >= lower
    rows.append({
        "case": idx,
        "A": [frac_text(a) for a in vals],
        "eps_bar": frac_text(eps),
        "t": frac_text(t),
        "herald_counts": [k for k in counts if k is not None],
        "M": frac_text(M),
        "alpha_integral": frac_text(alpha_integral),
        "alpha_equals_p_over_Mq_exactly": True,
        "jensen_exponent": frac_text(exponent),
        "jensen_bound_decimal": str(lower),
        "jensen_bound_passes_numerically": True,
    })

result = {
    "status": "FINITE-EVIDENCE",
    "scope": "Exact rational identity and numerical Jensen checks on three diagonal two-mode fixtures; not theorem validation.",
    "fixtures": rows,
}
Path("outputs/research/photonic_complexity/conditional_gaussian_rejection_check.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
