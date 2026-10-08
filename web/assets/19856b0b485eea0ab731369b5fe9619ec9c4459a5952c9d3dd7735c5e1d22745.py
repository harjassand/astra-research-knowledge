"""Finite checks of explicit sharpness witnesses; not theorem verification."""
import json
import math
from pathlib import Path

import numpy as np


def sharp_phase(theta, lipschitz):
    cutoff = math.pi * lipschitz / (lipschitz + 1)
    return np.where(
        np.abs(theta) <= cutoff,
        theta,
        np.sign(theta) * lipschitz * (math.pi - np.abs(theta)),
    )


def main():
    count = 2**20
    theta = -math.pi + (np.arange(count) + 0.5) * (2 * math.pi / count)
    circle = np.exp(1j * theta)
    sharp = []
    for lipschitz in (1, 3, 7, 31, 127):
        phase = sharp_phase(theta, lipschitz)
        error_sq = float(np.mean(np.abs(np.exp(1j * phase) - circle) ** 2))
        expected = 2 / (lipschitz + 1)
        assert abs(error_sq - expected) < 2e-10
        assert abs(float(np.mean(phase))) < 1e-12
        endpoint_error = abs(np.exp(1j * sharp_phase(np.array([math.pi]), lipschitz)[0]) + 1)
        assert endpoint_error == 2
        sharp.append({"L": lipschitz, "squared_L2": error_sq,
                      "analytic_value": expected, "centered_mean": float(np.mean(phase)),
                      "endpoint_norm_error": endpoint_error})
    mobius = []
    for r in (0, 0.5, 0.9, 0.99):
        image = (1 + r * circle) / (1 + r * np.conj(circle))
        error_sq = float(np.mean(np.abs(image - circle) ** 2))
        expected = 2 * (1 - r)
        assert abs(error_sq - expected) < 2e-10
        assert float(np.max(np.abs(np.abs(image) - 1))) < 1e-12
        mobius.append({"r": r, "squared_L2": error_sq,
                       "analytic_value": expected, "endpoint_norm_error": 2,
                       "phase_lipschitz": 2*r/(1-r),
                       "optimal_lower_bound_at_this_L": 2*(1-r)/(1+r)})
    output = {"status": "FINITE_DIAGNOSTICS_ONLY", "grid_points": count,
              "sharp_witnesses": sharp, "source_mobius_witnesses": mobius,
              "K1_obstruction": "proved symbolically; not represented by finite matrix testing"}
    Path(__file__).with_name("diagnostics.json").write_text(json.dumps(output, indent=2))
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
