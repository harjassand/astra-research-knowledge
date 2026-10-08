"""Independent exact-rational interface diagnostics, not theorem certification."""
from fractions import Fraction as F
from itertools import product, combinations
from math import isqrt
from pathlib import Path
import json


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def ceil_log2(x):
    k = 0
    while F(2**k) < x:
        k += 1
    return k


def norm2(v):
    return sum(x * x for x in v)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def clip_round(w, n, eps, e=F(0)):
    p = 0
    while F(2 ** (2 * p)) < 12 * n / eps:
        p += 1
    h = F(1, 2**p)
    rad2 = 3 * (1 + e) / n
    w2 = norm2(w)
    outside = w2 > rad2
    v = []
    for x in w:
        if outside:
            bound = x * x * rad2 / (h * h * w2)
            ell = isqrt(bound.numerator // bound.denominator)
            assert F(ell * ell) <= bound < F((ell + 1) ** 2)
        else:
            ell = (abs(x) / h).numerator // (abs(x) / h).denominator
            assert ell * h <= abs(x) < (ell + 1) * h
        v.append((-1 if x < 0 else 1) * ell * h)
    assert norm2(v) <= rad2
    return tuple(v), p


def upward_root(eps, e=F(0)):
    p = 0
    while F(1, 2 ** (2 * p)) > eps:
        p += 1
    h = F(1, 2**p)
    value2 = 12 * (1 + e) * eps
    ratio = value2 / (h * h)
    floor = isqrt(ratio.numerator // ratio.denominator)
    ell = floor if F(floor * floor) == ratio else floor + 1
    u = ell * h
    assert u * u >= value2
    assert (u - h) ** 2 < value2
    assert h * h <= eps
    return u


def score(n, r, v, axis, x):
    c = F(n * (r - 1), n - 1)
    t = F(r * (r - 1), n * (n - 1))
    return (3 * x * x - 3 * r - 6 * c * v[axis] * x
            + t * (n + n * n * norm2(v))) / r


def integer_score(n, r, v, p, axis, x):
    vv = [int(z * 2**p) for z in v]
    numerator = (3 * n * (n - 1) * r * 2 ** (2 * p) * (x * x - r)
                 - 6 * n * n * r * (r - 1) * 2**p * vv[axis] * x
                 + r * r * (r - 1)
                 * (n * 2 ** (2 * p) + n * n * sum(z * z for z in vv)))
    denominator = n * (n - 1) * r * r * 2 ** (2 * p)
    return F(numerator, denominator)


def product_mean(n, r, local_bloch, axes, v, correction):
    total = F(0)
    subsets = tuple(combinations(range(n), r))
    for axis, direction in enumerate(axes):
        local_means = [dot(direction, a) for a in local_bloch]
        for subset in subsets:
            for signs in product((-1, 1), repeat=r):
                probability = F(1)
                for index, sign in zip(subset, signs):
                    probability *= (1 + sign * local_means[index]) / 2
                total += probability * (score(n, r, v, axis, sum(signs)) + correction)
    return total / (3 * len(subsets))


def main():
    clipped = score_cases = gap_count_cases = axis_cases = 0
    coordinates = [F(-3), F(-1), F(-1, 8), F(0), F(1, 8), F(1), F(3)]
    for n, eps, w, e in product((4, 7, 16, 101), (F(1), F(1, 4), F(1, 256)),
                                product(coordinates, repeat=3), (F(0), F(1, 10))):
        v, p = clip_round(w, n, eps, e)
        u = upward_root(eps, e)
        gamma = n * norm2(v) - 1 - u - 4 * e
        assert gamma <= 2 - e
        clipped += 1
        for r in {2, n // 2}:
            for a in range(3):
                for x in range(-r, r + 1, 2):
                    assert integer_score(n, r, v, p, a, x) == score(n, r, v, a, x)
                    # Nonorthogonal correction can be accumulated by shifting
                    # the comparison threshold; no irrational score is needed.
                    corrected = integer_score(n, r, v, p, a, x) + F(r - 1, n - 1) * e
                    assert corrected == score(n, r, v, a, x) + F(r - 1, n - 1) * e
                    score_cases += 1

    eta = F(1, 10)
    for delta in [F(2), F(31, 16), F(1), F(15, 16), F(1, 2), F(1, 16), F(3, 64), F(1, 1024)]:
        k0 = max(4, ceil_log2(16 / delta))
        assert 8 * F(1, 2**k0) >= delta / 4
        assert 8 * F(1, 2**k0) <= delta / 2
        assert F(4**k0) <= 1024 / (delta * delta)
        l0 = ceil_log2(24 * (k0 - 3) ** 2 / eta)
        for n, r in [(4, 2), (7, 2), (101, 20)]:
            cost = 0
            for k in range(4, k0 + 1):
                zeta = eta / (4 * (k - 3) ** 2)
                eps = F(1, 4**k)
                kk = ceil_fraction(F(41472 * n, r) / eps * ceil_log2(6 / zeta))
                cost += 3 * kk
            bound = F(169869312 * n, r) * l0 / (delta * delta) + 3 * (k0 - 3)
            assert cost <= bound
            gap_count_cases += 1

    # Three actual unit axes with an exact rational nonorthogonality certificate:
    # G-I has eigenvalues +/-a,0, so e=a is a valid operator bound.
    a, b = F(200, 10001), F(9999, 10001)
    assert a * a + b * b == 1
    axes = [(F(1), F(0), F(0)), (a, b, F(0)), (F(0), F(0), F(1))]
    arrays = [
        [(F(1), F(0), F(0)), (F(-1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(-1), F(0))],
        [(F(1), F(0), F(0))] * 4,
        [(F(1, 2), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(-1)), (F(0), F(0), F(0))]
    ]
    for local_bloch in arrays:
        star = [tuple(dot(direction, vec) for direction in axes) for vec in local_bloch]
        mean = tuple(sum(vec[i] for vec in star) / 4 for i in range(3))
        qstar = sum(norm2(vec) for vec in star) / 4
        assert qstar <= 1 + a
        for v in [(F(0), F(0), F(0)), (F(1, 8), F(1, 4), F(-1, 8)), (F(1, 2), F(1, 4), F(0))]:
            actual = product_mean(4, 2, local_bloch, axes, v, a / 3)
            expected = F(1, 3) * (1 + a - qstar + 4 * norm2(tuple(x - y for x, y in zip(mean, v))))
            assert actual == expected
            assert actual >= 0
            axis_cases += 1

    result = {"scope": "exact finite interface diagnostics; not general proof validation",
              "clipped_rounded_anchors": clipped, "integer_score_equalities": score_cases,
              "unknown_gap_count_cases": gap_count_cases,
              "nonorthogonal_product_mean_cases": axis_cases,
              "all_equalities_exact_rational": True}
    target = Path(__file__).with_name("exact_checks.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
