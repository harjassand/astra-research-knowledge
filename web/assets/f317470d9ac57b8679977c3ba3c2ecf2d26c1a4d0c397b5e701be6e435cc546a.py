"""Exact finite diagnostics for several broad-cone rate choices.

These do not establish the theorem; report.md gives all-state proofs.
"""

from fractions import Fraction as Q
from math import ceil


def H(b):
    return Q(3, 2) * ((b + 1) // 2) + (Q(1, 2) if b == 1 else 0)


def F(b):
    return 0 if b == 0 else (5 if b == 1 else 2**b)


fixtures = [
    (Q(1), Q(1), Q(1), Q(4), Q(1)),
    (Q(7), Q(1000), Q(1), Q(2), Q(3, 2)),
    (Q(1, 1000), Q(10**6), Q(100), Q(151), Q(150)),
]
for k0, k1, k2, k3, k4 in fixtures:
    d = k3 + k4
    s = d / k2
    q = k4 / d
    assert s > 3 and q < Q(1, 2)
    r = min(Q(1), 2 * s / 3 - 2)
    A = max(3, 2 + ceil(k1 / (k2 * r)))
    rho = k1 / (k2 * (A - 2))
    assert rho <= r
    for b in range(1, 1001):
        birth = Q(b) + rho
        death = s * b * (b - 1)
        reward_drift = birth * (H(b + 1) - H(b))
        f_next = birth * F(b + 1)
        if b >= 2:
            reward_drift += death * (H(b - 2) - H(b) + 1)
            f_next += death * F(b - 2)
        assert reward_drift <= 0, (fixtures, b)
        assert f_next / (birth + death) <= Q(7, 8) * F(b), (fixtures, b)
    # A conservative exact-rational alternative to the report's root bound.
    M = max(2, ceil(1 + 3*(k2+k1)/d))
    for b in range(M + 1, M + 1001):
        birth = k2*b + k1
        death = d*b*(b-1)
        assert death >= 3*birth, (M,b)
        p = birth/(birth+death)
        assert 2*p-1 <= -Q(1, 2), (M,b)
    print('PASS fixture', tuple(str(v) for v in (k0,k1,k2,k3,k4)), 'A_*=',A,'M=',M)
print('All exact local checks passed; report.md gives the general proof.')
