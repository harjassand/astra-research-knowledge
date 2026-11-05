"""Exact-rational conservative marked-event uncertainty certificates.

This calculates certificates; it does not implement Gibbs counting or
general first-event sampling. Rational inequalities bound transcendentals.
"""
from fractions import Fraction as F
from math import isqrt


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def ceil_log2_fraction(x):
    if x <= 0:
        raise ValueError("positive input required")
    k = x.numerator.bit_length() - x.denominator.bit_length()
    p = F(2 ** k) if k >= 0 else F(1, 2 ** (-k))
    return k if p >= x else k + 1


def sqrt_up(x, digits=32):
    """An exact rational upper square-root, with verified endpoint."""
    if x < 0:
        raise ValueError("negative square root")
    scale = 10 ** digits
    k = isqrt((x.numerator * scale * scale) // x.denominator)
    if F(k * k, scale * scale) < x:
        k += 1
    y = F(k, scale)
    assert y * y >= x
    return y


def schedule(eps, g, zeta, H):
    eps, g, zeta = map(F, (eps, g, zeta))
    if not (0 < eps <= F(1, 4) and 0 < g <= 1 and 0 < zeta <= 1):
        raise ValueError("invalid certificate range")
    if not isinstance(H, int) or H < 0:
        raise ValueError("H must be a nonnegative integer")
    C = ceil_log2_fraction(128 / (eps * zeta))
    b = ceil_fraction(F(C) / g)
    L = ceil_fraction(1024 * (H + b + 2) / (g * eps))
    Tmax = ceil_fraction(16 * L * C / g) + 1
    return dict(C=C, b=b, L=L, Tmax=Tmax)


def rare_certificate(*, g, zeta, p_upper, H, b, L, E, a, q0=None):
    g, zeta, p_upper, E, a = map(F, (g, zeta, p_upper, E, a))
    if any(not isinstance(v, int) for v in (H, b, L)) or H < 0 or b < 0 or L < 1:
        raise ValueError("integer nonnegative window/buffer and positive block required")
    if not (g > 0 and zeta > 0 and 0 < p_upper < 1 and 0 <= E and 0 <= a < 1):
        raise ValueError("invalid envelope")
    if q0 is None:
        if L < 16 * (H + 1) / g or L * p_upper > 1:
            raise ValueError("uniform acceptance conditions not established")
        q0 = g / 8
    else:
        q0 = F(q0)
        if not 0 < q0 <= 1:
            raise ValueError("acceptance floor must be certified separately")
    exponent = (g * b).numerator // (g * b).denominator
    eta = F(1, 2 ** exponent) / zeta  # exp(-g*b) <= 2**(-floor(g*b))
    if eta >= 1:
        raise ValueError("buffer has no valid multiplicative mixing bound")
    kappa = (a / (1 - a)) ** 2  # exp(a)-1 <= a/(1-a)
    D = 2 * E * E + (L + 1) * kappa
    z = sqrt_up(D / q0)
    d = 2 * E + 2 * z
    geom = F(1) if d >= 1 else min(F(1), d / (1 - d))
    structural = eta / (1 - eta)
    structural += (1 + eta) / (1 - eta) * F(H + b + 2, L + 1) / q0
    structural += (1 + eta) * p_upper * (b + 1)
    prefix = sqrt_up(F(b, 2) * kappa)
    total = min(F(1), 2 * structural + prefix + z + geom)
    return dict(bound=total, structural_each=structural, prefix=prefix,
                accepted_path=z, geometric=geom, D=D, eta=eta, q0=q0)


def decimal_summary(obj):
    return {k: float(v) if isinstance(v, F) else v for k, v in obj.items()}

