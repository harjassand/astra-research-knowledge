#!/usr/bin/env python3
"""Small exact checks for the central-binomial witness in the phase-3 audit."""

from fractions import Fraction
from math import comb, erf, exp, log, sqrt
import json
from pathlib import Path


def central_mass(n: int, left: int, p: Fraction) -> Fraction:
    q = 1 - p
    return sum(
        (Fraction(comb(n, k)) * p**k * q ** (n - k)
         for k in range(left, n - left + 1)),
        Fraction(0),
    )


def normal_cdf(x: float) -> float:
    return (1.0 + erf(x / sqrt(2.0))) / 2.0


def finite_distance(n: int, kappa: float) -> float:
    denom = 2**n
    base = [comb(n, k) / denom for k in range(n + 1)]
    weights = [exp(-kappa * (k - n / 2) ** 2 / n) for k in range(n + 1)]
    z = sum(p * w for p, w in zip(base, weights))
    return 0.5 * sum(p * abs(w / z - 1.0) for p, w in zip(base, weights))


def main() -> None:
    rational_checks = 0
    largest_excess = Fraction(0)
    for n in range(1, 15):
        for left in range(n // 2 + 1):
            at_half = central_mass(n, left, Fraction(1, 2))
            for denominator in range(2, 18):
                for numerator in range(denominator + 1):
                    p = Fraction(numerator, denominator)
                    excess = central_mass(n, left, p) - at_half
                    largest_excess = max(largest_excess, excess)
                    assert excess <= 0, (n, left, p, excess)
                    rational_checks += 1

    kappa = 2.0
    beta = 1.0 + kappa / 2.0
    a = sqrt(2.0 * log(beta) / kappa)
    limit = 2.0 * (normal_cdf(a * sqrt(beta)) - normal_cdf(a))
    sizes = [16, 64, 256, 1024, 4096]
    finite = {str(n): finite_distance(n, kappa) for n in sizes}
    result = {
        "status": "PASS",
        "exact_rational_central_interval_checks": rational_checks,
        "largest_checked_mass_excess_over_p_half": str(largest_excess),
        "kappa": kappa,
        "gaussian_limit_tv": limit,
        "finite_n_tv": finite,
        "note": "The checks are diagnostics only; the derivative identity and CLT proof are in PHASE3_GROWING_ANISOTROPY_AUDIT.txt."
    }
    out = Path(__file__).with_name("growing_boundary_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
