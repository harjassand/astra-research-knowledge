#!/usr/bin/env python3
"""Exact rational witness: spectral clipping need not be CP after tensoring.

Each qutrit factor is a convex mixture of the 1->2 universal-cloner marginal
(depolarizing shrinkage 5/8) and MUB dephasing channels, hence is
self-compatible. Their tensor product is self-compatible. The clipped
Weyl-diagonal candidate mu_x=(2 lambda_x-1)_+ has a negative inverse-Weyl
probability, so it is not CP. This refutes that specific construction only;
it does not refute existence of another EB comparator.
"""

from fractions import Fraction as F


D = 3
labels = [(a, b) for a in range(D) for b in range(D)]
lines = [
    {((slope * t) % D, t) for t in range(1, D)} for slope in range(D)
] + [{(t, 0) for t in range(1, D)}]


def line_of(label):
    return next(i for i, line in enumerate(lines) if label in line)


def factor_spectrum(alpha, line_weights):
    """Line-constant spectrum of alpha*D_(5/8)+(1-alpha)*sum q_L Delta_L."""
    alpha = F(alpha)
    assert sum(line_weights, F(0)) == 1
    shrinkage = F(5, 8)
    values = []
    for label in labels:
        if label == (0, 0):
            values.append(F(1))
        else:
            q = line_weights[line_of(label)]
            values.append(alpha * shrinkage + (1 - alpha) * q)
    return values


q1 = [F(3, 100), F(92, 100), F(4, 100), F(1, 100)]
q2 = [F(33, 100), F(26, 100), F(36, 100), F(5, 100)]
lam1 = factor_spectrum(F(1, 4), q1)
lam2 = factor_spectrum(F(39, 50), q2)
lam = [x * y for x in lam1 for y in lam2]
mu = [max(2 * value - 1, F(0)) for value in lam]
mu[0] = F(1)

# Labels for a Weyl group element g=(c,e) and mode x=(a,b) have character
# omega^(e*a - b*c). In Q(omega), store r+s*omega, with omega^2=-1-omega.
omega_powers = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(-1))]


def exponent(g, x):
    c, e = g
    a, b = x
    return (e * a - b * c) % D


# Use g1=(2,1), g2=(1,0). p'_g is the inverse Fourier probability for
# the clipped map on M_3 tensor M_3. Its denominator is D^4 = 81.
g1, g2 = (2, 1), (1, 0)
real_coeff, omega_coeff = F(0), F(0)
for i, x1 in enumerate(labels):
    for j, x2 in enumerate(labels):
        e = (exponent(g1, x1) + exponent(g2, x2)) % D
        a, b = omega_powers[e]
        mass = mu[i * D * D + j]
        real_coeff += mass * a
        omega_coeff += mass * b

p_numerator = (real_coeff / D**4, omega_coeff / D**4)
assert p_numerator == (F(-71, 162000), F(0))
assert p_numerator[0] < 0

print("lambda factor 1:", lam1)
print("lambda factor 2:", lam2)
print("clipped nonzero support:", [(i, x) for i, x in enumerate(mu) if x])
print("clipped inverse-Weyl probability at g=((2,1),(1,0)):", p_numerator[0])
print("Conclusion: spectral clipping is not CP for this compatible M9 channel.")
