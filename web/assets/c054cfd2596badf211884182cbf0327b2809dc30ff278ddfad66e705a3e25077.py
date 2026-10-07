"""Exhaustive small check of the truncated exact rational coin."""

from fractions import Fraction
from itertools import product
import json
import math


def check_coin(a, b, m):
    bits = math.ceil(math.log2(b))
    size = 1 << bits
    accepted = 0
    aborted = 0
    total = size ** m
    for draws in product(range(size), repeat=m):
        result = None
        for x in draws:
            if x < b:
                result = x < a
                break
        if result is None:
            aborted += 1
        elif result:
            accepted += 1
    accept_prob = Fraction(accepted, total)
    abort_prob = Fraction(aborted, total)
    expected_accept = (1 - abort_prob) * Fraction(a, b)
    assert accept_prob == expected_accept
    assert abort_prob == Fraction(size - b, size) ** m
    assert abort_prob < Fraction(1, 1 << m)
    return accept_prob, abort_prob


def main():
    checked = 0
    max_draw_depth = 0
    for b in range(2, 9):
        for a in range(1, b):
            for m in range(1, 4):
                _, abort = check_coin(a, b, m)
                checked += 1
                max_draw_depth = max(max_draw_depth, (1 << math.ceil(math.log2(b))) ** m)
    print(json.dumps({
        "exact_exhaustive_cases": checked,
        "largest_random_tape_leaf_count": max_draw_depth,
        "verified": "acceptance=(1-abort)*a/b; abort=((2^B-b)/2^B)^m < 2^-m",
        "scope": "tiny rational-coin diagnostic only",
    }, indent=2))


if __name__ == "__main__":
    main()
