#!/usr/bin/env python3
"""Exact small-family diagnostics for entropy couplings on union-closed families.

No external packages are required.  The enumerator is exhaustive on a fixed
ground set [n] and checks closure directly.  It records exact integer pair
union multiplicities, coordinate frequencies, and the double-centered
log-multiplicity variance V used by the inverse-multiplicity coupling.

This is finite evidence only; it does not establish a universal inequality.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import product
from typing import Iterable


def members_from_code(code: int, universe_size: int) -> tuple[int, ...]:
    return tuple(s for s in range(1 << universe_size) if (code >> s) & 1)


def is_union_closed(members: tuple[int, ...]) -> bool:
    present = set(members)
    return all((a | b) in present for a in members for b in members)


def pair_data(members: tuple[int, ...], universe_size: int) -> dict:
    n = len(members)
    counts = {s: 0 for s in members}
    for a in members:
        for b in members:
            counts[a | b] += 1
    logs = {(a, b): math.log(counts[a | b]) for a in members for b in members}
    row = {a: sum(logs[a, b] for b in members) / n for a in members}
    mean = sum(row.values()) / n
    residual = {
        (a, b): logs[a, b] - row[a] - row[b] + mean
        for a in members for b in members
    }
    variance = sum(x * x for x in residual.values()) / (n * n)
    p = [sum(1 for a in members if (a >> i) & 1) / n for i in range(universe_size)]
    return {
        "N": n,
        "p": max(p, default=0.0),
        "frequencies": p,
        "V2": variance,
        "V2_over_logN": variance / math.log(n) if n > 1 else None,
        "V2_over_logN_squared": variance / (math.log(n) ** 2) if n > 1 else None,
        "r": [counts[s] for s in members],
    }


def kway_residual_variance(members: tuple[int, ...], k: int) -> float:
    """Compute V_k after projecting log r_k(union) off all one-slot terms.

    This is only intended for small N and k; it uses the full N**k tensor.
    The least-squares projection has a closed form for the product-uniform
    measure: R(x_1,...,x_k)=c-sum_j E[c|X_j]+(k-1)E[c].
    """
    n = len(members)
    if n ** k > 2_000_000:
        raise ValueError(f"N^k={n**k} too large for direct k-way diagnostic")
    tuples = list(product(members, repeat=k))
    union_values = []
    for tup in tuples:
        u = 0
        for a in tup:
            u |= a
        union_values.append(u)
    counts: dict[int, int] = {}
    for u in union_values:
        counts[u] = counts.get(u, 0) + 1
    cvals = [math.log(counts[u]) for u in union_values]
    mean = sum(cvals) / len(cvals)
    cond = []
    for slot in range(k):
        accum = {a: [0.0, 0] for a in members}
        for tup, c in zip(tuples, cvals):
            accum[tup[slot]][0] += c
            accum[tup[slot]][1] += 1
        cond.append({a: accum[a][0] / accum[a][1] for a in members})
    v = 0.0
    for tup, c in zip(tuples, cvals):
        r = c - sum(cond[j][tup[j]] for j in range(k)) + (k - 1) * mean
        v += r * r
    return v / len(tuples)


def boolean_cube_profile(n: int, k: int) -> dict:
    """Closed-form V_k for F=2^[n], with independent uniform input slots."""
    if n < 1 or k < 2:
        raise ValueError("require n>=1 and k>=2")
    log_mult = math.log((1 << k) - 1)
    per_coordinate = log_mult**2 * (2.0 ** (-k) - (k + 1) * 2.0 ** (-2 * k))
    return {
        "family": "2^[n]",
        "n": n,
        "N": 1 << n,
        "k": k,
        "V_k_closed_form": n * per_coordinate,
        "V_k_over_logN": per_coordinate / math.log(2.0),
    }


def enumerate_families(n: int) -> Iterable[tuple[int, ...]]:
    powerset_size = 1 << n
    if powerset_size > 20:
        raise ValueError("exhaustive family-code scan capped at n<=4")
    for code in range(1, 1 << powerset_size):
        members = members_from_code(code, n)
        if any(s != 0 for s in members) and is_union_closed(members):
            yield members


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4, help="ground-set size (exhaustive cap 4)")
    parser.add_argument("--k", type=int, default=3, help="also compute V_k for N^k <= 2,000,000")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--cube", action="store_true", help="print the closed-form Boolean-cube profile")
    parser.add_argument("--cube-n", type=int, default=4)
    args = parser.parse_args()

    if args.cube:
        print(json.dumps(boolean_cube_profile(args.cube_n, args.k), indent=2))
        return

    records = []
    for members in enumerate_families(args.n):
        rec = pair_data(members, args.n)
        if args.k >= 2 and rec["N"] ** args.k <= 2_000_000:
            rec[f"V{args.k}"] = kway_residual_variance(members, args.k)
        rec["family"] = list(members)
        records.append(rec)

    if args.json:
        print(json.dumps({"n": args.n, "k": args.k, "families": len(records), "records": records}, indent=2))
        return

    print(f"n={args.n}; enumerated_nontrivial_union_closed_families={len(records)}")
    if not records:
        return
    print("Smallest p record:")
    print(json.dumps(min(records, key=lambda r: (r["p"], r["N"])), indent=2))
    candidates = [r for r in records if r["N"] > 1]
    print("Smallest V2/log(N) among N>1:")
    print(json.dumps(min(candidates, key=lambda r: r["V2_over_logN"]), indent=2))
    if args.k >= 2:
        print(f"Smallest V{args.k}/log(N) among computed N>1:")
        eligible = [r for r in candidates if f"V{args.k}" in r]
        print(json.dumps(min(eligible, key=lambda r: r[f"V{args.k}"] / math.log(r["N"])), indent=2))


if __name__ == "__main__":
    main()
