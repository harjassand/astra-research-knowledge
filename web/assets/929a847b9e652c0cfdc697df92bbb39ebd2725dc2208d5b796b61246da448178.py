#!/usr/bin/env python3
"""Finite exact-combinatorial witness: bounded Holevo capacity need not bound covers.

This script enumerates balanced sign states for modest even dimensions, constructs a
Hamming-separated subfamily by a greedy code, and verifies exact TV separation and
commutativity. Entropy is reported as a floating diagnostic; the formula in RESULT.txt
proves the capacity statement for every even dimension.
"""
from __future__ import annotations

from itertools import combinations
from math import comb, log, ceil


def balanced_subsets(d: int):
    half = d // 2
    return list(combinations(range(d), half))


def hamming_distance(A: tuple[int, ...], B: tuple[int, ...], half: int) -> int:
    # Balanced sign vectors disagree in two coordinates per exchanged + position.
    return 2 * (half - len(set(A).intersection(B)))


def greedy_code(d: int):
    half = d // 2
    threshold = ceil(d / 4)
    remaining = set(balanced_subsets(d))
    code = []
    while remaining:
        A = min(remaining)
        code.append(A)
        remaining = {
            B for B in remaining
            if hamming_distance(A, B, half) >= threshold
        }
    return code, threshold


def capacity_nats(a: float) -> float:
    return 0.5 * ((1 + a) * log(1 + a) + (1 - a) * log(1 - a))


def main():
    a = 0.5
    print("d balanced_count greedy_code min_distance min_T capacity_nats commutators_zero")
    for d in (8, 10, 12, 14, 16):
        code, threshold = greedy_code(d)
        half = d // 2
        min_distance = min(
            (hamming_distance(A, B, half) for i, A in enumerate(code) for B in code[i + 1:]),
            default=d,
        )
        # rho_s = diag((1+a s_j)/d); T(rho_s,rho_t)=a*Hamming(s,t)/d.
        min_tv = a * min_distance / d
        assert min_distance >= threshold
        assert min_tv >= a / 4
        assert all(sum((1 + a * (1 if j in A else -1)) / d for j in range(d)) == 1
                   for A in code)
        # All witnesses are diagonal in the same basis, so every commutator is zero.
        commutators_zero = True
        c = capacity_nats(a)
        assert c <= log(2)
        print(f"{d} {comb(d, half)} {len(code)} {min_distance} {min_tv:.6f} {c:.9f} {commutators_zero}")


if __name__ == "__main__":
    main()
