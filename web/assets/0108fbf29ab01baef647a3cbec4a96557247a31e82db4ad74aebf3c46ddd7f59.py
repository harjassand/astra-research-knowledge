#!/usr/bin/env python3
"""Bounded diagnostics for the joint-posterior affine archive theorem.

Checks exact graded-mesh geometry used by the positive codec and evaluates the
claimed geometric-spectrum leading rates. These checks do not certify the
asymptotic proof or the joint-density assumptions for an arbitrary model.
"""
from fractions import Fraction
from math import exp, log, sqrt


def node(j: int, J: int) -> Fraction:
    t = Fraction(j, J)
    return -1 + 6 * t * t - 4 * t * t * t


def exact_mesh_diagnostic(max_J: int = 128) -> dict:
    checked = 0
    worst_centroid_scaled = Fraction(0)
    for J in range(3, max_J + 1):
        u = [node(j, J) for j in range(J + 1)]
        gaps = [u[j + 1] - u[j] for j in range(J)]
        assert max(gaps) <= Fraction(3, J)
        assert max((gaps[j + 1] - gaps[j] for j in range(J - 1)),
                   default=Fraction(0)) <= Fraction(12, J * J)
        assert max((gaps[j] - gaps[j + 1] for j in range(J - 1)),
                   default=Fraction(0)) <= Fraction(12, J * J)
        assert gaps[0] <= Fraction(6, J * J)
        assert gaps[-1] <= Fraction(6, J * J)
        for j in range(J + 1):
            if j == 0:
                displacement = gaps[0] / 3
            elif j == J:
                displacement = gaps[-1] / 3
            else:
                displacement = (gaps[j] - gaps[j - 1]) / 3
            assert abs(displacement) <= Fraction(4, J * J)
            worst_centroid_scaled = max(worst_centroid_scaled,
                                         abs(displacement) * J * J)
            checked += 1
    return {
        "max_J": max_J,
        "exact_hat_centroids_checked": checked,
        "worst_J2_centroid_displacement": str(worst_centroid_scaled),
        "result": "PASS",
    }


def geometric_rates(b: float = 0.4, a: float = 0.2) -> list[dict]:
    rows = []
    for L in (12.0, 18.0, 24.0, 30.0):
        eps = a * exp(-L)
        n = max(1, int(L / b))
        lower_sum = sum(max(0.0, log(a * exp(-b * i) / eps))
                        for i in range(1, n + 1))
        rows.append({
            "log_a_over_epsilon": L,
            "effective_modes_approx": n,
            "sum_log_s_over_eps_over_L2": lower_sum / (L * L),
            "half_sum_over_L2": 0.5 * lower_sum / (L * L),
        })
    return rows


if __name__ == "__main__":
    print({
        "mesh": exact_mesh_diagnostic(),
        "geometric_rate_diagnostic": geometric_rates(),
        "analytic_shared_scalar_rank": "Jacobian is d-by-1, so rank <= 1 for d>=2; the score law is singular in R^d.",
        "scope": "finite exact mesh checks and arithmetic diagnostics only",
    })
