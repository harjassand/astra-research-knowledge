"""Exact-rational logarithm certificate for the history entropy bounds.

This checks only scalar analytic constants, not the quantum-operator premise.
Python standard library only. The series remainder is proved in the report.
"""

from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
import json
import resource
import time


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def scale(s, a):
    return (s * a[0], s * a[1]) if s >= 0 else (s * a[1], s * a[0])


def divide_positive(a, b):
    assert a[0] >= 0 and b[0] > 0
    return a[0] / b[1], a[1] / b[0]


def log_ratio_interval(x, terms=48):
    """Enclose log(x), for rational 1 <= x <= 2, by exact rationals."""
    assert F(1) <= x <= F(2)
    z = (x - 1) / (x + 1)
    low = 2 * sum((z ** (2*j + 1) / (2*j + 1) for j in range(terms)), F(0))
    tail = 2 * z ** (2*terms + 1) / ((2*terms + 1) * (1-z*z))
    return low, low + tail


def display(a, digits=32):
    result = []
    with localcontext() as ctx:
        ctx.prec = 120
        unit = Decimal(1).scaleb(-digits)
        for x, rounding in zip(a, (ROUND_FLOOR, ROUND_CEILING)):
            d = Decimal(x.numerator) / Decimal(x.denominator)
            result.append(str(d.quantize(unit, rounding=rounding)))
    return result


def main():
    started = time.perf_counter()
    ln2 = log_ratio_interval(F(2))
    ln3over2 = log_ratio_interval(F(3, 2))
    ln25over16 = log_ratio_interval(F(25, 16))
    ln99over64 = log_ratio_interval(F(99, 64))
    # h2(1/100) = .06 + [ln(25/16)-.99 ln(99/64)] / ln 2.
    hn = add(ln25over16, scale(-F(99, 100), ln99over64))
    h = add((F(3, 50), F(3, 50)), divide_positive(hn, ln2))
    log2_3 = add((F(1), F(1)), divide_positive(ln3over2, ln2))
    rank = add(add((F(297, 200), F(297, 200)), h), scale(F(1, 100), log2_3))
    gap = add(log2_3, scale(-1, rank))
    uniform_tail = add(h, (-F(9, 100), -F(9, 100)))
    assert F('0.08079313589591117') < h[0] <= h[1] < F('0.08079313589591118')
    assert F('1.5816427609031227') < rank[0] <= rank[1] < F('1.5816427609031228')
    assert gap[0] > F('0.0033197398180334')
    assert uniform_tail[1] < F('-0.0092068641040888')
    # Coarse independently checkable rational upper/lower decimal separators.
    assert 3**200 < 2**317  # log2(3) < 1.585.
    assert 3**125 > 2**198  # log2(3) > 1.584.
    assert h[1] < F(81, 1000)
    out = {
        'status': 'exact_rational_checks_passed',
        'scope': 'scalar entropy bounds only; no quantum operator test',
        'q': '1/100', 'beta_max': '1/512',
        'logarithm_series_terms': 48,
        'h2_q_interval': display(h),
        'rank_exponent_interval': display(rank),
        'log2_3_interval': display(log2_3),
        'strict_port_gap_interval': display(gap),
        'uniform_tail_exponent_upper_bound_interval': display(uniform_tail),
        'wall_seconds': time.perf_counter() - started,
        'max_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
