"""Exact conditional inference for learned parity factors.

All matrices and vectors over GF(2) are represented by Python integer masks.
This module is a conventional affine-code / syndrome-trellis compiler.  It
does not learn A, assume a supplied planner, or enumerate the 2**n inputs.

Given A, positive rational pairs w_j, and evidence C x = z, it computes the
partition function, a MAP input, and exact samples.  Every sample is exact
relative to an ideal fair-bit source; Random(seed) is only for reproducible
verification.  The default bit source is SystemRandom.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
import random
from typing import Iterable


def parity(value: int) -> int:
    return value.bit_count() & 1


def lincomb(vectors: list[int], mask: int) -> int:
    answer = 0
    while mask:
        lowest = mask & -mask
        answer ^= vectors[lowest.bit_length() - 1]
        mask ^= lowest
    return answer


class InconsistentEvidence(ValueError):
    pass


class GF2System:
    """Compile elimination, a particular-solution map, and the kernel."""

    def __init__(self, rows: Iterable[int], ncols: int):
        self.ncols = ncols
        work = list(rows)
        self.nrows = len(work)
        if any(row < 0 or row >= (1 << ncols) for row in work):
            raise ValueError("Matrix row outside its declared width")
        transforms = [1 << i for i in range(len(work))]
        pivots = []
        row_index = 0
        for col in range(ncols):
            pivot = next((i for i in range(row_index, len(work))
                          if (work[i] >> col) & 1), None)
            if pivot is None:
                continue
            work[row_index], work[pivot] = work[pivot], work[row_index]
            transforms[row_index], transforms[pivot] = (
                transforms[pivot], transforms[row_index])
            for i in range(len(work)):
                if i != row_index and ((work[i] >> col) & 1):
                    work[i] ^= work[row_index]
                    transforms[i] ^= transforms[row_index]
            pivots.append(col)
            row_index += 1
        self.rank = row_index
        self.pivots = pivots
        self.transforms = transforms[:row_index]
        self.zero_transforms = transforms[row_index:]
        self.rref_rows = work[:row_index]
        pivot_set = set(pivots)
        self.kernel = []
        for free in range(ncols):
            if free in pivot_set:
                continue
            vector = 1 << free
            for row, pivot in zip(self.rref_rows, pivots):
                if (row >> free) & 1:
                    vector |= 1 << pivot
            self.kernel.append(vector)

    def particular(self, rhs: int, check: bool = True) -> int:
        if rhs < 0 or rhs >= (1 << self.nrows):
            raise ValueError("Right-hand side outside its declared width")
        if check and any(parity(t & rhs) for t in self.zero_transforms):
            raise InconsistentEvidence("Binary linear equations are inconsistent")
        return sum(parity(t & rhs) << p
                   for t, p in zip(self.transforms, self.pivots))


class BitSource:
    def __init__(self, seed: int | None = None):
        self.rng = random.SystemRandom() if seed is None else random.Random(seed)
        self.bits_used = 0
        self.draws = 0

    def getrandbits(self, count: int) -> int:
        self.bits_used += count
        self.draws += 1
        return self.rng.getrandbits(count)

    def randbelow(self, bound: int) -> int:
        if bound <= 0:
            raise ValueError("Positive bound required")
        if bound == 1:
            return 0
        count = (bound - 1).bit_length()
        while True:
            draw = self.getrandbits(count)
            if draw < bound:
                return draw


class ParityInference:
    """Condition and compile a positive rational parity-factor model."""

    def __init__(self, n: int, A: list[int],
                 weights: list[tuple[Fraction | int, Fraction | int]],
                 C: list[int] | None = None, z: int = 0):
        if len(A) != len(weights):
            raise ValueError("One pair of local weights is required per row of A")
        self.n, self.A, self.C, self.z = n, list(A), list(C or []), z
        self.weights = [(Fraction(a), Fraction(b)) for a, b in weights]
        if any(a <= 0 or b <= 0 for a, b in self.weights):
            raise ValueError("All local weights must be strictly positive")
        A_system = GF2System(A, n)
        self.rank_A = A_system.rank
        self.evidence_system = GF2System(self.C, n)
        self.x0 = self.evidence_system.particular(z)
        self.evidence_rank = self.evidence_system.rank
        N = self.evidence_system.kernel
        self.free_coordinates = len(N)
        self.projected_rows = [sum(parity(a & basis) << i
                                   for i, basis in enumerate(N)) for a in A]
        self.offsets = [parity(a & self.x0) for a in A]
        projected_system = GF2System(self.projected_rows, len(N))
        self.projected_rank = projected_system.rank
        self.raw_dependency = len(A) - projected_system.rank
        stack_rank = GF2System(A + self.C, n).rank
        assert self.raw_dependency == len(A) + self.evidence_rank - stack_rank
        assert self.raw_dependency == (len(A) - self.rank_A
                                       + self.rank_A + self.evidence_rank - stack_rank)

        # Integerize each weight pair using a common pair denominator.  All
        # later arithmetic is on positive integers, with one global denominator.
        self.denominator = 1
        self.constant = 1
        groups: dict[int, list[int]] = {}
        for row, offset, (w0, w1) in zip(self.projected_rows,
                                      self.offsets, self.weights):
            d0, d1 = w0.denominator, w1.denominator
            pair = [w0.numerator * d1, w1.numerator * d0]
            self.denominator *= d0 * d1
            if row == 0:
                self.constant *= pair[offset]
            else:
                current = groups.setdefault(row, [1, 1])
                current[0] *= pair[offset]
                current[1] *= pair[offset ^ 1]
        self.groups_before_constant_removal = len(groups)
        self.active_rows = []
        self.active_weights = []
        for row in sorted(groups):
            pair = groups[row]
            if pair[0] == pair[1]:
                self.constant *= pair[0]
            else:
                self.active_rows.append(row)
                self.active_weights.append(tuple(pair))
        self.g = len(self.active_rows)
        self.active_system = GF2System(self.active_rows, len(N))
        self.active_rank = self.active_system.rank
        self.fiber_dimension = len(N) - self.active_rank

        # Left nullspace: rows H satisfy H B = 0, so attainable active parity
        # vectors t are exactly the kernel of H.
        transpose = [sum(((row >> i) & 1) << j
                         for j, row in enumerate(self.active_rows))
                     for i in range(len(N))]
        self.checks = GF2System(transpose, self.g).kernel
        self.dependency = len(self.checks)
        assert self.dependency == self.g - self.active_rank
        assert self.dependency <= self.raw_dependency
        self.columns = [sum(((check >> j) & 1) << i
                            for i, check in enumerate(self.checks))
                        for j in range(self.g)]
        self.states = 1 << self.dependency

        # Compile a linear lift t -> x and a basis of the residual fiber.
        self.particular_lifts = [lincomb(N, self.active_system.particular(
            1 << j, check=False)) for j in range(self.g)]
        self.fiber_lifts = [lincomb(N, vector)
                           for vector in self.active_system.kernel]

        initial = [0] * self.states
        initial[0] = 1
        self.forward = [initial]
        maximum = initial
        self.max_choices = []
        for (u0, u1), h in zip(self.active_weights, self.columns):
            previous = self.forward[-1]
            self.forward.append([u0 * previous[a] + u1 * previous[a ^ h]
                                 for a in range(self.states)])
            next_maximum = []
            choices = []
            for a in range(self.states):
                zero, one = u0 * maximum[a], u1 * maximum[a ^ h]
                choose = int(one > zero)
                choices.append(choose)
                next_maximum.append(one if choose else zero)
            maximum = next_maximum
            self.max_choices.append(choices)
        self.partition = Fraction((1 << self.fiber_dimension) * self.constant
                                  * self.forward[-1][0], self.denominator)
        self.map_weight = Fraction(self.constant * maximum[0], self.denominator)

    def lift(self, active: int, fiber: int = 0) -> int:
        return (self.x0 ^ lincomb(self.particular_lifts, active)
                ^ lincomb(self.fiber_lifts, fiber))

    def map_input(self) -> int:
        syndrome, active = 0, 0
        for j in range(self.g - 1, -1, -1):
            bit = self.max_choices[j][syndrome]
            active |= bit << j
            if bit:
                syndrome ^= self.columns[j]
        assert syndrome == 0
        return self.lift(active)

    def sample(self, source: BitSource | None = None) -> int:
        source = source or BitSource()
        syndrome, active = 0, 0
        for j in range(self.g - 1, -1, -1):
            u0, u1 = self.active_weights[j]
            h = self.columns[j]
            mass0 = u0 * self.forward[j][syndrome]
            mass1 = u1 * self.forward[j][syndrome ^ h]
            if not mass0:
                bit = 1
            elif not mass1:
                bit = 0
            else:
                bit = int(source.randbelow(mass0 + mass1) >= mass0)
            active |= bit << j
            if bit:
                syndrome ^= h
        assert syndrome == 0
        fiber = source.getrandbits(self.fiber_dimension) if self.fiber_dimension else 0
        return self.lift(active, fiber)

    def objective(self, x: int) -> Fraction:
        if any(parity(c & x) != ((self.z >> i) & 1)
               for i, c in enumerate(self.C)):
            return Fraction(0)
        value = Fraction(1)
        for row, pair in zip(self.A, self.weights):
            value *= pair[parity(row & x)]
        return value

    def parity_event_probability(self, D: list[int], e: int) -> Fraction:
        """Exact Pr[D x=e | C x=z], with recompilation costs charged."""
        if e < 0 or e >= (1 << len(D)):
            raise ValueError("Event value outside its declared width")
        try:
            conditioned = ParityInference(self.n, self.A, self.weights,
                                          self.C + list(D),
                                          self.z | (e << len(self.C)))
        except InconsistentEvidence:
            return Fraction(0)
        return conditioned.partition / self.partition

    def enumerated_sampler_law(self) -> dict[int, Fraction]:
        """Verification-only exhaustive expansion of sampler branches."""
        paths = [(0, 0, Fraction(1))]
        for j in range(self.g - 1, -1, -1):
            next_paths = []
            u0, u1 = self.active_weights[j]
            h = self.columns[j]
            for syndrome, active, probability in paths:
                masses = [u0 * self.forward[j][syndrome],
                          u1 * self.forward[j][syndrome ^ h]]
                total = sum(masses)
                for bit in (0, 1):
                    if masses[bit]:
                        next_paths.append((syndrome ^ (h if bit else 0),
                                           active | (bit << j),
                                           probability * Fraction(masses[bit], total)))
            paths = next_paths
        output = {}
        for syndrome, active, probability in paths:
            assert syndrome == 0
            for fiber in range(1 << self.fiber_dimension):
                x = self.lift(active, fiber)
                assert x not in output
                output[x] = probability / (1 << self.fiber_dimension)
        return output

    def summary(self) -> dict:
        return {
            "n": self.n, "original_factors": len(self.A),
            "rank_A": self.rank_A, "rank_C": self.evidence_rank,
            "projected_rank": self.projected_rank,
            "raw_dependency": self.raw_dependency,
            "distinct_nonzero_projected_factors": self.groups_before_constant_removal,
            "active_factors": self.g, "active_rank": self.active_rank,
            "effective_dependency": self.dependency,
            "syndrome_states": self.states,
            "dp_cells": (self.g + 1) * self.states,
            "fiber_dimension": self.fiber_dimension,
            "feasible_input_count": 1 << (self.n - self.evidence_rank),
            "partition_numerator_bits": self.partition.numerator.bit_length(),
            "partition_denominator_bits": self.partition.denominator.bit_length(),
        }


def verify() -> dict:
    rng = random.Random(93257)
    exact_cases = 150
    sampler_law_cases = 40
    total_exhaustive_inputs = 0
    actual_samples = 0
    source = BitSource(13579)
    for trial in range(exact_cases):
        n = rng.randint(1, 9)
        s = rng.randint(0, 11)
        A = [rng.getrandbits(n) for _ in range(s)]
        C = [rng.getrandbits(n) for _ in range(rng.randint(0, n + 2))]
        truth = rng.getrandbits(n)
        z = sum(parity(c & truth) << i for i, c in enumerate(C))
        weights = [(Fraction(rng.randint(1, 7), rng.randint(1, 7)),
                    Fraction(rng.randint(1, 7), rng.randint(1, 7)))
                   for _ in range(s)]
        model = ParityInference(n, A, weights, C, z)
        brute = {x: model.objective(x) for x in range(1 << n)}
        brute = {x: weight for x, weight in brute.items() if weight}
        total_exhaustive_inputs += 1 << n
        assert model.partition == sum(brute.values(), Fraction(0))
        assert model.map_weight == max(brute.values())
        assert brute[model.map_input()] == model.map_weight
        if trial < sampler_law_cases:
            law = model.enumerated_sampler_law()
            assert law == {x: weight / model.partition for x, weight in brute.items()}
            event = rng.getrandbits(n)
            expected = sum((weight for x, weight in brute.items()
                            if parity(event & x)), Fraction(0)) / model.partition
            assert model.parity_event_probability([event], 1) == expected
        for _ in range(5):
            assert model.sample(source) in brute
            actual_samples += 1
    try:
        ParityInference(2, [1], [(1, 2)], [1, 1], 1)
    except InconsistentEvidence:
        pass
    else:
        raise AssertionError("Inconsistent evidence was not rejected")

    simplified = ParityInference(5, [1, 2, 3, 4, 5],
                                 [(3, 5), (2, 3), (3, 2), (1, 2), (1, 2)],
                                 [1], 0)
    assert simplified.partition == 720
    assert simplified.raw_dependency == 3
    assert simplified.dependency == 0
    assert simplified.g == 1

    # Dense, independent learned parities. Evidence contains five independent
    # combinations of learned parities and three independent external parities.
    n = 64
    A = []
    while len(A) < 60:
        candidate = rng.getrandbits(n)
        if GF2System(A + [candidate], n).rank > len(A):
            A.append(candidate)
    C = []
    while len(C) < 5:
        candidate = lincomb(A, rng.getrandbits(len(A)))
        if GF2System(C + [candidate], n).rank > len(C):
            C.append(candidate)
    while len(C) < 8:
        candidate = rng.getrandbits(n)
        if GF2System(A + C + [candidate], n).rank > GF2System(A + C, n).rank:
            C.append(candidate)
    truth = rng.getrandbits(n)
    z = sum(parity(c & truth) << i for i, c in enumerate(C))
    weights = [(Fraction(rng.randint(1, 7), rng.randint(1, 7)),
                Fraction(rng.randint(1, 7), rng.randint(1, 7))) for _ in A]
    # Ensure that the illustrated large case does not lose rows to constant factors.
    weights = [(a, b if b != a else b + 1) for a, b in weights]
    large = ParityInference(n, A, weights, C, z)
    assert large.raw_dependency == 5
    assert large.dependency == 5
    assert large.objective(large.map_input()) == large.map_weight
    large_sample = large.sample(source)
    assert large.objective(large_sample) > 0
    report = {
        "verification": {
            "exact_partition_and_MAP_cases": exact_cases,
            "complete_exact_sampler_laws": sampler_law_cases,
            "exact_conditional_event_probabilities": sampler_law_cases,
            "exhaustively_checked_raw_inputs": total_exhaustive_inputs,
            "sampled_inputs_checked_feasible": actual_samples + 1,
            "fair_bits_used_by_reproducible_sampler": source.bits_used,
            "inconsistent_evidence": "correctly rejected",
        },
        "simplification_example": simplified.summary(),
        "large_dense_example": large.summary(),
        "large_example_instance": {
            "A_hex": [hex(a) for a in A], "C_hex": [hex(c) for c in C],
            "z_hex": hex(z),
            "weights": [[str(a), str(b)] for a, b in weights],
            "map_input_hex": hex(large.map_input()),
            "partition": str(large.partition),
            "map_weight": str(large.map_weight),
        },
    }
    return report


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
