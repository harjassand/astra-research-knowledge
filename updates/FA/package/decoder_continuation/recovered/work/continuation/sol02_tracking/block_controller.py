#!/usr/bin/env python3
"""Exact integer-grid robust controller for one rational two-coordinate block.

The demonstration uses supplied rational directions without direction rounding.
Every scalar grid noise value is checked after the action.  No random sampling
or floating geometry enters the certificate.  NumPy performs integer/Boolean
array operations only.  See RESULT.txt for the general block-support theorem.
"""
from __future__ import annotations

import json
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def shift_back(dest, dx, dy):
    """Return indicator that (x+dx,y+dy) is in dest, with outside=False."""
    out = np.zeros_like(dest)
    height, width = dest.shape
    xlo, xhi = max(0, -dx), min(width, width - dx)
    ylo, yhi = max(0, -dy), min(height, height - dy)
    if xlo < xhi and ylo < yhi:
        out[ylo:yhi, xlo:xhi] = dest[ylo + dy:yhi + dy, xlo + dx:xhi + dx]
    return out


def action_good(dest, safe, vx, vy, kden, cap, action):
    good = safe.copy()
    for noise in range(-cap, cap + 1):
        coefficient = action * kden + noise
        good &= shift_back(dest, vx * coefficient, vy * coefficient)
    return good


def compile_controller(directions, denominator, kden, cap, radius, mode="optimal"):
    lattice = denominator * kden
    extent = (radius.numerator * lattice + radius.denominator - 1) // radius.denominator
    coordinates = np.arange(-extent, extent + 1, dtype=np.int64)
    xx, yy = np.meshgrid(coordinates, coordinates)
    safe = (xx * xx + yy * yy) * radius.denominator**2 <= (radius.numerator * lattice)**2
    masks = [None] * (len(directions) + 1)
    policies = [None] * len(directions)
    masks[-1] = safe
    for step in range(len(directions) - 1, -1, -1):
        vx, vy = directions[step]
        plus = action_good(masks[step + 1], safe, vx, vy, kden, cap, 1)
        minus = action_good(masks[step + 1], safe, vx, vy, kden, cap, -1)
        if mode == "greedy":
            use_plus = vx * xx + vy * yy <= 0
            winning = safe & ((use_plus & plus) | (~use_plus & minus))
            policy = np.where(use_plus, 1, -1).astype(np.int8)
        else:
            winning = safe & (plus | minus)
            policy = np.where(plus, 1, -1).astype(np.int8)
        masks[step], policies[step] = winning, policy
    return bool(masks[0][extent, extent]), np.stack(masks), np.stack(policies), extent, lattice


def main():
    start = time.perf_counter()
    directions = [(5, 0), (3, 4), (0, 5), (4, -3)]
    denominator = 5
    n = len(directions)
    gamma = F(1, 2)
    kden = 8 * n
    cap = (gamma.numerator * kden + gamma.denominator - 1) // gamma.denominator + 1
    candidates = [F(2), F(9, 4), F(5, 2), F(11, 4), F(3)]
    trials = []
    selected = None
    for mode in ("optimal", "greedy"):
        for radius in candidates:
            won, masks, policies, extent, lattice = compile_controller(
                directions, denominator, kden, cap, radius, mode
            )
            trials.append({"mode": mode, "radius": str(radius), "origin_winning": won})
            if won:
                if mode == "optimal":
                    selected = (radius, masks, policies, extent, lattice)
                break
    if selected is None:
        raise RuntimeError("No tested radius won; no certificate written")
    radius, masks, policies, extent, lattice = selected
    np.savez_compressed(
        HERE / "block_controller_certificate.npz",
        directions=np.asarray(directions, dtype=np.int64),
        denominator=np.int64(denominator),
        kden=np.int64(kden),
        cap=np.int64(cap),
        radius_numerator=np.int64(radius.numerator),
        radius_denominator=np.int64(radius.denominator),
        extent=np.int64(extent),
        lattice=np.int64(lattice),
        winning=masks,
        policy=policies,
    )
    scalar_error = F(5, 8 * kden)
    error_per_block = n * scalar_error
    h = F(3, 2)
    mixed_direction = (F(3, 5), F(4, 5))
    mixed_corner = (h, -h)
    extension_failures = []
    for epsilon, noise in [(1, gamma), (-1, -gamma)]:
        nxt = tuple(x + (epsilon + noise) * v for x, v in zip(mixed_corner, mixed_direction))
        assert any(abs(x) > h for x in nxt)
        extension_failures.append({"action": epsilon, "postdecision_noise": str(noise), "next_state": list(map(str, nxt))})
    receipt = {
        "evidence_status": "exact finite Boolean/integer game plus analytic continuous transfer",
        "directions": [[str(F(x, denominator)), str(F(y, denominator))] for x, y in directions],
        "noise_bound_original": str(gamma),
        "scalar_feedback_absolute_error_required": str(F(1, 8 * kden)),
        "virtual_noise_grid_denominator": kden,
        "virtual_noise_cap": cap,
        "virtual_noise_bound": str(F(cap, kden)),
        "trials": trials,
        "selected_virtual_radius": str(radius),
        "continuous_transfer_error_per_block": str(error_per_block),
        "continuous_radius_per_block": str(radius + error_per_block),
        "orthogonal_k_block_radius": f"({radius + error_per_block})*sqrt(k)",
        "winning_counts": [int(x.sum()) for x in masks],
        "mixed_direction_naive_product_failure": {
            "product_halfwidth": str(h),
            "corner": list(map(str, mixed_corner)),
            "direction": list(map(str, mixed_direction)),
            "branches": extension_failures,
            "scope": "invalidates only the independent coordinate-box product extension at this corner",
        },
        "elapsed_seconds": time.perf_counter() - start,
        "general_arbitrary_schedule_compiler": "NOT ESTABLISHED",
        "novelty": "UNKNOWN; robust finite safety DP and coordinate decomposition are known methods",
    }
    (HERE / "block_controller_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
