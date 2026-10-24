"""Independent quadrature check for one side resonator, m=M=K=1, k=4."""

import math
import numpy as np


def bose_weight(x):
    """Landauer thermal weight x^2 exp(x)/(exp(x)-1)^2."""
    if x < 1.0e-3:
        x2 = x * x
        return 1.0 - x2 / 12.0 + x2**2 / 240.0 - x2**3 / 6048.0
    if x > 50.0:
        return x * x * math.exp(-x)
    em1 = math.expm1(x)
    return x * x * (em1 + 1.0) / (em1 * em1)


def endpoints_k4():
    """(acoustic maximum, optical minimum, optical maximum)."""
    return math.sqrt(6.0 - math.sqrt(20.0)), math.sqrt(8.0), math.sqrt(6.0 + math.sqrt(20.0))


def simpson_interval(f, lo, hi, panels=1 << 15):
    """Composite Simpson quadrature; panels must be even."""
    if panels % 2:
        raise ValueError("Simpson panel count must be even")
    h = (hi - lo) / panels
    total = f(lo) + f(hi)
    total += 4.0 * sum(f(lo + j * h) for j in range(1, panels, 2))
    total += 2.0 * sum(f(lo + j * h) for j in range(2, panels, 2))
    return total * h / 3.0


def gauss_legendre_interval(f, lo, hi, order=160):
    """Independent high-order Gauss-Legendre quadrature."""
    x, w = np.polynomial.legendre.leggauss(order)
    mid = (lo + hi) / 2.0
    half = (hi - lo) / 2.0
    return half * sum(float(wi) * f(mid + half * float(xi)) for xi, wi in zip(x, w))


def band_integral(method, lo, hi, theta):
    return method(lambda omega: bose_weight(omega / theta), lo, hi)


def side_k4(theta, method):
    ac, op_lo, op_hi = endpoints_k4()
    return band_integral(method, 0.0, ac, theta) + band_integral(method, op_lo, op_hi, theta)


def rigid_total_mass(theta, method):
    return band_integral(method, 0.0, math.sqrt(2.0), theta)


def main():
    ac, op_lo, op_hi = endpoints_k4()
    assert ac < op_lo < op_hi
    print(f"k=4 bands: [0,{ac:.12f}] U [{op_lo:.12f},{op_hi:.12f}]")
    print("theta  side k=4 (Simpson)  rigid (Simpson)  relative difference  GL cross-check max error")
    for theta in (0.5, 1.0):
        side_s = side_k4(theta, simpson_interval)
        rigid_s = rigid_total_mass(theta, simpson_interval)
        side_g = side_k4(theta, gauss_legendre_interval)
        rigid_g = rigid_total_mass(theta, gauss_legendre_interval)
        err = max(abs(side_s - side_g), abs(rigid_s - rigid_g))
        print(f"{theta:4.1f}  {side_s:.12f}  {rigid_s:.12f}  {side_s/rigid_s - 1:+.8%}  {err:.3e}")
        assert err < 2.0e-12
    # At theta=1 the sign reverses: the result is a single operating-point
    # comparison, not a uniform finite-temperature advantage.
    assert side_k4(0.5, simpson_interval) < rigid_total_mass(0.5, simpson_interval)
    assert side_k4(1.0, simpson_interval) > rigid_total_mass(1.0, simpson_interval)
    print("PASS: complete acoustic+optical k=4 quadrature independently agrees (Simpson vs Gauss-Legendre).")


if __name__ == "__main__":
    main()
