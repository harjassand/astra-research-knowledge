#!/usr/bin/env python3
"""Exact verifier for a rational counterdirection to positive-rational endotacticity.

Input JSON format:
{
  "edges": [
    {"name": "e1", "nu": ["1", "0"],
     "P": [["0", "0"], ["1/2", "0"]],
     "Q": [["0", "0"]]}
  ],
  "direction": ["1", "0"]
}

Every vector entry is an integer or rational string. Positive polynomial
coefficients are intentionally omitted: for this structural test, only their
nonempty supports matter. A successful verification prints the exact active
minimum and offending minimum-tied labels, then exits 0. A direction that does
not refute endotacticity exits 1. This checks a supplied certificate; it is not
an all-directions recognizer.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Any


Vector = tuple[F, ...]


def vector(raw: list[Any]) -> Vector:
    return tuple(F(str(x)) for x in raw)


def dot(a: Vector, b: Vector) -> F:
    return sum((x * y for x, y in zip(a, b)), F(0))


@dataclass(frozen=True)
class Edge:
    name: str
    nu: Vector
    P: tuple[Vector, ...]
    Q: tuple[Vector, ...]


def parse(data: dict[str, Any]) -> tuple[list[Edge], Vector]:
    if not isinstance(data, dict) or not data.get("edges"):
        raise ValueError("input must contain a nonempty edges list")
    edges: list[Edge] = []
    for j, raw in enumerate(data["edges"]):
        name = str(raw.get("name", f"e{j}"))
        nu = vector(raw["nu"])
        P = tuple(vector(a) for a in raw["P"])
        Q = tuple(vector(b) for b in raw["Q"])
        if not P or not Q:
            raise ValueError(f"{name}: numerator and denominator supports must be nonempty")
        if any(len(v) != len(nu) for v in (*P, *Q)):
            raise ValueError(f"{name}: vector dimensions differ")
        if len(set(P)) != len(P) or len(set(Q)) != len(Q):
            raise ValueError(f"{name}: collect duplicate support exponents before verification")
        edges.append(Edge(name, nu, P, Q))
    d = len(edges[0].nu)
    if d == 0 or any(len(e.nu) != d for e in edges):
        raise ValueError("all jumps and support exponents must have one common positive dimension")
    r = vector(data["direction"])
    if len(r) != d:
        raise ValueError("direction dimension differs from the edge dimension")
    return edges, r


def evaluate(edges: list[Edge], r: Vector) -> dict[str, Any]:
    active: list[tuple[Edge, F, F]] = []
    for edge in edges:
        projected_jump = dot(r, edge.nu)
        if projected_jump == 0:
            continue  # Neutral channels are excluded before minimizing tau.
        tau = min(dot(r, a) for a in edge.P) - min(dot(r, b) for b in edge.Q)
        active.append((edge, projected_jump, tau))
    if not active:
        return {"vacuous": True, "bad": [], "minimum_tau": None, "active": []}
    minimum_tau = min(tau for _, _, tau in active)
    bad = [edge.name for edge, projected_jump, tau in active
           if tau == minimum_tau and projected_jump < 0]
    return {
        "vacuous": False,
        "bad": bad,
        "minimum_tau": minimum_tau,
        "active": [
            {"name": edge.name, "r_dot_nu": projected_jump, "tau": tau,
             "minimum_tied": tau == minimum_tau}
            for edge, projected_jump, tau in active
        ],
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} INPUT.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text())
        edges, r = parse(data)
        result = evaluate(edges, r)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    if result["vacuous"]:
        print("NOT A COUNTEREXAMPLE: every channel is neutral in this direction")
        return 1
    tau = result["minimum_tau"]
    print(f"active minimum tau = {tau}")
    for row in result["active"]:
        print(f"{row['name']}: r.nu={row['r_dot_nu']}, tau={row['tau']}, "
              f"minimum_tied={row['minimum_tied']}")
    if result["bad"]:
        print("VERIFIED COUNTEREXAMPLE: outward minimum-tied labels = "
              + ", ".join(result["bad"]))
        return 0
    print("NOT A COUNTEREXAMPLE: every active minimum-tied label has r.nu > 0")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
