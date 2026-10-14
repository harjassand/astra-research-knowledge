#!/usr/bin/env python3
"""Independent query/cache-count audit of shared balanced-tree cycle learner."""
from __future__ import annotations
import json, math, random
from collections import Counter
from pathlib import Path

N = 24

def tree(lo: int, hi: int):
    if hi - lo == 1:
        return (1 << lo, None, None)
    mid = (lo + hi) // 2
    left = tree(lo, mid)
    right = tree(mid, hi)
    return (left[0] | right[0], left, right)

def edges_from_order(order):
    n = len(order)
    return {tuple(sorted((order[j], order[(j+1) % n]))) for j in range(n)}

def learn(n, order):
    V = (1 << n) - 1
    # Store query weights as actual bitmasks. The bootstrap has q=t^2 from
    # W(V)W(0)/(W(V\{0})W({0})) = t^4; all n singleton masks are seeded.
    queried = {0, V, V ^ 1} | {1 << j for j in range(n)}
    tr = tree(0, n)
    cyc = edges_from_order(order)
    recovered = set()
    active_nodes = 0
    contrasts = 0

    def recurse(i, node_mask, left, right, k):
        nonlocal active_nodes, contrasts
        active_nodes += 1
        if left is None:  # singleton leaf, positive count means this is a neighbor
            assert node_mask.bit_count() == 1 and k == 1
            j = node_mask.bit_length() - 1
            recovered.add(tuple(sorted((i, j))))
            return
        # Query one child A that does not contain i. If i is in exactly one
        # child, use the other. If i is outside both, use left.
        if node_mask & (1 << i):
            A, other = (right, left) if left[0] & (1 << i) else (left, right)
        else:
            A, other = left, right
        a = A[0]
        queried.add(a)
        queried.add(a | (1 << i))
        contrasts += 1
        # Exact class oracle returns the true number of i's two cycle-neighbors
        # in A; inferred count in other is parent count minus this count.
        c_a = sum(tuple(sorted((i, j))) in cyc for j in range(n) if (a >> j) & 1)
        c_other = k - c_a
        assert 0 <= c_a <= 2 and 0 <= c_other <= 2
        if c_a:
            recurse(i, a, A[1], A[2], c_a)
        if c_other:
            recurse(i, other[0], other[1], other[2], c_other)

    # cycle edge order has degree 2 at every vertex
    for i in range(n):
        recurse(i, V, tr[1], tr[2], 2)
    true_edges = edges_from_order(order)
    if recovered != true_edges:
        raise AssertionError((sorted(true_edges - recovered), sorted(recovered - true_edges)))
    return {
        "n": n,
        "unique_energy_masks_total": len(queried),
        "bootstrap_seed_masks": len({0, V, V ^ 1} | {1 << j for j in range(n)}),
        "unique_masks_after_seed": len(queried - ({0, V, V ^ 1} | {1 << j for j in range(n)})),
        "pairwise_baseline_unique_masks": 1 + n + n*(n-1)//2,
        "contrast_calls": contrasts,
        "positive_tree_nodes_visited": active_nodes,
        "recovered_edges": len(recovered),
    }

def run():
    n = N
    rng = random.Random(20261014)
    results = []
    for _ in range(5000):
        order = list(range(n))
        rng.shuffle(order)
        results.append(learn(n, order))
    counts = [x["unique_energy_masks_total"] for x in results]
    contrast_counts = [x["contrast_calls"] for x in results]
    sorted_counts = sorted(counts)
    hist = Counter(counts)
    # Include a few reproducible examples at both extrema and median.
    examples = []
    for label, val in [("min", sorted_counts[0]), ("p10", sorted_counts[len(counts)//10]),
                       ("median", sorted_counts[len(counts)//2]),
                       ("p90", sorted_counts[9*len(counts)//10]), ("max", sorted_counts[-1])]:
        idx = counts.index(val)
        order = list(range(n))
        # Regenerate the indexed shuffled permutation deterministically.
        rr = random.Random(20261014)
        for _ in range(idx+1):
            order = list(range(n)); rr.shuffle(order)
        examples.append({"label":label,"order":order,**results[idx]})
    out = {
       "description":"5,000 independently randomized labelings of a 24-cycle; balanced coordinate tree [0,24), unique oracle weight bitmasks cached globally; exact counts only.",
       "seed":20261014,"samples":len(counts),"pairwise_baseline_unique_masks":301,
       "tree_unique_energy_masks":{"min":min(counts),"p10":sorted_counts[len(counts)//10],"median":sorted_counts[len(counts)//2],"mean":sum(counts)/len(counts),"p90":sorted_counts[9*len(counts)//10],"max":max(counts),"below_301":sum(c<301 for c in counts),"at_301":sum(c==301 for c in counts),"above_301":sum(c>301 for c in counts),"histogram":{str(k):v for k,v in sorted(hist.items())}},
       "contrast_calls":{"min":min(contrast_counts),"median":sorted(contrast_counts)[len(contrast_counts)//2],"max":max(contrast_counts)},
       "examples":examples,
       "audit_notes":["The seed uses {empty,V,all n singletons,V\\{0}} (n+3 distinct masks for n>2); seed overlap is counted by unique masks.","Each contrast adds W(A) and W(A+i), with all exact mask overlaps cached across all vertices.","The learned graph is checked against the planted cycle for every sample."]
    }
    dest = Path(__file__).parent / "replay" / "query_tree_audit.json"
    dest.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))

if __name__ == "__main__": run()
