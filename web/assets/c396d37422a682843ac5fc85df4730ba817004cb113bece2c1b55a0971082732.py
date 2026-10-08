"""Finite exact-rational diagnostics; the report provides all-b proofs."""

from fractions import Fraction as Q
from math import ceil, exp, log, sqrt


def H(b):
    return Q(3, 2) * ((b + 1) // 2) + (Q(1, 2) if b == 1 else 0)


def F(b):
    return 0 if b == 0 else (5 if b == 1 else 2**b)


gamma = Q(29, 35)
mu = Q(3, 5)
for b in range(1, 1001):
    birth = Q(b + 1)  # largest permissible rho=1
    death = Q(5 * b * (b - 1))
    h_reward_drift = birth * (H(b + 1) - H(b))
    if b >= 2:
        h_reward_drift += death * (H(b - 2) - H(b) + 1)
    assert h_reward_drift <= 0, (b, h_reward_drift)
    f_next = birth * F(b + 1)
    if b >= 2:
        f_next += death * F(b - 2)
    assert f_next / (birth + death) <= Q(4, 5) * F(b), b

assert Q(1, 7) + Q(6, 7) * Q(4, 5) == gamma
eta = -log(float(gamma)) / 4
r = sqrt(float(gamma))
K = 4 / r * (1 + float(Q(5, 4) / gamma) * ((1 + r) / (1 - r)**3 - 1))
theta = min(eta, float(mu) / K)
print("PASS: 1000 exact-rational H and F checks; all-b proof is in report.md.")
print(f"gamma={gamma}, mu={mu}")
print(f"Approximate constants only: eta={eta:.10g}, K={K:.10g}, theta={theta:.10g}")
print(f"Approximate explicit positive probability lower bound={(1-exp(-2*theta))/3:.10g}")
