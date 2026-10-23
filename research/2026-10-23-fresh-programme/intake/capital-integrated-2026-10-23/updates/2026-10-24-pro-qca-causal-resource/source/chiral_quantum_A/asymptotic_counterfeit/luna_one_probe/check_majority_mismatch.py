#!/usr/bin/env python3
"""Exact Fraction enumeration for the proved one-period local mismatch law."""

from fractions import Fraction
from itertools import product
from math import comb


def majority(bits):
    return int(sum(bits) > len(bits) // 2)


def encode(bits):
    syndrome = tuple(bits[j] ^ bits[j + 1] for j in range(len(bits) - 1))
    return majority(bits), syndrome


def decode(q, syndrome):
    base = [0]
    for bit in syndrome:
        base.append(base[-1] ^ bit)
    if majority(base) == q:
        return tuple(base)
    return tuple(1 - bit for bit in base)


def binomial_tail(n, threshold, p):
    return sum(
        Fraction(comb(n, k)) * p**k * (1 - p) ** (n - k)
        for k in range(threshold, n + 1)
    )


def audit(length):
    assert length in (3, 5) and length % 2 == 1
    p = Fraction(1, 3)
    eps = binomial_tail(length, length // 2 + 1, p)
    m = length // 2
    r1 = binomial_tail(length - 1, m, p)
    r0 = binomial_tail(length - 1, m + 1, p)
    assert eps == p * r1 + (1 - p) * r0

    joint = {0: [Fraction(0) for _ in range(length)],
             1: [Fraction(0) for _ in range(length)]}
    total_mismatch = [Fraction(0) for _ in range(length)]

    words = list(product((0, 1), repeat=length))
    for x in words:
        qx, sx = encode(x)
        wx = sum(x)
        for incoming in words:
            qin, _ = encode(incoming)
            wi = sum(incoming)
            weight = p ** (wx + wi) * (1 - p) ** (2 * length - wx - wi)
            y = decode(qin, sx)
            expected = x if qx == qin else tuple(1 - bit for bit in x)
            assert y == expected
            for j, bit in enumerate(x):
                mismatch = y[j] != bit
                if mismatch:
                    total_mismatch[j] += weight
                    joint[bit][j] += weight

    for j in range(length):
        assert total_mismatch[j] == 2 * eps * (1 - eps)
        for bit, r in ((0, r0), (1, r1)):
            prior = 1 - p if bit == 0 else p
            conditional = eps + (1 - 2 * eps) * r
            assert joint[bit][j] == prior * conditional


if __name__ == "__main__":
    audit(3)
    audit(5)
    print("exact mismatch and label-conditioned checks pass for L=3,5 at p=1/3")
