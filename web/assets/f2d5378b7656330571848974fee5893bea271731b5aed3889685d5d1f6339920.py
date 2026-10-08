#!/usr/bin/env python3
"""Exact all-direction check for the proposed order-7 network.

The implementation uses integer dot products and an exact arrangement of all
reaction-projection zero lines and source-score tie lines. It also checks the
same chain with the added branch omitted to expose the repaired face.
"""

from __future__ import annotations

from functools import cmp_to_key
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCHED = [
    ((0, 0), (2, 0)),
    ((2, 0), (4, 1)),
    ((4, 1), (5, 2)),
    ((5, 2), (3, 0)),
    ((4, 1), (4, 2)),
]
CHAIN = BRANCHED[:4]


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
    """Primitive direction vector spanning the line form·u=0."""
    d = primitive((-form[1], form[0]))
    return d if (d[0] > 0 or (d[0] == 0 and d[1] > 0)) else (-d[0], -d[1])


def half(v):
    return 0 if v[1] > 0 or (v[1] == 0 and v[0] > 0) else 1


def ray_cmp(p, q):
    hp, hq = half(p), half(q)
    if hp != hq:
        return -1 if hp < hq else 1
    c = cross(p, q)
    if c:
        return -1 if c > 0 else 1
    return 0


def sources_of(reactions):
    return list(dict.fromkeys(src for src, _ in reactions))


def critical_rays(reactions):
    sources = sources_of(reactions)
    deltas = [(dst[0] - src[0], dst[1] - src[1]) for src, dst in reactions]
    lines = {line_direction(delta) for delta in deltas}
    for i, p in enumerate(sources):
        for q in sources[i + 1:]:
            lines.add(line_direction((p[0] - q[0], p[1] - q[1])))
    return sorted({v for d in lines for v in (d, (-d[0], -d[1]))}, key=cmp_to_key(ray_cmp))


def exact_status(reactions, u):
    sources = sources_of(reactions)
    source_scores = {src: dot(src, u) for src in sources}
    projections = [dot((dst[0] - src[0], dst[1] - src[1]), u)
                   for src, dst in reactions]
    active_reactions = [i for i, q in enumerate(projections) if q != 0]
    active_sources = list(dict.fromkeys(reactions[i][0] for i in active_reactions))
    active_max = max(source_scores[src] for src in active_sources) if active_sources else None
    active_max_sources = [src for src in active_sources if source_scores[src] == active_max]
    active_max_ids = [i for i in active_reactions if reactions[i][0] in active_max_sources]
    violators = [i for i in active_max_ids if projections[i] > 0]
    global_max = max(source_scores.values())
    global_max_sources = [src for src in sources if source_scores[src] == global_max]
    maximal_decreasing = [i for i, ((src, _), q) in enumerate(zip(reactions, projections))
                          if src in global_max_sources and q < 0]
    endotactic = not violators
    return {
        "u": list(u),
        "source_scores": [[list(src), source_scores[src]] for src in sources],
        "reaction_projections": projections,
        "active_reactions_1based": [i + 1 for i in active_reactions],
        "active_max_sources": [list(src) for src in active_max_sources],
        "active_max_reactions_1based": [i + 1 for i in active_max_ids],
        "active_max_projections": [projections[i] for i in active_max_ids],
        "active_max_reaction_records": [
            [i + 1, list(reactions[i][0]), projections[i]] for i in active_max_ids
        ],
        "violating_reactions_1based": [i + 1 for i in violators],
        "global_max_sources": [list(src) for src in global_max_sources],
        "maximal_decreasing_reactions_1based": [i + 1 for i in maximal_decreasing],
        "endotactic": endotactic,
        "strongly_endotactic": endotactic and bool(maximal_decreasing),
    }


def analyze(reactions):
    rays = critical_rays(reactions)
    rows = []
    for ray in rays:
        row = exact_status(reactions, ray)
        row["stratum"] = "boundary_ray"
        rows.append(row)
    for i, p in enumerate(rays):
        q = rays[(i + 1) % len(rays)]
        u = (p[0] + q[0], p[1] + q[1])
        if u == (0, 0):
            raise AssertionError("adjacent boundary rays are antipodal")
        row = exact_status(reactions, u)
        row["stratum"] = "open_sector"
        row["boundary_rays"] = [list(p), list(q)]
        rows.append(row)
    return rays, rows


def reaction_payload(reactions):
    return [{"reaction_1based": i + 1, "source": list(src), "product": list(dst),
             "delta": [dst[0] - src[0], dst[1] - src[1]]}
            for i, (src, dst) in enumerate(reactions)]


def summary(reactions, rays, rows):
    return {
        "reactions": reaction_payload(reactions),
        "unique_source_complexes": [list(src) for src in sources_of(reactions)],
        "critical_line_count": len(rays) // 2,
        "critical_rays_ccw_from_positive_x": [list(v) for v in rays],
        "boundary_ray_count": len(rays),
        "open_sector_count": len(rays),
        "all_nonzero_directions_endotactic": all(r["endotactic"] for r in rows),
        "all_nonzero_directions_strongly_endotactic": all(r["strongly_endotactic"] for r in rows),
        "failures": [r for r in rows if not r["endotactic"]],
        "strong_failures": [r for r in rows if not r["strongly_endotactic"]],
        "strata": rows,
    }


def certificate_text(rays, rows, base_witness):
    out = [
        "Exact certificate for the order-7 network; reactions are listed in check_order7.py.",
        "u=(a,b), source score s_y=y·u, reaction projection q=(y'-y)·u.",
        "At each ray and sector, all active-source maximizers have q<=0; the final column is",
        "the set of decreasing reactions whose source is globally maximal. Nonempty means strong.",
        "Critical boundary rays CCW from +a: " + ", ".join(str(tuple(r)) for r in rays),
        "The seven critical lines are a=0, 4a+b=0, 5a+2b=0, 2a+b=0, 3a+2b=0, a+b=0, b=0.",
        "Rows below give stratum | u | active-max records (reaction, source, q) | global-max sources | decreasing global-max reactions.",
        "",
    ]
    for row in rows:
        kind = "ray" if row["stratum"] == "boundary_ray" else "sector"
        out.append(
            f"{kind} | {tuple(row['u'])} | "
            f"{row['active_max_reaction_records']} | "
            f"{row['global_max_sources']} | {row['maximal_decreasing_reactions_1based']}"
        )
    out += [
        "",
        "Unbranched-chain witness on the exceptional ray u=(1,-1):",
        f"scores={base_witness['source_scores']}; projections={base_witness['reaction_projections']};",
        f"active-max sources={base_witness['active_max_sources']}; "
        f"violating reactions={base_witness['violating_reactions_1based']}; "
        f"global-max sources={base_witness['global_max_sources']}; "
        f"decreasing reactions at global maxima={base_witness['maximal_decreasing_reactions_1based']}.",
    ]
    return "\n".join(out) + "\n"


def main():
    rays, rows = analyze(BRANCHED)
    chain_rays, chain_rows = analyze(CHAIN)
    base_witness = exact_status(CHAIN, (1, -1))
    branched_face = exact_status(BRANCHED, (1, -1))
    result = {
        "branched_network": summary(BRANCHED, rays, rows),
        "chain_without_added_branch": summary(CHAIN, chain_rays, chain_rows),
        "exceptional_face_comparison_u_1_minus1": {
            "chain_without_branch": base_witness,
            "with_added_branch": branched_face,
        },
        "proof_method": (
            "Exact central arrangement of every reaction-projection zero line and every "
            "pairwise source-score tie line. Evaluate every oriented boundary ray and an "
            "integer interior vector in each open sector; all signs and score orderings "
            "are constant within each sector."
        ),
    }
    (ROOT / "exact_results.json").write_text(json.dumps(result, indent=2) + "\n")
    (ROOT / "directional_certificate.txt").write_text(certificate_text(rays, rows, base_witness))
    print(json.dumps({
        "branched_endotactic": result["branched_network"]["all_nonzero_directions_endotactic"],
        "branched_strongly_endotactic": result["branched_network"]["all_nonzero_directions_strongly_endotactic"],
        "branched_critical_lines": result["branched_network"]["critical_line_count"],
        "branched_rays": result["branched_network"]["boundary_ray_count"],
        "branched_sectors": result["branched_network"]["open_sector_count"],
        "chain_without_branch_endotactic": result["chain_without_added_branch"]["all_nonzero_directions_endotactic"],
        "chain_without_branch_strong": result["chain_without_added_branch"]["all_nonzero_directions_strongly_endotactic"],
        "chain_failure_count": len(result["chain_without_added_branch"]["failures"]),
        "face_u_1_minus1_chain_violations": base_witness["violating_reactions_1based"],
        "face_u_1_minus1_branched_violations": branched_face["violating_reactions_1based"],
        "face_u_1_minus1_branched_maximal_decreasing": branched_face["maximal_decreasing_reactions_1based"],
    }, indent=2))


if __name__ == "__main__":
    main()
