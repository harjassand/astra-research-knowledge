#!/usr/bin/env python3
"""Exact rational certificates for pair exchange at arbitrary fixed total N.

This checks the closed-form potential from REVISION_01.txt against every
state/rate-box vertex.  For N <= 16 it also calls reaction_recovery's exact
Fourier-Motzkin synthesizer as an independent executable replay.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from reaction_recovery import (
    propensity,
    qs,
    states_and_target,
    synthesize,
    verify_potential,
)


def qstr(value: Fraction) -> str:
    return qs(value)


def make_network(total: int, ell: Fraction, upper: Fraction) -> dict:
    return {
        "name": f"pair-exchange total={total}",
        "total": total,
        "core_min_each": 2,
        "row_cap": 200_000,
        "reactions": [
            {"name": "AB_to_2A", "reactants": [1, 1], "products": [2, 0],
             "rate_min": qstr(ell), "rate_max": qstr(upper)},
            {"name": "2A_to_AB", "reactants": [2, 0], "products": [1, 1],
             "rate_min": qstr(ell), "rate_max": qstr(upper)},
            {"name": "AB_to_2B", "reactants": [1, 1], "products": [0, 2],
             "rate_min": qstr(ell), "rate_max": qstr(upper)},
            {"name": "2B_to_AB", "reactants": [0, 2], "products": [1, 1],
             "rate_min": qstr(ell), "rate_max": qstr(upper)},
        ],
    }


def closed_form(total: int, ell: Fraction, upper: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    if total < 4 or ell <= 0 or upper < ell:
        raise ValueError("require total >= 4 and 0 < ell <= upper")
    delta = Fraction(1, 1) / (ell * total * (total - 1))
    b = (Fraction(1, 1) / (ell * (total - 1) ** 2)
         + upper / (ell ** 2 * total * (total - 1) ** 2))
    a = b + delta
    return delta, b, a


def verify_closed_form(total: int, ell: Fraction, upper: Fraction) -> dict:
    delta, b, a = closed_form(total, ell, upper)
    net = make_network(total, ell, upper)
    states, target = states_and_target(total, 2)
    # Only the four states immediately outside the target can be transient.
    h = {x: Fraction(0) for x in target}
    h[(0, total)] = a
    h[(1, total - 1)] = b
    h[(total - 1, 1)] = b
    h[(total, 0)] = a
    reactions = []
    for item in net["reactions"]:
        reactants = tuple(item["reactants"])
        products = tuple(item["products"])
        reactions.append({
            "name": item["name"],
            "reactants": reactants,
            "products": products,
            "jump": (products[0] - reactants[0], products[1] - reactants[1]),
            "low": ell,
            "high": upper,
        })
    result = verify_potential(states, target, reactions, h)
    assert result["valid"], result
    assert result["minimum_negative_drift"] == "1", result
    assert result["max_h"] == qstr(a), result

    replay = None
    if total <= 16:
        replay = synthesize(net)
        assert replay["status"] == "CERTIFIED", replay
        replay_check = replay["checker"]
        assert replay_check["valid"] and replay_check["minimum_negative_drift"] != "infinity"
    return {
        "total": total,
        "ell": qstr(ell),
        "upper": qstr(upper),
        "delta": qstr(delta),
        "h_boundary1": qstr(b),
        "h_boundary0": qstr(a),
        "closed_form_exact_checker": result,
        "fourier_motzkin_replay": None if replay is None else {
            "status": replay["status"],
            "potential": replay["potential"],
            "checker": replay["checker"],
        },
        "rate_corner_checks": (1 if ell == upper else 16) * 4,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total", type=int, default=32)
    parser.add_argument("--ell", default="1")
    parser.add_argument("--upper", default="4")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    ell, upper = Fraction(args.ell), Fraction(args.upper)
    if args.max_total < 4:
        raise SystemExit("--max-total must be at least 4")
    cases = [verify_closed_form(n, ell, upper) for n in range(4, args.max_total + 1)]
    report = {
        "status": "ALL_EXACT_CHECKS_PASSED",
        "interpretation": "finite fixed-total classes; no unbounded-state theorem",
        "case_count": len(cases),
        "cases": cases,
    }
    encoded = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
