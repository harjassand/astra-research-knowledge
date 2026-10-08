"""Exact scalar replay of the fixed-vector MOE filter obstruction.

This checks identities and parameter implications for D=256. It does not
construct the enormous permutation matrices or validate the source theorem.
"""

from fractions import Fraction as Q
from math import sqrt

D = 256
d = D * (D - 1)
J2 = Q(50)
C2 = Q(103, 2)

# The off-diagonal all-ones coefficient matrix has HS norm one and its
# eigenvalue on the common constant vector is sqrt(d).
assert d == 65_280
assert J2 == 50
assert C2 == Q(103, 2)
assert d / J2 == Q(6528, 5)

# Unfiltered purity is 1. Free-model purity and source target are as stated.
free_purity = Q(D + J2, D**2)
target_purity = Q(1, D) + C2 / D**2
assert free_purity == Q(153, 32_768)
assert target_purity == Q(615, 131_072)
assert free_purity < target_purity < 1

# If F fixes the common line with amplitude f, the output purity is
# 1/D + (D-1) f^4/D. Meeting the source target is exactly this inequality.
# f^4 <= C^2/[D(D-1)] is an exact rational condition on f^4.
f4_cap = C2 / (D * (D - 1))
assert f4_cap == Q(103, 130_560)
assert Q(1, D) + Q(D - 1, D) * f4_cap == target_purity

# If F=(I+R)^(-1/2) acts as f on the line, f^4=1/(1+r0)^2.
# The necessary condition is (1+r0)^2 >= D(D-1)/C^2.
r0_ratio = Q(D * (D - 1), 1) / C2
assert r0_ratio == Q(130_560, 103)

print("PASS: exact purity target and fixed-line attenuation conditions")
print(f"sqrt(d)={sqrt(d):.9f}; free J={sqrt(J2):.9f}; target C={sqrt(C2):.9f}")
print(f"necessary f^2 <= {sqrt(float(f4_cap)):.9f}")
print(f"necessary R-eigenvalue >= {sqrt(float(r0_ratio)) - 1:.9f}")
