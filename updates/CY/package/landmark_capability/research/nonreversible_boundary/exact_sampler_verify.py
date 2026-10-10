"""Exact lazy-prefix sampler on the small unbalanced-gate fixture.

For this eight-state identity check, the certified prefix oracle is made
from exact Fraction stationary masses. The scalable version substitutes
the polynomial-precision oracle proved in UNBALANCED_STEADY_STATE.txt.
"""

from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from random import Random


n = 3
states = list(product(range(2), repeat=n))
N = len(states)
idx = {state: j for j, state in enumerate(states)}
up, down, gate_rate = F(1, 10), F(6, 5), F(7, 10)
q = [[F(0) for _ in range(N)] for _ in range(N)]
for j, state in enumerate(states):
    for i, bit in enumerate(state):
        rate = up if bit == 0 else down
        other = list(state)
        other[i] ^= 1
        q[j][idx[tuple(other)]] += rate
        q[j][j] -= rate
q[idx[(0, 0, 0)]][idx[(1, 1, 1)]] += gate_rate
q[idx[(0, 0, 0)]][idx[(0, 0, 0)]] -= gate_rate


def solve_rational(a, b):
    a = [row[:] for row in a]
    b = b[:]
    for col in range(len(b)):
        pivot = next(row for row in range(col, len(b)) if a[row][col])
        a[col], a[pivot] = a[pivot], a[col]
        b[col], b[pivot] = b[pivot], b[col]
        scale = a[col][col]
        a[col] = [z / scale for z in a[col]]
        b[col] /= scale
        for row in range(len(b)):
            if row == col:
                continue
            scale = a[row][col]
            if scale:
                a[row] = [x - scale*y for x, y in zip(a[row], a[col])]
                b[row] -= scale*b[col]
    return b


eq = [[q[col][row] for col in range(N)] for row in range(N)]
eq[-1] = [F(1)] * N
rhs = [F(0)] * (N-1) + [F(1)]
stationary = solve_rational(eq, rhs)

# Explicit lower bound from the local-path uniformization proof.
max_local_exit = n * down
max_gate_exit = gate_rate
M = 2 * (max_local_exit + max_gate_exit)
p = min(up / M, F(1, 2))
L = n
eta = (p / 4) ** L
assert all(mass >= eta for mass in stationary)


@lru_cache(maxsize=None)
def prefix_mass(prefix):
    return sum(mass for state, mass in zip(states, stationary)
               if state[:len(prefix)] == prefix)


@lru_cache(maxsize=None)
def certified_approx(prefix, ell, d):
    """Return dyadic mass with absolute error <= eta*2^-ell/(64*d)."""
    tolerance = eta * F(1, 2**ell) / (64*d)
    digits = 0
    while F(1, 2**digits) > tolerance:
        digits += 1
    true_mass = prefix_mass(prefix)
    floor_numerator = (true_mass.numerator * (2**digits)) // true_mass.denominator
    return F(floor_numerator, 2**digits)


def sample_exact(rng):
    prefix = ()
    bit_count = 0
    for _ in range(n):
        d = 2
        prefix_bits = 0
        ell = 0
        while True:
            ell += 1
            bit_count += 1
            prefix_bits = 2*prefix_bits + rng.getrandbits(1)
            lo = F(prefix_bits, 2**ell)
            hi = F(prefix_bits+1, 2**ell)
            masses = [certified_approx(prefix+(a,), ell, d) for a in range(d)]
            total = sum(masses)
            cumulative = [sum(masses[:a+1])/total for a in range(d-1)]
            radius = F(1, 2**(ell+4))
            choice = None
            for a in range(d):
                left = F(0) if a == 0 else cumulative[a-1]+radius
                right = F(1) if a == d-1 else cumulative[a]-radius
                if lo > left and hi < right:
                    choice = a
                    break
            if choice is not None:
                prefix += (choice,)
                break
    return prefix, bit_count


rng = Random(20261010)
draws = 5000
counts = Counter()
bits = 0
for _ in range(draws):
    x, b = sample_exact(rng)
    counts[x] += 1
    bits += b
empirical_tv = 0.5 * sum(abs(counts[x]/draws - float(stationary[idx[x]]))
                         for x in states)
print('minimum stationary mass', float(min(stationary)))
print('certified eta', float(eta))
print('exact stationary expected active',
      float(sum(stationary[j]*sum(x) for j, x in enumerate(states))))
print('samples', draws, 'mean fair bits per configuration', bits/draws)
print('empirical TV from exact stationary masses', empirical_tv)
