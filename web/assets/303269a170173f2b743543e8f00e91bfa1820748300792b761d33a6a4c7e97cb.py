#!/usr/bin/env python3
"""Exact all-direction endotacticity check for the frozen order-5 network."""

from __future__ import annotations

from functools import cmp_to_key
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REACTIONS = [
    ((0, 0), (2, 0)),
    ((2, 0), (3, 1)),
    ((3, 1), (3, 2)),
    ((3, 2), (3, 0)),
    ((3, 2), (2, 0)),
]


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def primitive(v):
    g = gcd(abs(v[0]), abs(v[1]))
    if not g:
        raise ValueError("zero vector")
    return (v[0] // g, v[1] // g)


def direction_for_line(form):
    """Return a canonical primitive direction spanning form·u=0."""
    d = primitive((-form[1], form[0]))
    if d[0] < 0 or (d[0] == 0 and d[1] < 0):
        d = (-d[0], -d[1])
    return d


def half(v):
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1


def polar_cmp(p, q):
    """Exact CCW order from +x, using only half-plane and cross product."""
    hp, hq = half(p), half(q)
    if hp != hq:
        return -1 if hp < hq else 1
    determinant = cross(p, q)
    if determinant:
        return -1 if determinant > 0 else 1
    return 0


def unique_sources():
    return list(dict.fromkeys(src for src, _ in REACTIONS))


def arrangement_rays():
    """Include every reaction-zero and every source-score-tie line."""
    srcs = unique_sources()
    line_directions = set()
    for src, dst in REACTIONS:
        delta = (dst[0] - src[0], dst[1] - src[1])
        line_directions.add(direction_for_line(delta))
    for i, src in enumerate(srcs):
        for other in srcs[i + 1:]:
            form = (src[0] - other[0], src[1] - other[1])
            line_directions.add(direction_for_line(form))
    rays = {r for d in line_directions for r in (d, (-d[0], -d[1]))}
    return sorted(rays, key=cmp_to_key(polar_cmp))


def evaluate(u):
    srcs = unique_sources()
    scores = {src: dot(src, u) for src in srcs}
    projections = [dot((dst[0] - src[0], dst[1] - src[1]), u)
                   for src, dst in REACTIONS]

    active_reactions = [i for i, q in enumerate(projections) if q != 0]
    active_sources = list(dict.fromkeys(REACTIONS[i][0] for i in active_reactions))
    active_max = max((scores[src] for src in active_sources), default=None)
    active_max_sources = [src for src in active_sources if scores[src] == active_max]
    active_max_reactions = [
        i for i in active_reactions if REACTIONS[i][0] in active_max_sources
    ]
    violations = [i for i in active_max_reactions if projections[i] > 0]

    global_max = max(scores.values())
    global_max_sources = [src for src in srcs if scores[src] == global_max]
    decreasing_at_global_max = [
        i for i, ((src, _), q) in enumerate(zip(REACTIONS, projections))
        if src in global_max_sources and q < 0
    ]
    endotactic = not violations
    return {
        "u": list(u),
        "source_scores": [[list(src), scores[src]] for src in srcs],
        "reaction_projections": projections,
        "active_reactions_1based": [i + 1 for i in active_reactions],
        "active_max_sources": [list(src) for src in active_max_sources],
        "active_max_reaction_records": [
            [i + 1, list(REACTIONS[i][0]), projections[i]] for i in active_max_reactions
        ],
        "violating_reactions_1based": [i + 1 for i in violations],
        "global_max_sources": [list(src) for src in global_max_sources],
        "maximal_decreasing_reactions_1based": [i + 1 for i in decreasing_at_global_max],
        "endotactic": endotactic,
        "strongly_endotactic": endotactic and bool(decreasing_at_global_max),
    }


def exact_strata():
    rays = arrangement_rays()
    rows = []
    # Each ray is an exceptional boundary stratum and is evaluated directly.
    for ray in rays:
        row = evaluate(ray)
        row["stratum"] = "boundary_ray"
        rows.append(row)
    # Adjacent rays make cones of angle < pi: the arrangement contains every
    # antipode, and there are multiple distinct critical lines. Their integer
    # sum is strictly inside each cone; all relevant signs/orderings are fixed there.
    for index, left in enumerate(rays):
        right = rays[(index + 1) % len(rays)]
        u = (left[0] + right[0], left[1] + right[1])
        if u == (0, 0):
            raise AssertionError("adjacent boundary rays are antipodal")
        row = evaluate(u)
        row["stratum"] = "open_sector"
        row["boundary_rays"] = [list(left), list(right)]
        rows.append(row)
    return rays, rows


def main():
    rays, rows = exact_strata()
    result = {
        "network": [
            {"reaction_1based": i + 1, "source": list(src), "product": list(dst),
             "delta": [dst[0] - src[0], dst[1] - src[1]]}
            for i, (src, dst) in enumerate(REACTIONS)
        ],
        "unique_source_complexes": [list(src) for src in unique_sources()],
        "max_source_molecularity": max(sum(src) for src in unique_sources()),
        "critical_line_count": len(rays) // 2,
        "critical_rays_ccw_from_positive_x": [list(v) for v in rays],
        "boundary_ray_count": len(rays),
        "open_sector_count": len(rays),
        "all_nonzero_directions_endotactic": all(row["endotactic"] for row in rows),
        "all_nonzero_directions_strongly_endotactic": all(row["strongly_endotactic"] for row in rows),
        "endotactic_failures": [row for row in rows if not row["endotactic"]],
        "strong_failures": [row for row in rows if not row["strongly_endotactic"]],
        "strata": rows,
        "method": (
            "Exact central arrangement: all reaction projection zero lines and all pairwise "
            "source-score tie lines are included. Every boundary ray and an integer vector "
            "inside every open sector are evaluated. Signs and score order are constant "
            "within each open sector."
        ),
    }
    (ROOT / "exact_results.json").write_text(json.dumps(result, indent=2) + "\n")

    certificate = [
        "Exact directional certificate for the frozen order-5 network.",
        "Indices follow check_order5.py. For u=(a,b), source score is s_y=y·u and q=(y'-y)·u.",
        "Each row: stratum | u | active-max records (reaction index, source, q) | global-max sources | decreasing reactions at a global maximum.",
        "Every active-max record has q<0; every last-column set is nonempty.",
        "Critical rays, in exact CCW order from +a: " + ", ".join(str(tuple(v)) for v in rays),
        "Critical lines: a=0, 3a+b=0, 3a+2b=0, a+b=0, a+2b=0, b=0.",
        "",
    ]
    for row in rows:
        kind = "ray" if row["stratum"] == "boundary_ray" else "sector"
        certificate.append(
            f"{kind} | {tuple(row['u'])} | {row['active_max_reaction_records']} | "
            f"{row['global_max_sources']} | {row['maximal_decreasing_reactions_1based']}"
        )
    (ROOT / "directional_certificate.txt").write_text("\n".join(certificate) + "\n")

    print(json.dumps({
        "max_source_molecularity": result["max_source_molecularity"],
        "critical_lines": result["critical_line_count"],
        "boundary_rays": result["boundary_ray_count"],
        "open_sectors": result["open_sector_count"],
        "all_directions_endotactic": result["all_nonzero_directions_endotactic"],
        "all_directions_strongly_endotactic": result["all_nonzero_directions_strongly_endotactic"],
        "endotactic_failure_count": len(result["endotactic_failures"]),
        "strong_failure_count": len(result["strong_failures"]),
    }, indent=2))


if __name__ == "__main__":
    main()
