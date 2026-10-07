#!/usr/bin/env python3
"""Exact small checks for the random-shift one-pivot lemma in REVISION-01.

Uses only real rational symmetric contractions and Fraction arithmetic. The
script enumerates every interval of shifts where the spectral partition is
constant, computes the exact expected A-coarsening loss, and independently
computes the pairwise commutator and expected pinching loss. It is a
transcription diagnostic, not a proof of the general lemma.
"""
from fractions import Fraction as F
from math import floor
import json
import random
import time
from itertools import combinations


def zeros(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def random_symmetric_contraction(rng, n):
    a = zeros(n)
    for i in range(n):
        a[i][i] = F(rng.randrange(-3, 4), 4)
        if i + 1 < n:
            v = F(rng.randrange(-2, 3), 8)
            a[i][i + 1] = a[i + 1][i] = v
    row = max(sum(abs(v) for v in r) for r in a)
    if row > 1:
        a = [[v / row for v in r] for r in a]
    return a


def commutator_energy(diag, ys, weights):
    n = len(diag)
    q = F(0)
    for y, w in zip(ys, weights):
        q += w * sum(((diag[i] - diag[j]) * y[i][j]) ** 2
                     for i in range(n) for j in range(n)) / n
    return q


def residues(diag, delta):
    return sorted({F(0), delta} | {a - floor(a / delta) * delta for a in diag})


def partition_costs(diag, y, delta, shift):
    n = len(diag)
    blocks = {}
    for i, a in enumerate(diag):
        blocks.setdefault(floor((a - shift) / delta), []).append(i)

    a_loss = F(0)
    for indices in blocks.values():
        mean = sum((diag[i] for i in indices), F(0)) / len(indices)
        a_loss += sum((diag[i] - mean) ** 2 for i in indices) / n

    y_loss = sum(y[i][j] ** 2 for i in range(n) for j in range(n)
                 if floor((diag[i] - shift) / delta)
                 != floor((diag[j] - shift) / delta)) / n
    return a_loss, y_loss


def expected_cost(diag, ys, weights, delta):
    cuts = residues(diag, delta)
    a_mean = F(0)
    y_mean = F(0)
    for lo, hi in zip(cuts, cuts[1:]):
        if hi == lo:
            continue
        shift = (lo + hi) / 2
        a_loss, _ = partition_costs(diag, ys[0], delta, shift)
        a_mean += (hi - lo) / delta * a_loss
        y_loss = sum(w * partition_costs(diag, y, delta, shift)[1]
                     for y, w in zip(ys, weights))
        y_mean += (hi - lo) / delta * y_loss
    return a_mean, y_mean


def check_case(case_id, rng, n):
    diag = [F(((7 * i + 5 * case_id + 3 * n) % 19) - 9, 9)
            for i in range(n)]
    ys = [random_symmetric_contraction(rng, n) for _ in range(4)]
    weights = [F(1, len(ys))] * len(ys)
    delta = F(1, 2 + (case_id % 3))
    q = commutator_energy(diag, ys, weights)
    a_loss, y_loss = expected_cost(diag, ys, weights, delta)
    total = a_loss + y_loss
    rhs_base = delta ** 2
    excess = max(F(0), total - rhs_base)
    if q == 0:
        ok = total <= rhs_base
    else:
        ok = total <= rhs_base or excess ** 2 * delta ** 2 <= q
    if not ok:
        raise AssertionError(f"case {case_id} violated exact squared form")
    if a_loss > delta ** 2:
        raise AssertionError(f"case {case_id} violated A coarsening bound")
    return {"case": case_id, "dimension": n, "delta": str(delta),
            "q_A": str(q), "expected_A_loss": str(a_loss),
            "expected_family_pinch_loss": str(y_loss),
            "squared_bound_passed": True}


def balanced_sign_partition_loss(d, block_sizes):
    """Exact block-center loss for all balanced signs and one partition."""
    if sum(block_sizes) != d or any(s < 1 for s in block_sizes):
        raise ValueError("block sizes must be positive and sum to d")
    n = d // 2
    total = F(0)
    count = 0
    for positive in combinations(range(d), n):
        h = [F(-1) for _ in range(d)]
        for i in positive:
            h[i] = F(1)
        capture = F(0)
        start = 0
        for size in block_sizes:
            block_sum = sum(h[start:start + size], F(0))
            capture += block_sum ** 2 / (d * size)
            start += size
        total += 1 - capture
        count += 1
    exact = total / count
    formula = F(1) - F(len(block_sizes) - 1, d - 1)
    if exact != formula:
        raise AssertionError(f"balanced-sign center loss mismatch at d={d}, m={len(block_sizes)}")
    return {"dimension": d, "balanced_signs": count,
            "blocks": len(block_sizes), "block_sizes": block_sizes,
            "center_channel_mean_loss": str(exact),
            "formula": str(formula), "exact_match": True}


def main():
    start = time.perf_counter()
    rng = random.Random(20261007)
    rows = [check_case(k, rng, 2 + (k % 7)) for k in range(1, 33)]
    sign_rows = []
    for d in (4, 6, 8, 10):
        for m in sorted({1, 2, d // 2, d}):
            sizes = [1] * (m - 1) + [d - m + 1]
            sign_rows.append(balanced_sign_partition_loss(d, sizes))
    elapsed = time.perf_counter() - start
    result = {"status": "PASS", "cases": len(rows), "max_dimension": 8,
              "arithmetic": "exact Fraction", "elapsed_seconds": elapsed,
              "scope": "transcription diagnostic only", "rows": rows,
              "block_center_not_EB_warning": sign_rows}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
