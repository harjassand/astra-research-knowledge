"""Small exact checks of the constructive opening and numerical constants.

These checks do not establish the proposed multiscale sufficiency theorem.
They verify the isolated Toom mechanism, a genuine interaction counterexample,
and independently integrate the Pareto radius law for the lower-bound rate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from scipy.integrate import quad


def toom_step(errors: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Infinite zero background, finite set of erroneous one cells."""
    candidates = set(errors)
    candidates.update((x - 1, y) for x, y in errors)
    candidates.update((x, y - 1) for x, y in errors)
    return {
        (x, y)
        for x, y in candidates
        if (
            ((x, y) in errors)
            + ((x + 1, y) in errors)
            + ((x, y + 1) in errors)
        )
        >= 2
    }


def check_rectangles() -> int:
    checked = 0
    for a in range(1, 12):
        for b in range(1, 12):
            state = {(x, y) for x in range(a) for y in range(b)}
            for t in range(a + b):
                expected = {
                    (x, y)
                    for x in range(a)
                    for y in range(b)
                    if (a - 1 - x) + (b - 1 - y) >= t
                }
                assert state == expected, (a, b, t, state, expected)
                state = toom_step(state)
            assert not state
            checked += 1
    return checked


def check_interactions() -> dict:
    examples = []
    for m in range(1, 25):
        start = {(x, m - x) for x in range(m + 1)}
        assert all(not toom_step({point}) for point in start)
        state = start
        for t in range(m + 1):
            expected = {(x, m - t - x) for x in range(m - t + 1)}
            assert state == expected
            state = toom_step(state)
        assert not state
        if m in (1, 4, 12, 24):
            examples.append(
                {
                    "initial_singleton_faults": m + 1,
                    "individual_healing_rounds": 1,
                    "joint_healing_rounds": m + 1,
                }
            )
    return {"checked_diagonals": 24, "examples": examples}


def numerical_constants() -> list[dict]:
    rows = []
    # Independent integration of the Pareto density after r=a/(1-u).
    # This maps the infinite radius interval onto [0,1].
    for d in (1, 2, 3):
        for alpha in (d + 0.5, d + 1.0, d + 1.5, d + 2.25):
            rstar, a = 1.3, 2.7
            exact = (
                math.gamma(d + 1)
                * math.gamma(alpha - d)
                / math.gamma(alpha)
                * rstar**alpha
                * a ** (d - alpha)
            )
            integrated, numerical_error = quad(
                lambda u: (
                    alpha
                    * rstar**alpha
                    * a ** (d - alpha)
                    * u**d
                    * (1 - u) ** (alpha - d - 1)
                ),
                0.0,
                1.0,
                epsabs=1e-10,
                epsrel=1e-10,
            )
            assert math.isclose(exact, integrated, rel_tol=2e-8)

            lam, v, horizon = 0.023, 0.7, 11.0
            constant = (
                2**d
                * math.gamma(d + 1)
                * math.gamma(alpha - d)
                / math.gamma(alpha)
                * rstar**alpha
            )
            beta = alpha - d
            if math.isclose(beta, 1.0):
                cumulative = lam * constant / v * math.log1p(v * horizon / a)
            else:
                cumulative = lam * constant / (v * (1 - beta)) * (
                    (a + v * horizon) ** (1 - beta) - a ** (1 - beta)
                )
            cumulative_quad, _ = quad(
                lambda t: lam * constant * (a + v * t) ** (-beta),
                0.0,
                horizon,
                epsabs=1e-11,
            )
            assert math.isclose(cumulative, cumulative_quad, rel_tol=1e-11)

            # A cube of side L has complete-reset rate lambda E(2R-L)^d_+.
            side = 2 * a
            kconstant = (
                2**alpha
                * math.gamma(d + 1)
                * math.gamma(alpha - d)
                / math.gamma(alpha)
                * rstar**alpha
            )
            device_rate = lam * kconstant * side ** (d - alpha)
            assert math.isclose(device_rate, lam * 2**d * exact, rel_tol=1e-12)
            rows.append(
                {
                    "d": d,
                    "alpha": alpha,
                    "radius_integral_relative_error": abs(integrated / exact - 1),
                    "cumulative_hazard": cumulative,
                    "fixed_cube_reset_rate": device_rate,
                    "quadrature_error_estimate": numerical_error,
                }
            )
    return rows


def main() -> None:
    results = {
        "status": "All scoped checks passed; no sufficiency theorem tested or claimed.",
        "rectangles_checked": check_rectangles(),
        "interaction_counterexample": check_interactions(),
        "pareto_constants": numerical_constants(),
    }
    destination = Path(__file__).with_name("check_results.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": "passed",
                "rectangle_cases": results["rectangles_checked"],
                "diagonal_cases": results["interaction_counterexample"][
                    "checked_diagonals"
                ],
                "pareto_cases": len(results["pareto_constants"]),
                "maximum_radius_integral_relative_error": max(
                    row["radius_integral_relative_error"]
                    for row in results["pareto_constants"]
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
