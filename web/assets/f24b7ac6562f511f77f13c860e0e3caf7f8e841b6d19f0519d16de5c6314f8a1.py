"""Exact-rational interval certificate for the d=5 EB comparator.

No floating-point operation is used. Decimal ket coordinates and weights are
parsed as exact rationals. The only irrational constants are enclosed by
rational intervals whose endpoints are checked by integer squaring.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from math import isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
FIXTURE = ROOT / "work/agents/weyl_compatible_lift/d5_eb_comparator.json"
SCALE = 10**50


@dataclass(frozen=True)
class I:
    lo: Fraction
    hi: Fraction

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
        vals = (self.lo * other.lo, self.lo * other.hi,
                self.hi * other.lo, self.hi * other.hi)
        return I(min(vals), max(vals))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_i(other)
        assert other.lo > 0 or other.hi < 0
        return self * I(1 / other.hi, 1 / other.lo)


def as_i(x):
    if isinstance(x, I):
        return x
    q = Fraction(x)
    return I(q, q)


def sqrt_fraction(q: Fraction) -> I:
    assert q >= 0
    n, d = q.numerator, q.denominator
    scaled_floor = isqrt((n * SCALE * SCALE) // d)
    lo = Fraction(scaled_floor, SCALE)
    hi_int = scaled_floor
    if hi_int * hi_int * d < n * SCALE * SCALE:
        hi_int += 1
    hi = Fraction(hi_int, SCALE)
    assert lo * lo <= q <= hi * hi
    return I(lo, hi)


def sqrt_interval(q: I) -> I:
    assert q.lo >= 0
    lo = sqrt_fraction(q.lo).lo
    hi = sqrt_fraction(q.hi).hi
    return I(lo, hi)


def square(q: I) -> I:
    hi = max(q.lo * q.lo, q.hi * q.hi)
    lo = Fraction(0) if q.lo <= 0 <= q.hi else min(q.lo * q.lo, q.hi * q.hi)
    return I(lo, hi)


def exact_target_lambdas():
    r = sqrt_fraction(Fraction(5))
    c1 = (r - 1) / 4
    c2 = -(r + 1) / 4
    x0 = (23 - 2 * r) / 25
    x1 = (75 - 16 * r) / 500
    x2, x3, x4 = Fraction(3, 20), Fraction(9, 100), Fraction(1, 4)
    n = x0*x0 + 10*x1*x1 + 10*x2*x2 + 2*x3*x3 + 2*x4*x4
    d0, d1, d2 = x0*x0 - x2*x2, x3*x3 - x2*x2, x4*x4 - x2*x2
    lv1 = (d0 + 2*d1*c1 + 2*d2*c2) / n
    lv2 = (d0 + 2*d1*c2 + 2*d2*c1) / n
    lu1 = (d0 + 2*d1 + 2*d2 + 10*(x1*x1-x2*x2)*c1) / n
    lu2 = (d0 + 2*d1 + 2*d2 + 10*(x1*x1-x2*x2)*c2) / n
    return lv1, lv2, lu1, lu2


def roots_of_unity_trig():
    r = sqrt_fraction(Fraction(5))
    c1, c2 = (r - 1) / 4, -(r + 1) / 4
    s1 = sqrt_interval((10 + 2*r) / 16)
    s2 = sqrt_interval((10 - 2*r) / 16)
    cos = [as_i(1), c1, c2, c2, c1]
    sin = [as_i(0), s1, s2, -s2, -s1]
    return cos, sin


def comparator_intervals():
    fixture = json.loads(FIXTURE.read_text(), parse_float=Decimal)
    weights = [Fraction(x) for x in fixture["weights_normalized_to_sum_one"]]
    total = sum(weights)
    weights = [w/total for w in weights]
    assert sum(weights) == 1 and all(w > 0 for w in weights)

    states = []
    for ket in fixture["product_kets"]:
        z = [(Fraction(a), Fraction(b)) for a, b in ket]
        norm2 = sum(a*a+b*b for a, b in z)
        assert norm2 > 0
        states.append((z, norm2))

    cos, sin = roots_of_unity_trig()
    modes = {}
    for u in range(5):
        for v in range(5):
            if (u, v) == (0, 0):
                continue
            mu = as_i(0)
            for w, (z, norm2) in zip(weights, states):
                real, imag = as_i(0), as_i(0)
                for j in range(5):
                    ar, ai = z[(j+u) % 5]
                    br, bi = z[j]
                    cr, ci = ar*br + ai*bi, ar*bi - ai*br
                    k = (v*j) % 5
                    real += cr*cos[k] + ci*sin[k]
                    imag += ci*cos[k] - cr*sin[k]
                real = real * Fraction(1, norm2)
                imag = imag * Fraction(1, norm2)
                mu += w * (square(real) + square(imag))
            modes[(u, v)] = mu
    return modes


def main():
    lv1, lv2, lu1, lu2 = exact_target_lambdas()
    comparator = comparator_intervals()
    gaps = []
    clipped = []
    for mode, mu in comparator.items():
        u, v = mode
        if v:
            lam = lv1 if v in (1, 4) else lv2
        else:
            lam = lu1 if u in (1, 4) else lu2
        direct = mu - (2*lam - 1)
        threshold = 2*lam - 1
        if threshold.hi <= 0:
            threshold = as_i(0)
        elif threshold.lo <= 0:
            threshold = I(Fraction(0), threshold.hi)
        else:
            pass
        gaps.append((direct.lo, mode, direct))
        cg = mu - threshold
        clipped.append((cg.lo, mode, cg))

    min_direct = min(gaps)
    min_clipped = min(clipped)
    direct_claim = Fraction(59, 2500)  # 0.0236
    clipped_claim = Fraction(139, 10000)  # 0.0139
    assert min_direct[0] > direct_claim
    assert min_clipped[0] > clipped_claim
    print("all 24 exact-rational interval gaps are positive")
    print("all direct gaps exceed 59/2500 = 0.0236;")
    print("smallest interval lower endpoint is at", min_direct[1])
    print("all clipped gaps exceed 139/10000 = 0.0139;")
    print("smallest interval lower endpoint is at", min_clipped[1])
    print("min direct lower bound (decimal):", float(min_direct[0]))
    print("min clipped lower bound (decimal):", float(min_clipped[0]))


if __name__ == "__main__":
    main()
