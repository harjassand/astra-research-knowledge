#!/usr/bin/env python3
"""Rational noise rounding for a stated-error use of a fixed-frame compiler.

It consumes the parent's net theorem as a mathematical interface; it does not
generate/claim a frame, solve the parent's LP, or claim a measured speedup.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json


def plan(c, local_noise_uses, epsilon):
    assert c >= 1 and local_noise_uses >= 1 and 0 < epsilon < 1
    s = 1 / (2 * c - 1)
    assert 3 * s * s < 1  # strict qubit EA promise, exact rational comparison
    h = 4 * epsilon / (3 * local_noise_uses)
    delta = min(s / 2, h)
    rounded_s = s - delta
    rounded_c = (1 + 1 / rounded_s) / 2
    lam = (1 - 3 * rounded_s * rounded_s) / 4
    tv_bound = F(3, 4) * local_noise_uses * delta
    uniform_lower = min(F(3, 16), epsilon / (2 * local_noise_uses))
    assert rounded_c > c
    assert tv_bound <= epsilon
    assert lam >= uniform_lower > 0
    return {"input_c": str(c), "local_noise_uses_upper_bound": local_noise_uses,
            "desired_joint_output_TV_epsilon": str(epsilon),
            "s": str(s), "delta_s": str(delta),
            "reference_s": str(rounded_s), "reference_c": str(rounded_c),
            "per_local_use_half_diamond_distance": str(F(3,4)*delta),
            "joint_output_TV_bound": str(tv_bound),
            "reference_PT_margin_lambda": str(lam),
            "uniform_lambda_lower_bound": str(uniform_lower),
            "rational_fidelity_net_tolerance_with_slack": str(lam/2),
            "frame_generation_and_kernel_LP_not_executed_here": True}


def c_above_threshold(bits):
    h = 1 << (bits - 1)
    return F(h + isqrt(3*h*h) + 1, 1 << bits)


def main():
    examples = []
    for bits in (16, 32, 64, 128):
        examples.append(plan(c_above_threshold(bits), 1000, F(1,1000)))
    examples.append(plan(F(10), 1, F(1,2)))
    result = {"status": "exact rational plans only; no claimed device or speedup",
              "cost": "reference error controlled by local uses, not input noise gap",
              "ordinary_comparator": "HN stated-error separability simulation",
              "samples_from_modified_reference_not_exact_original": True,
              "rare_outcome_conditioning_not_covered_by_unconditional_TV_bound": True,
              "examples": examples}
    folder = Path(__file__).resolve().parent
    (folder/"ACCURACY_RESULTS.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
