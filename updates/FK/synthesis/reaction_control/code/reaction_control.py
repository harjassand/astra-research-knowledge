#!/usr/bin/env python3
"""Dimensionless, exact-geometry falsification for a two-mode glide schedule.

This is a mathematical witness, not a fit to ZnS (or any other material).
All geometry is in a normalized glide-coordinate plane.  Burgers-vector checks
are exact in units of the lattice constant a.  No source model is executed.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path
from typing import Sequence

Vec = tuple[F, F]
Vec3 = tuple[F, F, F]


def dot(x: Sequence[F], y: Sequence[F]) -> F:
    return sum((a * b for a, b in zip(x, y)), F(0))


def sub(x: Sequence[F], y: Sequence[F]) -> tuple[F, ...]:
    return tuple(a - b for a, b in zip(x, y))


def add(x: Sequence[F], y: Sequence[F]) -> tuple[F, ...]:
    return tuple(a + b for a, b in zip(x, y))


def scale(t: F, x: Sequence[F]) -> tuple[F, ...]:
    return tuple(t * a for a in x)


def segment_distance_sq(p0: Vec, p1: Vec, c: Vec) -> F:
    d = sub(p1, p0)
    c0 = sub(c, p0)
    t = dot(c0, d) / dot(d, d)
    t = max(F(0), min(F(1), t))
    closest = add(p0, scale(t, d))
    delta = sub(c, closest)
    return dot(delta, delta)


def line_distance_sq_to_target(m: F) -> F:
    # Ray y=m x through the origin; target center is (3,2).
    return (3 * m - 2) ** 2 / (1 + m * m)


def burgertopology() -> dict[str, object]:
    # Zinc-blende/FCC {111} slip plane n=(1,-1,-1).  Vectors are in units a/2.
    n: Vec3 = (F(1), F(-1), F(-1))
    b_a: Vec3 = (F(1), F(1), F(0))
    b_c: Vec3 = (F(-1), F(0), F(-1))
    b_r: Vec3 = (F(0), F(1), F(-1))
    b_target_partner = tuple(-x for x in b_a)

    assert dot(n, b_a) == dot(n, b_c) == dot(n, b_r) == 0
    assert add(b_a, b_target_partner) == (F(0), F(0), F(0))
    assert add(b_a, b_c) == b_r
    # Multiply by (a/2)^2: each of these squared norms is 2*(a/2)^2=a^2/2.
    assert dot(b_a, b_a) == dot(b_c, b_c) == dot(b_r, b_r) == F(2)

    return {
        "slip_plane_normal": [1, -1, -1],
        "vectors_in_units_of_a_over_2": {
            "lead": [1, 1, 0],
            "target_partner": [-1, -1, 0],
            "competing_partner": [-1, 0, -1],
            "residual_product": [0, 1, -1],
        },
        "target_reaction": "(a/2)[110] + (a/2)[-1 -1 0] -> 0",
        "competitor_reaction": "(a/2)[110] + (a/2)[-1 0 -1] -> (a/2)[0 1 -1]",
        "all_vectors_lie_in_same_111_plane": True,
        "target_burgers_sum_zero": True,
        "competitor_burgers_sum_nonzero": True,
        "frank_b2_check": "|b_residual|^2=a^2/2 < |b_lead|^2+|b_competitor|^2=a^2; line/core/fault energetics still required",
    }


def main() -> None:
    # The sole control is a shared normalized illumination level phi in [0,1].
    # Illustrative coupled response: dark=(2,1), full light=(1,1),
    # constant phi=(2-phi,1).  These are unitless witness vectors, not material
    # parameters or a fit to the ZnS measurements.
    v_dark: Vec = (F(2), F(1))
    v_light: Vec = (F(1), F(1))
    determinant = v_dark[0] * v_light[1] - v_dark[1] * v_light[0]
    assert determinant == 1

    target_center: Vec = (F(3), F(2))
    sink_center: Vec = (F(2), F(4, 3))
    target_radius = F(1, 5)
    sink_radius = F(21, 100)

    # Dark for one time unit, then full light for one: equal total dose 1.
    dark_then_light_path: tuple[Vec, ...] = (
        (F(0), F(0)),
        (F(2), F(1)),
        target_center,
    )
    switched_clearance_sq = min(
        segment_distance_sq(p, q, sink_center)
        for p, q in zip(dark_then_light_path, dark_then_light_path[1:])
    )
    assert switched_clearance_sq == F(1, 18)
    assert switched_clearance_sq > sink_radius * sink_radius
    assert dot(sub(dark_then_light_path[-1], target_center), sub(dark_then_light_path[-1], target_center)) == 0

    # Reverse pulse order has the same dose and duration, but hits the sink.
    light_then_dark_path: tuple[Vec, ...] = (
        (F(0), F(0)),
        (F(1), F(1)),
        target_center,
    )
    reverse_clearance_sq = min(
        segment_distance_sq(p, q, sink_center)
        for p, q in zip(light_then_dark_path, light_then_dark_path[1:])
    )
    assert reverse_clearance_sq == F(1, 45)
    assert reverse_clearance_sq < sink_radius * sink_radius

    # Exact universal obstruction for every constant phi in [0,1].
    # A ray meeting the target disk has d(line,T)<=1/5.  Since 1/2<=m<=1,
    # sqrt(1+m^2)<3/2, hence 17/30<m<23/30.  At x=2 its vertical distance
    # from the sink center is then <1/5<21/100, before it reaches the target.
    constant_target_slope_interval = (F(17, 30), F(23, 30))
    max_sink_center_offset_sq = F(1, 25)
    assert max_sink_center_offset_sq < sink_radius * sink_radius
    assert F(2, 1) < F(14, 5)  # x=2 is before every point of target disk.

    # Endpoint/line checks for the two constant extremes and dose-matched mean.
    dark_m = F(1, 2)
    light_m = F(1)
    mean_dose_m = F(2, 3)  # phi=1/2 over two time units reaches (3,2).
    assert line_distance_sq_to_target(dark_m) == F(1, 5) > target_radius**2
    assert line_distance_sq_to_target(light_m) == F(1, 2) > target_radius**2
    assert line_distance_sq_to_target(mean_dose_m) == 0
    assert line_distance_sq_to_target(mean_dose_m) < F(1, 25)  # it crosses sink.

    # Falsify the steering claim if the same optical input only rescales both
    # species.  Such controls preserve the dark ray, so switching cannot help.
    proportional_light: Vec = (F(1), F(1, 2))
    proportional_det = v_dark[0] * proportional_light[1] - v_dark[1] * proportional_light[0]
    assert proportional_det == 0
    assert proportional_light[1] / proportional_light[0] == v_dark[1] / v_dark[0]

    result = {
        "scope": "exact dimensionless geometric witness only; no material prediction",
        "control": "one global normalized flux phi in [0,1], dose integral phi dt <= 1",
        "coupled_velocity_witness": {
            "dark": [2, 1],
            "full_light": [1, 1],
            "constant_phi": "(2-phi,1)",
            "determinant_dark_light": str(determinant),
        },
        "target": {"center": [3, 2], "radius": str(target_radius), "meaning": "opposite-Burgers annihilation event"},
        "failure_sink": {"center": [2, "4/3"], "radius": str(sink_radius), "meaning": "nonzero-Burgers residual/junction event"},
        "dark_then_light_equal_dose": {
            "path_vertices": [[0, 0], [2, 1], [3, 2]],
            "minimum_squared_distance_to_failure_sink": str(switched_clearance_sq),
            "outcome": "reaches target without entering failure sink",
        },
        "light_then_dark_equal_dose": {
            "path_vertices": [[0, 0], [1, 1], [3, 2]],
            "minimum_squared_distance_to_failure_sink": str(reverse_clearance_sq),
            "outcome": "failure sink is hit first",
        },
        "constant_flux_obstruction": {
            "all_target_intersecting_slopes": [str(x) for x in constant_target_slope_interval],
            "proof": "At x=2 every ray that reaches the target disk is inside the failure disk; all constant-flux schedules therefore fail first-hit selection.",
            "optimized_dark": "all dark stress amplitudes in the model rescale (2,1) and miss the target disk",
            "constant_average_phi_1_over_2": "reaches the target point only along a ray that first enters the failure disk",
        },
        "falsification": {
            "proportional_control_determinant": str(proportional_det),
            "result": "If light rescales both glide velocities proportionally, the switched path stays on the dark ray and this advantage disappears.",
        },
        "burgers_compatibility": burgertopology(),
        "clearance_margin": "sqrt(1/18)-21/100 > 0; a stochastic claim requires acquired diffusion/pinning/reaction rates",
        "limitations": [
            "event centers are abstract reduced glide coordinates, not an experimentally mapped ZnS network",
            "mobility ratios are dimensionless witness values, not measured parameters",
            "line continuity, core chemistry, stacking-fault evolution, pinning and non-equilibrium noise are not fitted",
            "the source ZnS paper establishes core-selective mobility changes, not this reaction schedule or retained endpoint",
        ],
    }

    out = Path(__file__).resolve().parents[1] / "results" / "geometric_witness.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
