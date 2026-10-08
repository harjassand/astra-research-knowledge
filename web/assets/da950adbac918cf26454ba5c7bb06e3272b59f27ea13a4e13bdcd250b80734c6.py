"""Exact rational replay of the parameter substitutions in arXiv:2610.06533v1.

Scope: checks the arithmetic used for its eight-output-qubit, p=1 certificate.
It does not independently reconstruct the high-girth representation or prove
the paper's general entropy and operator inequalities.
"""

from fractions import Fraction as Q
from math import factorial


gamma = 2
k = 64
D = 2 * gamma * k
d = D * (D - 1)
m = 3 * (4 * d + 53)
N = 48 * m - 14

assert D == 256
assert d == 65280
assert m == 783519
assert N == 37608898

# Chebyshev-filter inflation condition, with B^2 = 50, C^2 = 103/2,
# and u = 9/8.
filter_margin = Q(127, 128) ** 2 * Q(103, 100) - Q(145, 144) ** 2
assert filter_margin == Q(4247, 132710400)
assert filter_margin > 0

# (9/8)^6 > 2 implies (9/8)^(2m) > 4 for m >= 6.
assert 9**6 > 2 * 8**6
assert m >= 6

# The trace penalty in the source has alpha < 2^(4d + 3 - m/3) = 2^-50.
assert m % 3 == 0
assert 4 * d + 3 - m // 3 == -50
assert 257 * Q(1, 2**50) < Q(1, 2**40)

# The channel entropy criterion uses delta=2^-40 and epsilon=D^2 delta.
delta = Q(1, 2**40)
epsilon = D**2 * delta
assert delta < Q(1, D**2)
assert epsilon == Q(1, 2**24)

# Exact logarithm enclosures used in the paper.  The first four terms of
# log(2)=2*atanh(1/3) give the lower bound.  The source's atanh remainder
# bound gives log(615/512) < 183299/10^6.
log2_lower = sum(
    (Q(2, 3 ** (2 * j + 1) * (2 * j + 1)) for j in range(4)), Q(0)
)
assert log2_lower == Q(53056, 76545)
log615_512_upper = Q(183299, 10**6)
z = Q(103, 1127)
atanh_upper = 2 * (z + z**3 / 3 + z**5 / (5 * (1 - z**2)))
assert atanh_upper < log615_512_upper

fixed_margin_lower = Q(17, 32) * log2_lower - 2 * log615_512_upper
assert fixed_margin_lower > Q(12891, 8_000_000)
assert Q(12891, 8_000_000) > Q(1, 640)

# For epsilon=2^-24, 2 epsilon log(K) + h_b(epsilon)
# <= epsilon*(1 + 40 log 2) < 29*2^-24, using log(2)<7/10.
# The finite Taylor polynomial below proves exp(7/10)>2.
x = Q(7, 10)
exp_partial = sum((x**j / factorial(j) for j in range(6)), Q(0))
assert exp_partial == Q(24162857, 12000000)
assert exp_partial > 2
error_upper = Q(29, 2**24)
assert Q(1, 640) - error_upper > Q(1, 1024)

print("PASS: source parameter arithmetic; gap lower bound > 1/1024 nats")
print(f"D={D}, d={d}, m={m}, input qubits N={N}")
print(f"epsilon=2^-24, fixed margin lower={fixed_margin_lower}")
print(f"final certified rational lower={Q(1, 640) - error_upper}")
