#!/usr/bin/env python3
"""Independently check a rational outward top-tie direction.

Usage: verify_sparse_rational_counterdirection.py NETWORK.json DIRECTION.json

NETWORK.json uses the same `edges` format as recognize_sparse_rational.py.
DIRECTION.json is either a vector such as ["1", "-2/3"] or an object with a
`direction` field (the witness subobject printed by the recognizer).

This verifier uses only Python's standard-library Fraction arithmetic. Exit 0
means REFUTED with a fully checked exact witness; exit 1 means this direction
does not refute the property; exit 2 means malformed input.
"""

from __future__ import annotations

import json
import argparse
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any, Sequence


def rational(value: Any) -> F:
    if isinstance(value, bool):
        raise ValueError("boolean is not a rational number")
    return F(str(value))


def vector(raw: Any, label: str) -> tuple[F, ...]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{label} must be a nonempty rational vector")
    return tuple(rational(x) for x in raw)


def terms(raw: Any, label: str, d: int) -> tuple[tuple[F, ...], ...]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{label} must be a nonempty support")
    out = []
    for j, item in enumerate(raw):
        if isinstance(item, dict):
            exp = vector(item.get("exp"), f"{label}[{j}].exp")
            coef = rational(item.get("coef", "1"))
        else:
            exp = vector(item, f"{label}[{j}]")
            coef = F(1)
        if len(exp) != d or coef <= 0:
            raise ValueError(f"{label}[{j}] has a wrong dimension or nonpositive coefficient")
        out.append(exp)
    return tuple(out)


def dot(a: Sequence[F], b: Sequence[F]) -> F:
    return sum((x * y for x, y in zip(a, b)), F(0))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("network", type=Path)
    parser.add_argument("direction", type=Path)
    parser.add_argument("--property", choices=("endotactic", "strong"), default="endotactic")
    args = parser.parse_args(argv[1:])
    try:
        network = json.loads(args.network.read_text())
        raw_direction = json.loads(args.direction.read_text())
        if isinstance(raw_direction, dict):
            raw_direction = raw_direction["direction"]
        w = vector(raw_direction, "direction")
        if not isinstance(network, dict) or not isinstance(network.get("edges"), list) or not network["edges"]:
            raise ValueError("network must contain a nonempty edges list")
        parsed = []
        for i, edge in enumerate(network["edges"]):
            name = str(edge.get("name", f"e{i}"))
            nu = vector(edge["nu"], f"{name}.nu")
            if len(nu) != len(w):
                raise ValueError(f"{name} has a different dimension")
            P = terms(edge["P"], f"{name}.P", len(w))
            Q = terms(edge["Q"], f"{name}.Q", len(w))
            parsed.append((name, nu, P, Q))
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "reason": str(exc)}, indent=2))
        return 2

    active = []
    all_rows = []
    for name, nu, P, Q in parsed:
        drift = dot(nu, w)
        tau = max(dot(a, w) for a in P) - max(dot(b, w) for b in Q)
        row = {"name": name, "w_dot_nu": drift, "tau": tau}
        all_rows.append(row)
        if drift != 0:
            active.append(row)
    if not active:
        print(json.dumps({"status": "NOT_A_COUNTERDIRECTION", "reason": "all channels are neutral"}, indent=2))
        return 1
    top_active = max(row["tau"] for row in active)
    active_outward = [row["name"] for row in active
                      if row["tau"] == top_active and row["w_dot_nu"] > 0]
    top_all = max(row["tau"] for row in all_rows)
    no_inward_global_top = not any(row["tau"] == top_all and row["w_dot_nu"] < 0
                                   for row in all_rows)
    if args.property == "endotactic":
        refuted = bool(active_outward)
        reason = "outward active channel is tied at the maximum active score"
        top = top_active
        relevant = active
        bad = active_outward
    elif active_outward:
        refuted = True
        reason = "the endotactic condition fails"
        top = top_active
        relevant = active
        bad = active_outward
    else:
        refuted = no_inward_global_top
        reason = "no inward channel occurs at the global all-source maximum"
        top = top_all
        relevant = all_rows
        bad = [row["name"] for row in relevant
               if row["tau"] == top and row["w_dot_nu"] >= 0] if refuted else []
    result = {
        "status": "REFUTED" if refuted else "NOT_A_COUNTERDIRECTION",
        "property": args.property,
        "reason": reason if refuted else "the supplied direction does not refute the property",
        "direction": [str(x) for x in w],
        "tested_top_tau": str(top),
        "outward_or_neutral_top_channels": bad,
        "active_top_tau": str(top_active),
        "active_outward_top_channels": active_outward,
        "global_all_source_top_tau": str(top_all),
        "active_channels": [
            {"name": row["name"], "w_dot_nu": str(row["w_dot_nu"]),
             "tau": str(row["tau"]), "top_active_tied": row["tau"] == top_active}
            for row in active
        ],
        "all_channels": [
            {"name": row["name"], "w_dot_nu": str(row["w_dot_nu"]),
             "tau": str(row["tau"]), "global_top_tied": row["tau"] == top_all}
            for row in all_rows
        ],
    }
    print(json.dumps(result, indent=2))
    return 0 if refuted else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
