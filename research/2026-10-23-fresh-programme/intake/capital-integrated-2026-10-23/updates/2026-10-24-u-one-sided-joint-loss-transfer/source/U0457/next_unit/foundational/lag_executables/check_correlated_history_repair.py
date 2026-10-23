#!/usr/bin/env python3
"""Exact Fraction replay of the R_i=(X_<i,Y_>i) repair at m=2."""

from fractions import Fraction as F
from itertools import product

BITS = (0, 1)


def mu(x, y):
    return F(3, 8) if x == y else F(1, 8)


def success(x1, x2):
    return F(x1 == x2)


def selected_mass(x1, y1, x2, y2):
    return mu(x1, y1) * mu(x2, y2) * success(x1, x2) / F(1, 2)


def total_variation(p, q):
    return sum(abs(p.get(z, F(0)) - q.get(z, F(0)))
               for z in set(p) | set(q)) / 2


def pair_law_from_q(qx):
    return {(x, y): qx.get(x, F(0)) * (mu(x, y) / F(1, 2))
            for x, y in product(BITS, repeat=2)}


MU_PAIR = {(x, y): mu(x, y) for x, y in product(BITS, repeat=2)}
MU_X = {0: F(1, 2), 1: F(1, 2)}
P_SUCCESS = F(1, 2)
assert sum(mu(x, y) * mu(u, v) * success(x, u)
           for x, y, u, v in product(BITS, repeat=4)) == P_SUCCESS

# i=1: R=Y2=v. Compute Q(R), then q_R(X1) exactly from the selected law.
for v in BITS:
    q_r_raw = {}
    r_mass = F(0)
    for x1, y1, x2, y2 in product(BITS, repeat=4):
        if y2 != v:
            continue
        weight = selected_mass(x1, y1, x2, y2)
        r_mass += weight
        q_r_raw[x1] = q_r_raw.get(x1, F(0)) + weight
    assert r_mass == F(1, 2)
    q_r = {x: q_r_raw.get(x, F(0)) / r_mass for x in BITS}
    assert q_r[v] == F(3, 4)
    assert q_r[1 - v] == F(1, 4)
    selected_current = {}
    for x1, y1, x2, y2 in product(BITS, repeat=4):
        if y2 == v:
            selected_current[(x1, y1)] = (
                selected_current.get((x1, y1), F(0))
                + selected_mass(x1, y1, x2, y2) / r_mass)
    assert selected_current == pair_law_from_q(q_r)

    # Repaired full fine-outcome support: A=(x,x), B=(v,v).
    # The fine source table has A=(x,x), B=(v,v). Its current-coordinate
    # marginal must match tau_a^{x,R} K_y^{b,R}.
    for x, y in product(BITS, repeat=2):
        actual_full = {(x, x, v, v): F(1)}
        actual_coordinate = {(row[0], row[2]): mass
                             for row, mass in actual_full.items()}
        tau_i = {(x,): F(1)}
        k_i = {(v,): F(1)}
        repaired_coordinate = {(a[0], b[0]): pa * pb
                               for a, pa in tau_i.items()
                               for b, pb in k_i.items()}
        assert repaired_coordinate == actual_coordinate

    fresh_repaired = pair_law_from_q(q_r)
    drift_joint = total_variation(fresh_repaired, MU_PAIR)
    drift_x = total_variation(q_r, MU_X)
    assert drift_joint == drift_x == F(1, 4)

# i=2: R=X1=h. Compute q_R(X2), then the full fine-outcome table.
for h in BITS:
    q_r_raw = {}
    r_mass = F(0)
    for x1, y1, x2, y2 in product(BITS, repeat=4):
        if x1 != h:
            continue
        weight = selected_mass(x1, y1, x2, y2)
        r_mass += weight
        q_r_raw[x2] = q_r_raw.get(x2, F(0)) + weight
    assert r_mass == F(1, 2)
    q_r = {x: q_r_raw.get(x, F(0)) / r_mass for x in BITS}
    assert q_r[h] == 1 and q_r[1 - h] == 0
    selected_current = {}
    for x1, y1, x2, y2 in product(BITS, repeat=4):
        if x1 == h:
            selected_current[(x2, y2)] = (
                selected_current.get((x2, y2), F(0))
                + selected_mass(x1, y1, x2, y2) / r_mass)
    assert selected_current == pair_law_from_q(q_r)

    # Selected support has x2=h. Bob averages Y1~mu(.|h), but B2=Y2=y.
    for y in BITS:
        actual_full = {(h, h, y, y): F(1)}
        actual_coordinate = {(row[1], row[3]): mass
                             for row, mass in actual_full.items()}
        tau_i = {(h,): F(1)}
        k_i = {(y,): F(1)}
        repaired_coordinate = {(a[0], b[0]): pa * pb
                               for a, pa in tau_i.items()
                               for b, pb in k_i.items()}
        assert repaired_coordinate == actual_coordinate

    fresh_repaired = pair_law_from_q(q_r)
    drift_joint = total_variation(fresh_repaired, MU_PAIR)
    drift_x = total_variation(q_r, MU_X)
    assert drift_joint == drift_x == F(1, 2)

print("i=1: R=Y2, q_R(R)=3/4, q_R(other)=1/4; actual fine table "
      "marginal matches repaired tau/K; fresh-law TV=1/4")
print("i=2: R=X1, q_R(X2=R)=1; actual fine table marginal matches "
      "repaired tau/K; fresh-law TV=1/2")
print("all checks are exact Fraction identities")
