#!/usr/bin/env python3
"""Exact-Fraction generator check for a mixed-cofactor threshold ray."""
from fractions import Fraction as F
from math import prod

ALPHA = DELTA_A = ETA1 = ETA2 = ZETA1 = ZETA2 = F(1)
GAMMA1 = MU1 = F(1)
GAMMA2 = MU2 = F(2)
R = F(6, 5)
EPS = F(1)


def fall(x, r):
    if x < r:
        return 0
    return prod(range(x-r+1, x+1)) if r else 1


def q(c1, c2):
    # Toggle cofactors nu_1=(2,2), nu_2=(0,1).
    return ZETA1 * fall(c1, 2) * fall(c2, 2) + ZETA2 * fall(c2, 1)


def e(c1, c2):
    # eta_j=zeta_j=1, so E=Q in this fixture.
    return ETA1 * fall(c1, 2) * fall(c2, 2) + ETA2 * fall(c2, 1)


def drift_u(c1, c2):
    Q = q(c1, c2)
    H = F(0)
    J = F(0)
    for k, count, mu, gamma in (
        (1, c1, MU1, GAMMA1),
        (2, c2, MU2, GAMMA2),
    ):
        if count:
            cm = (c1 - 1, c2) if k == 1 else (c1, c2 - 1)
            qm = q(*cm)
            dm = Q - qm
            H += mu * count * dm / ((1 + qm) * (1 + Q))
        cp = (c1 + 1, c2) if k == 1 else (c1, c2 + 1)
        qp = q(*cp)
        dp = qp - Q
        J += gamma * dp / ((1 + Q) * (1 + qp))
    return H, J


def margins(n):
    Q = q(n, 2)
    H, J = drift_u(n, 2)
    theta = (ALPHA + Q) / (1 + Q) + J - H
    kappa = (DELTA_A + e(n, 2)) / (1 + Q) - H
    return Q, H, J, theta, kappa


def falling_propensity(source, state):
    return prod(fall(x, r) for x, r in zip(state, source))


# Exact mass-action reaction list on species (A,B,C1,C2).
REACTIONS = [
    ((0, 0, 0, 0), (1, 0, 0, 0), F(1)),   # 0 -> A
    ((1, 0, 0, 0), (0, 0, 0, 0), F(1)),   # A -> 0
    ((0, 0, 0, 0), (0, 0, 1, 0), F(1)),   # 0 -> C1
    ((0, 0, 1, 0), (0, 0, 0, 0), F(1)),   # C1 -> 0
    ((0, 0, 0, 0), (0, 0, 0, 1), F(2)),   # 0 -> C2
    ((0, 0, 0, 1), (0, 0, 0, 0), F(2)),   # C2 -> 0
    ((1, 0, 0, 0), (1, 1, 0, 0), F(1)),   # A -> A+B
    ((1, 1, 0, 0), (1, 0, 0, 0), F(1)),   # A+B -> A
    ((1, 0, 2, 2), (0, 0, 2, 2), F(1)),   # A+2C1+2C2 -> 2C1+2C2
    ((0, 0, 2, 2), (1, 0, 2, 2), F(1)),   # reverse
    ((1, 0, 0, 1), (0, 0, 0, 1), F(1)),   # A+C2 -> C2
    ((0, 0, 0, 1), (1, 0, 0, 1), F(1)),   # reverse
]


def potential(state):
    a, b, c1, c2 = state
    uu = 1 / (1 + q(c1, c2))
    return (F(1) + c1 + c2 + a * uu
            + R**b * (1 + EPS * (uu if a == 0 else 0))
            + (1 if a + c1 + c2 == 0 else 0))


def direct_generator(n):
    x = (0, n, n, 2)
    out = F(0)
    for src, dst, rate in REACTIONS:
        propensity = rate * falling_propensity(src, x)
        if not propensity:
            continue
        y = tuple(xi - si + di for xi, si, di in zip(x, src, dst))
        out += propensity * (potential(y) - potential(x))
    return out


def formula_generator(n):
    Q, H, J, theta, _ = margins(n)
    # At a=0 the B edge is disabled, the K-face is not reached, and
    # (alpha+Q)/(1+Q)=1. The weighted C drift is -n-1.
    assert (ALPHA + Q) / (1 + Q) == 1
    return -F(n) - theta * R**n

if __name__ == "__main__":
    for n in (8, 16, 32):
        Q, H, J, theta, kappa = margins(n)
        direct = direct_generator(n)
        formula = formula_generator(n)
        assert direct == formula, (n, direct, formula)
        assert theta < 0 and kappa < 0, (n, theta, kappa)
        if n >= 16:
            assert direct > 0, (n, direct)
        print(f"n={n} Q={Q} H={H} J={J} theta={theta} kappa={kappa} LV={direct}")
    print("exact rational generator identity verified for all displayed states")
