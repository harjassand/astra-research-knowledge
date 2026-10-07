#!/usr/bin/env python3
"""Exact rational calculator for the Dirichlet power-lift envelope."""

from fractions import Fraction as Q
import json
from pathlib import Path


def g(m: int) -> Q:
    if m == 0:
        return Q(1)
    return Q((2 * m) ** (2 * m), (2 * m + 1) ** (2 * m + 1))


def main() -> None:
    rows = []
    for m in range(33):
        gm = g(m)
        rows.append({
            "m": m,
            "g_m": str(gm),
            "c2_error_squared": str(2 * gm),
            "c4_error_squared": str(4 * gm),
        })
    result = {
        "arithmetic": "fractions.Fraction; exact rational values",
        "formula": "g_0=1; g_m=(2m)^(2m)/(2m+1)^(2m+1) for m>=1",
        "rows": rows,
        "floating_point_used": False,
        "solver_used": False,
    }
    Path(__file__).with_name("dirichlet_power_bounds.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps({
        "rows": len(rows),
        "g_1": str(g(1)),
        "c2_error_squared_at_m32": str(2 * g(32)),
        "exact_rational": True,
    }, indent=2))


if __name__ == "__main__":
    main()
