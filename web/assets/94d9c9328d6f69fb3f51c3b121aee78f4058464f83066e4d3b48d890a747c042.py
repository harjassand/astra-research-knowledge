#!/usr/bin/env python3
"""Exact Fraction check for the non-detailed-balanced weighted-correction fixture."""
from fractions import Fraction
from itertools import product

R = Fraction(3, 2)
EPS = Fraction(1)
K = Fraction(1)
ALPHA, DELTA = Fraction(2), Fraction(1)
GAMMA = (Fraction(1), Fraction(1))
MU = (Fraction(1), Fraction(1))
ETA = (Fraction(1), Fraction(1))
ZETA = (Fraction(1), Fraction(2))
WEIGHT = (Fraction(2), Fraction(3))
P = Q = U = VREV = Fraction(1)


def potential(x):
    a, c1, c2, b = x
    S = c1 + c2
    return (Fraction(1 + a) + WEIGHT[0]*c1 + WEIGHT[1]*c2
            + R**b * (1 + EPS * Fraction(int(a == 0), 1 + S))
            + K * int(a + S == 0))


def channels(x):
    a, c1, c2, b = x
    c = (c1, c2)
    out = [
        ((1, 0, 0, 0), ALPHA),
        ((-1, 0, 0, 0), Fraction(a)*DELTA),
        ((0, 1, 0, 0), GAMMA[0]),
        ((0, -1, 0, 0), MU[0]*c1),
        ((0, 0, 1, 0), GAMMA[1]),
        ((0, 0, -1, 0), MU[1]*c2),
        ((0, 0, 0, 1), P*a),
        ((0, 0, 0, -1), Q*a*b),
        ((1, 0, 0, 0), U*a*b),
        ((-1, 0, 0, 0), VREV*a*(a-1)*b),
    ]
    for k in range(2):
        dc = [0, 0]
        out.append(((-1, *dc, 0), ETA[k]*a*c[k]))
        out.append(((1, *dc, 0), ZETA[k]*c[k]))
    return out


def direct_generator(x):
    a, c1, c2, b = x
    total = Fraction(0)
    for jump, rate in channels(x):
        if rate == 0:
            continue
        y = tuple(xi + di for xi, di in zip(x, jump))
        assert min(y) >= 0, (x, jump, rate)
        total += rate * (potential(y) - potential(x))
    return total


def closed_form(x):
    a, c1, c2, b = x
    c = (c1, c2)
    S = sum(c)
    W = R**b
    d = 1 - 1/R
    G = P*(R-1)*W - Q*d*b*W + U*b
    total = (ALPHA - DELTA*a
             + sum(WEIGHT[k]*(GAMMA[k]-MU[k]*c[k]) for k in range(2))
             + sum(c[k]*(ZETA[k]-ETA[k]*a) for k in range(2))
             + a*G - VREV*a*(a-1)*b)
    if a == 0:
        f = -ALPHA/Fraction(1+S) - sum(ZETA[k]*c[k] for k in range(2))/Fraction(1+S)
        f += sum(GAMMA[k]*(Fraction(1, 2+S)-Fraction(1, 1+S)) for k in range(2))
        if S:
            f += sum(MU[k]*c[k]*(Fraction(1, S)-Fraction(1, 1+S)) for k in range(2))
        total += EPS*W*f
    elif a == 1:
        total += EPS*W*(DELTA+sum(ETA[k]*c[k] for k in range(2)))/Fraction(1+S)
    total += -K*(ALPHA+sum(GAMMA))*int(a+S == 0)
    total += K*DELTA*int(a == 1 and S == 0)
    total += K*sum(MU[k]*int(a == 0 and c[k] == 1 and c[1-k] == 0) for k in range(2))
    return total


checked = 0
for x in product(range(5), range(5), range(5), range(7)):
    assert direct_generator(x) == closed_form(x), (x, direct_generator(x), closed_form(x))
    checked += 1

# Exact inactive-face theta bound for the explicit rates on a finite grid;
# the all-S analytic lower bound theta>=1 is proved in RESULT.txt.
for c1, c2 in product(range(21), repeat=2):
    S = c1 + c2
    if S == 0:
        theta = ALPHA + sum(GAMMA)/2
    else:
        mubar = sum(MU[k]*(c1, c2)[k] for k in range(2))/S
        theta = (ALPHA + sum(ZETA[k]*(c1, c2)[k] for k in range(2))
                 + sum(GAMMA)/(S+2) - mubar)/(S+1)
    assert theta >= 1, ((c1, c2), theta)

assert ZETA[0]/ETA[0] != ZETA[1]/ETA[1]
print(f"PASS: direct reaction-list generator equals closed form on {checked} states")
print("PASS: explicit inactive-face theta>=1 on c1,c2=0,...,20 (analytic bound in RESULT.txt)")
print("PASS: toggle ratios 1 and 2 conflict, so no positive complex-balanced equilibrium")
print("Finite evidence only; global Foster inequality is proved analytically in RESULT.txt")
