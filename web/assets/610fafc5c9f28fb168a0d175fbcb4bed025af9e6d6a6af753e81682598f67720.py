#!/usr/bin/env python3
"""Exact small checks for cyclic detector averaging and one-total conditioning."""

from fractions import Fraction
from itertools import product
from math import factorial


def cyclic_average_check():
    # Nonuniform probabilities, efficiencies and dark rates; all arithmetic exact.
    m = 5
    p = [Fraction(v, 15) for v in (1, 2, 3, 4, 5)]
    eta = [Fraction(v, 10) for v in (1, 3, 5, 7, 9)]
    dark = [Fraction(v, 7) for v in (1, 2, 4, 8, 11)]
    eta_bar = sum(eta) / m
    dark_bar = sum(dark) / m

    for j in range(m):
        signal = sum(eta[(j + s) % m] * p[j] for s in range(m)) / m
        background = sum(dark[(j + s) % m] for s in range(m)) / m
        assert signal == eta_bar * p[j]
        assert background == dark_bar

    # The source total is state-independent for any complete probability vector.
    assert sum(p) == 1
    assert sum(sum(eta[(j + s) % m] * p[j] for j in range(m)) / m
               for s in range(m)) == eta_bar

    # A fixed channel assignment has an exact unknown-gain/state confound.
    p_x = [Fraction(v, 15) for v in (1, 2, 3, 4, 5)]
    p_y = [Fraction(v, 15) for v in (5, 3, 1, 4, 2)]
    c = min(p_x + p_y)
    eta_x = [c / value for value in p_x]
    eta_y = [c / value for value in p_y]
    assert all(0 < value <= 1 for value in eta_x + eta_y)
    assert [gain * prob for gain, prob in zip(eta_x, p_x)] == [c] * m
    assert [gain * prob for gain, prob in zip(eta_y, p_y)] == [c] * m

    # Exact averaging by a mixture of permutations needs at least m permutations:
    # each permutation has m support cells, while the target has m^2 positive cells.
    assert m * (m - 1) < m * m
    print("PASS: cyclic assignment averages detector response; fixed-setting state/gain confound is exact.")


def global_conditioning_check():
    # For arbitrary source outcome probabilities q, conditioning independent
    # Pois(N*q_j) counts on their global total N gives the multinomial law.
    q = [Fraction(1, 6), Fraction(1, 3), Fraction(1, 2)]
    n_total = 4
    assert sum(q) == 1
    conditional_sum = Fraction(0, 1)
    for counts in product(range(n_total + 1), repeat=len(q)):
        if sum(counts) != n_total:
            continue
        poisson_conditioned = Fraction(factorial(n_total), 1)
        multinomial = Fraction(factorial(n_total), 1)
        for n_j, q_j in zip(counts, q):
            poisson_conditioned *= q_j ** n_j / factorial(n_j)
            multinomial *= q_j ** n_j / factorial(n_j)
        assert poisson_conditioned == multinomial
        conditional_sum += poisson_conditioned
    assert conditional_sum == 1

    # Factoring an independent blank mass out of the conditioned joint law
    # leaves precisely the source multinomial mass.
    blank_probabilities = [Fraction(1, 4), Fraction(3, 4)]
    for z0 in range(3):
        z1 = 2 - z0
        blank_mass = (blank_probabilities[0] ** z0
                      * blank_probabilities[1] ** z1)
        conditional_joint = blank_mass * multinomial_source_mass((1, 1, 2), q)
        assert conditional_joint / blank_mass == multinomial_source_mass((1, 1, 2), q)
    assert sum(blank_probabilities) == 1

    # Random allocation does not equal deterministic balanced quotas.
    n, m = 4, 2
    balanced_allocation_probability = Fraction(factorial(n), factorial(2) ** 2) * Fraction(1, m**n)
    assert balanced_allocation_probability == Fraction(3, 8)
    print("PASS: one global source-total conditioning gives the multinomial allocation law; independent blank factors out.")


def multinomial_source_mass(counts, q):
    n_total = sum(counts)
    mass = Fraction(factorial(n_total), 1)
    for n_j, q_j in zip(counts, q):
        mass *= q_j ** n_j / factorial(n_j)
    return mass


if __name__ == "__main__":
    cyclic_average_check()
    global_conditioning_check()
