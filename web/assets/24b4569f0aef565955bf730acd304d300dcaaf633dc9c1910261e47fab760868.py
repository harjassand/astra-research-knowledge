#!/usr/bin/env python3
"""Exact principal-minor replay of H_{k,r} <= C(13,k) I for Spin(13), r>=1.

Reads the inherited sparse highest-weight extraction.  It does not rebuild the
262144-dimensional star matrix and it says nothing about general n.
"""
from __future__ import annotations

from itertools import combinations
from math import comb
from pathlib import Path
import json
import sympy as sp

HERE = Path(__file__).parent
SOURCE = (HERE.parent / "c11_spin_uniform" / "obstruction" /
          "spin13_fullstar_blocks.json")


def matrix(rows):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in rows])


def check_psd_by_principal_minors(M):
    checked = 0
    failures = []
    undecided = []
    cert = []
    for size in range(1, M.rows + 1):
        for inds in combinations(range(M.rows), size):
            det = sp.factor(M.extract(inds, inds).det())
            checked += 1
            cert.append({"indices_zero_based": list(inds), "determinant": str(det)})
            if det.is_negative is True:
                failures.append({"indices_zero_based": list(inds), "determinant": str(det)})
            elif det.is_nonnegative is not True:
                undecided.append({"indices_zero_based": list(inds), "determinant": str(det)})
    return not failures and not undecided, checked, failures, undecided, cert


def main():
    source = json.loads(SOURCE.read_text())
    records = []
    total_minors = 0
    total_blocks = 0
    for key, block in source["blocks"].items():
        r = int(key.split(",")[0])
        if r == 0:
            continue
        G = matrix(block["gram"])
        for k, raw in enumerate(block["bilinear_H"], start=1):
            B = matrix(raw)
            degree = comb(13, k)
            gap = degree * G - B
            ok, count, failures, undecided, cert = check_psd_by_principal_minors(gap)
            total_minors += count
            total_blocks += 1
            records.append({
                "block": key,
                "r": r,
                "swap": int(key.split(",")[1]),
                "grade": k,
                "degree": degree,
                "order": G.rows,
                "psd_by_all_exact_principal_minors": ok,
                "principal_minor_count": count,
                "failures": failures,
                "undecided": undecided,
                "certificate": cert,
            })
    result = {
        "status": "FINITE_EXACT_PASS" if all(x["psd_by_all_exact_principal_minors"] for x in records) else "FINITE_FAILURE",
        "dimension": 64,
        "group": "Spin(13)",
        "n": 6,
        "scope": "Exact reduced-star termwise inequalities H_{k,r} <= C(13,k) I for every extracted r>=1 block and grade k=1..6 only.",
        "excluded_r0": "r=0 is the distinct unresolved spinor block and is intentionally excluded.",
        "input": str(SOURCE),
        "reduced_grade_block_count": total_blocks,
        "principal_minor_count": total_minors,
        "checks": records,
        "limitation": "Finite exact arithmetic on supplied internally reconstructed Spin(13) blocks; not an all-n proof, not an independent extraction audit, and not a proof of the mixed common-comparator theorem.",
    }
    out = HERE / "spin13_r_ge1_termwise_certificate.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"], "blocks", total_blocks, "principal minors", total_minors)
    for rec in records:
        if not rec["psd_by_all_exact_principal_minors"]:
            print("FAIL", rec["block"], "grade", rec["grade"], rec["failures"][:1], rec["undecided"][:1])
    print("certificate", out)


if __name__ == "__main__":
    main()
