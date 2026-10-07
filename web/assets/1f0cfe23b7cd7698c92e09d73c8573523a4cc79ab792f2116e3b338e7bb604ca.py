"""Finite quadrature fixtures, not a proof or finite-bit compiler.

Tests the exact-reference conditional hat kernel for Gaussian and quartic
location noise. Gaussian [-12,12] and quartic [-4,4] numerical cutoffs are
used only by these diagnostics; the mathematical kernel has no cutoff.
"""
from pathlib import Path
import json
import math
import numpy as np


def fixture(k, a, cutoff, theta, labels, resolution):
    x = np.linspace(-cutoff, cutoff, resolution + 1)
    dx = 2 * cutoff / resolution
    quadrature = np.full(x.size, dx)
    quadrature[[0, -1]] *= 0.5
    norm = k * a ** (1 / (2 * k)) / math.gamma(1 / (2 * k))
    p0 = norm * np.exp(-a * x ** (2 * k))
    delta = p0 * np.expm1(-a * ((x - theta) ** (2 * k) - x ** (2 * k)))
    u = 0.5 + np.arctan(x) / math.pi
    coordinate = labels * u
    left = np.floor(coordinate).astype(int) % labels
    right = (left + 1) % labels
    fraction = coordinate - np.floor(coordinate)
    alpha = np.bincount(left, weights=(1 - fraction) * p0 * quadrature,
                        minlength=labels)
    alpha += np.bincount(right, weights=fraction * p0 * quadrature,
                         minlength=labels)
    perturbation = np.bincount(left,
                              weights=(1 - fraction) * delta * quadrature,
                              minlength=labels)
    perturbation += np.bincount(right,
                               weights=fraction * delta * quadrature,
                               minlength=labels)
    ratios = np.divide(perturbation, alpha, out=np.zeros_like(alpha),
                       where=alpha > 0)
    output_delta = p0 * ((1 - fraction) * ratios[left] + fraction * ratios[right])
    tv = float(0.5 * np.sum(quadrature * np.abs(output_delta - delta)))
    return {
        "k": k, "a": a, "theta": theta, "labels": labels,
        "resolution": resolution, "tv": tv,
        "scaled_tv_J2_over_theta": tv * labels ** 2 / abs(theta),
        "reference_mass": float(np.sum(alpha)),
        "perturbation_mass": float(np.sum(perturbation)),
        "output_perturbation_mass": float(np.sum(quadrature * output_delta)),
        "unused_labels_in_numeric_cutoff": int(np.sum(alpha == 0)),
    }


if __name__ == "__main__":
    results = []
    for k, a, cutoff in [(1, 0.5, 12.0), (2, 1.0, 4.0)]:
        for theta in [1e-4, 0.01, 0.25, 1.0]:
            for labels in [32, 64, 128]:
                results.append(fixture(k, a, cutoff, theta, labels, 262144))
    for k, a, cutoff in [(1, 0.5, 12.0), (2, 1.0, 4.0)]:
        results.append(fixture(k, a, cutoff, 1e-4, 128, 524288))
    for labels in [256, 512, 1024, 2048]:
        results.append(fixture(2, 1.0, 4.0, 1.0, labels, 524288))
    out = Path(__file__).with_name("kernel_diagnostic.json")
    out.write_text(json.dumps({"scope": __doc__, "fixtures": results}, indent=2) + "\n")
    for r in results:
        print(f"k={r['k']} mean={r['theta']:g} J={r['labels']} "
              f"TV={r['tv']:.9g} J2*TV/mean={r['scaled_tv_J2_over_theta']:.6g} "
              f"resolution={r['resolution']}")
