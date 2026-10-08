#!/usr/bin/env python3
"""Exact rational fixture for the uniform mixing certificate.

Run from the repository root with:
    python3 -B outputs/research/reaction_dynamics/cycle4/leaves/uniform_mixing/rational_fixture.py

This checks the displayed rational inequalities and constants. The analytic
proof in PROOF.txt supplies the all-state argument; this script is a fixture
reproducer, not a substitute for that proof.
"""

from fractions import Fraction as Q
from math import factorial
R = Q(6, 5)
c = Q(1, 10)


def g(m: int) -> Q:
    """Uniform upper envelope of p(R-1)R^m-q(1-R^-1)mR^m+u m."""
    return Q(2, 5) * R**m - Q(m, 6) * R**m + 2 * m


def w_one(m: int) -> Q:
    """max over the [1,2] box of LV+cV at a=1, substrate count m."""
    return 2 + 2 * (R**m - 1) + g(m) + c * (1 + R**m)


def w_ge_two(a: int, m: int) -> Q:
    """max over the box of LV+cV at a>=2 and substrate count m."""
    return 2 - a + a * g(m) - a * (a - 1) * m + c * (a + R**m)


# The high-substrate tail estimate uses f(m)=g(m)/R^m. For m>=5,
# (m+1)/R^(m+1) <= m/R^m, so f is strictly decreasing.
f25 = Q(2, 5) - Q(25, 6) + Q(50, 1) / R**25
assert R == Q(6, 5)
assert f25 == Q(-230465642630552213999, 71075720074824253440)
assert f25 <= -3

# Exact maximization of LV+cV over all a>=0 on the low substrate set m<=24.
# For a>=2 and m>=1 this is a concave quadratic in a, so checking the two
# integers bracketing its rational vertex (and a=2) is exhaustive. At m=0
# the expression is decreasing in a>=2.
low_candidates = []
for m in range(25):
    if m == 0:
        candidates = {2}
    else:
        linear = -1 + g(m) + m + c
        vertex = linear / (2 * m)
        below = vertex.numerator // vertex.denominator
        candidates = {2, max(2, below), max(2, below + 1)}
    low_candidates.append((w_one(m), 1, m))
    low_candidates.extend((w_ge_two(a, m), a, m) for a in candidates)
low_max, low_a, low_b = max(low_candidates)
assert (low_max, low_a, low_b) == (
    Q(369138966157, 12207031250), 1, 14
)
C = low_max
# On a=0, LV+cV = alpha(1-R^m)+(1/5)R^m <= 1/5 uniformly for alpha in [1,2].
assert Q(1, 5) < C
# For m>=25, g(m)<=-3R^m and the catalyst-death boundary correction gives
# LV<=2-aR^m<=2-(a+R^m)/2=2-V/2. Since C>2, this is below C-cV.
assert C > 2

# Common finite skeleton drift set D={V<d}, with V(a,m)=a+R^m for a>=1
# and V(0,m)=2R^m. The slightly conservative floor/ceil bounds are intentional.
d = 2 * C / c + 4
A_C = d.numerator // d.denominator
B_C = 0
while R ** (B_C + 1) < d:
    B_C += 1
assert (A_C, B_C) == (608, 35)
assert R**B_C < d <= R ** (B_C + 1)
L_C = A_C + B_C
A_path = A_C
assert (L_C, A_path) == (643, 608)

# Maximum total exit rate on every state of every clearing path. The channels
# are alpha; delta*a; p*a; (q+u)*a*m; and v*(a)_2*m, with every upper endpoint 2.
Lambda = (
    2
    + 4 * A_path
    + 4 * A_path * B_C
    + 2 * B_C * A_path * (A_path - 1)
)
assert Lambda == 25921474

T = 1 / (2 * C + Lambda)
lam = 1 / (1 + c * T)
b = C * T
lam_out = lam + b / d
assert T > 0 and T <= 1 / (2 * C)
assert Lambda * T < 1
assert d > 2 * C * (1 + c * T) / c
assert lam_out < 1

# rho*=1. Since T<1, (T^ell)/ell! decreases in ell, so the rational
# minorization is exactly eta=T^L/(3 L!). Leave it factored to avoid a huge
# decimal rendering; it is positive and less than 1/3.
assert T < 1
assert L_C == 643
eta = T**L_C / (3 * factorial(L_C))
assert 0 < eta < Q(1, 3)

print("R =", R)
print("c =", c)
print("C =", C)
print("low max LV+cV =", low_max, "at (a,m) =", (low_a, low_b))
print("d =", d)
print("A_C, B_C, L_C, A_path =", A_C, B_C, L_C, A_path)
print("Lambda =", Lambda)
print("T =", T)
print("lambda =", lam)
print("b =", b)
print("lambda_hat = lambda+b/d =", lam_out)
print("Lambda*T < 1:", Lambda * T < 1)
print("eta = T^643/(3*643!) (exact positive rational, factored)")
