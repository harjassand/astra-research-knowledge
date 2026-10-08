"""Exact arithmetic for the two-state molecular counterexample.

This checks only the displayed rational pulse kernels and the selected S_4
instance.  The universal vanishing on all 2x2 matrices follows from the
Amitsur--Levitzki identity, not from this finite diagnostic.
"""

from fractions import Fraction as F
from itertools import permutations


def mm(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def permutation_sign(sigma):
    inversions = sum(
        sigma[i] > sigma[j]
        for i in range(len(sigma))
        for j in range(i + 1, len(sigma))
    )
    return -1 if inversions % 2 else 1


def standard_s4(matrices):
    out = [[F(0), F(0)], [F(0), F(0)]]
    for sigma in permutations(range(4)):
        term = matrices[sigma[0]]
        for i in sigma[1:]:
            term = mm(term, matrices[i])
        sign = permutation_sign(sigma)
        for i in range(2):
            for j in range(2):
                out[i][j] += sign * term[i][j]
    return out


P_A = [[F(9, 10), F(1, 10)], [F(1, 5), F(4, 5)]]
P_B = [[F(7, 10), F(3, 10)], [F(2, 5), F(3, 5)]]
P_3 = [[F(4, 5), F(1, 5)], [F(1, 10), F(9, 10)]]
P_4 = [[F(17, 20), F(3, 20)], [F(3, 10), F(7, 10)]]

AB = mm(P_A, P_B)
BA = mm(P_B, P_A)
S4 = standard_s4([P_A, P_B, P_3, P_4])

assert AB == [[F(67, 100), F(33, 100)], [F(23, 50), F(27, 50)]]
assert BA == [[F(69, 100), F(31, 100)], [F(12, 25), F(13, 25)]]
assert AB[0][1] - BA[0][1] == F(1, 50)
assert S4 == [[F(0), F(0)], [F(0), F(0)]]

print("P_A P_B =", AB)
print("P_B P_A =", BA)
print("OFF-to-ON order effect =", AB[0][1] - BA[0][1])
print("S4(P_A,P_B,P_3,P_4) =", S4)
