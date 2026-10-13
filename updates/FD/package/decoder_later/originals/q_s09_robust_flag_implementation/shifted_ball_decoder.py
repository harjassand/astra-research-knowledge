"""Random sampled Reed majority decoding, with shared shifted Hamming balls.

Input is a raw binary callback. No clean label, target coefficients, or bad-set
identities enter this module.  See PROOF.txt for the conditional error theorem.
Python stdlib only.  The decoder is a proposal routine outside its noise promise.
"""
from __future__ import annotations
from itertools import combinations
import math
from typing import Callable


def monomials(n: int, d: int) -> list[int]:
    return [sum(1 << i for i in inds)
            for k in range(min(n, d) + 1) for inds in combinations(range(n), k)]


def submasks(s: int) -> list[int]:
    out = []
    a = s
    while True:
        out.append(a)
        if a == 0:
            return out
        a = (a - 1) & s


def odd_ceil(z: float) -> int:
    r = max(1, math.ceil(z))
    return r if r & 1 else r + 1


def repetitions(n: int, d: int, rho: float, failure: float) -> dict[int, int]:
    if not 0 <= d <= n or not 0 <= rho < 2.0 ** (-d - 1) or not 0 < failure < 1:
        raise ValueError("invalid degree/noise/confidence contract")
    M = len(monomials(n, d))
    return {k: odd_ceil(math.log(M / failure) / (2 * (0.5 - (1 << k) * rho) ** 2))
            for k in range(d + 1)}


def evaluate(terms: list[int], x: int) -> int:
    return sum((x & s) == s for s in terms) & 1


class ShiftedBallDecoder:
    """Recover all coefficients, or propose a degree-d body outside the promise.

    A round queries raw(x xor a) at every weight-at-most-d mask a, for uniform x.
    Coefficient votes descend by degree.  Higher recovered coefficients are
    subtracted algebraically from finite differences, with all rounds retained.
    These data are shared safely: the proof uses a union bound on votes defined
    using the fixed TRUE higher coefficients, not conditioning those votes on
    successful higher recovery.
    """
    def __init__(self, n: int, d: int, rho: float, failure: float, rng):
        self.n, self.d, self.rho, self.failure, self.rng = n, d, rho, failure, rng
        self.anchors = monomials(n, d)
        self.repeats = repetitions(n, d, rho, failure)
        index = {a: j for j, a in enumerate(self.anchors)}
        self.instructions = [(s, [index[a] for a in submasks(s)])
                             for s in reversed(self.anchors)]
        self.raw_requests = self.random_bits = self.coefficient_votes = 0
        self.rounds = self.calls = self.peak_retained_bits = 0

    def decode(self, raw: Callable[[int], int]) -> list[int]:
        R = max(self.repeats.values())
        records = []
        for _ in range(R):
            x = self.rng.getrandbits(self.n)
            self.random_bits += self.n
            # Byte arrays hold actual binary labels, not Python integer objects.
            labels = []
            for a in self.anchors:
                labels.append(int(raw(x ^ a)))
                self.raw_requests += 1
            word = bytes(labels)
            if any(b > 1 for b in word):
                raise ValueError("raw callback must return a binary label")
            records.append((x, word))
        self.rounds += R
        self.peak_retained_bits = max(self.peak_retained_bits,
                                     R * (self.n + len(self.anchors)))
        terms = []
        for s, indices in self.instructions:
            k = s.bit_count()
            higher_differences = [t ^ s for t in terms if (t & s) == s]
            votes = 0
            for x, word in records[:self.repeats[k]]:
                bit = 0
                for j in indices:
                    bit ^= word[j]
                for t in higher_differences:
                    bit ^= int((x & t) == t)
                votes += bit
            self.coefficient_votes += self.repeats[k]
            if 2 * votes > self.repeats[k]:
                terms.append(s)
        self.calls += 1
        return sorted(terms)

    def ledger(self):
        return dict(decoder="sampled_shifted_ball_reed_majority", degree=self.d,
                    raw_error_density_promise=self.rho,
                    per_body_failure_budget=self.failure,
                    repetitions_by_degree=self.repeats,
                    shifted_ball_positions=len(self.anchors),
                    decoded_bodies=self.calls, raw_label_requests=self.raw_requests,
                    shift_random_bits=self.random_bits,
                    sampled_rounds=self.rounds, coefficient_votes=self.coefficient_votes,
                    peak_retained_logical_bits=self.peak_retained_bits)
