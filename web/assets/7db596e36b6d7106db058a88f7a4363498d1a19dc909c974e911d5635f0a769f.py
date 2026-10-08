#!/usr/bin/env python3
"""Exact finite diagnostic for the nontrivial sparse rate-box constants.

The analytic all-state argument is in REPORT.txt. This script recomputes its
rational constants and checks the robust generator upper bound on a finite
box only; the grid is not used as a proof of the theorem.
"""

from fractions import Fraction as F
from itertools import product


R = F(6, 5)
E = ((0, 0), (1, 0), (1, 1))  # A1-B1, A2-B1, A2-B2
KVAL = F(7, 3)
ALPHA = (F(9, 10), F(11, 10))
DELTA = (F(9, 10), F(11, 10))
P = (F(9, 10), F(11, 10))
Q = (F(19, 10), F(21, 10))
U = (F(9, 10), F(11, 10))
VV = (F(19, 10), F(21, 10))


def qtext(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def falling(n, k):
    out = 1
    for z in range(k):
        out *= n - z
    return max(0, out)


def V(a, b):
    A = sum(a)
    value = F(A) + sum((R ** b[i]) * (1 + int(sum(a[j] for j, ii in E if ii == i) == 0)) for i in range(2))
    if A == 0:
        value += KVAL
    return value


def endpoint_term(rate_interval, prop, jump):
    coef = F(prop) * jump
    rate = rate_interval[1] if coef >= 0 else rate_interval[0]
    return rate * coef


def lv_sup(a, b):
    out = F(0)
    for j in range(2):
        aa = list(a); aa[j] += 1
        out += endpoint_term(ALPHA, 1, V(tuple(aa), b) - V(a, b))
        if a[j]:
            aa = list(a); aa[j] -= 1
            out += endpoint_term(DELTA, a[j], V(tuple(aa), b) - V(a, b))
    for j, i in E:
        if a[j]:
            bb = list(b); bb[i] += 1
            out += endpoint_term(P, a[j], V(a, tuple(bb)) - V(a, b))
        if a[j] and b[i]:
            bb = list(b); bb[i] -= 1
            out += endpoint_term(Q, a[j] * b[i], V(a, tuple(bb)) - V(a, b))
            aa = list(a); aa[j] += 1
            out += endpoint_term(U, a[j] * b[i], V(tuple(aa), b) - V(a, b))
            if a[j] >= 2:
                aa = list(a); aa[j] -= 1
                out += endpoint_term(VV, falling(a[j], 2) * b[i], V(tuple(aa), b) - V(a, b))
    return out


def main():
    c, d = R - 1, 1 - 1 / R
    delta_lo, delta_hi = DELTA
    p_lo, p_hi = P
    q_lo, q_hi = Q
    u_lo, u_hi = U
    v_lo, v_hi = VV
    deg_A = (1, 2)
    chi = (delta_lo - p_hi * c, delta_lo - 2 * p_hi * c)
    cj = tuple(x / 2 for x in chi)

    M = 1
    while not (R**M >= 2 * u_hi / (q_lo * d)
               and q_lo * d * M / 2 >= p_hi * c + delta_hi + 1):
        M += 1
    assert M == 15
    gamma = [p_hi * c * R**m - q_lo * d * m * R**m + u_hi * m for m in range(M)]
    gmax = max(gamma)
    assert gmax == F(34838, 15625)
    Gj = (gmax, 2 * gmax)
    Nj = []
    for j in range(2):
        n = 2
        while v_lo * (n - 1) < Gj[j] + cj[j]:
            n += 1
        Nj.append(n)
    assert Nj == [3, 4]
    Cj = tuple((Gj[j] + cj[j]) * Nj[j] for j in range(2))
    alpha_sum_lo = 2 * ALPHA[0]
    Hhi = 2 * ALPHA[1]
    Kcalc = max(F(1), (Hhi + 2) / alpha_sum_lo)
    assert Kcalc == KVAL
    switch_const = 3 * delta_hi * R ** (M - 1)
    C0 = Hhi + KVAL * delta_hi + sum(Cj) + switch_const
    zeta = (F(1), F(9, 10))
    cA = min(cj)
    beta = min(cA, min(zeta) / 2)
    D = 2 * R ** (M - 1)
    Cgeo = C0 + beta * (2 * D + KVAL)
    Tstar = max(F(1), 2 * Cgeo / beta, (Cgeo + 1) / beta)
    assert beta == F(23, 100)
    assert M == 15 and q_lo * d == F(19, 60)

    checked = 0
    for a1, a2, b1, b2 in product(range(6), range(6), range(17), range(17)):
        a, b = (a1, a2), (b1, b2)
        support_bound = C0 - cj[0] * a1 - cj[1] * a2
        support_bound -= zeta[0] * R**b1 * int(b1 >= M)
        support_bound -= zeta[1] * R**b2 * int(b2 >= M)
        if lv_sup(a, b) > support_bound:
            raise AssertionError((a, b, lv_sup(a, b), support_bound))
        checked += 1
    print("rate box: alpha,delta,p,u in [9/10,11/10]; q,v in [19/10,21/10]")
    print("R=6/5; chi=(17/25,23/50); c=(17/50,23/100)")
    print(f"M_i={M}; Gamma_max={qtext(gmax)}; N_j={Nj}; C_j={[qtext(x) for x in Cj]}")
    print(f"K={qtext(KVAL)}; C0={qtext(C0)}; beta={qtext(beta)}; Cgeo={qtext(Cgeo)}")
    print(f"F threshold T*={qtext(Tstar)}; physical-time exponential rate beta/2={qtext(beta/2)}")
    print(f"checked robust generator bound at {checked} states with exact Fractions")


if __name__ == "__main__":
    main()
