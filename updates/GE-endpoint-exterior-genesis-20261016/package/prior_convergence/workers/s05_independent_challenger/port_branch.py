"""Replay a branch-scoped exterior-port response calculation.

This is a synthetic algebraic fixture, not an electrical or material measurement.
The hidden cubic is used only by the simulator and the full-model comparator.
The reduced predictor receives a sampled port-current curve and a curvature bound.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


K = 0.8
Y0 = math.sqrt(1.0 - K)
J0 = -K * Y0
STEP = 0.01
NOISE = 1.0e-4
H = 1.0


def bisect(f, lo: float, hi: float, iterations: int = 90) -> float:
    flo = f(lo)
    fhi = f(hi)
    assert flo <= 0.0 <= fhi, (lo, hi, flo, fhi)
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        if f(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def cubic(y: float, z: float) -> float:
    return y**3 + (K - 1.0) * y - K * z


def positive_branch(z: float) -> float:
    assert 0.0 <= z <= 0.2
    return bisect(lambda y: cubic(y, z), Y0, 2.0)


def exact_port(z: float) -> float:
    return K * (z - positive_branch(z))


def reduced_root(port, h: float) -> tuple[float, float]:
    # U(x,z;h) = x^2/2 + (x-z)^2/2 + 3z^2/2 - hx - J0*z.
    # U_x=0 gives x=(h+z)/2; U_z+j=0 gives the scalar equation below.
    z = bisect(lambda z: 3.5 * z + port(z) - J0 - h / 2.0, 0.0, 0.2)
    x = (h + z) / 2.0
    return x, z


def interpolated_port(samples: list[float], z: float) -> float:
    assert 0.0 <= z <= 0.2
    u = min(z / STEP, len(samples) - 1.0)
    i = min(int(u), len(samples) - 2)
    t = u - i
    return (1.0 - t) * samples[i] + t * samples[i + 1]


def stable_cubic_roots(z: float) -> list[float]:
    critical = math.sqrt((1.0 - K) / 3.0)
    intervals = [(-2.0, -critical), (critical, 2.0)]
    roots = []
    for lo, hi in intervals:
        flo, fhi = cubic(lo, z), cubic(hi, z)
        if flo <= 0.0 <= fhi:
            roots.append(bisect(lambda y: cubic(y, z), lo, hi))
    return roots


def quasistatic_sweep(zs: list[float], initial_sign: int) -> list[tuple[float, float, float]]:
    prev = max(stable_cubic_roots(zs[0])) if initial_sign > 0 else min(stable_cubic_roots(zs[0]))
    out = []
    for z in zs:
        candidates = stable_cubic_roots(z)
        y = min(candidates, key=lambda candidate: abs(candidate - prev))
        out.append((z, y, K * (z - y)))
        prev = y
    return out


def main() -> None:
    samples = [exact_port(i * STEP) + (NOISE if i % 2 else -NOISE) for i in range(21)]
    sampled_port = lambda z: interpolated_port(samples, z)
    true_x, true_z = reduced_root(exact_port, H)
    sample_x, sample_z = reduced_root(sampled_port, H)
    jprime0 = K - K * K / (3.0 * Y0 * Y0 - 1.0 + K)
    tangent_port = lambda z: J0 + jprime0 * z
    tangent_x, tangent_z = reduced_root(tangent_port, H)

    # j''(z)=6 K^3 y/(3y^2-1+K)^3, decreasing for y >= Y0.
    curvature_bound = 6.0 * K**3 * Y0 / (3.0 * Y0 * Y0 - 1.0 + K) ** 3
    port_error_bound = NOISE + curvature_bound * STEP * STEP / 8.0
    mu = (5.2 - math.sqrt(5.44)) / 2.0
    state_error_bound = port_error_bound / mu
    target_error_bound = port_error_bound / 5.4
    min_secant_slope = min((samples[i + 1] - samples[i]) / STEP for i in range(20))
    assert min_secant_slope >= -0.82 - 1.0e-12
    assert abs(sample_x - true_x) <= target_error_bound
    assert math.hypot(sample_x - true_x, sample_z - true_z) <= state_error_bound

    zs_down = [0.08 - i * 0.0002 for i in range(801)]
    zs_up = list(reversed(zs_down))
    down = quasistatic_sweep(zs_down, 1)
    up = quasistatic_sweep(zs_up, -1)
    down_at_zero = min(down, key=lambda row: abs(row[0]))
    up_at_zero = min(up, key=lambda row: abs(row[0]))
    down_jumps = [(down[i][0], down[i][1] - down[i - 1][1]) for i in range(1, len(down)) if abs(down[i][1] - down[i - 1][1]) > 0.1]
    up_jumps = [(up[i][0], up[i][1] - up[i - 1][1]) for i in range(1, len(up)) if abs(up[i][1] - up[i - 1][1]) > 0.1]
    fold_abs = (2.0 * (1.0 - K) / (3.0 * K)) * math.sqrt((1.0 - K) / 3.0)
    assert len(down_jumps) == len(up_jumps) == 1
    assert abs(down_jumps[0][0] + fold_abs) < 0.0002
    assert abs(up_jumps[0][0] - fold_abs) < 0.0002

    result = {
        "status": "synthetic_finite_discriminator_only",
        "parameters": {"k": K, "control_h": H, "port_grid_step": STEP, "port_queries": len(samples), "injected_absolute_port_error": NOISE},
        "exact_full_branch": {"x": true_x, "z": true_z, "hidden_y": positive_branch(true_z)},
        "sampled_port_prediction": {"x": sample_x, "z": sample_z, "actual_x_error": abs(sample_x - true_x), "actual_state_error": math.hypot(sample_x - true_x, sample_z - true_z)},
        "linear_tangent_prediction": {"x": tangent_x, "z": tangent_z, "actual_x_error": abs(tangent_x - true_x)},
        "analytic_certificate": {"port_curvature_bound": curvature_bound, "port_uniform_error_bound": port_error_bound, "reduced_strong_monotonicity_mu": mu, "state_error_bound": state_error_bound, "target_x_error_bound": target_error_bound, "sampled_min_secant_slope": min_secant_slope},
        "hysteresis_discriminator": {"fold_abs_z": fold_abs, "down_at_zero": down_at_zero, "up_at_zero": up_at_zero, "same_z_port_gap": abs(down_at_zero[2] - up_at_zero[2]), "down_jumps": down_jumps, "up_jumps": up_jumps},
        "resource_scope": "21 simulated clamped port evaluations, two reduced scalar bisections, two quasi-static simulated sweeps of 801 states; no physical acquisitions, calibration, wall-clock advantage, or energy measurement",
    }
    path = Path(__file__).with_name("RESULTS.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
