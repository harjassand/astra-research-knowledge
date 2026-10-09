#!/usr/bin/env python3
"""Exact checks for recursive-composition counterexample to A <= C I.

Uses only the Python standard library and integer Walsh-Hadamard transforms.
It checks the 4-bit seed and its first composition (16 input bits). The proof
of the composition identity in the companion Markdown establishes all levels.
"""
from fractions import Fraction
from math import prod


def walsh(values):
    a = list(values)
    width = 1
    while width < len(a):
        for base in range(0, len(a), 2 * width):
            for j in range(width):
                x, y = a[base + j], a[base + j + width]
                a[base + j], a[base + j + width] = x + y, x - y
        width *= 2
    return a


def seed_h(bits):
    plus = {i + 1 for i, bit in enumerate(bits) if bit == 1}
    w = len(plus)
    return 1 if w >= 3 or (w == 2 and plus in ({1, 2}, {3, 4}, {1, 3})) else -1


def truth_table_h():
    n = 4
    return [seed_h([1 if (x >> i) & 1 else -1 for i in range(n)])
            for x in range(1 << n)]


def truth_table_composed():
    # F_1 = h(h(block 0), ..., h(block 3)) on four disjoint 4-bit blocks.
    vals = []
    for x in range(1 << 16):
        outputs = []
        for block in range(4):
            bits = [1 if (x >> (4 * block + i)) & 1 else -1
                    for i in range(4)]
            outputs.append(seed_h(bits))
        vals.append(seed_h(outputs))
    return vals


def exact_metrics(values):
    n = (len(values)).bit_length() - 1
    w = walsh(values)  # normalized coefficient is w[mask] / 2**n
    den = 1 << n
    assert sum(x * x for x in w) == den * den
    A_num = 0
    for i in range(n):
        bit = 1 << i
        for mask in range(1 << n):
            if not (mask & bit):
                A_num += abs(w[mask] * w[mask | bit])
    I_num = sum(mask.bit_count() * w[mask] * w[mask]
                for mask in range(1 << n))
    L1_num = sum(abs(w[1 << i]) for i in range(n))
    denom2 = den * den
    return {
        "n": n,
        "balanced": sum(values) == 0,
        "A": Fraction(A_num, denom2),
        "I": Fraction(I_num, denom2),
        "L1": Fraction(L1_num, den),
        "ratio": Fraction(A_num, I_num),
    }


def coordinate_metrics(values):
    """Return exact (A_i, I_i, A_i/I_i) triples in coordinate order."""
    n = len(values).bit_length() - 1
    den = 1 << n
    w = walsh(values)
    result = []
    for i in range(n):
        bit = 1 << i
        A_num = sum(abs(w[mask] * w[mask | bit])
                    for mask in range(1 << n) if not mask & bit)
        I_num = sum(w[mask] * w[mask]
                    for mask in range(1 << n) if mask & bit)
        result.append((Fraction(A_num, den * den),
                       Fraction(I_num, den * den),
                       Fraction(A_num, I_num)))
    return result


def main():
    seed = exact_metrics(truth_table_h())
    composed = exact_metrics(truth_table_composed())
    assert seed == {
        "n": 4,
        "balanced": True,
        "A": Fraction(1),
        "I": Fraction(3, 2),
        "L1": Fraction(3, 2),
        "ratio": Fraction(2, 3),
    }, seed
    assert composed["balanced"]
    assert composed["A"] == Fraction(3), composed
    assert composed["I"] == Fraction(9, 4), composed
    assert composed["L1"] == Fraction(9, 4), composed
    assert composed["ratio"] == Fraction(4, 3), composed
    seed_coordinates = coordinate_metrics(truth_table_h())
    composed_coordinates = coordinate_metrics(truth_table_composed())
    assert [x[2] for x in seed_coordinates] == [
        Fraction(1, 2), Fraction(1), Fraction(1, 2), Fraction(1)
    ], seed_coordinates
    assert [x[2] for x in composed_coordinates] == [
        Fraction(1), Fraction(3, 2), Fraction(1), Fraction(3, 2),
        Fraction(3, 2), Fraction(2), Fraction(3, 2), Fraction(2),
        Fraction(1), Fraction(3, 2), Fraction(1), Fraction(3, 2),
        Fraction(3, 2), Fraction(2), Fraction(3, 2), Fraction(2),
    ], composed_coordinates
    print("seed:", seed)
    print("first composition:", composed)
    print("verified exact recurrence: A_1=3, I_1=9/4, A_1/I_1=4/3")
    print("seed local ratios:", [x[2] for x in seed_coordinates])
    print("first-composition local ratios:",
          [x[2] for x in composed_coordinates])


if __name__ == "__main__":
    main()
