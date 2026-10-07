#!/usr/bin/env python3
"""Small floating diagnostic for the mapping-torus symmetric-space formulas.

This checks explicit smooth determinant-one paths over a hyperbolic torus
mapping torus. It does not verify the general cocycle theorem, entropy formula,
CAT(0) stability argument, or any numerical error bound.
"""
from __future__ import annotations

import json
import math


LAMBDA = (3.0 + math.sqrt(5.0)) / 2.0
H = math.log(LAMBDA)


def values(t: float, amp_u: float, amp_v: float) -> tuple[float, float]:
    angle = 2.0 * math.pi * t
    u = amp_u * math.sin(angle)
    up = 2.0 * math.pi * amp_u * math.cos(angle)
    v = amp_v * math.sin(angle)
    vp = 2.0 * math.pi * amp_v * math.cos(angle)
    g11 = math.exp(2.0 * H * t + u)
    g12 = v
    g22 = math.exp(-2.0 * H * t - u) * (1.0 + v * v)
    g11p = g11 * (2.0 * H + up)
    g12p = vp
    g22p = g22 * (-2.0 * H - up + 2.0 * v * vp / (1.0 + v * v))

    # Since det(G)=1, G^{-1}=[[g22,-g12],[-g12,g11]].
    c11 = g22 * g11p - g12 * g12p
    c12 = g22 * g12p - g12 * g22p
    c21 = -g12 * g11p + g11 * g12p
    # C=G^{-1}Gdot has trace zero; its eigenvalues are +/-2s.
    kappa2 = c11 * c11 + c12 * c21
    if kappa2 < -1.0e-10:
        raise ArithmeticError(f"negative squared eigenvalue at t={t}: {kappa2}")
    s = 0.5 * math.sqrt(max(0.0, kappa2))
    axis_distance = math.asinh(abs(g12))
    return s, axis_distance


def simpson(fn, n: int = 40000) -> float:
    if n % 2:
        raise ValueError("Simpson grid size must be even")
    h = 1.0 / n
    total = fn(0.0) + fn(1.0)
    total += 4.0 * sum(fn(j * h) for j in range(1, n, 2))
    total += 2.0 * sum(fn(j * h) for j in range(2, n, 2))
    return total * h / 3.0


def run_case(amp_u: float, amp_v: float) -> dict[str, float | bool]:
    speed_mean = simpson(lambda t: values(t, amp_u, amp_v)[0])
    work_ratio = simpson(lambda t: values(t, amp_u, amp_v)[0] ** 2)
    defect = work_ratio - H * H
    excess = 2.0 * (speed_mean - H)
    variance_about_H = simpson(lambda t: (values(t, amp_u, amp_v)[0] - H) ** 2)
    max_axis_distance = max(values(j / 20000.0, amp_u, amp_v)[1] for j in range(20001))
    cat_tube_bound = math.sqrt(max(0.0, H * excess + excess * excess / 4.0))
    return {
        "amp_u": amp_u,
        "amp_v": amp_v,
        "H": H,
        "mean_s": speed_mean,
        "integral_s_squared": work_ratio,
        "power_defect_D": defect,
        "path_length_excess_epsilon": excess,
        "integral_(s-H)^2": variance_about_H,
        "max_distance_to_Sol_axis": max_axis_distance,
        "CAT0_tube_bound": cat_tube_bound,
        "checks": {
            "mean_s_ge_H": speed_mean + 1.0e-10 >= H,
            "D_ge_H_epsilon_plus_epsilon2_over4": defect + 1.0e-9 >= H * excess + excess * excess / 4.0,
            "variance_identity": abs(defect - H * excess - variance_about_H) < 2.0e-7,
            "axis_distance_within_CAT0_bound": max_axis_distance <= cat_tube_bound + 1.0e-6,
            "axis_distance_within_sqrt_defect": max_axis_distance <= math.sqrt(max(0.0, defect)) + 1.0e-6,
        },
    }


def main() -> None:
    cases = [run_case(0.0, 0.0), run_case(0.03, 0.02), run_case(0.10, 0.06)]
    print(json.dumps({"status": "PASS" if all(all(c["checks"].values()) for c in cases) else "FAIL",
                      "diagnostic_scope": "floating Simpson quadrature, sampled axis distance; not a proof or certified numerical bound",
                      "cases": cases}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
