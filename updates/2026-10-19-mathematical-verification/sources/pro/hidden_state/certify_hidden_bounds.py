#!/usr/bin/env python3
"""Exact algebraic certificates for the hidden-state example (standard library).

No floating-point operation is used in any certificate or assertion. The
positive algebraic number y=2**(-1/64) is isolated on a dyadic grid. The
general inequalities being illustrated are proved in proof.tex.
"""
from fractions import Fraction as F
import json


def decimal_enclosure(lo, hi, places=24):
    scale = 10 ** places
    lower = lo.numerator * scale // lo.denominator
    upper = -((-hi.numerator * scale) // hi.denominator)

    def fmt(n):
        sign = '-' if n < 0 else ''
        n = abs(n)
        q, r = divmod(n, scale)
        return f'{sign}{q}.{r:0{places}d}'
    return [fmt(lower), fmt(upper)]


def main():
    bits = 120
    den = 2 ** bits
    target = 2 ** (64 * bits - 1)
    low, high = 0, den
    while high - low > 1:
        middle = (low + high) // 2
        if middle ** 64 <= target:
            low = middle
        else:
            high = middle
    assert low ** 64 < target < high ** 64
    yl, yh = F(low, den), F(high, den)

    ml = (2 * yl**8 - 1 - yh**18) / 4
    mh = (2 * yh**8 - 1 - yl**18) / 4
    assert ml > 0
    alpha = F(1, 64)
    nu = F(1, 2**18)
    c = nu / 2
    factor = F(2**38) * (c / 64 + F(63, 16))
    cl, ch = factor * yl**19, factor * yh**19
    floorl, floorh = ml / (4 * ch), mh / (4 * cl)
    assert mh/cl < c
    assert floorl > F('0.000000000000000789')

    # nu**(2-alpha) = 2**(-36) / y**18.
    defectl = ml / (2**36 * yh**18 * (1-alpha))
    defecth = mh / (2**36 * yl**18 * (1-alpha))
    assert defectl > F('0.0000000000000499')
    out = {
        'status': 'PASS',
        'arithmetic': 'exact integers and Fraction intervals only',
        'algebraic_number': 'positive y satisfying y**64=1/2',
        'root_isolation_bits': bits,
        'alpha': '1/64',
        'observed_min_eigenvalue': '1/262144',
        'observed_stationary_minimum': '1/4',
        'fractional_power_negative_entry_magnitude': decimal_enclosure(ml,mh),
        'equilibrium_second_lag_defect_floor': decimal_enclosure(defectl,defecth,30),
        'arbitrary_hidden_entropy_bound_constant': decimal_enclosure(floorl,floorh,33),
        'certified_strict_hidden_entropy_floor': 'sigma > 7.89e-16 / observation interval',
        'scope': 'stationary homogeneous finite hidden CTMC; deterministic observation partition; all-even time reversal; observed P and P^2 at lags 1 and 2',
        'does_not_claim': 'the four-state minimum 26.1789 holds for arbitrary hidden realizations',
    }
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
