#!/usr/bin/env python3
"""Evaluate the explicit beta(L) sufficient condition from cycle 7."""
import argparse
import json
import math


def bound(L: int, S: float, Jmin: float, r: float, geometry: str = "periodic"):
    if L < 4 or L % 2:
        raise ValueError("L must be even and at least 4")
    if S <= 0 or Jmin <= 0 or not (0 < r <= 1):
        raise ValueError("require S,Jmin>0 and 0<r<=1")
    c_geom = 6 if geometry == "periodic" else 12
    V = L**3
    x = math.log(2 * V / math.log1p(r))
    beta = c_geom * L**2 * x / (S * Jmin)
    q = math.exp(-x)
    # The proof uses A(q)^V <= (1-q)^(-V) <= exp(2Vq) <= 1+r.
    log_R_bound = math.log(math.expm1(2 * V * q)) if q > 0 else -math.inf
    return {
        "L": L, "V": V, "S": S, "Jmin": Jmin,
        "geometry": geometry, "c_geom": c_geom,
        "r_excited_partition_ratio": r,
        "x_beta_gap": x,
        "beta_min": beta,
        "beta_Jmin": beta * Jmin,
        "exp_minus_x": q,
        "2V_exp_minus_x": 2 * V * q,
        "log_R_bound_from_proof": log_R_bound,
        "excited_probability_bound": r / (1 + r),
        "W1_to_uniform_minusS_S_bound": 1 / (3 * V) + S * r / (2 * (1 + r)),
        "second_moment_abs_error_bound": S / (3 * V) + (2 * S**2 / 3) * r / (1 + r),
        "2_abs_component_radius_estimator_bias_bound": 1 / (2 * V) + S * r / (1 + r),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=8)
    parser.add_argument("--S", type=float, default=0.5)
    parser.add_argument("--Jmin", type=float, default=1.0)
    parser.add_argument("--r", type=float, default=0.01)
    parser.add_argument("--geometry", choices=("periodic", "open"), default="periodic")
    args = parser.parse_args()
    print(json.dumps(bound(args.L, args.S, args.Jmin, args.r, args.geometry), indent=2))


if __name__ == "__main__":
    main()
