#!/usr/bin/env python3
"""Small exact grid over resonant near-contact rank-one Fourier profiles."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as s

from near_contact_modes import eps, run_family


def leading(expr: s.Expr) -> tuple[int, s.Expr]:
    expr = s.factor(expr)
    num, den = s.fraction(expr)
    def valuation(poly: s.Expr) -> int:
        p = s.Poly(s.expand(poly), eps)
        return min(power[0] for power, coeff in p.terms() if coeff != 0)
    order = valuation(num) - valuation(den)
    coefficient = s.factor(s.limit(expr / eps**order, eps, 0, dir="+"))
    return order, coefficient


rows = []
delta_sets = (
    (s.Integer(0), s.Integer(0), s.Integer(0)),
    (s.Integer(1), s.Integer(1), s.Integer(1)),
    (s.Integer(-1), s.Integer(-1), s.Integer(-1)),
    (s.Integer(1), s.Integer(-1), s.Integer(0)),
    (s.Integer(-1), s.Integer(1), s.Integer(0)),
)
amp_sets = ((1, 1, 1), (1, 1, -1))
for deltas in delta_sets:
    mu1 = s.Rational(3, 2) + deltas[0]
    mu2 = s.Integer(3) + deltas[1]
    mu3 = s.Rational(9, 4) + deltas[2]
    for amps in amp_sets:
        modes = [
            ((1, 0), (eps, 1, mu1*eps**2, mu1*eps), s.Integer(amps[0])),
            ((0, 1), (2*eps, 1, 2*mu2*eps**2, mu2*eps), s.Integer(amps[1])),
            ((1, 1), (s.Rational(3, 2)*eps, 1,
                      s.Rational(3, 2)*mu3*eps**2, mu3*eps), s.Integer(amps[2])),
        ]
        try:
            out = run_family(modes)
        except Exception as exc:
            rows.append({"deltas": list(map(str, deltas)), "amps": amps,
                         "status": f"skipped:{type(exc).__name__}"})
            continue
        loss = s.factor(out["b_schur_contact"]**2/(2*out["H_schur_contact"]))
        loss_order, loss_coeff = leading(loss, )
        gap_order, gap_coeff = leading(out["full_optimized_gap"])
        rows.append({
            "deltas": list(map(str, deltas)), "amps": amps,
            "h_schur": [str(x) for x in leading(out["H_schur_contact"])],
            "b_schur": [str(x) for x in leading(out["b_schur_contact"])],
            "loss": [str(loss_order), str(loss_coeff)],
            "full_gap": [str(gap_order), str(gap_coeff)],
            "covariance_rank": out["covariance_rank"],
        })

Path(__file__).with_name("scan_resonant_contacts.json").write_text(
    json.dumps(rows, indent=2) + "\n"
)
for row in rows:
    if row.get("status"):
        print(row)
    elif int(row["loss"][0]) <= 0:
        print(row)
print(f"checked {len(rows)} exact families; loss limits saved to scan_resonant_contacts.json")
