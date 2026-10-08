#!/usr/bin/env python3
"""Exact finite checks for the N76 Foster obstruction and N77 class escape core.

Uses only Python's standard library. This script checks rational factorial
ratios and finite-state flux identities. It is evidence for the displayed
algebra, not a proof of the asymptotic claims or a general recurrence theorem.
"""
from fractions import Fraction
from math import factorial, log


def falling(x: int, order: int) -> int:
    out = 1
    for j in range(order):
        out *= x - j
    return out


def prop(x: tuple[int, ...], source: tuple[int, ...]) -> int:
    out = 1
    for value, order in zip(x, source):
        if value < order:
            return 0
        out *= falling(value, order)
    return out


def factorial_potential_factor(x: tuple[int, int]) -> int:
    complexes = ((2, 0), (1, 1), (0, 0), (1, 0))
    available = [
        factorial(x[0] - a) * factorial(x[1] - b)
        for a, b in complexes
        if x[0] >= a and x[1] >= b
    ]
    return min(available)


# Network: 2A <-> A+B, 0 <-> A, with rates 1, 3, 1, 1.
sources = ((2, 0), (1, 1), (0, 0), (1, 0))
products = ((1, 1), (2, 0), (1, 0), (0, 0))
rate_constants = (1, 3, 1, 1)
for n in range(4, 41):
    state = (2 * n, n)
    base = factorial_potential_factor(state)
    expected = (
        Fraction(n + 1, 2 * n - 2),
        Fraction(2 * n - 1, n),
        Fraction(2 * n - 1, 1),
        Fraction(1, 2 * n - 2),
    )
    observed = []
    for source, product in zip(sources, products):
        after = tuple(x - y + z for x, y, z in zip(state, source, product))
        observed.append(Fraction(factorial_potential_factor(after), base))
    assert tuple(observed) == expected, (n, observed, expected)

# Independently check the generator formula at a large n. The exact
# factorial ratios above are the primary finite checks; this numeric line
# merely confirms positive drift on a large sample, not its asymptotics.
n = 10000
terms = (
    2 * n * (2 * n - 1) * log((n + 1) / (2 * n - 2)),
    6 * n * n * log((2 * n - 1) / n),
    log(2 * n - 1),
    -2 * n * log(2 * n - 2),
)
lf = sum(terms)
assert lf > 0

# Three-reaction N77 core: 2C -> A+B+C -> 3A+2B -> 2C.
core_sources = ((0, 0, 2), (1, 1, 1), (3, 2, 0))
core_products = ((1, 1, 1), (3, 2, 0), (0, 0, 2))
for n in range(0, 41):
    states = ((n, 0, 2), (n + 1, 1, 1), (n + 3, 2, 0))
    rates = (2, n + 1, 2 * (n + 1) * (n + 2) * (n + 3))
    poisson_weights = tuple(
        Fraction(1, factorial(a) * factorial(b) * factorial(c))
        for a, b, c in states
    )
    fluxes = tuple(w * rate for w, rate in zip(poisson_weights, rates))
    assert fluxes == (Fraction(1, factorial(n)),) * 3, (n, fluxes)
    for phase, state in enumerate(states):
        enabled = []
        for i, (source, product) in enumerate(zip(core_sources, core_products)):
            rate = prop(state, source)
            if rate:
                target = tuple(x - y + z for x, y, z in zip(state, source, product))
                enabled.append((i, target, rate))
        assert enabled == [(phase, states[(phase + 1) % 3], rates[phase])]
    assert min(s[0] for s in states) == n

# N50 exact unbounded-class certificate for 0 <-> A, rates in [1,4].
# q=4, z_P=1/4, eta=1/4, a=1/2, p=0, c=1, and
# F_z(x)=min{0, x-2z^2, (1/2)z^-2-x}.
# The interval is Q_z=[2z^2,(1/2)z^-2]. For every 0<z<=1/4:
#   2z^2 >= z^2 and (1/2)z^-2 <= z^-2 (condition B);
#   z >= 2z^2 and z^-1 <= (1/2)z^-2 (condition C), both from z<=1/2;
#   at c=1, 1-2z^2 >= 7/8 and (1/2)z^-2-1 >= 7 (condition A).
# At the lower active facet x<=2z^2, k_birth-k_death*x >= 1-8z^2 >= 1/2.
# At the upper active facet x>=(1/2)z^-2,
# k_death*x-k_birth >= (1/2)z^-2-4 >= 4 >= 1/2 (condition D).
z_endpoint = Fraction(1, 4)
assert 2 * z_endpoint**2 >= z_endpoint**2
assert Fraction(1, 2) * z_endpoint**-2 <= z_endpoint**-2
assert z_endpoint >= 2 * z_endpoint**2
assert z_endpoint**-1 <= Fraction(1, 2) * z_endpoint**-2
assert 1 - 2 * z_endpoint**2 >= Fraction(7, 8)
assert Fraction(1, 2) * z_endpoint**-2 - 1 >= 7
assert 1 - 8 * z_endpoint**2 >= Fraction(1, 2)
assert Fraction(1, 2) * z_endpoint**-2 - 4 >= 4

print(
    "PASS: N76 exact factorial ratios for n=4..40; N77 exact transition and "
    "Poisson-flux identities for n=0..40; N50 0<->A endpoint inequalities; "
    "sample N76 LF(2n,n)>0 at n=10000."
)
