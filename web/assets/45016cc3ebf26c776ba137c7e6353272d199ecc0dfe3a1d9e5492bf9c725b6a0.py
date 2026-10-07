#!/usr/bin/env python3
"""Exact rational diagnostics for the qubit post-composition example."""

from fractions import Fraction
import json
from pathlib import Path


def nearest_integer(x: Fraction) -> int:
    """Nearest integer, ties to even, implemented exactly."""
    q, r = divmod(x.numerator, x.denominator)
    twice = 2 * r
    if twice < x.denominator:
        return q
    if twice > x.denominator:
        return q + 1
    return q if q % 2 == 0 else q + 1


rows = []
for n in (2, 3, 4, 8, 16):
    s = Fraction(2 * n, n * n + 1)
    c = Fraction(n * n - 1, n * n + 1)
    s2 = s * s
    assert c * c + s2 == 1

    delta = s2 / (1 + s2)
    lam = 1 - delta
    m = nearest_integer(Fraction(1, 2) / delta)
    assert m >= 1
    assert 1 - s2 + s2 / delta == 2

    scaled_error_squared = Fraction(m) * lam ** (2 * m) * s2
    rows.append(
        {
            "n": n,
            "sin_alpha": str(s),
            "cos_alpha": str(c),
            "delta": str(delta),
            "lambda": str(lam),
            "m": m,
            "m_delta": str(m * delta),
            "m_error_squared": str(scaled_error_squared),
        }
    )

output = {
    "method": "exact Fraction arithmetic; finite checks only",
    "checks": "Pythagorean angle, optimal comparison constant 2, and exact norm formula",
    "rows": rows,
}
target = Path(__file__).with_name("postcomposition_rate_sharpness_checks.json")
target.write_text(json.dumps(output, indent=2) + "\n")
print(f"wrote {target}; exact checks passed for {len(rows)} rows")
