#!/usr/bin/env python3
"""Finite stress tests of full-family inverse-union-multiplicity coupling.

Floating calculations are diagnostics, not a theorem certificate.  All family
members are integer bitsets and union closure is checked exactly.  No external
data other than the mathematical families explicitly generated below is used.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import random
import time

import numpy as np


def union_closed(family):
    values = set(family)
    return all((a | b) in values for a in values for b in values)


def close(generators):
    values = {0}
    for g in generators:
        values |= {a | g for a in values}
    return sorted(values)


def analyze(family, solve=True):
    f = sorted(set(family))
    assert len(f) > 1 and union_closed(f)
    N = len(f)
    index = {a: i for i, a in enumerate(f)}
    joins = np.array([[index[a | b] for b in f] for a in f], dtype=np.int64)
    counts = np.bincount(joins.ravel(), minlength=N)
    c = np.log(counts[joins])
    row = c.mean(axis=1)
    R = c - row[:, None] - row[None, :] + c.mean()
    nu0 = counts / (N * N)
    H0 = float(-np.sum(nu0 * np.log(nu0)))
    H = math.log(N)
    p = max(sum(bool(a & (1 << i)) for a in f) / N
            for i in range(max(f).bit_length()))
    V = float(np.mean(R * R))
    result = {
        "N": N, "max_frequency": p, "entropy": H,
        "independent_union_entropy": H0,
        "independent_entropy_deficit_fraction": (H - H0) / H,
        "residual_variance": V,
        "variance_over_logN_squared": V / H**2,
        "variance_over_logN": V / H,
    }
    if solve:
        K = np.exp(-c)
        scale = np.ones(N) / N
        for iteration in range(20000):
            rows = scale * (K @ scale)
            error = float(np.max(np.abs(rows - 1/N)))
            if error < 1e-13 / N:
                break
            scale *= np.sqrt((1/N) / rows)
        else:
            raise RuntimeError(("symmetric scaling did not converge", N, error))
        P = scale[:, None] * K * scale[None, :]
        nu = np.bincount(joins.ravel(), weights=P.ravel(), minlength=N)
        Hstar = float(-np.sum(nu * np.log(nu)))
        Q = K / N
        D0star = float(np.mean(-math.log(N*N) - np.log(P)))
        DstarQ = float(np.sum(P * np.log(P / Q)))
        projection_error = abs((H-H0) - D0star - DstarQ)
        assert projection_error < 2e-10
        assert Hstar + 1e-10 >= H0 + D0star
        assert Hstar < H + 1e-10
        result.update({
            "scaled_union_entropy": Hstar,
            "gain": Hstar-H0,
            "gain_over_logN": (Hstar-H0)/H,
            "gain_over_variance": (Hstar-H0)/V,
            "reverse_relative_entropy": D0star,
            "projection_identity_error": projection_error,
            "marginal_max_error": error,
            "scaling_iterations": iteration,
        })
    return result


def ordinal_cube_chain(d, chain_fraction):
    """Boolean d-cube followed by L strictly larger chain elements."""
    M = 1 << d
    L = max(1, round(chain_fraction * M))
    return list(range(M)) + [(1 << (d+j)) - 1 for j in range(1, L+1)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-count", type=int, default=300)
    parser.add_argument("--output", default="probe_results.json")
    args = parser.parse_args()
    start = time.perf_counter()
    records = []
    # Exhaustive labelled families on a 4-point ground set, omitting singletons.
    for mask in range(1, 1 << 16):
        if mask.bit_count() < 2:
            continue
        f = [a for a in range(16) if (mask >> a) & 1]
        if not union_closed(f):
            continue
        item = analyze(f)
        item["family"] = f
        item["kind"] = "exhaustive_n4"
        records.append(item)
    exhaustive_count = len(records)
    rng = random.Random(20261015)
    for _ in range(args.random_count):
        n = rng.randrange(5, 11)
        f = close(rng.sample(range(1 << n), rng.randrange(2, min(35, 1 << n))))
        if len(f) < 2 or len(f) > 400:
            continue
        item = analyze(f)
        item["family"] = f
        item["kind"] = "random_generated"
        records.append(item)
    structured = []
    for d in range(1, 9):
        for alpha in [1/16, 1/4, 1]:
            f = ordinal_cube_chain(d, alpha)
            item = analyze(f)
            item.update({"kind": "ordinal_cube_chain", "d": d, "alpha": alpha})
            structured.append(item)
    minima = []
    for cap in [.5, .55, .6, .65, .7, .75, .8, .9, 1]:
        qualifying = [r for r in records if r["max_frequency"] <= cap]
        for key in ["gain_over_logN", "gain_over_variance",
                    "independent_entropy_deficit_fraction", "variance_over_logN"]:
            if qualifying:
                item = min(qualifying, key=lambda r:r[key]).copy()
                minima.append({"cap":cap,"key":key,"qualifying":len(qualifying),"witness":item})
    out = {
        "scope": "finite floating diagnostics only; no universal frequency theorem",
        "elapsed_seconds": time.perf_counter()-start,
        "exhaustive_n4_nontrivial_count": exhaustive_count,
        "random_seed": 20261015,
        "total_records": len(records),
        "minima": minima,
        "structured": structured,
    }
    Path(args.output).write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k not in ["minima", "structured"]},indent=2))
    for item in minima:
        if item["key"] == "gain_over_logN":
            w=item["witness"]
            print("cap",item["cap"],"gain/logN",w["gain_over_logN"],"N",w["N"],"family",w["family"])


if __name__ == "__main__":
    main()
