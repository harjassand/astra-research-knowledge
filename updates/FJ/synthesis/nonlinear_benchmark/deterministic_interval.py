#!/usr/bin/env python3
"""Interval check of the finite sparse-Fourier first Picard correction.

Only the assigned benchmark model is loaded.  mpmath.iv evaluates the same
finite Fourier expression with directed interval endpoints; the PDE error
radius is separately computed as an exact Fraction from the global tube
certificate.  This checks the finite precision evaluation of e1, not an exact
solution or the sampler implementation.
"""
from __future__ import annotations

import json
import math
import time
from fractions import Fraction as Q
from pathlib import Path

import mpmath as mp

OUT = Path(__file__).resolve().parent
iv = mp.iv
iv.dps = 40
D, J = 8, 16
Key = tuple[int, ...]
Map = dict[Key, object]


def convolve(a: Map, b: Map) -> Map:
    out: Map = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key = tuple(x + y for x, y in zip(ka, kb))
            out[key] = out.get(key, iv.mpc(0)) + va * vb
    return out


def bounds() -> tuple[Q, Q, Q]:
    A = Q(5, 102) + Q(5, 103)
    lo = 1 + 100 * (1 - A) ** 3
    hi = 1 + 100 * (1 + A) ** 3
    gamma = 2 * (150 * (1 + A) ** 2) * Q(1, 40)
    gamma += 3 * (100 * (1 + A)) * Q(1, 40) ** 2
    gamma += 4 * 25 * Q(1, 40) ** 3
    vmid = (lo + hi) / 2
    q = ((hi - lo) / 2 + gamma) / vmid
    return lo, hi, q * Q(1, 40)


def endpoints(x) -> list[str]:
    return [str(x.a), str(x.b)]


def main() -> None:
    start = time.perf_counter()
    modes: list[tuple[Key, int]] = []
    for i in range(D):
        k = [0] * D
        k[i] = 1
        modes.append((tuple(k), 1))
    for i in range(D):
        k = [0] * D
        k[i] = 1
        k[(i + 1) % D] = 1
        modes.append((tuple(k), 2))

    E0: Map = {}
    for j, (k, norm2) in enumerate(modes):
        phase = iv.mpf("0.17") * (j + 1) + iv.mpf("0.013") * (j + 1) ** 2
        amplitude = (iv.mpf(10) / J) / (101 + norm2) / 2
        for sign in (1, -1):
            kk = tuple(sign * a for a in k)
            z = iv.mpc(iv.cos(phase), sign * iv.sin(phase))
            E0[kk] = amplitude * z

    E2 = convolve(E0, E0)
    E3 = convolve(E2, E0)
    E4 = convolve(E2, E2)
    residual: Map = {}
    for source, scale in ((E2, -150), (E3, -100), (E4, -25)):
        for key, value in source.items():
            residual[key] = residual.get(key, iv.mpc(0)) + scale * value

    A = Q(5, 102) + Q(5, 103)
    lam = 1 + 100 * (1 - A) ** 3
    Lam = 1 + 100 * (1 + A) ** 3
    vmid = (lam + Lam) / 2
    vmid_iv = iv.mpf(vmid.numerator) / vmid.denominator
    x = [iv.mpf("0.21") + iv.mpf("0.19") * i for i in range(D)]

    predictor = iv.mpf(1)
    for key, value in E0.items():
        theta = sum((key[i] * x[i] for i in range(D)), iv.mpf(0))
        factor = iv.mpc(iv.cos(theta), iv.sin(theta))
        predictor += (value * factor).real

    correction = iv.mpc(0)
    for key, value in residual.items():
        norm2 = sum(z * z for z in key)
        theta = sum((key[i] * x[i] for i in range(D)), iv.mpf(0))
        factor = iv.mpc(iv.cos(theta), iv.sin(theta))
        correction += value * factor / (vmid_iv + norm2)
    e1 = predictor + correction.real

    _, _, err = bounds()
    err_iv = iv.mpf(err.numerator) / err.denominator
    solution_lower = e1.a - err_iv
    solution_upper = e1.b + err_iv
    elapsed = time.perf_counter() - start
    result = {
        "method": "40-decimal-digit mpmath.iv sparse Fourier evaluation of e1",
        "mpmath_version": mp.__version__,
        "mpmath_iv_dps": iv.dps,
        "candidate_support_sizes": {
            "e0_signed": len(E0), "e0_squared": len(E2),
            "e0_cubed": len(E3), "e0_fourth": len(E4),
            "residual": len(residual),
        },
        "sparse_complex_product_count": 32 * 32 + 465 * 32 + 465 * 465,
        "residual_mode_phase_evaluations": len(residual),
        "e1_interval": endpoints(e1),
        "e1_correction_interval": endpoints(correction.real),
        "exact_sup_error_radius_fraction": str(err),
        "u_query_interval_from_contraction": [str(solution_lower.a), str(solution_upper.b)],
        "wall_seconds_including_interval_build_and_query": elapsed,
        "scope": "The interval encloses the finite e1 Fourier expression; adding/subtracting the exact contraction radius encloses the PDE solution at the query. This is not a field-wide interval solution or validation of the stochastic sampler.",
    }
    (OUT / "deterministic_interval_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
