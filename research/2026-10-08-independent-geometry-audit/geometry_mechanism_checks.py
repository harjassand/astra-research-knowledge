#!/usr/bin/env python3
"""Finite-dimensional diagnostics for Astra N175 and N210 (not a PDE proof)."""
from math import cos, pi, sin, sqrt


def trapz(values, width):
    return width * (sum(values) - (values[0] + values[-1]) / 2)


def avg_over_unit(f, n=40000):
    h = 1.0 / n
    return trapz([f(i * h) for i in range(n + 1)], h)


def spectral_ratio(v, M):
    n = (M + 1) ** 2
    total = sum((2 * l + 1) * (-1 + sqrt(1 + 4 * l * (l + 1) / v)) / 2
                for l in range(M + 1))
    mean = total / n
    return n / (mean ** 2)


def upper_eigen(s, eps):
    d = s - 0.5
    radial_sq = d * d + eps * eps + 2 * d * eps * cos(pi * s)
    assert radial_sq >= -1e-14
    return 1.5 + sqrt(max(radial_sq, 0.0))


def gap(s, eps):
    return 2 * (upper_eigen(s, eps) - 1.5)


def run():
    v = 0.81
    limit = 9 * v / 4
    print(f'frozen_cone: v={v}; predicted_capacity={limit:.9f}')
    for M in (10, 30, 100, 300, 1000):
        ratio = spectral_ratio(v, M)
        print(f'M={M:4d}; band_dim={(M+1)**2:8d}; capacity_ratio={ratio:.9f}; excess={ratio-limit:.9f}')
    assert abs(spectral_ratio(v, 1000) - limit) < 0.004

    # The closed, real-symmetric 2x2 path A_0(s) is exactly degenerate at s=1/2.
    # Its two continued eigenvalue labels are 1+s and 2-s, so each has mean 3/2.
    m1 = avg_over_unit(lambda s: 1 + s)
    m2 = avg_over_unit(lambda s: 2 - s)
    ordered_high = avg_over_unit(lambda s: upper_eigen(s, 0.0))
    print(f'exact_crossing: continued_means=({m1:.9f},{m2:.9f}); ordered_high_mean={ordered_high:.9f}')
    assert abs(m1 - 1.5) < 1e-12
    assert abs(m2 - 1.5) < 1e-12
    assert abs(ordered_high - 1.75) < 1e-8

    for eps in (0.01, 0.05, 0.10):
        high = avg_over_unit(lambda s: upper_eigen(s, eps))
        min_gap = min(gap(i / 10000, eps) for i in range(10001))
        print(f'avoided_crossing: eps={eps:.3f}; high_label_mean={high:.9f}; min_gap_sample={min_gap:.9f}')
        assert high >= 1.75 - eps - 1e-8
        assert min_gap > 0

    # h_t=(1+eta*sin(sqrt(t)))h_round for t large, d=2.
    eta = 0.2
    mean_inverse_area = avg_over_unit(lambda s: (1 + eta * sin(2*pi*s)) ** (-0.5))
    averaged_capacity = limit / (mean_inverse_area ** 2)
    print(f'variable_area: inverse_sqrt_area_mean={mean_inverse_area:.9f}; averaged_capacity_bound={averaged_capacity:.9f}')
    assert mean_inverse_area > 1
    assert averaged_capacity < limit

    print('PASS finite-diagnostic assertions. These do not validate any PDE metric construction.')


if __name__ == '__main__':
    run()
