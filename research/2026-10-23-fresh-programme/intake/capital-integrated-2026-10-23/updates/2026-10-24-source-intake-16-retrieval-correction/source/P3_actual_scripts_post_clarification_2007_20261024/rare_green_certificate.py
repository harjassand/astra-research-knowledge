"""Fresh scratch calculation: exact rational Green-function enclosures.

Independent symmetric sites have relaxation rates lambda_i=1+2**(-i).
No 2**n species/configuration expansion is used in the n=80 calculation.
All enclosure arithmetic is integer arithmetic; Decimal is display only.
"""
from math import comb
from fractions import Fraction
from decimal import Decimal, localcontext
import json
import time


def green_enclosure(n=80, b=10, moment_order=6, precision_bits=240):
    assert 0 <= b < n and moment_order >= 2 and moment_order % 2 == 0
    ell = n - b
    scale = 1 << n
    tail_sum = (1 << ell) - 1
    grid = 1 << precision_bits
    order = moment_order

    # raw[k][r] = sum over size-k subsets of tail integer weights of U**r.
    raw = [[0] * (order + 1) for _ in range(ell + 1)]
    raw[0][0] = 1
    for j in range(ell):
        powers = [1 << (j * r) for r in range(order + 1)]
        for k in range(j + 1, 0, -1):
            prev = raw[k - 1]
            for r in range(order + 1):
                raw[k][r] += sum(
                    comb(r, a) * powers[r - a] * prev[a]
                    for a in range(r + 1)
                )

    # centered[k][r] = sum (ell*U-k*tail_sum)**r over size-k subsets.
    centered = []
    for k in range(ell + 1):
        moments = [
            sum(
                comb(r, a) * ell**a * (-k * tail_sum) ** (r - a)
                * raw[k][a]
                for a in range(r + 1)
            )
            for r in range(order + 1)
        ]
        assert moments[0] == comb(ell, k) and moments[1] == 0
        assert all(moments[r] >= 0 for r in range(0, order + 1, 2))
        centered.append(moments)

    low_num = high_num = groups = 0
    for head in range(1 << b):
        h = head.bit_count()
        head_weight = head << ell
        for k in range(ell + 1):
            if h + k == 0:
                continue
            groups += 1
            d0 = (h + k) * scale + head_weight
            d = ell * d0 + k * tail_sum
            denominator = d
            # Exact finite reciprocal expansion through odd order order-1.
            for r in range(order):
                numerator = ell * (-1) ** r * centered[k][r] * grid
                low_num += numerator // denominator
                high_num += -((-numerator) // denominator)
                denominator *= d
            vmin = ell * ((1 << k) - 1) - k * tail_sum
            vmax = ell * ((1 << ell) - (1 << (ell - k))) - k * tail_sum
            numerator = ell * centered[k][order] * grid
            lower_denominator = d**order * (d + vmax)
            upper_denominator = d**order * (d + vmin)
            assert lower_denominator > 0 and upper_denominator > 0
            low_num += numerator // lower_denominator
            high_num += -((-numerator) // upper_denominator)
    return Fraction(low_num, grid), Fraction(high_num, grid), groups


def exact_small_green(n):
    scale = 1 << n
    return sum(
        (Fraction(1, mask.bit_count() * scale + mask)
         for mask in range(1, scale)), Fraction(0)
    )


def display(q, digits=85):
    with localcontext() as ctx:
        ctx.prec = digits
        return str(Decimal(q.numerator) / Decimal(q.denominator))


if __name__ == '__main__':
    for small_n in range(2, 11):
        lower, upper, _ = green_enclosure(small_n, min(3, small_n - 1))
        truth = exact_small_green(small_n)
        assert lower <= truth <= upper
    started = time.perf_counter()
    n, b, order, bits = 80, 10, 6, 240
    lower, upper, groups = green_enclosure(n, b, order, bits)
    elapsed = time.perf_counter() - started
    pi = Fraction(1, 1 << n)
    gamma = 1 + pi
    kappa = Fraction(1)
    mean_lower = (1 / kappa + lower) / pi
    mean_upper = (1 / kappa + upper) / pi
    mu_upper = 1 / mean_lower
    # lambda_S >= |S| gives a rigorous, inexpensive G1 upper bound.
    g1_upper = sum(
        (pi * Fraction(comb(n, k), k * k) for k in range(1, n + 1)),
        Fraction(0),
    )
    a_upper = mu_upper**2 * g1_upper / (pi * (1 - mu_upper / gamma)**2)
    fast_weight_upper = a_upper / (1 + a_upper)
    tv_upper = 2 * fast_weight_upper
    assert tv_upper < Fraction(1024, 10**30)  # 1.024e-27, exact comparison.
    # The reported executable exponential can use the rational midpoint mean.
    mean_midpoint = (mean_lower + mean_upper) / 2
    mean_rounding_tv = (mean_upper - mean_lower) / (2 * mean_lower)
    executable_tv = tv_upper + mean_rounding_tv
    assert executable_tv < Fraction(1024, 10**30)
    assert upper - lower < Fraction(428, 10**39)  # 4.28e-37.
    assert mean_upper - mean_lower < Fraction(517, 10**15)
    print(json.dumps({
        'n': n, 'head_bits': b, 'moment_order': order,
        'groups': groups, 'precision_bits': bits,
        'runtime_seconds': elapsed, 'small_exact_checks': 9,
        'grid_lower_numerator': (lower * (1 << bits)).numerator,
        'grid_upper_numerator': (upper * (1 << bits)).numerator,
        'G0_lower': display(lower), 'G0_upper': display(upper),
        'G0_width': display(upper - lower),
        'mean_lower_kappa_1': display(mean_lower),
        'mean_upper_kappa_1': display(mean_upper),
        'rational_midpoint_mean': display(mean_midpoint),
        'mean_enclosure_TV_cost': display(mean_rounding_tv),
        'G1_upper': display(g1_upper),
        'generic_TV_upper': display(2 / (gamma * mean_lower)),
        'rank_one_TV_upper': display(tv_upper),
        'executable_midpoint_TV_upper': display(executable_tv),
        'certified_rank_one_TV_less_than': '1.024e-27'
    }, indent=2))
