"""Independent exact-arithmetic replay of source020 Appendix A.

This checks only the finite rational certificate printed in the manuscript; it
does not validate the geometric lemmas to which the parameters are applied.
"""

from fractions import Fraction as F
from math import comb

K, G = 3000, 100000


def polynomials(d):
    k = d - 2
    for i in range(1, 500):
        t = F(i, 50)
        values = [
            sum(
                comb(d - r, j - s)
                * comb(k, j - 1)
                * k ** (j - 1)
                * t ** (j - s)
                for j in range(1, d)
            )
            for r, s in [(0, 0), (1, 0), (1, 1)]
        ]
        yield (t, *values)


def upper(x, e):
    """Least r/G with (r/G)^e > x, using integer comparisons only."""
    assert 0 <= x < 1
    lo, hi = 0, G
    while hi > lo + 1:
        mid = (lo + hi) // 2
        if F(mid, G) ** e > x:
            hi = mid
        else:
            lo = mid
    return F(hi, G)


def check_derivatives():
    for k in range(2, 7):
        for t in [F(3, 20), F(5)]:
            for a, b in [(1, 0), (0, 1), (1, 1)]:
                for h in range(2, k + 3):
                    numerator = t * (
                        1
                        + 1 / t
                        - F(h - 1, h) * (k + 1) / (k + t)
                        - F(1, h) * (a + b) / (a + b * t)
                    )
                    assert numerator >= 0
                    assert numerator**h < (k + t) ** (h - 1) * (a + b * t)


def check_degree(d):
    k, choices, least = d - 2, list(polynomials(d)), F(1)
    for z in range(K, 2 * K):
        eta_l, eta_h = F(z, K), F(z + 1, K)
        if eta_l * (1 - k * eta_l / d) < F(2495, 10000):
            return z, least
        b_l, b_h = d - k * eta_h, d - k * eta_l
        t, hval, ha, hb = min(
            choices, key=lambda row: (eta_h + b_h * row[0]) ** d / row[1]
        )
        w = upper(((d + 1) * (eta_h + b_h * t) / d**2) ** d / hval, d - 1)
        assert w ** (d - 2) * min(ha, hb) > ((eta_h + b_h * t) / (d - 1)) ** (d - 1)
        m = (d - 1) * w
        u, v = (eta_h - m) / d, (b_h - m) / d
        assert 0 < m < 1 and min(eta_l, b_l) > m
        assert min(u, v) > 0 and F(3, 20) <= v / u <= 5

        def delta(h, den):
            return upper((u * v) ** h / ((k * u + v) ** (h - 1) * den), h)

        p = [delta(d, u + v)]
        if d == 4 and z < 4000:
            assert m + 2 * u < F(999, 1000)
            p += [
                delta(3, v),
                max(delta(2, min(3 * u, 2 * v, u + v)), upper(u * u / 3, 2)),
            ]
        else:
            p += [delta(h, min(u, v)) for h in range(d - 1, 1, -1)]
        g = (d - 1) * (k - 1) + (d == 4)
        p.append(max(u / 2, min(u, v / g)))
        gap = 1 - m - sum(max(p[:h]) for h in range(1, d + 1))
        assert gap > F(1, 1000)
        least = min(least, gap)
    raise AssertionError("cutoff not reached")


def check_enlarged_first_quartic_cell():
    epsilon = F(1, 10**6)
    eta_l, eta_h = 1 - epsilon, F(3001, 3000)
    b_l, b_h = 4 - 2 * eta_h, 2 + 2 * epsilon
    t, w = F(1, 2), F(24809, 100000)
    m = 3 * w
    u, v = (eta_h - m) / 4, (b_h - m) / 4
    assert 0 < epsilon < F(1, 2)
    assert 0 < m < 1 and m < min(eta_l, b_l)
    assert w**3 * 10 > (F(5, 16) * (eta_h + b_h * t)) ** 4
    assert w**2 * 5 > ((eta_h + b_h * t) / 3) ** 3
    assert min(u, v) > 0 and F(3, 20) <= v / u <= 5

    def quartic_delta(h, den):
        return upper((u * v) ** h / ((2 * u + v) ** (h - 1) * den), h)

    p = [
        quartic_delta(4, u + v),
        quartic_delta(3, v),
        max(quartic_delta(2, min(3 * u, 2 * v, u + v)), upper(u * u / 3, 2)),
        max(u / 2, min(u, v / 4)),
    ]
    assert p == [F(4729, 100000), F(5097, 100000), F(6899, 100000), F(76819, 1200000)]
    gap = 1 - m - sum(max(p[:i]) for i in range(1, 5))
    tau = F(1, 50000)
    assert gap - 4 * tau == F(1941, 100000)
    assert 1 - m - 2 * u - 2 * tau == F(15319, 120000)


if __name__ == "__main__":
    check_derivatives()
    results = [check_degree(d) for d in range(4, 9)]
    assert results == [
        (5124, F(191, 100000)),
        (4084, F(293, 50000)),
        (3552, F(321, 2500)),
        (3226, F(23177, 100000)),
        (3003, F(31683, 100000)),
    ]
    check_enlarged_first_quartic_cell()
    print(results)
    print("enlarged quartic cell: verified")
