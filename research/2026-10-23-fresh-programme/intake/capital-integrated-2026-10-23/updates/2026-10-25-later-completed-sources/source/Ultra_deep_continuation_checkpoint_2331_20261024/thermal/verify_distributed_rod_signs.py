"""High-precision diagnostic of the exact distributed-rod sign construction.

The analytical argument is in DISTRIBUTED_ROD_CHALLENGE.md. These finitely
many checks are numerical challenges, not interval certificates or a proof.
All rods, their exact trigonometric inertia, and every selected q sample
are included. Requires mpmath only.
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp


mp.mp.dps = 55


def check_case(N: int, mu_text: str, full_index_set: bool = True) -> dict:
    mu = mp.mpf(mu_text)
    B = 12 * mu / (N * N * (N * N - 1))
    b = [mp.mpf(0)] + [B * (N - ell) for ell in range(1, N)]
    assert mp.almosteq(sum(ell * ell * b[ell] for ell in range(1, N)), mu)
    # Total connector mass / point mass is exactly mu.
    assert mp.almosteq(sum(b[ell] * ell * ell for ell in range(1, N)), mu)

    indices = list(range(2 * N // 3, 3 * N // 4 + 1))
    if not full_index_set:
        indices = sorted({indices[0], indices[len(indices) // 2], indices[-1]})

    min_even_margin = mp.inf
    min_odd_margin = mp.inf
    max_center_rest_scaled = mp.mpf(0)
    max_shifted_rest_scaled = mp.mpf(0)
    max_rest_derivative_scaled = mp.mpf(0)
    min_sine_ratio = mp.inf
    samples = 0

    for n in indices:
        xn = mp.pi / n
        for j in range(n + 1):
            q = j * mp.pi / n
            center_terms = []
            for ell in range(1, N):
                if ell != n:
                    y = ell * xn
                    center_terms.append(
                        2 * b[ell] * y * (mp.cos(y) - mp.cos(ell * q)) / mp.sin(y)
                    )
            center_rest = mp.fsum(center_terms)
            max_center_rest_scaled = max(
                max_center_rest_scaled, abs(center_rest) * N * N / mu
            )
            assert abs(center_rest) < 64 * mu / (N * N)

            for factor in (mp.mpf(1), mp.mpf("1.5"), mp.mpf(2)):
                delta = factor * b[n] / xn
                x = xn + delta
                terms = []
                rest_derivative_abs = mp.mpf(0)
                for ell in range(1, N):
                    y = ell * x
                    sy, cy = mp.sin(y), mp.cos(y)
                    cq = mp.cos(ell * q)
                    terms.append(2 * b[ell] * y * (cy - cq) / sy)
                    if ell != n:
                        h = min(ell, abs(ell - n))
                        ratio = abs(sy) * n / h
                        min_sine_ratio = min(min_sine_ratio, ratio)
                        assert ratio >= 1
                        derivative = 2 * b[ell] * ell * (
                            (cy - cq) / sy + y * (-1 + cq * cy) / (sy * sy)
                        )
                        rest_derivative_abs += abs(derivative)
                D = -x * x + mp.fsum(terms)
                rest = mp.fsum(terms[: n - 1] + terms[n:])
                assert abs(rest) < (64 * mu + 2304 * mu * mu) / (N * N)
                assert abs(rest) < mp.mpf(".06") * xn * xn
                assert rest_derivative_abs < 768 * mu
                max_shifted_rest_scaled = max(
                    max_shifted_rest_scaled, abs(rest) / (xn * xn)
                )
                max_rest_derivative_scaled = max(
                    max_rest_derivative_scaled, rest_derivative_abs / mu
                )
                if j % 2 == 0:
                    assert D > 0
                    min_even_margin = min(min_even_margin, D / (xn * xn))
                else:
                    assert D < 0
                    min_odd_margin = min(min_odd_margin, -D / (xn * xn))
                samples += 1

    all_indices = list(range(2 * N // 3, 3 * N // 4 + 1))
    intervals = []
    weighted_width = mp.mpf(0)
    for n in all_indices:
        xn = mp.pi / n
        intervals.append((xn + b[n] / xn, xn + 2 * b[n] / xn))
        weighted_width += n * b[n] / xn
    for earlier, later in zip(intervals, intervals[1:]):
        assert later[1] < earlier[0]
    assert weighted_width >= mu / (9 * mp.pi)
    assert max(upper for _, upper in intervals) <= (
        3 * mp.pi / (2 * N) + 3 * mu / (N * N)
    )

    def short(value: mp.mpf) -> str:
        return mp.nstr(value, 18)

    return {
        "N": N,
        "mu": mu_text,
        "selected_resonant_indices": indices,
        "sample_count": samples,
        "minimum_even_D_over_xn_squared": short(min_even_margin),
        "minimum_minus_odd_D_over_xn_squared": short(min_odd_margin),
        "maximum_center_rest_N_squared_over_mu": short(max_center_rest_scaled),
        "maximum_shifted_rest_over_xn_squared": short(max_shifted_rest_scaled),
        "maximum_sum_abs_rest_derivative_over_mu": short(max_rest_derivative_scaled),
        "minimum_nonresonant_sine_ratio": short(min_sine_ratio),
        "weighted_width_over_mu": short(weighted_width / mu),
        "guaranteed_width_over_mu": short(1 / (9 * mp.pi)),
    }


if __name__ == "__main__":
    cases = [
        check_case(12, ".01"),
        check_case(24, ".01"),
        check_case(24, ".000001"),
        check_case(120, ".01", full_index_set=False),
    ]
    result = {
        "precision_decimal_digits": mp.mp.dps,
        "scope": "finite high-precision diagnostic; analytical proof is separate",
        "all_assertions_pass": True,
        "cases": cases,
    }
    destination = Path(__file__).with_name("distributed_rod_sign_checks.json")
    if destination.exists():
        raise FileExistsError(f"Refusing to replace preserved results: {destination}")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
