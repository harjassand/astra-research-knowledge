#!/usr/bin/env python3
"""Exact finite checks for S4's explicit witnesses and proof constants.

This script does not integrate Navier--Stokes and does not certify the PDE
energy identities.  It independently checks the algebraic packet ingredients
with fractions, including the cutoff edge that invalidated an earlier packet.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from fractions import Fraction as F
from math import factorial
from pathlib import Path


def norm2(p):
    return p[0] * p[0] + p[1] * p[1]


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def coeff(p, q):
    return cross(p, q) * (F(1, norm2(q)) - F(1, norm2(p)))


def neg(p):
    return (-p[0], -p[1])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def ceil_half(n):
    return (n + 1) // 2


def exp_upper(x: F, order=24):
    assert 0 <= x <= 1
    partial = sum((x**n / factorial(n) for n in range(order + 1)), F(0))
    nxt = x ** (order + 1) / factorial(order + 1)
    # Every subsequent term ratio is <= x/(order+2).
    return partial + nxt / (1 - x / (order + 2))


def ratio(f):
    return {"exact": str(f), "decimal": float(f)}


def check_constants():
    min_c = 320 * (F(1, 1170) - F(1, 1600))
    assert min_c > F(1, 16)
    exponent = F(16, 100000) + F(2852, 6000)
    assert exponent < F(1, 2)
    assert exp_upper(F(1, 2)) < 2
    packet_relative_bound = F(23040, 100000) * 2
    assert packet_relative_bound < F(1, 2)
    assert F(1, 48000000) > F(1, 100000000)
    assert exp_upper(F(5, 8)) < 2
    assert F(24, 32 * 3) <= F(1, 4)
    # pi <22/7 and sqrt(2)<10/7 suffice for the chosen Ladyzhenskaya 10.
    lady_upper = 1 + 2 * F(22, 7) * F(10, 7)
    assert lady_upper < 10
    # Count and |k| estimates for the difference force on D.
    assert 15 * F(1, 4) * 3 < 12
    assert F(100, 4) == 5 * 5  # global heat-error squared constant
    for K in range(1, 1025):
        sk_squared = F(2 * K * (K + 1) * (2 * K + 1) ** 2, 3)
        assert sk_squared <= 16 * K**4
        assert sk_squared <= 4 * (K + 1) ** 4
    return {
        "interaction_uniform_lower": ratio(min_c),
        "packet_exponent_upper": ratio(exponent),
        "packet_remainder_relative_bound": ratio(packet_relative_bound),
        "exp_half_rational_upper": ratio(exp_upper(F(1, 2))),
        "exp_five_eighths_rational_upper": ratio(exp_upper(F(5, 8))),
        "universal_lower_before_rounding": ratio(F(1, 48000000)),
        "ladyzhenskaya_constant_upper": ratio(lady_upper),
        "global_heat_error_constant": 5,
        "universal_minimax_upper_constant": 10,
    }


def packet(L):
    A = {(40 * L + i, j) for i in range(L + 1) for j in range(L + 1)}
    B = {(-33 * L + i, 8 * L + j) for i in range(L + 1) for j in range(L + 1)}
    I = range(ceil_half(L), (3 * L) // 2 + 1)
    Dp = {(7 * L + s, 8 * L + t) for s in I for t in I}
    return A, B, Dp


def check_packet(L):
    A, B, Dp = packet(L)
    supports = [A, B, {neg(p) for p in A}, {neg(p) for p in B}]
    flat = set().union(*supports)
    assert len(flat) == 4 * (L + 1) ** 2
    assert len(Dp) >= L * L
    assert max(norm2(k) for k in Dp) <= 225 * L * L
    counts = defaultdict(int)
    desired = defaultdict(F)
    min_c = None
    for p in A:
        for q in B:
            k = add(p, q)
            if k not in Dp:
                continue
            c = coeff(p, q)
            assert c > F(1, 16)
            assert norm2(p) + norm2(q) <= 2852 * L * L
            counts[k] += 1
            desired[k] += c
            min_c = c if min_c is None else min(min_c, c)
    assert set(counts) == Dp
    assert min(counts.values()) >= F(L * L, 4)
    # Independently form the unsymmetrized convolution for both signs.
    sign_outputs = {}
    for sign in [-1, 1]:
        omega = {p: F(1) for p in A | {neg(p) for p in A}}
        omega.update({p: F(sign) for p in B | {neg(p) for p in B}})
        outputs = defaultdict(F)
        for p, wp in omega.items():
            for q, wq in omega.items():
                k = add(p, q)
                if k in Dp:
                    outputs[k] -= F(cross(p, q), norm2(p)) * wp * wq
                    assert (p in A and q in B) or (p in B and q in A)
        assert all(outputs[k] == sign * desired[k] for k in Dp)
        sign_outputs[sign] = outputs
    assert all(sign_outputs[-1][k] == -sign_outputs[1][k] for k in Dp)
    energy_for_E1 = sum((F(64, norm2(p)) for p in flat), F(0))
    assert energy_for_E1 <= 1
    for K in range(16 * L, 16 * L + 16):
        assert all(max(abs(p[0]), abs(p[1])) > K for p in flat)
        assert all(max(abs(k[0]), abs(k[1])) <= K for k in Dp)
    return {
        "L": L,
        "K_range": [16 * L, 16 * L + 15],
        "initial_nonzero_mode_count": len(flat),
        "positive_target_count": len(Dp),
        "minimum_desired_pair_count": min(counts.values()),
        "minimum_interaction_coefficient": ratio(min_c),
        "minimum_target_vorticity_derivative_divided_by_a_squared": ratio(min(desired.values())),
        "energy_squared_for_E1_a8": ratio(energy_for_E1),
    }


def check_a5(N):
    p, q, k = (N, 0), (-N + 1, 1), (1, 1)
    S = norm2(p) + norm2(q)
    # E=1, alpha=1/3, a=N/3.
    a = F(N, 3)
    c = coeff(p, q) * a * a
    assert c == F(2 * N * (N - 1), 9 * norm2(q))
    assert c >= F(2, 9)
    energy = 2 * a * a * (F(1, norm2(p)) + F(1, norm2(q)))
    assert energy < 1
    support = {p, q, neg(p), neg(q)}
    output = defaultdict(F)
    for l in support:
        for m in support:
            j = add(l, m)
            if j != (0, 0):
                output[j] -= F(cross(l, m), norm2(l)) * a * a
    output = {j: val for j, val in output.items() if val}
    r = (p[0] - q[0], p[1] - q[1])
    assert output == {k: c, neg(k): c, r: -c, neg(r): -c}
    return {"N": N, "S": S, "c_for_E1": ratio(c), "energy_squared_for_E1": ratio(energy)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("S4_checks.json"))
    parser.add_argument("--max-L", type=int, default=8)
    args = parser.parse_args()
    data = {
        "status": "PASS",
        "scope": "exact finite Fourier algebra and global rational constants; not a PDE formal proof or numerical simulation",
        "constants": check_constants(),
        "packets": [check_packet(L) for L in range(1, args.max_L + 1)],
        "A5": [check_a5(N) for N in [3, 4, 6, 10, 32, 128, 1024]],
        "historical_failed_packet": {
            "K": 31, "L": 1, "old_B_edge": [-31, 8],
            "is_resolved": True, "corrected_B_edge": [-32, 8],
            "corrected_is_resolved": False,
        },
    }
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"status": data["status"], "packets_checked": len(data["packets"]), "output": str(args.output)}))


if __name__ == "__main__":
    main()
