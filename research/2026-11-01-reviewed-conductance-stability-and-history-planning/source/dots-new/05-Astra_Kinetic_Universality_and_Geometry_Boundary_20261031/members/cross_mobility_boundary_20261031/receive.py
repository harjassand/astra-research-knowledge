#!/usr/bin/env python3
"""Exact rational receiver for the explicitly proved cross-mobility family.

This receives a fixed analytic grammar, not an arbitrary dynamics model.
No quadrature, simulation, PDE solve, sampling, or unverified partition input.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from math import gcd
from pathlib import Path
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SCHEMA = "fixed_quadratic_cross_mobility_v1"
FIELDS = {"schema", "k", "epsilon"}
DEFAULT_MAX_EXPANDED_POWER = 1_000_000


def exact_int(value, label):
    if type(value) is not int:
        raise ValueError(f"{label} must be an exact JSON integer, not float/bool/string")
    return value


def rational_object(x):
    x = Fraction(x)
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def strict_json_loads(raw):
    def no_duplicate_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=no_duplicate_keys)


def receive(source, *, max_expanded_power=DEFAULT_MAX_EXPANDED_POWER):
    if type(source) is not dict or set(source) != FIELDS:
        raise ValueError("input must have exactly schema, k, epsilon")
    if source["schema"] != SCHEMA:
        raise ValueError("unreceived model grammar")
    k = exact_int(source["k"], "k")
    if k < 1:
        raise ValueError("k must be at least 1")
    item = source["epsilon"]
    if type(item) is not dict or set(item) != {"numerator", "denominator"}:
        raise ValueError("epsilon must have exactly numerator and denominator")
    n = exact_int(item["numerator"], "epsilon numerator")
    d = exact_int(item["denominator"], "epsilon denominator")
    if d <= 0 or gcd(n, d) != 1:
        raise ValueError("epsilon must be reduced with positive denominator")
    epsilon = Fraction(n, d)
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must lie strictly between 0 and 1")

    if type(max_expanded_power) is not int or max_expanded_power < 1:
        raise ValueError("resource budget must be a positive exact integer")
    if (k * k + 1) // 2 > max_expanded_power:
        raise ValueError("resource_budget: expanded integer power exceeds configured limit; theorem not rejected")
    gamma = Fraction(k * k, 1) / (1 - epsilon)
    determinant = gamma - k * k
    schur = 1 - Fraction(k * k, 1) / gamma
    assert determinant > 0 and schur == epsilon
    core_upper = 36 * epsilon
    tail_exponent = k * k // 128
    tail_upper = Fraction(1200, k) / (1 << tail_exponent)
    tilted_exponent = (k * k + 1) // 2
    tilted_lower = Fraction(1, 16 * 3**tilted_exponent)
    schur_lower = epsilon / 16
    cap_lower = max(schur_lower, tilted_lower)
    cap_upper = core_upper + tail_upper
    assert 0 < cap_lower <= cap_upper
    condition_lower = gamma / epsilon
    condition_upper = (gamma + 1) ** 2 / (gamma * epsilon)
    return {
        "status": "received",
        "schema": SCHEMA,
        "input": source,
        "model": {
            "potential": "F(y,z)=(1+(1-y^2)^2)*z^2/2",
            "beta": 1,
            "A": "all (y,z) with y<=-1/2",
            "B": "all (y,z) with y>=1/2",
            "mobility": [[rational_object(1), rational_object(k)],
                         [rational_object(k), rational_object(gamma)]],
            "determinant": rational_object(determinant),
            "longitudinal_schur_complement": rational_object(schur),
        },
        "global_receiving": {
            "gibbs_normalizer_interval": [3, 16],
            "basin_probability_interval": ["1/4", "1/2"],
            "lyapunov": "V_D=1+x^T D^-1 x",
            "generator_lyapunov_identity":
                "L V_D=4-[6(y^2-2/3)^2+4/3]*z^2<=4",
            "each_actual_D_nonexplosive_reversible_invariant": True,
        },
        "capacity_normalized": {
            "lower": rational_object(cap_lower),
            "upper": rational_object(cap_upper),
            "schur_lower": rational_object(schur_lower),
            "tilted_line_lower": rational_object(tilted_lower),
            "core_upper": rational_object(core_upper),
            "patch_upper": rational_object(tail_upper),
            "tail_power_two_exponent": tail_exponent,
            "tilted_power_three_exponent": tilted_exponent,
        },
        "capacity_over_basin_mass": {
            "lower": rational_object(2 * cap_lower),
            "upper": rational_object(4 * cap_upper),
        },
        "eigenvalue_condition_number": {
            "lower": rational_object(condition_lower),
            "upper": rational_object(condition_upper),
        },
        "guarantee": "deterministic exact rational theorem enclosure; not a PDE estimate",
        "scope": "fixed received analytic grammar and constant SPD/FDT interface only",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-expanded-power", type=int,
                        default=DEFAULT_MAX_EXPANDED_POWER,
                        help="finite integer-expansion budget; default 1000000")
    args = parser.parse_args()
    try:
        result = receive(strict_json_loads(args.input.read_text()),
                         max_expanded_power=args.max_expanded_power)
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        result = {"status": "rejected", "reason": str(error)}
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")
    return 0 if result["status"] == "received" else 2


if __name__ == "__main__":
    raise SystemExit(main())
