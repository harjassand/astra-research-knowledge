#!/usr/bin/env python3
"""Exact all-direction endotacticity check for a finite planar network.

No floating point arithmetic is used. The critical arrangement consists of
the lines where a reaction projection vanishes or two source scores tie.
Each critical ray and one integer vector in every open angular cell are tested.
"""

from __future__ import annotations

from functools import cmp_to_key
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REACTIONS = [
    ((0, 0), (2, 0)),
    ((2, 0), (4, 1)),
    ((4, 1), (5, 3)),
    ((5, 3), (3, 0)),
]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def primitive(v):
    from math import gcd

    g = gcd(abs(v[0]), abs(v[1]))
    if not g:
        raise ValueError("zero vector")
    return (v[0] // g, v[1] // g)


def half(v):
    # Increasing polar angle from +x; exact integer partition.
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1


def ray_cmp(a, b):
    ha, hb = half(a), half(b)
    if ha != hb:
        return -1 if ha < hb else 1
    c = cross(a, b)
    if c:
        return -1 if c > 0 else 1
    return 0


def canonical_line_normal(v):
    """A primitive normal to the line v·u=0, in a canonical sign."""
    n = primitive((-v[1], v[0]))
    return n if (n[0] > 0 or (n[0] == 0 and n[1] > 0)) else (-n[0], -n[1])


def critical_rays():
    sources = [y for y, _ in REACTIONS]
    deltas = [(z[0] - y[0], z[1] - y[1]) for y, z in REACTIONS]
    lines = {canonical_line_normal(d) for d in deltas}
    for i in range(len(sources)):
        for j in range(i + 1, len(sources)):
            diff = (sources[i][0] - sources[j][0], sources[i][1] - sources[j][1])
            if diff != (0, 0):
                lines.add(canonical_line_normal(diff))
    return sorted({v for n in lines for v in (n, (-n[0], -n[1]))}, key=cmp_to_key(ray_cmp))


def exact_status(u):
    ys = [y for y, _ in REACTIONS]
    ds = [(z[0] - y[0], z[1] - y[1]) for y, z in REACTIONS]
    scores = [dot(y, u) for y in ys]
    projections = [dot(d, u) for d in ds]
    active = [i for i, q in enumerate(projections) if q != 0]
    active_max = max((scores[i] for i in active), default=None)
    active_maximizers = [i for i in active if scores[i] == active_max] if active_max is not None else []
    violations = [
        i for i in active
        if projections[i] > 0 and scores[i] == active_max
    ]
    endotactic = not violations
    global_max = max(scores)
    global_maximizers = [i for i, score in enumerate(scores) if score == global_max]
    maximal_decreasing = [
        i for i in range(len(REACTIONS))
        if projections[i] < 0 and scores[i] == global_max
    ]
    strongly_endotactic = endotactic and bool(maximal_decreasing)
    return {
        "u": list(u),
        "scores": scores,
        "projections": projections,
        "active_reactions_1based": [i + 1 for i in active],
        "active_max_score": active_max,
        "active_maximizers_1based": [i + 1 for i in active_maximizers],
        "active_maximizer_projections": [projections[i] for i in active_maximizers],
        "violating_reactions_1based": [i + 1 for i in violations],
        "global_max_score": global_max,
        "global_maximizers_1based": [i + 1 for i in global_maximizers],
        "maximal_decreasing_reactions_1based": [i + 1 for i in maximal_decreasing],
        "endotactic": endotactic,
        "strongly_endotactic": strongly_endotactic,
    }


def all_strata():
    rays = critical_rays()
    results = []
    # Every boundary ray is evaluated separately, preserving all zero and tie cases.
    for ray in rays:
        row = exact_status(ray)
        row["stratum"] = "boundary_ray"
        results.append(row)
    # The sum of two adjacent ray generators lies strictly inside their cone;
    # all such cones have angle < pi because every critical line contributes
    # both antipodal rays. The arrangement signs are constant in each cone.
    for i, a in enumerate(rays):
        b = rays[(i + 1) % len(rays)]
        u = (a[0] + b[0], a[1] + b[1])
        if u == (0, 0):
            raise AssertionError("adjacent rays unexpectedly antipodal")
        row = exact_status(u)
        row["stratum"] = "open_sector"
        row["boundary_rays"] = [list(a), list(b)]
        results.append(row)
    return rays, results


def main():
    rays, results = all_strata()
    summary = {
        "network": [
            {"source": list(y), "product": list(z), "delta": [z[0] - y[0], z[1] - y[1]]}
            for y, z in REACTIONS
        ],
        "critical_line_count": len(rays) // 2,
        "critical_rays_ccw_from_positive_x": [list(r) for r in rays],
        "boundary_ray_count": len(rays),
        "open_sector_count": len(rays),
        "all_directions_endotactic": all(r["endotactic"] for r in results),
        "all_directions_strongly_endotactic": all(r["strongly_endotactic"] for r in results),
        "first_endotactic_failure": next((r for r in results if not r["endotactic"]), None),
        "first_strong_failure": next((r for r in results if not r["strongly_endotactic"]), None),
        "strata": results,
        "method": (
            "Exact finite arrangement: all reaction-projection zero lines and all pairwise "
            "source-score tie lines; evaluate every ray and an integer interior vector in "
            "each open sector. Sign/order data are constant in every open sector."
        ),
    }
    out = ROOT / "exact_results.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    cert = [
        "Exact directional certificate. Reaction indices are the listed network order.",
        "Each row gives u; the active-source maximizers and their outgoing projections;",
        "then the all-source maximizers and indices among them with negative projection.",
        "Nonpositive active-max projections prove no violation; a nonempty final set proves strong u-endotacticity.",
        "Critical rays are listed below in counterclockwise order; adjacent rays bound the open sectors.",
        "Critical rays: " + ", ".join(str(tuple(v)) for v in rays),
        "",
        "stratum | u | active-max sources: q_i | all-source maxima | max-source decreasing reactions",
    ]
    for row in results:
        kind = "ray" if row["stratum"] == "boundary_ray" else "sector"
        cert.append(
            f"{kind} | {tuple(row['u'])} | "
            f"{list(zip(row['active_maximizers_1based'], row['active_maximizer_projections']))} | "
            f"{row['global_maximizers_1based']} | {row['maximal_decreasing_reactions_1based']}"
        )
    (ROOT / "directional_certificate.txt").write_text("\n".join(cert) + "\n")
    print(json.dumps({k: summary[k] for k in (
        "critical_line_count", "boundary_ray_count", "open_sector_count",
        "all_directions_endotactic", "all_directions_strongly_endotactic",
        "first_endotactic_failure", "first_strong_failure"
    )}, indent=2))


if __name__ == "__main__":
    main()
