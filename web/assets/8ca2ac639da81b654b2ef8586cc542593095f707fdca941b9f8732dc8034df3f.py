#!/usr/bin/env python3
"""Certified dyadic interval evaluation of the diagonal Racah coefficient.

This is a finite diagnostic, not an asymptotic proof.  It evaluates the exact
terminating series

    eta = sum_{r=0}^l (-1)^r t_r,
    t_0 = 1,
    t_{r+1}/t_r = (L-r(r+1))^2 / ((r+1)^2 (N-r(r+2))),

using outward-rounded integer intervals with denominator 2**P.  Precision is
chosen from the certified majorant R_r <= z^2/(r+1)^2, where
z = L/sqrt(N).  The output interval endpoints are exact dyadic rationals.

No dependency on floating point is used in either the enclosure or the
precision choice.  Decimal strings are display-only and are rounded outward.
"""

from __future__ import annotations

import json
import math
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from pathlib import Path


def ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def ceil_log2_positive(k: int) -> int:
    assert k > 0
    return (k - 1).bit_length()


def z_upper(n: int, ell: int) -> Fraction:
    """Rational upper bound L/sqrt(N) using floor(sqrt(N))."""
    L = ell * (ell + 1)
    N = n * (n + 2)
    return Fraction(L, math.isqrt(N))


def precision_bits(n: int, ell: int, target_bits: int = 100) -> int:
    """P making the total eta interval width <= 2**(-target_bits).

    The recurrence interval incurs at most one fixed-point unit of width per
    step.  Every suffix product of the ratio majorants z^2/(r+1)^2 is <=
    exp(2z), so summing the l term-interval widths costs at most
    l(l+1) exp(2z) / 2**P.  Use ln(2)>693/1000 and z<=z_upper.
    """
    zu = z_upper(n, ell)
    exp_bits = ceil_fraction(Fraction(2000, 693) * zu)
    count_bits = ceil_log2_positive(ell * (ell + 1))
    return exp_bits + count_bits + target_bits + 2


def term_interval(n: int, ell: int, P: int) -> tuple[int, int, int]:
    """Return exact integer endpoints [lo,hi]/2**P for eta and width."""
    S = 1 << P
    lo = hi = S  # t_0 = 1 exactly
    elo = ehi = 0
    L = ell * (ell + 1)
    N = n * (n + 2)

    for r in range(ell + 1):
        if r & 1:
            elo -= hi
            ehi -= lo
        else:
            elo += lo
            ehi += hi
        if r == ell:
            break
        p = (L - r * (r + 1)) ** 2
        q = (r + 1) ** 2 * (N - r * (r + 2))
        assert p >= 0 and q > 0
        lo, hi = (lo * p) // q, (hi * p + q - 1) // q

    return elo, ehi, ehi - elo


def product_interval(n: int, ell: int, P: int) -> tuple[int, int, int]:
    """Exact outward enclosure of mu=prod_{s<ell}(n-s)/(n+s+2)."""
    S = 1 << P
    lo = hi = S
    for s in range(ell):
        p, q = n - s, n + s + 2
        lo, hi = (lo * p) // q, (hi * p + q - 1) // q
    return lo, hi, hi - lo


def outward_decimal(x: Fraction, places: int, upward: bool) -> str:
    with localcontext() as ctx:
        ctx.prec = max(places + 30, 80)
        dec = Decimal(x.numerator) / Decimal(x.denominator)
        quantum = Decimal(1).scaleb(-places)
        rounding = ROUND_CEILING if upward else ROUND_FLOOR
        return format(dec.quantize(quantum, rounding=rounding), "f")


def interval_record(n: int, ell: int, target_bits: int = 100) -> dict[str, object]:
    P = precision_bits(n, ell, target_bits)
    S = 1 << P
    elo, ehi, ewidth = term_interval(n, ell, P)
    mlo, mhi, mwidth = product_interval(n, ell, P)
    assert ewidth <= (S >> target_bits)
    assert mwidth <= (S >> target_bits)
    eta_lo, eta_hi = Fraction(elo, S), Fraction(ehi, S)
    mu_lo, mu_hi = Fraction(mlo, S), Fraction(mhi, S)
    zu = z_upper(n, ell)
    # The exact z is irrational in general.  Record a rational lower bound too.
    # Since sqrt(N) <= ceil(sqrt(N)), L/ceil(sqrt(N)) <= z.
    L = ell * (ell + 1)
    N = n * (n + 2)
    zlo = Fraction(L, math.isqrt(N) if math.isqrt(N) ** 2 == N else math.isqrt(N) + 1)
    rec: dict[str, object] = {
        "n": n,
        "ell": ell,
        "P_bits": P,
        "z_interval_rational": [str(zlo), str(zu)],
        "ell_over_n": outward_decimal(Fraction(ell, n), 12, False),
        "eta_interval": [outward_decimal(eta_lo, 18, False), outward_decimal(eta_hi, 18, True)],
        "eta_interval_width_upper": f"< 2^-{target_bits}",
        "mu_interval": [outward_decimal(mu_lo, 18, False), outward_decimal(mu_hi, 18, True)],
        "eta_dyadic_numerators": [str(elo), str(ehi)],
        "mu_dyadic_numerators": [str(mlo), str(mhi)],
        "endpoint_denominator": f"2^{P}",
        "eta_width_integer_units": str(ewidth),
        "mu_width_integer_units": str(mwidth),
    }
    if eta_hi < 1 and mu_hi < 1:
        qlo = (1 - eta_hi) / (1 - mu_lo) ** 2
        qhi = (1 - eta_lo) / (1 - mu_hi) ** 2
        rec["q_interval"] = [outward_decimal(qlo, 15, False), outward_decimal(qhi, 15, True)]
    else:
        rec["q_interval"] = "not certified positive from this enclosure"
    return rec


def main() -> None:
    # Geometric n grids and mesoscopic power laws.  Each sampled sequence has
    # ell/n -> 0 and z -> infinity as n grows (the finite points are diagnostics).
    ns = [2**10, 2**12, 2**14, 2**16]
    exponents = [0.55, 0.65, 0.75, 0.85]
    rows = []
    for n in ns:
        for alpha in exponents:
            ell = int(n**alpha)
            if ell < 1:
                continue
            row = interval_record(n, ell)
            row["power_exponent_alpha"] = alpha
            rows.append(row)
    json.dump(rows, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
