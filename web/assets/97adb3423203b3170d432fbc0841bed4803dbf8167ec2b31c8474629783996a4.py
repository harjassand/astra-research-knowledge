#!/usr/bin/env python3
"""Finite arithmetic check for the A20 deadline-pair diagnostic theorem.

This checks only the stated independent-bit model. It is not evidence for a
general online scheduling or dynamic-bin-packing theorem.
"""

from fractions import Fraction
from itertools import product


def exact_expected_cost(k: int, q: int, fee: Fraction, move: Fraction,
                        error: Fraction) -> Fraction:
    """Enumerate b uniform and q queried forecast-noise bits iid Ber(error)."""
    total = Fraction(0)
    for actual in product((0, 1), repeat=k):
        for noise in product((0, 1), repeat=q):
            probability = Fraction(1, 2**k)
            for bit in noise:
                probability *= error if bit else 1 - error
            conflicts = 0
            for i, b_i in enumerate(actual):
                if i < q:
                    prediction = b_i ^ noise[i]
                    assigned_machine = 1 - prediction
                else:
                    assigned_machine = 0
                conflicts += assigned_machine == b_i
            total += probability * (Fraction(k) + fee * q + move * conflicts)
    return total


def formula(k: int, q: int, fee: Fraction, move: Fraction,
            error: Fraction) -> Fraction:
    return (Fraction(k) + fee * q + move *
            (error * q + Fraction(k - q, 2)))


def main() -> None:
    fee = Fraction(1, 5)
    move = Fraction(2)
    error = Fraction(1, 10)
    for k in range(1, 7):
        for q in range(k + 1):
            observed = exact_expected_cost(k, q, fee, move, error)
            predicted = formula(k, q, fee, move, error)
            assert observed == predicted, (k, q, observed, predicted)
    print("exact enumeration agrees with formula for 1 <= k <= 6 and 0 <= q <= k")
    print("example: k=4, fee=1/5, migration delay=2, error=1/10")
    for q in (0, 2, 4):
        cost = formula(4, q, fee, move, error)
        print(f"queries={q}: expected_cost={cost} ratio={cost / 4}")


if __name__ == "__main__":
    main()
