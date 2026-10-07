#!/usr/bin/env python3
"""Acquired exact conditional sampler for block+fixed-rank F; small checks only.

Derived from the fully audited c02_l05 signed tag transfer.  This file owns all
outputs.  No peer file is imported or modified.  Fraction arithmetic and exact
Gaussian rationals retain interference through the final completion mass.
"""
from fractions import Fraction
from itertools import combinations, product
from math import lcm
from pathlib import Path
from random import Random
from time import perf_counter
import json


class QI:
    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re, self.im = Fraction(re), Fraction(im)

    def __add__(self, other):
        other = qi(other)
        return QI(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return QI(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-qi(other))

    def __rsub__(self, other):
        return qi(other) - self

    def __mul__(self, other):
        other = qi(other)
        return QI(self.re * other.re - self.im * other.im,
                  self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = qi(other)
        return self * other.conj() * (1 / other.norm2())

    def __bool__(self):
        return bool(self.re or self.im)

    def __eq__(self, other):
        other = qi(other)
        return self.re == other.re and self.im == other.im

    def conj(self):
        return QI(self.re, -self.im)

    def norm2(self):
        return self.re ** 2 + self.im ** 2


def qi(x):
    return x if isinstance(x, QI) else QI(x)


def det(matrix):
    """O(d^3) exact elimination; no factorial permutation enumeration."""
    d = len(matrix)
    if d == 0:
        return QI(1)
    a = [[qi(x) for x in row] for row in matrix]
    assert all(len(row) == d for row in a)
    ans = QI(1)
    for j in range(d):
        pivot = next((i for i in range(j, d) if a[i][j]), None)
        if pivot is None:
            return QI(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            ans = -ans
        value = a[j][j]
        ans = ans * value
        for i in range(j + 1, d):
            if a[i][j]:
                factor = a[i][j] / value
                for k in range(j + 1, d):
                    a[i][k] = a[i][k] - factor * a[j][k]
                a[i][j] = QI(0)
    return ans


def sub(matrix, rows, columns):
    return [[matrix[i][j] for j in columns] for i in rows]


def weighted_index(weights, rng):
    """Exact rational draw; expected fewer than two power-of-two trials."""
    assert all(w >= 0 for w in weights)
    common = lcm(*(w.denominator for w in weights))
    ints = [w.numerator * (common // w.denominator) for w in weights]
    total = sum(ints)
    if total == 0:
        raise ValueError("empty conditional sector")
    bits = total.bit_length()
    while True:
        value = rng.getrandbits(bits)
        if value < total:
            break
    for i, weight in enumerate(ints):
        if value < weight:
            return i
        value -= weight
    raise AssertionError("unreachable")


class TaggedSampler:
    def __init__(self, blocks, X, Y, k, activities=None):
        self.blocks = [[[qi(x) for x in row] for row in B] for B in blocks]
        self.n = sum(len(B) for B in blocks)
        self.r = len(X[0]) if X else 0
        self.X = [[qi(x) for x in row] for row in X]
        self.Y = [[qi(x) for x in row] for row in Y]
        self.k = k
        self.activities = [Fraction(x) for x in (activities or [1] * self.n)]
        assert len(self.activities) == self.n and all(x >= 0 for x in self.activities)
        self.G = [[QI() for _ in range(self.n)] for _ in range(self.n)]
        self.configs, self.offsets = [], []
        off = 0
        for B in self.blocks:
            self.offsets.append(off)
            for i, row in enumerate(B):
                for j, x in enumerate(row):
                    self.G[off + i][off + j] = x
            choices = []
            for labels in product(range(3), repeat=len(B)):
                I = tuple(off + i for i, s in enumerate(labels) if s == 1)
                J = tuple(off + i for i, s in enumerate(labels) if s == 2)
                choices.append((I, J))
            self.configs.append(choices)
            off += len(B)
        self.F = [[self.G[i][j] + sum(self.X[i][s] * self.Y[j][s]
                                    for s in range(self.r))
                   for j in range(self.n)] for i in range(self.n)]
        self.tags = []
        self.total_enumerated_tags = 0
        for p in range(min(self.r, self.k) + 1):
            for R in combinations(range(self.n), p):
                for C in combinations(range(self.n), p):
                    for S in combinations(range(self.r), p):
                        self.total_enumerated_tags += 1
                        if set(R) & set(C):
                            continue
                        coef = det(sub(self.X, R, S)) * det(sub(self.Y, C, S))
                        if coef:
                            self.tags.append((R, C, coef))
        self.local_cache = {}
        self.mass_cache = {}
        self.mass_calls = 0

    def local(self, a, b, t, choice):
        key = (a, b, t, choice)
        if key in self.local_cache:
            return self.local_cache[key]
        I, J = self.configs[t][choice]
        off, B = self.offsets[t], self.blocks[t]
        R, C, _ = self.tags[a]
        R2, C2, _ = self.tags[b]
        Rt = tuple(i for i in R if off <= i < off + len(B))
        Ct = tuple(i for i in C if off <= i < off + len(B))
        R2t = tuple(i for i in R2 if off <= i < off + len(B))
        C2t = tuple(i for i in C2 if off <= i < off + len(B))
        if (not set(Rt + R2t) <= set(I) or not set(Ct + C2t) <= set(J)
                or len(I) - len(Rt) != len(J) - len(Ct)
                or len(I) - len(R2t) != len(J) - len(C2t)):
            self.local_cache[key] = None
            return None
        posI = {i: p + 1 for p, i in enumerate(I)}
        posJ = {j: p + 1 for p, j in enumerate(J)}
        local_exp = sum(posI[i] for i in Rt + R2t) + sum(posJ[j] for j in Ct + C2t)
        d = det(sub(B, [i - off for i in I if i not in Rt],
                    [j - off for j in J if j not in Ct]))
        d2 = det(sub(B, [i - off for i in I if i not in R2t],
                     [j - off for j in J if j not in C2t]))
        weight = Fraction(1)
        for i in I:
            weight *= self.activities[i]
        value = d * d2.conj() * weight * (-1 if local_exp % 2 else 1)
        result = (len(I), len(J), value,
                  (len(Rt) + len(R2t)) % 2, (len(Ct) + len(C2t)) % 2)
        self.local_cache[key] = result
        return result

    def completion_mass(self, prefix=()):
        prefix = tuple(prefix)
        if prefix in self.mass_cache:
            return self.mass_cache[prefix]
        self.mass_calls += 1
        total = QI()
        for a, (_, _, ca) in enumerate(self.tags):
            for b, (_, _, cb) in enumerate(self.tags):
                dp = {(0, 0): QI(1)}
                for t in range(len(self.blocks)):
                    choices = [prefix[t]] if t < len(prefix) else range(len(self.configs[t]))
                    nxt = {}
                    for (rows, cols), value in dp.items():
                        for choice in choices:
                            entry = self.local(a, b, t, choice)
                            if entry is None:
                                continue
                            li, lj, w, ar, ac = entry
                            nr, nc = rows + li, cols + lj
                            if nr > self.k or nc > self.k:
                                continue
                            term = value * w * (-1 if (rows * ar + cols * ac) % 2 else 1)
                            if term:
                                nxt[nr, nc] = nxt.get((nr, nc), QI()) + term
                    dp = nxt
                total = total + ca * cb.conj() * dp.get((self.k, self.k), QI())
        assert total.im == 0, "completion mass must be real"
        assert total.re >= 0, "completion mass must be nonnegative"
        self.mass_cache[prefix] = total.re
        return total.re

    def sample(self, rng):
        if self.completion_mass() == 0:
            raise ValueError("zero coefficient; no target law")
        prefix = ()
        for t in range(len(self.blocks)):
            masses = [self.completion_mass(prefix + (choice,))
                      for choice in range(len(self.configs[t]))]
            assert sum(masses) == self.completion_mass(prefix)
            prefix += (weighted_index(masses, rng),)
        return self.decode(prefix)

    def decode(self, choices):
        I, J = [], []
        for t, choice in enumerate(choices):
            it, jt = self.configs[t][choice]
            I.extend(it)
            J.extend(jt)
        return tuple(I), tuple(J)

    def direct_mass(self, prefix=()):
        """Bounded exhaustive diagnostic only; not part of sampling algorithm."""
        total = Fraction(0)
        choices = [[prefix[t]] if t < len(prefix) else range(len(self.configs[t]))
                   for t in range(len(self.blocks))]
        for item in product(*choices):
            I, J = self.decode(item)
            if len(I) != self.k or len(J) != self.k:
                continue
            w = det(sub(self.F, I, J)).norm2()
            for i in I:
                w *= self.activities[i]
            total += w
        return total

    def pair_step(self, A, B, rng):
        """Actual reversible two-replica refresh kernel; no partition oracle."""
        if rng.getrandbits(1):
            return self.sample(rng), B
        return A, self.sample(rng)


def main():
    start = perf_counter()
    blocks = [[[1, 2], [0, 1]], [[0, 1], [2, -1]]]
    X = [[1, 0], [0, 1], [1, -1], [2, 1]]
    Y = [[0, 1], [1, 1], [-1, 0], [2, -1]]
    cases = []
    total_prefixes = 0
    for k in [0, 1, 2]:
        sampler = TaggedSampler(blocks, X, Y, k, [1, Fraction(2, 3), 2, 3])
        for length in range(len(blocks) + 1):
            for prefix in product(*(range(len(sampler.configs[t])) for t in range(length))):
                assert sampler.completion_mass(prefix) == sampler.direct_mass(prefix)
                total_prefixes += 1
        rng = Random(20261007 + k)
        samples = [sampler.sample(rng) for _ in range(24)]
        assert all(len(I) == len(J) == k and not set(I) & set(J) for I, J in samples)
        for I, J in samples:
            assert det(sub(sampler.F, I, J)).norm2() > 0
        A, B = samples[:2]
        for _ in range(24):
            A, B = sampler.pair_step(A, B, rng)
        cases.append({"k": k, "coefficient": str(sampler.completion_mass()),
                      "active_tags": len(sampler.tags), "prefix_mass_calls": sampler.mass_calls,
                      "samples": len(samples), "pair_steps": 24})

    complex_blocks = [[[QI(0, 1), 1], [1, QI(0, -1)]],
                      [[QI(1, 1), QI(0, 1)], [1, QI(1, -1)]]]
    sampler = TaggedSampler(complex_blocks,
                            [[QI(1, 1)], [QI(0, -1)], [2], [QI(1, -1)]],
                            [[QI(0, 1)], [1], [QI(-1, 1)], [2]], 2)
    for length in range(3):
        for prefix in product(*(range(len(sampler.configs[t])) for t in range(length))):
            assert sampler.completion_mass(prefix) == sampler.direct_mass(prefix)
            total_prefixes += 1
    assert sampler.completion_mass() > 0
    sampler.sample(Random(8))

    zero = TaggedSampler([[[0, 1], [0, 0]], [[0, 1], [0, 0]]],
                         [[1, 0], [0, 0], [0, 1], [0, 0]],
                         [[0, 0], [0, 1], [0, 0], [1, 0]], 2)
    assert zero.completion_mass() == zero.direct_mass() == 0
    try:
        zero.sample(Random(1))
    except ValueError:
        pass
    else:
        raise AssertionError("empty sector was sampled")
    result = {"status": "PASS exact conditional sampler and pair kernel checks",
              "origin": "c02_l05 full signed-tag proof, independently implemented by c02_s02",
              "real_weighted_cases": cases,
              "complex_rank_one_coefficient": str(sampler.completion_mass()),
              "exact_prefixes_compared": total_prefixes,
              "zero_dephasing_fixture": "exact empty-sector rejection",
              "elapsed_seconds": perf_counter() - start,
              "scope": "Finite bookkeeping and draw-interface checks only; no unrestricted mixing or FPRAS validation."}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
