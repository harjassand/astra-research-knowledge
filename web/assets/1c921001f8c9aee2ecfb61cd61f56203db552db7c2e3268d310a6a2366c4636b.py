#!/usr/bin/env python3
"""Check closed-form constants in the quartic binary-testing consequence."""

import math


if __name__ == "__main__":
    a = 4.0 / 3.0
    mean_abs_coordinate = 1.0 / (2.0 * a ** 0.25 * math.gamma(0.75))
    error_slope = mean_abs_coordinate / 2.0
    print(f"d/d_beta TV(P_+, P_-) at 0+ = {mean_abs_coordinate:.12f}")
    print(f"small-beta Helstrom-error reduction coefficient = {error_slope:.12f}")
