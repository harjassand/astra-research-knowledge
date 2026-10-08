"""Search the exact Weyl compatibility SDP for a maximal-abelian-line cover.

For each line L, B(q)=max_{choice in {empty} union (L\\{0})}
sum_L (2 lambda_choice - 1), so maximizing B over compatible channels is the
finite maximum of linear SDP objectives. Exhaustive mode is exact at the
combinatorial level; solver outputs remain numerical diagnostics.
"""
from __future__ import annotations

import argparse
import itertools
import json
import time
import numpy as np
from weyl_sdp import compatibility_sdp, line_system, line_cover


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=int, required=True)
    ap.add_argument("--samples", type=int, default=1000)
    ap.add_argument("--exhaustive", action="store_true")
    ap.add_argument("--seed", type=int, default=20261008)
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--eps", type=float, default=2e-7)
    ap.add_argument("--hs-positive", action="store_true",
                    help="restrict to nonnegative Weyl superoperator spectrum")
    args = ap.parse_args()

    d = args.d
    points, index, qv, lamv, solve = compatibility_sdp(
        d, eps=args.eps, hs_positive=args.hs_positive)
    lines = line_system(d)
    n = d * d
    if args.exhaustive:
        choices = [None, *range(1, d)]
        selections = itertools.product(choices, repeat=d + 1)
    else:
        rng = np.random.default_rng(args.seed)
        def random_selections():
            for _ in range(args.samples):
                yield tuple(None if rng.random() < 0.30 else int(rng.integers(1, d))
                            for _ in range(d + 1))
        selections = random_selections()

    started = time.time()
    best = {"value": -float("inf")}
    count = 0
    for sel in selections:
        direction = np.zeros(n)
        active = 0
        for line, k in zip(lines, sel):
            if k is not None:
                direction[line[k - 1]] += 2.0
                active += 1
        result = solve(direction)
        value = result["value"] - active
        count += 1
        if value > best["value"]:
            budget, peaks, terms = line_cover(result["lambda"], lines)
            best = {
                "value": value,
                "budget_at_optimizer": budget,
                "peaks": peaks,
                "terms": terms,
                "selection": sel,
                "q": result["q"].tolist(),
                "lambda": result["lambda"].tolist(),
                "sdp_objective": result["value"],
                "solver_status": result["status"],
                "solver_stats": result["solver_stats"],
            }
    payload = {
        "dimension": d,
        "domain": ("HS-positive, HS-self-adjoint, unital CPTP Weyl-covariant self-compatible maps"
                   if args.hs_positive else
                   "HS-self-adjoint, unital CPTP Weyl-covariant self-compatible maps; spectrum may be negative"),
        "selection_search": "exhaustive" if args.exhaustive else "random-selections",
        "selection_count": count,
        "seed": None if args.exhaustive else args.seed,
        "objective": "max_q sum_lines max(0, max_{x in line}(2 lambda_x - 1))",
        "best": best,
        "wall_seconds": time.time() - started,
        "solver": "SCS",
        "solver_eps": args.eps,
        "caveat": "Finite floating-point SDP search; not a proof or rational certificate.",
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(json.dumps({k: payload[k] for k in ("dimension", "selection_search", "selection_count", "best", "wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
