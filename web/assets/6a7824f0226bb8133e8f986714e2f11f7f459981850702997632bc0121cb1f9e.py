#!/usr/bin/env python3
"""Exact all-direction endotacticity check for the proposed order-6 network."""

from __future__ import annotations

from functools import cmp_to_key
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REACTIONS = [
    ((0, 0), (2, 0)),
    ((2, 0), (4, 1)),
    ((4, 1), (4, 2)),
    ((4, 2), (3, 0)),
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


def line_direction(form):
    """Return a primitive ray generator for the line form·u=0."""
    d = primitive((-form[1], form[0]))
    return d if (d[0] > 0 or (d[0] == 0 and d[1] > 0)) else (-d[0], -d[1])


def half(v):
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1


def ray_cmp(p, q):
    hp, hq = half(p), half(q)
    if hp != hq:
        return -1 if hp < hq else 1
    c = cross(p, q)
    if c:
        return -1 if c > 0 else 1
    return 0


def sources():
    return list(dict.fromkeys(src for src, _ in REACTIONS))


def critical_rays():
    srcs = sources()
    deltas = [(dst[0] - src[0], dst[1] - src[1]) for src, dst in REACTIONS]
    directions = {line_direction(delta) for delta in deltas}
    for i, p in enumerate(srcs):
        for q in srcs[i + 1:]:
            directions.add(line_direction((p[0] - q[0], p[1] - q[1])))
    return sorted({v for d in directions for v in (d, (-d[0], -d[1]))}, key=cmp_to_key(ray_cmp))


def exact_status(u):
    srcs = sources()
    scores = {src: dot(src, u) for src in srcs}
    projections = [dot((dst[0] - src[0], dst[1] - src[1]), u)
                   for src, dst in REACTIONS]
    active_reactions = [i for i, q in enumerate(projections) if q != 0]
    active_sources = list(dict.fromkeys(REACTIONS[i][0] for i in active_reactions))
    active_max = max(scores[src] for src in active_sources) if active_sources else None
    active_max_sources = [src for src in active_sources if scores[src] == active_max]
    active_max_ids = [i for i in active_reactions if REACTIONS[i][0] in active_max_sources]
    violations = [i for i in active_max_ids if projections[i] > 0]
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
            [i + 1, list(REACTIONS[i][0]), projections[i]] for i in active_max_ids
        ],
        "violating_reactions_1based": [i + 1 for i in violations],
        "global_max_sources": [list(src) for src in global_max_sources],
        "maximal_decreasing_reactions_1based": [i + 1 for i in decreasing_at_global_max],
        "endotactic": endotactic,
        "strongly_endotactic": endotactic and bool(decreasing_at_global_max),
    }


def analyze():
    rays = critical_rays()
    rows = []
    for ray in rays:
        row = exact_status(ray)
        row["stratum"] = "boundary_ray"
        rows.append(row)
    for i, p in enumerate(rays):
        q = rays[(i + 1) % len(rays)]
        u = (p[0] + q[0], p[1] + q[1])
        if u == (0, 0):
            raise AssertionError("adjacent rays unexpectedly antipodal")
        row = exact_status(u)
        row["stratum"] = "open_sector"
        row["boundary_rays"] = [list(p), list(q)]
        rows.append(row)
    return rays, rows


def main():
    rays, rows = analyze()
    result = {
        "network": [
            {"reaction_1based": i + 1, "source": list(src), "product": list(dst),
             "delta": [dst[0] - src[0], dst[1] - src[1]]}
            for i, (src, dst) in enumerate(REACTIONS)
        ],
        "unique_source_complexes": [list(src) for src in sources()],
        "critical_line_count": len(rays) // 2,
        "critical_rays_ccw_from_positive_x": [list(v) for v in rays],
        "boundary_ray_count": len(rays),
        "open_sector_count": len(rays),
        "all_nonzero_directions_endotactic": all(r["endotactic"] for r in rows),
        "all_nonzero_directions_strongly_endotactic": all(r["strongly_endotactic"] for r in rows),
        "failures": [r for r in rows if not r["endotactic"]],
        "strong_failures": [r for r in rows if not r["strongly_endotactic"]],
        "strata": rows,
        "method": (
            "Integer arrangement of all reaction-projection zero lines and pairwise source-score "
            "tie lines. Each oriented boundary ray and an integer interior vector in each open "
            "sector are evaluated; signs and score order are constant within each sector."
        ),
    }
    (ROOT / "exact_results.json").write_text(json.dumps(result, indent=2) + "\n")
    cert = [
        "Exact all-direction certificate for the order-6 network.",
        "Reaction indices follow check_order6.py; u=(a,b), source score s_y=y·u, q=(y'-y)·u.",
        "Each row gives stratum | u | active-max reaction records (index, source, q) | global-max sources | decreasing reactions at global maxima.",
        "No positive q occurs at an active-source maximum, and the final set is nonempty in every row.",
        "Critical boundary rays CCW from +a: " + ", ".join(str(tuple(v)) for v in rays),
        "Critical lines: a=0, 2a+b=0, b=0, a+2b=0, 4a+b=0, a+b=0.",
        "",
    ]
    for row in rows:
        kind = "ray" if row["stratum"] == "boundary_ray" else "sector"
        cert.append(
            f"{kind} | {tuple(row['u'])} | {row['active_max_reaction_records']} | "
            f"{row['global_max_sources']} | {row['maximal_decreasing_reactions_1based']}"
        )
    (ROOT / "directional_certificate.txt").write_text("\n".join(cert) + "\n")
    print(json.dumps({
        "endotactic": result["all_nonzero_directions_endotactic"],
        "strongly_endotactic": result["all_nonzero_directions_strongly_endotactic"],
        "critical_lines": result["critical_line_count"],
        "boundary_rays": result["boundary_ray_count"],
        "open_sectors": result["open_sector_count"],
        "endotactic_failure_count": len(result["failures"]),
        "strong_failure_count": len(result["strong_failures"]),
    }, indent=2))


if __name__ == "__main__":
    main()
