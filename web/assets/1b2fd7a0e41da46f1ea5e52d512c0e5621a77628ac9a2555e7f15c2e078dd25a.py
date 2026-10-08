#!/usr/bin/env python3
"""Exact small-instance certificate for robust radius-cluster recovery.

The input is an N x M JSON array of frequency vectors. Decimal JSON numbers
are converted to rational numbers, so all squared-distance comparisons and
the strict-gap stopping certificate are exact. The exhaustive search is
exponential and is intended as a transparent verifier for small instances,
not a scalable clustering implementation.

Model-free inputs: known K and the calibrated outlier budget b. The search
does not take E, kappa, r, labels, or cluster centers as input.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from fractions import Fraction
from itertools import combinations
from typing import Iterable, Iterator, Sequence

Vector = tuple[Fraction, ...]
Partition = tuple[tuple[int, ...], ...]


def as_fraction(x: object) -> Fraction:
    if isinstance(x, Decimal):
        return Fraction(x)
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, float):
        return Fraction(str(x))
    raise TypeError(f"coordinate must be a JSON number, got {type(x).__name__}")


def squared_distance(x: Vector, y: Vector) -> Fraction:
    return sum(((a - b) ** 2 for a, b in zip(x, y)), Fraction(0))


def partitions_of_size_at_least(items: Sequence[int], k: int, minimum: int) -> Iterator[Partition]:
    """Yield each unordered k-partition once, with every block >= minimum."""
    blocks: list[list[int]] = []

    def visit(pos: int) -> Iterator[Partition]:
        left = len(items) - pos
        if pos == len(items):
            if len(blocks) == k and all(len(block) >= minimum for block in blocks):
                yield tuple(tuple(block) for block in blocks)
            return
        if len(blocks) > k or len(blocks) + left < k:
            return

        item = items[pos]
        # Place in an existing block; this canonical recursion avoids block
        # permutations because the first item always starts block zero.
        for j in range(len(blocks)):
            blocks[j].append(item)
            yield from visit(pos + 1)
            blocks[j].pop()

        if len(blocks) < k:
            blocks.append([item])
            yield from visit(pos + 1)
            blocks.pop()

    yield from visit(0)


def canonical_partition(partition: Partition) -> Partition:
    return tuple(sorted((tuple(sorted(block)) for block in partition), key=lambda block: block[0]))


def gap_certificate(points: Sequence[Vector], partition: Partition) -> tuple[Fraction, Fraction, Fraction] | None:
    """Return (max within squared distance, min cross squared distance, gap)."""
    within = Fraction(0)
    cross: Fraction | None = None
    for i, block in enumerate(partition):
        for a, b in combinations(block, 2):
            within = max(within, squared_distance(points[a], points[b]))
        for other in partition[i + 1 :]:
            for a in block:
                for b in other:
                    d2 = squared_distance(points[a], points[b])
                    cross = d2 if cross is None else min(cross, d2)
    if cross is None:
        return None
    gap = cross - within
    if gap <= 0:
        return None
    return within, cross, gap


def certify(points: Sequence[Vector], k: int, bad_budget: int) -> dict[str, object]:
    n = len(points)
    if not points or any(len(x) != len(points[0]) for x in points):
        raise ValueError("points must be a nonempty rectangular array")
    if not 1 <= k <= n or bad_budget < 0 or bad_budget >= n:
        raise ValueError("require 1 <= K <= N and 0 <= bad_budget < N")

    witnesses: dict[tuple[tuple[int, ...], Partition], tuple[Fraction, Fraction, Fraction]] = {}
    indices = tuple(range(n))
    for drop_count in range(bad_budget + 1):
        for dropped in combinations(indices, drop_count):
            dropped_set = set(dropped)
            kept = tuple(i for i in indices if i not in dropped_set)
            if len(kept) < k * (bad_budget + 1):
                continue
            for part in partitions_of_size_at_least(kept, k, bad_budget + 1):
                part = canonical_partition(part)
                cert = gap_certificate(points, part)
                if cert is not None:
                    witnesses[(tuple(dropped), part)] = cert

    if len(witnesses) != 1:
        return {
            "status": "UNKNOWN",
            "reason": "no strict-gap witness or more than one distinct outlier/partition witness",
            "N": n,
            "K": k,
            "bad_budget": bad_budget,
            "feasible_witness_count": len(witnesses),
        }

    (dropped, part), (within2, cross2, gap2) = next(iter(witnesses.items()))
    labels = [-1] * n
    centers: list[list[str]] = []
    for state, block in enumerate(part):
        for i in block:
            labels[i] = state
        center = [
            sum((points[i][j] for i in block), Fraction(0)) / len(block)
            for j in range(len(points[0]))
        ]
        centers.append([str(x) for x in center])

    return {
        "status": "CERTIFIED",
        "N": n,
        "K": k,
        "bad_budget": bad_budget,
        "dropped_indices": list(dropped),
        "labels_up_to_permutation": labels,
        "cluster_indices": [list(block) for block in part],
        "center_means_exact_rational": centers,
        "max_within_squared_distance": str(within2),
        "min_between_squared_distance": str(cross2),
        "strict_squared_gap": str(gap2),
        "feasible_witness_count": 1,
        "certificate": "unique exhaustive partition/outlier witness; max within squared distance < min cross squared distance",
    }


def self_test() -> None:
    # Two tight clusters and one arbitrary outlier; the strict-gap witness
    # uniquely identifies the two cores without supplying centers or labels.
    raw = [
        ["0.1", "0"],
        ["-0.1", "0"],
        ["9.9", "0"],
        ["10.1", "0"],
        ["50", "50"],
    ]
    points = [tuple(Fraction(Decimal(x)) for x in row) for row in raw]
    result = certify(points, k=2, bad_budget=1)
    assert result["status"] == "CERTIFIED", result
    assert sorted(tuple(x) for x in result["cluster_indices"]) == [(0, 1), (2, 3)]
    assert result["dropped_indices"] == [4]

    # This data have no strict-gap decomposition at the requested K and budget.
    ambiguous = [
        (Fraction(0),),
        (Fraction(1),),
        (Fraction(2),),
        (Fraction(3),),
    ]
    abstained = certify(ambiguous, k=2, bad_budget=1)
    assert abstained["status"] == "UNKNOWN", abstained
    print(json.dumps({"separated_example": result, "ambiguous_example": abstained}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--points", help="JSON file containing an N x M array")
    parser.add_argument("--states", type=int, help="known number K of hidden states")
    parser.add_argument("--bad-budget", type=int, help="known upper bound b on contaminated points")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if not args.points or args.states is None or args.bad_budget is None:
        parser.error("provide --points, --states, and --bad-budget, or use --self-test")

    with open(args.points, "r", encoding="utf-8") as f:
        raw = json.load(f, parse_float=Decimal, parse_int=Decimal)
    points = [tuple(as_fraction(x) for x in row) for row in raw]
    print(json.dumps(certify(points, args.states, args.bad_budget), indent=2))


if __name__ == "__main__":
    main()
