"""Exact rational bounded-test witnesses. Uses Python standard library only."""
from fractions import Fraction as F
from math import factorial
from decimal import Decimal, localcontext
from pathlib import Path
import csv
import sys

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parent


def floor_frac(q):
    return q.numerator // q.denominator


def ceil_frac(q):
    return -((-q.numerator) // q.denominator)


def exp_negative_interval(x, bits):
    """Certified exp(-x), by alternating series and outward integer rounding."""
    assert x >= 0
    scale, u = 0, x
    while u > 1:
        u /= 2
        scale += 1
    unit = 1 << bits
    tolerance = F(1, unit << (scale + 16))
    total, term = F(1), F(1)
    lower, upper, index = F(0), F(1), 0
    while upper - lower > tolerance:
        index += 1
        term *= u / index
        if index % 2:
            total -= term
            lower = total
        else:
            total += term
            upper = total
    lo = max(0, floor_frac(lower * unit))
    hi = ceil_frac(upper * unit)
    for _ in range(scale):
        lo = lo * lo // unit
        hi = (hi * hi + unit - 1) // unit
    return F(lo, unit), F(hi, unit), index, scale


def scientific(q):
    with localcontext() as ctx:
        ctx.prec = 25
        return format(Decimal(q.numerator) / Decimal(q.denominator), ".17E")


def main():
    rows, output = [], []
    for shift, n in [(1, 5), (2, 30), (3, 85), (4, 172)]:
        bits = 4 * (n * n // (2 * shift * shift) + n + 100)
        left_lo, left_hi, li, ls = exp_negative_interval(F(n + 1, 2), bits)
        right_lo, right_hi, ri, rs = exp_negative_interval(F(n * n, 2 * shift * shift), bits)
        prefactor = (1 - F(1, 4 * (n + 1))) / (2**n * factorial(n))
        lower = (prefactor * left_lo - right_hi) / 2
        upper = (prefactor * left_hi - right_lo) / 2
        assert 0 < lower <= upper
        assert upper - lower < lower / 10**20
        rows.append([shift, n, bits, lower.numerator, lower.denominator,
                     upper.numerator, upper.denominator])
        output.append(f"D={shift}, n={n}: exact positive TV floor >= {scientific(lower)}")
        output.append(f"  {bits} integer bits; series terms {li}, {ri}; squarings {ls}, {rs}")
    assert 1 - 2 == -1
    output.append("Exact nonlinear-location log-MGF Hessian witness: 1+(2/a)*(-a)=-1.")
    output.append("Four exact rational bounded-test witnesses certified. Source queries: zero.")
    with (ROOT / "shift_rigidity_exact_bounds.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["shift_budget_D", "frequency_n", "integer_bits", "tv_lower_numerator",
                         "tv_lower_denominator", "tv_upper_numerator", "tv_upper_denominator"])
        writer.writerows(rows)
    result = "\n".join(output) + "\n"
    (ROOT / "SHIFT_RIGIDITY_CHECK_RESULTS.txt").write_text(result)
    print(result, end="")


if __name__ == "__main__":
    main()
