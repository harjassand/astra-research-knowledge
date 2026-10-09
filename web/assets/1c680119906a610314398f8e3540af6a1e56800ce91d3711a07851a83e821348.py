#!/usr/bin/env python3
"""Finite sanity check for the discrete-concavity lemma in v2.txt.

This checks small rational rows and grid sizes; it is not a proof of the theorem.
Run with: python3 work/natural/n06_evolutionary_memory/check_grid_ascent.py
"""

from itertools import product
from math import log


def allocations(d, total, floor):
    if d == 1:
        if total >= floor:
            yield (total,)
        return
    for head in range(floor, total - floor * (d - 1) + 1):
        for tail in allocations(d - 1, total - head, floor):
            yield (head,) + tail


def score(k, p):
    return sum(pi * log(ki) for ki, pi in zip(k, p))


def has_improving_transfer(k, p, floor):
    before = score(k, p)
    for donor in range(len(k)):
        if k[donor] <= floor:
            continue
        for recipient in range(len(k)):
            if donor == recipient:
                continue
            candidate = list(k)
            candidate[donor] -= 1
            candidate[recipient] += 1
            if score(candidate, p) > before + 1e-12:
                return True
    return False


def positive_probability_vectors(d):
    for weights in product(range(1, 5), repeat=d):
        total = sum(weights)
        yield tuple(weight / total for weight in weights)


def main():
    checked = 0
    for d in (2, 3, 4):
        floor = 1
        for total in range(d * floor + 1, d * floor + 8):
            grid = tuple(allocations(d, total, floor))
            for p in positive_probability_vectors(d):
                best = max(score(k, p) for k in grid)
                for k in grid:
                    local_maximum = not has_improving_transfer(k, p, floor)
                    if local_maximum and score(k, p) < best - 1e-12:
                        raise AssertionError((d, total, p, k, best))
                    checked += 1
    print(f"PASS: checked {checked} row allocations; no suboptimal local maxima found")


if __name__ == "__main__":
    main()
