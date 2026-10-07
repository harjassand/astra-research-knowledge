#!/usr/bin/env python3
"""Exact rational spot checks for the stopped-diffusion anisotropy boundary.

This is a small independent algebra diagnostic, not a proof of the all-N
diffusion theorem or a finite-bit sampler.  All entries below are Fractions.
"""
from fractions import Fraction as F
import json
from pathlib import Path

C = (F(1), F(2), F(1))
M = F(1)
Lambda = M + 1
Lc = 2 * M + 1


def d_diagonal(r):
    r2 = r * r
    return (
        C[0] - r2 * C[1],
        C[1] - r2 * C[0],
        C[2] * (1 - r2) ** 2,
    )


def fmt_tuple(xs):
    return [f"{x.numerator}/{x.denominator}" for x in xs]


def main():
    r0sq = 1 / (16 * (Lc + 1))
    # For this M=1 fixture, r0^2=1/64 and hence r0=1/8 exactly.
    r0 = F(1, 8)
    assert r0 * r0 == r0sq
    s5_margin = (1 - r0sq) ** 2 - Lc * r0sq
    rows = []
    for label, r in (("inner_stop_radius", r0), ("interior_global", F(3, 4)), ("sphere_boundary", F(1))):
        rows.append({"case": label, "r": f"{r}", "D_diagonal": fmt_tuple(d_diagonal(r))})

    # A=C-Lambda I is diag(-1,0,-1), so its operator norm is exactly M=1.
    A_diagonal = tuple(ci - Lambda for ci in C)
    out = {
        "purpose": "Exact rational check of an allowed compact-parameter anisotropy where global D_C is indefinite, while the prescribed inner stop has a positive S5 margin.",
        "M": str(M),
        "Lambda": str(Lambda),
        "C_diagonal": fmt_tuple(C),
        "A_diagonal": fmt_tuple(A_diagonal),
        "A_operator_norm": str(max(abs(x) for x in A_diagonal)),
        "Lc": str(Lc),
        "r0_squared": str(r0sq),
        "S5_lower_margin_at_stop": str(s5_margin),
        "cases": rows,
        "conclusion": "D_C has a negative eigenvalue at r=3/4 and r=1, but the S5 lower bound at r0=1/8 is strictly greater than 3/4. This refutes an un-stopped global PSD claim and does not refute the stopped construction.",
        "scope": "Fraction-exact fixture; not an all-parameter proof or sampler validation.",
    }
    out_path = Path(__file__).with_suffix(".json")
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
