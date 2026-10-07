#!/usr/bin/env python3
"""Independent bounded exact audit of c10_s02's N76 boundary identities.

This script reconstructs the complex set and six propensities directly. It
checks exact factorial minima/ratios and detailed-balance edge identities on
bounded boxes. The all-a formulas and concavity no-go remain symbolic claims
proved in the accompanying audit note; finite loops are not those proofs.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial, isclose, log

State = tuple[int, int, int]

# Complexes: 0, C, B, A+B, A+C.  Coordinates are (A,B,C).
COMPLEXES: tuple[State, ...] = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (1, 1, 0),
    (1, 0, 1),
)


def available(x: State, y: State) -> bool:
    return all(xi >= yi for xi, yi in zip(x, y))


def residual_factorial(x: State) -> int:
    vals = [
        factorial(x[0] - y[0])
        * factorial(x[1] - y[1])
        * factorial(x[2] - y[2])
        for y in COMPLEXES
        if available(x, y)
    ]
    assert vals
    return min(vals)


def transitions(x: State) -> list[tuple[int, State]]:
    a, b, c = x
    out: list[tuple[int, State]] = []
    if a and c:
        out.append((a * c, (a, b + 1, c - 1)))  # A+C -> A+B
    if a and b:
        out.append((a * b, (a, b - 1, c + 1)))  # A+B -> A+C
        out.append((a * b, (a - 1, b, c)))      # A+B -> B
    if b:
        out.append((b, (a + 1, b, c)))          # B -> A+B
    if c:
        out.append((c, (a, b, c - 1)))          # C -> 0
    out.append((1, (a, b, c + 1)))              # 0 -> C
    return out


def poisson_unnormalized(x: State) -> Fraction:
    a, b, c = x
    return Fraction(1, factorial(a) * factorial(b) * factorial(c))


def two_jump_additive_drift(x: State) -> float:
    """Compute E[F(Y_2)-F(Y_0)|Y_0=x] for the embedded jump chain."""
    fx = residual_factorial(x)
    first = transitions(x)
    total = sum(rate for rate, _ in first)
    ans = 0.0
    for rate1, y in first:
        fy = residual_factorial(y)
        second = transitions(y)
        total2 = sum(rate2 for rate2, _ in second)
        for rate2, z in second:
            ans += (rate1 / total) * (rate2 / total2) * log(
                residual_factorial(z) / fx
            )
    return ans


def main() -> None:
    checked_f_points = 0
    checked_z_points = 0
    checked_balance_edges = 0
    checked_component_states = 0
    checked_two_jump_points = 0
    checked_flat_ray_skeleton_points = 0

    # Reconstruct the exact N76 min over the supplied complex set.
    for a in range(2, 81):
        x = (a, 0, 1)
        fx = residual_factorial(x)
        assert fx == factorial(a - 1)
        actual = transitions(x)
        expected = [
            (a, (a, 1, 0)),
            (1, (a, 0, 0)),
            (1, (a, 0, 2)),
        ]
        assert actual == expected
        ratios = [Fraction(residual_factorial(y), fx) for _, y in actual]
        assert ratios == [Fraction(1), Fraction(a), Fraction(1)]
        # The only nonzero log increment is the C-death edge, so LF=log(a).
        lf = sum(rate * log(float(ratio)) for (rate, _), ratio in zip(actual, ratios))
        assert isclose(lf, log(a), rel_tol=1e-13, abs_tol=1e-13)
        checked_f_points += 1

        # Independent direct P^2 calculation for F at the problematic ray.
        # The formula below follows by enumerating all six possible two-jump
        # paths from x_a; several terms are zero because their net F change is
        # zero. It is a reaction-event skeleton, not physical-time LF.
        direct = two_jump_additive_drift(x)
        formula = (
            -Fraction(a * a, (a + 2) * (2 * a + 2)) * log(a - 1)
            + Fraction(a, (a + 2) * (2 * a + 2)) * log(a)
            + Fraction(1, (a + 2) * (2 * a + 3)) * log(2)
        )
        assert isclose(direct, formula, rel_tol=1e-12, abs_tol=1e-12)
        if a == 2:
            assert direct > 0
        else:
            assert direct < 0
        checked_two_jump_points += 1

    # The other unbounded flat ray z_n=(0,n,0) is corrected by the same
    # two-event jump skeleton for n>=3, with a finite positive exception n=2.
    for n in range(2, 81):
        z = (0, n, 0)
        direct = two_jump_additive_drift(z)
        formula = (
            -Fraction(n * n, (n + 1) * (3 * n + 1)) * log(n - 1)
            + Fraction(1, (n + 1) * (n + 2)) * log(2)
        )
        assert isclose(direct, formula, rel_tol=1e-12, abs_tol=1e-12)
        if n == 2:
            assert direct > 0
        else:
            assert direct < 0
        checked_flat_ray_skeleton_points += 1

    # At z_n=(0,n,0), only B->A+B and 0->C fire, and both preserve F.
    for n in range(1, 81):
        z = (0, n, 0)
        fz = residual_factorial(z)
        assert fz == factorial(n - 1)
        actual = transitions(z)
        expected = [(n, (1, n, 0)), (1, (0, n, 1))]
        assert actual == expected
        assert [Fraction(residual_factorial(y), fz) for _, y in actual] == [1, 1]
        checked_z_points += 1

    # For each feasible directed edge whose endpoints lie in this box,
    # verify pi(x)q(x,y)=pi(y)q(y,x) for the product-Poisson weights.
    box = range(5)
    for a in box:
        for b in box:
            for c in box:
                x = (a, b, c)
                if a + b == 0:
                    continue  # the closed Gamma_0 component is excluded
                for rate, y in transitions(x):
                    if max(y) >= 5 or y[0] + y[1] == 0:
                        continue
                    reverse_rate = next(
                        (rr for rr, yy in transitions(y) if yy == x), None
                    )
                    assert reverse_rate is not None
                    assert poisson_unnormalized(x) * rate == poisson_unnormalized(y) * reverse_rate
                    checked_balance_edges += 1

    # Check component predicate preservation on a bounded cube. This is a
    # diagnostic for the six listed transitions, not an all-state proof.
    for a in range(9):
        for b in range(9):
            for c in range(9):
                x = (a, b, c)
                for _, y in transitions(x):
                    assert (a + b >= 1) == (y[0] + y[1] >= 1)
                checked_component_states += 1

    print(
        "PASS",
        {
            "complex_set_size": len(COMPLEXES),
            "F_boundary_points_a_2_to_80": checked_f_points,
            "direct_two_jump_formula_points_a_2_to_80": checked_two_jump_points,
            "direct_two_jump_formula_points_z_n_2_to_80": checked_flat_ray_skeleton_points,
            "flat_rays_n_1_to_80": checked_z_points,
            "product_poisson_balance_edges_box_0_to_4": checked_balance_edges,
            "component_predicate_states_box_0_to_8": checked_component_states,
            "scope": "finite exact checks plus floating log identity; symbolic proof remains in audit note",
        },
    )


if __name__ == "__main__":
    main()
