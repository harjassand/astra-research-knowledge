#!/usr/bin/env python3
"""Rational codec certificates for shared-scalar and independent-score sensors."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scalar_periodic_codec import verify_exact_joint_posterior  # noqa: E402


def ceil_sqrt(q: F) -> int:
    if q <= 0:
        return 0
    n = isqrt(q.numerator // q.denominator)
    while n * n * q.denominator < q.numerator:
        n += 1
    while n and (n - 1) * (n - 1) * q.denominator >= q.numerator:
        n -= 1
    return n


def fixed_bits(alphabet_size: int) -> int:
    return (alphabet_size - 1).bit_length()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon", default="1/1000")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    epsilon = F(args.epsilon)
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")

    # Shared family: feature vector (cos(2*pi*t1), cos(4*pi*t1)).
    # Product family: feature vector (cos(2*pi*t1), cos(2*pi*t2)).
    # Both live on the same observation torus and share reference dt1 dt2.
    shared_tv_constant = F(3025, 588)

    # For a single first harmonic, ||U''|| <= 4*pi^2. Tensor-product hats
    # preserve constants, and rho=1/4 with ||v||_2<=1 gives the following
    # uniform product-family TV coefficient. Use sqrt(2)<3/2 and pi<22/7.
    product_tv_constant = F(605, 392)

    shared_j = max(3, ceil_sqrt(shared_tv_constant / epsilon))
    product_j = max(3, ceil_sqrt(product_tv_constant / epsilon))
    shared_tv = shared_tv_constant / (shared_j * shared_j)
    product_tv = product_tv_constant / (product_j * product_j)
    shared_dimension = shared_j  # ancillary second coordinate is regenerated
    product_dimension = product_j * product_j
    assert shared_tv <= epsilon
    assert product_tv <= epsilon

    exact_joint = verify_exact_joint_posterior()
    assert exact_joint["fisher_gram"] == [["1/32", "0/1"], ["0/1", "1/32"]]
    rho = F(1, 4)
    independent_fisher = [
        [rho * rho * F(1, 2), F(0)],
        [F(0), rho * rho * F(1, 2)],
    ]
    assert independent_fisher == [[F(1, 32), F(0)], [F(0), F(1, 32)]]

    result = {
        "status": "exact rational codec certificates; heat-flow and memory-order derivations are in the accompanying report",
        "common_interface": "one blind observation on T^2; parameter ||v||_2<=1; rho=1/4; continuous decoded output; TV error <= epsilon",
        "shared_scalar_family": {
            "density": "1+(1/4)*(v1*cos(2*pi*t1)+v2*cos(4*pi*t1))",
            "fisher_at_zero": [["1/32", "0/1"], ["0/1", "1/32"]],
            "feature_relation": "V=2*U^2-1; t2 is ancillary uniform",
            "periodic_labels_per_active_coordinate": shared_j,
            "total_memory_dimension": shared_dimension,
            "ideal_bits": f"log2({shared_dimension})",
            "fixed_binary_bits": fixed_bits(shared_dimension),
            "exact_TV_bound": f"{shared_tv.numerator}/{shared_tv.denominator}",
            "uniform_TV_coefficient_over_J_squared": "3025/588",
        },
        "independent_feature_family": {
            "density": "1+(1/4)*(v1*cos(2*pi*t1)+v2*cos(2*pi*t2))",
            "fisher_at_zero": [["1/32", "0/1"], ["0/1", "1/32"]],
            "reference_features": "independent arcsine variables U1,U2",
            "periodic_labels_per_coordinate": product_j,
            "total_memory_dimension": product_dimension,
            "ideal_bits": f"log2({product_dimension})",
            "fixed_binary_bits": fixed_bits(product_dimension),
            "exact_TV_bound": f"{product_tv.numerator}/{product_tv.denominator}",
            "uniform_TV_coefficient_over_J_squared": "605/392",
        },
        "asymptotic_codec_dimensions": {
            "shared": "O(epsilon^(-1/2))",
            "independent": "O(epsilon^(-1))",
            "memory_bit_coefficients": "1/2 versus 1 multiplying log2(1/epsilon)",
        },
        "scope": "These finite fixed-parameter-dimension bounds are analytic interpolation certificates. Continuous randomization/output, model calibration, and finite-bit output costs are not included.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
