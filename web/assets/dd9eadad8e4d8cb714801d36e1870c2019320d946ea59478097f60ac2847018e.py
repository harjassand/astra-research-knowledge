#!/usr/bin/env python3
"""Exact Fraction replay for the sparse-positive-rate 3SAT reduction.

This checks support orders and the essential-source neutral/tie rule at a
supplied rational direction. The bounded UNSAT grid is a diagnostic only; the
all-direction implication is proved in HARDNESS.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable, Sequence


Vector = tuple[int, ...]
Direction = tuple[Fraction, ...]


@dataclass(frozen=True)
class Channel:
    name: str
    nu: Vector
    p_support: tuple[Vector, ...]
    q_support: tuple[Vector, ...]


def add(*vectors: Vector) -> Vector:
    if not vectors:
        return ()
    return tuple(sum(v[i] for v in vectors) for i in range(len(vectors[0])))


def unit(dimension: int, index: int, scale: int = 1) -> Vector:
    return tuple(scale if i == index else 0 for i in range(dimension))


def dot(a: Sequence[int], b: Sequence[Fraction]) -> Fraction:
    return sum((Fraction(x) * y for x, y in zip(a, b)), Fraction(0))


def build_instance(n: int, clauses: Sequence[Sequence[int]]) -> list[Channel]:
    """Build channels; literals are signed one-based variable indices."""
    if n < 1:
        raise ValueError("n must be positive")
    d = n + 1
    zidx = n
    zero = (0,) * d
    ez = unit(d, zidx)
    channels: list[Channel] = [Channel("target", ez, (zero,), (zero,))]

    for i in range(n):
        ei = unit(d, i)
        # P=u_i*z; Q=u_i^2+1. These supports yield tau=z-|u_i|.
        channels.append(Channel(f"variable[{i + 1}]", unit(d, zidx, -2),
                                (add(ez, ei),),
                                (unit(d, i, 2), zero)))

    for j, clause in enumerate(clauses, start=1):
        if len(clause) != 3:
            raise ValueError("the replay fixture expects 3-literal clauses")
        indices = [abs(lit) - 1 for lit in clause]
        if any(i < 0 or i >= n for i in indices):
            raise ValueError("literal index outside 1..n")
        if len(set(indices)) != 3:
            raise ValueError("each clause must use three distinct variables")
        base = add(*(unit(d, i) for i in indices))
        p_exp = add(base, ez)
        q_exps = tuple(add(base, unit(d, abs(lit) - 1,
                                            1 if lit > 0 else -1))
                         for lit in clause)
        nu = add(*(unit(d, abs(lit) - 1, 1 if lit > 0 else -1)
                   for lit in clause), unit(d, zidx, -3))
        channels.append(Channel(f"clause[{j}]", nu, (p_exp,), q_exps))

    for i in range(n):
        ei = unit(d, i)
        channels.append(Channel(f"guard_plus[{i + 1}]", unit(d, i, -1),
                                (ei,), (unit(d, zidx, 2),)))
        channels.append(Channel(f"guard_minus[{i + 1}]", ei,
                                (zero,), (add(ei, unit(d, zidx, 2)),)))
    return channels


def evaluate(channels: Sequence[Channel], direction: Iterable[int | Fraction]):
    w = tuple(Fraction(x) for x in direction)
    if not channels or any(len(c.nu) != len(w) for c in channels):
        raise ValueError("dimension mismatch")
    rows = []
    for c in channels:
        drift = dot(c.nu, w)
        tau = max(dot(a, w) for a in c.p_support) - max(
            dot(b, w) for b in c.q_support)
        rows.append({"name": c.name, "drift": drift, "tau": tau,
                     "active": drift != 0})
    active = [r for r in rows if r["active"]]
    if not active:
        return {"direction": w, "vacuous": True, "top": None,
                "maximizers": [], "outward_top": [], "rows": rows}
    top = max(r["tau"] for r in active)
    maximizers = [r["name"] for r in active if r["tau"] == top]
    outward_top = [r["name"] for r in active
                   if r["tau"] == top and r["drift"] > 0]
    return {"direction": w, "vacuous": False, "top": top,
            "maximizers": maximizers, "outward_top": outward_top,
            "rows": rows}


def all_3clauses(n: int) -> list[tuple[int, int, int]]:
    """All sign patterns of the one clause over variables 1,2,3."""
    if n != 3:
        raise ValueError("the UNSAT fixture uses three variables")
    return [tuple(sign * variable for variable, sign in enumerate(signs, start=1))
            for signs in product((1, -1), repeat=3)]


def finite_grid_diagnostic(channels: Sequence[Channel], radius: int = 2):
    d = len(channels[0].nu)
    seen = 0
    witnesses = []
    for coordinates in product(range(-radius, radius + 1), repeat=d):
        if all(x == 0 for x in coordinates):
            continue
        seen += 1
        result = evaluate(channels, coordinates)
        if result["outward_top"]:
            witnesses.append((coordinates, result["outward_top"]))
    return seen, witnesses


def main() -> None:
    sat = build_instance(3, [(1, 2, 3)])
    sat_result = evaluate(sat, (1, 1, -1, 1))
    assert sat_result["top"] == 0
    assert "target" in sat_result["outward_top"]
    assert "variable[1]" in sat_result["maximizers"]
    assert "clause[1]" in sat_result["maximizers"]
    assert "guard_plus[1]" not in sat_result["maximizers"]

    unsat = build_instance(3, all_3clauses(3))
    count, witnesses = finite_grid_diagnostic(unsat, radius=2)
    assert not witnesses

    # Check the zero-z guard slice at a direction where all literal channels
    # are active: the largest guard order is attained by an inward guard.
    zero_z = evaluate(unsat, (2, -1, 1, 0))
    assert zero_z["top"] == 2
    assert not zero_z["outward_top"]

    print("PASS: exact Fraction supports, orders, neutral exclusion, and ties")
    print(f"SAT witness: top={sat_result['top']}, "
          f"maximizers={sat_result['maximizers']}, "
          f"outward_top={sat_result['outward_top']}")
    print(f"UNSAT fixture: no outward-top witness on {count} nonzero integer "
          "directions in [-2,2]^4 (finite diagnostic only)")
    print(f"z=0 guard check: top={zero_z['top']}, "
          f"maximizers={zero_z['maximizers']}")


if __name__ == "__main__":
    main()
