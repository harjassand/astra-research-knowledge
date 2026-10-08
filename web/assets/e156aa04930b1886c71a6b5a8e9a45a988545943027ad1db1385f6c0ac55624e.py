#!/usr/bin/env python3
"""Exact support-witness rescue for the n=7 alpha=e5+e6 seed-hull miss."""
from __future__ import annotations

from itertools import combinations
from math import comb
from pathlib import Path
import json
import sys

import sympy as sp

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import r0_seed_cone_probe as base


def main():
    n = 7
    alpha = [0, 0, 0, 0, 1, 1, 0]
    F = base.recoupling(n)
    D = sum((alpha[k - 1] * base.grade_diagonal(n, k)
             for k in range(1, n + 1)), sp.zeros(n + 1))
    H = sp.simplify(D + F * D * F)
    trace = sum(comb(2 * n + 1, k) * alpha[k - 1]
                for k in range(1, n + 1))

    # The exact rational state is recorded and replayed in the companion JSON.
    state = json.loads((HERE / "spin15_rational_seed_certificate.json").read_text())
    s = [sp.Rational(x) for x in state["grade_moments"]]
    attained = sum(alpha[k] * s[k] for k in range(n))
    q = sp.Rational(80711, 10)
    gap = sp.simplify(q * sp.eye(n + 1) - H)
    minors = []
    failures = []
    undecided = []
    for size in range(1, n + 2):
        for indices in combinations(range(n + 1), size):
            det = sp.factor(gap.extract(indices, indices).det())
            minors.append({"indices_zero_based": list(indices), "determinant": str(det)})
            if det.is_negative is True:
                failures.append({"indices_zero_based": list(indices), "determinant": str(det)})
            elif det.is_nonnegative is not True:
                undecided.append({"indices_zero_based": list(indices), "determinant": str(det)})

    result = {
        "status": "EXACT_R0_DIRECTION_RESCUED" if not failures and not undecided and attained > q - trace else "CHECK_FAILED",
        "group": "Spin(15)",
        "n": n,
        "spinor_dimension": 2**n,
        "scope": "One nonnegative grade ray alpha=e5+e6 in the exact r=0 block; proves this particular 8-seed hull failure is repaired by an attained pure-state support value.",
        "alpha_grades_1_to_7": alpha,
        "trace_term": str(trace),
        "r0_star_exact_upper_certificate": {
            "q": str(q),
            "claim": "lambda_max(H_alpha,r0) <= q",
            "method": "all exact principal minors of q I - H are nonnegative",
            "principal_minor_count": len(minors),
            "negative_minors": failures,
            "undecided_minors": undecided,
            "principal_minors": minors,
        },
        "attained_pure_seed": {
            "certificate_path": "spin15_rational_seed_certificate.json",
            "grade5_plus_grade6": str(attained),
            "grade5_plus_grade6_decimal": float(attained),
            "strict_margin_over_star_excess_upper": str(sp.factor(attained - (q - trace))),
            "star_excess_upper": str(q - trace),
        },
        "finite_seed_hull": {
            "eight_original_seed_support": 62,
            "seed_hull_star_gap_failure_determinant": "-38153371047622852770144000",
            "source_path": "r0_seed_cone_n7.json",
        },
        "limitation": "This closes one direction and one isotypic block only. It neither classifies full canonical support nor proves the all-r/all-n star inequality or provides a channel counterexample.",
    }
    out = HERE / "r0_seed_rescue_n7.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"], "principal minors", len(minors),
          "exact margin", result["attained_pure_seed"]["strict_margin_over_star_excess_upper"])
    print("certificate", out)


if __name__ == "__main__":
    main()
