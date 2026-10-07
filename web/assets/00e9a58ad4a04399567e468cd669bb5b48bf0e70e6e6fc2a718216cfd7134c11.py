#!/usr/bin/env python3
"""Exact corner algebra for the graph certificate's concrete example.

No stochastic trajectory, rare event estimate or continuum simulation is used.
The global probability theorem is the analytic stopped-generator proof.
"""

from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json


FACETS = (
    ((F(1), F(0)), F(-1)),
    ((F(-1), F(0)), F(3)),
    ((F(0), F(1)), F(-1)),
    ((F(0), F(-1)), F(3)),
    ((F(1), F(1)), F(-3)),
)


def gap(constraint, point):
    normal, offset = constraint
    return sum(a * b for a, b in zip(normal, point)) + offset


def vertices(constraints):
    points = set()
    for (n1, b1), (n2, b2) in combinations(constraints, 2):
        determinant = n1[0] * n2[1] - n1[1] * n2[0]
        if not determinant:
            continue
        x = (-b1 * n2[1] + b2 * n1[1]) / determinant
        y = (-n1[0] * b2 + n2[0] * b1) / determinant
        point = (x, y)
        if all(gap(c, point) >= 0 for c in constraints):
            points.add(point)
    return sorted(points)


def frac(value):
    return str(value)


def check():
    poly_vertices = vertices(FACETS)
    assert poly_vertices == [
        (F(1), F(2)), (F(1), F(3)), (F(2), F(1)),
        (F(3), F(1)), (F(3), F(3)),
    ]
    width = F(1, 4)
    summaries = []
    total_corners = 0
    for facet in FACETS:
        normal, offset = facet
        # The extra inequality is eta-g_i >= 0.
        collar = FACETS + ((tuple(-a for a in normal), width - offset),)
        collar_vertices = vertices(collar)
        values = []
        for local, neighbor, diffusion in product(
            collar_vertices, poly_vertices, (F(0), F(1))
        ):
            reaction = tuple(F(2) - x for x in local)
            drift = sum(n * f for n, f in zip(normal, reaction))
            drift += diffusion * (gap(facet, neighbor) - gap(facet, local))
            values.append(drift)
        assert min(values) == F(1, 2)
        total_corners += len(values)

        # Birth/death intensities at one site are 2,x,2,y. An incident
        # species hop has two scaled intensities D*x_j and D*y_j.
        squared_bounds = []
        affected_rate_bounds = []
        for local, neighbor, diffusion in product(
            poly_vertices, poly_vertices, (F(0), F(1))
        ):
            variance_rate = sum(
                n * n * (F(2) + x + diffusion * (x + y))
                for n, x, y in zip(normal, local, neighbor)
            )
            squared_bounds.append(variance_rate)
            affected_rate_bounds.append(
                F(4) + sum(local)
                + diffusion * (sum(local) + sum(neighbor))
            )
        expected_q = F(22) if normal == (F(1), F(1)) else F(11)
        assert max(squared_bounds) == expected_q
        assert max(affected_rate_bounds) == F(22)
        summaries.append({
            "normal": [frac(n) for n in normal],
            "offset": frac(offset),
            "collar_width": frac(width),
            "collar_vertices": [[frac(c) for c in p] for p in collar_vertices],
            "corner_checks": len(values),
            "minimum_total_drift": frac(min(values)),
            "maximum_projected_variance_rate": frac(max(squared_bounds)),
            "maximum_site_affected_rate": frac(max(affected_rate_bounds)),
            "theta_valid_formula": f"1/({int(expected_q)}*e)",
        })

    epsilon = F(1, 1000)
    first_initial = (F(1) + epsilon, F(2))
    second_initial = (F(2), F(1) + epsilon)
    initial_gaps = [
        [gap(c, p) for c in FACETS]
        for p in (first_initial, second_initial)
    ]
    assert min(g for row in initial_gaps for g in row) == epsilon
    u = F(99, 100)
    # Exact solution for common reaction drifts 2-x_j with different
    # exchange coefficients D_A=1 and D_B=3.
    first_x = F(2) - (F(1) - epsilon) * (u + u ** 3) / 2
    first_y = F(2) - (F(1) - epsilon) * u / 2 + (F(1) - epsilon) * u ** 7 / 2
    sum_gap = first_x + first_y - 3
    claimed_gap = F(1) - (F(1) - epsilon) * (u + u ** 3 / 2 - u ** 7 / 2)
    assert sum_gap == claimed_gap < 0
    assert F(1) < first_x < F(3) and F(1) < first_y < F(3)
    total_rate = F(2) * F(10) + F(2) * F(1) * F(2) * F(3) * F(1)
    assert total_rate == 32
    return {
        "classification": "exact rational endpoint algebra, not rare-event simulation",
        "common_diffusion": {
            "N": 2,
            "edges": 1,
            "maximum_degree": 1,
            "D_max": 1,
            "coordinate_bound_R": 3,
            "total_collar_corner_checks": total_corners,
            "site_affected_scaled_rate_bound": 22,
            "global_scaled_rate_bound": frac(total_rate),
            "minimum_reliability_exponent_formula": "1/(88*e)",
            "facets": summaries,
        },
        "unequal_diffusion_counterexample": {
            "epsilon": frac(epsilon),
            "D_A": 1,
            "D_B": 3,
            "initial_gaps": [[frac(g) for g in row] for row in initial_gaps],
            "evaluation_time": "-log(99/100)",
            "first_site_x": frac(first_x),
            "first_site_y": frac(first_y),
            "first_site_sum_facet_gap": frac(sum_gap),
            "first_site_sum_facet_gap_decimal": float(sum_gap),
            "verified_negative": True,
        },
    }


if __name__ == "__main__":
    result = check()
    path = Path(__file__).with_name("chemical_graph_checks.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "output": str(path),
        "collar_corner_checks": result["common_diffusion"]["total_collar_corner_checks"],
        "unequal_diffusion_gap": result["unequal_diffusion_counterexample"]["first_site_sum_facet_gap"],
        "passed": True,
    }))
