#!/usr/bin/env python3
"""Independent exact checks for boundary cases in the c8 3SAT reduction.

These are finite rational diagnostics only. The all-directions implication is
proved algebraically in REPORT.md; this file is not used as its proof.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from typing import Sequence

Exp = tuple[int, ...]
Dir = tuple[F, ...]


@dataclass(frozen=True)
class Edge:
    name: str
    nu: Exp
    p_terms: tuple[Exp, ...]
    q_terms: tuple[Exp, ...]


def add(*xs: Exp) -> Exp:
    if not xs:
        return ()
    return tuple(sum(x[i] for x in xs) for i in range(len(xs[0])))


def unit(d: int, i: int, a: int = 1) -> Exp:
    return tuple(a if k == i else 0 for k in range(d))


def dot(a: Exp, w: Dir) -> F:
    return sum((F(x) * y for x, y in zip(a, w)), F(0))


def build(n: int, clauses: Sequence[Sequence[int]]) -> list[Edge]:
    """Literal indices are signed one-based; duplicate variables are allowed."""
    d, zi = n + 1, n
    ez, zero = unit(n + 1, zi), (0,) * (n + 1)
    edges = [Edge("T", ez, (zero,), (zero,))]
    for i in range(n):
        ei = unit(d, i)
        edges.append(Edge(f"V{i+1}", unit(d, zi, -2),
                          (add(ei, ez),), (unit(d, i, 2), zero)))
    for j, c in enumerate(clauses):
        if len(c) != 3 or any(abs(lit) > n or lit == 0 for lit in c):
            raise ValueError("expected three valid literal occurrences")
        ids = [abs(lit) - 1 for lit in c]
        base = add(*(unit(d, i) for i in ids))
        q = tuple(add(base, unit(d, abs(lit) - 1, 1 if lit > 0 else -1))
                  for lit in c)
        nu = add(*(unit(d, abs(lit) - 1, 1 if lit > 0 else -1) for lit in c),
                 unit(d, zi, -3))
        edges.append(Edge(f"C{j+1}", nu, (add(base, ez),), q))
    for i in range(n):
        ei = unit(d, i)
        edges.append(Edge(f"G+{i+1}", unit(d, i, -1), (ei,), (unit(d, zi, 2),)))
        edges.append(Edge(f"G-{i+1}", ei, (zero,), (add(ei, unit(d, zi, 2)),)))
    return edges


def check(edges: Sequence[Edge], w0: Sequence[int | F]):
    w = tuple(F(x) for x in w0)
    rows = []
    for e in edges:
        drift = dot(e.nu, w)
        tau = max(dot(a, w) for a in e.p_terms) - max(dot(b, w) for b in e.q_terms)
        rows.append((e.name, drift, tau))
    active = [r for r in rows if r[1] != 0]
    if not active:
        return w, rows, None, [], []
    top = max(r[2] for r in active)
    maximizers = [r[0] for r in active if r[2] == top]
    outward = [r[0] for r in active if r[2] == top and r[1] > 0]
    return w, rows, top, maximizers, outward


def validate_formulas(n: int, clauses: Sequence[Sequence[int]], w: Dir) -> None:
    """Cross-check support calculations against closed-form tau and drift."""
    rows = {name: (drift, tau) for name, drift, tau in check(build(n, clauses), w)[1]}
    u, z = w[:-1], w[-1]
    for i in range(n):
        assert rows[f"V{i+1}"][0] == -2 * z
        assert rows[f"V{i+1}"][1] == z - abs(u[i])
        assert rows[f"G+{i+1}"] == (-u[i], u[i] - 2 * z)
        assert rows[f"G-{i+1}"] == (u[i], -u[i] - 2 * z)
    for j, c in enumerate(clauses):
        signed = [F(1 if lit > 0 else -1) * u[abs(lit) - 1] for lit in c]
        assert rows[f"C{j+1}"][0] == sum(signed, F(0)) - 3 * z
        assert rows[f"C{j+1}"][1] == z - max(signed)


def main() -> None:
    # A satisfied clause with all three literals true is exactly neutral.
    sat = build(3, [(1, 2, 3)])
    w, rows, top, tops, outward = check(sat, (1, 1, 1, 1))
    assert top == 0 and "T" in outward and "C1" not in tops
    assert dict((n, (v, t)) for n, v, t in rows)["C1"] == (F(0), F(0))
    guards = {n: t for n, _, t in rows if n.startswith("G")}
    assert set(guards.values()) == {F(-1), F(-3)}

    # Repeated literals aggregate duplicate denominator exponents positively;
    # the support maximum still equals the occurrence-wise max formula.
    dup_sat = build(1, [(1, 1, 1)])
    c = next(e for e in dup_sat if e.name == "C1")
    assert len(c.q_terms) == 3 and len(set(c.q_terms)) == 1
    assert Counter(c.q_terms)[c.q_terms[0]] == 3  # aggregated coefficient 3
    _, rows, top, tops, outward = check(dup_sat, (1, 1))
    assert top == 0 and "T" in outward
    assert dict((n, (v, t)) for n, v, t in rows)["C1"] == (F(0), F(0))

    # The n=1 unsatisfiable duplicated-literal formula tests the all-directions
    # logic's occurrence-level formulation at exact rational sample points.
    dup_unsat = build(1, [(1, 1, 1), (-1, -1, -1)])
    for w in ((F(2, 3), F(1, 2)), (F(-2, 3), F(-1, 2)),
              (F(0), F(1, 3)), (F(1, 2), F(0))):
        validate_formulas(1, [(1, 1, 1), (-1, -1, -1)], w)
        _, _, _, _, out = check(dup_unsat, w)
        assert not out

    # The guard-completed z=0 slice and both signs of z on a 3-variable UNSAT
    # formula are checked with exact nonintegral directions.
    all_clauses = [tuple(s * i for i, s in zip((1, 2, 3), signs))
                   for signs in product((1, -1), repeat=3)]
    unsat = build(3, all_clauses)
    for w in ((F(2, 3), F(-1, 2), F(1, 7), F(3, 5)),
              (F(2, 3), F(-1, 2), F(1, 7), F(-3, 5)),
              (F(2, 3), F(-1, 2), F(1, 7), F(0))):
        validate_formulas(3, all_clauses, w)
        _, _, _, _, out = check(unsat, w)
        assert not out

    # Empty-variable/empty-clause SAT instance maps to just an outward target.
    trivial_sat = build(0, [])
    _, _, top, _, outward = check(trivial_sat, (F(2, 5),))
    assert top == 0 and outward == ["T"]
    _, _, top, _, _ = check(trivial_sat, (F(0),))
    assert top is None  # no active channel

    # Standard strong uses all sources: this UNSAT formula has only neutral
    # guards at global source order 2, while the weak active top is inward T.
    strong_w = (F(0), F(0), F(0), F(-1))
    _, rows, weak_top, weak_tops, weak_out = check(unsat, strong_w)
    global_top = max(t for _, _, t in rows)
    global_tops = [name for name, _, tau in rows if tau == global_top]
    assert weak_top == 0 and "T" in weak_tops and not weak_out
    assert global_top == 2 and all(name.startswith("G") for name in global_tops)
    assert all(drift == 0 for name, drift, _ in rows if name in global_tops)

    print("PASS: exact Fraction support orders and reaction projections")
    print("PASS: all-true clause is neutral; target remains an outward active top tie")
    print("PASS: duplicate-literal denominator support aggregates with positive coefficient 3")
    print("PASS: n=1 duplicated-clause and n=0 empty-formula boundary fixtures")
    print("PASS: rational directions checked in z>0, z<0, z=0 slices")
    print("PASS: weak/standard-strong distinction at the neutral global source face")


if __name__ == "__main__":
    main()
