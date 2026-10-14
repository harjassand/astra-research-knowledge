#!/usr/bin/env python3
"""Bounded exact compatible-cycle search for one acoustic-certified quartic.

The source package is imported only from its copy under this owned directory.
All Fourier averages and edge actions are rational Laurent-polynomial integrals.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "incoming_resonant"))
from profile_algebra import add, scale, mul, cos, sin, meanprod, poly_terms, edge_coeffs, edge_value, r, s, p, q


def energy(n: int, m: int, lam=Q(1,10)):
    # Matrix entries are [[a,b],[c,d]]; carriers n,m enter the two
    # output coordinates as in the copied producer's Laurent convention.
    a = add(scale(cos(n), p), scale(cos(m), q))
    c = add(scale(sin(n), p), scale(sin(m), q))
    b = add(scale(sin(n), -n*r), scale(sin(m), -m*s))
    d = add(scale(cos(n), n*r), scale(cos(m), m*s))
    u = add(mul(a, a), mul(c, c))
    v = add(mul(b, b), mul(d, d))
    w = add(mul(a, b), mul(c, d))
    det = add(mul(a, d), scale(mul(b, c), -1))
    # F_lam = F_* - lam det^2.  Exact acoustic certificates are recorded
    # separately for lam=1/10 and 11/100.
    F = (meanprod(u, u) + meanprod(v, v) + 4*meanprod(w, w)
         + (Q(7,2)-lam)*meanprod(det, det)
         - Q(29, 10)*meanprod(det, add(u, v)))
    N4 = meanprod(add(u, v), add(u, v))
    return F, N4


def bellman(vertices, edge_choices):
    """Exact all-source Bellman-Ford on the min-width graph; return cycle/potential."""
    n = len(vertices)
    best = {}
    for i, j, k, cost in edge_choices:
        if (i, j) not in best or cost < best[i, j][0]:
            best[i, j] = (cost, k)
    dist = [Q(0) for _ in range(n)]
    pred = [None for _ in range(n)]
    changed = None
    for iteration in range(n):
        changed = None
        for (i, j), (cost, k) in best.items():
            cand = dist[i] + cost
            if cand < dist[j]:
                dist[j] = cand
                pred[j] = (i, k, cost)
                changed = j
        if changed is None:
            # Verify every original width choice, not merely each minimum.
            slacks = [cost + dist[i] - dist[j] for i, j, _k, cost in edge_choices]
            assert min(slacks) >= 0
            return {"kind": "NO_NEGATIVE_CYCLE", "passes": iteration+1,
                    "potential": [str(v) for v in dist],
                    "minimum_slack": str(min(slacks)),
                    "tight_edges": sum(v == 0 for v in slacks)}
    # Follow predecessors n times to enter a negative cycle, then close it.
    v = changed
    for _ in range(n):
        assert pred[v] is not None
        v = pred[v][0]
    start = v
    rev = []
    while True:
        edge = pred[v]
        assert edge is not None
        i, k, cost = edge
        rev.append((i, v, k, cost))
        v = i
        if v == start:
            break
        assert len(rev) <= n+1
    cycle = list(reversed(rev))
    total = sum((e[3] for e in cycle), Q(0))
    assert total < 0
    return {"kind": "NEGATIVE_CYCLE", "passes": n, "cycle_weight": str(total),
            "cycle": [[i, j, k, str(cost)] for i, j, k, cost in cycle]}


def run_graph(n, m, low=Q(0), radius=Q(2), step=Q(1,4), widths=None, lam=Q(1,10)):
    widths = widths or [Q(1,8), Q(1,4), Q(1,2), Q(1), Q(2)]
    axis=[]; x=Q(low)
    while x <= radius:
        axis.append(x); x += step
    vertices=[(x,y) for x in axis for y in axis]
    F, N4 = energy(n,m,lam)
    ft, nt = poly_terms(F), poly_terms(N4)
    choices=[]; negative_edges=0; min_edge=None
    for i, a in enumerate(vertices):
        for j, b in enumerate(vertices):
            fc=edge_coeffs(ft,a,b)
            for k,h in enumerate(widths):
                cost=edge_value(fc,h)
                choices.append((i,j,k,cost))
                if cost < 0: negative_edges += 1
                if min_edge is None or cost < min_edge[0]: min_edge=(cost,i,j,k)
    graph=bellman(vertices,choices)
    if graph["kind"] == "NEGATIVE_CYCLE":
        graph["cycle_profiles"]=[[list(map(str,vertices[i])),list(map(str,vertices[j])),str(widths[k]),cost]
                                  for i,j,k,cost in graph.pop("cycle")]
    return {"integrand": f"Fstar - ({lam}) q^2",
            "carriers": [n,m], "profile_box": [str(low),str(radius)],
            "profile_step": str(step), "vertex_count": len(vertices),
            "widths": [str(h) for h in widths],
            "edge_width_count": len(choices), "negative_raw_edges": negative_edges,
            "minimum_raw_edge": {"cost":str(min_edge[0]),"from":list(map(str,vertices[min_edge[1]])),
                                 "to":list(map(str,vertices[min_edge[2]])),"width":str(widths[min_edge[3]])},
            **graph}


if __name__ == "__main__":
    lam=Q(sys.argv[1]) if len(sys.argv)>1 else Q(1,10)
    runs=[]
    # Replay the incoming nonnegative 81-vertex geometry on three carrier
    # pairs, then broaden signs while holding the vertex count and widths
    # fixed.  The second family is not a generic fine grid.
    for n,m in [(1,-1),(1,3),(1,5),(1,-3),(3,-1)]:
        runs.append(run_graph(n,m,lam=lam))
        print(json.dumps({k:v for k,v in runs[-1].items()
                          if k not in ("potential",)}, indent=2), flush=True)
    for n,m in [(1,-1),(1,3),(1,-3)]:
        runs.append(run_graph(n,m,low=Q(-2),radius=Q(2),step=Q(1,2),lam=lam))
        print(json.dumps({k:v for k,v in runs[-1].items()
                          if k not in ("potential",)}, indent=2), flush=True)
    out=ROOT/f"exact_cycle_search_{lam.numerator}_{lam.denominator}.json"
    out.write_text(json.dumps(runs,indent=2)+"\n")
    if lam==Q(1,10): (ROOT/"exact_cycle_search.json").write_text(json.dumps(runs,indent=2)+"\n")
