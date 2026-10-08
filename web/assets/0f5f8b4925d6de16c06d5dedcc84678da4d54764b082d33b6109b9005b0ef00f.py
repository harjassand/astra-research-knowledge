"""Exact 2x2 checks for Poisson, geometric, and NB conditional laws."""
from fractions import Fraction
from itertools import product
from math import factorial

row_margins = (2, 2)
col_margins = (2, 2)
# Multiplicatively separable Poisson/NB odds: q_ij = a_i b_j.
a = (2, 3)
b = (1, 2)
q = tuple(tuple(Fraction(ai * bj, 10) for bj in b) for ai in a)

tables = []
for x11 in range(3):
    x12 = row_margins[0] - x11
    x21 = col_margins[0] - x11
    x22 = row_margins[1] - x21
    table = ((x11, x12), (x21, x22))
    if x12 >= 0 and x21 >= 0 and x22 >= 0 and x21 + x22 == col_margins[1]:
        tables.append(table)

poisson_weights = []
for table in tables:
    w = Fraction(1)
    for i, j in product(range(2), repeat=2):
        w *= q[i][j] ** table[i][j] / factorial(table[i][j])
    poisson_weights.append(w)
poisson_total = sum(poisson_weights)
poisson_law = tuple(w / poisson_total for w in poisson_weights)

# NB(shape=r, odds=q) has base weight (r)_x / x! after q^x cancels
# on the fixed-margin fiber. Shape 1 is geometric; shape 2 is overdispersed.
def rising_factorial(r, k):
    out = 1
    for j in range(k):
        out *= r + j
    return out

def nb_law(shape):
    weights = []
    for table in tables:
        w = Fraction(1)
        for i, j in product(range(2), repeat=2):
            w *= Fraction(rising_factorial(shape, table[i][j]), factorial(table[i][j])) * q[i][j] ** table[i][j]
        weights.append(w)
    z = sum(weights)
    return tuple(w / z for w in weights)

geometric_law = nb_law(1)
nb2_law = nb_law(2)
assert len(tables) == 3
assert poisson_law == (Fraction(1, 6), Fraction(2, 3), Fraction(1, 6))
assert geometric_law == (Fraction(1, 3),) * 3
assert nb2_law == (Fraction(9, 34), Fraction(16, 34), Fraction(9, 34))

for table, p, g, n in zip(tables, poisson_law, geometric_law, nb2_law):
    print(table, "Poisson=", p, "geometric(shape 1)=", g, "NB(shape 2)=", n)
