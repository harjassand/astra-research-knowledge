#!/usr/bin/env python3
"""Finite exact checks of the modified sparsification inequalities.

This does not execute the governing ETH counter or establish a practical speedup.
All checks use Python integers/Fraction; no floating-point acceptance decisions.
"""
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
import json


def ceil_log2_integer(x):
    assert x >= 1
    return (x - 1).bit_length()


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def first_power_two_at_least(x):
    x = ceil_fraction(Fraction(x))
    return 1 << ceil_log2_integer(max(x, 1))


def recurrence_check(max_j=100):
    records = []
    for M in (2, 3, 32, 64):
        theta = [M**j * factorial(j)**2 for j in range(max_j)]
        T = [0, 2]
        max_ratio = Fraction(0)
        for j in range(2, max_j + 1):
            tj = 4 * theta[j-1] + 2 * sum(theta[j-i] * T[i] for i in range(1, j))
            T.append(tj)
            bound = 16 * M**(j-1) * factorial(j-1)**2
            assert tj <= bound, (M, j)
            ratio = Fraction(tj, bound)
            max_ratio = max(max_ratio, ratio)
            inverse_binomial_sum = sum((Fraction(1, comb(j-1, b)**2) for b in range(1, j-1)), Fraction(0))
            assert inverse_binomial_sum <= Fraction(1, 4)
            assert 8 + 32 * inverse_binomial_sum <= 16
        b_choices = sum((Fraction(T[j], M**j * factorial(j)**2) for j in range(1, max_j + 1)), Fraction(0))
        assert b_choices <= Fraction(32, M)
        records.append({'M': M, 'max_j': max_j, 'maximum_recurrence_to_bound_ratio': str(max_ratio), 'B_choices_per_n_below_32_over_M': True})
    return records


def parameter_cap_checks():
    records = []
    for k in (2, 3, 4, 8, 16, 32, 64):
        for sigma in (Fraction(1), Fraction(1, 2), Fraction(1, 8), Fraction(1, 64), Fraction(1, 1024)):
            h0 = ceil_log2_integer(ceil_fraction(4*k/sigma))
            M = first_power_two_at_least(2048*k*h0/sigma)
            assert M < 4096*k*h0/sigma
            C = 16 * sum(M**j * factorial(j)**2 for j in range(k-1))
            B = 2 * sum(M**j * factorial(j)**2 for j in range(k))
            h = ceil_log2_integer(4*C*M)
            assert ceil_log2_integer(M) <= 5*h0
            assert h <= 9*k*h0
            assert 32*h <= sigma*M
            assert C <= 32*M**(k-2)*factorial(k-2)**2
            assert B <= 4*M**(k-1)*factorial(k-1)**2
            records.append({'k': k, 'sigma': str(sigma), 'log2_M': ceil_log2_integer(M), 'log2_4CM_ceiling': h, 'cap_certified': True})
    return records


def main():
    result = {
        'scope': 'Finite exact algebraic checks only; not an implementation of the full asymptotic counter.',
        'recurrence_cases': recurrence_check(),
        'explicit_parameter_cap_cases': parameter_cap_checks(),
        'all_assertions_passed': True,
    }
    path = Path(__file__).with_name('uniform_width_bound_checks.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(f'PASS: 396 insertion recurrences and 35 exact parameter caps; results {path}')


if __name__ == '__main__':
    main()
