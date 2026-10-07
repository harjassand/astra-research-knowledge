#!/usr/bin/env python3
"""Small exact checks for the cross-phase acquisition-cost audit.

This checks arithmetic in two constructions only. It does not verify a general
information bound or make a physical sampling claim.
"""
from fractions import Fraction
import json


def main():
    # Y uniform on {+-1}^m; log B(Y)=a*diag(Y). The population Frobenius
    # variance is exactly m*a^2. The explicit table has 2^m rows and m entries
    # per row; a compact sampling oracle still consumes m coordinates/sample.
    a = Fraction(3, 7)
    dimensions = []
    for m in (1, 2, 8, 16):
        variance = Fraction(m) * a * a
        dimensions.append({
            "m": m,
            "exact_log_field_variance": str(variance),
            "table_rows": 2**m,
            "table_log_entries": m * 2**m,
            "compact_oracle_coordinates_per_draw": m,
        })

    # Rare-state acquisition witness: a scalar log-field is 0 with
    # probability 1-p and K with probability p. Its variance is
    # p(1-p)K^2, while n iid draws miss the rare state with probability
    # (1-p)^n. All values are exact rationals.
    n = 100
    p = Fraction(1, 2 * n)
    K = Fraction(1000)
    variance = p * (1 - p) * K * K
    miss = (1 - p) ** n
    rare = {
        "samples": n,
        "rare_probability": str(p),
        "rare_log_field_value": str(K),
        "population_variance": str(variance),
        "miss_probability": str(miss),
        "miss_probability_decimal": float(miss),
        "constant_instance_transcript_on_miss": "all observed log fields are 0",
    }

    print(json.dumps({"dimension_scaling": dimensions, "rare_state": rare}, indent=2))


if __name__ == "__main__":
    main()
