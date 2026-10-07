"""Directed-integer positive Taylor, reciprocal and square scalar intervals.

Independent acquisition for posterior certificates; does not execute a Gibbs
optimizer or modify the previous conservative rational Taylor implementation.
"""
from fractions import Fraction as F


def ceil_div(n, d):
    if d <= 0:
        raise ValueError("positive divisor required")
    return -((-n) // d)


def exp_negative_interval(x, bits):
    """Return exact rational outward bounds of exp(-x), width<=2^-bits."""
    x = F(x)
    if x < 0 or bits < 1:
        raise ValueError("nonnegative rational argument and positive bits required")
    if x == 0:
        return F(1), F(1)
    if x >= bits + 2:
        # e>2; lower zero is deliberate, with no huge positive denominator.
        return F(0), F(1, 1 << (bits + 2))
    y, squares = x, 0
    while y > F(1, 16):
        y /= 2
        squares += 1
    guard_bits = bits + 2 * squares + 2 * (bits + 2 * squares + 16).bit_length() + 24
    D = 1 << guard_bits
    a, d = y.numerator, y.denominator
    lo_term = hi_term = lo_sum = hi_sum = D
    # Terms are scaled by D. Both recurrences enclose y^n/n! exactly.
    for n in range(1, guard_bits + 2):
        lo_term = lo_term * a // (d * n)
        hi_term = ceil_div(hi_term * a, d * n)
        lo_sum += lo_term
        hi_sum += hi_term
    n = guard_bits + 1
    next_upper = ceil_div(hi_term * a, d * (n + 1))
    # Every subsequent exact-term ratio <=y<=1/16, so the complete omitted
    # tail is at most16/15 times its first omitted upper term.
    hi_sum += ceil_div(16 * next_upper, 15)
    # Outward reciprocal to exp(-y), followed by outward repeated squaring.
    lo = D * D // hi_sum
    hi = min(D, ceil_div(D * D, lo_sum))
    for _ in range(squares):
        lo = lo * lo // D
        hi = min(D, ceil_div(hi * hi, D))
    assert 0 <= lo <= hi <= D
    assert (hi - lo) * (1 << bits) <= D
    return F(lo, D), F(hi, D)
