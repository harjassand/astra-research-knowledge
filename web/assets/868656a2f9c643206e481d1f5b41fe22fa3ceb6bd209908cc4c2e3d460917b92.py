#!/usr/bin/env python3
"""Exact finite-alphabet enumeration of adjacent-parity AH sum rates.

This is a diagnostic for the binary modulo-sum source only.  For iid
P_XY=(theta_00, theta_01, theta_10, theta_11), let
U_i=X_i xor X_{i+1}, V_i=Y_i xor Y_{i+1}.  The m-letter AH point has sum
rate (2 H(U,V,Z_m) - H(U,V))/m, because Z_1,...,Z_{m-1} are determined by
(U,V,Z_m).  The code enumerates the 4^m source words and evaluates those
entropies directly; it is not an encoder simulation or a converse proof.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections import defaultdict


def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0.0)


def ah_adjacent_parity_sum_rate(theta, m):
    if len(theta) != 4 or any(p < 0.0 for p in theta):
        raise ValueError("theta must be four nonnegative probabilities")
    if not math.isclose(sum(theta), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("theta must sum to one")
    if m < 1:
        raise ValueError("m must be positive")

    mass_uv = defaultdict(float)
    mass_uvz = defaultdict(float)
    for x in itertools.product((0, 1), repeat=m):
        for y in itertools.product((0, 1), repeat=m):
            probability = math.prod(theta[2 * xi + yi] for xi, yi in zip(x, y))
            u = tuple(x[i] ^ x[i + 1] for i in range(m - 1))
            v = tuple(y[i] ^ y[i + 1] for i in range(m - 1))
            z_m = x[-1] ^ y[-1]
            mass_uv[(u, v)] += probability
            mass_uvz[(u, v, z_m)] += probability

    return (2.0 * entropy(mass_uvz.values()) - entropy(mass_uv.values())) / m


def report(theta, max_m):
    h_xy = entropy(theta)
    p_z_one = theta[1] + theta[2]
    h_z = entropy((p_z_one, 1.0 - p_z_one))
    p_x_one = theta[2] + theta[3]
    p_y_one = theta[1] + theta[3]
    h_x = entropy((p_x_one, 1.0 - p_x_one))
    h_y = entropy((p_y_one, 1.0 - p_y_one))

    print(f"theta={tuple(theta)}")
    print(f"H(X,Y)={h_xy:.12f}")
    print(f"H(Z)={h_z:.12f}; 2 H(Z)={2.0 * h_z:.12f}")
    print(f"H(X)={h_x:.12f}; H(Y)={h_y:.12f}")
    print("m, AH adjacent-parity sum rate")
    for m in range(1, max_m + 1):
        print(f"{m}, {ah_adjacent_parity_sum_rate(theta, m):.12f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--theta",
        nargs=4,
        type=float,
        default=(0.379, 0.008, 0.246, 0.367),
        metavar=("P00", "P01", "P10", "P11"),
    )
    parser.add_argument("--max-m", type=int, default=5)
    args = parser.parse_args()
    report(args.theta, args.max_m)


if __name__ == "__main__":
    main()
