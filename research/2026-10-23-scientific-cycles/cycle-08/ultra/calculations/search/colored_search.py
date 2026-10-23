#!/usr/bin/env python3
"""Exact-integer search receiver. No shared random rows or quantum oracle.

The caller supplies the actual local parity instrument through raw_query(j,
    color), returning whether Alice's and Bob's mod-D parity outcomes agree. Each
color is used once. PROOF.txt states the physical implementation and bounds.
The fixture at the bottom is a classical admission of the search control only.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from fractions import Fraction
import argparse
import json
import random
import time


def ceil_log_ratio(base: int, numerator: int, denominator: int = 1) -> int:
    if base < 2 or numerator < 1 or denominator < 1:
        raise ValueError("positive rational and integer base >=2 required")
    exponent, power = 0, denominator
    while power < numerator:
        power *= base
        exponent += 1
    return exponent


@dataclass
class _Node:
    lo: int
    hi: int
    total: int
    lazy: int = 1
    left: "_Node | None" = None
    right: "_Node | None" = None

    def multiply(self, factor: int) -> None:
        self.total *= factor
        self.lazy *= factor

    def push(self) -> None:
        if self.hi - self.lo == 1:
            return
        if self.left is None:
            # A never-split node has uniform weight; include its lazy factor
            # through total, then reset lazy after constructing both children.
            unit, remainder = divmod(self.total, self.hi - self.lo)
            assert remainder == 0
            mid = (self.lo + self.hi) // 2
            self.left = _Node(self.lo, mid, (mid - self.lo) * unit)
            self.right = _Node(mid, self.hi, (self.hi - mid) * unit)
        elif self.lazy != 1:
            self.left.multiply(self.lazy)
            self.right.multiply(self.lazy)
        self.lazy = 1


class IntegerWeights:
    """Implicit lazy interval tree: O(log n) exact operations per MW step."""

    def __init__(self, n: int):
        self.n = n
        self.root = _Node(0, n, n)

    def _multiply(self, node: _Node, lo: int, hi: int, factor: int) -> None:
        if hi <= node.lo or node.hi <= lo:
            return
        if lo <= node.lo and node.hi <= hi:
            node.multiply(factor)
            return
        node.push()
        self._multiply(node.left, lo, hi, factor)
        self._multiply(node.right, lo, hi, factor)
        node.total = node.left.total + node.right.total

    def multiply(self, lo: int, hi: int, factor: int) -> None:
        if lo < hi:
            self._multiply(self.root, lo, hi, factor)

    def _set(self, node: _Node, index: int, value: int) -> None:
        if node.hi - node.lo == 1:
            node.total, node.lazy = value, 1
            return
        node.push()
        child = node.left if index < node.left.hi else node.right
        self._set(child, index, value)
        node.total = node.left.total + node.right.total

    def set(self, index: int, value: int) -> None:
        if value <= 0:
            raise ValueError("weights stay positive")
        self._set(self.root, index, value)

    def median(self) -> tuple[int, int, int]:
        """Return median atom h, its weight, cumulative weight before it."""
        node, target_twice, cumulative = self.root, self.root.total, 0
        while node.hi - node.lo > 1:
            node.push()
            if 2 * node.left.total >= target_twice:
                node = node.left
            else:
                target_twice -= 2 * node.left.total
                cumulative += node.left.total
                node = node.right
        return node.lo, node.total, cumulative

    def update(self, h: int, weight: int, cumulative: int, yes: bool) -> None:
        old_total = self.root.total
        if yes:
            self.multiply(0, h, 2)
            self.multiply(h + 1, self.n, 4)
            middle = 4 * weight - (old_total - 2 * cumulative)
        else:
            self.multiply(0, h, 4)
            self.multiply(h + 1, self.n, 2)
            middle = 4 * weight - (2 * (cumulative + weight) - old_total)
        self.set(h, middle)
        if self.root.total != 3 * old_total:
            raise AssertionError("fractional-median contraction failed")


@dataclass
class SearchResult:
    L: int
    D: int
    epsilon: str
    T: int
    s: int
    Q: int
    raw_calls: int
    candidates: list[int]
    U: int
    cut: int
    queried: list[int]
    raw_transcript: list[tuple[int, int, bool]]


def colored_search(L: int, D: int, epsilon: Fraction, raw_query) -> SearchResult:
    """Receiver control using only a public algorithm and fresh color parities.

    raw_query(j, color) must implement equality of local mod-D sums over positions
    2<=i<=j with color 1+((i-2) mod Q). Caller may compute Q via parameters().
    The search never receives K or a hidden memory register.
    """
    T, s, Q = parameters(L, D, epsilon)
    weights = IntegerWeights(L + 1)
    U, raw_count = L, 0
    raw_transcript, queried = [], []

    def raw(j: int) -> bool:
        nonlocal U, raw_count
        raw_count += 1
        if raw_count > Q:
            raise AssertionError("fresh-color budget exceeded")
        if j <= 0:
            yes = True
        elif j >= L + 1:
            yes = False
        else:
            yes = bool(raw_query(j, raw_count))
        raw_transcript.append((j, raw_count, yes))
        if not yes:
            U = min(U, j - 1)
        return yes

    for _ in range(T):
        total = weights.root.total
        h, weight, cumulative = weights.median()
        j = h if total - 2 * cumulative <= weight else h + 1
        queried.append(j)
        answers = [raw(j) for _ in range(4)]
        weights.update(h, weight, cumulative, all(answers))

    ordered = sorted(queried)
    ranks = [min(T - 1, (ell * T) // 8) for ell in range(9)]
    candidates = sorted({ordered[rank] for rank in ranks})
    for j in candidates:
        threshold = min(L + 1, j + Q + 1)
        for _ in range(s):
            raw(threshold)

    return SearchResult(L, D, str(epsilon), T, s, Q, raw_count, candidates,
                        U, max(1, U - 2 * Q), queried, raw_transcript)


def parameters(L: int, D: int, epsilon: Fraction) -> tuple[int, int, int]:
    if L < 1 or D < 2 or not 0 < epsilon < 1:
        raise ValueError("L>=1, D>=2, 0<epsilon<1 required")
    log_n = ceil_log_ratio(2, L + 1)
    log_error = ceil_log_ratio(2, 2 * epsilon.denominator, epsilon.numerator)
    T = 32 * log_n + 128 * log_error
    s = ceil_log_ratio(D, 2 * epsilon.denominator, epsilon.numerator)
    return T, s, 4 * T + 9 * s


class DifferenceFixture:
    """Classical simulation of commuting difference labels for any D>=2.

    This is fixture generation from the modeled mixed tail, not the receiver's
    access to K, and not additional shared random seed inside the operation.
    Each tail coordinate is generated only if its unique-color query uses it.
    """

    def __init__(self, L: int, K: int, D: int, Q: int, seed: int):
        if not 1 <= K <= L or D < 2 or Q < 1:
            raise ValueError("valid queue, dimension and color budget required")
        self.L, self.K, self.D, self.Q = L, K, D, Q
        self.random = random.Random(seed)
        self.touched = 0
        self.colors = set()

    def __call__(self, threshold: int, color: int) -> bool:
        if color in self.colors:
            raise AssertionError("reused color")
        self.colors.add(color)
        difference = 0
        for index in range(color + 1, threshold + 1, self.Q):
            self.touched += 1
            if index > self.K:
                difference = (difference + self.random.randrange(self.D)) % self.D
        return difference == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=1048576)
    parser.add_argument("--K", type=int, default=524288)
    parser.add_argument("--D", type=int, default=2)
    parser.add_argument("--epsilon", default="1/64")
    parser.add_argument("--seed", type=int, default=20261022)
    args = parser.parse_args()
    eps = Fraction(args.epsilon)
    T, s, Q = parameters(args.L, args.D, eps)
    fixture = DifferenceFixture(args.L, args.K, args.D, Q, args.seed)
    wall, cpu = time.perf_counter(), time.process_time()
    result = colored_search(args.L, args.D, eps, fixture)
    elapsed, process = time.perf_counter() - wall, time.process_time() - cpu
    output = asdict(result)
    output.pop("queried")
    output.pop("raw_transcript")
    output.update({"K_fixture_only": args.K, "safe_on_this_fixture": result.cut <= args.K,
                   "every_branch_bound": result.cut >= args.K - 2 * Q,
                   "difference_coordinates_touched": fixture.touched,
                   "wall_seconds": elapsed, "cpu_seconds": process,
                   "scope": "classical search-control admission, not a statistical proof"})
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
