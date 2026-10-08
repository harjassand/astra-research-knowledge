"""Exact interval lower certificate for the six-mode d=5 POVM support.

The stated rationalized pure seed is Weyl-twirled to a 25-outcome rank-one
POVM. Exact rational intervals for fifth roots of unity prove that this one
legal POVM scores strictly above 3, which is enough for this Q because the
exact star maximum is strictly below 15 and Tr_HS(Q)=12.
"""
from fractions import Fraction
from math import isqrt


SCALE = 10**40


class I:
    def __init__(self, lo, hi=None):
        self.lo = Fraction(lo)
        self.hi = Fraction(lo if hi is None else hi)

    def __add__(self, other):
        other = as_i(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_i(other))

    def __rsub__(self, other):
        return as_i(other) - self

    def __mul__(self, other):
        other = as_i(other)
        values = (self.lo * other.lo, self.lo * other.hi,
                  self.hi * other.lo, self.hi * other.hi)
        return I(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_i(other)
        assert other.lo > 0 or other.hi < 0
        return self * I(1 / other.hi, 1 / other.lo)


def as_i(value):
    return value if isinstance(value, I) else I(Fraction(value))


def sqrt_fraction(q):
    q = Fraction(q)
    assert q >= 0
    n, d = q.numerator, q.denominator
    k = isqrt((n * SCALE * SCALE) // d)
    lo = Fraction(k, SCALE)
    h = k + int(k * k * d < n * SCALE * SCALE)
    hi = Fraction(h, SCALE)
    assert lo * lo <= q <= hi * hi
    return I(lo, hi)


def sqrt_interval(q):
    assert q.lo >= 0
    return I(sqrt_fraction(q.lo).lo, sqrt_fraction(q.hi).hi)


def square(q):
    hi = max(q.lo * q.lo, q.hi * q.hi)
    lo = Fraction(0) if q.lo <= 0 <= q.hi else min(q.lo * q.lo, q.hi * q.hi)
    return I(lo, hi)


def roots_of_unity_trig():
    r5 = sqrt_fraction(Fraction(5))
    c1, c2 = (r5 - 1) / 4, -(r5 + 1) / 4
    s1 = sqrt_interval((10 + 2 * r5) / 16)
    s2 = sqrt_interval((10 - 2 * r5) / 16)
    return ([as_i(1), c1, c2, c2, c1],
            [as_i(0), s1, s2, -s2, -s1])


def main():
    # Decimal strings are exact rationals. The vector is rounded from a
    # numerical local maximum; its later use is certified independently.
    z = [
        (Fraction("-0.453247"), Fraction("-0.432812")),
        (Fraction("0.272132"), Fraction("0.036691")),
        (Fraction("-0.198028"), Fraction("0.411862")),
        (Fraction("-0.552038"), Fraction("-0.074431")),
        (Fraction("-0.081529"), Fraction("-0.077853")),
    ]
    norm2 = sum(a*a + b*b for a, b in z)
    assert norm2 > 0

    # One selected mode pair per projective line in Z_5^2.
    modes = [(0, 2), (1, 0), (1, 1), (2, 4), (2, 1), (2, 3)]
    cos, sin = roots_of_unity_trig()
    score = as_i(0)
    for u, v in modes:
        re, im = as_i(0), as_i(0)
        for j in range(5):
            ar, ai = z[(j - u) % 5]  # conjugated ket coefficient; X shifts j to j-u
            br, bi = z[j]
            cr, ci = ar * br + ai * bi, ar * bi - ai * br
            k = (v * j) % 5
            re += cr * cos[k] - ci * sin[k]
            im += ci * cos[k] + cr * sin[k]
        re, im = re / norm2, im / norm2
        score += 2 * (square(re) + square(im))

    assert score.lo > 3
    print("rational seed norm^2", norm2)
    print("support lower interval", float(score.lo), float(score.hi))
    print("certified support lower bound > 3: PASS")
    print("Weyl orbit of this seed has 25 outcomes and barycenter I/5.")


if __name__ == "__main__":
    main()
