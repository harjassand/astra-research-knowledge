#!/usr/bin/env python3
"""Small exact label-budget audit for a geometric Gaussian spectrum.

This computes algebraic mode counts and mixed-radix field widths only. It does
not execute or validate the statistical-memory codec or its TV theorem.
"""
from math import isqrt


def ceil_sqrt_power_of_two(exponent: int) -> int:
    """ceil(sqrt(2**exponent)) using integer arithmetic."""
    n = 1 << exponent
    q = isqrt(n)
    return q if q * q == n else q + 1


def geometric_binary(q: int, dimension: int | None = None) -> dict[str, int]:
    """For r_i=2**(-i), eps=2**(-q), i=1,...,d (or infinity)."""
    if q < 4:
        raise ValueError("q must be >= 4 for this tabulation")
    active = q - 1 if dimension is None else min(dimension, q - 1)
    # Strict r_i > eps means i < q.
    s_bits = sum(q - i for i in range(1, active + 1))
    # Illustrative scalar grid constant 8: J_i=ceil(sqrt(8*r_i/eps)).
    # The N31 summary gives a conservative 14 bits per active mode, but does
    # not specify this grid constant; this field count is illustrative only.
    serial = 0
    for i in range(1, active + 1):
        j = ceil_sqrt_power_of_two(q - i + 3)
        k = 2 * j - 1
        serial += (k - 1).bit_length()  # ceil(log2(k)) fixed field width
    return {
        "q": q,
        "dimension": dimension if dimension is not None else -1,
        "active_modes": active,
        "S_exact_bits": s_bits,
        "half_S_bits": s_bits // 2 if s_bits % 2 == 0 else -1,
        "N31_reported_upper_bound_bits": s_bits / 2 + 14 * active,
        "illustrative_fixed_field_bits": serial,
        "tail_TV_bound_over_epsilon": 0.5,
    }


if __name__ == "__main__":
    for q in (8, 16, 32, 64):
        print(geometric_binary(q))
    print("truncated", geometric_binary(32, dimension=12))
