"""Exact rational check of the scoped latent-exchange repair in REPORT.md.

This is a finite fixture, not a proof of the general statement or a biochemical
experiment. The four pathway rate coefficients are fixed to one; the fifth
exchange coefficient eta is arbitrary and nonnegative.
"""

from fractions import Fraction as F


def currents(B, C, gates, eta):
    g1, g2, g3, g4 = gates
    return (
        g1 * (F(4) - B),
        g2 * (B - F(1)),
        g3 * (F(4) - C),
        g4 * (C - F(1)),
        eta * (B - C),
    )


def residual(js):
    j1, j2, j3, j4, j5 = js
    return (j1 - j2 - j5, j3 - j4 + j5)


old_gates = (F(1, 2), F(1), F(1, 2), F(1))
new_gates = (F(9, 8), F(9, 8), F(3, 8), F(3, 8))
old = currents(F(2), F(2), old_gates, F(17, 19))
new = currents(F(5, 2), F(5, 2), new_gates, F(17, 19))

assert old == (F(1), F(1), F(1), F(1), F(0))
assert new == (F(27, 16), F(27, 16), F(9, 16), F(9, 16), F(0))
assert residual(old) == (F(0), F(0))
assert residual(new) == (F(0), F(0))
assert sum(old_gates) == sum(new_gates) == F(3)
assert new[1] / new[3] == F(3)

# For arbitrary eta>=0, v^T(-J)v = 9/4*v_B^2 + 3/4*v_C^2
#                              + eta*(v_B-v_C)^2 >= 3/4*||v||_2^2.
# Check an exact nonzero example, while the displayed identity proves the
# uniform statement for this linear two-state fixture.
eta = F(17, 19)
vB, vC = F(7, 5), F(-2, 3)
quadratic = F(9, 4) * vB**2 + F(3, 4) * vC**2 + eta * (vB - vC) ** 2
assert quadratic >= F(3, 4) * (vB**2 + vC**2)

print(f"baseline currents={old}; target currents={new}")
print(f"gate sum={sum(new_gates)}; product ratio={new[1] / new[3]}")
print("unknown exchange cancels identically when B=C=5/2")
print("uniform Jacobian decay bound: at least 3/4 in this toy's time units")
